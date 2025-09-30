"""
Promptware Python Client Library

Provides MCP client for calling Promptware services over HTTP.
"""

from .client import MCPClient, call_verb
from .exceptions import (
    MCPError,
    ConnectionError,
    TimeoutError,
    ServiceUnavailableError,
    InvalidVerbError,
    InvalidParamsError,
    ProtocolError,
)

__version__ = "0.1.0"

__all__ = [
    "MCPClient",
    "call_verb",
    "MCPError",
    "ConnectionError",
    "TimeoutError",
    "ServiceUnavailableError",
    "InvalidVerbError",
    "InvalidParamsError",
    "ProtocolError",
]
