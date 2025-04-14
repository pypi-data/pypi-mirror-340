"""
Custom exceptions for the Firefly database client.
"""

class ConnectionError(Exception):
    """Exception raised when there is an error connecting to the Firefly server."""
    pass

class AuthenticationError(Exception):
    """Exception raised when there is an error authenticating with the Firefly server."""
    pass

class FireflyError(Exception):
    """Exception raised when there is an error in the Firefly database."""
    pass