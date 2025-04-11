"""
Sequential thinking tools for managing thought chains and context in ChromaDB.
"""

import time
import uuid
import json
import logging

from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict

from mcp import types
from mcp.shared.exceptions import McpError
from mcp.types import ErrorData, INVALID_PARAMS, INTERNAL_ERROR
from pydantic import BaseModel, Field, field_validator

# Import InvalidDimensionException
from chromadb.errors import InvalidDimensionException

from ..types import ThoughtMetadata
from ..utils import (
    get_logger,
    get_chroma_client,
    get_embedding_function,
    ValidationError,
)

# Constants
THOUGHTS_COLLECTION = "sequential_thoughts_v1"
SESSIONS_COLLECTION = "thinking_sessions"
DEFAULT_SIMILARITY_THRESHOLD = 0.75


@dataclass
class ThoughtMetadata:
    """Metadata structure for thoughts."""

    session_id: str
    thought_number: int
    total_thoughts: int
    timestamp: int
    branch_from_thought: Optional[int] = None
    branch_id: Optional[str] = None
    next_thought_needed: bool = False
    custom_data: Optional[Dict[str, Any]] = None


# Get logger instance for this module
# logger = get_logger("tools.thinking")

# --- Pydantic Input Models for Thinking Tools ---


class SequentialThinkingInput(BaseModel):
    thought: str = Field(description="Content of the thought being recorded.")
    thought_number: int = Field(gt=0, description="Sequential number of this thought (must be > 0).")
    total_thoughts: int = Field(description="Total anticipated number of thoughts in this sequence.")
    session_id: Optional[str] = Field(
        default=None, description="Unique session ID. If None, a new session ID is generated."
    )
    branch_id: Optional[str] = Field(default=None, description="Optional identifier for a branch within the session.")
    branch_from_thought: Optional[int] = Field(
        default=None, gt=0, description="If creating a new branch, the parent thought number (> 0) it originates from."
    )
    next_thought_needed: Optional[bool] = Field(
        default=False, description="Flag indicating if a subsequent thought is expected."
    )
    custom_data: Optional[Dict[str, Any]] = Field(
        default=None, description="Optional dictionary for arbitrary metadata."
    )


class FindSimilarThoughtsInput(BaseModel):
    query: str = Field(description="Text to search for similar thoughts.")
    session_id: Optional[str] = Field(default=None, description="If provided, limits search to this session.")
    n_results: Optional[int] = Field(
        default=5, ge=1, description="Maximum number of similar thoughts to return (must be >= 1)."
    )
    threshold: Optional[float] = Field(
        default=None, description="Optional minimum similarity score (distance threshold, lower is more similar)."
    )
    include_branches: Optional[bool] = Field(
        default=True, description="Whether to include thoughts from branches in the search."
    )


class GetSessionSummaryInput(BaseModel):
    session_id: str = Field(description="The unique identifier for the thinking session to summarize.")
    include_branches: Optional[bool] = Field(
        default=True, description="Whether to include thoughts from branches in the summary."
    )


class FindSimilarSessionsInput(BaseModel):
    query: str = Field(description="Text to search for similar thinking sessions based on overall content.")
    n_results: Optional[int] = Field(
        default=5, ge=1, description="Maximum number of similar sessions to return (must be >= 1)."
    )
    threshold: Optional[float] = Field(
        default=None, description="Optional minimum similarity score (distance threshold, lower is more similar)."
    )


# --- End Pydantic Input Models ---

# --- Implementation Functions ---


