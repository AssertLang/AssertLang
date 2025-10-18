"""
Unit tests for AssertLang MCP client library.

Tests the client API, transport layer, and error handling.
"""

import sys
from pathlib import Path
from unittest.mock import MagicMock, Mock, patch

import requests

import pytest

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from assertlang.client import MCPClient, call_verb
from assertlang.exceptions import (
    ConnectionError,
    InvalidParamsError,
    InvalidVerbError,
    ProtocolError,
    ServiceUnavailableError,
    TimeoutError,
)
from assertlang.transport import HTTPTransport


def test_mcp_client_initialization():
    """Test MCPClient initialization."""
    client = MCPClient("http://localhost:23450", timeout=10.0, retries=2)

    assert client.address == "http://localhost:23450"
    assert client.transport.base_url == "http://localhost:23450"
    assert client.transport.timeout == 10.0
    assert client.transport.retries == 2
    assert client._initialized is False
    assert client._server_info is None


def test_mcp_client_context_manager():
    """Test MCPClient as context manager."""
    with patch.object(HTTPTransport, "close") as mock_close:
        with MCPClient("http://localhost:23450") as client:
            assert client is not None

        mock_close.assert_called_once()


def test_http_transport_request_success():
    """Test successful HTTP transport request."""
    transport = HTTPTransport("http://localhost:23450")

    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"jsonrpc": "2.0", "id": 1, "result": {"status": "ok"}}

    with patch.object(transport.session, "post", return_value=mock_response):
        result = transport.request("initialize", params={})

        assert result == {"status": "ok"}


def test_http_transport_invalid_json():
    """Test handling of invalid JSON response."""
    transport = HTTPTransport("http://localhost:23450")

    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.side_effect = ValueError("Invalid JSON")

    with patch.object(transport.session, "post", return_value=mock_response):
        with pytest.raises(ProtocolError, match="Invalid JSON response"):
            transport.request("initialize")


def test_http_transport_missing_jsonrpc_field():
    """Test handling of response missing jsonrpc field."""
    transport = HTTPTransport("http://localhost:23450")

    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"id": 1, "result": {}}

    with patch.object(transport.session, "post", return_value=mock_response):
        with pytest.raises(ProtocolError, match="missing jsonrpc field"):
            transport.request("initialize")


def test_http_transport_id_mismatch():
    """Test handling of response with mismatched ID."""
    transport = HTTPTransport("http://localhost:23450")

    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"jsonrpc": "2.0", "id": 999, "result": {}}  # Wrong ID

    with patch.object(transport.session, "post", return_value=mock_response):
        with pytest.raises(ProtocolError, match="ID mismatch"):
            transport.request("initialize", request_id=1)


def test_http_transport_verb_not_found_error():
    """Test handling of verb not found error."""
    transport = HTTPTransport("http://localhost:23450")

    mock_response = Mock()
    mock_response.status_code = 404
    mock_response.json.return_value = {
        "jsonrpc": "2.0",
        "id": 1,
        "error": {"code": -32601, "message": "Method not found: unknown.verb@v1"},
    }

    with patch.object(transport.session, "post", return_value=mock_response):
        with pytest.raises(InvalidVerbError, match="unknown.verb@v1"):
            transport.request("tools/call", params={"name": "unknown.verb@v1"})


def test_http_transport_invalid_params_error():
    """Test handling of invalid params error."""
    transport = HTTPTransport("http://localhost:23450")

    mock_response = Mock()
    mock_response.status_code = 400
    mock_response.json.return_value = {
        "jsonrpc": "2.0",
        "id": 1,
        "error": {"code": -32602, "message": "Invalid params: missing required field 'user_id'"},
    }

    with patch.object(transport.session, "post", return_value=mock_response):
        with pytest.raises(InvalidParamsError, match="missing required field"):
            transport.request("tools/call")


def test_http_transport_timeout():
    """Test timeout handling with retries."""
    transport = HTTPTransport("http://localhost:23450", retries=2, initial_delay=0.01)

    with patch.object(transport.session, "post", side_effect=requests.exceptions.Timeout):
        with pytest.raises(TimeoutError, match="timed out"):
            transport.request("initialize")


def test_http_transport_connection_error():
    """Test connection error handling with retries."""
    transport = HTTPTransport("http://localhost:23450", retries=2, initial_delay=0.01)

    with patch.object(transport.session, "post", side_effect=requests.exceptions.ConnectionError):
        with pytest.raises(ConnectionError, match="Failed to connect"):
            transport.request("initialize")


