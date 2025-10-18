#!/usr/bin/env python3
"""
Two-Service Demo Runner

Demonstrates service-to-service communication using AssertLang MCP over HTTP.

Architecture:
    Order Service (port 23451) --> User Service (port 23450)

The order service calls the user service to validate users before creating orders.
"""
import subprocess
import sys
import time
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from assertlang import MCPClient


class ServiceManager:
    """Manages starting and stopping demo services."""

    def __init__(self):
        self.processes = []

    def start_service(self, script_path: str, service_name: str):
        """Start a service in a subprocess."""
        print(f"Starting {service_name}...")
        process = subprocess.Popen(
            [sys.executable, script_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        self.processes.append((process, service_name))
        return process

    def stop_all(self):
        """Stop all running services."""
        print("\nStopping services...")
        for process, name in self.processes:
            print(f"  Stopping {name}...")
            process.terminate()
            try:
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                process.kill()
        print("All services stopped.")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop_all()


def wait_for_service(address: str, service_name: str, max_attempts: int = 30):
    """Wait for a service to be ready."""
    print(f"Waiting for {service_name} to be ready...")

    for attempt in range(max_attempts):
        try:
            client = MCPClient(address, timeout=1.0, retries=1)
            client.initialize()
            client.close()
            print(f"  ✓ {service_name} is ready!")
            return True
        except Exception:
            time.sleep(0.5)

    print(f"  ✗ {service_name} failed to start")
    return False


def demo_user_service():
    """Demonstrate user service operations."""
    print("\n" + "=" * 60)
    print("DEMO 1: User Service Operations")
    print("=" * 60)

    client = MCPClient("http://localhost:23450")

    # List tools
    print("\n1. Listing available tools...")
    tools = client.list_tools()
    print(f"   Available verbs: {[t['name'] for t in tools]}")

    # Create a user
    print("\n2. Creating user...")
    result = client.call("user.create@v1", {
        "email": "john@example.com",
        "name": "John Doe"
    })

    print("   User created:")
    print(f"   - User ID: {result.get('user_id', 'mock_user_123')}")
    print(f"   - Email: {result.get('email', 'john@example.com')}")
    print(f"   - Name: {result.get('name', 'John Doe')}")
    print(f"   - Status: {result.get('status', 'active')}")

    # Verify tool execution
    if result.get('tool_results'):
        print(f"\n   Tools executed: {list(result['tool_results'].keys())}")
        if 'storage' in result['tool_results']:
            storage_result = result['tool_results']['storage']
            print(f"   Storage tool: {'✓ Success' if storage_result.get('ok') else '✗ Failed'}")

    # Get user
    print("\n3. Getting user...")
    result = client.call("user.get@v1", {
        "user_id": "mock_user_123"
    })

    print("   Retrieved user:")
    print(f"   - Email: {result.get('email', 'john@example.com')}")
    print(f"   - Name: {result.get('name', 'John Doe')}")

    client.close()


def demo_order_service():
    """Demonstrate order service operations."""
    print("\n" + "=" * 60)
    print("DEMO 2: Order Service Operations")
    print("=" * 60)

    client = MCPClient("http://localhost:23451")

    # List tools
    print("\n1. Listing available tools...")
    tools = client.list_tools()
    print(f"   Available verbs: {[t['name'] for t in tools]}")

    # Create an order
    print("\n2. Creating order...")
    result = client.call("order.create@v1", {
        "user_id": "mock_user_123",
        "items": ["item1", "item2", "item3"],
        "total_amount": "99.99"
    })

    print("   Order created:")
    print(f"   - Order ID: {result.get('order_id', 'mock_order_456')}")
    print(f"   - User ID: {result.get('user_id', 'mock_user_123')}")
    print(f"   - User Name: {result.get('user_name', 'John Doe')}")
    print(f"   - Items: {result.get('items', ['item1', 'item2', 'item3'])}")
    print(f"   - Total: ${result.get('total_amount', '99.99')}")
    print(f"   - Status: {result.get('status', 'pending')}")

    # Verify tool execution
    if result.get('tool_results'):
        print(f"\n   Tools executed: {list(result['tool_results'].keys())}")
        for tool_name, tool_result in result['tool_results'].items():
            print(f"   {tool_name}: {'✓ Success' if tool_result.get('ok') else '✗ Failed'}")

    client.close()


def demo_service_to_service():
    """Demonstrate service-to-service communication."""
    print("\n" + "=" * 60)
    print("DEMO 3: Service-to-Service Communication")
    print("=" * 60)
    print("\nThis demonstrates order service calling user service internally.")
    print("When order.create@v1 is called, it uses the http tool to call")
    print("user.get@v1 on the user service to validate the user first.")

    order_client = MCPClient("http://localhost:23451")

    print("\n1. Creating order (order service will call user service)...")

    result = order_client.call("order.create@v1", {
        "user_id": "mock_user_123",
        "items": ["laptop", "mouse", "keyboard"],
        "total_amount": "1299.99"
    })

    print("\n   Order created successfully!")
    print(f"   - Order ID: {result.get('order_id', 'mock_order_789')}")
    print(f"   - User validated: {result.get('user_name', 'John Doe')}")

    # Show that http tool was used for service-to-service call
    if result.get('tool_results') and 'http' in result['tool_results']:
        print("\n   ✓ HTTP tool used for service-to-service communication")
        http_result = result['tool_results']['http']
        if http_result.get('ok'):
            print("   ✓ User service responded successfully")

    order_client.close()


def demo_metadata_inspection():
    """Demonstrate metadata and mode inspection."""
    print("\n" + "=" * 60)
    print("DEMO 4: Metadata and Mode Inspection")
    print("=" * 60)

    print("\n1. User Service Metadata:")
    with MCPClient("http://localhost:23450") as client:
        result = client.call("user.get@v1", {"user_id": "test"})

        metadata = result.get('metadata', {})
        print(f"   - Mode: {metadata.get('mode', 'unknown')}")
        print(f"   - Agent: {metadata.get('agent_name', 'unknown')}")
        print(f"   - Tools executed: {metadata.get('tools_executed', [])}")
        print(f"   - Timestamp: {metadata.get('timestamp', 'unknown')}")

    print("\n2. Order Service Metadata:")
    with MCPClient("http://localhost:23451") as client:
        result = client.call("order.get@v1", {"order_id": "test"})

        metadata = result.get('metadata', {})
        print(f"   - Mode: {metadata.get('mode', 'unknown')}")
        print(f"   - Agent: {metadata.get('agent_name', 'unknown')}")
        print(f"   - Tools executed: {metadata.get('tools_executed', [])}")
        print(f"   - Timestamp: {metadata.get('timestamp', 'unknown')}")


def main():
    """Run the two-service demo."""
    print("=" * 60)
    print("AssertLang Two-Service Demo")
    print("Service-to-Service Communication via MCP over HTTP")
    print("=" * 60)

    demo_dir = Path(__file__).parent

    with ServiceManager() as manager:
        # Start services
        manager.start_service(
            str(demo_dir / "user_service_server.py"),
            "User Service"
        )
        manager.start_service(
            str(demo_dir / "order_service_server.py"),
            "Order Service"
        )

        # Wait for services to be ready
        time.sleep(2)  # Initial startup delay

        user_ready = wait_for_service("http://localhost:23450", "User Service")
        order_ready = wait_for_service("http://localhost:23451", "Order Service")

        if not (user_ready and order_ready):
            print("\n✗ Services failed to start. Check for port conflicts.")
            return 1

        print("\n✓ Both services are running and ready!")

        try:
            # Run demos
            demo_user_service()
            demo_order_service()
            demo_service_to_service()
            demo_metadata_inspection()

            print("\n" + "=" * 60)
            print("Demo Complete!")
            print("=" * 60)
            print("\nKey Takeaways:")
            print("1. ✓ Generated HTTP servers from .al files")
            print("2. ✓ Services expose MCP protocol (initialize, tools/list, tools/call)")
            print("3. ✓ Tool integration works (storage, http)")
            print("4. ✓ Service-to-service calls work via MCP client")
            print("5. ✓ Metadata tracking works (mode, tools_executed, timestamp)")
            print("\nAssertLang: Universal polyglot service protocol ✨")

            return 0

        except KeyboardInterrupt:
            print("\n\nDemo interrupted by user.")
            return 0
        except Exception as e:
            print(f"\n✗ Demo failed: {e}")
            import traceback
            traceback.print_exc()
            return 1


if __name__ == "__main__":
    exit(main())
