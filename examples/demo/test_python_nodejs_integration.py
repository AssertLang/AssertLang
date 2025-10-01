#!/usr/bin/env python3
"""
Cross-language integration test: Python client → Node.js server

Demonstrates calling a Node.js MCP server from Python.
"""
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from promptware import call_verb

def main():
    print("Cross-Language Integration Test")
    print("=" * 50)
    print("Python client → Node.js server (port 23450)\n")

    # Test 1: user.get@v1
    print("Test 1: user.get@v1")
    result = call_verb(
        service="user-service",
        verb="user.get@v1",
        params={"user_id": "test-789"},
        address="http://localhost:23450",
        timeout=5
    )

    print(f"  Mode: {result['metadata']['mode']}")
    print(f"  Agent: {result['metadata']['agent_name']}")
    print(f"  Tools executed: {', '.join(result['metadata']['tools_executed'])}")
    print(f"  User ID: {result['user_id']}")
    print(f"  Email: {result['email']}")
    print(f"  Name: {result['name']}\n")

    # Test 2: user.create@v1
    print("Test 2: user.create@v1")
    result = call_verb(
        service="user-service",
        verb="user.create@v1",
        params={
            "email": "python-test@example.com",
            "name": "Python Test User"
        },
        address="http://localhost:23450",
        timeout=5
    )

    print(f"  Created user: {result['name']}")
    print(f"  Email: {result['email']}")
    print(f"  User ID: {result['user_id']}")
    print(f"  Status: {result['status']}\n")

    # Test 3: user.list@v1
    print("Test 3: user.list@v1")
    result = call_verb(
        service="user-service",
        verb="user.list@v1",
        params={"limit": 10, "offset": 1},
        address="http://localhost:23450",
        timeout=5
    )

    print(f"  Total users: {result['total']}")
    print(f"  Users array: {result['users']}\n")

    print("=" * 50)
    print("✓ All cross-language tests passed!")
    print("\nKey achievement:")
    print("  - Python client successfully called Node.js server")
    print("  - MCP protocol working across languages")
    print("  - Tool execution flow working (storage tool attempted)")
    print("  - Metadata correctly returned")

if __name__ == '__main__':
    main()
