"""
Example: Using the Promptware Python SDK

Demonstrates all SDK features:
- Dynamic verb discovery
- Automatic retries
- Circuit breaker
- Health checks
- Error handling
"""

import logging

from assertlang.sdk import (
    Agent,
    CircuitBreakerError,
    ConnectionError,
    InvalidParamsError,
    VerbNotFoundError,
)

# Enable logging to see what's happening
logging.basicConfig(level=logging.INFO)


def basic_usage():
    """Basic SDK usage example."""
    print("=== Basic Usage ===\n")

    # Create agent client
    agent = Agent("http://localhost:3000")

    # Health check
    health = agent.health()
    print(f"Health: {health}")

    # List available verbs
    verbs = agent.list_verbs()
    print(f"\nAvailable verbs: {verbs}")

    # Call verb with dot notation (assumes @v1)
    try:
        result = agent.user.create(
            email="alice@example.com",
            name="Alice Johnson"
        )
        print(f"\nUser created: {result}")
    except VerbNotFoundError:
        print("\nNote: user.create@v1 verb not found - using mock agent")


def with_context_manager():
    """Using context manager for automatic cleanup."""
    print("\n=== Context Manager ===\n")

    with Agent("http://localhost:3000") as agent:
        # Connection automatically closed when exiting
        ready = agent.ready()
        print(f"Readiness: {ready}")


def error_handling():
    """Comprehensive error handling."""
    print("\n=== Error Handling ===\n")

    agent = Agent("http://localhost:3000")

    try:
        # This will fail if verb doesn't exist
        agent.nonexistent.verb()
    except VerbNotFoundError as e:
        print(f"Verb not found: {e}")

    try:
        # This will fail if parameters are invalid
        agent.user.create()  # Missing required params
    except InvalidParamsError as e:
        print(f"Invalid parameters: {e}")

    try:
        # This will fail if service is down
        bad_agent = Agent("http://localhost:9999", timeout=5)
        bad_agent.health()
    except ConnectionError as e:
        print(f"Connection failed: {e}")


def with_retries():
    """Automatic retry configuration."""
    print("\n=== Automatic Retries ===\n")

    agent = Agent(
        "http://localhost:3000",
        max_retries=5,
        retry_delay=2.0,
        timeout=60
    )

    # Will automatically retry on network errors
    try:
        result = agent.user.get(user_id="123")
        print(f"User retrieved (with retries): {result}")
    except VerbNotFoundError:
        print("Note: user.get@v1 verb not found - using mock agent")


def circuit_breaker_example():
    """Circuit breaker pattern."""
    print("\n=== Circuit Breaker ===\n")

    Agent(
        "http://localhost:3000",
        circuit_breaker_threshold=3,  # Open after 3 failures
        circuit_breaker_timeout=10    # Try again after 10 seconds
    )

    # Simulate failures
    bad_agent = Agent(
        "http://localhost:9999",  # Bad URL
        circuit_breaker_threshold=2,
        timeout=2
    )

    for i in range(5):
        try:
            bad_agent.health()
        except CircuitBreakerError:
            print(f"Attempt {i+1}: Circuit breaker is OPEN - service unavailable")
            break
        except ConnectionError:
            print(f"Attempt {i+1}: Connection failed")


def verb_discovery():
    """Discover and introspect verbs."""
    print("\n=== Verb Discovery ===\n")

    agent = Agent("http://localhost:3000")

    # Discover all verbs
    verbs = agent.discover()
    print(f"Discovered {len(verbs)} verbs:")

    for verb in verbs:
        print(f"\nVerb: {verb['name']}")
        print(f"  Description: {verb.get('description', 'N/A')}")

        # Show parameters
        input_schema = verb.get('inputSchema', {})
        properties = input_schema.get('properties', {})
        required = input_schema.get('required', [])

        if properties:
            print("  Parameters:")
            for param_name, param_schema in properties.items():
                required_str = " (required)" if param_name in required else ""
                param_type = param_schema.get('type', 'unknown')
                print(f"    - {param_name}: {param_type}{required_str}")


def production_config():
    """Production-ready configuration."""
    print("\n=== Production Configuration ===\n")

    agent = Agent(
        base_url="http://localhost:3000",
        timeout=60,
        max_retries=5,
        retry_delay=2.0,
        circuit_breaker_threshold=10,
        circuit_breaker_timeout=120,
        enable_logging=True
    )

    # Use in production with proper error handling
    try:
        with agent:
            # Health check before processing
            health = agent.health()
            if health.get('status') != 'alive':
                raise RuntimeError("Service not healthy")

            # Process requests
            result = agent.user.create(
                email="production@example.com",
                name="Production User"
            )
            print(f"Production request successful: {result}")

    except VerbNotFoundError:
        print("Note: user.create@v1 verb not found - using mock agent")
    except Exception as e:
        print(f"Production error: {e}")


def convenience_function():
    """Using the convenience function for one-off calls."""
    print("\n=== Convenience Function ===\n")

    from assertlang.sdk import call_verb

    # One-off verb call
    try:
        result = call_verb(
            base_url="http://localhost:3000",
            verb_name="user.get@v1",
            params={"user_id": "123"}
        )
        print(f"One-off call result: {result}")
    except VerbNotFoundError:
        print("Note: user.get@v1 verb not found - using mock agent")


if __name__ == "__main__":
    print("Promptware SDK Examples\n")
    print("Make sure you have an agent running on http://localhost:3000")
    print("Or use: promptware generate test.al --lang python && cd generated/test && python test_server.py\n")

    try:
        basic_usage()
        with_context_manager()
        error_handling()
        with_retries()
        circuit_breaker_example()
        verb_discovery()
        production_config()
        convenience_function()

        print("\n=== All Examples Complete ===")

    except KeyboardInterrupt:
        print("\n\nExamples interrupted by user")
