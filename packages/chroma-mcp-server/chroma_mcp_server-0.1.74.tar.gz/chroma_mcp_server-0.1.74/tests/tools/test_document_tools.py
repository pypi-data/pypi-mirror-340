"""Tests for document management tools."""

import pytest
import uuid
import time  # Import time for ID generation check
import json
import re
import numpy as np

from typing import Dict, Any, List, Optional
from unittest.mock import patch, MagicMock, ANY, call, AsyncMock
from contextlib import contextmanager # Import contextmanager

# Import CallToolResult and TextContent for helpers
from mcp import types
from mcp.types import ErrorData, INTERNAL_ERROR, INVALID_PARAMS
from mcp.shared.exceptions import McpError

# Keep only ValidationError from errors module
from src.chroma_mcp.utils.errors import ValidationError
from src.chroma_mcp.tools import document_tools

# Import the implementation functions directly - Updated for variants
from src.chroma_mcp.tools.document_tools import (
    # Add variants
    _add_documents_impl,
    _add_documents_with_ids_impl,
    _add_documents_with_metadata_impl,
    _add_documents_with_ids_and_metadata_impl,
    # Query variants
    _query_documents_impl,
    _query_documents_with_where_filter_impl,
    _query_documents_with_document_filter_impl,
    # Get variants (replace old _get_documents_impl)
    _get_documents_by_ids_impl,
    _get_documents_with_where_filter_impl,
    _get_documents_with_document_filter_impl,
    _get_all_documents_impl,
    # Update variants (replace old _update_documents_impl)
    _update_document_content_impl,
    _update_document_metadata_impl,
    # Delete variants (replace old _delete_documents_impl)
    _delete_documents_by_ids_impl,
    _delete_documents_by_where_filter_impl,
    _delete_documents_by_document_filter_impl,
)

# Import Pydantic models - Updated for variants
from src.chroma_mcp.tools.document_tools import (
    # Add variants
    AddDocumentsInput,
    AddDocumentsWithIDsInput,
    AddDocumentsWithMetadataInput,
    AddDocumentsWithIDsAndMetadataInput,
    # Query variants
    QueryDocumentsInput,
    QueryDocumentsWithWhereFilterInput,
    QueryDocumentsWithDocumentFilterInput,
    # Get variants (replace old GetDocumentsInput)
    GetDocumentsByIdsInput,
    GetDocumentsWithWhereFilterInput,
    GetDocumentsWithDocumentFilterInput,
    GetAllDocumentsInput,
    # Update variants (replace old UpdateDocumentsInput)
    UpdateDocumentContentInput,
    UpdateDocumentMetadataInput,
    # Delete variants (replace old DeleteDocumentsInput)
    DeleteDocumentsByIdsInput,
    DeleteDocumentsByWhereFilterInput,
    DeleteDocumentsByDocumentFilterInput,
)

# Import Chroma exceptions used in mocking
from chromadb.errors import InvalidDimensionException # No longer needed

# Import necessary helpers from utils
from src.chroma_mcp.utils.config import get_collection_settings # Not used here
from src.chroma_mcp.utils import get_logger, get_chroma_client, get_embedding_function, ValidationError
from src.chroma_mcp.utils.config import validate_collection_name

DEFAULT_SIMILARITY_THRESHOLD = 0.7

# --- Helper Functions (Consider moving to a shared conftest.py) ---

