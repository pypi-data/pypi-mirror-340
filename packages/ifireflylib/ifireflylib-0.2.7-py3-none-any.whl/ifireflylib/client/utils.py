"""
Utility functions for the FireflyDB client.

This module provides common utility functions used across the client implementation.
"""

import logging
import os
import platform
import sys
from ctypes import cdll, c_char_p, c_bool, c_void_p, c_int

logger = logging.getLogger("FireflyDB.Client.Utils")

def load_library(lib_path):
    """Load the appropriate Firefly library for the current platform
    
    Args:
        lib_path: Base path to the native directory
        
    Returns:
        The loaded library
        
    Raises:
        FileNotFoundError: If the library file is not found
        OSError: If the library cannot be loaded
    """
    try:
        if platform.system() == "Windows":
            lib_file = os.path.join(lib_path, "libFireflyClient.dll")
        else:  # Linux/macOS
            lib_file = os.path.join(lib_path, "libFireflyClient.so")

        if not os.path.exists(lib_file):
            raise FileNotFoundError(f"Firefly library not found: {lib_file}")

        # Load the library
        lib = cdll.LoadLibrary(lib_file)
        if lib is None:  # Explicitly check for None
            raise OSError("Failed to load the Firefly library")

        logger.debug(f"Firefly library loaded from: {lib_file}")
        return lib

    except FileNotFoundError as e:
        logger.error(f"Error loading library: {e}")
        raise  # Re-raise to halt execution
    except OSError as e:
        logger.error(f"OS Error loading library: {e}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error loading library: {e}")
        raise

def setup_library_functions(lib):
    """Set up the library function signatures
    
    Args:
        lib: The loaded library
    """
    # Set up the library function signatures
    lib.CreateClient.restype = c_void_p
    lib.CreateClient.argtypes = [c_char_p, c_int]
    lib.DestroyClient.argtypes = [c_void_p]
    lib.Authenticate.restype = c_bool
    lib.Authenticate.argtypes = [c_void_p, c_char_p]
    lib.StringSet.restype = c_bool
    lib.StringSet.argtypes = [c_void_p, c_char_p, c_char_p]
    lib.StringGet.restype = c_char_p
    lib.StringGet.argtypes = [c_void_p, c_char_p]
    lib.FreeString.argtypes = [c_char_p]
    lib.ListLeftPush.restype = c_int
    lib.ListLeftPush.argtypes = [c_void_p, c_char_p, c_char_p]
    lib.ListRightPush.restype = c_int
    lib.ListRightPush.argtypes = [c_void_p, c_char_p, c_char_p]
    lib.ListLeftPop.restype = c_char_p
    lib.ListLeftPop.argtypes = [c_void_p, c_char_p]
    lib.ListRightPop.restype = c_char_p
    lib.ListRightPop.argtypes = [c_void_p, c_char_p]
    lib.ListRange.restype = c_char_p
    lib.ListRange.argtypes = [c_void_p, c_char_p, c_int, c_int]
    lib.ListIndex.restype = c_char_p
    lib.ListIndex.argtypes = [c_void_p, c_char_p, c_int]
    lib.ListSet.restype = c_bool
    lib.ListSet.argtypes = [c_void_p, c_char_p, c_int, c_char_p]
    lib.ListPosition.restype = c_int
    lib.ListPosition.argtypes = [
        c_void_p,
        c_char_p,
        c_char_p,
        c_int,
        c_int,
    ]
    lib.ListTrim.restype = c_bool
    lib.ListTrim.argtypes = [c_void_p, c_char_p, c_int, c_int]
    lib.ListRemove.restype = c_int
    lib.ListRemove.argtypes = [
        c_void_p,
        c_char_p,
        c_int,
        c_char_p,
    ]
    lib.HashSet.restype = c_bool
    lib.HashSet.argtypes = [
        c_void_p,
        c_char_p,
        c_char_p,
        c_char_p,
    ]
    lib.HashMultiSet.argtypes = [c_void_p, c_char_p, c_char_p]
    lib.HashMultiSet.restype = c_bool
    lib.HashGet.restype = c_char_p
    lib.HashGet.argtypes = [c_void_p, c_char_p, c_char_p]
    lib.HashDelete.restype = c_bool
    lib.HashDelete.argtypes = [c_void_p, c_char_p, c_char_p]
    lib.HashFieldExists.restype = c_bool
    lib.HashFieldExists.argtypes = [c_void_p, c_char_p, c_char_p]
    lib.HashGetAll.restype = c_char_p
    lib.HashGetAll.argtypes = [c_void_p, c_char_p]
    lib.Keys.restype = c_char_p
    lib.Keys.argtypes = [c_void_p, c_char_p]
    lib.ExecuteCommand.restype = c_char_p
    lib.ExecuteCommand.argtypes = [c_void_p, c_char_p, c_char_p]

def to_bytes(value):
    """Convert a value to bytes for C API
    
    Args:
        value: The value to convert
        
    Returns:
        The value as bytes
    """
    if isinstance(value, bytes):
        return value
    return str(value).encode("utf-8")

def from_bytes(value):
    """Convert bytes from C API to string
    
    Args:
        value: The bytes to convert
        
    Returns:
        The decoded string, or None if conversion fails
    """
    try:
        if value is None:
            logger.debug("from_bytes received None value")
            return None

        if not value:  # Zero value check
            logger.debug("from_bytes received empty value")
            return ""

        # Try to decode safely
        try:
            result = value.decode("utf-8")
            return result
        except UnicodeDecodeError as e:
            logger.error(f"Unicode decode error in from_bytes: {e}")
            # Try with a more forgiving approach
            return value.decode("utf-8", errors="replace")
    except Exception as e:
        logger.error(f"Error in from_bytes: {e}")
        return None

def free_string(lib, ptr):
    """Free a string pointer allocated by the C API
    
    Args:
        lib: The loaded library
        ptr: The pointer to free
    """
    logger.debug("Starting free string")
    try:
        # Skip if ptr is a bytes object (Python managed memory)
        if isinstance(ptr, bytes):
            logger.debug("Skipping free for bytes object")
            return
            
        # Check if ptr is valid and non-zero
        if ptr and ptr != 0:
            # Wrap in another try/except to catch any errors from the FreeString call
            try:
                lib.FreeString(ptr)
                logger.debug("String freed successfully")
            except Exception as inner_e:
                logger.error(f"Error in FreeString call: {inner_e}")
        else:
            logger.debug(f"Skipping free for null or zero pointer: {ptr}")
    except Exception as e:
        logger.error(f"Error in free_string outer block: {e}")
        # Do not re-raise; resource cleanup, caller cannot handle.

def setup_logging():
    """Set up logging for the client
    
    Returns:
        The configured logger
    """
    logger = logging.getLogger("FireflyDB.Client")
    
    # FIREFLY_DEBUG is set to 'true' if debug logging is desired
    enable_debug = os.environ.get("FIREFLY_DEBUG", "false").lower() == "true"
    
    if not logger.handlers and enable_debug:
        logging.basicConfig(
            level=logging.DEBUG,
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            handlers=[
                logging.FileHandler("firefly_debug.log"),
                logging.StreamHandler(sys.stdout),
            ],
        )
    
    return logger