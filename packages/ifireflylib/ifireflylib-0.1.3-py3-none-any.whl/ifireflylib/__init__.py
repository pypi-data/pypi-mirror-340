"""
FireflyDB Python Client Library

A high-performance, in-memory database client library organized into two main modules:
- api: Core API interfaces for database operations
- client: Client implementation for connecting to FireflyDB

Features:
- String operations
- List operations
- Hash operations
- Connection management
"""

# Import main client class from client module
from ifireflylib.client.client import IFireflyClient, setup_logging

# Import API components from api module
from ifireflylib.api.string_operations import StringOperations
from ifireflylib.api.list_operations import ListOperations
from ifireflylib.api.hash_operations import HashOperations
from ifireflylib.api.exceptions import ConnectionError, AuthenticationError

__version__ = "0.1.1"
__author__ = "IDSolutions"

__all__ = [
    # Client module exports
    "IFireflyClient",
    "setup_logging",
    
    # API module exports
    "StringOperations",
    "ListOperations",
    "HashOperations",
    "ConnectionError",
    "AuthenticationError",
]