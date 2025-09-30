"""Promptware SDK - Host integration for Promptware daemon."""

from .mcp import mcp, MCP
from .timeline import TimelineReader
from .errors import (
    PromptwareError,
    CompatibilityError,
    E_RUNTIME,
    E_POLICY,
    E_TIMEOUT,
    E_BUILD,
    E_JSON,
    E_FS,
    E_METHOD,
    E_COMPAT,
)
from .types import ToolRequest, ToolResponse, TimelineEvent, MCPEnvelope
from .version import __version__

__all__ = [
    # MCP verbs
    "mcp",
    "MCP",
    # Timeline
    "TimelineReader",
    # Errors
    "PromptwareError",
    "CompatibilityError",
    "E_RUNTIME",
    "E_POLICY",
    "E_TIMEOUT",
    "E_BUILD",
    "E_JSON",
    "E_FS",
    "E_METHOD",
    "E_COMPAT",
    # Types
    "ToolRequest",
    "ToolResponse",
    "TimelineEvent",
    "MCPEnvelope",
    # Version
    "__version__",
]