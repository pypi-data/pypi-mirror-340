"""
Document management tools for ChromaDB operations.
"""

import time
import json
import logging

from typing import Dict, List, Optional, Any, Union, cast
from dataclasses import dataclass

from mcp import types
from mcp.shared.exceptions import McpError
from mcp.types import ErrorData, INVALID_PARAMS, INTERNAL_ERROR
from pydantic import BaseModel, Field, field_validator  # Import Pydantic

# Use relative imports
from ..utils.errors import ValidationError
from ..types import DocumentMetadata

from chromadb.errors import InvalidDimensionException

# --- Imports ---
import chromadb
import chromadb.errors as chroma_errors
from ..utils import (
    get_logger,
    get_chroma_client,
    get_embedding_function,
    ValidationError,
)

# REMOVE invalid validation imports
# from ..utils.validation import validate_collection_name, validate_document_ids, validate_metadata
# REMOVE invalid error imports (commented out or non-existent)
# from ..utils.errors import handle_chroma_error, is_collection_not_found_error, CollectionNotFoundError
# REMOVE invalid helper imports
# from ..utils.helpers import (
#     dict_to_text_content,
#     prepare_metadata_for_chroma,
#     process_chroma_results,
#     format_add_result,
#     format_update_result,
#     format_delete_result,
#     MAX_DOC_LENGTH_FOR_PEEK
# )

# --- Constants ---
# Existing constants...
DEFAULT_QUERY_N_RESULTS = 10

# Get logger instance for this module
logger = get_logger("tools.document")

# --- Pydantic Input Models for Document Tools ---


class AddDocumentsInput(BaseModel):
    collection_name: str = Field(description="Name of the collection to add documents to.")
    documents: List[str] = Field(description="List of document contents (strings).")
    ids: Optional[List[str]] = Field(
        default=None, description="Optional list of unique IDs. If None, IDs are generated."
    )
    metadatas: Optional[List[Dict[str, Any]]] = Field(
        default=None, description="Optional list of metadata dictionaries."
    )
    increment_index: Optional[bool] = Field(default=True, description="Whether to immediately index added documents.")

    # TODO: Consider adding validators to ensure lists (if provided) match document count?
    # Pydantic can do this, but it adds complexity. Current impl checks this.


class QueryDocumentsInput(BaseModel):
    collection_name: str = Field(description="Name of the collection to query.")
    query_texts: List[str] = Field(description="List of query strings for semantic search.")
    n_results: Optional[int] = Field(default=10, ge=1, description="Number of results per query.")
    where: Optional[Dict[str, Any]] = Field(default=None, description="Metadata filter (e.g., {'source': 'pdf'}).")
    where_document: Optional[Dict[str, Any]] = Field(
        default=None, description="Document content filter (e.g., {'$contains': 'keyword'})."
    )
    include: Optional[List[str]] = Field(
        default=None, description="Fields to include (documents, metadatas, distances). Defaults to ChromaDB standard."
    )

    # TODO: Add validator for 'include' list contents?
    # Current impl checks this.


class GetDocumentsInput(BaseModel):
    collection_name: str = Field(description="Name of the collection to get documents from.")
    ids: Optional[List[str]] = Field(default=None, description="List of document IDs to retrieve.")
    where: Optional[Dict[str, Any]] = Field(default=None, description="Metadata filter.")
    where_document: Optional[Dict[str, Any]] = Field(default=None, description="Document content filter.")
    limit: Optional[int] = Field(default=None, ge=1, description="Maximum number of documents to return.")
    offset: Optional[int] = Field(default=None, ge=0, description="Number of documents to skip.")
    include: Optional[List[str]] = Field(default=None, description="Fields to include.")

    # Note: Logically, at least one of ids, where, or where_document should be provided for a targeted get.
    # A Pydantic root_validator could enforce this, but is omitted for simplicity for now.


class UpdateDocumentsInput(BaseModel):
    collection_name: str = Field(description="Name of the collection to update documents in.")
    ids: List[str] = Field(description="List of document IDs to update.")
    documents: Optional[List[str]] = Field(default=None, description="Optional new list of document contents.")
    metadatas: Optional[List[Dict[str, Any]]] = Field(
        default=None, description="Optional new list of metadata dictionaries."
    )

    # Note: Logically, at least one of documents or metadatas must be provided.
    # A Pydantic root_validator could enforce this.
    # TODO: Consider adding validators to ensure lists (if provided) match ID count?