def assert_successful_json_result(
    result: List[types.TextContent],
    expected_data: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """Asserts the tool result is a successful list containing valid JSON, returning the parsed data."""
    assert isinstance(result, list)
    assert len(result) > 0, "Result list cannot be empty for successful JSON result."
    content_item = result[0]
    assert isinstance(content_item, types.TextContent), f"Expected TextContent, got {type(content_item)}"
    assert content_item.type == "text", f"Expected content type 'text', got '{content_item.type}'"
    assert content_item.text is not None, "Text content cannot be None for JSON result."
    try:
        parsed_data = json.loads(content_item.text)
        assert isinstance(parsed_data, dict), f"Parsed JSON is not a dictionary, got {type(parsed_data)}"
    except (json.JSONDecodeError, AssertionError) as e:
        pytest.fail(f"Result content is not valid JSON: {e}\nContent: {content_item.text}")
    if expected_data is not None:
        # Basic check: Ensure all keys in expected_data exist in parsed_data
        # More thorough checks might be needed depending on the tool
        for key in expected_data:
            assert key in parsed_data, f"Expected key '{key}' not found in result JSON"
            # Optionally add value comparison: assert parsed_data[key] == expected_data[key]
    return parsed_data

# Define the helper context manager for McpError
@contextmanager
def assert_raises_mcp_error(expected_error_substring: Optional[str] = None):
    """Asserts that McpError is raised and optionally checks the error message."""
    with pytest.raises(McpError) as exc_info:
        yield # Code under test executes here

    # After the block, check the exception details
    error_message = str(exc_info.value) # Use the string representation of the exception
    # print(f"DEBUG: Caught McpError message: {error_message}") # Keep commented out for now
    if expected_error_substring:
        assert expected_error_substring.lower() in error_message.lower(), \
               f"Expected substring '{expected_error_substring}' not found in error message '{error_message}'"

# --- End Helper Functions ---


# Fixture to mock client and collection for document tools
@pytest.fixture
def mock_chroma_client_document():
    """Fixture to mock Chroma client, collection, and helpers for document tests."""
    with patch("src.chroma_mcp.tools.document_tools.get_chroma_client") as mock_get_client, patch(
        "src.chroma_mcp.tools.document_tools.get_embedding_function"
    ) as mock_get_embedding_function, patch(
        "src.chroma_mcp.tools.document_tools.validate_collection_name"
    ) as mock_validate_name:
        # Use AsyncMock for the client and collection methods if they are awaited
        # But the underlying Chroma client is synchronous, so MagicMock is appropriate
        mock_client_instance = MagicMock()
        mock_collection_instance = MagicMock(name="document_collection") # Name for clarity

        # Configure default behaviors for collection methods
        mock_collection_instance.add.return_value = None # add returns None
        mock_collection_instance.query.return_value = { # Default empty query result
             "ids": [], "distances": [], "metadatas": [], "embeddings": [], "documents": [], "uris": [], "data": None
        }
        mock_collection_instance.get.return_value = { # Default empty get result
             "ids": [], "metadatas": [], "embeddings": [], "documents": [], "uris": [], "data": None
        }
        mock_collection_instance.update.return_value = None # update returns None
        mock_collection_instance.delete.return_value = [] # delete returns list of deleted IDs
        mock_collection_instance.count.return_value = 0 # Default count

        # Configure client methods
        mock_client_instance.get_collection.return_value = mock_collection_instance

        # Configure helper mocks
        mock_get_client.return_value = mock_client_instance
        mock_get_embedding_function.return_value = MagicMock(name="mock_embedding_function")
        mock_validate_name.return_value = None # Assume valid name by default

        yield mock_client_instance, mock_collection_instance, mock_validate_name # Yield validator too


class TestDocumentTools:
    """Test cases for document management tools."""

    # --- _add_documents_impl Tests ---
    @pytest.mark.asyncio
    async def test_add_documents_success(self, mock_chroma_client_document):
        """Test successful document addition (auto-ID, no metadata)."""
        mock_client, mock_collection, mock_validate = mock_chroma_client_document
        collection_name = "test_add_success"
        documents_to_add = ["doc1", "doc2"]

        # --- Act ---
        input_model = AddDocumentsInput(collection_name=collection_name, documents=documents_to_add)
        result = await _add_documents_impl(input_model)

        # --- Assert ---
        mock_validate.assert_called_once_with(collection_name)
        # Ensure get_collection is called correctly (only name needed)
        mock_client.get_collection.assert_called_once_with(name=collection_name)
        # Check that add was called on the collection mock
        # We now expect generated IDs, so use ANY for the ids parameter
        mock_collection.add.assert_called_once_with(documents=documents_to_add, ids=ANY, metadatas=None)
        # Assert result format
        assert isinstance(result, list)
        assert len(result) == 1
        assert isinstance(result[0], types.TextContent)
        # Updated success message check
        assert f"Successfully added {len(documents_to_add)} documents with generated IDs" in result[0].text

    @pytest.mark.asyncio
    async def test_add_documents_increment_index(self, mock_chroma_client_document):
        """Test document addition respecting increment_index flag (though Chroma client might ignore it)."""
        mock_client, mock_collection, mock_validate = mock_chroma_client_document
        collection_name = "test_add_increment"
        documents_to_add = ["doc_inc1"]

        # --- Act #
        # Test with increment_index=False (explicitly)
        input_model_false = AddDocumentsInput(collection_name=collection_name, documents=documents_to_add, increment_index=False)
        await _add_documents_impl(input_model_false)

        # --- Assert #
        mock_validate.assert_called_once_with(collection_name)
        mock_client.get_collection.assert_called_once_with(name=collection_name)
        # Check add was called (expecting generated IDs)
        mock_collection.add.assert_called_once_with(documents=documents_to_add, ids=ANY, metadatas=None)

        # Reset mocks for next call
        mock_validate.reset_mock()
        mock_client.get_collection.reset_mock()
        mock_collection.add.reset_mock()

        # --- Act #
        # Test with increment_index=True (default)
        input_model_true = AddDocumentsInput(collection_name=collection_name, documents=documents_to_add)
        await _add_documents_impl(input_model_true)

        # --- Assert #
        mock_validate.assert_called_once_with(collection_name)
        mock_client.get_collection.assert_called_once_with(name=collection_name)
        # Check add was called (expecting generated IDs)
        mock_collection.add.assert_called_once_with(documents=documents_to_add, ids=ANY, metadatas=None)

    @pytest.mark.asyncio
    async def test_add_documents_collection_not_found(self, mock_chroma_client_document):
        """Test adding documents to a non-existent collection."""
        mock_client, _, mock_validate = mock_chroma_client_document
        collection_name = "add_not_found"
        error_message = f"Collection {collection_name} does not exist."
        # Configure get_collection to raise ValueError for not found
        mock_client.get_collection.side_effect = ValueError(error_message)

        # --- Act & Assert ---
        input_model = AddDocumentsInput(collection_name=collection_name, documents=["doc"])
        with assert_raises_mcp_error(f"Collection \'{collection_name}\' not found."):
            await _add_documents_impl(input_model)

        mock_validate.assert_called_once_with(collection_name)
        # Verify get_collection was called (even though it failed)
        mock_client.get_collection.assert_called_once_with(name=collection_name)

    @pytest.mark.asyncio
    async def test_add_documents_chroma_error(self, mock_chroma_client_document):
        """Test handling errors during the actual Chroma add call."""
        mock_client, mock_collection, mock_validate = mock_chroma_client_document
        collection_name = "add_chroma_fail"
        error_message = "Chroma add failure"
        # Mock get success, add failure
        mock_client.get_collection.return_value = mock_collection
        mock_collection.add.side_effect = Exception(error_message)

        # --- Act & Assert ---
        input_model = AddDocumentsInput(collection_name=collection_name, documents=["doc"])
        # Updated expected message format
        with assert_raises_mcp_error(f"An unexpected error occurred: {error_message}"):
            await _add_documents_impl(input_model)

        mock_validate.assert_called_once_with(collection_name)
        mock_client.get_collection.assert_called_once_with(name=collection_name)
        mock_collection.add.assert_called_once() # Verify add was attempted

    @pytest.mark.asyncio
    async def test_add_documents_generate_ids(self, mock_chroma_client_document):
        """Test successful addition using AddDocumentsWithIDsInput (IDs provided)."""
        mock_client, mock_collection, mock_validate = mock_chroma_client_document
        collection_name = "test_add_with_ids"
        documents_to_add = ["doc_id1", "doc_id2"]
        ids_to_add = ["id1", "id2"]

        # --- Act ---
        input_model = AddDocumentsWithIDsInput(
            collection_name=collection_name, documents=documents_to_add, ids=ids_to_add
        )
        result = await _add_documents_with_ids_impl(input_model)

        # --- Assert ---
        mock_validate.assert_called_once_with(collection_name)
        mock_client.get_collection.assert_called_once_with(name=collection_name)
        mock_collection.add.assert_called_once_with(documents=documents_to_add, ids=ids_to_add, metadatas=None)
        assert f"Successfully added {len(documents_to_add)} documents with specified IDs" in result[0].text

    @pytest.mark.asyncio
    async def test_add_documents_generate_ids_no_increment(self, mock_chroma_client_document):
        """Test addition with IDs and increment_index=False."""
        mock_client, mock_collection, mock_validate = mock_chroma_client_document
        collection_name = "test_add_with_ids_noinc"
        documents_to_add = ["doc_id_noinc"]
        ids_to_add = ["id_noinc1"]

        # --- Act ---
        input_model = AddDocumentsWithIDsInput(
            collection_name=collection_name, documents=documents_to_add, ids=ids_to_add, increment_index=False
        )
        result = await _add_documents_with_ids_impl(input_model)

        # --- Assert ---
        mock_validate.assert_called_once_with(collection_name)
        mock_client.get_collection.assert_called_once_with(name=collection_name)
        mock_collection.add.assert_called_once_with(documents=documents_to_add, ids=ids_to_add, metadatas=None)
        assert f"Successfully added {len(documents_to_add)} documents with specified IDs" in result[0].text

    @pytest.mark.asyncio
    async def test_add_documents_validation_no_docs(self, mock_chroma_client_document):
        """Test validation failure when documents list is empty."""
        mock_client, mock_collection, mock_validate = mock_chroma_client_document
        collection_name = "test_add_valid_docs"

        # Test AddDocumentsInput
        input_model_base = AddDocumentsInput(collection_name=collection_name, documents=[])
        with assert_raises_mcp_error("Documents list cannot be empty."):
            await _add_documents_impl(input_model_base)

        # Test AddDocumentsWithIDsInput
        input_model_ids = AddDocumentsWithIDsInput(collection_name=collection_name, documents=[], ids=[])
        with assert_raises_mcp_error("Documents list cannot be empty."):
            await _add_documents_with_ids_impl(input_model_ids)

        # Test AddDocumentsWithMetadataInput
        input_model_meta = AddDocumentsWithMetadataInput(collection_name=collection_name, documents=[], metadatas=[])
        with assert_raises_mcp_error("Documents list cannot be empty."):
            await _add_documents_with_metadata_impl(input_model_meta)

        # Test AddDocumentsWithIDsAndMetadataInput
        input_model_full = AddDocumentsWithIDsAndMetadataInput(collection_name=collection_name, documents=[], ids=[], metadatas=[])
        with assert_raises_mcp_error("Documents list cannot be empty."):
            await _add_documents_with_ids_and_metadata_impl(input_model_full)

        # Ensure validation happened before client calls
        mock_validate.assert_called()
        mock_client.get_collection.assert_not_called()
        mock_collection.add.assert_not_called()

    @pytest.mark.asyncio
    async def test_add_documents_with_metadata_success(self, mock_chroma_client_document):
        """Test successful addition using AddDocumentsWithMetadataInput."""
        mock_client, mock_collection, mock_validate = mock_chroma_client_document
        collection_name = "test_add_with_meta"
        documents_to_add = ["doc_m1", "doc_m2"]
        # Metadata provided as JSON strings
        metadatas_str_list = ['{"key": "value1"}', '{"key": "value2"}']
        # Expected parsed metadata for assertion
        parsed_metadatas_list = [{"key": "value1"}, {"key": "value2"}]

        input_model = AddDocumentsWithMetadataInput(
            collection_name=collection_name, documents=documents_to_add, metadatas=metadatas_str_list
        )
        result = await _add_documents_with_metadata_impl(input_model)

        mock_validate.assert_called_once_with(collection_name)
        mock_client.get_collection.assert_called_once_with(name=collection_name)
        # Assert add was called with the PARSED metadata
        mock_collection.add.assert_called_once_with(documents=documents_to_add, ids=None, metadatas=parsed_metadatas_list)
        assert f"Successfully added {len(documents_to_add)} documents with specified metadata" in result[0].text

    @pytest.mark.asyncio
    async def test_add_documents_with_ids_and_metadata_success(self, mock_chroma_client_document):
        """Test successful addition using AddDocumentsWithIDsAndMetadataInput."""
        mock_client, mock_collection, mock_validate = mock_chroma_client_document
        collection_name = "test_add_full"
        documents_to_add = ["doc_f1"]
        ids_to_add = ["id_f1"]
        # Metadata provided as JSON strings
        metadatas_str_list = ['{"source": "full_test"}']
        # Expected parsed metadata for assertion
        parsed_metadatas_list = [{"source": "full_test"}]

        input_model = AddDocumentsWithIDsAndMetadataInput(
            collection_name=collection_name, documents=documents_to_add, ids=ids_to_add, metadatas=metadatas_str_list
        )
        result = await _add_documents_with_ids_and_metadata_impl(input_model)

        mock_validate.assert_called_once_with(collection_name)
        mock_client.get_collection.assert_called_once_with(name=collection_name)
        # Assert add was called with the PARSED metadata
        mock_collection.add.assert_called_once_with(documents=documents_to_add, ids=ids_to_add, metadatas=parsed_metadatas_list)
        assert f"Successfully added {len(documents_to_add)} documents with specified IDs and metadata" in result[0].text

    @pytest.mark.asyncio
    async def test_add_documents_invalid_metadata_json(self, mock_chroma_client_document):
        """Test adding documents with invalid metadata JSON string."""
        mock_client, mock_collection, mock_validate = mock_chroma_client_document
        collection_name = "test_add_invalid_json"
        documents_to_add = ["doc_ij1"]
        ids_to_add = ["id_ij1"]
        # Invalid JSON string (missing closing brace)
        invalid_metadatas_str_list = ['{"key": "value1' ]

        # Test AddDocumentsWithMetadataInput
        input_meta = AddDocumentsWithMetadataInput(
            collection_name=collection_name, documents=documents_to_add, metadatas=invalid_metadatas_str_list
        )
        with assert_raises_mcp_error("Invalid JSON format for metadata string at index 0"):
            await _add_documents_with_metadata_impl(input_meta)

        # Test AddDocumentsWithIDsAndMetadataInput
        input_full = AddDocumentsWithIDsAndMetadataInput(
            collection_name=collection_name, documents=documents_to_add, ids=ids_to_add, metadatas=invalid_metadatas_str_list
        )
        with assert_raises_mcp_error("Invalid JSON format for metadata string at index 0"):
            await _add_documents_with_ids_and_metadata_impl(input_full)

        # Ensure validation happened before client calls
        mock_validate.assert_called()
        mock_client.get_collection.assert_not_called()
        mock_collection.add.assert_not_called()

    @pytest.mark.asyncio
    async def test_add_documents_metadata_not_dict(self, mock_chroma_client_document):
        """Test adding documents where metadata string decodes to non-dict."""
        mock_client, mock_collection, mock_validate = mock_chroma_client_document
        collection_name = "test_add_meta_not_dict"
        documents_to_add = ["doc_nd1"]
        ids_to_add = ["id_nd1"]
        # Valid JSON, but not an object/dict
        not_dict_metadatas_str_list = ['["list", "not_dict"]' ]

        # Test AddDocumentsWithMetadataInput
        input_meta = AddDocumentsWithMetadataInput(
            collection_name=collection_name, documents=documents_to_add, metadatas=not_dict_metadatas_str_list
        )
        with assert_raises_mcp_error("Metadata string at index 0 did not decode to a dictionary"):
            await _add_documents_with_metadata_impl(input_meta)

        # Test AddDocumentsWithIDsAndMetadataInput
        input_full = AddDocumentsWithIDsAndMetadataInput(
            collection_name=collection_name, documents=documents_to_add, ids=ids_to_add, metadatas=not_dict_metadatas_str_list
        )
        with assert_raises_mcp_error("Metadata string at index 0 did not decode to a dictionary"):
            await _add_documents_with_ids_and_metadata_impl(input_full)

        # Ensure validation happened before client calls
        mock_validate.assert_called()
        mock_client.get_collection.assert_not_called()
        mock_collection.add.assert_not_called()

    # --- Query Documents Tests ---

    @pytest.mark.asyncio
    async def test_query_documents_success(self, mock_chroma_client_document):
        """Test successful document query."""
        mock_client, mock_collection, mock_validate = mock_chroma_client_document
        collection_name = "test_query_success"
        query = ["test query"]
        n_results = 5
        include_fields = ["metadatas", "documents"]
        expected_query_result = {"ids": [["id1"]], "documents": [["doc1"]], "metadatas": [[{"key": "val"}]]}
        mock_collection.query.return_value = expected_query_result

        # --- Act ---
        input_model = QueryDocumentsInput(
            collection_name=collection_name, query_texts=query, n_results=n_results, include=include_fields
        )
        result = await _query_documents_impl(input_model)

        # --- Assert ---
        mock_validate.assert_called_once_with(collection_name)
        mock_client.get_collection.assert_called_once_with(name=collection_name)
        mock_collection.query.assert_called_once_with(
            query_texts=query, n_results=n_results, where=None, where_document=None, include=include_fields
        )
        assert_successful_json_result(result, expected_query_result)

    @pytest.mark.asyncio
    async def test_query_documents_collection_not_found(self, mock_chroma_client_document):
        """Test querying a non-existent collection."""
        mock_client, _, mock_validate = mock_chroma_client_document
        collection_name = "query_not_found"
        error_message = f"Collection {collection_name} does not exist."
        mock_client.get_collection.side_effect = ValueError(error_message)

        # --- Act & Assert ---
        input_model = QueryDocumentsInput(collection_name=collection_name, query_texts=["q"])
        with assert_raises_mcp_error(f"Collection \'{collection_name}\' not found."):
            await _query_documents_impl(input_model)

        mock_validate.assert_called_once_with(collection_name)
        mock_client.get_collection.assert_called_once_with(name=collection_name)

    @pytest.mark.asyncio
    async def test_query_documents_chroma_error(self, mock_chroma_client_document):
        """Test handling errors during the actual Chroma query call."""
        mock_client, mock_collection, mock_validate = mock_chroma_client_document
        collection_name = "query_chroma_fail"
        error_message = "Query failed internally."
        mock_client.get_collection.return_value = mock_collection
        mock_collection.query.side_effect = Exception(error_message)

        # --- Act & Assert ---
        input_model = QueryDocumentsInput(collection_name=collection_name, query_texts=["q"])
        # Updated expected message format
        with assert_raises_mcp_error(f"An unexpected error occurred during query: {error_message}"):
            await _query_documents_impl(input_model)

        mock_validate.assert_called_once_with(collection_name)
        mock_client.get_collection.assert_called_once_with(name=collection_name)
        mock_collection.query.assert_called_once() # Verify query was attempted


    # --- Get Documents Tests ---

    @pytest.mark.asyncio
    async def test_get_documents_success_by_ids(self, mock_chroma_client_document):
        """Test successful get by IDs."""
        mock_client, mock_collection, mock_validate = mock_chroma_client_document
        collection_name = "test_get_ids_success"
        ids_to_get = ["id1", "id2"]
        include_fields = ["metadatas"]
        expected_get_result = {"ids": ids_to_get, "metadatas": [{"k": "v1"}, {"k": "v2"}]}
        mock_collection.get.return_value = expected_get_result

        # --- Act ---
        input_model = GetDocumentsByIdsInput(
            collection_name=collection_name, ids=ids_to_get, include=include_fields
        )
        result = await _get_documents_by_ids_impl(input_model)

        # --- Assert ---
        mock_validate.assert_called_once_with(collection_name)
        mock_client.get_collection.assert_called_once_with(name=collection_name)
        mock_collection.get.assert_called_once_with(
            ids=ids_to_get, where=None, where_document=None, limit=None, offset=None, include=include_fields
        )
        assert_successful_json_result(result, expected_get_result)

    @pytest.mark.asyncio
    async def test_get_documents_success_by_where(self, mock_chroma_client_document):
        """Test successful get by where filter."""
        mock_client, mock_collection, mock_validate = mock_chroma_client_document
        collection_name = "test_get_where_success"
        where_filter = {"status": "active"}
        limit, offset = 10, 0
        expected_get_result = {"ids": ["id_w1"], "documents": ["doc_w1"], "metadatas": [{"status": "active"}]}
        mock_collection.get.return_value = expected_get_result

        # --- Act ---
        input_model = GetDocumentsWithWhereFilterInput(
            collection_name=collection_name, where=where_filter, limit=limit, offset=offset
        )
        result = await _get_documents_with_where_filter_impl(input_model)

        # --- Assert ---
        mock_validate.assert_called_once_with(collection_name)
        mock_client.get_collection.assert_called_once_with(name=collection_name)
        mock_collection.get.assert_called_once_with(
            ids=None, where=where_filter, where_document=None, limit=limit, offset=offset, include=[] # default include
        )
        assert_successful_json_result(result, expected_get_result)

    # Test for GetDocumentsWithDocumentFilterInput - similar structure
    @pytest.mark.asyncio
    async def test_get_documents_success_by_where_doc(self, mock_chroma_client_document):
        """Test successful get by where_document filter."""
        mock_client, mock_collection, mock_validate = mock_chroma_client_document
        collection_name = "test_get_wheredoc_success"
        where_doc_filter = {"$contains": "obsolete"}
        expected_get_result = {"ids": ["id_wd1"], "documents": ["very important doc"]}
        mock_collection.get.return_value = expected_get_result

        input_model = GetDocumentsWithDocumentFilterInput(
            collection_name=collection_name, where_document=where_doc_filter
        )
        result = await _get_documents_with_document_filter_impl(input_model)

        mock_validate.assert_called_once_with(collection_name)
        mock_client.get_collection.assert_called_once_with(name=collection_name)
        mock_collection.get.assert_called_once_with(
            ids=None, where=None, where_document=where_doc_filter, limit=None, offset=None, include=[]
        )
        assert_successful_json_result(result, expected_get_result)

    # Test for GetAllDocumentsInput - similar structure
    @pytest.mark.asyncio
    async def test_get_all_documents_success(self, mock_chroma_client_document):
        """Test successful get all documents."""
        mock_client, mock_collection, mock_validate = mock_chroma_client_document
        collection_name = "test_get_all_success"
        limit = 5
        expected_get_result = {"ids": [f"id_a{i}" for i in range(limit)], "documents": [f"doc_a{i}" for i in range(limit)]}
        mock_collection.get.return_value = expected_get_result

        input_model = GetAllDocumentsInput(collection_name=collection_name, limit=limit)
        result = await _get_all_documents_impl(input_model)

        mock_validate.assert_called_once_with(collection_name)
        mock_client.get_collection.assert_called_once_with(name=collection_name)
        mock_collection.get.assert_called_once_with(
            ids=None, where=None, where_document=None, limit=limit, offset=None, include=[]
        )
        assert_successful_json_result(result, expected_get_result)


    @pytest.mark.skip(reason="Include value validation now primarily handled by Pydantic model.")
    @pytest.mark.asyncio
    async def test_get_documents_validation_invalid_include(self, mock_chroma_client_document):
        """Test validation failure for invalid include values."""
        mock_client, mock_collection, mock_validate = mock_chroma_client_document
        collection_name = "test_get_valid_include"
        # This test needs adjustment based on where include validation happens
        # If Pydantic handles it, test the dispatcher/server level
        # If _impl handles it, mock appropriately

        input_model = GetDocumentsByIdsInput(
            collection_name=collection_name, ids=["id1"], include=["invalid_field"] # Invalid field
        )

        # Example: Assuming _impl or a helper raises McpError for invalid include
        with assert_raises_mcp_error("Invalid include field"): # Adjust expected message
            await _get_documents_by_ids_impl(input_model)

    @pytest.mark.asyncio
    async def test_get_documents_validation_no_criteria(self, mock_chroma_client_document):
        """Test validation failure when no specific criteria provided to a specific getter."""
        mock_client, mock_collection, mock_validate = mock_chroma_client_document
        collection_name = "test_get_valid_criteria"

        # Test GetDocumentsByIdsInput with empty list (should fail in _impl)
        input_ids_empty = GetDocumentsByIdsInput(collection_name=collection_name, ids=[])
        with assert_raises_mcp_error("IDs list cannot be empty for get_documents_by_ids."):
             await _get_documents_by_ids_impl(input_ids_empty)

        # Pydantic ensures where/where_document are provided for other variants, so no test needed here
        # for empty filters on those specific tool variants.

        # Ensure validation happened before client calls
        mock_validate.assert_called()
        mock_client.get_collection.assert_not_called()
        mock_collection.get.assert_not_called()

    @pytest.mark.asyncio
    async def test_get_documents_collection_not_found(self, mock_chroma_client_document):
        """Test getting documents when the collection is not found."""
        mock_client, _, mock_validate = mock_chroma_client_document
        collection_name = "get_not_found"
        error_message = f"Collection {collection_name} does not exist."
        mock_client.get_collection.side_effect = ValueError(error_message)

        # Test one variant, e.g., GetDocumentsByIdsInput
        input_model = GetDocumentsByIdsInput(collection_name=collection_name, ids=["id1"])
        with assert_raises_mcp_error(f"Collection \'{collection_name}\' not found."):
            await _get_documents_by_ids_impl(input_model)

        mock_validate.assert_called_once_with(collection_name)
        mock_client.get_collection.assert_called_once_with(name=collection_name)

    @pytest.mark.asyncio
    async def test_get_documents_chroma_error(self, mock_chroma_client_document):
        """Test handling errors during the actual Chroma get call."""
        mock_client, mock_collection, mock_validate = mock_chroma_client_document
        collection_name = "get_chroma_fail"
        error_message = "Get failed internally."
        mock_client.get_collection.return_value = mock_collection
        mock_collection.get.side_effect = Exception(error_message)

        # Test one variant, e.g., GetDocumentsByIdsInput
        input_model = GetDocumentsByIdsInput(collection_name=collection_name, ids=["id1"])
        # Updated expected message format
        with assert_raises_mcp_error(f"An unexpected error occurred during get: {error_message}"):
            await _get_documents_by_ids_impl(input_model)

        mock_validate.assert_called_once_with(collection_name)
        mock_client.get_collection.assert_called_once_with(name=collection_name)
        mock_collection.get.assert_called_once() # Verify get was attempted

    # --- Update Documents Tests ---

    @pytest.mark.asyncio
    async def test_update_documents_success(self, mock_chroma_client_document):
        """Test successful document update (content only)."""
        mock_client, mock_collection, mock_validate = mock_chroma_client_document
        collection_name = "test_update_success"
        ids_to_update = ["id1", "id2"]
        new_docs = ["new_doc1", "new_doc2"]

        # --- Act ---
        input_model = UpdateDocumentContentInput(
            collection_name=collection_name, ids=ids_to_update, documents=new_docs
        )
        result = await _update_document_content_impl(input_model)

        # --- Assert ---
        mock_validate.assert_called_once_with(collection_name)
        mock_client.get_collection.assert_called_once_with(name=collection_name)
        mock_collection.update.assert_called_once_with(ids=ids_to_update, documents=new_docs, metadatas=None)
        assert f"Successfully updated content for {len(ids_to_update)}" in result[0].text

    @pytest.mark.asyncio
    async def test_update_documents_only_metadata(self, mock_chroma_client_document):
        """Test successful document update (metadata only)."""
        mock_client, mock_collection, mock_validate = mock_chroma_client_document
        collection_name = "test_update_meta_success"
        ids_to_update = ["id_m1"]
        new_metadatas = [{"status": "updated"}]

        # --- Act ---
        input_model = UpdateDocumentMetadataInput(
            collection_name=collection_name, ids=ids_to_update, metadatas=new_metadatas
        )
        result = await _update_document_metadata_impl(input_model)

        # --- Assert ---
        mock_validate.assert_called_once_with(collection_name)
        mock_client.get_collection.assert_called_once_with(name=collection_name)
        mock_collection.update.assert_called_once_with(ids=ids_to_update, documents=None, metadatas=new_metadatas)
        assert f"Successfully updated metadata for {len(ids_to_update)}" in result[0].text


    @pytest.mark.asyncio
    async def test_update_documents_validation_mismatch(self, mock_chroma_client_document):
        """Test validation failure for mismatched ids/documents/metadata lengths."""
        mock_client, mock_collection, mock_validate = mock_chroma_client_document
        collection_name = "test_update_valid_mismatch"

        # Test content update mismatch
        input_content = UpdateDocumentContentInput(
            collection_name=collection_name, ids=["id1"], documents=["doc1", "doc2"] # Mismatch
        )
        with assert_raises_mcp_error("Number of documents must match number of IDs"):
            await _update_document_content_impl(input_content)

        # Test metadata update mismatch
        input_meta = UpdateDocumentMetadataInput(
            collection_name=collection_name, ids=["id1", "id2"], metadatas=[{"k": "v"}] # Mismatch
        )
        with assert_raises_mcp_error("Number of metadatas must match number of IDs"):
            await _update_document_metadata_impl(input_meta)

        # Ensure validation happened before client calls
        mock_validate.assert_called()
        mock_client.get_collection.assert_not_called()
        mock_collection.update.assert_not_called()

    @pytest.mark.asyncio
    async def test_update_documents_collection_not_found(self, mock_chroma_client_document):
        """Test updating documents when the collection is not found."""
        mock_client, _, mock_validate = mock_chroma_client_document
        collection_name = "update_not_found"
        error_message = f"Collection {collection_name} does not exist."
        mock_client.get_collection.side_effect = ValueError(error_message)

        # Test one variant, e.g., UpdateDocumentContentInput
        input_model = UpdateDocumentContentInput(collection_name=collection_name, ids=["id1"], documents=["d"])
        with assert_raises_mcp_error(f"Collection \'{collection_name}\' not found."):
            await _update_document_content_impl(input_model)

        mock_validate.assert_called_once_with(collection_name)
        mock_client.get_collection.assert_called_once_with(name=collection_name)

    @pytest.mark.asyncio
    async def test_update_documents_chroma_error(self, mock_chroma_client_document):
        """Test handling errors during the actual Chroma update call."""
        mock_client, mock_collection, mock_validate = mock_chroma_client_document
        collection_name = "update_chroma_fail"
        error_message = "Update failed internally."
        mock_client.get_collection.return_value = mock_collection
        mock_collection.update.side_effect = Exception(error_message)

        # Test one variant, e.g., UpdateDocumentContentInput
        input_model = UpdateDocumentContentInput(collection_name=collection_name, ids=["id1"], documents=["d"])
        # Use the specific error message from the content update implementation
        with assert_raises_mcp_error(f"ChromaDB Error: Failed to update documents. {error_message}"):
            await _update_document_content_impl(input_model)

        mock_validate.assert_called_once_with(collection_name)
        mock_client.get_collection.assert_called_once_with(name=collection_name)
        mock_collection.update.assert_called_once() # Verify update was attempted

    # --- Delete Documents Tests ---

    @pytest.mark.asyncio
    async def test_delete_documents_success_by_ids(self, mock_chroma_client_document):
        """Test successful deletion by IDs."""
        mock_client, mock_collection, mock_validate = mock_chroma_client_document
        collection_name = "test_delete_ids"
        ids_to_delete = ["id_del1", "id_del2"]
        # Mock the return value of delete (list of IDs that were deleted)
        mock_collection.delete.return_value = ids_to_delete

        # --- Act ---
        input_model = DeleteDocumentsByIdsInput(collection_name=collection_name, ids=ids_to_delete)
        result = await _delete_documents_by_ids_impl(input_model)

        # --- Assert ---
        mock_validate.assert_called_once_with(collection_name)
        mock_client.get_collection.assert_called_once_with(name=collection_name)
        mock_collection.delete.assert_called_once_with(ids=ids_to_delete, where=None, where_document=None)
        assert_successful_json_result(result, {"deleted_ids": ids_to_delete})

    @pytest.mark.asyncio
    async def test_delete_documents_success_by_where(self, mock_chroma_client_document):
        """Test successful deletion by where filter."""
        mock_client, mock_collection, mock_validate = mock_chroma_client_document
        collection_name = "test_delete_where"
        where_filter = {"status": "to_delete"}
        # Mock delete return value
        deleted_ids_returned = ["id_matched1", "id_matched2"]
        mock_collection.delete.return_value = deleted_ids_returned

        # --- Act ---
        input_model = DeleteDocumentsByWhereFilterInput(collection_name=collection_name, where=where_filter)
        result = await _delete_documents_by_where_filter_impl(input_model)

        # --- Assert ---
        mock_validate.assert_called_once_with(collection_name)
        mock_client.get_collection.assert_called_once_with(name=collection_name)
        mock_collection.delete.assert_called_once_with(ids=None, where=where_filter, where_document=None)
        assert_successful_json_result(result, {"deleted_ids": deleted_ids_returned})

    # Test for DeleteDocumentsByDocumentFilterInput - similar structure
    @pytest.mark.asyncio
    async def test_delete_documents_success_by_where_doc(self, mock_chroma_client_document):
        """Test successful deletion by where_document filter."""
        mock_client, mock_collection, mock_validate = mock_chroma_client_document
        collection_name = "test_delete_wheredoc"
        where_doc_filter = {"$contains": "obsolete"}
        deleted_ids_returned = ["id_wd1"]
        mock_collection.delete.return_value = deleted_ids_returned

        input_model = DeleteDocumentsByDocumentFilterInput(
            collection_name=collection_name, where_document=where_doc_filter
        )
        result = await _delete_documents_by_document_filter_impl(input_model)

        mock_validate.assert_called_once_with(collection_name)
        mock_client.get_collection.assert_called_once_with(name=collection_name)
        mock_collection.delete.assert_called_once_with(
            ids=None, where=None, where_document=where_doc_filter
        )
        assert_successful_json_result(result, {"deleted_ids": deleted_ids_returned})


    @pytest.mark.asyncio
    async def test_delete_documents_validation_no_criteria(self, mock_chroma_client_document):
        """Test validation failure when no criteria (ids/where/where_doc) provided."""
        mock_client, mock_collection, mock_validate = mock_chroma_client_document
        collection_name = "test_delete_valid"
        # Use DeleteDocumentsByIdsInput and provide required 'ids' (even if empty)
        # Pydantic needs 'ids' to be present. The internal logic should then check if it's empty.
        input_model = DeleteDocumentsByIdsInput(collection_name=collection_name, ids=[])

        # Expect McpError from internal validation because the ids list is empty.
        # Adjust expected message based on actual implementation.
        with assert_raises_mcp_error("IDs list cannot be empty for delete_documents_by_ids."): # Updated message
            await _delete_documents_by_ids_impl(input_model)

        # Ensure validation happened before client calls
        mock_validate.assert_called_once_with(collection_name)
        mock_client.get_collection.assert_not_called()
        mock_collection.delete.assert_not_called()


    @pytest.mark.asyncio
    async def test_delete_documents_collection_not_found(self, mock_chroma_client_document):
        """Test deleting documents when the collection is not found."""
        mock_client, _, mock_validate = mock_chroma_client_document
        collection_name = "delete_not_found"
        error_message = f"Collection {collection_name} does not exist."
        mock_client.get_collection.side_effect = ValueError(error_message)

        # --- Act & Assert --- #
        # Test one variant, e.g., DeleteDocumentsByIdsInput
        input_model = DeleteDocumentsByIdsInput(collection_name=collection_name, ids=["id1"])
        with assert_raises_mcp_error(f"Collection \'{collection_name}\' not found."):
            await _delete_documents_by_ids_impl(input_model)

        mock_validate.assert_called_once_with(collection_name)
        mock_client.get_collection.assert_called_once_with(name=collection_name)

    @pytest.mark.asyncio
    async def test_delete_documents_chroma_error(self, mock_chroma_client_document):
        """Test handling errors during the actual delete call."""
        mock_client, mock_collection, mock_validate = mock_chroma_client_document
        collection_name = "delete_chroma_fail"
        error_message = "Delete failed internally."
        # Mock get success, delete failure
        mock_client.get_collection.return_value = mock_collection
        mock_collection.delete.side_effect = Exception(error_message)

        # --- Act & Assert --- #
        # Test one variant, e.g., DeleteDocumentsByIdsInput
        input_model = DeleteDocumentsByIdsInput(collection_name=collection_name, ids=["id1"])
        # Check the specific error message from the _delete_documents_by_ids_impl variant
        with assert_raises_mcp_error(f"ChromaDB Error: Failed to delete documents. {error_message}"):
             await _delete_documents_by_ids_impl(input_model)

        mock_validate.assert_called_once_with(collection_name)
        mock_client.get_collection.assert_called_once_with(name=collection_name)
        mock_collection.delete.assert_called_once() # Verify delete was attempted


    # --- Generic Error Handling Test ---

    @pytest.mark.asyncio
    async def test_generic_chroma_error_handling(self, mock_chroma_client_document):
        """Test that generic ChromaDB errors are caught and wrapped in McpError."""
        mock_client, mock_collection, mock_validate = mock_chroma_client_document
        collection_name = "generic_error_test"
        generic_error_message = "A generic ChromaDB internal error occurred."

        # --- Test Add --- #
        mock_client.get_collection.reset_mock(side_effect=None)
        mock_client.get_collection.return_value = mock_collection
        mock_collection.add.side_effect = Exception(generic_error_message)
        input_add = AddDocumentsInput(collection_name=collection_name, documents=["d"])
        with assert_raises_mcp_error(f"An unexpected error occurred: {generic_error_message}"):
            await _add_documents_impl(input_add)
        mock_validate.assert_called_with(collection_name)
        mock_client.get_collection.assert_called_with(name=collection_name)
        mock_collection.add.assert_called_once()
        mock_client.reset_mock(); mock_collection.reset_mock(); mock_validate.reset_mock()

        # --- Test Query --- #
        mock_client.get_collection.return_value = mock_collection
        mock_collection.query.side_effect = Exception(generic_error_message)
        input_query = QueryDocumentsInput(collection_name=collection_name, query_texts=["q"])
        with assert_raises_mcp_error(f"An unexpected error occurred during query: {generic_error_message}"):
            await _query_documents_impl(input_query)
        mock_validate.assert_called_with(collection_name)
        mock_client.get_collection.assert_called_with(name=collection_name)
        mock_collection.query.assert_called_once()
        mock_client.reset_mock(); mock_collection.reset_mock(); mock_validate.reset_mock()

        # --- Test Get --- #
        mock_client.get_collection.return_value = mock_collection
        mock_collection.get.side_effect = Exception(generic_error_message)
        input_get = GetDocumentsByIdsInput(collection_name=collection_name, ids=["id1"])
        with assert_raises_mcp_error(f"An unexpected error occurred during get: {generic_error_message}"):
            await _get_documents_by_ids_impl(input_get)
        mock_validate.assert_called_with(collection_name)
        mock_client.get_collection.assert_called_with(name=collection_name)
        mock_collection.get.assert_called_once()
        mock_client.reset_mock(); mock_collection.reset_mock(); mock_validate.reset_mock()

        # --- Test Update (Content) --- #
        mock_client.get_collection.return_value = mock_collection
        mock_collection.update.side_effect = Exception(generic_error_message)
        input_update_content = UpdateDocumentContentInput(collection_name=collection_name, ids=["id1"], documents=["d"])
        with assert_raises_mcp_error(f"ChromaDB Error: Failed to update documents. {generic_error_message}"):
             await _update_document_content_impl(input_update_content)
        mock_validate.assert_called_with(collection_name)
        mock_client.get_collection.assert_called_with(name=collection_name)
        mock_collection.update.assert_called_once()
        mock_client.reset_mock(); mock_collection.reset_mock(); mock_validate.reset_mock()

        # --- Test Delete --- #
        mock_client.get_collection.return_value = mock_collection
        mock_collection.delete.side_effect = Exception(generic_error_message)
        input_delete = DeleteDocumentsByIdsInput(collection_name=collection_name, ids=["id1"])
        with assert_raises_mcp_error(f"ChromaDB Error: Failed to delete documents. {generic_error_message}"):
             await _delete_documents_by_ids_impl(input_delete)
        mock_validate.assert_called_with(collection_name)
        mock_client.get_collection.assert_called_with(name=collection_name)
        mock_collection.delete.assert_called_once()


    # --- Test Query Collection Not Found (Specific Test) ---
    # This test specifically focuses on the ValueError raised by get_collection
    @pytest.mark.asyncio
    async def test_query_collection_not_found(self, mock_chroma_client_document):
        """Test querying a non-existent collection (using specific test)."""
        mock_client, _, mock_validate = mock_chroma_client_document
        collection_name = "non_existent_coll"
        # Configure the client's get_collection mock to raise the specific ValueError
        error_message = f"Collection {collection_name} does not exist."
        mock_client.get_collection.side_effect = ValueError(error_message)

        # ACT & Assert
        input_model = QueryDocumentsInput(collection_name=collection_name, query_texts=["test"])
        with assert_raises_mcp_error(f"Collection \'{collection_name}\' not found."):
            await _query_documents_impl(input_model)

        # Assert mocks were called correctly
        mock_validate.assert_called_once_with(collection_name)
        mock_client.get_collection.assert_called_once_with(name=collection_name)
