"""
Hash operations for the Firefly database client.
"""

import logging
import traceback
from ifireflylib.client.utils import Dictionary

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
                    value = self.client._from_bytes(result)
                    self.client._free_string(result)
                    logger.debug(f"HashGet on key '{key}' field '{field}': {value}")
                    return value
                except Exception as e:
                    logger.error(f"Error processing HashGet result: {e}")
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
            True if the field was deleted, False otherwise
        """
        try:
            self.client._check_connection()
            key_bytes = self.client._to_bytes(key)
            field_bytes = self.client._to_bytes(field)
            result = self.lib.HashDelete(self.client.client, key_bytes, field_bytes)
            logger.debug(f"HashDelete on key '{key}' field '{field}': {result}")
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
            True if the field exists, False otherwise
        """
        try:
            self.client._check_connection()
            key_bytes = self.client._to_bytes(key)
            field_bytes = self.client._to_bytes(field)
            result = self.lib.HashFieldExists(self.client.client, key_bytes, field_bytes)
            logger.debug(f"HashFieldExists on key '{key}' field '{field}': {result}")
            return result
        except ConnectionError as e:
            logger.error(f"Connection error in hash_field_exists: {e}")
            raise
        except Exception as e:
            logger.error(
                f"Error in hash_field_exists: {e}. Traceback:\n{traceback.format_exc()}"
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
            logger.debug(f"HashGetAll raw result type: {type(result)}")

            if result and isinstance(result, Dictionary):
                try:
                    # Extract values from the Dictionary structure
                    field_values = {}
                    for i in range(result.Count):
                        # Get the key-value pair at index i
                        pair = result.Pairs[i]
                        if pair.Key and pair.Value:
                            field = self.client._from_bytes(pair.Key)
                            value = self.client._from_bytes(pair.Value)
                            field_values[field] = value
                    
                    # Free the Dictionary structure
                    self.client._free_dictionary(result)
                    logger.debug(f"HashGetAll on key '{key}'. Found {len(field_values)} fields")
                    return field_values
                except Exception as e:
                    logger.error(f"Error processing HashGetAll result: {e}")
                    try:
                        self.client._free_dictionary(result)
                    except Exception as free_e:
                        logger.error(f"Error freeing Dictionary in HashGetAll: {free_e}")
                    return {}
            logger.debug(f"HashGetAll on key '{key}'. Empty hash or invalid result type")
            return {}
        except ConnectionError as e:
            logger.error(f"Connection error in hash_get_all: {e}")
            raise
        except Exception as e:
            logger.error(
                f"Error in hash_get_all: {e}. Traceback:\n{traceback.format_exc()}"
            )
            return {}

    def hash_multi_set(self, key, field_values):
        """Set multiple fields in a hash

        Args:
            key: The hash key
            field_values: Dictionary of field names and values

        Returns:
            True if successful
        """
        try:
            self.client._check_connection()
            key_bytes = self.client._to_bytes(key)
            
            # Format field-value pairs as a space-separated string
            pairs_str = " ".join(f"{field} {value}" for field, value in field_values.items())
            pairs_bytes = self.client._to_bytes(pairs_str)
            
            result = self.lib.HashMultiSet(self.client.client, key_bytes, pairs_bytes)
            logger.debug(f"HashMultiSet on key '{key}' with {len(field_values)} fields: {result}")
            return result
        except ConnectionError as e:
            logger.error(f"Connection error in hash_multi_set: {e}")
            raise
        except Exception as e:
            logger.error(
                f"Error in hash_multi_set: {e}. Traceback:\n{traceback.format_exc()}"
            )
            return False
