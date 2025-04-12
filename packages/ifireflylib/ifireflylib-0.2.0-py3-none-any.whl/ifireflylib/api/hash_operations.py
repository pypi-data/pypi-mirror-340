"""
Hash operations for the Firefly database client.
"""

import logging
import traceback
from typing import Dict, List, Optional

logger = logging.getLogger("FireflyDB.HashOperations")

class HashOperations:
    """Mixin class for hash operations in the Firefly database client."""
    
    def __init__(self, client):
        """Initialize the hash operations mixin.
        
        Args:
            client: The IFireflyClient instance
        """
        self.client = client
        self.lib = client.lib
    
    def hash_set(self, key, field, value):
        """Set a field in a hash

        Args:
            key: The hash key
            field: The field name
            value: The field value

        Returns:
            True if successful
        """
        try:
            self.client._check_connection()
            key_bytes = self.client._to_bytes(key)
            field_bytes = self.client._to_bytes(field)
            value_bytes = self.client._to_bytes(value)
            result = self.lib.HashSet(self.client.client, key_bytes, field_bytes, value_bytes)
            logger.debug(
                f"HashSet on key '{key}' field '{field}' with value '{value}': {result}"
            )
            return result
        except ConnectionError as e:
            logger.error(f"Connection error in hash_set: {e}")
            raise
        except Exception as e:
            logger.error(
                f"Error in hash_set: {e}. Traceback:\n{traceback.format_exc()}"
            )
            return False

    def hash_get(self, key, field):
        """Get a field value from a hash

        Args:
            key: The hash key
            field: The field name

        Returns:
            The field value, or None if not found
        """
        try:
            self.client._check_connection()
            key_bytes = self.client._to_bytes(key)
            field_bytes = self.client._to_bytes(field)
            result = self.lib.HashGet(self.client.client, key_bytes, field_bytes)
            logger.debug(f"HashGet raw result: {result}")

            if result:
                try:
                    # If result is already a bytes object
                    if isinstance(result, bytes):
                        logger.debug(
                            "Result is already a Python bytes object, no need to free"
                        )
                        value = result.decode("utf-8")
                        logger.debug(
                            f"HashGet on key '{key}' field '{field}': {value}"
                        )
                        return value

                    # Regular C pointer handling
                    value = self.client._from_bytes(result)
                    logger.debug(f"About to free string at address: {result}")
                    self.client._free_string(result)
                    logger.debug(f"HashGet on key '{key}' field '{field}': {value}")
                    return value
                except Exception as e:
                    logger.error(f"Error processing HashGet result: {e}")
                    if result and not isinstance(result, bytes):
                        try:
                            self.client._free_string(result)
                        except Exception as free_e:
                            logger.error(f"Error freeing HashGet result: {free_e}")
                    return None
            logger.debug(f"HashGet on key '{key}' field '{field}': Not found")
            return None
        except ConnectionError as e:
            logger.error(f"Connection error in hash_get: {e}")
            raise
        except Exception as e:
            logger.error(
                f"Error in hash_get: {e}. Traceback:\n{traceback.format_exc()}"
            )
            return None

    def hash_delete(self, key, field):
        """Delete a field from a hash

        Args:
            key: The hash key
            field: The field name

        Returns:
            True if the field was deleted
        """
        try:
            self.client._check_connection()
            key_bytes = self.client._to_bytes(key)
            field_bytes = self.client._to_bytes(field)
            result = self.lib.HashDelete(self.client.client, key_bytes, field_bytes)
            logger.debug(
                f"HashDelete on key '{key}' field '{field}': {result}"
            )
            return result
        except ConnectionError as e:
            logger.error(f"Connection error in hash_delete: {e}")
            raise
        except Exception as e:
            logger.error(
                f"Error in hash_delete: {e}. Traceback:\n{traceback.format_exc()}"
            )
            return False

    def hash_field_exists(self, key, field):
        """Check if a field exists in a hash

        Args:
            key: The hash key
            field: The field name

        Returns:
            True if the field exists
        """
        try:
            self.client._check_connection()
            key_bytes = self.client._to_bytes(key)
            field_bytes = self.client._to_bytes(field)
            result = self.lib.HashFieldExists(self.client.client, key_bytes, field_bytes)
            logger.debug(
                f"HashFieldExists on key '{key}' field '{field}': {result}"
            )
            return result
        except ConnectionError as e:
            logger.error(f"Connection error in hash_field_exists: {e}")
            raise
        except Exception as e:
            logger.error(
                f"Error in hash_field_exists: {e}. Traceback:\n{traceback.format_exc()}"
            )
            return False

    def hash_multi_set(self, key, field_values):
        """Set multiple fields in a hash at once

        Args:
            key: The hash key
            field_values: Dictionary of field-value pairs to set

        Returns:
            True if successful
        """
        try:
            self.client._check_connection()
            key_bytes = self.client._to_bytes(key)
            
            # Convert field_values to a string format that the C API can understand
            # Format: field1=value1\nfield2=value2\n...
            field_value_str = ""
            for field, value in field_values.items():
                field_value_str += f"{field}={value}\n"
            
            # Convert to bytes
            field_value_bytes = self.client._to_bytes(field_value_str)
            
            # Execute the command directly since we don't have a proper HashMultiSet function
            # result = self.client.execute_command("HMSET", key, field_value_str)
            result = self.lib.HashMultiSet(self.client.client, key_bytes, field_value_bytes)
            logger.debug(
                f"HashMultiSet on key '{key}' with {len(field_values)} fields: {result}"
            )
            return result is not None
        except ConnectionError as e:
            logger.error(f"Connection error in hash_multi_set: {e}")
            raise
        except Exception as e:
            logger.error(
                f"Error in hash_multi_set: {e}. Traceback:\n{traceback.format_exc()}"
            )
            return False

    def hash_get_all(self, key):
        """Get all fields and values from a hash

        Args:
            key: The hash key

        Returns:
            Dictionary of field names and values
        """
        try:
            self.client._check_connection()
            key_bytes = self.client._to_bytes(key)
            result = self.lib.HashGetAll(self.client.client, key_bytes)
            logger.debug(f"HashGetAll raw result: {result}")

            if result:
                try:
                    # The result is a newline-delimited string of alternating field and value pairs
                    if isinstance(result, bytes):
                        # Directly decode the bytes object
                        value_str = result.decode("utf-8")
                    else:
                        # Handle as C pointer to string
                        value_str = self.client._from_bytes(result)
                        # Free the allocated string
                        self.client._free_string(result)

                    # Split by newlines and create field-value pairs
                    parts = value_str.split("\n") if value_str else []
                    field_values = {}
                    
                    # Process pairs of field and value
                    for i in range(0, len(parts), 2):
                        if i + 1 < len(parts):
                            field = parts[i]
                            value = parts[i + 1]
                            field_values[field] = value

                    logger.debug(
                        f"HashGetAll on key '{key}'. Found {len(field_values)} fields"
                    )
                    return field_values
                except Exception as e:
                    logger.error(f"Error processing HashGetAll result: {e}")
                    # Try to free if it was a C pointer
                    if result and not isinstance(result, bytes):
                        try:
                            self.client._free_string(result)
                        except Exception as free_e:
                            logger.error(f"Error freeing HashGetAll result: {free_e}")
                    return {}
            logger.debug(f"HashGetAll on key '{key}'. Empty hash")
            return {}
        except ConnectionError as e:
            logger.error(f"Connection error in hash_get_all: {e}")
            raise
        except Exception as e:
            logger.error(
                f"Error in hash_get_all: {e}. Traceback:\n{traceback.format_exc()}"
            )
            return {} 