"""
Collection management tools for ChromaDB operations.
"""

import json
import logging
import chromadb
import chromadb.errors as chroma_errors
from chromadb.api.client import ClientAPI
from chromadb.errors import InvalidDimensionException
import numpy as np

from pydantic import BaseModel, Field
from typing import Any, Dict, List, Optional, Union, cast
from dataclasses import dataclass

from chromadb.api.types import CollectionMetadata, GetResult, QueryResult
from chromadb.errors import InvalidDimensionException

from mcp import types
from mcp.types import ErrorData, INVALID_PARAMS, INTERNAL_ERROR
from mcp.shared.exceptions import McpError

from ..utils import (
    get_logger,
    get_chroma_client,
    get_embedding_function,
    ValidationError,
    ClientError,
    ConfigurationError,
)
from ..utils.config import get_collection_settings, validate_collection_name

# Ensure mcp instance is imported/available for decorators
# Might need to adjust imports if mcp is not globally accessible here.
# Assuming FastMCP instance is created elsewhere and decorators register to it.
# We need to import the mcp instance or pass it.
# Let's assume FastMCP handles registration implicitly upon import.
# Need to ensure FastMCP is imported here:
# REMOVE: from mcp.server.fastmcp import FastMCP

# It's more likely the mcp instance is needed. Let's assume it's globally accessible
# or passed to a setup function that imports this module. For now, leave as is.
# If errors persist, we might need to import the global _mcp_instance from server.py.

# --- Pydantic Input Models for Collection Tools ---


class CreateCollectionInput(BaseModel):
    collection_name: str = Field(
        description="The name for the new collection. Must adhere to ChromaDB naming conventions."
    )
    metadata: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Optional metadata and settings (e.g., {'description': '...', 'settings': {'hnsw:space': 'cosine'}}). Uses server defaults if None.",
    )


class ListCollectionsInput(BaseModel):
    limit: Optional[int] = Field(
        default=None, ge=0, description="Maximum number of collections to return (0 or None for no limit)."
    )
    offset: Optional[int] = Field(default=None, ge=0, description="Number of collections to skip.")
    name_contains: Optional[str] = Field(
        default=None, description="Filter collections by name (case-insensitive contains)."
    )


class GetCollectionInput(BaseModel):
    collection_name: str = Field(description="The name of the collection to retrieve information for.")


class SetCollectionDescriptionInput(BaseModel):
    collection_name: str = Field(description="The name of the collection to update.")
    description: str = Field(description="The new description for the collection.")


class SetCollectionSettingsInput(BaseModel):
    collection_name: str = Field(description="The name of the collection to update.")
    settings: Dict[str, Any] = Field(
        description="A dictionary containing the new settings (e.g., HNSW parameters). Replaces existing settings."
    )


class UpdateCollectionMetadataInput(BaseModel):
    collection_name: str = Field(description="The name of the collection to update.")
    metadata_update: Dict[str, Any] = Field(
        description="Key-value pairs to add/update in the collection's custom metadata block. Replaces existing custom metadata."
    )


class RenameCollectionInput(BaseModel):
    collection_name: str = Field(description="The current name of the collection to rename.")
    new_name: str = Field(description="The new name for the collection.")


class DeleteCollectionInput(BaseModel):
    collection_name: str = Field(description="The name of the collection to delete.")


class PeekCollectionInput(BaseModel):
    collection_name: str = Field(description="The name of the collection to peek into.")
    limit: Optional[int] = Field(
        default=None,
        ge=1,
        description="Maximum number of documents to return (defaults to ChromaDB's internal default, often 10). Must be >= 1.",
    )


# --- End Pydantic Input Models ---


