"""
Document management tools for ChromaDB operations.
"""

import time
import json
import logging
import uuid
import numpy as np # Needed for NumpyEncoder usage

from typing import Dict, List, Optional, Any, Union, cast
from dataclasses import dataclass

# Import ChromaDB result types
from chromadb.api.types import QueryResult, GetResult

from mcp import types
from mcp.shared.exceptions import McpError
from mcp.types import ErrorData, INVALID_PARAMS, INTERNAL_ERROR
from pydantic import BaseModel, Field, field_validator, ConfigDict  # Import Pydantic

# Use relative imports
from ..utils.errors import ValidationError
from ..types import DocumentMetadata

from chromadb.errors import InvalidDimensionException

# --- Imports ---
import chromadb
# REMOVE: Unnecessary DuplicateCollectionError import
from ..utils import (
    get_logger,
    get_chroma_client,
    get_embedding_function,
    ValidationError,
    NumpyEncoder, # Now defined and exported from utils.__init__
)
from ..utils.config import validate_collection_name

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
# logger = get_logger("tools.document")

# --- Pydantic Input Models for Document Tools ---

# --- Add Documents Variants --- #

class AddDocumentsInput(BaseModel):
    """Input model for adding documents (auto-generates IDs, no metadata)."""
    collection_name: str = Field(..., description="Name of the collection to add documents to.")
    documents: List[str] = Field(..., description="List of document contents (strings).")
    # Keep simple optional bool
    increment_index: Optional[bool] = Field(True, description="Whether to immediately index added documents.")

    model_config = ConfigDict(extra='forbid')

class AddDocumentsWithIDsInput(BaseModel):
    """Input model for adding documents with specified IDs (no metadata)."""
    collection_name: str = Field(..., description="Name of the collection to add documents to.")
    documents: List[str] = Field(..., description="List of document contents (strings).")
    ids: List[str] = Field(..., description="List of unique IDs corresponding to the documents.")
    increment_index: Optional[bool] = Field(True, description="Whether to immediately index added documents.")

    model_config = ConfigDict(extra='forbid')

class AddDocumentsWithMetadataInput(BaseModel):
    """Input model for adding documents with specified metadata (auto-generates IDs)."""
    collection_name: str = Field(..., description="Name of the collection to add documents to.")
    documents: List[str] = Field(..., description="List of document contents (strings).")
    # Change to List[str], expect JSON strings
    metadatas: List[str] = Field(..., description="List of metadata JSON strings corresponding to the documents (e.g., ['{\"key\": \"value\"}']).")
    increment_index: Optional[bool] = Field(True, description="Whether to immediately index added documents.")

    model_config = ConfigDict(extra='forbid')

class AddDocumentsWithIDsAndMetadataInput(BaseModel):
    """Input model for adding documents with specified IDs and metadata."""
    collection_name: str = Field(..., description="Name of the collection to add documents to.")
    documents: List[str] = Field(..., description="List of document contents (strings).")
    ids: List[str] = Field(..., description="List of unique IDs corresponding to the documents.")
    # Change to List[str], expect JSON strings
    metadatas: List[str] = Field(..., description="List of metadata JSON strings corresponding to the documents (e.g., ['{\"key\": \"value\"}']).")
    increment_index: Optional[bool] = Field(True, description="Whether to immediately index added documents.")

    model_config = ConfigDict(extra='forbid')

# --- Query Documents Variants --- #

class QueryDocumentsInput(BaseModel):
    """Input model for basic querying (no filters)."""
    collection_name: str = Field(..., description="Name of the collection to query.")
    query_texts: List[str] = Field(..., description="List of query strings for semantic search.")
    n_results: Optional[int] = Field(10, ge=1, description="Maximum number of results per query.")
    include: Optional[List[str]] = Field(None, description="Optional list of fields to include (e.g., ['metadatas', 'documents', 'distances']).")

    model_config = ConfigDict(extra='forbid')

class QueryDocumentsWithWhereFilterInput(BaseModel):
    """Input model for querying with a metadata filter."""
    collection_name: str = Field(..., description="Name of the collection to query.")
    query_texts: List[str] = Field(..., description="List of query strings for semantic search.")
    where: Dict[str, Any] = Field(..., description="Metadata filter to apply (e.g., {'source': 'pdf'}).")
    n_results: Optional[int] = Field(10, ge=1, description="Maximum number of results per query.")
    include: Optional[List[str]] = Field(None, description="Optional list of fields to include.")

    model_config = ConfigDict(extra='forbid')

class QueryDocumentsWithDocumentFilterInput(BaseModel):
    """Input model for querying with a document content filter."""
    collection_name: str = Field(..., description="Name of the collection to query.")
    query_texts: List[str] = Field(..., description="List of query strings for semantic search.")
    where_document: Dict[str, Any] = Field(..., description="Document content filter to apply (e.g., {'$contains': 'keyword'}).")
    n_results: Optional[int] = Field(10, ge=1, description="Maximum number of results per query.")
    include: Optional[List[str]] = Field(None, description="Optional list of fields to include.")

    model_config = ConfigDict(extra='forbid')


# --- Get Documents Variants --- #

# Original GetDocumentsInput removed/commented out as it's replaced by variants
# class GetDocumentsInput(BaseModel):
#     collection_name: str
#     ids: Optional[List[str]] = None
#     where: Optional[Dict[str, Any]] = None
#     where_document: Optional[Dict[str, Any]] = None
#     limit: Optional[int] = Field(default=None, ge=1)
#     offset: Optional[int] = Field(default=None, ge=0)
#     include: Optional[List[str]] = None

class GetDocumentsByIdsInput(BaseModel):
    """Input model for getting documents by their specific IDs."""
    collection_name: str = Field(..., description="Name of the collection to get documents from.")
    ids: List[str] = Field(..., description="List of document IDs to retrieve.")
    include: Optional[List[str]] = Field(None, description="Optional list of fields to include.")

    model_config = ConfigDict(extra='forbid')

