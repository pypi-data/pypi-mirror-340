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
from .client.src.client import IFireflyClient
from .client.src.utils import setup_logging

# Import API components from api module
from .api.src.string_operations import StringOperations
from .api.src.list_operations import ListOperations
from .api.src.hash_operations import HashOperations
from .api.src.exceptions import ConnectionError, AuthenticationError

__version__ = "0.1.0"
__author__ = "FireflyDB Team"

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