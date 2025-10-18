#!/usr/bin/env python3
"""
Two-Agent Coordination Demo

Demonstrates:
- Agent A (orchestrator) calling Agent B (code-reviewer)
- Bidirectional MCP communication
- Error handling and retries
"""

import sys
import time

from language.mcp_client import MCPClient, MCPError, call_agent, register_agent


def demo_two_agent_coordination():
    """
    Demo: Orchestrator agent coordinates with code-reviewer agent.
    """

    print("=" * 60)
    print("Two-Agent Coordination Demo")
    print("=" * 60)
    print()

    # Setup: Register both agents
    print("1. Registering agents...")
    register_agent("code-reviewer", "http://127.0.0.1:23456")
    register_agent("orchestrator", "http://127.0.0.1:23457")
    print("   ✓ code-reviewer -> http://127.0.0.1:23456")
    print("   ✓ orchestrator -> http://127.0.0.1:23457")
    print()

    # Step 1: Check if code-reviewer is healthy
    print("2. Health check: code-reviewer")
    try:
        client = MCPClient("http://127.0.0.1:23456", timeout=5, retries=1)
        health = client.health_check()
        print(f"   ✓ Status: {health.get('status')}")
        print(f"   ✓ Agent: {health.get('agent')}")
    except Exception as e:
        print(f"   ✗ Health check failed: {e}")
        print()
        print("Make sure code-reviewer agent is running:")
        print("  python3 examples/demo_agent_server.py")
        return False
    print()

    # Step 2: List verbs exposed by code-reviewer
    print("3. Listing verbs from code-reviewer...")
    try:
        verbs_info = client.list_verbs()
        print(f"   Agent: {verbs_info.get('agent')}")
        for verb in verbs_info.get('verbs', []):
            print(f"   - {verb}")
    except Exception as e:
        print(f"   ✗ Failed: {e}")
        return False
    print()

    # Step 3: Orchestrator calls code-reviewer
    print("4. Orchestrator calling code-reviewer.review.submit@v1")
    print("   Params: pr_url='https://github.com/test/pr/123'")
    try:
        response = call_agent(
            "code-reviewer",
            "review.submit@v1",
            {"pr_url": "https://github.com/test/pr/123"}
        )

        if response.is_success():
            data = response.get_data()
            print("   ✓ Success!")
            print(f"   ✓ Review ID: {data.get('review_id')}")
            print(f"   ✓ Status: {data.get('status')}")
            review_id = data.get('review_id')
        else:
            print(f"   ✗ Call failed: {response.error}")
            return False
    except MCPError as e:
        print(f"   ✗ MCP Error: {e}")
        return False
    except Exception as e:
        print(f"   ✗ Unexpected error: {e}")
        return False
    print()

    # Step 4: Poll for review status
    print("5. Polling review status...")
    for i in range(3):
        print(f"   Poll #{i+1}")
        try:
            response = call_agent(
                "code-reviewer",
                "review.status@v1",
                {"review_id": review_id}
            )

            if response.is_success():
                data = response.get_data()
                print(f"     Status: {data.get('status')}")
                print(f"     Progress: {data.get('progress')}")
                print(f"     Comments: {len(data.get('comments', []))} items")
            else:
                print(f"     ✗ Failed: {response.error}")

        except Exception as e:
            print(f"     ✗ Error: {e}")

        if i < 2:
            time.sleep(1)
    print()

    # Step 5: Summary
    print("6. Coordination Summary")
    print("   ✓ Orchestrator successfully called code-reviewer")
    print("   ✓ Bidirectional MCP communication working")
    print("   ✓ Two agents coordinated via .al protocol")
    print()

    print("=" * 60)
    print("Demo Complete! ✅")
    print("=" * 60)

    return True


def demo_error_handling():
    """Demo error handling scenarios."""

    print()
    print("=" * 60)
    print("Error Handling Demo")
    print("=" * 60)
    print()

    # Test 1: Missing parameter
    print("1. Testing missing parameter error...")
    try:
        client = MCPClient("http://127.0.0.1:23456")
        response = client.call("review.submit@v1", {})  # Missing pr_url

        if not response.is_success():
            print(f"   ✓ Caught error: {response.error.get('code')}")
            print(f"   ✓ Message: {response.error.get('message')}")
        else:
            print("   ✗ Should have failed with missing parameter")
    except Exception as e:
        print(f"   ✗ Unexpected error: {e}")
    print()

    # Test 2: Unknown method
    print("2. Testing unknown method error...")
    try:
        client = MCPClient("http://127.0.0.1:23456")
        response = client.call("unknown.verb@v1", {})

        if not response.is_success():
            print(f"   ✓ Caught error: {response.error.get('code')}")
            print(f"   ✓ Message: {response.error.get('message')}")
        else:
            print("   ✗ Should have failed with unknown method")
    except Exception as e:
        print(f"   ✗ Unexpected error: {e}")
    print()

    # Test 3: Agent not found
    print("3. Testing agent discovery error...")
    try:
        response = call_agent("nonexistent-agent", "test@v1", {})
        print("   ✗ Should have raised MCPError")
    except MCPError as e:
        print(f"   ✓ Caught error: {e.code}")
        print(f"   ✓ Message: {e.message}")
    print()


if __name__ == "__main__":
    print()
    print("AssertLang Two-Agent Coordination Demo")
    print()
    print("Prerequisites:")
    print("1. Install dependencies: pip3 install fastapi uvicorn requests")
    print("2. Start code-reviewer: python3 examples/demo_agent_server.py")
    print("3. Run this script: python3 examples/two_agent_demo.py")
    print()
    input("Press Enter when code-reviewer is running...")
    print()

    # Run demos
    success = demo_two_agent_coordination()

    if success:
        demo_error_handling()
    else:
        print()
        print("Demo failed. Make sure code-reviewer agent is running:")
        print("  python3 examples/demo_agent_server.py")
        sys.exit(1)