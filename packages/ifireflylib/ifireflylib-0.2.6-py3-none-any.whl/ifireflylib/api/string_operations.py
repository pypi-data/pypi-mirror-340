"""
String operations for the Firefly database client.
"""

import logging
import traceback
from typing import Optional

logger = logging.getLogger("FireflyDB.StringOperations")

class StringOperations:
    """Mixin class for string operations in the Firefly database client."""

    def __init__(self, client):
        """Initialize the string operations mixin.

        Args:
            client: The IFireflyClient instance
        """
        self.client = client
        self.lib = client.lib

    def string_set(self, key, value):
        """Set a string value

        Args:
            key: The key to set
            value: The value to set

        Returns:
            True if successful
        """
        try:
            self.client._check_connection()
            key_bytes = self.client._to_bytes(key)
            value_bytes = self.client._to_bytes(value)

            # Normal mode
            result = self.lib.StringSet(self.client.client, key_bytes, value_bytes)
            logger.debug(f"StringSet result for key '{key}': {result}")
            return result
        except ConnectionError as e:
            logger.error(f"Connection error in string_set: {e}")
            raise
        except Exception as e:
            logger.error(
                f"Error in string_set: {e}. Traceback:\n{traceback.format_exc()}"
            )
            return False

    def string_get(self, key):
        """Get a string value

        Args:
            key: The key to get

        Returns:
            The value, or None if not found
        """
        try:
            self.client._check_connection()
            key_bytes = self.client._to_bytes(key)
            result = self.lib.StringGet(self.client.client, key_bytes)
            logger.debug(f"StringGet raw result pointer: {result}")

            if result:
                try:
                    # If the result is already a bytes object, we don't need to free it
                    if isinstance(result, bytes):
                        logger.debug(
                            "Result is already a Python bytes object, no need to free"
                        )
                        value = result.decode("utf-8")
                        logger.debug(f"StringGet for key '{key}': {value}")
                        return value

                    # Otherwise, treat it as a C pointer that needs to be freed
                    value = self.client._from_bytes(result)
                    logger.debug(f"StringGet decoded value: {value}")

                    # Log before freeing
                    logger.debug(f"About to free string at address: {result}")
                    self.client._free_string(result)
                    logger.debug(f"StringGet for key '{key}': {value}")
                    return value
                except Exception as decode_e:
                    logger.error(f"Error processing StringGet result: {decode_e}")
                    # Try to free anyway, but only if it's not a bytes object
                    try:
                        if not isinstance(result, bytes):
                            self.client._free_string(result)
                    except Exception as free_e:
                        logger.error(f"Error freeing string in StringGet: {free_e}")
                    return None
            logger.debug(f"StringGet for key '{key}': Key not found")
            return None
        except ConnectionError as e:
            logger.error(f"Connection error in string_get: {e}")
            raise
        except Exception as e:
            logger.error(
                f"Error in string_get: {e}. Traceback:\n{traceback.format_exc()}"
            )
            return None

    def delete(self, key):
        """Delete a key

        Args:
            key: The key to delete

        Returns:
            The number of keys removed
        """
        try:
            self.client._check_connection()
            key_bytes = self.client._to_bytes(key)
            result = self.lib.ExecuteCommand(self.client.client, b"DEL", key_bytes)
            logger.debug(f"Delete result: {result}")

            if result:
                try:
                    # Handle as bytes or C pointer
                    if isinstance(result, bytes):
                        # Directly decode bytes
                        response = result.decode("utf-8")

                        # Regular response format
                        try:
                            count = int(response.strip(":\r\n"))
                        except ValueError:
                            logger.warning(
                                f"Unexpected response from DEL command: {response}"
                            )
                            count = 0
                    else:
                        # Handle as C pointer
                        try:
                            response = self.client._from_bytes(result)
                            count = int(response.strip(":\r\n"))
                            self.client._free_string(result)
                        except ValueError:
                            self.client._free_string(
                                result
                            )  # Free memory even on error
                            logger.warning(
                                f"Unexpected response from DEL command: {response}"
                            )
                            count = 0

                    logger.debug(f"Deleted key '{key}'. Count: {count}")
                    return count
                except Exception as e:
                    logger.error(f"Error processing DEL result: {e}")
                    # Try to free if needed
                    if result and not isinstance(result, bytes):
                        try:
                            self.client._free_string(result)
                        except Exception as free_e:
                            logger.error(f"Error freeing DEL result: {free_e}")
                    return 0
            logger.debug(f"Key '{key}' not found.")
            return 0
        except ConnectionError as e:
            logger.error(f"Connection error in delete: {e}")
            raise
        except Exception as e:
            logger.error(f"Error in delete: {e}. Traceback:\n{traceback.format_exc()}")
            return 0

    def keys(self, pattern):
        """Get all keys matching the pattern

        Args:
            pattern: The pattern to match against keys

        Returns:
            A list of keys that match the pattern
        """
        try:
            self.client._check_connection()
            pattern_bytes = self.client._to_bytes(pattern)
            result = self.lib.Keys(self.client.client, pattern_bytes)
            logger.debug(f"Keys result: {result}")

            if result:
                try:
                    # Handle as bytes or C pointer
                    if isinstance(result, bytes):
                        # Directly decode bytes
                        keys = result.decode("utf-8").split("\n")
                        logger.debug(f"Keys result as bytes: {keys}")
                        return keys
                    else:
                        # Handle as C pointer
                        keys = self.client._from_bytes(result)
                        logger.debug(f"Keys result as C pointer: {keys}")
                        return keys
                except Exception as e:
                    logger.error(f"Error processing Keys result: {e}")
                    return []
            else:
                logger.debug(f"No keys found matching pattern '{pattern}'")
                return []
        except ConnectionError as e:
            logger.error(f"Connection error in keys: {e}")
            raise

    def type(self, key):
        """Get the type of a key

        Args:
            key: The key to get the type of

        Returns:
            The type of the key (string, list, hash, etc.) or None if key doesn't exist
        """
        try:
            self.client._check_connection()
            key_bytes = self.client._to_bytes(key)
            # Use ExecuteCommand since Type is not directly exposed in the library
            result = self.lib.ExecuteCommand(self.client.client, b"TYPE", key_bytes)
            logger.debug(f"Type result: {result}")
            
            if result:
                try:
                    type_str = self.client._from_bytes(result)
                    # Free the string allocated by the C library
                    self.client._free_string(result)
                    return type_str
                except Exception as e:
                    logger.error(f"Error processing TYPE result: {e}")
                    # Ensure we free the string even if processing fails
                    self.client._free_string(result)
                    return None
            else:
                logger.debug(f"Key '{key}' not found or TYPE command failed")
                return None
        except ConnectionError as e:
            logger.error(f"Connection error in type: {e}")
            raise
        except Exception as e:
            logger.error(f"Error in type: {e}. Traceback:\n{traceback.format_exc()}")
            return None
