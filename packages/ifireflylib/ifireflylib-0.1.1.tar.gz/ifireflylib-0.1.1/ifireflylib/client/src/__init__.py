"""
FireflyDB Client Module

This module provides the main client interface for connecting to and interacting with FireflyDB.
All client functionality is implemented in the src folder of the client module.
"""

from .client import IFireflyClient
from .utils import setup_logging

__all__ = ["IFireflyClient", "setup_logging"]
