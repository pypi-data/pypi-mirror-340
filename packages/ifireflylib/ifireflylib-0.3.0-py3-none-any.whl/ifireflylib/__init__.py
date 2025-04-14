from .client.client import IFireflyClient, setup_logging
from .client.utils import StringArray, KeyValuePair, Dictionary
from .api.string_operations import StringOperations
from .api.list_operations import ListOperations
from .api.hash_operations import HashOperations
from .api.exceptions import ConnectionError, AuthenticationError

__all__ = [
    "IFireflyClient",
    "setup_logging",
    "StringArray",
    "KeyValuePair",
    "Dictionary",
    "StringOperations",
    "ListOperations",
    "HashOperations",
    "AuthenticationError",
    "ConnectionError",
    "FireflyError"
]