class GetDocumentsWithWhereFilterInput(BaseModel):
    """Input model for getting documents using a metadata filter."""
    collection_name: str = Field(..., description="Name of the collection to get documents from.")
    where: Dict[str, Any] = Field(..., description="Metadata filter to apply (e.g., {'source': 'pdf'}).")
    limit: Optional[int] = Field(None, ge=1, description="Maximum number of documents to return.")
    offset: Optional[int] = Field(None, ge=0, description="Number of documents to skip.")
    include: Optional[List[str]] = Field(None, description="Optional list of fields to include.")

    model_config = ConfigDict(extra='forbid')

class GetDocumentsWithDocumentFilterInput(BaseModel):
    """Input model for getting documents using a document content filter."""
    collection_name: str = Field(..., description="Name of the collection to get documents from.")
    where_document: Dict[str, Any] = Field(..., description="Document content filter to apply (e.g., {'$contains': 'keyword'}).")
    limit: Optional[int] = Field(None, ge=1, description="Maximum number of documents to return.")
    offset: Optional[int] = Field(None, ge=0, description="Number of documents to skip.")
    include: Optional[List[str]] = Field(None, description="Optional list of fields to include.")

    model_config = ConfigDict(extra='forbid')

class GetAllDocumentsInput(BaseModel):
    """Input model for getting all documents in a collection (potentially limited)."""
    collection_name: str = Field(..., description="Name of the collection to get all documents from.")
    limit: Optional[int] = Field(None, ge=1, description="Optional limit on the number of documents to return.")
    offset: Optional[int] = Field(None, ge=0, description="Optional number of documents to skip.")
    include: Optional[List[str]] = Field(None, description="Optional list of fields to include.")

    model_config = ConfigDict(extra='forbid')


# --- Update Documents Variants --- #

# Original UpdateDocumentsInput removed/commented out
# class UpdateDocumentsInput(BaseModel):
#     collection_name: str
#     ids: List[str]
#     documents: Optional[List[str]] = None
#     metadatas: Optional[List[Dict[str, Any]]] = None

class UpdateDocumentContentInput(BaseModel):
    """Input model for updating the content of existing documents."""
    collection_name: str = Field(..., description="Name of the collection containing the documents.")
    ids: List[str] = Field(..., description="List of document IDs to update.")
    documents: List[str] = Field(..., description="List of new document contents corresponding to the IDs.")

    model_config = ConfigDict(extra='forbid')

class UpdateDocumentMetadataInput(BaseModel):
    """Input model for updating the metadata of existing documents."""
    collection_name: str = Field(..., description="Name of the collection containing the documents.")
    ids: List[str] = Field(..., description="List of document IDs to update.")
    metadatas: List[Dict[str, Any]] = Field(..., description="List of new metadata dictionaries corresponding to the IDs.")

    model_config = ConfigDict(extra='forbid')


# --- Delete Documents Variants --- #

# Original DeleteDocumentsInput removed/commented out
# class DeleteDocumentsInput(BaseModel):
#     collection_name: str
#     ids: Optional[List[str]] = None
#     where: Optional[Dict[str, Any]] = None
#     where_document: Optional[Dict[str, Any]] = None

class DeleteDocumentsByIdsInput(BaseModel):
    """Input model for deleting documents by specific IDs."""
    collection_name: str = Field(..., description="Name of the collection to delete documents from.")
    ids: List[str] = Field(..., description="List of document IDs to delete.")

    model_config = ConfigDict(extra='forbid')

class DeleteDocumentsByWhereFilterInput(BaseModel):
    """Input model for deleting documents using a metadata filter."""
    collection_name: str = Field(..., description="Name of the collection to delete documents from.")
    where: Dict[str, Any] = Field(..., description="Metadata filter to select documents for deletion.")

    model_config = ConfigDict(extra='forbid')

class DeleteDocumentsByDocumentFilterInput(BaseModel):
    """Input model for deleting documents using a document content filter."""
    collection_name: str = Field(..., description="Name of the collection to delete documents from.")
    where_document: Dict[str, Any] = Field(..., description="Document content filter to select documents for deletion.")

    model_config = ConfigDict(extra='forbid')

# --- End Pydantic Input Models --- #

# --- Implementation Functions ---

async def _validate_add_arguments(collection, documents, ids, metadatas):
    """Internal helper to validate document/id/metadata alignment."""
    logger = get_logger("tools.document.validate_add")
    if ids and len(documents) != len(ids):
        logger.warning(f"Mismatch: {len(documents)} documents vs {len(ids)} IDs for {collection.name}.")
        raise McpError(ErrorData(code=INVALID_PARAMS, message="Number of documents and IDs must match."))
    if metadatas and len(documents) != len(metadatas):
        logger.warning(f"Mismatch: {len(documents)} documents vs {len(metadatas)} metadatas for {collection.name}.")
        raise McpError(ErrorData(code=INVALID_PARAMS, message="Number of documents and metadatas must match."))
    # Add other potential checks if needed (e.g., ID format)

# --- Add Documents Impl Variants --- #