class DeleteDocumentsInput(BaseModel):
    collection_name: str = Field(description="Name of the collection to delete documents from.")
    ids: Optional[List[str]] = Field(default=None, description="List of document IDs to delete.")
    where: Optional[Dict[str, Any]] = Field(default=None, description="Metadata filter for deletion.")
    where_document: Optional[Dict[str, Any]] = Field(default=None, description="Document content filter for deletion.")

    # Note: Logically, at least one of ids, where, or where_document must be provided.
    # A Pydantic root_validator could enforce this.


# --- End Pydantic Input Models ---

# --- Implementation Functions ---


# Signature changed to accept Pydantic model
async def _add_documents_impl(input_data: AddDocumentsInput) -> types.CallToolResult:
    """Adds documents to the specified ChromaDB collection.

    Args:
        input_data: An AddDocumentsInput object containing validated arguments.

    Returns:
        A CallToolResult object.
        On success, content contains a TextContent object with a JSON string
        confirming the addition, typically including the number of items added.
        On error (e.g., collection not found, ID conflict, mismatched list lengths,
        validation error, unexpected issue), isError is True and content contains
        a TextContent object with an error message.
    """

    # Access validated data from the input model
    collection_name = input_data.collection_name
    documents = input_data.documents
    ids = input_data.ids
    metadatas = input_data.metadatas
    # Pydantic handles the default for increment_index
    effective_increment_index = input_data.increment_index

    try:
        # REMOVED: Pydantic handles None default assignment for lists implicitly
        # Handle None defaults for lists
        # effective_metadatas = metadatas if metadatas is not None else []
        # effective_ids = ids if ids is not None else []

        # REMOVED: Basic document presence checked by Pydantic
        # Input validation
        # if not documents:
        #     raise ValidationError("No documents provided")
        # Check list lengths match if provided (Still needs to be done)
        if metadatas and len(metadatas) != len(documents):
            raise ValidationError("Number of metadatas must match number of documents")
        if ids and len(ids) != len(documents):
            raise ValidationError("Number of IDs must match number of documents")

        # Get collection
        client = get_chroma_client()
        collection = client.get_collection(name=collection_name, embedding_function=get_embedding_function())

        # Generate IDs if not provided
        generated_ids = False
        final_ids = ids
        if not final_ids:
            generated_ids = True
            # Note: This count might be inaccurate if increment_index is False, but it's for ID generation
            current_count = collection.count()
            timestamp = int(time.time())
            final_ids = [f"doc_{timestamp}_{current_count + i}" for i in range(len(documents))]

        # Prepare metadatas (pass None if original was None or empty list)
        final_metadatas = metadatas if metadatas else None

        # Add documents
        collection.add(
            documents=documents,
            metadatas=final_metadatas,
            ids=final_ids
            # increment_index is not directly settable here in v0.5+ API
        )

        logger.info(f"Added {len(documents)} documents to collection '{collection_name}'.")
        result_data = {
            "status": "success",
            "added_count": len(documents),
            "collection_name": collection_name,
            "document_ids": final_ids,  # Return the actual IDs used
            "ids_generated": generated_ids,
        }
        result_json = json.dumps(result_data, indent=2)
        return types.CallToolResult(content=[types.TextContent(type="text", text=result_json)])

    except ValidationError as e:
        logger.warning(f"Validation error adding documents to '{collection_name}': {e}")
        return types.CallToolResult(
            isError=True, content=[types.TextContent(type="text", text=f"Validation Error: {str(e)}")]
        )
    except ValueError as e:  # Often used by Chroma for collection not found, duplicate ID etc.
        logger.error(f"ChromaDB error adding documents to '{collection_name}': {e}", exc_info=True)
        error_msg = f"ChromaDB Error: {str(e)}"
        if f"Collection {collection_name} does not exist." in str(e):
            error_msg = f"Tool Error: Collection '{collection_name}' not found."
        elif "ID already exists" in str(e):
            error_msg = f"Tool Error: One or more provided IDs already exist in collection '{collection_name}'."
        return types.CallToolResult(isError=True, content=[types.TextContent(type="text", text=error_msg)])
    except Exception as e:
        logger.error(f"Unexpected error adding documents to '{collection_name}': {e}", exc_info=True)
        return types.CallToolResult(
            isError=True,
            content=[
                types.TextContent(
                    type="text",
                    text=f"Tool Error: An unexpected error occurred while adding documents to '{collection_name}'. Details: {str(e)}",
                )
            ],
        )


