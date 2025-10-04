"""
Integration tests for HTTP transport with MCP JSON-RPC 2.0 protocol.

Tests service-to-service communication over HTTP.
"""

import pytest
from promptware import MCPClient, call_verb
from promptware.exceptions import ConnectionError, InvalidVerbError


def test_http_transport_jsonrpc_format():
    """Test that HTTP transport uses JSON-RPC 2.0 format."""
    # This test assumes user-service is running on port 23450
    # Run manually: python3 generated/user-service/user-service_server.py

    try:
        result = call_verb(
            service="user-service",
            verb="user.create@v1",
            params={"email": "test@example.com", "name": "Test User"},
            address="http://localhost:23450",
            timeout=5,
        )

        # Verify response structure
        assert "metadata" in result
        assert "mode" in result["metadata"]
        assert result["metadata"]["mode"] in ("ide_integrated", "standalone_ai")
        assert "tools_executed" in result["metadata"]

        # Verify MCP envelope (JSON-RPC 2.0 result content)
        assert "input_params" in result

    except ConnectionError:
        pytest.skip("user-service not running on port 23450")


def test_mcp_client_initialize():
    """Test MCP client initialize method."""
    try:
        with MCPClient("http://localhost:23450") as client:
            server_info = client.initialize()

            # Check JSON-RPC 2.0 initialize response
            assert "protocolVersion" in server_info
            assert "capabilities" in server_info
            assert "serverInfo" in server_info
            assert server_info["serverInfo"]["name"] == "user-service"

    except ConnectionError:
        pytest.skip("user-service not running on port 23450")


def test_mcp_client_list_tools():
    """Test MCP client tools/list method."""
    try:
        with MCPClient("http://localhost:23450") as client:
            tools = client.list_tools()

            # Should return list of tool definitions
            assert isinstance(tools, list)
            assert len(tools) > 0

            # Check tool schema structure
            tool = tools[0]
            assert "name" in tool
            assert "description" in tool
            assert "inputSchema" in tool
            assert tool["inputSchema"]["type"] == "object"

    except ConnectionError:
        pytest.skip("user-service not running on port 23450")


def test_service_to_service_communication():
    """Test that one service can call another service."""
    try:
        # Call user-service
        user_result = call_verb(
            service="user-service",
            verb="user.get@v1",
            params={"user_id": "test-123"},
            address="http://localhost:23450",
            timeout=5,
        )

        # Call order-service (which has http tool and can call user-service)
        order_result = call_verb(
            service="order-service",
            verb="order.create@v1",
            params={"user_id": "test-123", "items": ["item1", "item2"], "total_amount": "99.99"},
            address="http://localhost:23451",
            timeout=5,
        )

        # Both should respond
        assert user_result["metadata"]["agent_name"] == "user-service"
        assert order_result["metadata"]["agent_name"] == "order-service"

        # Order service should have executed http tool (can call user-service)
        assert "http" in order_result["metadata"]["tools_executed"]

    except ConnectionError:
        pytest.skip("Services not running on ports 23450/23451")


def test_invalid_verb_error():
    """Test that invalid verb returns proper error."""
    try:
        with pytest.raises(InvalidVerbError):
            call_verb(
                service="user-service",
                verb="nonexistent.verb@v1",
                params={},
                address="http://localhost:23450",
                timeout=5,
            )
    except ConnectionError:
        pytest.skip("user-service not running on port 23450")


def test_health_endpoint():
    """Test that generated services have health endpoint."""
    import requests

    try:
        response = requests.get("http://localhost:23450/health", timeout=5)
        assert response.status_code == 200

        data = response.json()
        assert data["status"] == "alive"
        assert "uptime_seconds" in data
        assert "timestamp" in data

    except requests.exceptions.ConnectionError:
        pytest.skip("user-service not running on port 23450")


def test_verbs_endpoint():
    """Test that generated services list available verbs."""
    import requests

    try:
        response = requests.get("http://localhost:23450/verbs", timeout=5)
        assert response.status_code == 200

        data = response.json()
        assert "verbs" in data
        assert len(data["verbs"]) > 0

        # Check verb structure - verbs is a list of verb names
        assert isinstance(data["verbs"], list)
        verb_names = data["verbs"]
        assert "user.create@v1" in verb_names
        assert "user.get@v1" in verb_names

    except requests.exceptions.ConnectionError:
        pytest.skip("user-service not running on port 23450")