def test_http_transport_server_error_retries():
    """Test 5xx server error triggers retries."""
    transport = HTTPTransport("http://localhost:23450", retries=2, initial_delay=0.01)

    mock_response = Mock()
    mock_response.status_code = 503
    mock_response.text = "Service Unavailable"

    with patch.object(transport.session, "post", return_value=mock_response):
        with pytest.raises(ServiceUnavailableError, match="503"):
            transport.request("initialize")


def test_http_transport_retry_success_after_failure():
    """Test successful retry after transient failure."""
    transport = HTTPTransport("http://localhost:23450", retries=3, initial_delay=0.01)

    # First call fails, second succeeds
    fail_response = Mock()
    fail_response.status_code = 503
    fail_response.text = "Service Unavailable"

    success_response = Mock()
    success_response.status_code = 200
    success_response.json.return_value = {"jsonrpc": "2.0", "id": 1, "result": {"status": "ok"}}

    with patch.object(transport.session, "post", side_effect=[fail_response, success_response]):
        result = transport.request("initialize")
        assert result == {"status": "ok"}


def test_mcp_client_initialize():
    """Test MCPClient.initialize() method."""
    client = MCPClient("http://localhost:23450")

    mock_result = {
        "protocolVersion": "0.1.0",
        "capabilities": {"tools": {}, "prompts": {}},
        "serverInfo": {"name": "test-service", "version": "v1"},
    }

    with patch.object(client.transport, "request", return_value=mock_result):
        result = client.initialize()

        assert result == mock_result
        assert client._initialized is True
        assert client._server_info == {"name": "test-service", "version": "v1"}


def test_mcp_client_list_tools():
    """Test MCPClient.list_tools() method."""
    client = MCPClient("http://localhost:23450")

    mock_result = {
        "tools": [
            {"name": "user.get@v1", "description": "Get user"},
            {"name": "user.create@v1", "description": "Create user"},
        ]
    }

    with patch.object(client.transport, "request", return_value=mock_result):
        tools = client.list_tools()

        assert len(tools) == 2
        assert tools[0]["name"] == "user.get@v1"
        assert client._available_tools is not None
        assert "user.get@v1" in client._available_tools


def test_mcp_client_call():
    """Test MCPClient.call() method."""
    client = MCPClient("http://localhost:23450")

    mock_result = {
        "input_params": {"user_id": "123"},
        "tool_results": {},
        "metadata": {"mode": "ide_integrated"},
        "user_id": "123",
        "name": "John Doe",
    }

    with patch.object(client.transport, "request", return_value=mock_result):
        result = client.call("user.get@v1", {"user_id": "123"})

        assert result == mock_result
        assert result["input_params"]["user_id"] == "123"
        assert result["metadata"]["mode"] == "ide_integrated"


def test_mcp_client_get_tool_schema():
    """Test MCPClient.get_tool_schema() method."""
    client = MCPClient("http://localhost:23450")

    # Before list_tools is called
    assert client.get_tool_schema("user.get@v1") is None

    # After list_tools
    mock_result = {
        "tools": [
            {"name": "user.get@v1", "description": "Get user", "inputSchema": {"type": "object"}}
        ]
    }

    with patch.object(client.transport, "request", return_value=mock_result):
        client.list_tools()

        schema = client.get_tool_schema("user.get@v1")
        assert schema is not None
        assert schema["name"] == "user.get@v1"
        assert "inputSchema" in schema


def test_call_verb_helper():
    """Test call_verb() helper function."""
    mock_result = {
        "input_params": {"user_id": "123"},
        "tool_results": {},
        "metadata": {"mode": "ide_integrated"},
        "name": "John Doe",
    }

    with patch.object(HTTPTransport, "request", return_value=mock_result):
        result = call_verb(
            service="user-service",
            verb="user.get@v1",
            params={"user_id": "123"},
            address="http://localhost:23450",
        )

        assert result == mock_result


def test_call_verb_default_address():
    """Test call_verb() uses default address if not provided."""
    mock_result = {"status": "ok"}

    with patch.object(HTTPTransport, "request", return_value=mock_result):
        with patch("assertlang.client.MCPClient") as MockClient:
            mock_client = MagicMock()
            mock_client.call.return_value = mock_result
            MockClient.return_value.__enter__.return_value = mock_client

            call_verb(service="user-service", verb="user.get@v1", params={"user_id": "123"})

            # Verify default address was used
            MockClient.assert_called_once()
            call_args = MockClient.call_args[0]
            assert call_args[0] == "http://localhost:23450"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
