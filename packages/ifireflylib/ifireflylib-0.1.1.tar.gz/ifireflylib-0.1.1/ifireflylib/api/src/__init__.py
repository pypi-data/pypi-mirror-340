"""
FireflyDB API Module

This module provides the core API interfaces for FireflyDB operations:
- String operations
- List operations
- Hash operations
- Exception handling
"""

from .string_operations import StringOperations
from .list_operations import ListOperations
from .hash_operations import HashOperations
from .exceptions import ConnectionError, AuthenticationError

__all__ = [
    "StringOperations",
    "ListOperations",
    "HashOperations",
    "ConnectionError",
    "AuthenticationError",
]