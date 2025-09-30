"""
Unit tests for tool executor.

Tests tool loading, parameter mapping, and execution orchestration.
"""
import pytest
from language.tool_executor import ToolExecutor


def test_tool_executor_no_tools():
    """Test executor with agent that has no tools."""
    class MockAgent:
        tools = None

    executor = ToolExecutor(None)

    assert not executor.has_tools()
    assert executor.execute_tools({}) == {}


def test_tool_executor_empty_tools_list():
    """Test executor with empty tools list."""
    executor = ToolExecutor([])

    assert not executor.has_tools()
    assert executor.execute_tools({}) == {}


def test_tool_executor_loads_http_tool():
    """Test that executor loads http tool."""
    executor = ToolExecutor(["http"])

    assert executor.has_tools()
    assert "http" in executor.loaded_tools


def test_tool_executor_skips_nonexistent_tool():
    """Test that executor gracefully skips tools that don't exist."""
    executor = ToolExecutor(["http", "this_tool_does_not_exist", "also_fake"])

    # Should load http but skip the fake ones
    assert executor.has_tools()
    assert "http" in executor.loaded_tools
    assert "this_tool_does_not_exist" not in executor.loaded_tools
    assert "also_fake" not in executor.loaded_tools


def test_tool_executor_executes_http_tool():
    """Test executing http tool via executor."""
    executor = ToolExecutor(["http"])

    results = executor.execute_tools({
        "url": "https://api.github.com/zen",
        "method": "GET"
    })

    # Should have http result
    assert "http" in results
    http_result = results["http"]

    # Check envelope
    assert "ok" in http_result
    assert "version" in http_result

    # Should succeed
    assert http_result["ok"] is True

    # Check data
    assert "data" in http_result
    data = http_result["data"]

    assert "status" in data
    assert "body" in data
    assert data["status"] == 200


def test_tool_executor_handles_tool_failure():
    """Test that executor handles tool execution failures gracefully."""
    executor = ToolExecutor(["http"])

    # Invalid URL should cause failure
    results = executor.execute_tools({
        "url": "not-a-valid-url",
        "method": "GET"
    })

    assert "http" in results
    http_result = results["http"]

    # Should have error envelope
    assert "ok" in http_result
    assert http_result["ok"] is False
    assert "error" in http_result


def test_tool_executor_passes_all_params_to_tools():
    """Test that executor passes all verb parameters to tools."""
    executor = ToolExecutor(["http"])

    # Pass extra parameters - tool should ignore what it doesn't need
    results = executor.execute_tools({
        "url": "https://api.github.com/zen",
        "method": "GET",
        "extra_param": "ignored",
        "another_param": 123
    })

    # Should still work
    assert "http" in results
    assert results["http"]["ok"] is True


def test_tool_executor_multiple_tools():
    """Test executor with multiple tools (if available)."""
    # Try to load multiple tools
    executor = ToolExecutor(["http", "storage", "logger"])

    # At least http should load
    assert executor.has_tools()
    assert "http" in executor.loaded_tools

    # Execute with params for http
    results = executor.execute_tools({
        "url": "https://api.github.com/zen",
        "method": "GET"
    })

    # http should execute
    assert "http" in results

    # Other tools may or may not execute depending on their param requirements


def test_tool_executor_caches_loaded_tools():
    """Test that executor caches loaded tools."""
    executor = ToolExecutor(["http"])

    # Load once
    assert "http" in executor.loaded_tools
    tool1 = executor.loaded_tools["http"]

    # Execute (shouldn't reload)
    executor.execute_tools({"url": "https://api.github.com/zen", "method": "GET"})

    # Should still be same tool instance
    tool2 = executor.loaded_tools["http"]
    assert tool1 is tool2


def test_tool_executor_empty_params():
    """Test executor with empty parameters."""
    executor = ToolExecutor(["http"])

    # Empty params should cause http to fail (url required)
    results = executor.execute_tools({})

    assert "http" in results
    # Should fail due to missing required params
    assert results["http"]["ok"] is False


def test_tool_executor_integration_with_agent():
    """Test tool executor with a mock agent definition."""
    class MockAgent:
        def __init__(self):
            self.tools = ["http"]
            self.name = "test-agent"

    agent = MockAgent()
    executor = ToolExecutor(agent.tools)

    # Should load tools from agent
    assert executor.has_tools()

    # Execute
    results = executor.execute_tools({
        "url": "https://api.github.com/zen",
        "method": "GET"
    })

    # Should work
    assert "http" in results
    assert results["http"]["ok"] is True


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
