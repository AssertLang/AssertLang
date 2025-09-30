#!/usr/bin/env python3
"""
Simple demo: Call the code-reviewer agent
"""

from language.mcp_client import MCPClient

print("=" * 60)
print("Simple Agent Communication Demo")
print("=" * 60)
print()

# Create a client to talk to code-reviewer agent
client = MCPClient("http://127.0.0.1:23456")

print("1. Checking if agent is alive...")
try:
    health = client.health_check()
    print(f"   ✓ Agent is healthy: {health['agent']}")
except Exception as e:
    print(f"   ✗ Agent not running: {e}")
    print()
    print("Start the agent first:")
    print("  python3 examples/demo_agent_server.py")
    exit(1)

print()

print("2. Asking agent: What verbs do you expose?")
verbs = client.list_verbs()
print(f"   Agent '{verbs['agent']}' exposes:")
for verb in verbs['verbs']:
    print(f"     - {verb}")

print()

print("3. Calling agent: Please review this PR")
print("   Sending: review.submit@v1 with pr_url")

response = client.call(
    "review.submit@v1",
    {"pr_url": "https://github.com/myteam/myrepo/pull/123"}
)

if response.is_success():
    data = response.get_data()
    print(f"   ✓ Agent responded!")
    print(f"   ✓ Review ID: {data['review_id']}")
    print(f"   ✓ Status: {data['status']}")
else:
    print(f"   ✗ Agent returned error: {response.error}")

print()

print("4. Asking agent: What's the status of that review?")
response = client.call(
    "review.status@v1",
    {"review_id": data['review_id']}
)

if response.is_success():
    status_data = response.get_data()
    print(f"   ✓ Status: {status_data['status']}")
    print(f"   ✓ Progress: {status_data['progress']}%")
    print(f"   ✓ Comments: {len(status_data['comments'])} items")

print()
print("=" * 60)
print("Two agents just coordinated! ✅")
print("=" * 60)
print()
print("What happened:")
print("1. Agent A (this script) asked Agent B (code-reviewer) if it's alive")
print("2. Agent A asked Agent B what it can do")
print("3. Agent A told Agent B to review a PR")
print("4. Agent B processed the request and responded")
print("5. Agent A asked for status, Agent B responded")
print()
print("This is bidirectional MCP communication working.")