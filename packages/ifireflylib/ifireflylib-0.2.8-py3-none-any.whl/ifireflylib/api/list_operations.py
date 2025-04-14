"""
List operations for the Firefly database client.
"""

import logging
import traceback
from client.utils import StringArray

logger = logging.getLogger("FireflyDB.ListOperations")

class ListOperations:
    """Mixin class for list operations in the Firefly database client."""
    
    def __init__(self, client):
        """Initialize the list operations mixin.
        
        Args:
            client: The IFireflyClient instance
        """
        self.client = client
        self.lib = client.lib
    
    def list_left_push(self, key, value):
        """Push a value to the left of a list

        Args:
            key: The list key
            value: The value to push

        Returns:
            The length of the list after the push
        """
        try:
            self.client._check_connection()
            key_bytes = self.client._to_bytes(key)
            value_bytes = self.client._to_bytes(value)
            result = self.lib.ListLeftPush(self.client.client, key_bytes, value_bytes)
            logger.debug(
                f"ListLeftPush on key '{key}' with value '{value}'. New length: {result}"
            )
            return result
        except ConnectionError as e:
            logger.error(f"Connection error in list_left_push: {e}")
            raise
        except Exception as e:
            logger.error(
                f"Error in list_left_push: {e}. Traceback:\n{traceback.format_exc()}"
            )
            return 0

    def list_right_push(self, key, value):
        """Push a value to the right of a list

        Args:
            key: The list key
            value: The value to push

        Returns:
            The length of the list after the push
        """
        try:
            self.client._check_connection()
            key_bytes = self.client._to_bytes(key)
            value_bytes = self.client._to_bytes(value)
            result = self.lib.ListRightPush(self.client.client, key_bytes, value_bytes)
            logger.debug(
                f"ListRightPush on key '{key}' with value '{value}'. New length: {result}"
            )
            return result
        except ConnectionError as e:
            logger.error(f"Connection error in list_right_push: {e}")
            raise
        except Exception as e:
            logger.error(
                f"Error in list_right_push: {e}. Traceback:\n{traceback.format_exc()}"
            )
            return 0

    def list_left_pop(self, key):
        """Pop a value from the left of a list

        Args:
            key: The list key

        Returns:
            The popped value, or None if the list is empty
        """
        try:
            self.client._check_connection()
            key_bytes = self.client._to_bytes(key)
            result = self.lib.ListLeftPop(self.client.client, key_bytes)
            logger.debug(f"ListLeftPop raw result: {result}")

            if result:
                try:
                    value = self.client._from_bytes(result)
                    self.client._free_string(result)
                    logger.debug(f"ListLeftPop on key '{key}'. Popped value: {value}")
                    return value
                except Exception as e:
                    logger.error(f"Error processing ListLeftPop result: {e}")
                    # Try to free if needed
                    try:
                        self.client._free_string(result)
                    except Exception as free_e:
                        logger.error(f"Error freeing string in ListLeftPop: {free_e}")
                    return None
            logger.debug(f"ListLeftPop on key '{key}'. List is empty.")
            return None
        except ConnectionError as e:
            logger.error(f"Connection error in list_left_pop: {e}")
            raise
        except Exception as e:
            logger.error(
                f"Error in list_left_pop: {e}. Traceback:\n{traceback.format_exc()}"
            )
            return None

    def list_right_pop(self, key):
        """Pop a value from the right of a list

        Args:
            key: The list key

        Returns:
            The popped value, or None if the list is empty
        """
        try:
            self.client._check_connection()
            key_bytes = self.client._to_bytes(key)
            result = self.lib.ListRightPop(self.client.client, key_bytes)
            logger.debug(f"ListRightPop raw result: {result}")

            if result:
                try:
                    value = self.client._from_bytes(result)
                    self.client._free_string(result)
                    logger.debug(f"ListRightPop on key '{key}'. Popped value: {value}")
                    return value
                except Exception as e:
                    logger.error(f"Error processing ListRightPop result: {e}")
                    try:
                        self.client._free_string(result)
                    except Exception as free_e:
                        logger.error(f"Error freeing string in ListRightPop: {free_e}")
                    return None
            logger.debug(f"ListRightPop on key '{key}'. List empty")
            return None
        except ConnectionError as e:
            logger.error(f"Connection error in list_right_pop: {e}")
            raise
        except Exception as e:
            logger.error(
                f"Error in list_right_pop: {e}. Traceback:\n{traceback.format_exc()}"
            )
            return None

    def list_range(self, key, start, stop):
        """Get a range of elements from a list

        Args:
            key: The list key
            start: The start index (inclusive)
            stop: The stop index (inclusive)

        Returns:
            A list of values in the specified range
        """
        try:
            self.client._check_connection()
            key_bytes = self.client._to_bytes(key)
            result = self.lib.ListRange(self.client.client, key_bytes, start, stop)
            logger.debug(f"ListRange raw result type: {type(result)}")

            if result and isinstance(result, StringArray):
                try:
                    # Extract values from the StringArray
                    values = []
                    for i in range(result.Count):
                        # Get the string at index i
                        string_ptr = result.Strings[i]
                        if string_ptr:
                            value = self.client._from_bytes(string_ptr)
                            values.append(value)
                    
                    # Free the StringArray structure
                    self.client._free_list(result)
                    logger.debug(f"ListRange on key '{key}' from {start} to {stop}. Values: {values}")
                    return values
                except Exception as e:
                    logger.error(f"Error processing ListRange result: {e}")
                    try:
                        self.client._free_list(result)
                    except Exception as free_e:
                        logger.error(f"Error freeing StringArray in ListRange: {free_e}")
                    return []
            logger.debug(f"ListRange on key '{key}' from {start} to {stop}. Empty list or invalid result type")
            return []
        except ConnectionError as e:
            logger.error(f"Connection error in list_range: {e}")
            raise
        except Exception as e:
            logger.error(
                f"Error in list_range: {e}. Traceback:\n{traceback.format_exc()}"
            )
            return []

    def list_index(self, key, index):
        """Get an element at a specific index in a list

        Args:
            key: The list key
            index: The index of the element

        Returns:
            The element at the specified index, or None if not found
        """
        try:
            self.client._check_connection()
            key_bytes = self.client._to_bytes(key)
            result = self.lib.ListIndex(self.client.client, key_bytes, index)
            if result:
                value = self.client._from_bytes(result)
                self.client._free_string(result)
                logger.debug(f"ListIndex on key '{key}' at index {index}: {value}")
                return value
            logger.debug(f"ListIndex on key '{key}' at index {index}: Not found.")
            return None
        except ConnectionError as e:
            logger.error(f"Connection error in list_index: {e}")
            raise
        except Exception as e:
            logger.error(
                f"Error in list_index: {e}. Traceback:\n{traceback.format_exc()}"
            )
            return None

    def list_set(self, key, index, value):
        """Set an element at a specific index in a list

        Args:
            key: The list key
            index: The index of the element
            value: The value to set

        Returns:
            True if successful
        """
        try:
            self.client._check_connection()
            key_bytes = self.client._to_bytes(key)
            value_bytes = self.client._to_bytes(value)
            result = self.lib.ListSet(self.client.client, key_bytes, index, value_bytes)
            logger.debug(
                f"ListSet on key '{key}' at index {index} with value '{value}': {result}"
            )
            return result
        except ConnectionError as e:
            logger.error(f"Connection error in list_set: {e}")
            raise
        except Exception as e:
            logger.error(
                f"Error in list_set: {e}. Traceback:\n{traceback.format_exc()}"
            )
            return False

    def list_position(self, key, element, rank=1, maxlen=0):
        """Find the position of an element in a list

        Args:
            key: The list key
            element: The element to find
            rank: The rank of the element to find (default: 1)
            maxlen: Maximum number of elements to scan (default: 0, meaning no limit)

        Returns:
            The index of the element, or -1 if not found
        """
        try:
            self.client._check_connection()
            key_bytes = self.client._to_bytes(key)
            element_bytes = self.client._to_bytes(element)
            result = self.lib.ListPosition(
                self.client.client, key_bytes, element_bytes, rank, maxlen
            )
            logger.debug(
                f"ListPosition on key '{key}' for element '{element}' (rank={rank}, maxlen={maxlen}): {result}"
            )
            return result
        except ConnectionError as e:
            logger.error(f"Connection error in list_position: {e}")
            raise
        except Exception as e:
            logger.error(
                f"Error in list_position: {e}. Traceback:\n{traceback.format_exc()}"
            )
            return -1

    def list_trim(self, key, start, stop):
        """Trim a list to the specified range

        Args:
            key: The list key
            start: The start index (inclusive)
            stop: The stop index (inclusive)

        Returns:
            True if successful
        """
        try:
            self.client._check_connection()
            key_bytes = self.client._to_bytes(key)
            result = self.lib.ListTrim(self.client.client, key_bytes, start, stop)
            logger.debug(f"ListTrim on key '{key}' from {start} to {stop}: {result}")
            return result
        except ConnectionError as e:
            logger.error(f"Connection error in list_trim: {e}")
            raise
        except Exception as e:
            logger.error(
                f"Error in list_trim: {e}. Traceback:\n{traceback.format_exc()}"
            )
            return False

    def list_remove(self, key, count, element):
        """Remove elements equal to the given value from a list

        Args:
            key: The list key
            count: The number of occurrences to remove (positive: from head, negative: from tail, 0: all)
            element: The element to remove

        Returns:
            The number of elements removed
        """
        try:
            self.client._check_connection()
            key_bytes = self.client._to_bytes(key)
            element_bytes = self.client._to_bytes(element)
            result = self.lib.ListRemove(self.client.client, key_bytes, count, element_bytes)
            logger.debug(
                f"ListRemove on key '{key}' removing {count} of element '{element}': {result}"
            )
            return result
        except ConnectionError as e:
            logger.error(f"Connection error in list_remove: {e}")
            raise
        except Exception as e:
            logger.error(
                f"Error in list_remove: {e}. Traceback:\n{traceback.format_exc()}"
            )
            return 0