async def _sequential_thinking_impl(input_data: SequentialThinkingInput) -> types.CallToolResult:
    """Records a thought within a thinking session, potentially in a branch.

    Args:
        input_data: A SequentialThinkingInput object containing validated arguments.

    Returns:
        A CallToolResult object.
        On success, content contains a TextContent object with a JSON string
        including the 'session_id' (either provided or newly generated) and potentially
        the ID of the recorded thought document.
        On error (e.g., invalid parameters, database error, unexpected issue),
        isError is True and content contains a TextContent object with an error message.
    """

    logger = get_logger("tools.thinking")
    try:
        # Access validated data from input model
        thought = input_data.thought
        thought_number = input_data.thought_number
        total_thoughts = input_data.total_thoughts
        session_id = input_data.session_id  # Could be None
        branch_id = input_data.branch_id  # Could be None
        branch_from_thought = input_data.branch_from_thought  # Could be None
        next_thought_needed = input_data.next_thought_needed  # Has default
        custom_data = input_data.custom_data  # Could be None

        effective_session_id = session_id if session_id else str(uuid.uuid4())
        timestamp = int(time.time())
        metadata = ThoughtMetadata(
            session_id=effective_session_id,
            thought_number=thought_number,
            total_thoughts=total_thoughts,
            timestamp=timestamp,
            branch_from_thought=branch_from_thought,
            branch_id=branch_id,
            next_thought_needed=next_thought_needed,
            custom_data=custom_data if custom_data else None,
        )

        client = get_chroma_client()

        try:
            collection = client.get_or_create_collection(
                name=THOUGHTS_COLLECTION, embedding_function=get_embedding_function()
            )
        except Exception as e:
            logger.error(f"Error getting/creating collection '{THOUGHTS_COLLECTION}': {e}", exc_info=True)
            return types.CallToolResult(
                isError=True,
                content=[
                    types.TextContent(
                        type="text", text=f"ChromaDB Error accessing collection '{THOUGHTS_COLLECTION}': {str(e)}"
                    )
                ],
            )

        thought_id = f"thought_{effective_session_id}_{thought_number}"
        if branch_id:
            thought_id += f"_branch_{branch_id}"

        metadata_dict = asdict(metadata)
        metadata_dict = {k: v for k, v in metadata_dict.items() if v is not None}
        if "custom_data" in metadata_dict:  # Check existence before popping
            custom = metadata_dict.pop("custom_data")
            if custom:  # Check if custom data is not empty
                for ck, cv in custom.items():
                    metadata_dict[f"custom:{ck}"] = cv

        try:
            collection.add(documents=[thought], metadatas=[metadata_dict], ids=[thought_id])
        except (ValueError, InvalidDimensionException) as e:
            logger.error(f"Error adding thought to collection '{THOUGHTS_COLLECTION}': {e}", exc_info=True)
            return types.CallToolResult(
                isError=True, content=[types.TextContent(type="text", text=f"ChromaDB Error adding thought: {str(e)}")]
            )

        previous_thoughts = []
        if thought_number > 1:
            # Use $and for multiple conditions
            where_clause = {"$and": [{"session_id": effective_session_id}, {"thought_number": {"$lt": thought_number}}]}

            try:
                results = collection.get(
                    where=where_clause,
                    include=["documents", "metadatas"],
                )

                if results and results.get("ids"):
                    thought_data = []
                    for i in range(len(results["ids"])):
                        raw_meta = results["metadatas"][i] or {}
                        reconstructed_custom = {
                            k[len("custom:") :]: v for k, v in raw_meta.items() if k.startswith("custom:")
                        }
                        base_meta = {k: v for k, v in raw_meta.items() if not k.startswith("custom:")}
                        if reconstructed_custom:
                            base_meta["custom_data"] = reconstructed_custom

                        thought_data.append(
                            {
                                "id": results["ids"][i],
                                "content": results["documents"][i],
                                "metadata": base_meta,
                                "thought_number_sort_key": base_meta.get("thought_number", 999999),
                            }
                        )

                    sorted_thoughts = sorted(thought_data, key=lambda x: x["thought_number_sort_key"])

                    previous_thoughts = [
                        {k: v for k, v in thought.items() if k != "thought_number_sort_key"}
                        for thought in sorted_thoughts
                    ]

            except ValueError as e:
                logger.error(
                    f"Error retrieving previous thoughts for session '{effective_session_id}': {e}", exc_info=True
                )
                previous_thoughts = []

        logger.info(f"Recorded thought {thought_number}/{total_thoughts} for session {effective_session_id}")

        result_data = {
            "status": "success",
            "thought_id": thought_id,
            "session_id": effective_session_id,
            "thought_number": thought_number,
            "total_thoughts": total_thoughts,
            "previous_thoughts": previous_thoughts,
            "next_thought_needed": next_thought_needed,
        }
        result_json = json.dumps(result_data, indent=2)
        return types.CallToolResult(content=[types.TextContent(type="text", text=result_json)])

    except ValidationError as e:
        logger.warning(f"Validation error recording thought for session '{session_id or '(new)'}': {e}")
        return types.CallToolResult(
            isError=True, content=[types.TextContent(type="text", text=f"Validation Error: {str(e)}")]
        )
    except Exception as e:
        logger.error(f"Unexpected error recording thought for session '{session_id or '(new)'}': {e}", exc_info=True)
        return types.CallToolResult(
            isError=True,
            content=[
                types.TextContent(
                    type="text",
                    text=f"Tool Error: An unexpected error occurred while recording thought. Details: {str(e)}",
                )
            ],
        )