# Signature changed to accept Pydantic model
async def _query_documents_impl(input_data: QueryDocumentsInput) -> types.CallToolResult:
    """Performs semantic search within a ChromaDB collection.

    Args:
        input_data: A QueryDocumentsInput object containing validated arguments.

    Returns:
        A CallToolResult object.
        On success, content contains a TextContent object with a JSON string
        representing the QueryResult (containing lists for ids, documents,
        metadatas, distances, etc., corresponding to each query).
        On error (e.g., collection not found, invalid filter format,
        unexpected issue), isError is True and content contains a TextContent
        object with an error message.
    """

    # Access validated data from the input model
    collection_name = input_data.collection_name
    query_texts = input_data.query_texts
    # Pydantic handles default and ge=1 validation
    effective_n_results = input_data.n_results
    where = input_data.where
    where_document = input_data.where_document
    include = input_data.include

    try:
        # REMOVED: Pydantic handles None defaults for where, where_document, include
        # REMOVED: Validation handled by Pydantic (query_texts presence, n_results > 0)

        # Validate include values if provided (still useful)
        valid_includes = ["documents", "embeddings", "metadatas", "distances"]
        if include and not all(item in valid_includes for item in include):
            invalid_items = [item for item in include if item not in valid_includes]
            raise ValidationError(
                f"Invalid item(s) in include list: {invalid_items}. Valid items are: {valid_includes}"
            )

        # Get collection, handle not found
        client = get_chroma_client()
        try:
            collection = client.get_collection(name=collection_name, embedding_function=get_embedding_function())
        except ValueError as e:
            if f"Collection {collection_name} does not exist." in str(e):
                logger.warning(f"Cannot query documents: Collection '{collection_name}' not found.")
                return types.CallToolResult(
                    isError=True,
                    content=[
                        types.TextContent(type="text", text=f"Tool Error: Collection '{collection_name}' not found.")
                    ],
                )
            else:
                raise e  # Re-raise other ValueErrors from get_collection
        except Exception as e:
            logger.error(f"Unexpected error getting collection '{collection_name}' for query: {e}", exc_info=True)
            return types.CallToolResult(
                isError=True,
                content=[
                    types.TextContent(
                        type="text", text=f"Tool Error: Failed to get collection '{collection_name}'. Details: {str(e)}"
                    )
                ],
            )

        # Set default includes if list was empty or None
        final_include = include if include else ["documents", "metadatas", "distances"]

        # Query documents, handle query-specific errors
        try:
            results = collection.query(
                query_texts=query_texts,
                n_results=effective_n_results,
                where=where,  # Pass directly (None if not provided)
                where_document=where_document,  # Pass directly (None if not provided)
                include=final_include,
            )
        except (ValueError, InvalidDimensionException) as e:  # Catch errors from query
            logger.error(f"Error executing query on collection '{collection_name}': {e}", exc_info=True)
            return types.CallToolResult(
                isError=True, content=[types.TextContent(type="text", text=f"ChromaDB Query Error: {str(e)}")]
            )

        # Format results - Convert embeddings if included
        if "embeddings" in final_include and results.get("embeddings"):
            processed_embeddings = []
            for query_embeddings in results.get("embeddings", []) or []:
                processed_query_embeddings = []
                if query_embeddings:
                    for emb in query_embeddings:
                        if hasattr(emb, "tolist") and callable(emb.tolist):
                            processed_query_embeddings.append(emb.tolist())
                        else:
                            processed_query_embeddings.append(emb)
                processed_embeddings.append(processed_query_embeddings)
            results["embeddings"] = processed_embeddings

        # Success result
        result_json = json.dumps(results, indent=2)
        return types.CallToolResult(content=[types.TextContent(type="text", text=result_json)])

    except ValidationError as e:
        logger.warning(f"Validation error querying documents in '{collection_name}': {e}")
        return types.CallToolResult(
            isError=True, content=[types.TextContent(type="text", text=f"Validation Error: {str(e)}")]
        )
    except ValueError as e:  # Catch ValueErrors re-raised from get_collection
        logger.error(f"Value error getting collection '{collection_name}' for query: {e}", exc_info=False)
        return types.CallToolResult(
            isError=True,
            content=[types.TextContent(type="text", text=f"ChromaDB Value Error getting collection: {str(e)}")],
        )
    except Exception as e:
        logger.error(f"Unexpected error querying documents in '{collection_name}': {e}", exc_info=True)
        return types.CallToolResult(
            isError=True,
            content=[
                types.TextContent(
                    type="text",
                    text=f"Tool Error: An unexpected error occurred while querying documents in '{collection_name}'. Details: {str(e)}",
                )
            ],
        )