def _reconstruct_metadata(metadata: Optional[Dict[str, Any]]) -> Dict[str, Any]:
    """Reconstructs the structured metadata (with 'settings') from ChromaDB's internal format."""
    if not metadata:
        return {}

    reconstructed = {}
    settings = {}
    for key, value in metadata.items():
        setting_key_to_store = None
        # Check for flattened setting keys
        if key.startswith("chroma:setting:"):
            # Convert 'chroma_setting_hnsw_space' back to 'hnsw:space'
            original_key = key[len("chroma:setting:") :].replace("_", ":")
            setting_key_to_store = original_key
        # Also recognize common raw keys like hnsw:*
        elif key.startswith("hnsw:"):
            setting_key_to_store = key

        if setting_key_to_store:
            settings[setting_key_to_store] = value
        # Explicitly check for 'description' as it's handled separately
        elif key == "description":
            reconstructed[key] = value
        # Store other keys directly (custom user keys)
        elif not key.startswith("chroma:"):  # Avoid other potential internal chroma keys
            reconstructed[key] = value

    if settings:
        reconstructed["settings"] = settings

    return reconstructed


# --- Implementation Functions ---


# Signature changed to accept Pydantic model
async def _create_collection_impl(input_data: CreateCollectionInput) -> types.CallToolResult:
    """Creates a new ChromaDB collection.

    Args:
        input_data: A CreateCollectionInput object containing validated arguments.

    Returns:
        A CallToolResult object.
        On success, content contains a TextContent object with a JSON string
        detailing the created collection's name, id, metadata, count, and
        sample entries (up to 5).
        On error (e.g., validation error, collection exists, unexpected issue),
        isError is True and content contains a TextContent object with an
        error message.
    """
    logger = get_logger("tools.collection")
    try:
        # Access validated data from the input model
        collection_name = input_data.collection_name
        metadata = input_data.metadata

        validate_collection_name(collection_name)
        client = get_chroma_client()

        # Determine metadata: Use provided or get defaults
        metadata_to_use = None
        log_msg_suffix = ""
        if metadata is not None:
            # REMOVED: Type check handled by Pydantic
            # if not isinstance(metadata, dict):
            #     logger.warning(f"Invalid metadata type provided: {type(metadata)}")
            #     return types.CallToolResult(isError=True, content=[types.TextContent(type="text", text="Tool Error: metadata must be a dictionary.")])
            metadata_to_use = metadata
            log_msg_suffix = "with provided metadata."
        else:
            metadata_to_use = get_collection_settings()
            log_msg_suffix = "with default settings."

        # Call create_collection directly with embedding function and target metadata
        logger.debug(
            f"Attempting to create collection '{collection_name}' with embedding function and metadata: {metadata_to_use}"
        )
        collection = client.create_collection(
            name=collection_name,
            metadata=metadata_to_use,
            embedding_function=get_embedding_function(),
            get_or_create=False,
        )
        logger.info(f"Created collection: {collection_name} {log_msg_suffix}")

        # Get the count (should be 0)
        count = collection.count()
        # REMOVED: peek_results = collection.peek(limit=5) # Useless on a new collection

        # REMOVED: Process peek_results logic is no longer needed here

        result_data = {
            "name": collection.name,
            "id": str(collection.id),  # Ensure ID is string if it's UUID
            "metadata": _reconstruct_metadata(collection.metadata),
            "count": count,
            # REMOVED: "sample_entries": processed_peek
        }
        # Serialize success result to JSON
        result_json = json.dumps(result_data, indent=2)
        return types.CallToolResult(content=[types.TextContent(type="text", text=result_json)])

    except ValidationError as e:
        logger.warning(f"Validation error creating collection '{collection_name}': {e}")
        return types.CallToolResult(
            isError=True, content=[types.TextContent(type="text", text=f"Validation Error: {str(e)}")]
        )
    except ValueError as e:
        # Check if the error message indicates a duplicate collection
        if f"Collection {collection_name} already exists." in str(e):
            logger.warning(f"Collection '{collection_name}' already exists.")
            return types.CallToolResult(
                isError=True,
                content=[
                    types.TextContent(type="text", text=f"Tool Error: Collection '{collection_name}' already exists.")
                ],
            )
        else:
            # Handle other ValueErrors as likely invalid parameters
            logger.error(f"Validation error during collection creation '{collection_name}': {e}", exc_info=True)
            return types.CallToolResult(
                isError=True,
                content=[
                    types.TextContent(
                        type="text", text=f"Tool Error: Invalid parameter during collection creation. Details: {e}"
                    )
                ],
            )
    except InvalidDimensionException as e:  # Example of another specific Chroma error
        logger.error(f"Dimension error creating collection '{collection_name}': {e}", exc_info=True)
        return types.CallToolResult(
            isError=True,
            content=[types.TextContent(type="text", text=f"ChromaDB Error: Invalid dimension configuration. {str(e)}")],
        )
    except Exception as e:
        # Log the full unexpected error server-side
        logger.error(f"Unexpected error creating collection '{collection_name}': {e}", exc_info=True)
        # Return a Tool Error instead of raising McpError
        return types.CallToolResult(
            isError=True,
            content=[
                types.TextContent(
                    type="text",
                    text=f"Tool Error: An unexpected error occurred while creating collection '{collection_name}'. Details: {str(e)}",
                )
            ],
        )


