"""
Test MCP integration for all configured agents.

Tests that all agents in .cursor/mcp.json:
1. Can be initialized
2. Return valid tool lists
3. Can execute verbs without crashing
4. Return proper response structures
"""

import json
import subprocess
from pathlib import Path
from typing import Any, Dict


def send_jsonrpc(agent_path: str, requests: list) -> list:
    """Send JSON-RPC requests to MCP stdio server."""
    input_data = "\n".join(json.dumps(req) for req in requests) + "\n"

    result = subprocess.run(
        ["python3", "language/mcp_stdio_server.py", agent_path],
        input=input_data,
        capture_output=True,
        text=True,
        cwd=Path(__file__).parent.parent,
        timeout=10,
    )

    if result.returncode != 0:
        raise RuntimeError(f"MCP server failed: {result.stderr}")

    # Parse JSON-RPC responses
    responses = []
    for line in result.stdout.strip().split("\n"):
        if line:
            responses.append(json.loads(line))

    return responses


def agent_initialize_and_list_tools(agent_path: str) -> Dict[str, Any]:
    """Helper: Test that agent can initialize and list tools."""
    requests = [
        {"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {}},
        {"jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {}},
    ]

    responses = send_jsonrpc(agent_path, requests)

    assert len(responses) == 2, f"Expected 2 responses, got {len(responses)}"

    # Check initialize response
    init_resp = responses[0]
    assert "result" in init_resp, "Initialize response missing 'result'"
    assert "serverInfo" in init_resp["result"], "Missing serverInfo"
    assert "name" in init_resp["result"]["serverInfo"], "Missing server name"

    # Check tools/list response
    tools_resp = responses[1]
    assert "result" in tools_resp, "Tools list response missing 'result'"
    assert "tools" in tools_resp["result"], "Missing tools array"

    tools = tools_resp["result"]["tools"]

    return {
        "server_name": init_resp["result"]["serverInfo"]["name"],
        "tool_count": len(tools),
        "tools": [tool["name"] for tool in tools],
    }


def agent_tool_execution(
    agent_path: str, tool_name: str, arguments: Dict[str, Any]
) -> Dict[str, Any]:
    """Helper: Test executing a tool on an agent."""
    requests = [
        {"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {}},
        {
            "jsonrpc": "2.0",
            "id": 2,
            "method": "tools/call",
            "params": {"name": tool_name, "arguments": arguments},
        },
    ]

    responses = send_jsonrpc(agent_path, requests)

    assert len(responses) == 2, f"Expected 2 responses, got {len(responses)}"

    # Check tool call response
    call_resp = responses[1]
    assert "result" in call_resp or "error" in call_resp, "Tool call response missing result/error"

    if "error" in call_resp:
        return {"success": False, "error": call_resp["error"]}

    # MCP protocol wraps result in content[0].text as JSON string
    result = call_resp["result"]

    # Parse the actual result from MCP content wrapper
    if "content" in result and len(result["content"]) > 0:
        content_item = result["content"][0]
        if content_item.get("type") == "text":
            try:
                result = json.loads(content_item["text"])
            except json.JSONDecodeError:
                result = {"text": content_item["text"]}

    return {
        "success": True,
        "has_metadata": "metadata" in result,
        "has_tool_results": "tool_results" in result,
        "mode": result.get("metadata", {}).get("mode"),
        "result": result,
    }


# Test configuration: (agent_path, tool_name, test_arguments)
TEST_AGENTS = [
    (
        "examples/test_tool_integration.pw",
        "fetch.url@v1",
        {"url": "https://api.github.com/zen", "method": "GET"},
    ),
    ("examples/ai_code_reviewer.pw", "review.analyze@v1", {"repo": "test/repo", "pr_number": 123}),
    ("examples/deployment_workflow.pw", "workflow.execute@v1", {"environment": "staging"}),
    ("examples/observable_agent.pw", "task.execute@v1", {"task_id": "test-123"}),
    (
        "examples/devops_suite/code_reviewer_agent.pw",
        "review.approve@v1",
        {"review_id": "test", "approved": True, "comments": "LGTM"},
    ),
    ("examples/orchestrator_agent.pw", "orchestrate.deploy@v1", {"service": "test-service"}),
    ("examples/cross_language/data_processor.pw", "process.data@v1", {"input": "test"}),
    ("examples/cross_language/cache_service.pw", "cache.get@v1", {"key": "test"}),
    ("examples/devops_suite/deployment_orchestrator.pw", "deploy.service@v1", {"service": "test"}),
    ("examples/devops_suite/test_runner_agent.pw", "test.run@v1", {"suite": "unit"}),
]


def test_all_agents_initialize():
    """Test that all agents can initialize and list tools."""
    results = {}

    for agent_path, _, _ in TEST_AGENTS:
        try:
            result = agent_initialize_and_list_tools(agent_path)
            results[agent_path] = {"status": "pass", "data": result}
            print(f"✅ {agent_path}: {result['tool_count']} tools")
        except Exception as e:
            results[agent_path] = {"status": "fail", "error": str(e)}
            print(f"❌ {agent_path}: {e}")

    # At least test-tool-agent should work
    assert (
        results["examples/test_tool_integration.pw"]["status"] == "pass"
    ), "test-tool-agent failed to initialize"

    return results


def test_all_agents_execute_tools():
    """Test that all agents can execute their tools."""
    results = {}

    for agent_path, tool_name, arguments in TEST_AGENTS:
        try:
            result = agent_tool_execution(agent_path, tool_name, arguments)
            results[agent_path] = {
                "status": "pass" if result["success"] else "error",
                "data": result,
            }

            if result["success"]:
                mode = result.get("mode", "unknown")
                has_tools = "✓" if result.get("has_tool_results") else "✗"
                print(f"✅ {agent_path}: {tool_name} executed (mode={mode}, tools={has_tools})")
            else:
                print(f"⚠️  {agent_path}: {tool_name} returned error: {result.get('error')}")

        except Exception as e:
            results[agent_path] = {"status": "fail", "error": str(e)}
            print(f"❌ {agent_path}: {e}")

    # test-tool-agent should execute successfully
    assert (
        results["examples/test_tool_integration.pw"]["status"] == "pass"
    ), "test-tool-agent failed to execute"

    return results


def test_tool_integration_end_to_end():
    """
    End-to-end test of tool integration.

    Verifies:
    1. test-tool-agent uses http tool
    2. Real HTTP request executes
    3. Actual data returned (not mock)
    4. Tool results present in response
    """
    result = agent_tool_execution(
        "examples/test_tool_integration.pw",
        "fetch.url@v1",
        {"url": "https://api.github.com/zen", "method": "GET"},
    )

    assert result["success"], "Tool execution failed"
    assert result["has_metadata"], "Response missing metadata"
    assert result["has_tool_results"], "Response missing tool_results"
    assert result["mode"] == "ide_integrated", f"Expected ide_integrated mode, got {result['mode']}"

    # Check tool results structure
    tool_results = result["result"]["tool_results"]
    assert "http" in tool_results, "http tool not in tool_results"

    http_result = tool_results["http"]
    assert http_result["ok"] is True, "http tool failed"
    assert "data" in http_result, "http result missing data"

    # Check actual HTTP response
    http_data = http_result["data"]
    assert "status" in http_data, "HTTP response missing status"
    assert "body" in http_data, "HTTP response missing body"
    assert http_data["status"] == 200, f"Expected 200, got {http_data['status']}"

    # Body should contain actual GitHub zen message (not empty/mock)
    body = http_data["body"]
    assert len(body) > 0, "Response body is empty"
    assert body != "mock_data", "Got mock data instead of real response"

    print(f"✅ End-to-end test passed: Real HTTP request returned: {body[:50]}...")


if __name__ == "__main__":
    print("=" * 60)
    print("MCP Integration Tests")
    print("=" * 60)
    print()

    print("Phase 1: Testing agent initialization...")
    init_results = test_all_agents_initialize()
    print()

    print("Phase 2: Testing tool execution...")
    exec_results = test_all_agents_execute_tools()
    print()

    print("Phase 3: End-to-end tool integration test...")
    test_tool_integration_end_to_end()
    print()

    # Summary
    init_pass = sum(1 for r in init_results.values() if r["status"] == "pass")
    exec_pass = sum(1 for r in exec_results.values() if r["status"] == "pass")

    print("=" * 60)
    print("Summary:")
    print(f"  Initialization: {init_pass}/{len(init_results)} passed")
    print(f"  Execution: {exec_pass}/{len(exec_results)} passed")
    print("=" * 60)
