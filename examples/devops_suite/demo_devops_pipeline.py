#!/usr/bin/env python3
"""
End-to-end DevOps Pipeline Demo

Demonstrates all Promptware features:
- AI-powered code review (LangChain + Claude)
- Observability (OpenTelemetry traces + metrics)
- Multi-agent communication (MCP)
- Workflow orchestration (Temporal)

Architecture:
  1. Code Reviewer Agent (port 23450) - AI code analysis
  2. Test Runner Agent (port 23451) - Test execution
  3. Deployment Orchestrator (port 23452) - Temporal workflow coordination
"""

import asyncio
import sys
import requests
sys.path.insert(0, '../..')

from language.mcp_client import MCPClient


async def demo_code_review():
    """Demo: AI-powered code review."""
    print("\n" + "="*60)
    print("DEMO 1: AI Code Review with LangChain + Claude")
    print("="*60)

    client = MCPClient("http://127.0.0.1:23450")

    # Sample code to review
    sample_code = """
def login(username, password):
    query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
    result = db.execute(query)
    return result
"""

    print(f"\n📝 Submitting code for review...")
    print(f"Code:\n{sample_code}")

    try:
        response = client.call(
            "review.analyze@v1",
            {
                "code": sample_code,
                "language": "python",
                "context": "User authentication function"
            }
        )

        if response.is_success():
            data = response.get_data()
            print(f"\n✅ Review completed!")
            print(f"Summary: {data.get('summary', 'N/A')}")
            print(f"Issues: {data.get('issues', [])}")
            print(f"Severity: {data.get('severity', 'N/A')}")
        else:
            print(f"\n❌ Review failed: {response.error}")

    except Exception as e:
        print(f"\n⚠️  Code reviewer agent not running: {e}")
        print("   Start with: python3 code_reviewer_agent_server.py")


async def demo_test_execution():
    """Demo: Test execution with observability."""
    print("\n" + "="*60)
    print("DEMO 2: Test Execution with OpenTelemetry")
    print("="*60)

    client = MCPClient("http://127.0.0.1:23451")

    print(f"\n🧪 Running test suite...")

    try:
        response = client.call(
            "test.run@v1",
            {
                "project_path": "/path/to/project",
                "test_suite": "unit",
                "environment": "ci"
            }
        )

        if response.is_success():
            data = response.get_data()
            print(f"\n✅ Tests started!")
            print(f"Test ID: {data.get('test_id', 'N/A')}")
            print(f"Status: {data.get('status', 'N/A')}")
            print(f"Total: {data.get('total_tests', 0)}")
            print(f"Passed: {data.get('passed', 0)}")
            print(f"Failed: {data.get('failed', 0)}")
        else:
            print(f"\n❌ Test execution failed: {response.error}")

    except Exception as e:
        print(f"\n⚠️  Test runner agent not running: {e}")
        print("   Start with: python3 test_runner_agent_server.py")


async def demo_deployment_workflow():
    """Demo: Temporal workflow with multi-step deployment."""
    print("\n" + "="*60)
    print("DEMO 3: CI/CD Pipeline with Temporal Workflows")
    print("="*60)

    client = MCPClient("http://127.0.0.1:23452")

    print(f"\n🚀 Starting CI/CD pipeline...")
    print("   Steps: Review → Test → Build → Stage → Smoke Test → Prod (approval) → Verify")

    try:
        response = client.call(
            "workflow.execute@v1",
            {
                "workflow_id": "deploy-2025-001",
                "params": {
                    "service": "api-gateway",
                    "version": "v2.1.0",
                    "branch": "main",
                    "commit_sha": "abc123def"
                }
            }
        )

        if response.is_success():
            data = response.get_data()
            print(f"\n✅ Pipeline started!")
            print(f"Execution ID: {data.get('execution_id', 'N/A')}")
            print(f"Status: {data.get('status', 'N/A')}")
            print(f"\nWorkflow includes:")
            print(f"  - Code review analysis")
            print(f"  - Automated testing")
            print(f"  - Staging deployment")
            print(f"  - Production approval gate")
            print(f"  - Rollback on failure")
        else:
            print(f"\n❌ Pipeline failed: {response.error}")

    except Exception as e:
        print(f"\n⚠️  Deployment orchestrator not running: {e}")
        print("   Start with: python3 deployment_orchestrator_server.py")
        print("   Note: Requires Temporal server on localhost:7233")


async def demo_agent_communication():
    """Demo: Multi-agent coordination."""
    print("\n" + "="*60)
    print("DEMO 4: Multi-Agent Communication (MCP)")
    print("="*60)

    print(f"\n🔗 Demonstrating agent-to-agent communication...")
    print(f"   Architecture: Orchestrator → Code Reviewer → Test Runner")

    print(f"\n📡 Checking agents:")
    for name, url in [
        ("code-reviewer", "http://127.0.0.1:23450"),
        ("test-runner", "http://127.0.0.1:23451"),
        ("deployment-orchestrator", "http://127.0.0.1:23452")
    ]:
        try:
            client = MCPClient(url, timeout=2)
            response = requests.get(f"{url}/health", timeout=2)
            if response.status_code == 200:
                print(f"   ✅ {name}: {url}")
            else:
                print(f"   ❌ {name}: {url} (not healthy)")
        except:
            print(f"   ❌ {name}: {url} (not running)")


async def main():
    """Run all demos."""
    print("\n" + "="*70)
    print(" " * 10 + "PROMPTWARE DEVOPS SUITE DEMO")
    print(" " * 5 + "AI + Observability + Workflows + Agent Communication")
    print("="*70)

    print("\nThis demo showcases:")
    print("  ✨ AI-powered code review (LangChain + Claude 3.5 Sonnet)")
    print("  📊 Distributed tracing & metrics (OpenTelemetry)")
    print("  🔄 Durable workflows (Temporal)")
    print("  🤖 Agent-to-agent communication (MCP)")

    # Run demos
    await demo_code_review()
    await asyncio.sleep(1)

    await demo_test_execution()
    await asyncio.sleep(1)

    await demo_deployment_workflow()
    await asyncio.sleep(1)

    await demo_agent_communication()

    print("\n" + "="*70)
    print(" " * 20 + "DEMO COMPLETE")
    print("="*70)

    print("\n📚 To start the agents:")
    print("   Terminal 1: python3 code_reviewer_agent_server.py")
    print("   Terminal 2: python3 test_runner_agent_server.py")
    print("   Terminal 3: python3 deployment_orchestrator_server.py")
    print("\n   Then run: python3 demo_devops_pipeline.py\n")


if __name__ == "__main__":
    asyncio.run(main())