# Signature changed to accept Pydantic model
async def _list_collections_impl(input_data: ListCollectionsInput) -> types.CallToolResult:
    """Lists available ChromaDB collections.

    Args:
        input_data: A ListCollectionsInput object containing validated arguments.

    Returns:
        A CallToolResult object.
        On success, content contains a TextContent object with a JSON string
        containing a list of 'collection_names', the 'total_count' (before pagination),
        and the requested 'limit' and 'offset'.
        On error (e.g., validation error, unexpected issue), isError is True and
        content contains a TextContent object with an error message.
    """
    logger = get_logger("tools.collection")
    try:
        # Access validated data from the input model
        # Pydantic handles None defaults and ge=0 validation
        effective_limit = input_data.limit
        effective_offset = input_data.offset
        name_contains = input_data.name_contains

        # REMOVE: Assign effective defaults - Pydantic handles None default assignment
        # effective_limit = 0 if limit is None else limit
        # effective_offset = 0 if offset is None else offset

        # REMOVE: Validation handled by Pydantic model (ge=0)
        # Input validation
        # if effective_limit < 0:
        #     raise ValidationError("limit cannot be negative")
        # if effective_offset < 0:
        #     raise ValidationError("offset cannot be negative")

        client = get_chroma_client()
        # In ChromaDB v0.5+, list_collections returns Collection objects
        # The code needs to handle this correctly.
        all_collections = client.list_collections()

        # Correctly extract names from Collection objects
        collection_names = []
        if isinstance(all_collections, list):
            for col in all_collections:
                try:
                    # Access the name attribute of the Collection object
                    collection_names.append(col.name)
                except AttributeError:
                    logger.warning(f"Object in list_collections result does not have a .name attribute: {type(col)}")
        else:
            logger.warning(f"client.list_collections() returned unexpected type: {type(all_collections)}")

        # REMOVE: Redundant check - already handled above
        # Safety check, though Chroma client should return a list of Collections (already handled above)
        # if not isinstance(collection_names, list): # This check is redundant now
        #     logger.warning(f"client.list_collections() yielded unexpected structure, processing as empty list.")
        #     collection_names = []

        # Filter by name_contains if provided (case-insensitive)
        filtered_names = collection_names
        if name_contains is not None:  # Check against None
            filtered_names = [name for name in collection_names if name_contains.lower() in name.lower()]

        total_count = len(filtered_names)

        # Apply pagination
        start_index = effective_offset if effective_offset is not None else 0
        end_index = (
            (start_index + effective_limit) if effective_limit is not None and effective_limit > 0 else total_count
        )

        paginated_names = filtered_names[start_index:end_index]

        result_data = {
            "collection_names": paginated_names,
            "total_count": total_count,
            "limit": effective_limit,
            "offset": effective_offset,
        }
        result_json = json.dumps(result_data, indent=2)
        return types.CallToolResult(content=[types.TextContent(type="text", text=result_json)])
    except ValidationError as e:
        logger.warning(f"Validation error listing collections: {e}")
        return types.CallToolResult(
            isError=True, content=[types.TextContent(type="text", text=f"Validation Error: {str(e)}")]
        )
    except Exception as e:
        logger.error(f"Unexpected error listing collections: {e}", exc_info=True)
        return types.CallToolResult(
            isError=True,
            content=[
                types.TextContent(
                    type="text",
                    text=f"Tool Error: An unexpected error occurred while listing collections. Details: {str(e)}",
                )
            ],
        )


