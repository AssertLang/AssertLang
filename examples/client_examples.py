"""
Examples of using the AssertLang MCP client library.

Demonstrates both simple function calls and reusable client instances.
"""
from assertlang import MCPClient, call_verb
from assertlang.exceptions import ConnectionError, InvalidVerbError, TimeoutError


def example_simple_call():
    """Simple one-off verb call using call_verb helper."""
    print("=== Example 1: Simple Call ===")

    result = call_verb(
        service="user-service",
        verb="user.get@v1",
        params={"user_id": "123"},
        address="http://localhost:23450"
    )

    print(f"User: {result.get('name')}")
    print(f"Email: {result.get('email')}")
    print(f"Mode: {result['metadata']['mode']}")


def example_reusable_client():
    """Reusable client instance for multiple calls."""
    print("\n=== Example 2: Reusable Client ===")

    client = MCPClient("http://localhost:23450")

    try:
        # Initialize connection
        server_info = client.initialize()
        print(f"Connected to: {server_info['serverInfo']['name']}")

        # List available tools
        tools = client.list_tools()
        print(f"Available tools: {[t['name'] for t in tools]}")

        # Make multiple calls
        result1 = client.call("user.get@v1", {"user_id": "123"})
        print(f"User 123: {result1.get('name')}")

        result2 = client.call("user.get@v1", {"user_id": "456"})
        print(f"User 456: {result2.get('name')}")

    finally:
        client.close()


def example_context_manager():
    """Using client as context manager (automatic cleanup)."""
    print("\n=== Example 3: Context Manager ===")

    with MCPClient("http://localhost:23450") as client:
        result = client.call("user.get@v1", {"user_id": "789"})
        print(f"User: {result.get('name')}")
        print(f"Tool results: {list(result.get('tool_results', {}).keys())}")


def example_error_handling():
    """Proper error handling for various failure modes."""
    print("\n=== Example 4: Error Handling ===")

    try:
        call_verb(
            service="user-service",
            verb="unknown.verb@v1",
            params={"param": "value"},
            address="http://localhost:23450",
            timeout=5.0,
            retries=2
        )
    except InvalidVerbError as e:
        print(f"Verb not found: {e.verb}")
    except TimeoutError as e:
        print(f"Request timed out: {e}")
    except ConnectionError as e:
        print(f"Connection failed: {e}")


def example_service_to_service():
    """One service calling another service."""
    print("\n=== Example 5: Service-to-Service Call ===")

    # Order service calling user service
    with MCPClient("http://localhost:23450") as user_client:
        # Validate user exists before creating order
        user = user_client.call("user.get@v1", {"user_id": "123"})

        if user.get('status') == 'active':
            print(f"User {user.get('name')} is active")

            # Now create order (would call order service in real scenario)
            with MCPClient("http://localhost:23451") as order_client:
                order = order_client.call("order.create@v1", {
                    "user_id": "123",
                    "items": ["item1", "item2"],
                    "total": 99.99
                })
                print(f"Order created: {order.get('order_id')}")
        else:
            print("User is not active, cannot create order")


def example_inspect_tools():
    """Inspect available tools and their schemas."""
    print("\n=== Example 6: Inspect Tools ===")

    with MCPClient("http://localhost:23450") as client:
        # List all tools
        tools = client.list_tools()

        for tool in tools:
            print(f"\nTool: {tool['name']}")
            print(f"Description: {tool.get('description', 'N/A')}")

            # Show parameters
            schema = tool.get('inputSchema', {})
            props = schema.get('properties', {})
            required = schema.get('required', [])

            print("Parameters:")
            for param_name, param_info in props.items():
                req_marker = "*" if param_name in required else " "
                print(f"  {req_marker} {param_name}: {param_info.get('type', 'any')}")


def example_custom_timeouts():
    """Configure custom timeouts and retries."""
    print("\n=== Example 7: Custom Timeouts ===")

    # Short timeout for fast fail
    client = MCPClient(
        "http://localhost:23450",
        timeout=2.0,  # 2 second timeout
        retries=1,    # Only 1 retry
        backoff_factor=1.5
    )

    try:
        result = client.call("user.get@v1", {"user_id": "123"})
        print(f"Success: {result.get('name')}")
    except TimeoutError:
        print("Request timed out quickly (2s)")
    finally:
        client.close()


def example_tool_results():
    """Inspect tool execution results."""
    print("\n=== Example 8: Tool Results ===")

    # Service that uses tools (e.g., http tool)
    with MCPClient("http://localhost:23460") as client:
        result = client.call("fetch.url@v1", {
            "url": "https://api.github.com/zen",
            "method": "GET"
        })

        # Check metadata
        print(f"Mode: {result['metadata']['mode']}")
        print(f"Tools executed: {result['metadata']['tools_executed']}")

        # Inspect tool results
        for tool_name, tool_result in result['tool_results'].items():
            print(f"\nTool: {tool_name}")
            print(f"Success: {tool_result.get('ok', False)}")
            if 'data' in tool_result:
                print(f"Data: {tool_result['data']}")


if __name__ == "__main__":
    print("AssertLang MCP Client Examples")
    print("=" * 50)
    print("\nNote: These examples assume services are running.")
    print("Start services first with:")
    print("  python3 generated_server.py")
    print()

    # Run examples
    # Uncomment to run (requires running servers):
    # example_simple_call()
    # example_reusable_client()
    # example_context_manager()
    # example_error_handling()
    # example_service_to_service()
    # example_inspect_tools()
    # example_custom_timeouts()
    # example_tool_results()

    print("\nTo run examples, uncomment function calls in __main__")
