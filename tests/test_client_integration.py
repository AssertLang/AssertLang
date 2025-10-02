"""
Integration tests for Promptware MCP client library.

Tests client against a real generated HTTP server.
"""

import importlib.util
import os
import sys
import tempfile
import threading
import time
from pathlib import Path

import pytest

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

import uvicorn

from language.mcp_server_generator import generate_mcp_server_from_pw
from promptware.client import MCPClient, call_verb
from promptware.exceptions import InvalidVerbError


@pytest.fixture(scope="module")
def test_server():
    """
    Start a test HTTP server in the background.

    Generates and runs a real MCP HTTP server for integration testing.
    """
    # Generate server code
    pw_code = """
lang python
agent test-integration
port 23470

tools:
  - http

expose echo@v1:
  params:
    message string
  returns:
    echo string

expose calculate@v1:
  params:
    a int
    b int
  returns:
    sum int
"""

    server_code = generate_mcp_server_from_pw(pw_code)

    # Save to temp file
    with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
        f.write(server_code)
        temp_path = f.name

    try:
        # Load server module
        spec = importlib.util.spec_from_file_location("test_server", temp_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        # Start server in background thread
        def run_server():
            uvicorn.run(module.app, host="127.0.0.1", port=23470, log_level="error")

        server_thread = threading.Thread(target=run_server, daemon=True)
        server_thread.start()

        # Wait for server to start
        time.sleep(2)

        yield "http://127.0.0.1:23470"

        # Cleanup happens automatically (daemon thread)

    finally:
        os.unlink(temp_path)


def test_client_initialize(test_server):
    """Test client can initialize connection to server."""
    client = MCPClient(test_server)

    result = client.initialize()

    assert "protocolVersion" in result
    assert result["protocolVersion"] == "0.1.0"
    assert "serverInfo" in result
    assert result["serverInfo"]["name"] == "test-integration"


def test_client_list_tools(test_server):
    """Test client can list tools from server."""
    client = MCPClient(test_server)

    tools = client.list_tools()

    assert len(tools) == 2
    tool_names = [t["name"] for t in tools]
    assert "echo@v1" in tool_names
    assert "calculate@v1" in tool_names

    # Check schema
    echo_tool = next(t for t in tools if t["name"] == "echo@v1")
    assert "inputSchema" in echo_tool
    assert "message" in echo_tool["inputSchema"]["properties"]


def test_client_call_verb(test_server):
    """Test client can call a verb successfully."""
    client = MCPClient(test_server)

    result = client.call("echo@v1", {"message": "hello world"})

    assert "input_params" in result
    assert result["input_params"]["message"] == "hello world"
    assert "metadata" in result
    assert result["metadata"]["agent_name"] == "test-integration"
    assert result["metadata"]["mode"] == "ide_integrated"


def test_client_call_with_tools(test_server):
    """Test client receives tool execution results."""
    client = MCPClient(test_server)

    # Call echo which should trigger http tool execution
    result = client.call(
        "echo@v1", {"message": "test", "url": "https://httpbin.org/get", "method": "GET"}
    )

    assert "tool_results" in result
    assert "http" in result["tool_results"]

    http_result = result["tool_results"]["http"]
    assert http_result["ok"] is True
    assert "data" in http_result


def test_client_invalid_verb(test_server):
    """Test client raises InvalidVerbError for unknown verbs."""
    client = MCPClient(test_server)

    with pytest.raises(InvalidVerbError, match="unknown.verb"):
        client.call("unknown.verb@v1", {"param": "value"})


def test_client_missing_params(test_server):
    """Test server validates required parameters."""
    client = MCPClient(test_server)

    # echo@v1 requires 'message' parameter
    # Server's generated handler checks for required params and returns error
    from promptware.exceptions import MCPError

    with pytest.raises(MCPError, match="Missing required parameter"):
        client.call("echo@v1", {})


def test_call_verb_helper(test_server):
    """Test call_verb() helper function."""
    result = call_verb(
        service="test-integration",
        verb="echo@v1",
        params={"message": "hello from helper"},
        address=test_server,
    )

    assert result["input_params"]["message"] == "hello from helper"
    assert result["metadata"]["agent_name"] == "test-integration"


def test_client_context_manager(test_server):
    """Test client works as context manager."""
    with MCPClient(test_server) as client:
        result = client.call("echo@v1", {"message": "context test"})
        assert result["input_params"]["message"] == "context test"


def test_client_get_tool_schema(test_server):
    """Test client can retrieve tool schema after list_tools."""
    client = MCPClient(test_server)

    # Before listing
    assert client.get_tool_schema("echo@v1") is None

    # After listing
    client.list_tools()

    schema = client.get_tool_schema("echo@v1")
    assert schema is not None
    assert schema["name"] == "echo@v1"
    assert "inputSchema" in schema


def test_client_multiple_calls(test_server):
    """Test client can make multiple calls."""
    client = MCPClient(test_server)

    # First call
    result1 = client.call("echo@v1", {"message": "first"})
    assert result1["input_params"]["message"] == "first"

    # Second call
    result2 = client.call("echo@v1", {"message": "second"})
    assert result2["input_params"]["message"] == "second"

    # Third call to different verb
    result3 = client.call("calculate@v1", {"a": 5, "b": 3})
    assert result3["input_params"]["a"] == 5
    assert result3["input_params"]["b"] == 3


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