# Signature changed to accept Pydantic model
async def _get_collection_impl(input_data: GetCollectionInput) -> types.CallToolResult:
    """Retrieves details about a specific ChromaDB collection.

    Args:
        input_data: A GetCollectionInput object containing validated arguments.

    Returns:
        A CallToolResult object.
        On success, content contains a TextContent object with a JSON string
        detailing the collection's name, id, metadata, count, and sample entries.
        On error (e.g., collection not found, unexpected issue), isError is True
        and content contains a TextContent object with an error message.
    """
    logger = get_logger("tools.collection")
    try:
        collection_name = input_data.collection_name

        validate_collection_name(collection_name)
        client = get_chroma_client()
        # Use get_collection which raises an error if not found
        collection = client.get_collection(name=collection_name, embedding_function=get_embedding_function())

        count = collection.count()
        peek_results = collection.peek(limit=5)  # Get a small sample

        # Process peek results for JSON serialization
        processed_peek = peek_results.copy() if peek_results else {}
        if processed_peek.get("embeddings"):
            processed_peek["embeddings"] = [
                arr.tolist() if hasattr(arr, "tolist") and callable(arr.tolist) else arr
                for arr in processed_peek["embeddings"]
                if arr is not None
            ]

        result_data = {
            "name": collection.name,
            "id": str(collection.id),  # Ensure ID is string if it's UUID
            "metadata": _reconstruct_metadata(collection.metadata),
            "count": count,
            "sample_entries": processed_peek,
        }
        result_json = json.dumps(result_data, indent=2)
        return types.CallToolResult(content=[types.TextContent(type="text", text=result_json)])
    except ValueError as e:
        # Check if the error message indicates collection not found
        if f"Collection {collection_name} does not exist." in str(e):
            logger.warning(f"Collection '{collection_name}' not found.")
            return types.CallToolResult(
                isError=True,
                content=[types.TextContent(type="text", text=f"Tool Error: Collection '{collection_name}' not found.")],
            )
        else:
            # Handle other ValueErrors as likely internal errors
            logger.error(f"Error getting collection '{collection_name}': {e}", exc_info=True)
            return types.CallToolResult(
                isError=True,
                content=[
                    types.TextContent(
                        type="text", text=f"Tool Error: Problem accessing collection '{collection_name}'. Details: {e}"
                    )
                ],
            )
    except Exception as e:
        logger.error(f"Unexpected error getting collection '{collection_name}': {e}", exc_info=True)
        return types.CallToolResult(
            isError=True,
            content=[
                types.TextContent(
                    type="text",
                    text=f"Tool Error: An unexpected error occurred while getting collection '{collection_name}'. Details: {str(e)}",
                )
            ],
        )


# Signature changed to accept Pydantic model
async def _set_collection_description_impl(input_data: SetCollectionDescriptionInput) -> types.CallToolResult:
    """Sets the description metadata field for a collection.
    Note: Due to ChromaDB limitations, this tool will likely fail on existing collections.
          Set description during creation via metadata instead.

    Args:
        input_data: A SetCollectionDescriptionInput object containing validated arguments.

    Returns:
        A CallToolResult object.
        On success, content confirms the description update attempt.
        On error, isError is True and content contains an error message.
    """
    logger = get_logger("tools.collection")
    try:
        collection_name = input_data.collection_name
        description = input_data.description

        validate_collection_name(collection_name)
        # REMOVED: Type check handled by Pydantic
        # if not isinstance(description, str):
        #     raise ValidationError("Description must be a string.")

        client = get_chroma_client()
        collection = client.get_collection(name=collection_name)

        # Modify metadata - WARNING: This might not persist in ChromaDB versions
        # where metadata is largely immutable after creation.
        # The official way is often to set it during create_collection.
        logger.warning(
            f"Attempting to set description for '{collection_name}'. This operation might fail due to ChromaDB limitations."
        )
        try:
            collection.modify(metadata={"description": description})  # Use modify method
            logger.info(f"Modify call completed for setting description on '{collection_name}'. Verification needed.")
            return types.CallToolResult(
                content=[
                    types.TextContent(
                        type="text",
                        text=f"Attempted to set description for collection '{collection_name}'. Note: Persistence depends on ChromaDB version and setup.",
                    )
                ]
            )
        except Exception as e:  # Catch potential errors during modify itself
            logger.error(f"Error during collection.modify for description on '{collection_name}': {e}", exc_info=True)
            return types.CallToolResult(
                isError=True,
                content=[
                    types.TextContent(
                        type="text",
                        text=f"Tool Error: Failed during modify operation for '{collection_name}'. Details: {str(e)}",
                    )
                ],
            )

    except ValidationError as e:
        logger.warning(f"Validation error setting description for '{collection_name}': {e}")
        return types.CallToolResult(
            isError=True, content=[types.TextContent(type="text", text=f"Validation Error: {str(e)}")]
        )
    except ValueError as e:  # Catch collection not found from get_collection
        if f"Collection {collection_name} does not exist." in str(e):
            logger.warning(f"Cannot set description: Collection '{collection_name}' not found.")
            return types.CallToolResult(
                isError=True,
                content=[types.TextContent(type="text", text=f"Tool Error: Collection '{collection_name}' not found.")],
            )
        else:
            logger.error(f"Value error setting description for '{collection_name}': {e}", exc_info=True)
            return types.CallToolResult(
                isError=True,
                content=[
                    types.TextContent(
                        type="text", text=f"Tool Error: Problem accessing collection '{collection_name}'. Details: {e}"
                    )
                ],
            )
    except Exception as e:
        logger.error(f"Unexpected error setting description for '{collection_name}': {e}", exc_info=True)
        return types.CallToolResult(
            isError=True,
            content=[
                types.TextContent(
                    type="text",
                    text=f"Tool Error: An unexpected error occurred setting description for '{collection_name}'. Details: {str(e)}",
                )
            ],
        )


