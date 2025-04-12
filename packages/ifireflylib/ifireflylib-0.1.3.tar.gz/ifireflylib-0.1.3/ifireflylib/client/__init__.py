"""
Client package for FireflyDB.

This package provides the client implementation for connecting to and
interacting with FireflyDB servers.
"""

from ifireflylib.client.client import IFireflyClient
from ifireflylib.client.utils import setup_logging

__all__ = ["IFireflyClient", "setup_logging"]