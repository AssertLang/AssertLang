"""
Minimal test for standalone AI mode.

COST WARNING: This test makes real API calls to Anthropic.
- Estimated cost per test: ~$0.01-0.02 (depends on response length)
- Uses Claude Sonnet model as specified in agent configs
- To run: ANTHROPIC_API_KEY=your-key python3 tests/test_standalone_mode.py

This test is intentionally minimal to avoid burning through API credits.
"""

import json
import os
import subprocess
from pathlib import Path


def test_standalone_mode_single_call():
    """
    Single economical test of standalone AI mode.

    COST: ~$0.01 per run (estimated)
    - Input: ~100 tokens (agent prompt + tool results)
    - Output: ~50-100 tokens (AI summary)
    - Model: Claude Sonnet (~$3/1M input, ~$15/1M output)
    """
    api_key = os.environ.get("ANTHROPIC_API_KEY")

    # Try loading from .env.local if not in environment
    if not api_key:
        env_file = Path(__file__).parent.parent / ".env.local"
        if env_file.exists():
            for line in env_file.read_text().splitlines():
                if line.startswith("ANTHROPIC_API_KEY="):
                    api_key = line.split("=", 1)[1].strip()
                    break

    if not api_key:
        print("⚠️  ANTHROPIC_API_KEY not set - skipping test")
        print("   To test: export ANTHROPIC_API_KEY=your-key")
        print("   Or add to .env.local file")
        return

    print("🔑 API key found - running ONE test call...")
    print("   Estimated cost: $0.01-0.02")

    # Use code-reviewer agent which has AI prompts configured
    # Minimal code to review to keep token usage low
    agent_path = "examples/devops_suite/code_reviewer_agent.pw"

    requests = [
        {"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {}},
        {
            "jsonrpc": "2.0",
            "id": 2,
            "method": "tools/call",
            "params": {
                "name": "review.analyze@v1",
                "arguments": {
                    "code": "def add(a, b): return a + b",
                    "language": "python",
                    "context": "test",
                },
            },
        },
    ]

    input_data = "\n".join(json.dumps(req) for req in requests) + "\n"

    # Set API key in environment
    env = os.environ.copy()
    env["ANTHROPIC_API_KEY"] = api_key
    env["PYTHONPATH"] = str(Path(__file__).parent.parent)

    result = subprocess.run(
        ["python3", "language/mcp_stdio_server.py", agent_path],
        input=input_data,
        capture_output=True,
        text=True,
        cwd=Path(__file__).parent.parent,
        timeout=30,
        env=env,
    )

    if result.returncode != 0:
        print(f"❌ Test failed: {result.stderr}")
        return

    # Parse response
    responses = [json.loads(line) for line in result.stdout.strip().split("\n") if line]

    if len(responses) < 2:
        print(f"❌ Expected 2 responses, got {len(responses)}")
        return

    call_resp = responses[1]

    if "error" in call_resp:
        print(f"❌ Tool call failed: {call_resp['error']}")
        return

    # Extract result
    result_data = call_resp["result"]

    # Parse MCP content wrapper
    if "content" in result_data and len(result_data["content"]) > 0:
        content_item = result_data["content"][0]
        if content_item.get("type") == "text":
            result_data = json.loads(content_item["text"])

    # Check for standalone mode indicators
    metadata = result_data.get("metadata", {})
    mode = metadata.get("mode")

    print("\n" + "=" * 60)
    print("Test Results:")
    print("=" * 60)
    print(f"Mode: {mode}")
    print(f"Agent: {metadata.get('agent_name')}")
    print(f"Tools executed: {metadata.get('tools_executed', [])}")

    if mode == "standalone_ai":
        print("✅ STANDALONE MODE ACTIVE")
        print(f"   LLM Model: {metadata.get('llm_model', 'unknown')}")
        print("   AI processed tool results")

        # Check if response has AI analysis
        if "summary" in result_data:
            summary = result_data["summary"]
            print(f"\n   AI Summary: {summary[:100]}...")

        print("\n🎉 Test PASSED - Standalone AI mode working!")
        print("   Cost: ~$0.01-0.02 for this test")

    elif mode == "ide_integrated":
        print("⚠️  IDE MODE (not standalone)")
        print("   This means ANTHROPIC_API_KEY was not detected by the agent")
        print("   Check that .env.local is loaded or export the key directly")

    else:
        print(f"❌ Unknown mode: {mode}")

    print("=" * 60)


if __name__ == "__main__":
    print("=" * 60)
    print("Standalone AI Mode Test - ECONOMICAL")
    print("=" * 60)
    print("\n⚠️  WARNING: This makes ONE real API call to Anthropic")
    print("   Estimated cost: $0.01-0.02 per run")
    print("   Press Ctrl+C within 5 seconds to cancel...")
    print()

    import time

    try:
        for i in range(5, 0, -1):
            print(f"   Starting in {i}...")
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n\n❌ Cancelled by user")
        exit(0)

    print("\n🚀 Running test...\n")
    test_standalone_mode_single_call()