async def _find_similar_thoughts_impl(input_data: FindSimilarThoughtsInput) -> types.CallToolResult:
    """Performs a semantic search for similar thoughts.

    Args:
        input_data: A FindSimilarThoughtsInput object containing validated arguments.

    Returns:
        A CallToolResult object.
        On success, content contains a TextContent object with a JSON string representing
        the query results (similar to ChromaDB query results, including lists for ids,
        documents/thoughts, metadatas, distances).
        On error (e.g., invalid parameters, collection not found, unexpected issue),
        isError is True and content contains a TextContent object with an error message.
    """

    logger = get_logger("tools.thinking")
    try:
        # Access validated data
        query = input_data.query
        session_id = input_data.session_id
        n_results = input_data.n_results  # Has default
        threshold = input_data.threshold
        include_branches = input_data.include_branches  # Has default

        # Use default threshold if None is passed (moved handling here)
        if threshold is None:
            threshold = DEFAULT_SIMILARITY_THRESHOLD

        client = get_chroma_client()

        # Get collection, handle not found specifically
        try:
            collection = client.get_collection(name=THOUGHTS_COLLECTION, embedding_function=get_embedding_function())
        except ValueError as e:
            if f"Collection {THOUGHTS_COLLECTION} does not exist." in str(e):
                logger.warning(f"Cannot find similar thoughts: Collection '{THOUGHTS_COLLECTION}' not found.")
                # Return success with empty results, indicating collection doesn't exist
                return types.CallToolResult(
                    content=[
                        types.TextContent(
                            type="text",
                            text=json.dumps(
                                {
                                    "similar_thoughts": [],
                                    "total_found": 0,
                                    "threshold_used": threshold,
                                    "message": f"Collection '{THOUGHTS_COLLECTION}' not found.",
                                },
                                indent=2,
                            ),
                        )
                    ]
                )
            else:
                raise e  # Re-raise other ValueErrors
        except Exception as e:  # Catch other potential errors during get_collection
            logger.error(f"Error getting collection '{THOUGHTS_COLLECTION}' for query: {e}", exc_info=True)
            return types.CallToolResult(
                isError=True,
                content=[
                    types.TextContent(
                        type="text", text=f"ChromaDB Error accessing collection '{THOUGHTS_COLLECTION}': {str(e)}"
                    )
                ],
            )

        # Prepare where clause if session_id is provided
        where_clause = None
        if session_id:
            where_clause = {"session_id": session_id}
            # TODO: Add branch filtering logic if needed based on include_branches

        # Perform query, handle errors
        try:
            results = collection.query(
                query_texts=[query],
                n_results=n_results,
                where=where_clause,
                include=["documents", "metadatas", "distances"],
            )
        except ValueError as e:  # Catch query-specific errors
            logger.error(f"Error querying thoughts collection '{THOUGHTS_COLLECTION}': {e}", exc_info=True)
            return types.CallToolResult(
                isError=True, content=[types.TextContent(type="text", text=f"ChromaDB Query Error: {str(e)}")]
            )

        # Process results and filter by threshold
        similar_thoughts = []
        if results and results.get("ids") and results["ids"][0]:
            for i in range(len(results["ids"][0])):
                distance = results["distances"][0][i]
                similarity = 1.0 - distance  # Ensure float calculation

                if similarity >= threshold:
                    raw_meta = results["metadatas"][0][i] or {}
                    # Reconstruct custom data
                    reconstructed_custom = {
                        k[len("custom:") :]: v for k, v in raw_meta.items() if k.startswith("custom:")
                    }
                    base_meta = {k: v for k, v in raw_meta.items() if not k.startswith("custom:")}
                    if reconstructed_custom:
                        base_meta["custom_data"] = reconstructed_custom

                    thought = {
                        "id": results["ids"][0][i],  # Include ID
                        "content": results["documents"][0][i],
                        "metadata": base_meta,
                        "similarity": similarity,
                    }
                    similar_thoughts.append(thought)

        # Success result
        result_data = {
            "similar_thoughts": similar_thoughts,
            "total_found": len(similar_thoughts),
            "threshold_used": threshold,
        }
        result_json = json.dumps(result_data, indent=2)
        return types.CallToolResult(content=[types.TextContent(type="text", text=result_json)])

    except ValueError as e:  # Catch ValueErrors re-raised from get_collection
        logger.error(f"Value error accessing collection '{THOUGHTS_COLLECTION}' for query: {e}", exc_info=False)
        # This path should likely not be hit due to specific handling above, but acts as a fallback
        return types.CallToolResult(
            isError=True,
            content=[types.TextContent(type="text", text=f"ChromaDB Value Error accessing collection: {str(e)}")],
        )
    except Exception as e:
        logger.error(f"Unexpected error finding similar thoughts: {e}", exc_info=True)
        return types.CallToolResult(
            isError=True,
            content=[
                types.TextContent(
                    type="text",
                    text=f"Tool Error: An unexpected error occurred while finding similar thoughts. Details: {str(e)}",
                )
            ],
        )