async def _add_documents_impl(input_data: AddDocumentsInput) -> List[types.TextContent]:
    """Implementation for adding documents without specified IDs or metadata."""
    logger = get_logger("tools.document.add")
    collection_name = input_data.collection_name
    documents = input_data.documents
    increment_index = input_data.increment_index

    # --- Validation ---
    validate_collection_name(collection_name) # Added validation
    if not documents:
        raise McpError(ErrorData(code=INVALID_PARAMS, message="Documents list cannot be empty."))
    # --- End Validation ---

    logger.info(f"Adding {len(documents)} documents to '{collection_name}' (generating IDs). Increment index: {increment_index}")
    try:
        client = get_chroma_client()
        collection = client.get_collection(name=collection_name)

        # Generate unique IDs for each document
        generated_ids = [str(uuid.uuid4()) for _ in documents]
        logger.debug(f"Generated {len(generated_ids)} IDs for documents in '{collection_name}'.")

        # No need to validate IDs/Metadatas for this variant
        logger.info(f"Adding {len(documents)} documents to '{collection_name}' (auto-ID, no metadata). Increment index: {increment_index}")
        collection.add(
            documents=documents,
            ids=generated_ids, # Use the generated IDs
            metadatas=None, # Explicitly None
            # increment_index=increment_index # Chroma client seems to not have this yet
        )
        return [types.TextContent(type="text", text=f"Successfully added {len(documents)} documents with generated IDs to '{collection_name}'.")]
    except ValueError as e:
        # Handle collection not found
        if f"Collection {collection_name} does not exist" in str(e):
            logger.warning(f"Collection '{collection_name}' not found for adding documents.")
            raise McpError(ErrorData(code=INVALID_PARAMS, message=f"Collection '{collection_name}' not found."))
        else:
            logger.error(f"Value error adding documents to '{collection_name}': {e}", exc_info=True)
            raise McpError(ErrorData(code=INVALID_PARAMS, message=f"Invalid parameter adding documents: {e}"))
    except Exception as e:
        logger.error(f"Unexpected error adding documents to '{collection_name}': {e}", exc_info=True)
        raise McpError(ErrorData(code=INTERNAL_ERROR, message=f"An unexpected error occurred: {e}"))

async def _add_documents_with_ids_impl(input_data: AddDocumentsWithIDsInput) -> List[types.TextContent]:
    """Implementation for adding documents with specified IDs."""
    logger = get_logger("tools.document.add_with_ids")
    collection_name = input_data.collection_name
    documents = input_data.documents
    ids = input_data.ids
    increment_index = input_data.increment_index

    # --- Validation ---
    validate_collection_name(collection_name) # Added validation
    if not documents:
        raise McpError(ErrorData(code=INVALID_PARAMS, message="Documents list cannot be empty."))
    if len(documents) != len(ids):
        raise McpError(ErrorData(code=INVALID_PARAMS, message="Number of documents and IDs must match."))
    # --- End Validation ---

    logger.info(f"Adding {len(documents)} documents with {len(ids)} IDs to '{collection_name}'. Increment index: {increment_index}")
    try:
        client = get_chroma_client()
        collection = client.get_collection(name=collection_name)

        await _validate_add_arguments(collection, documents, ids, None)

        logger.info(f"Adding {len(documents)} documents with {len(ids)} specified IDs to '{collection_name}' (no metadata). Increment index: {increment_index}")
        collection.add(
            documents=documents,
            ids=ids,
            metadatas=None, # Explicitly None
            # increment_index=increment_index
        )
        return [types.TextContent(type="text", text=f"Successfully added {len(documents)} documents with specified IDs to '{collection_name}'.")]
    except ValueError as e:
        if f"Collection {collection_name} does not exist" in str(e):
            logger.warning(f"Collection '{collection_name}' not found.")
            raise McpError(ErrorData(code=INVALID_PARAMS, message=f"Collection '{collection_name}' not found."))
        else:
            logger.error(f"Value error: {e}", exc_info=True)
            raise McpError(ErrorData(code=INVALID_PARAMS, message=f"Invalid parameter: {e}"))
    except McpError: # Re-raise validation errors
        raise
    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)
        raise McpError(ErrorData(code=INTERNAL_ERROR, message=f"An unexpected error occurred: {e}"))

async def _add_documents_with_metadata_impl(input_data: AddDocumentsWithMetadataInput) -> List[types.TextContent]:
    """Implementation for adding documents with metadata (auto-IDs)."""
    logger = get_logger("tools.document.add_with_metadata")
    collection_name = input_data.collection_name
    documents = input_data.documents
    # metadatas is now List[str]
    metadatas_str_list = input_data.metadatas
    increment_index = input_data.increment_index

    # --- Validation ---
    validate_collection_name(collection_name) # Added validation
    if not documents:
        raise McpError(ErrorData(code=INVALID_PARAMS, message="Documents list cannot be empty."))
    if len(documents) != len(metadatas_str_list):
        raise McpError(ErrorData(code=INVALID_PARAMS, message="Number of documents and metadatas must match."))

    # --- Parse Metadata JSON Strings ---
    parsed_metadatas = []
    for i, meta_str in enumerate(metadatas_str_list):
        try:
            parsed_meta = json.loads(meta_str)
            if not isinstance(parsed_meta, dict):
                raise ValueError("Metadata string must decode to a JSON object (dictionary).")
            parsed_metadatas.append(parsed_meta)
        except json.JSONDecodeError as e:
            logger.warning(f"Failed to parse metadata JSON string at index {i} for '{collection_name}': {e}")
            raise McpError(ErrorData(code=INVALID_PARAMS, message=f"Invalid JSON format for metadata string at index {i}: {str(e)}"))
        except ValueError as e: # Catch the isinstance check
            logger.warning(f"Metadata at index {i} did not decode to a dictionary for '{collection_name}': {e}")
            raise McpError(ErrorData(code=INVALID_PARAMS, message=f"Metadata string at index {i} did not decode to a dictionary: {str(e)}"))
    # --- End Parsing ---

    logger.info(f"Adding {len(documents)} documents with parsed metadata to '{collection_name}' (auto-IDs). Increment index: {increment_index}")
    try:
        client = get_chroma_client()
        collection = client.get_collection(name=collection_name)

        # Validation using parsed_metadatas length is implicitly done by the length check above
        # await _validate_add_arguments(collection, documents, None, parsed_metadatas)

        logger.info(f"Adding {len(documents)} documents with specified metadata to '{collection_name}' (auto-ID). Increment index: {increment_index}")
        collection.add(
            documents=documents,
            ids=None, # Explicitly None
            metadatas=parsed_metadatas, # Use the parsed list of dicts
            # increment_index=increment_index
        )
        return [types.TextContent(type="text", text=f"Successfully added {len(documents)} documents with specified metadata to '{collection_name}'.")]
    except ValueError as e:
        if f"Collection {collection_name} does not exist" in str(e):
            logger.warning(f"Collection '{collection_name}' not found.")
            raise McpError(ErrorData(code=INVALID_PARAMS, message=f"Collection '{collection_name}' not found."))
        else:
            logger.error(f"Value error: {e}", exc_info=True)
            raise McpError(ErrorData(code=INVALID_PARAMS, message=f"Invalid parameter: {e}"))
    except McpError: # Re-raise validation errors
        raise
    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)
        raise McpError(ErrorData(code=INTERNAL_ERROR, message=f"An unexpected error occurred: {e}"))