# Signature changed to accept Pydantic model
async def _get_documents_impl(input_data: GetDocumentsInput) -> types.CallToolResult:
    """Retrieves documents from a collection by ID or using filters.

    Args:
        input_data: A GetDocumentsInput object containing validated arguments.

    Returns:
        A CallToolResult object.
        On success, content contains a TextContent object with a JSON string
        representing the GetResult (containing lists for ids, documents,
        metadatas, etc.). If IDs are provided and some are not found, they
        will be omitted from the results without an error.
        On error (e.g., collection not found, invalid filter format,
        unexpected issue), isError is True and content contains a TextContent
        object with an error message.
    """

    try:
        # Access validated data from the input model
        collection_name = input_data.collection_name
        ids = input_data.ids
        where = input_data.where
        where_document = input_data.where_document
        # Pydantic handles None defaults and validation (ge=1 for limit, ge=0 for offset)
        limit = input_data.limit
        offset = input_data.offset
        include = input_data.include

        # REMOVED: Pydantic handles type/range validation for limit/offset
        # Check logical condition: at least one filter/id must be provided
        if ids is None and where is None and where_document is None:
            raise ValidationError("At least one of ids, where, or where_document must be provided for get operation.")

        # Validate include values if provided
        valid_includes = ["documents", "embeddings", "metadatas"]
        if include and not all(item in valid_includes for item in include):
            invalid_items = [item for item in include if item not in valid_includes]
            raise ValidationError(
                f"Invalid item(s) in include list: {invalid_items}. Valid items are: {valid_includes}"
            )

        # Get collection, handle not found
        client = get_chroma_client()
        try:
            collection = client.get_collection(name=collection_name, embedding_function=get_embedding_function())
        except ValueError as e:
            if f"Collection {collection_name} does not exist." in str(e):
                logger.warning(f"Cannot get documents: Collection '{collection_name}' not found.")
                return types.CallToolResult(
                    isError=True,
                    content=[
                        types.TextContent(type="text", text=f"Tool Error: Collection '{collection_name}' not found.")
                    ],
                )
            else:
                raise e  # Re-raise other ValueErrors
        except Exception as e:
            logger.error(f"Unexpected error getting collection '{collection_name}' for get: {e}", exc_info=True)
            return types.CallToolResult(
                isError=True,
                content=[
                    types.TextContent(
                        type="text", text=f"Tool Error: Failed to get collection '{collection_name}'. Details: {str(e)}"
                    )
                ],
            )

        # Set default includes if empty or None
        final_include = include if include else ["documents", "metadatas"]

        # Get documents, handle errors
        try:
            results = collection.get(
                ids=ids,
                where=where,
                limit=limit,  # Pass directly (None if not provided)
                offset=offset,  # Pass directly (None if not provided)
                where_document=where_document,
                include=final_include,
            )
        except ValueError as e:  # Catch errors from get (e.g., bad filter)
            logger.error(f"Error executing get on collection '{collection_name}': {e}", exc_info=True)
            return types.CallToolResult(
                isError=True, content=[types.TextContent(type="text", text=f"ChromaDB Get Error: {str(e)}")]
            )

        # Format results - Convert embeddings if included
        if "embeddings" in final_include and results.get("embeddings"):
            processed_embeddings = []
            for emb in results.get("embeddings", []) or []:
                if hasattr(emb, "tolist") and callable(emb.tolist):
                    processed_embeddings.append(emb.tolist())
                else:
                    processed_embeddings.append(emb)
            results["embeddings"] = processed_embeddings

        # Success result
        result_json = json.dumps(results, indent=2)
        return types.CallToolResult(content=[types.TextContent(type="text", text=result_json)])

    except ValidationError as e:
        logger.warning(f"Validation error getting documents from '{collection_name}': {e}")
        return types.CallToolResult(
            isError=True, content=[types.TextContent(type="text", text=f"Validation Error: {str(e)}")]
        )
    except ValueError as e:  # Catch ValueErrors re-raised from get_collection
        logger.error(f"Value error getting collection '{collection_name}' for get: {e}", exc_info=False)
        return types.CallToolResult(
            isError=True,
            content=[types.TextContent(type="text", text=f"ChromaDB Value Error getting collection: {str(e)}")],
        )
    except Exception as e:
        logger.error(f"Unexpected error getting documents from '{collection_name}': {e}", exc_info=True)
        return types.CallToolResult(
            isError=True,
            content=[
                types.TextContent(
                    type="text",
                    text=f"Tool Error: An unexpected error occurred while getting documents from '{collection_name}'. Details: {str(e)}",
                )
            ],
        )


