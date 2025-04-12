"""
API package for FireflyDB.

This package provides the API implementation for interacting with FireflyDB servers,
including string operations, list operations, and hash operations.
"""

from ifireflylib.api.string_operations import StringOperations
from ifireflylib.api.list_operations import ListOperations
from ifireflylib.api.hash_operations import HashOperations
from ifireflylib.api.exceptions import ConnectionError, AuthenticationError

__all__ = ["StringOperations", "ListOperations", "HashOperations", "ConnectionError", "AuthenticationError"]