async def _add_documents_with_ids_and_metadata_impl(input_data: AddDocumentsWithIDsAndMetadataInput) -> List[types.TextContent]:
    """Implementation for adding documents with specified IDs and metadata."""
    logger = get_logger("tools.document.add_full")
    collection_name = input_data.collection_name
    documents = input_data.documents
    ids = input_data.ids
    # metadatas is now List[str]
    metadatas_str_list = input_data.metadatas
    increment_index = input_data.increment_index

    # --- Validation ---
    validate_collection_name(collection_name) # Added validation
    if not documents:
        raise McpError(ErrorData(code=INVALID_PARAMS, message="Documents list cannot be empty."))
    if len(documents) != len(ids):
        raise McpError(ErrorData(code=INVALID_PARAMS, message="Number of documents and IDs must match."))
    if len(documents) != len(metadatas_str_list):
        raise McpError(ErrorData(code=INVALID_PARAMS, message="Number of documents and metadatas must match."))

    # --- Parse Metadata JSON Strings ---
    parsed_metadatas = []
    for i, meta_str in enumerate(metadatas_str_list):
        try:
            parsed_meta = json.loads(meta_str)
            if not isinstance(parsed_meta, dict):
                raise ValueError("Metadata string must decode to a JSON object (dictionary).")
            parsed_metadatas.append(parsed_meta)
        except json.JSONDecodeError as e:
            logger.warning(f"Failed to parse metadata JSON string at index {i} for '{collection_name}': {e}")
            raise McpError(ErrorData(code=INVALID_PARAMS, message=f"Invalid JSON format for metadata string at index {i}: {str(e)}"))
        except ValueError as e: # Catch the isinstance check
            logger.warning(f"Metadata at index {i} did not decode to a dictionary for '{collection_name}': {e}")
            raise McpError(ErrorData(code=INVALID_PARAMS, message=f"Metadata string at index {i} did not decode to a dictionary: {str(e)}"))
    # --- End Parsing ---

    logger.info(f"Adding {len(documents)} documents with {len(ids)} IDs and parsed metadata to '{collection_name}'. Increment index: {increment_index}")
    try:
        client = get_chroma_client()
        collection = client.get_collection(name=collection_name)

        # Validation using parsed_metadatas length is implicitly done by the length check above
        # await _validate_add_arguments(collection, documents, ids, parsed_metadatas)

        logger.info(f"Adding {len(documents)} documents with specified IDs and metadata to '{collection_name}'. Increment index: {increment_index}")
        collection.add(
            documents=documents,
            ids=ids,
            metadatas=parsed_metadatas, # Use the parsed list of dicts
            # increment_index=increment_index
        )
        return [types.TextContent(type="text", text=f"Successfully added {len(documents)} documents with specified IDs and metadata to '{collection_name}'.")]
    except ValueError as e:
        if f"Collection {collection_name} does not exist" in str(e):
            logger.warning(f"Collection '{collection_name}' not found.")
            raise McpError(ErrorData(code=INVALID_PARAMS, message=f"Collection '{collection_name}' not found."))
        else:
            logger.error(f"Value error: {e}", exc_info=True)
            raise McpError(ErrorData(code=INVALID_PARAMS, message=f"Invalid parameter: {e}"))
    except McpError: # Re-raise validation errors
        raise
    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)
        raise McpError(ErrorData(code=INTERNAL_ERROR, message=f"An unexpected error occurred: {e}"))

# --- End Add Document Impl Variants --- #

# --- Query Documents Impl Variants --- #

async def _query_documents_impl(input_data: QueryDocumentsInput) -> List[types.TextContent]:
    """Implementation for basic document query."""
    logger = get_logger("tools.document.query")
    collection_name = input_data.collection_name
    query_texts = input_data.query_texts
    n_results = input_data.n_results if input_data.n_results is not None else DEFAULT_QUERY_N_RESULTS
    include = input_data.include

    # --- Validation ---
    validate_collection_name(collection_name) # Added validation
    if not query_texts:
        raise McpError(ErrorData(code=INVALID_PARAMS, message="Query texts list cannot be empty."))
    # --- End Validation ---

    logger.info(f"Querying '{collection_name}' with {len(query_texts)} texts, n_results={n_results}. Include: {include}")
    try:
        client = get_chroma_client()
        collection = client.get_collection(name=collection_name)

        logger.info(f"Querying {len(query_texts)} texts in '{collection_name}' (no filters). N_results: {n_results}, Include: {include}")
        results: QueryResult = collection.query(
            query_texts=query_texts,
            n_results=n_results,
            where=None, # Explicitly None
            where_document=None, # Explicitly None
            include=include or [], # Pass include or empty list if None
        )

        # Ensure results are JSON serializable (handle numpy arrays)
        serialized_results = json.dumps(results, cls=NumpyEncoder)
        return [types.TextContent(type="text", text=serialized_results)]

    except ValueError as e:
        if f"Collection {collection_name} does not exist" in str(e):
            logger.warning(f"Collection '{collection_name}' not found for query.")
            raise McpError(ErrorData(code=INVALID_PARAMS, message=f"Collection '{collection_name}' not found."))
        else:
            logger.error(f"Value error querying '{collection_name}': {e}", exc_info=True)
            raise McpError(ErrorData(code=INVALID_PARAMS, message=f"Invalid parameter during query: {e}"))
    except Exception as e:
        logger.error(f"Unexpected error querying '{collection_name}': {e}", exc_info=True)
        raise McpError(ErrorData(code=INTERNAL_ERROR, message=f"An unexpected error occurred during query: {e}"))