# Signature changed to accept Pydantic model
async def _set_collection_settings_impl(input_data: SetCollectionSettingsInput) -> types.CallToolResult:
    """Sets the 'settings' metadata block for a collection.
    Warning: This replaces existing settings. Likely fails on existing collections.

    Args:
        input_data: A SetCollectionSettingsInput object containing validated arguments.

    Returns:
        A CallToolResult object.
        On success, content confirms the settings update attempt.
        On error, isError is True and content contains an error message.
    """
    logger = get_logger("tools.collection")
    try:
        collection_name = input_data.collection_name
        settings = input_data.settings

        validate_collection_name(collection_name)
        # REMOVED: Type check handled by Pydantic
        # if not isinstance(settings, dict):
        #     raise ValidationError("Settings must be a dictionary.")

        client = get_chroma_client()
        collection = client.get_collection(name=collection_name)

        # Prepare metadata for ChromaDB (flattening settings)
        prepared_metadata = {}
        for key, value in settings.items():
            # Prefix setting keys for storage within Chroma metadata
            # Convert hnsw:space to chroma_setting_hnsw_space
            setting_key = f"chroma:setting:{key.replace(':', '_')}"
            prepared_metadata[setting_key] = value

        # Also include any existing non-setting metadata to avoid wiping it?
        # This is tricky. Chroma's modify might replace the whole block.
        # Let's assume for now it ONLY updates the provided keys.
        # If it replaces, we need to fetch existing metadata first.
        # Fetching existing metadata:
        existing_metadata = collection.metadata or {}
        final_metadata = existing_metadata.copy()
        final_metadata.update(prepared_metadata)  # Merge new settings

        # Modify metadata - WARNING: Likely fails or has unintended consequences.
        logger.warning(
            f"Attempting to set settings for '{collection_name}'. This operation is likely to fail or replace other metadata due to ChromaDB limitations."
        )
        try:
            collection.modify(metadata=final_metadata)  # Modify with merged data
            logger.info(f"Modify call completed for settings on '{collection_name}'. Verification needed.")
            return types.CallToolResult(
                content=[
                    types.TextContent(
                        type="text",
                        text=f"Attempted to set settings for collection '{collection_name}'. Note: Persistence and behavior depend heavily on ChromaDB version.",
                    )
                ]
            )
        except Exception as e:  # Catch potential errors during modify itself
            logger.error(f"Error during collection.modify for settings on '{collection_name}': {e}", exc_info=True)
            return types.CallToolResult(
                isError=True,
                content=[
                    types.TextContent(
                        type="text",
                        text=f"Tool Error: Failed during modify operation for '{collection_name}'. Details: {str(e)}",
                    )
                ],
            )

    except ValidationError as e:
        logger.warning(f"Validation error setting settings for '{collection_name}': {e}")
        return types.CallToolResult(
            isError=True, content=[types.TextContent(type="text", text=f"Validation Error: {str(e)}")]
        )
    except ValueError as e:  # Catch collection not found from get_collection
        if f"Collection {collection_name} does not exist." in str(e):
            logger.warning(f"Cannot set settings: Collection '{collection_name}' not found.")
            return types.CallToolResult(
                isError=True,
                content=[types.TextContent(type="text", text=f"Tool Error: Collection '{collection_name}' not found.")],
            )
        else:
            logger.error(f"Value error setting settings for '{collection_name}': {e}", exc_info=True)
            return types.CallToolResult(
                isError=True,
                content=[
                    types.TextContent(
                        type="text", text=f"Tool Error: Problem accessing collection '{collection_name}'. Details: {e}"
                    )
                ],
            )
    except Exception as e:
        logger.error(f"Unexpected error setting settings for '{collection_name}': {e}", exc_info=True)
        return types.CallToolResult(
            isError=True,
            content=[
                types.TextContent(
                    type="text",
                    text=f"Tool Error: An unexpected error occurred setting settings for '{collection_name}'. Details: {str(e)}",
                )
            ],
        )


