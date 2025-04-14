"""
FireflyDB Client Implementation

This module provides the main client class for connecting to and interacting with FireflyDB.
"""

import os
import traceback

from ctypes import cdll
from ifireflylib.api.exceptions import ConnectionError, AuthenticationError
from ifireflylib.api.string_operations import StringOperations
from ifireflylib.api.list_operations import ListOperations
from ifireflylib.api.hash_operations import HashOperations
from ifireflylib.client.utils import (
    setup_library_functions,
    to_bytes,
    from_bytes,
    free_string,
    free_list,
    free_dictionary,
    setup_logging,
)

# Set up logging
logger = setup_logging()

class IFireflyClient:
    """Main client class for FireflyDB"""

    def __init__(self, host="localhost", port=6379, password=None):
        """Initialize the Firefly database connection

        Args:
            host: Hostname of the Firefly server (default: localhost)
            port: Port number of the Firefly server (default: 6379)
            password: Optional password for authentication
        """
        self.client = None
        self.lib = None
        self._load_library()
        self._connect(host, port, password)
        
        # Initialize operation mixins using composition
        self.string_ops = StringOperations(self)
        self.list_ops = ListOperations(self)
        self.hash_ops = HashOperations(self)

    def _load_library(self):
        """Load the appropriate Firefly library for the current platform"""
        try:
            # Get the path to the native directory
            native_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "ifireflylib", "native")
            
            # Determine platform-specific library name
            import platform
            system = platform.system().lower()
            
            # Map system to library name
            if system == "windows":
                lib_name = "libFireflyClient.dll"
            elif system == "linux":
                lib_name = "libFireflyClient.so"
            elif system == "darwin":  # macOS
                lib_name = "libFireflyClient.dylib"
            else:
                raise OSError(f"Unsupported platform: {system}")
            
            # Complete path to the library file
            lib_path = os.path.join(native_path, lib_name)
            
            # Load the library using the utility function
            self.lib = cdll.LoadLibrary(lib_path)
            
            # Set up the library functions
            setup_library_functions(self.lib)
            
        except Exception as e:
            logger.error(f"Error loading library: {e}")
            raise

    def _connect(self, host, port, password=None):
        """Connect to the Firefly server and authenticate if needed"""
        try:
            # Convert host to bytes for C API
            host_bytes = to_bytes(host)
            logger.debug(f"Connecting to {host}:{port}")

            # Create client
            self.client = self.lib.CreateClient(host_bytes, port)
            if not self.client:
                raise ConnectionError(
                    f"Failed to connect to Firefly server at {host}:{port}"
                )
            logger.debug("Client created successfully")

            # Authenticate if password is provided
            if password:
                password_bytes = to_bytes(password)
                logger.debug("Authenticating...")
                if not self.lib.Authenticate(self.client, password_bytes):
                    self.close()
                    raise AuthenticationError("Authentication failed")
                logger.debug("Authentication successful")
            else:
                logger.debug("No password provided, skipping authentication")

        except ConnectionError as e:
            logger.error(f"Connection error: {e}")
            if self.client:
                self.close()  # Clean up the client if it was created
            raise  # Re-raise the exception for the caller to handle
        except Exception as e:
            logger.error(f"Unexpected error during connection: {e}")
            if self.client:
                self.close()
            raise

    def close(self):
        """Close the connection to the Firefly server"""
        try:
            if self.client:
                logger.debug("Destroying client connection")
                self.lib.DestroyClient(self.client)
                self.client = None
                logger.debug("Client connection destroyed")
            else:
                logger.debug("Client connection already closed")
        except Exception as e:
            logger.error(f"Error closing connection: {e}")
            # Do not re-raise here, as close() should not throw exceptions in normal usage.
            # Caller has no recovery options.

    def __enter__(self):
        """Context manager entry"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.close()
        if exc_type:  # Log the exception if one occurred within the context
            logger.error(
                f"Exception in context: {exc_type.__name__}, {exc_val}. Traceback:\n{''.join(traceback.format_exception(exc_type, exc_val, exc_tb))}"
            )

    def _check_connection(self):
        """Check if the client is connected"""
        if not self.client:
            raise ConnectionError("Not connected to Firefly server")

    def _to_bytes(self, value):
        """Convert a value to bytes for C API"""
        return to_bytes(value)

    def _from_bytes(self, value):
        """Convert bytes from C API to string"""
        return from_bytes(value)

    def _free_string(self, ptr):
        """Free a string pointer allocated by the C API"""
        free_string(self.lib, ptr)
    
    def _free_list(self, list):
        """Free an array allocated by the C API"""
        free_list(self.lib, list)
    
    def _free_dictionary(self, dict):
        """Free a dictionary allocated by the C API"""
        free_dictionary(self.lib, dict)

    def execute_command(self, command, *args):
        """Execute a command on the server

        Args:
            command: The command to execute
            *args: The command arguments

        Returns:
            The command result
        """
        try:
            self._check_connection()
            command_bytes = self._to_bytes(command)
            
            # Format arguments as a space-separated string
            args_str = " ".join(str(arg) for arg in args)
            args_bytes = self._to_bytes(args_str)
            
            result = self.lib.ExecuteCommand(self.client, command_bytes, args_bytes)
            logger.debug(f"Executing command: {command} with args: {args}")
            
            if result:
                try:
                    # If the result is already a bytes object, we don't need to free it
                    if isinstance(result, bytes):
                        logger.debug("Result is a bytes object, decoding")
                        return result.decode("utf-8")
                    
                    # Otherwise, treat it as a C pointer that needs to be freed
                    value = self._from_bytes(result)
                    self._free_string(result)
                    return value
                except Exception as e:
                    logger.error(f"Error processing command result: {e}")
                    # Try to free if needed
                    if result and not isinstance(result, bytes):
                        try:
                            self._free_string(result)
                        except Exception as free_e:
                            logger.error(f"Error freeing command result: {free_e}")
                    return None
            return None
        except ConnectionError as e:
            logger.error(f"Connection error in execute_command: {e}")
            raise
        except Exception as e:
            logger.error(
                f"Error in execute_command: {e}. Traceback:\n{traceback.format_exc()}"
            )
            return None

    def ping(self):
        """Test the connection to the server

        Returns:
            True if the server responds with PONG, False otherwise
        """
        try:
            logger.debug("Sending PING command")
            self._check_connection()

            # Add a try/except specifically around execute_command
            try:
                response = self.execute_command("PING", "")
                logger.debug(f"Raw ping response: '{response}'")
            except Exception as e:
                logger.error(f"Exception in execute_command during ping: {e}")
                return False

            # Log the type and value of the response
            logger.debug(
                f"Response type: {type(response)}, value: '{response}'"
            )

            if response is None:
                logger.warning("Received NULL response from ping")
                return False

            # Normalize: strip whitespace, remove leading '+', uppercase
            try:
                normalized = response.strip().lstrip("+").upper()
                logger.debug(f"Normalized response: '{normalized}'")

                if normalized == "PONG":
                    logger.debug(
                        "PONG found in normalized response - ping successful"
                    )
                    return True
                else:
                    logger.warning(
                        f"PONG not found in response: raw='{response}', normalized='{normalized}'"
                    )
                    return False
            except AttributeError:
                logger.error(f"Unable to process ping response: {response}")
                return False
        except Exception as e:
            logger.error(
                f"Ping failed: {e}. Traceback:\n{traceback.format_exc()}"
            )
            return False 