async def _query_documents_with_where_filter_impl(input_data: QueryDocumentsWithWhereFilterInput) -> List[types.TextContent]:
    """Implementation for querying documents with a metadata filter."""
    logger = get_logger("tools.document.query_where")
    collection_name = input_data.collection_name
    query_texts = input_data.query_texts
    where = input_data.where
    n_results = input_data.n_results if input_data.n_results is not None else DEFAULT_QUERY_N_RESULTS
    include = input_data.include

    # --- Validation ---
    validate_collection_name(collection_name) # Added validation
    if not query_texts:
        raise McpError(ErrorData(code=INVALID_PARAMS, message="Query texts list cannot be empty."))
    if not where: # where is required by Pydantic, but check anyway
        raise McpError(ErrorData(code=INVALID_PARAMS, message="Where filter cannot be empty for this tool variant."))
    # --- End Validation ---

    logger.info(f"Querying '{collection_name}' with {len(query_texts)} texts, WHERE filter, n_results={n_results}. Include: {include}")
    try:
        client = get_chroma_client()
        collection = client.get_collection(name=collection_name)

        logger.info(f"Querying {len(query_texts)} texts in '{collection_name}' with WHERE filter. N_results: {n_results}, Include: {include}")
        results: QueryResult = collection.query(
            query_texts=query_texts,
            n_results=n_results,
            where=where,
            where_document=None, # Explicitly None
            include=include or [],
        )

        serialized_results = json.dumps(results, cls=NumpyEncoder)
        return [types.TextContent(type="text", text=serialized_results)]

    except ValueError as e:
        if f"Collection {collection_name} does not exist" in str(e):
            logger.warning(f"Collection '{collection_name}' not found for query.")
            raise McpError(ErrorData(code=INVALID_PARAMS, message=f"Collection '{collection_name}' not found."))
        else:
            logger.error(f"Value error querying '{collection_name}': {e}", exc_info=True)
            raise McpError(ErrorData(code=INVALID_PARAMS, message=f"Invalid parameter during query: {e}"))
    except Exception as e:
        logger.error(f"Unexpected error querying '{collection_name}': {e}", exc_info=True)
        raise McpError(ErrorData(code=INTERNAL_ERROR, message=f"An unexpected error occurred during query: {e}"))

async def _query_documents_with_document_filter_impl(input_data: QueryDocumentsWithDocumentFilterInput) -> List[types.TextContent]:
    """Implementation for querying documents with a document content filter."""
    logger = get_logger("tools.document.query_where_doc")
    collection_name = input_data.collection_name
    query_texts = input_data.query_texts
    where_document = input_data.where_document
    n_results = input_data.n_results if input_data.n_results is not None else DEFAULT_QUERY_N_RESULTS
    include = input_data.include

    # --- Validation ---
    validate_collection_name(collection_name) # Added validation
    if not query_texts:
        raise McpError(ErrorData(code=INVALID_PARAMS, message="Query texts list cannot be empty."))
    if not where_document: # where_document is required by Pydantic, but check anyway
        raise McpError(ErrorData(code=INVALID_PARAMS, message="Where document filter cannot be empty for this tool variant."))
    # --- End Validation ---

    logger.info(f"Querying '{collection_name}' with {len(query_texts)} texts, WHERE_DOCUMENT filter, n_results={n_results}. Include: {include}")
    try:
        client = get_chroma_client()
        collection = client.get_collection(name=collection_name)

        logger.info(f"Querying {len(query_texts)} texts in '{collection_name}' with document filter. N_results: {n_results}, Include: {include}")
        results: QueryResult = collection.query(
            query_texts=query_texts,
            n_results=n_results,
            where=None, # Explicitly None
            where_document=where_document,
            include=include or [],
        )

        serialized_results = json.dumps(results, cls=NumpyEncoder)
        return [types.TextContent(type="text", text=serialized_results)]

    except ValueError as e:
        if f"Collection {collection_name} does not exist" in str(e):
            logger.warning(f"Collection '{collection_name}' not found for query.")
            raise McpError(ErrorData(code=INVALID_PARAMS, message=f"Collection '{collection_name}' not found."))
        else:
            logger.error(f"Value error querying '{collection_name}': {e}", exc_info=True)
            raise McpError(ErrorData(code=INVALID_PARAMS, message=f"Invalid parameter during query: {e}"))
    except Exception as e:
        logger.error(f"Unexpected error querying '{collection_name}': {e}", exc_info=True)
        raise McpError(ErrorData(code=INTERNAL_ERROR, message=f"An unexpected error occurred during query: {e}"))

# --- End Query Document Impl Variants --- #

# --- Get Documents Impl Variants --- #

async def _get_documents_by_ids_impl(input_data: GetDocumentsByIdsInput) -> List[types.TextContent]:
    """Implementation for getting documents by IDs."""
    logger = get_logger("tools.document.get_by_ids")
    collection_name = input_data.collection_name
    ids = input_data.ids
    include = input_data.include

    # --- Validation ---
    validate_collection_name(collection_name) # Added validation
    if not ids: # Added check for empty list
        raise McpError(ErrorData(code=INVALID_PARAMS, message="IDs list cannot be empty for get_documents_by_ids."))
    # --- End Validation ---

    logger.info(f"Getting {len(ids)} documents by ID from '{collection_name}'. Include: {include}")
    try:
        client = get_chroma_client()
        collection = client.get_collection(name=collection_name)

        logger.info(f"Getting {len(ids)} documents by ID from '{collection_name}'. Include: {include}")
        results: GetResult = collection.get(
            ids=ids,
            where=None,
            where_document=None,
            limit=None, # Limit/offset not applicable when getting by specific ID
            offset=None,
            include=include or [],
        )

        serialized_results = json.dumps(results, cls=NumpyEncoder)
        return [types.TextContent(type="text", text=serialized_results)]

    except ValueError as e:
        if f"Collection {collection_name} does not exist" in str(e):
            logger.warning(f"Collection '{collection_name}' not found for get.")
            raise McpError(ErrorData(code=INVALID_PARAMS, message=f"Collection '{collection_name}' not found."))
        else:
            logger.error(f"Value error getting documents from '{collection_name}': {e}", exc_info=True)
            raise McpError(ErrorData(code=INVALID_PARAMS, message=f"Invalid parameter during get: {e}"))
    except Exception as e:
        logger.error(f"Unexpected error getting documents from '{collection_name}': {e}", exc_info=True)
        raise McpError(ErrorData(code=INTERNAL_ERROR, message=f"An unexpected error occurred during get: {e}"))