# Signature changed to accept Pydantic model
async def _update_documents_impl(input_data: UpdateDocumentsInput) -> types.CallToolResult:
    """Updates the content and/or metadata of existing documents.

    Args:
        input_data: An UpdateDocumentsInput object containing validated arguments.

    Returns:
        A CallToolResult object.
        On success, content contains a TextContent object with a JSON string
        confirming the update, potentially indicating the number of documents affected.
        On error (e.g., collection not found, ID not found, mismatched list lengths,
        validation error, unexpected issue), isError is True and content contains
        a TextContent object with an error message.
    """

    try:
        # Access validated data
        collection_name = input_data.collection_name
        ids = input_data.ids
        documents = input_data.documents
        metadatas = input_data.metadatas

        # REMOVED: Basic validation handled by Pydantic (presence of ids)
        # Logical validation: at least one field to update must be provided
        if documents is None and metadatas is None:
            raise ValidationError("Either 'documents' or 'metadatas' must be provided to update.")

        # Check list lengths match if provided (Still needs to be done)
        if documents is not None and len(documents) != len(ids):
            raise ValidationError("Number of documents must match number of IDs.")
        if metadatas is not None and len(metadatas) != len(ids):
            raise ValidationError("Number of metadatas must match number of IDs.")

        # Get collection, handle not found
        client = get_chroma_client()
        try:
            collection = client.get_collection(name=collection_name, embedding_function=get_embedding_function())
        except ValueError as e:
            if f"Collection {collection_name} does not exist." in str(e):
                logger.warning(f"Cannot update documents: Collection '{collection_name}' not found.")
                return types.CallToolResult(
                    isError=True,
                    content=[
                        types.TextContent(type="text", text=f"Tool Error: Collection '{collection_name}' not found.")
                    ],
                )
            else:
                raise e  # Re-raise other ValueErrors
        except Exception as e:
            logger.error(f"Unexpected error getting collection '{collection_name}' for update: {e}", exc_info=True)
            return types.CallToolResult(
                isError=True,
                content=[
                    types.TextContent(
                        type="text", text=f"Tool Error: Failed to get collection '{collection_name}'. Details: {str(e)}"
                    )
                ],
            )

        # Update documents, handle potential errors
        try:
            # Note: ChromaDB's update might not error if IDs don't exist.
            collection.update(
                ids=ids,
                documents=documents,  # Pass None if not provided
                metadatas=metadatas,  # Pass None if not provided
            )
        except ValueError as e:  # Catch errors from update
            error_msg = f"ChromaDB Update Error: {str(e)}"
            # Example check (might need adjustment)
            if "ID not found" in str(e) or "does not exist" in str(e):
                error_msg = f"ChromaDB Update Error: One or more specified IDs do not exist in collection '{collection_name}'. Details: {str(e)}"

            logger.error(f"Error updating documents in collection '{collection_name}': {e}", exc_info=True)
            return types.CallToolResult(isError=True, content=[types.TextContent(type="text", text=error_msg)])
        except InvalidDimensionException as e:
            logger.error(f"Dimension error updating documents in '{collection_name}': {e}", exc_info=True)
            return types.CallToolResult(
                isError=True, content=[types.TextContent(type="text", text=f"ChromaDB Dimension Error: {str(e)}")]
            )

        logger.info(f"Attempted update for {len(ids)} documents in collection '{collection_name}'")

        # Success result
        result_data = {
            "status": "success",
            "processed_count": len(ids),
            "collection_name": collection_name,
            "document_ids_submitted": ids,
        }
        result_json = json.dumps(result_data, indent=2)
        return types.CallToolResult(content=[types.TextContent(type="text", text=result_json)])

    except ValidationError as e:
        logger.warning(f"Validation error updating documents in '{collection_name}': {e}")
        return types.CallToolResult(
            isError=True, content=[types.TextContent(type="text", text=f"Validation Error: {str(e)}")]
        )
    except ValueError as e:  # Catch ValueErrors re-raised from get_collection
        logger.error(f"Value error getting collection '{collection_name}' for update: {e}", exc_info=False)
        return types.CallToolResult(
            isError=True,
            content=[types.TextContent(type="text", text=f"ChromaDB Value Error getting collection: {str(e)}")],
        )
    except Exception as e:
        logger.error(f"Unexpected error updating documents in '{collection_name}': {e}", exc_info=True)
        return types.CallToolResult(
            isError=True,
            content=[
                types.TextContent(
                    type="text",
                    text=f"Tool Error: An unexpected error occurred while updating documents in '{collection_name}'. Details: {str(e)}",
                )
            ],
        )