# Signature changed to accept Pydantic model
async def _update_collection_metadata_impl(input_data: UpdateCollectionMetadataInput) -> types.CallToolResult:
    """Updates custom key-value pairs in a collection's metadata.
    Warning: This REPLACES the existing custom metadata block. Likely fails on existing collections.

    Args:
        input_data: An UpdateCollectionMetadataInput object containing validated arguments.

    Returns:
        A CallToolResult object.
        On success, content confirms the metadata update attempt.
        On error, isError is True and content contains an error message.
    """
    logger = get_logger("tools.collection")
    try:
        collection_name = input_data.collection_name
        metadata_update = input_data.metadata_update

        validate_collection_name(collection_name)
        # REMOVED: Type check handled by Pydantic
        # if not isinstance(metadata_update, dict):
        #     raise ValidationError("Metadata update must be a dictionary.")

        client = get_chroma_client()
        collection = client.get_collection(name=collection_name)

        # Modify metadata - WARNING: Replaces ENTIRE metadata block in some Chroma versions.
        logger.warning(
            f"Attempting to update metadata for '{collection_name}'. This operation might replace the entire metadata block."
        )
        try:
            collection.modify(metadata=metadata_update)  # Use the provided update directly
            logger.info(f"Modify call completed for metadata update on '{collection_name}'. Verification needed.")
            return types.CallToolResult(
                content=[
                    types.TextContent(
                        type="text",
                        text=f"Attempted to update metadata for collection '{collection_name}'. Note: Behavior depends heavily on ChromaDB version (may replace all metadata).",
                    )
                ]
            )
        except Exception as e:  # Catch potential errors during modify itself
            logger.error(
                f"Error during collection.modify for metadata update on '{collection_name}': {e}", exc_info=True
            )
            return types.CallToolResult(
                isError=True,
                content=[
                    types.TextContent(
                        type="text",
                        text=f"Tool Error: Failed during modify operation for '{collection_name}'. Details: {str(e)}",
                    )
                ],
            )

    except ValidationError as e:
        logger.warning(f"Validation error updating metadata for '{collection_name}': {e}")
        return types.CallToolResult(
            isError=True, content=[types.TextContent(type="text", text=f"Validation Error: {str(e)}")]
        )
    except ValueError as e:  # Catch collection not found from get_collection
        if f"Collection {collection_name} does not exist." in str(e):
            logger.warning(f"Cannot update metadata: Collection '{collection_name}' not found.")
            return types.CallToolResult(
                isError=True,
                content=[types.TextContent(type="text", text=f"Tool Error: Collection '{collection_name}' not found.")],
            )
        else:
            logger.error(f"Value error updating metadata for '{collection_name}': {e}", exc_info=True)
            return types.CallToolResult(
                isError=True,
                content=[
                    types.TextContent(
                        type="text", text=f"Tool Error: Problem accessing collection '{collection_name}'. Details: {e}"
                    )
                ],
            )
    except Exception as e:
        logger.error(f"Unexpected error updating metadata for '{collection_name}': {e}", exc_info=True)
        return types.CallToolResult(
            isError=True,
            content=[
                types.TextContent(
                    type="text",
                    text=f"Tool Error: An unexpected error occurred updating metadata for '{collection_name}'. Details: {str(e)}",
                )
            ],
        )