async def _get_documents_with_where_filter_impl(input_data: GetDocumentsWithWhereFilterInput) -> List[types.TextContent]:
    """Implementation for getting documents using a metadata filter."""
    logger = get_logger("tools.document.get_where")
    collection_name = input_data.collection_name
    where = input_data.where
    limit = input_data.limit
    offset = input_data.offset
    include = input_data.include

    # --- Validation ---
    validate_collection_name(collection_name) # Added validation
    if not where: # Required by Pydantic, but check
         raise McpError(ErrorData(code=INVALID_PARAMS, message="Where filter cannot be empty for this tool variant."))
    # --- End Validation ---

    log_limit_offset = f" Limit: {limit}, Offset: {offset}" if limit or offset is not None else ""
    logger.info(f"Getting documents from '{collection_name}' using WHERE filter.{log_limit_offset} Include: {include}")
    try:
        client = get_chroma_client()
        collection = client.get_collection(name=collection_name)

        logger.info(f"Getting documents from '{collection_name}' with WHERE filter. Limit: {limit}, Offset: {offset}, Include: {include}")
        results: GetResult = collection.get(
            ids=None,
            where=where,
            where_document=None,
            limit=limit,
            offset=offset,
            include=include or [],
        )

        serialized_results = json.dumps(results, cls=NumpyEncoder)
        return [types.TextContent(type="text", text=serialized_results)]

    except ValueError as e:
        if f"Collection {collection_name} does not exist" in str(e):
            logger.warning(f"Collection '{collection_name}' not found for get.")
            raise McpError(ErrorData(code=INVALID_PARAMS, message=f"Collection '{collection_name}' not found."))
        else:
            logger.error(f"Value error getting documents from '{collection_name}': {e}", exc_info=True)
            raise McpError(ErrorData(code=INVALID_PARAMS, message=f"Invalid parameter during get: {e}"))
    except Exception as e:
        logger.error(f"Unexpected error getting documents from '{collection_name}': {e}", exc_info=True)
        raise McpError(ErrorData(code=INTERNAL_ERROR, message=f"An unexpected error occurred during get: {e}"))

async def _get_documents_with_document_filter_impl(input_data: GetDocumentsWithDocumentFilterInput) -> List[types.TextContent]:
    """Implementation for getting documents using a document content filter."""
    logger = get_logger("tools.document.get_where_doc")
    collection_name = input_data.collection_name
    where_document = input_data.where_document
    limit = input_data.limit
    offset = input_data.offset
    include = input_data.include

    # --- Validation ---
    validate_collection_name(collection_name) # Added validation
    if not where_document: # Required by Pydantic, but check
        raise McpError(ErrorData(code=INVALID_PARAMS, message="Where document filter cannot be empty for this tool variant."))
    # --- End Validation ---

    log_limit_offset = f" Limit: {limit}, Offset: {offset}" if limit or offset is not None else ""
    logger.info(f"Getting documents from '{collection_name}' using WHERE_DOCUMENT filter.{log_limit_offset} Include: {include}")
    try:
        client = get_chroma_client()
        collection = client.get_collection(name=collection_name)

        logger.info(f"Getting documents from '{collection_name}' with document filter. Limit: {limit}, Offset: {offset}, Include: {include}")
        results: GetResult = collection.get(
            ids=None,
            where=None,
            where_document=where_document,
            limit=limit,
            offset=offset,
            include=include or [],
        )

        serialized_results = json.dumps(results, cls=NumpyEncoder)
        return [types.TextContent(type="text", text=serialized_results)]

    except ValueError as e:
        if f"Collection {collection_name} does not exist" in str(e):
            logger.warning(f"Collection '{collection_name}' not found for get.")
            raise McpError(ErrorData(code=INVALID_PARAMS, message=f"Collection '{collection_name}' not found."))
        else:
            logger.error(f"Value error getting documents from '{collection_name}': {e}", exc_info=True)
            raise McpError(ErrorData(code=INVALID_PARAMS, message=f"Invalid parameter during get: {e}"))
    except Exception as e:
        logger.error(f"Unexpected error getting documents from '{collection_name}': {e}", exc_info=True)
        raise McpError(ErrorData(code=INTERNAL_ERROR, message=f"An unexpected error occurred during get: {e}"))