# Signature changed to accept Pydantic model
async def _delete_documents_impl(input_data: DeleteDocumentsInput) -> types.CallToolResult:
    """Deletes documents from a collection by ID or filter.

    Args:
        input_data: A DeleteDocumentsInput object containing validated arguments.

    Returns:
        A CallToolResult object.
        On success, content contains a TextContent object with a JSON string
        containing the list of IDs that were actually deleted.
        On error (e.g., collection not found, invalid filter format,
        unexpected issue), isError is True and content contains a TextContent
        object with an error message.
    """

    try:
        # Access validated data
        collection_name = input_data.collection_name
        ids = input_data.ids
        where = input_data.where
        where_document = input_data.where_document

        # REMOVED: Basic validation handled by Pydantic
        # Logical validation: at least one filter/id must be provided
        if ids is None and where is None and where_document is None:
            raise ValidationError("At least one of ids, where, or where_document must be provided for deletion.")

        # Get collection
        client = get_chroma_client()
        try:
            collection = client.get_collection(name=collection_name, embedding_function=get_embedding_function())
        except ValueError as e:
            if f"Collection {collection_name} does not exist." in str(e):
                logger.warning(f"Cannot delete documents: Collection '{collection_name}' not found.")
                return types.CallToolResult(
                    isError=True,
                    content=[
                        types.TextContent(type="text", text=f"Tool Error: Collection '{collection_name}' not found.")
                    ],
                )
            else:
                raise e  # Re-raise other ValueErrors
        except Exception as e:
            logger.error(f"Unexpected error getting collection '{collection_name}' for delete: {e}", exc_info=True)
            return types.CallToolResult(
                isError=True,
                content=[
                    types.TextContent(
                        type="text", text=f"Tool Error: Failed to get collection '{collection_name}'. Details: {str(e)}"
                    )
                ],
            )

        # Delete documents, handle potential errors
        try:
            # Chroma's delete returns the list of IDs that matched the criteria
            deleted_ids = collection.delete(
                ids=ids,  # Pass None if not provided
                where=where,  # Pass None if not provided
                where_document=where_document,  # Pass None if not provided
            )
        except ValueError as e:  # Catch errors from delete (e.g., bad filter)
            logger.error(f"Error executing delete on collection '{collection_name}': {e}", exc_info=True)
            return types.CallToolResult(
                isError=True, content=[types.TextContent(type="text", text=f"ChromaDB Delete Error: {str(e)}")]
            )

        # Success result
        logger.info(
            f"Delete operation completed for collection '{collection_name}'. Matched IDs: {len(deleted_ids) if deleted_ids else 0}"
        )
        result_data = {
            "status": "success",
            "deleted_ids": deleted_ids if deleted_ids else [],  # Return matched IDs
            "collection_name": collection_name,
        }
        result_json = json.dumps(result_data, indent=2)
        return types.CallToolResult(content=[types.TextContent(type="text", text=result_json)])

    except ValidationError as e:
        logger.warning(f"Validation error deleting documents from '{collection_name}': {e}")
        return types.CallToolResult(
            isError=True, content=[types.TextContent(type="text", text=f"Validation Error: {str(e)}")]
        )
    except ValueError as e:  # Catch ValueErrors re-raised from get_collection
        logger.error(f"Value error getting collection '{collection_name}' for delete: {e}", exc_info=False)
        return types.CallToolResult(
            isError=True,
            content=[types.TextContent(type="text", text=f"ChromaDB Value Error getting collection: {str(e)}")],
        )
    except Exception as e:
        logger.error(f"Unexpected error deleting documents from '{collection_name}': {e}", exc_info=True)
        return types.CallToolResult(
            isError=True,
            content=[
                types.TextContent(
                    type="text",
                    text=f"Tool Error: An unexpected error occurred while deleting documents from '{collection_name}'. Details: {str(e)}",
                )
            ],
        )
