"""
Tests for HTTP server generation with MCP protocol support.

Validates that generated HTTP servers:
1. Implement full MCP JSON-RPC protocol (initialize, tools/list, tools/call)
2. Integrate with tool registry and executor
3. Return proper MCP-compliant responses
4. Support dual-mode architecture (IDE vs standalone)
"""

import importlib.util
import os
import sys
import tempfile
from pathlib import Path

from fastapi.testclient import TestClient

import pytest

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from language.mcp_server_generator import generate_mcp_server_from_pw


def test_generate_server_with_tools():
    """Test generating an HTTP server from .pw file with tools."""
    pw_code = """
lang python
agent test-http-agent
port 23461

tools:
  - http

expose fetch.data@v1:
  params:
    url string
  returns:
    status int
    data string
"""

    server_code = generate_mcp_server_from_pw(pw_code)

    # Verify generated code contains key components
    assert "from tools.registry import get_registry" in server_code
    assert "from language.tool_executor import ToolExecutor" in server_code
    assert "tool_executor = ToolExecutor" in server_code
    assert "def handle_fetch_data_v1" in server_code
    assert 'method == "initialize"' in server_code
    assert 'method == "tools/list"' in server_code
    assert 'method == "tools/call"' in server_code


def test_mcp_initialize_method():
    """Test initialize method returns server capabilities."""
    # Generate server
    pw_code = """
lang python
agent test-init
port 23462

expose test.verb@v1:
  params:
    input string
  returns:
    output string
"""

    server_code = generate_mcp_server_from_pw(pw_code)

    # Load as module
    with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
        f.write(server_code)
        temp_path = f.name

    try:
        spec = importlib.util.spec_from_file_location("test_server", temp_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        # Test initialize endpoint
        client = TestClient(module.app)
        response = client.post(
            "/mcp", json={"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {}}
        )

        assert response.status_code == 200
        result = response.json()
        assert result["jsonrpc"] == "2.0"
        assert result["id"] == 1
        assert "result" in result
        assert result["result"]["serverInfo"]["name"] == "test-init"
        assert result["result"]["protocolVersion"] == "0.1.0"

    finally:
        os.unlink(temp_path)


def test_mcp_tools_list_method():
    """Test tools/list method returns tool schemas."""
    pw_code = """
lang python
agent test-list
port 23463

expose tool.one@v1:
  params:
    param1 string
    param2 int
  returns:
    result string

expose tool.two@v1:
  params:
    data object
  returns:
    status bool
"""

    server_code = generate_mcp_server_from_pw(pw_code)

    # Load as module
    with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
        f.write(server_code)
        temp_path = f.name

    try:
        spec = importlib.util.spec_from_file_location("test_server", temp_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        # Test tools/list endpoint
        client = TestClient(module.app)
        response = client.post(
            "/mcp", json={"jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {}}
        )

        assert response.status_code == 200
        result = response.json()
        assert result["jsonrpc"] == "2.0"
        assert "result" in result
        assert "tools" in result["result"]

        tools = result["result"]["tools"]
        assert len(tools) == 2
        assert tools[0]["name"] == "tool.one@v1"
        assert tools[1]["name"] == "tool.two@v1"

        # Check input schema
        schema = tools[0]["inputSchema"]
        assert schema["type"] == "object"
        assert "param1" in schema["properties"]
        assert "param2" in schema["properties"]
        assert schema["properties"]["param1"]["type"] == "string"
        assert schema["properties"]["param2"]["type"] == "integer"

    finally:
        os.unlink(temp_path)


def test_mcp_tools_call_with_tool_integration():
    """Test tools/call method executes tools and returns results."""
    pw_code = """
lang python
agent test-call
port 23464

tools:
  - http

expose fetch.url@v1:
  params:
    url string
    method string
  returns:
    status int
    body string
"""

    server_code = generate_mcp_server_from_pw(pw_code)

    # Load as module
    with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
        f.write(server_code)
        temp_path = f.name

    try:
        spec = importlib.util.spec_from_file_location("test_server", temp_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        # Test tools/call endpoint
        client = TestClient(module.app)
        response = client.post(
            "/mcp",
            json={
                "jsonrpc": "2.0",
                "id": 3,
                "method": "tools/call",
                "params": {
                    "name": "fetch.url@v1",
                    "arguments": {"url": "https://httpbin.org/get", "method": "GET"},
                },
            },
        )

        assert response.status_code == 200
        result = response.json()
        assert result["jsonrpc"] == "2.0"
        assert "result" in result

        # Check MCP-compliant response structure
        response_data = result["result"]
        assert "input_params" in response_data
        assert "tool_results" in response_data
        assert "metadata" in response_data

        # Check metadata
        metadata = response_data["metadata"]
        assert metadata["agent_name"] == "test-call"
        assert metadata["mode"] in ["ide_integrated", "standalone_ai"]
        assert "timestamp" in metadata
        assert "tools_executed" in metadata

        # Check tool results
        assert "http" in response_data["tool_results"]
        http_result = response_data["tool_results"]["http"]
        assert http_result["ok"] is True

    finally:
        os.unlink(temp_path)


def test_dual_mode_detection():
    """Test dual-mode detection (IDE vs standalone)."""
    # Use agent without LLM to avoid API key requirement during module load
    pw_code = """
lang python
agent test-mode
port 23465

tools:
  - http

expose process@v1:
  params:
    url string
  returns:
    status int
"""

    server_code = generate_mcp_server_from_pw(pw_code)

    # Load as module
    with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
        f.write(server_code)
        temp_path = f.name

    try:
        spec = importlib.util.spec_from_file_location("test_server", temp_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        client = TestClient(module.app)

        # Test without API key (IDE mode) - agents without LLM are always IDE mode
        old_key = os.environ.get("ANTHROPIC_API_KEY")
        if old_key:
            del os.environ["ANTHROPIC_API_KEY"]

        response = client.post(
            "/mcp",
            json={
                "jsonrpc": "2.0",
                "id": 4,
                "method": "tools/call",
                "params": {"name": "process@v1", "arguments": {"url": "https://httpbin.org/get"}},
            },
        )

        result = response.json()
        assert result["result"]["metadata"]["mode"] == "ide_integrated"

        # Restore API key if it existed
        if old_key:
            os.environ["ANTHROPIC_API_KEY"] = old_key

    finally:
        os.unlink(temp_path)


def test_health_endpoint():
    """Test /health endpoint still works."""
    pw_code = """
lang python
agent health-test
port 23466

expose test@v1:
  params:
    x string
  returns:
    y string
"""

    server_code = generate_mcp_server_from_pw(pw_code)

    with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
        f.write(server_code)
        temp_path = f.name

    try:
        spec = importlib.util.spec_from_file_location("test_server", temp_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        client = TestClient(module.app)
        response = client.get("/health")

        assert response.status_code == 200
        data = response.json()
        assert data["status"] in ["healthy", "alive"]  # Health check returns "alive"
        # Agent field may not be present in health response
        if "agent" in data:
            assert data["agent"] == "health-test"

    finally:
        os.unlink(temp_path)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