async def _get_all_documents_impl(input_data: GetAllDocumentsInput) -> List[types.TextContent]:
    """Implementation for getting all documents (potentially limited)."""
    logger = get_logger("tools.document.get_all")
    collection_name = input_data.collection_name
    limit = input_data.limit
    offset = input_data.offset
    include = input_data.include

    # --- Validation ---
    validate_collection_name(collection_name) # Added validation
    # No specific filter validation needed here
    # --- End Validation ---

    log_limit_offset = f" Limit: {limit}, Offset: {offset}" if limit or offset is not None else ""
    logger.info(f"Getting all documents from '{collection_name}'.{log_limit_offset} Include: {include}")
    try:
        client = get_chroma_client()
        collection = client.get_collection(name=collection_name)

        logger.info(f"Getting all documents from '{collection_name}'. Limit: {limit}, Offset: {offset}, Include: {include}")
        results: GetResult = collection.get(
            ids=None,
            where=None,
            where_document=None,
            limit=limit,
            offset=offset,
            include=include or [],
        )

        serialized_results = json.dumps(results, cls=NumpyEncoder)
        return [types.TextContent(type="text", text=serialized_results)]

    except ValueError as e:
        if f"Collection {collection_name} does not exist" in str(e):
            logger.warning(f"Collection '{collection_name}' not found for get.")
            raise McpError(ErrorData(code=INVALID_PARAMS, message=f"Collection '{collection_name}' not found."))
        else:
            logger.error(f"Value error getting documents from '{collection_name}': {e}", exc_info=True)
            raise McpError(ErrorData(code=INVALID_PARAMS, message=f"Invalid parameter during get: {e}"))
    except Exception as e:
        logger.error(f"Unexpected error getting documents from '{collection_name}': {e}", exc_info=True)
        raise McpError(ErrorData(code=INTERNAL_ERROR, message=f"An unexpected error occurred during get: {e}"))


# --- End Get Document Impl Variants --- #

# --- Update Documents Impl Variants --- #

async def _update_document_content_impl(input_data: UpdateDocumentContentInput) -> List[types.TextContent]:
    """Implementation for updating document content."""
    logger = get_logger("tools.document.update_content")
    collection_name = input_data.collection_name
    ids = input_data.ids
    documents = input_data.documents

    # --- Validation ---
    validate_collection_name(collection_name) # Added validation
    if not ids:
        raise McpError(ErrorData(code=INVALID_PARAMS, message="IDs list cannot be empty for update."))
    if not documents:
        raise McpError(ErrorData(code=INVALID_PARAMS, message="Documents list cannot be empty for update."))
    if len(ids) != len(documents):
        logger.warning(f"Validation error updating documents in '{collection_name}': Number of documents must match number of IDs")
        raise McpError(ErrorData(code=INVALID_PARAMS, message="Number of documents must match number of IDs"))
    # --- End Validation ---

    logger.info(f"Updating content for {len(ids)} documents in '{collection_name}'.")
    try:
        client = get_chroma_client()
        collection = client.get_collection(name=collection_name)

        logger.info(f"Updating content for {len(ids)} documents in '{collection_name}'.")
        collection.update(ids=ids, documents=documents, metadatas=None)

        return [types.TextContent(type="text", text=f"Successfully updated content for {len(ids)} documents in '{collection_name}'.")]

    except ValidationError as e:
        logger.warning(f"Validation error updating documents in '{collection_name}': {e}")
        raise McpError(ErrorData(code=INVALID_PARAMS, message=f"Validation Error: {str(e)}"))
    except ValueError as e:
        if f"Collection {collection_name} does not exist" in str(e):
            logger.warning(f"Collection '{collection_name}' not found for update.")
            raise McpError(ErrorData(code=INVALID_PARAMS, message=f"Collection '{collection_name}' not found."))
        else:
            logger.error(f"Value error updating documents in '{collection_name}': {e}", exc_info=True)
            raise McpError(ErrorData(code=INTERNAL_ERROR, message=f"Tool Error: Unexpected value error during update. Details: {e}"))
    except Exception as e:
        logger.error(f"Unexpected error updating documents in '{collection_name}': {e}", exc_info=True)
        raise McpError(ErrorData(code=INTERNAL_ERROR, message=f"ChromaDB Error: Failed to update documents. {str(e)}"))

async def _update_document_metadata_impl(input_data: UpdateDocumentMetadataInput) -> List[types.TextContent]:
    """Implementation for updating document metadata."""
    logger = get_logger("tools.document.update_metadata")
    collection_name = input_data.collection_name
    ids = input_data.ids
    metadatas = input_data.metadatas

    # --- Validation ---
    validate_collection_name(collection_name) # Added validation
    if not ids:
        raise McpError(ErrorData(code=INVALID_PARAMS, message="IDs list cannot be empty for update."))
    if not metadatas:
        raise McpError(ErrorData(code=INVALID_PARAMS, message="Metadatas list cannot be empty for update."))
    if len(ids) != len(metadatas):
        logger.warning(f"Validation error updating metadata in '{collection_name}': Number of metadatas must match number of IDs")
        raise McpError(ErrorData(code=INVALID_PARAMS, message="Number of metadatas must match number of IDs"))
    # --- End Validation ---

    logger.info(f"Updating metadata for {len(ids)} documents in '{collection_name}'.")
    try:
        client = get_chroma_client()
        collection = client.get_collection(name=collection_name)

        logger.info(f"Updating metadata for {len(ids)} documents in '{collection_name}'.")
        collection.update(ids=ids, documents=None, metadatas=metadatas)

        return [types.TextContent(type="text", text=f"Successfully updated metadata for {len(ids)} documents in '{collection_name}'.")]

    except ValidationError as e:
        logger.warning(f"Validation error updating documents in '{collection_name}': {e}")
        raise McpError(ErrorData(code=INVALID_PARAMS, message=f"Validation Error: {str(e)}"))
    except ValueError as e:
        if f"Collection {collection_name} does not exist" in str(e):
            logger.warning(f"Collection '{collection_name}' not found for update.")
            raise McpError(ErrorData(code=INVALID_PARAMS, message=f"Collection '{collection_name}' not found."))
        else:
            logger.error(f"Value error updating documents in '{collection_name}': {e}", exc_info=True)
            raise McpError(ErrorData(code=INTERNAL_ERROR, message=f"Tool Error: Unexpected value error during update. Details: {e}"))
    except Exception as e:
        logger.error(f"Unexpected error updating documents in '{collection_name}': {e}", exc_info=True)
        raise McpError(ErrorData(code=INTERNAL_ERROR, message=f"ChromaDB Error: Failed to update document metadata. {str(e)}"))

