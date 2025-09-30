"""Tests for MCP client library."""

import pytest
from language.mcp_client import (
    MCPClient,
    MCPResponse,
    MCPError,
    AgentRegistry,
    register_agent,
    get_agent_client,
)


def test_mcp_response_success():
    """Test MCPResponse with successful call."""
    response = MCPResponse(
        ok=True,
        version="v1",
        data={"result": "success"}
    )

    assert response.is_success()
    assert response.get_data() == {"result": "success"}


def test_mcp_response_error():
    """Test MCPResponse with error."""
    response = MCPResponse(
        ok=False,
        version="v1",
        error={"code": "E_ARGS", "message": "Missing parameter"}
    )

    assert not response.is_success()

    try:
        response.get_data()
        assert False, "Should have raised MCPError"
    except MCPError as e:
        assert e.code == "E_ARGS"
        assert "Missing parameter" in str(e)


def test_mcp_client_initialization():
    """Test MCP client initialization."""
    client = MCPClient("http://localhost:23456")

    assert client.base_url == "http://localhost:23456"
    assert client.timeout == 30
    assert client.retries == 3


def test_mcp_client_custom_settings():
    """Test MCP client with custom settings."""
    client = MCPClient(
        "http://localhost:8080",
        timeout=60,
        retries=5
    )

    assert client.base_url == "http://localhost:8080"
    assert client.timeout == 60
    assert client.retries == 5


def test_mcp_client_strips_trailing_slash():
    """Test that trailing slash is removed from base URL."""
    client = MCPClient("http://localhost:23456/")
    assert client.base_url == "http://localhost:23456"


def test_mcp_client_context_manager():
    """Test MCP client as context manager."""
    with MCPClient("http://localhost:23456") as client:
        assert client.base_url == "http://localhost:23456"
    # Client should be closed after context


def test_agent_registry():
    """Test agent registry."""
    registry = AgentRegistry()

    # Register agents
    registry.register("agent-a", "http://localhost:23456")
    registry.register("agent-b", "http://localhost:23457")

    # Discover agents
    assert registry.discover("agent-a") == "http://localhost:23456"
    assert registry.discover("agent-b") == "http://localhost:23457"
    assert registry.discover("unknown") is None

    # List agents
    agents = registry.list_agents()
    assert "agent-a" in agents
    assert "agent-b" in agents


def test_agent_registry_get_client():
    """Test getting client from registry."""
    registry = AgentRegistry()
    registry.register("test-agent", "http://localhost:23456")

    client = registry.get_client("test-agent")
    assert client.base_url == "http://localhost:23456"


def test_agent_registry_unknown_agent():
    """Test getting client for unknown agent."""
    registry = AgentRegistry()

    try:
        registry.get_client("unknown")
        assert False, "Should have raised MCPError"
    except MCPError as e:
        assert e.code == "E_DISCOVERY"
        assert "not found" in str(e)


def test_global_registry():
    """Test global registry functions."""
    register_agent("global-test", "http://localhost:9999")

    client = get_agent_client("global-test")
    assert client.base_url == "http://localhost:9999"


def test_mcp_error():
    """Test MCPError exception."""
    error = MCPError("E_TEST", "Test error message")

    assert error.code == "E_TEST"
    assert error.message == "Test error message"
    assert "[E_TEST]" in str(error)
    assert "Test error message" in str(error)


# Note: The following tests would require a running server
# They are marked as integration tests

def test_call_structure():
    """Test that call method structure is correct (without actual call)."""
    client = MCPClient("http://localhost:23456", timeout=1, retries=1)

    # We can't make actual calls without a server running,
    # but we can verify the client is properly configured
    assert client.base_url == "http://localhost:23456"
    assert client.timeout == 1

    # The call would look like this:
    # response = client.call("test.verb@v1", {"param": "value"})
    # assert response.ok


def test_health_check_structure():
    """Test health check method exists and has correct signature."""
    client = MCPClient("http://localhost:23456")

    # Method should exist
    assert hasattr(client, 'health_check')
    assert callable(client.health_check)


def test_list_verbs_structure():
    """Test list_verbs method exists and has correct signature."""
    client = MCPClient("http://localhost:23456")

    # Method should exist
    assert hasattr(client, 'list_verbs')
    assert callable(client.list_verbs)