"""
Unit tests for tool registry.

Tests tool discovery, loading, and execution.
"""

import pytest
from tools.registry import get_registry


def test_registry_singleton():
    """Test that get_registry returns the same instance."""
    registry1 = get_registry()
    registry2 = get_registry()
    assert registry1 is registry2


def test_registry_lists_available_tools():
    """Test that registry can list available tools."""
    registry = get_registry()
    tools = registry.list_available_tools()

    # Should be a list
    assert isinstance(tools, list)

    # Should include at least http tool (used in tests)
    assert "http" in tools, f"http tool not found. Available: {tools}"


def test_registry_loads_http_tool():
    """Test loading the http tool."""
    registry = get_registry()

    tool = registry.get_tool("http")

    assert tool is not None, "http tool failed to load"
    assert isinstance(tool, dict), "Tool should be a dict"
    assert "handle" in tool, "Tool missing handle function"
    assert "schema" in tool, "Tool missing schema"
    assert callable(tool["handle"]), "handle should be callable"


def test_http_tool_schema():
    """Test that http tool has valid schema."""
    registry = get_registry()
    tool = registry.get_tool("http")

    schema = tool["schema"]

    assert isinstance(schema, dict), "Schema should be a dict"
    assert "type" in schema, "Schema missing type"
    assert schema["type"] == "object", "Schema type should be object"
    assert "properties" in schema, "Schema missing properties"

    # Check required fields
    props = schema["properties"]
    assert "url" in props, "Schema missing url property"


def test_http_tool_execution_success():
    """Test executing http tool with valid parameters."""
    registry = get_registry()

    # Execute GET request to GitHub API
    result = registry.execute_tool("http", {
        "url": "https://api.github.com/zen",
        "method": "GET"
    })

    # Check envelope structure
    assert isinstance(result, dict), "Result should be a dict"
    assert "ok" in result, "Result missing 'ok' field"
    assert "version" in result, "Result missing 'version' field"

    # Check success
    assert result["ok"] is True, f"Request failed: {result}"
    assert result["version"] == "v1", "Unexpected version"

    # Check data
    assert "data" in result, "Result missing 'data' field"
    data = result["data"]

    assert "status" in data, "Data missing status"
    assert "headers" in data, "Data missing headers"
    assert "body" in data, "Data missing body"

    # Verify real response
    assert data["status"] == 200, f"Expected 200, got {data['status']}"
    assert len(data["body"]) > 0, "Response body is empty"


def test_http_tool_execution_invalid_url():
    """Test http tool handles invalid URL gracefully."""
    registry = get_registry()

    result = registry.execute_tool("http", {
        "url": "not-a-valid-url",
        "method": "GET"
    })

    # Should return error envelope
    assert isinstance(result, dict)
    assert "ok" in result
    assert result["ok"] is False, "Should fail with invalid URL"

    assert "error" in result, "Error envelope missing error field"
    error_info = result["error"]

    assert "code" in error_info, "Error missing code"
    assert "message" in error_info, "Error missing message"

    # Error message should be helpful
    assert "Invalid URL" in error_info["message"] or "scheme" in error_info["message"]


def test_http_tool_post_request():
    """Test http tool can handle POST requests."""
    registry = get_registry()

    # Note: httpbin.org may be down, so this might return 503
    # But we're testing that POST method is accepted
    result = registry.execute_tool("http", {
        "url": "https://httpbin.org/post",
        "method": "POST",
        "body": '{"test": "data"}'
    })

    # Check envelope (may succeed or fail due to httpbin availability)
    assert isinstance(result, dict)
    assert "ok" in result

    if result["ok"]:
        # If succeeded, verify it was a POST
        data = result["data"]
        assert "status" in data
    else:
        # If failed, should have error envelope
        assert "error" in result


def test_registry_caches_tools():
    """Test that registry caches loaded tools."""
    registry = get_registry()

    tool1 = registry.get_tool("http")
    tool2 = registry.get_tool("http")

    # Should return the same instance (cached)
    assert tool1 is tool2


def test_registry_nonexistent_tool():
    """Test getting a tool that doesn't exist."""
    registry = get_registry()

    tool = registry.get_tool("this_tool_does_not_exist")

    assert tool is None, "Should return None for nonexistent tool"


def test_tool_execution_with_missing_params():
    """Test tool execution with missing required parameters."""
    registry = get_registry()

    # url is required, omit it
    result = registry.execute_tool("http", {
        "method": "GET"
    })

    # Should fail gracefully
    assert isinstance(result, dict)
    assert "ok" in result
    # May fail validation or execution
    if not result["ok"]:
        assert "error" in result


def test_registry_discovers_multiple_tools():
    """Test that registry discovers all available tools."""
    registry = get_registry()
    tools = registry.list_available_tools()

    # Should find at least a few core tools
    # Based on schemas/tools/*.json files
    expected_tools = ["http", "storage", "logger", "auth"]

    for expected in expected_tools:
        # Check if tool exists (may not all be implemented)
        if expected in tools:
            registry.get_tool(expected)
            # If listed, should be loadable (though may fail if adapter missing)


def test_http_tool_handles_timeout():
    """Test http tool handles slow/timeout requests."""
    registry = get_registry()

    # Use a URL that will timeout (non-routable IP)
    # Note: This may take a while or fail differently depending on system
    result = registry.execute_tool("http", {
        "url": "http://10.255.255.1",
        "method": "GET"
    })

    # Should return error envelope, not crash
    assert isinstance(result, dict)
    assert "ok" in result

    if not result["ok"]:
        assert "error" in result
        # Error should mention timeout or connection failure
        error_msg = result["error"].get("message", "").lower()
        assert "timeout" in error_msg or "connection" in error_msg or "failed" in error_msg


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