# Signature changed to accept Pydantic model
async def _rename_collection_impl(input_data: RenameCollectionInput) -> types.CallToolResult:
    """Renames an existing ChromaDB collection.

    Args:
        input_data: A RenameCollectionInput object containing validated arguments.

    Returns:
        A CallToolResult object.
        On success, content confirms the rename operation.
        On error, isError is True and content contains an error message.
    """
    
    logger = get_logger("tools.collection")
    try:
        collection_name = input_data.collection_name
        new_name = input_data.new_name

        validate_collection_name(collection_name)
        validate_collection_name(new_name)  # Validate the new name too

        client = get_chroma_client()
        collection = client.get_collection(name=collection_name)  # Ensure collection exists

        # Rename the collection
        collection.modify(name=new_name)  # Use modify with the new name
        logger.info(f"Renamed collection '{collection_name}' to '{new_name}'.")

        return types.CallToolResult(
            content=[
                types.TextContent(
                    type="text", text=f"Collection '{collection_name}' successfully renamed to '{new_name}'."
                )
            ]
        )

    except ValidationError as e:
        logger.warning(f"Validation error renaming collection '{collection_name}': {e}")
        return types.CallToolResult(
            isError=True, content=[types.TextContent(type="text", text=f"Validation Error: {str(e)}")]
        )
    except ValueError as e:  # Catch collection not found from get_collection
        if f"Collection {collection_name} does not exist." in str(e):
            logger.warning(f"Cannot rename: Collection '{collection_name}' not found.")
            return types.CallToolResult(
                isError=True,
                content=[types.TextContent(type="text", text=f"Tool Error: Collection '{collection_name}' not found.")],
            )
        # Check if the NEW name already exists
        elif f"Collection {new_name} already exists." in str(e):
            logger.warning(f"Cannot rename: New collection name '{new_name}' already exists.")
            return types.CallToolResult(
                isError=True,
                content=[
                    types.TextContent(type="text", text=f"Tool Error: Collection name '{new_name}' already exists.")
                ],
            )
        else:
            logger.error(f"Value error renaming '{collection_name}': {e}", exc_info=True)
            return types.CallToolResult(
                isError=True,
                content=[
                    types.TextContent(
                        type="text",
                        text=f"Tool Error: Problem accessing collection '{collection_name}' or invalid new name. Details: {e}",
                    )
                ],
            )
    except Exception as e:
        logger.error(f"Unexpected error renaming collection '{collection_name}': {e}", exc_info=True)
        return types.CallToolResult(
            isError=True,
            content=[
                types.TextContent(
                    type="text",
                    text=f"Tool Error: An unexpected error occurred renaming collection '{collection_name}'. Details: {str(e)}",
                )
            ],
        )


# Signature changed to accept Pydantic model
async def _delete_collection_impl(input_data: DeleteCollectionInput) -> types.CallToolResult:
    """Deletes a ChromaDB collection.

    Args:
        input_data: A DeleteCollectionInput object containing validated arguments.

    Returns:
        A CallToolResult object.
        On success, content confirms the deletion.
        On error (e.g., collection not found, unexpected issue), isError is True
        and content contains an error message.
    """
    logger = get_logger("tools.collection")
    try:
        collection_name = input_data.collection_name

        validate_collection_name(collection_name)
        client = get_chroma_client()

        # Delete the collection
        client.delete_collection(name=collection_name)
        logger.info(f"Deleted collection: {collection_name}")

        return types.CallToolResult(
            content=[types.TextContent(type="text", text=f"Collection '{collection_name}' deleted successfully.")]
        )
    except ValueError as e:
        # Handle collection not found error specifically
        if f"Collection {collection_name} does not exist." in str(e):
            logger.warning(f"Collection '{collection_name}' not found for deletion.")
            return types.CallToolResult(
                isError=True,
                content=[types.TextContent(type="text", text=f"Tool Error: Collection '{collection_name}' not found.")],
            )
        else:
            # Handle other ValueErrors as unexpected issues
            logger.error(f"Value error deleting collection '{collection_name}': {e}", exc_info=True)
            return types.CallToolResult(
                isError=True,
                content=[
                    types.TextContent(
                        type="text",
                        text=f"Tool Error: An unexpected error occurred deleting '{collection_name}'. Details: {e}",
                    )
                ],
            )
    except Exception as e:
        logger.error(f"Unexpected error deleting collection '{collection_name}': {e}", exc_info=True)
        return types.CallToolResult(
            isError=True,
            content=[
                types.TextContent(
                    type="text",
                    text=f"Tool Error: An unexpected error occurred deleting collection '{collection_name}'. Details: {str(e)}",
                )
            ],
        )


