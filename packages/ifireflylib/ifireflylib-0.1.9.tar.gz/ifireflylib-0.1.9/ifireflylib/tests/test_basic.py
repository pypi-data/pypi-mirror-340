#!/usr/bin/env python3
"""
Basic tests for the Firefly library.

These tests verify the core functionality of the IFireflyClient class,
including connection, string operations, list operations, and hash operations.
"""

import os
import pytest
import time
from ifireflylib.client.src.client import IFireflyClient
from ifireflylib.api.src.exceptions import FireflyError

# Configuration for tests
HOST = os.environ.get("FIREFLY_HOST", "localhost")
PORT = int(os.environ.get("FIREFLY_PORT", "6379"))
TEST_PREFIX = "test:"

@pytest.fixture
def client():
    """Create a client instance for testing."""
    client = IFireflyClient(host=HOST, port=PORT)
    client.connect()
    yield client
    # Clean up after tests
    try:
        # Delete all test keys
        client.string_delete(f"{TEST_PREFIX}string_key")
        client.list_delete(f"{TEST_PREFIX}list_key")
        client.hash_delete(f"{TEST_PREFIX}hash_key")
    except Exception:
        pass
    finally:
        client.close()

def test_connection(client):
    """Test that the client can connect to the server."""
    assert client.is_connected() is True

def test_string_operations(client):
    """Test string operations."""
    key = f"{TEST_PREFIX}string_key"
    value = "Hello, FireflyDB!"
    
    # Test string_set
    client.string_set(key, value)
    
    # Test string_get
    result = client.string_get(key)
    assert result == value
    
    # Test string_delete
    client.string_delete(key)
    
    # Verify deletion
    result = client.string_get(key)
    assert result is None

def test_list_operations(client):
    """Test list operations."""
    key = f"{TEST_PREFIX}list_key"
    items = ["item1", "item2", "item3"]
    
    # Test list_push
    for item in items:
        client.list_push(key, item)
    
    # Test list_length
    length = client.list_length(key)
    assert length == len(items)
    
    # Test list_range
    result = client.list_range(key, 0, -1)
    assert result == items
    
    # Test list_remove
    client.list_remove(key, "item2")
    
    # Verify removal
    result = client.list_range(key, 0, -1)
    assert "item2" not in result
    assert len(result) == len(items) - 1
    
    # Test list_delete
    client.list_delete(key)
    
    # Verify deletion
    length = client.list_length(key)
    assert length == 0

def test_hash_operations(client):
    """Test hash operations."""
    key = f"{TEST_PREFIX}hash_key"
    fields = {
        "field1": "value1",
        "field2": "value2"
    }
    
    # Test hash_set
    for field, value in fields.items():
        client.hash_set(key, field, value)
    
    # Test hash_get
    for field, value in fields.items():
        result = client.hash_get(key, field)
        assert result == value
    
    # Test hash_get_all
    result = client.hash_get_all(key)
    assert result == fields
    
    # Test hash_field_exists
    assert client.hash_field_exists(key, "field1") is True
    assert client.hash_field_exists(key, "field3") is False
    
    # Test hash_delete
    client.hash_delete(key, "field1")
    
    # Verify deletion
    assert client.hash_field_exists(key, "field1") is False
    result = client.hash_get_all(key)
    assert "field1" not in result
    assert len(result) == len(fields) - 1

def test_error_handling(client):
    """Test error handling."""
    # Test with invalid host
    with pytest.raises(FireflyError):
        invalid_client = IFireflyClient(host="invalid_host", port=PORT)
        invalid_client.connect()
    
    # Test with invalid port
    with pytest.raises(FireflyError):
        invalid_client = IFireflyClient(host=HOST, port=9999)
        invalid_client.connect()
    
    # Test with invalid operation
    with pytest.raises(FireflyError):
        client.string_get(None)  # Invalid key

def test_concurrent_operations(client):
    """Test concurrent operations."""
    key = f"{TEST_PREFIX}concurrent_key"
    
    # Set initial value
    client.string_set(key, "initial")
    
    # Perform multiple operations in quick succession
    for i in range(10):
        client.string_set(key, f"value{i}")
        time.sleep(0.01)  # Small delay to simulate concurrent access
    
    # Verify final value
    result = client.string_get(key)
    assert result == "value9"
    
    # Clean up
    client.string_delete(key)

if __name__ == "__main__":
    pytest.main([__file__])