async def _get_session_summary_impl(input_data: GetSessionSummaryInput) -> types.CallToolResult:
    """Fetches all thoughts belonging to a specific session.

    Args:
        input_data: A GetSessionSummaryInput object containing validated arguments.

    Returns:
        A CallToolResult object.
        On success, content contains a TextContent object with a JSON string containing
        a list of thoughts (documents/metadata), ordered sequentially by thought_number
        (and potentially by branch structure if included).
        On error (e.g., session not found, database error, unexpected issue),
        isError is True and content contains a TextContent object with an error message.
    """

    logger = get_logger("tools.thinking")
    try:
        # Access validated data
        session_id = input_data.session_id
        include_branches = input_data.include_branches  # Has default

        client = get_chroma_client()

        # Get collection, handle not found
        try:
            collection = client.get_collection(name=THOUGHTS_COLLECTION, embedding_function=get_embedding_function())
        except ValueError as e:
            if f"Collection {THOUGHTS_COLLECTION} does not exist." in str(e):
                logger.warning(f"Cannot get session summary: Collection '{THOUGHTS_COLLECTION}' not found.")
                # Return success with empty results
                return types.CallToolResult(
                    content=[
                        types.TextContent(
                            type="text",
                            text=json.dumps(
                                {
                                    "session_id": session_id,
                                    "session_thoughts": [],
                                    "total_thoughts_in_session": 0,
                                    "message": f"Collection '{THOUGHTS_COLLECTION}' not found.",
                                },
                                indent=2,
                            ),
                        )
                    ]
                )
            else:
                raise e  # Re-raise other ValueErrors
        except Exception as e:  # Catch other potential errors during get_collection
            logger.error(f"Error getting collection '{THOUGHTS_COLLECTION}' for session summary: {e}", exc_info=True)
            return types.CallToolResult(
                isError=True, content=[types.TextContent(type="text", text=f"ChromaDB Error: {str(e)}")]
            )

        # Apply filtering based on effective_include_branches if needed
        where_clause = {"session_id": session_id}
        if not include_branches:
            # Modify where_clause to exclude branches, e.g. check if branch_id is null/absent
            # Example (exact field depends on storage): where_clause["branch_id"] = None
            # This might need $and: [{"session_id": ...}, {"branch_id": None}] depending on DB
            pass  # Placeholder - Add actual branch exclusion logic here if needed

        # Get thoughts, handle errors
        try:
            results = collection.get(where=where_clause, include=["documents", "metadatas", "ids"])  # Include IDs
        except ValueError as e:  # Catch errors from get (e.g., bad filter)
            logger.error(f"Error getting thoughts for session '{session_id}': {e}", exc_info=True)
            return types.CallToolResult(
                isError=True, content=[types.TextContent(type="text", text=f"ChromaDB Get Error: {str(e)}")]
            )

        # Process and sort results
        session_thoughts = []
        if results and results.get("ids"):
            thought_data = []
            for i in range(len(results["ids"])):
                raw_meta = results["metadatas"][i] or {}
                # Reconstruct custom data
                reconstructed_custom = {k[len("custom:") :]: v for k, v in raw_meta.items() if k.startswith("custom:")}
                base_meta = {k: v for k, v in raw_meta.items() if not k.startswith("custom:")}
                if reconstructed_custom:
                    base_meta["custom_data"] = reconstructed_custom

                thought_data.append(
                    {
                        "id": results["ids"][i],  # Include ID
                        "content": results["documents"][i],
                        "metadata": base_meta,
                        "thought_number_sort_key": base_meta.get("thought_number", 999999),  # Temp key for sorting
                    }
                )

            # Sort based on thought_number
            sorted_thoughts = sorted(thought_data, key=lambda x: x["thought_number_sort_key"])

            # Final list without the sort key
            session_thoughts = [
                {k: v for k, v in thought.items() if k != "thought_number_sort_key"} for thought in sorted_thoughts
            ]

        # Success result
        result_data = {
            "session_id": session_id,
            "session_thoughts": session_thoughts,
            "total_thoughts_in_session": len(session_thoughts),
        }
        result_json = json.dumps(result_data, indent=2)
        return types.CallToolResult(content=[types.TextContent(type="text", text=result_json)])

    except ValueError as e:  # Catch ValueErrors re-raised from get_collection
        logger.error(
            f"Value error accessing collection '{THOUGHTS_COLLECTION}' for session summary: {e}", exc_info=False
        )
        return types.CallToolResult(
            isError=True,
            content=[types.TextContent(type="text", text=f"ChromaDB Value Error accessing collection: {str(e)}")],
        )
    except Exception as e:
        logger.error(f"Unexpected error getting session summary for '{session_id}': {e}", exc_info=True)
        return types.CallToolResult(
            isError=True,
            content=[
                types.TextContent(
                    type="text",
                    text=f"Tool Error: An unexpected error occurred while getting session summary for '{session_id}'. Details: {str(e)}",
                )
            ],
        )