# Signature changed to accept Pydantic model
async def _peek_collection_impl(input_data: PeekCollectionInput) -> types.CallToolResult:
    """Retrieves a small sample of entries from a collection.

    Args:
        input_data: A PeekCollectionInput object containing validated arguments.

    Returns:
        A CallToolResult object.
        On success, content contains a TextContent object with a JSON string
        of the peek results (ids, embeddings, metadatas, documents).
        On error (e.g., collection not found, unexpected issue), isError is True
        and content contains an error message.
    """
    logger = get_logger("tools.collection")
    try:
        collection_name = input_data.collection_name
        # Pydantic handles None default and ge=1 validation
        limit = input_data.limit

        validate_collection_name(collection_name)
        # REMOVED: Validation handled by Pydantic
        # if limit is not None and limit < 1:
        #     raise ValidationError("Limit for peek must be >= 1 if provided.")

        client = get_chroma_client()
        collection = client.get_collection(name=collection_name)

        # Call peek with the validated limit (or None if not provided, letting Chroma use its default)
        peek_results = collection.peek(limit=limit if limit is not None else 10)  # Pass explicit default if None

        # Process results to make them JSON serializable if needed
        # Convert numpy arrays (or anything with a tolist() method) to lists
        processed_peek = peek_results.copy() if peek_results else {}
        if processed_peek.get("embeddings"):
            processed_peek["embeddings"] = [
                arr.tolist() if hasattr(arr, "tolist") and callable(arr.tolist) else arr
                for arr in processed_peek["embeddings"]
                if arr is not None
            ]

        result_json = json.dumps(processed_peek, indent=2)
        return types.CallToolResult(content=[types.TextContent(type="text", text=result_json)])
    except ValueError as e:  # Catch collection not found from get_collection
        if f"Collection {collection_name} does not exist." in str(e):
            logger.warning(f"Cannot peek: Collection '{collection_name}' not found.")
            return types.CallToolResult(
                isError=True,
                content=[types.TextContent(type="text", text=f"Tool Error: Collection '{collection_name}' not found.")],
            )
        else:
            logger.error(f"Value error peeking collection '{collection_name}': {e}", exc_info=True)
            return types.CallToolResult(
                isError=True,
                content=[
                    types.TextContent(
                        type="text", text=f"Tool Error: Problem accessing collection '{collection_name}'. Details: {e}"
                    )
                ],
            )
    except Exception as e:
        logger.error(f"Unexpected error peeking collection '{collection_name}': {e}", exc_info=True)
        return types.CallToolResult(
            isError=True,
            content=[
                types.TextContent(
                    type="text",
                    text=f"Tool Error: An unexpected error occurred peeking collection '{collection_name}'. Details: {str(e)}",
                )
            ],
        )


def _get_collection_info(collection) -> dict:
    """Helper to get basic info (name, id, metadata) about a collection object."""
    # ADD logger assignment inside the function
    logger = get_logger("tools.collection")
    try:
        return {
            "name": collection.name,
            "id": str(collection.id),
            "metadata": _reconstruct_metadata(collection.metadata),
        }
    except Exception as e:
        logger.error(f"Failed to get info for collection: {e}", exc_info=True)
        return {"error": f"Failed to retrieve collection info: {str(e)}"}