# --- End Update Document Impl Variants --- #

# --- Delete Documents Impl Variants --- #

async def _delete_documents_by_ids_impl(input_data: DeleteDocumentsByIdsInput) -> List[types.TextContent]:
    """Implementation for deleting documents by IDs."""
    logger = get_logger("tools.document.delete_by_ids")
    collection_name = input_data.collection_name
    ids = input_data.ids

    # --- Validation ---
    validate_collection_name(collection_name) # Added validation
    if not ids: # Added check for empty list
        raise McpError(ErrorData(code=INVALID_PARAMS, message="IDs list cannot be empty for delete_documents_by_ids."))
    # --- End Validation ---

    logger.info(f"Deleting {len(ids)} documents by ID from '{collection_name}'.")
    try:
        client = get_chroma_client()
        collection = client.get_collection(name=collection_name)

        logger.info(f"Deleting {len(ids)} documents by ID from '{collection_name}'.")
        # Chroma's delete returns the list of IDs provided for deletion
        deleted_ids_list = collection.delete(ids=ids, where=None, where_document=None)

        return [
            types.TextContent(
                type="text",
                text=json.dumps({"deleted_ids": deleted_ids_list if deleted_ids_list else []}),
            )
        ]

    except ValueError as e:
        if f"Collection {collection_name} does not exist" in str(e):
            logger.warning(f"Collection '{collection_name}' not found for delete.")
            raise McpError(ErrorData(code=INVALID_PARAMS, message=f"Collection '{collection_name}' not found."))
        else:
            logger.error(f"Value error deleting documents from '{collection_name}': {e}", exc_info=True)
            raise McpError(ErrorData(code=INTERNAL_ERROR, message=f"Tool Error: Unexpected value error during delete. Details: {e}"))
    except Exception as e:
        logger.error(f"Unexpected error deleting documents from '{collection_name}': {e}", exc_info=True)
        raise McpError(ErrorData(code=INTERNAL_ERROR, message=f"ChromaDB Error: Failed to delete documents. {str(e)}"))

async def _delete_documents_by_where_filter_impl(input_data: DeleteDocumentsByWhereFilterInput) -> List[types.TextContent]:
    """Implementation for deleting documents using a metadata filter."""
    logger = get_logger("tools.document.delete_where")
    collection_name = input_data.collection_name
    where = input_data.where

    # --- Validation ---
    validate_collection_name(collection_name) # Added validation
    if not where: # Required by Pydantic, but check
        raise McpError(ErrorData(code=INVALID_PARAMS, message="Where filter cannot be empty for this tool variant."))
    # --- End Validation ---

    logger.info(f"Deleting documents from '{collection_name}' using WHERE filter: {where}")
    try:
        client = get_chroma_client()
        collection = client.get_collection(name=collection_name)

        logger.info(f"Deleting documents from '{collection_name}' using WHERE filter: {where}")
        deleted_ids_list = collection.delete(ids=None, where=where, where_document=None)

        return [
            types.TextContent(
                type="text",
                text=json.dumps({"deleted_ids": deleted_ids_list if deleted_ids_list else []}),
            )
        ]

    except ValueError as e:
        if f"Collection {collection_name} does not exist" in str(e):
            logger.warning(f"Collection '{collection_name}' not found for delete.")
            raise McpError(ErrorData(code=INVALID_PARAMS, message=f"Collection '{collection_name}' not found."))
        else:
            logger.error(f"Value error deleting documents from '{collection_name}': {e}", exc_info=True)
            raise McpError(ErrorData(code=INTERNAL_ERROR, message=f"Tool Error: Unexpected value error during delete. Details: {e}"))
    except Exception as e:
        logger.error(f"Unexpected error deleting documents from '{collection_name}': {e}", exc_info=True)
        raise McpError(ErrorData(code=INTERNAL_ERROR, message=f"ChromaDB Error: Failed to delete documents using WHERE filter. {str(e)}"))

async def _delete_documents_by_document_filter_impl(input_data: DeleteDocumentsByDocumentFilterInput) -> List[types.TextContent]:
    """Implementation for deleting documents using a document content filter."""
    logger = get_logger("tools.document.delete_where_doc")
    collection_name = input_data.collection_name
    where_document = input_data.where_document

    # --- Validation ---
    validate_collection_name(collection_name) # Added validation
    if not where_document: # Required by Pydantic, but check
        raise McpError(ErrorData(code=INVALID_PARAMS, message="Where document filter cannot be empty for this tool variant."))
    # --- End Validation ---

    logger.info(f"Deleting documents from '{collection_name}' using WHERE_DOCUMENT filter: {where_document}")
    try:
        client = get_chroma_client()
        collection = client.get_collection(name=collection_name)

        logger.info(f"Deleting documents from '{collection_name}' using WHERE_DOCUMENT filter: {where_document}")
        deleted_ids_list = collection.delete(ids=None, where=None, where_document=where_document)

        return [
            types.TextContent(
                type="text",
                text=json.dumps({"deleted_ids": deleted_ids_list if deleted_ids_list else []}),
            )
        ]

    except ValueError as e:
        if f"Collection {collection_name} does not exist" in str(e):
            logger.warning(f"Collection '{collection_name}' not found for delete.")
            raise McpError(ErrorData(code=INVALID_PARAMS, message=f"Collection '{collection_name}' not found."))
        else:
            logger.error(f"Value error deleting documents from '{collection_name}': {e}", exc_info=True)
            raise McpError(ErrorData(code=INTERNAL_ERROR, message=f"Tool Error: Unexpected value error during delete. Details: {e}"))
    except Exception as e:
        logger.error(f"Unexpected error deleting documents from '{collection_name}': {e}", exc_info=True)
        raise McpError(ErrorData(code=INTERNAL_ERROR, message=f"ChromaDB Error: Failed to delete documents using WHERE_DOCUMENT filter. {str(e)}"))

# --- End Delete Document Impl Variants --- #