async def _find_similar_sessions_impl(input_data: FindSimilarSessionsInput) -> types.CallToolResult:
    """Performs a semantic search for sessions similar to the query.

    (Note: This functionality might require pre-calculating session embeddings
     or performing aggregation queries, depending on the implementation.)

    Args:
        input_data: A FindSimilarSessionsInput object containing validated arguments.

    Returns:
        A CallToolResult object.
        On success, content contains a TextContent object with a JSON string listing
        similar session IDs and potentially their similarity scores.
        On error (e.g., supporting collection/index not found, invalid query,
        unexpected issue), isError is True and content contains a TextContent
        object with an error message.
    """

    logger = get_logger("tools.thinking")
    try:
        # Access validated data
        query = input_data.query
        n_results = input_data.n_results  # Has default
        threshold = input_data.threshold

        # Use default threshold if None is passed (moved handling here)
        if threshold is None:
            threshold = DEFAULT_SIMILARITY_THRESHOLD

        client = get_chroma_client()

        # --- Step 1: Get all unique session IDs from the thoughts collection ---
        thoughts_collection = None
        all_session_ids = set()
        try:
            thoughts_collection = client.get_collection(
                name=THOUGHTS_COLLECTION, embedding_function=get_embedding_function()
            )
            # Efficiently get all unique session_ids from metadata
            # This might be slow for very large collections, consider optimization if needed
            all_metadata = thoughts_collection.get(include=["metadatas"])
            if all_metadata and all_metadata.get("metadatas"):
                for meta in all_metadata["metadatas"]:
                    if meta and "session_id" in meta:
                        all_session_ids.add(meta["session_id"])
        except ValueError as e:
            if f"Collection {THOUGHTS_COLLECTION} does not exist." in str(e):
                logger.warning(f"Cannot find similar sessions: Collection '{THOUGHTS_COLLECTION}' not found.")
                # Return empty result if thoughts collection is missing
                return types.CallToolResult(
                    content=[
                        types.TextContent(
                            type="text",
                            text=json.dumps(
                                {"similar_sessions": [], "total_found": 0, "threshold_used": threshold}, indent=2
                            ),
                        )
                    ]
                )
            else:
                raise e  # Re-raise other ValueErrors
        except Exception as e:
            logger.error(f"Error accessing thoughts collection '{THOUGHTS_COLLECTION}': {e}", exc_info=True)
            return types.CallToolResult(
                isError=True,
                content=[
                    types.TextContent(type="text", text=f"ChromaDB Error accessing thoughts collection: {str(e)}")
                ],
            )

        if not all_session_ids:
            logger.info("No sessions found in the thoughts collection.")
            return types.CallToolResult(
                content=[
                    types.TextContent(
                        type="text",
                        text=json.dumps(
                            {"similar_sessions": [], "total_found": 0, "threshold_used": threshold}, indent=2
                        ),
                    )
                ]
            )

        # --- Step 2: Create/Get Sessions Collection and Embed Session Summaries ---
        sessions_collection = None
        try:
            # Try getting the sessions collection
            sessions_collection = client.get_collection(
                name=SESSIONS_COLLECTION, embedding_function=get_embedding_function()
            )
        except ValueError as e:
            # Handle case where SESSIONS_COLLECTION specifically does not exist
            if f"Collection {SESSIONS_COLLECTION} does not exist." in str(e):
                logger.warning(f"Cannot find similar sessions: Required collection '{SESSIONS_COLLECTION}' not found.")
                return types.CallToolResult(
                    isError=True,
                    content=[
                        types.TextContent(type="text", text=f"Tool Error: Collection '{SESSIONS_COLLECTION}' not found")
                    ],
                )
            else:
                # Re-raise other ValueErrors to be caught by the general exception handler below
                raise e
        except Exception as e:
            # Catch other errors during get_collection (non-ValueError)
            logger.error(f"Error accessing sessions collection '{SESSIONS_COLLECTION}': {e}", exc_info=True)
            return types.CallToolResult(
                isError=True,
                content=[types.TextContent(type="text", text=f"ChromaDB Error accessing sessions collection: {str(e)}")],
            )

        # If collection exists, proceed with embedding and adding summaries
        try:
            # Embed summaries for sessions not already in the sessions collection
            existing_session_ids = set(sessions_collection.get().get("ids", []))
            sessions_to_embed = []
            ids_to_embed = []

            for session_id in all_session_ids:
                if session_id not in existing_session_ids:
                    # Get session summary (needs await)
                    summary_result = await _get_session_summary_impl(GetSessionSummaryInput(session_id=session_id))
                    # Check if the internal call succeeded
                    if not summary_result.isError:
                        # Safely parse the JSON content
                        try:
                            summary_data = json.loads(summary_result.content[0].text)
                            summary_text = " ".join(
                                [t.get("content", "") for t in summary_data.get("session_thoughts", [])]
                            )
                            if summary_text:  # Only embed if there's content
                                sessions_to_embed.append(summary_text)
                                ids_to_embed.append(session_id)
                        except (json.JSONDecodeError, IndexError, AttributeError) as parse_error:
                            logger.warning(f"Could not parse summary result for session '{session_id}': {parse_error}")
                    else:
                        logger.warning(
                            f"Failed to get summary for session '{session_id}' to embed: {summary_result.content[0].text if summary_result.content else 'Unknown error'}"
                        )

            if sessions_to_embed:
                logger.info(f"Embedding summaries for {len(sessions_to_embed)} new/updated sessions.")
                sessions_collection.add(documents=sessions_to_embed, ids=ids_to_embed)

        except Exception as e:
            # Catch errors during the embedding/adding process
            logger.error(f"Error embedding/adding to sessions collection '{SESSIONS_COLLECTION}': {e}", exc_info=True)
            return types.CallToolResult(
                isError=True, content=[types.TextContent(type="text", text=f"ChromaDB Error updating sessions: {str(e)}")]
            )

        # --- Step 3: Query the Sessions Collection ---
        similar_sessions = []
        if sessions_collection:  # Ensure collection was accessed successfully
            try:
                query_results = sessions_collection.query(
                    query_texts=[query],
                    n_results=n_results,
                    include=["metadatas", "distances"],  # Only need distance and ID (implicit)
                )

                if query_results and query_results.get("ids") and query_results["ids"][0]:
                    for i in range(len(query_results["ids"][0])):
                        session_id = query_results["ids"][0][i]
                        distance = query_results["distances"][0][i]
                        similarity = 1.0 - distance

                        if similarity >= threshold:
                            # Fetch the full summary details again for the result
                            # This is slightly inefficient but ensures fresh data
                            summary_result = await _get_session_summary_impl(
                                GetSessionSummaryInput(session_id=session_id)
                            )
                            if not summary_result.isError:
                                try:
                                    summary_data = json.loads(summary_result.content[0].text)
                                    summary_data["similarity_score"] = similarity  # Add score
                                    similar_sessions.append(summary_data)
                                except (json.JSONDecodeError, IndexError, AttributeError) as parse_error:
                                    logger.warning(
                                        f"Could not parse final summary result for session '{session_id}': {parse_error}"
                                    )
                            else:
                                logger.warning(
                                    f"Failed to get final summary for session '{session_id}': {summary_result.content[0].text if summary_result.content else 'Unknown error'}"
                                )
            except ValueError as e:
                logger.error(f"Error querying sessions collection '{SESSIONS_COLLECTION}': {e}", exc_info=True)
                return types.CallToolResult(
                    isError=True,
                    content=[types.TextContent(type="text", text=f"ChromaDB Query Error on sessions: {str(e)}")],
                )

        # Success result
        result_data = {
            "similar_sessions": similar_sessions,
            "total_found": len(similar_sessions),
            "threshold_used": threshold,
        }
        result_json = json.dumps(result_data, indent=2)
        return types.CallToolResult(content=[types.TextContent(type="text", text=result_json)])

    except ValueError as e:  # Catch ValueErrors re-raised from get_collection (thoughts)
        logger.error(f"Value error accessing thoughts collection '{THOUGHTS_COLLECTION}': {e}", exc_info=False)
        return types.CallToolResult(
            isError=True,
            content=[
                types.TextContent(type="text", text=f"ChromaDB Value Error accessing thoughts collection: {str(e)}")
            ],
        )
    except Exception as e:
        logger.error(f"Unexpected error finding similar sessions: {e}", exc_info=True)
        return types.CallToolResult(
            isError=True,
            content=[
                types.TextContent(
                    type="text",
                    text=f"Tool Error: An unexpected error occurred while finding similar sessions. Details: {str(e)}",
                )
            ],
        )


# Ensure mcp instance is imported/available for decorators
