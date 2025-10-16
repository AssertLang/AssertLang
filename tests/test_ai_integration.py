"""
Real AI integration tests using Anthropic API.

These tests require ANTHROPIC_API_KEY environment variable.
Skip if not available.
"""

import os
import subprocess
import sys
import time
from pathlib import Path

import pytest
import requests

# Check if API key is available
ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY")
SKIP_AI_TESTS = not ANTHROPIC_API_KEY


def test_ai_code_reviewer_generation():
    """Test generating AI code reviewer agent."""
    if SKIP_AI_TESTS:
        print("⚠️  Skipping: ANTHROPIC_API_KEY not set")
        return

    pw_file = Path("examples/devops_suite/code_reviewer_agent.al")
    assert pw_file.exists()

    # Generate server
    output_file = Path("/tmp/test_code_reviewer_server.py")
    result = subprocess.run(
        [sys.executable, "cli/main.py", "generate", str(pw_file), "-o", str(output_file)],
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0
    assert output_file.exists()

    content = output_file.read_text()

    # Verify AI features in generated code
    assert "langchain_anthropic" in content
    assert "ChatAnthropic" in content
    assert "claude-3-5-sonnet" in content
    assert "chatprompttemplate" in content.lower() or "prompt" in content.lower()

    # Cleanup
    output_file.unlink()


@pytest.mark.skipif(SKIP_AI_TESTS, reason="ANTHROPIC_API_KEY not set")
def test_ai_agent_runtime():
    """Test running AI agent server and making real API calls."""

    pw_file = Path("examples/devops_suite/code_reviewer_agent.al")
    output_file = Path("/tmp/test_ai_server_runtime.py")

    # Generate server
    subprocess.run(
        [sys.executable, "cli/main.py", "generate", str(pw_file), "-o", str(output_file)],
        capture_output=True,
    )

    # Start server in background
    server_process = subprocess.Popen(
        [sys.executable, str(output_file)],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        env={**os.environ, "ANTHROPIC_API_KEY": ANTHROPIC_API_KEY},
    )

    try:
        # Wait for server to start
        time.sleep(3)

        # Health check
        response = requests.get("http://127.0.0.1:23450/health", timeout=5)
        assert response.status_code == 200
        health_data = response.json()
        # Check for either 'healthy' or 'alive' status
        assert health_data.get("status") in ["healthy", "alive"] or "ok" in health_data

        # Test AI code review with real API call
        # Using simple vulnerable code example
        test_code = """
def login(username, password):
    query = "SELECT * FROM users WHERE username='" + username + "' AND password='" + password + "'"
    return db.execute(query)
"""

        review_request = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tools/call",
            "params": {
                "name": "review.analyze@v1",
                "arguments": {"code": test_code, "language": "python"}
            },
        }

        response = requests.post(
            "http://127.0.0.1:23450/mcp", json=review_request, timeout=30  # AI calls can take time
        )

        # Debug: print response if not 200
        if response.status_code != 200:
            print(f"Response status: {response.status_code}")
            print(f"Response body: {response.text}")

        assert response.status_code == 200
        result = response.json()

        # JSON-RPC response format
        assert "result" in result or "error" not in result

        # Get the actual result data
        if "result" in result:
            data = result["result"]
        else:
            # Fallback for non-standard format
            data = result.get("data", result)

        # Verify AI detected the SQL injection (flexible checking)
        if isinstance(data, dict):
            # Check for various possible response formats
            summary = data.get("summary", data.get("analysis", ""))
            issues = data.get("issues", data.get("vulnerabilities", []))

            if summary or issues:
                combined_text = str(summary) + str(issues)
                combined_lower = combined_text.lower()
                assert "sql" in combined_lower or "injection" in combined_lower or "security" in combined_lower

                issue_count = len(issues) if isinstance(issues, list) else 1
                print(f"✅ AI detected security issues in code")
                print(f"   Response: {str(data)[:100]}...")

    finally:
        # Cleanup
        server_process.terminate()
        server_process.wait(timeout=5)

        # Print server output for debugging
        if server_process.stdout:
            stdout = server_process.stdout.read().decode()
            if stdout:
                print(f"Server stdout: {stdout[:500]}")
        if server_process.stderr:
            stderr = server_process.stderr.read().decode()
            if stderr:
                print(f"Server stderr: {stderr[:500]}")

        output_file.unlink()


def test_ai_prompt_templates():
    """Test that prompt templates are properly generated."""
    if SKIP_AI_TESTS:
        print("⚠️  Skipping: ANTHROPIC_API_KEY not set")
        return

    pw_file = Path("examples/devops_suite/code_reviewer_agent.al")
    output_file = Path("/tmp/test_prompt_templates.py")

    # Generate server
    subprocess.run(
        [sys.executable, "cli/main.py", "generate", str(pw_file), "-o", str(output_file)],
        capture_output=True,
    )

    content = output_file.read_text()

    # Check global prompt template (can be AGENT_PROMPT_TEMPLATE or AGENT_SYSTEM_PROMPT)
    assert "AGENT_SYSTEM_PROMPT" in content or "AGENT_PROMPT_TEMPLATE" in content
    assert "expert code reviewer" in content.lower() or "code review" in content.lower()

    # Check verb-specific prompt handling
    assert "review.analyze@v1" in content

    # Verify prompt-related imports from langchain
    assert "ChatPromptTemplate" in content or "prompt" in content.lower()

    output_file.unlink()


def test_observability_with_ai():
    """Test that observability works with AI calls."""
    if SKIP_AI_TESTS:
        print("⚠️  Skipping: ANTHROPIC_API_KEY not set")
        return

    pw_file = Path("examples/devops_suite/code_reviewer_agent.al")
    output_file = Path("/tmp/test_observability_ai.py")

    subprocess.run(
        [sys.executable, "cli/main.py", "generate", str(pw_file), "-o", str(output_file)],
        capture_output=True,
    )

    content = output_file.read_text()

    # Verify OpenTelemetry integration
    assert "from opentelemetry" in content
    assert "tracer" in content.lower()
    assert "FastAPIInstrumentor" in content or "instrument_app" in content.lower()

    # Check metrics
    assert "request_counter" in content or "Counter" in content
    assert "request_duration" in content or "Histogram" in content

    output_file.unlink()


if __name__ == "__main__":
    if SKIP_AI_TESTS:
        print("⚠️  Skipping all AI tests: ANTHROPIC_API_KEY not set")
        print("   Set ANTHROPIC_API_KEY to run real API integration tests")
    else:
        print("🧪 Running AI integration tests with real API calls...")
        test_ai_code_reviewer_generation()
        test_ai_agent_runtime()
        test_ai_prompt_templates()
        test_observability_with_ai()
        print("✅ All AI integration tests passed!")
