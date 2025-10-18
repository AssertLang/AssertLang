"""
Example: Testing a AssertLang MCP Agent

Demonstrates how to use the AgentTester class to:
- Auto-generate test fixtures
- Run integration tests
- Perform load testing
- Track coverage
- Export reports
"""

from assertlang.testing import AgentTester, TestCase

# Configuration
AGENT_URL = "http://localhost:3000"


def example_health_check():
    """Example: Basic health check."""
    print("=== Health Check ===\n")

    tester = AgentTester(AGENT_URL)

    # Check if agent is alive
    if tester.health_check(verbose=True):
        print("\n✓ Agent is healthy and ready to test\n")
    else:
        print("\n✗ Agent is not responding\n")
        return False

    return True


def example_verb_discovery():
    """Example: Discover available verbs."""
    print("=== Verb Discovery ===\n")

    tester = AgentTester(AGENT_URL)

    # Discover all verbs
    verbs = tester.discover_verbs()

    print(f"Discovered {len(verbs)} verbs:\n")
    for verb in verbs:
        print(f"  • {verb['name']}")
        if verb.get('description'):
            print(f"    {verb['description']}")

        # Show parameters
        input_schema = verb.get('inputSchema', {})
        properties = input_schema.get('properties', {})
        if properties:
            print(f"    Parameters: {', '.join(properties.keys())}")
        print()


def example_auto_generated_tests():
    """Example: Auto-generate and run tests."""
    print("=== Auto-Generated Integration Tests ===\n")

    tester = AgentTester(AGENT_URL)

    # Auto-generate test fixtures from verb schemas
    test_cases = tester.generate_test_fixtures()
    print(f"Generated {len(test_cases)} test cases\n")

    # Run integration tests
    summary = tester.run_integration_tests(test_cases, verbose=True)

    return summary['failed'] == 0


def example_custom_tests():
    """Example: Custom test cases."""
    print("\n=== Custom Test Cases ===\n")

    tester = AgentTester(AGENT_URL)

    # Define custom test cases
    test_cases = [
        TestCase(
            name="test_user_create_valid",
            verb="user.create@v1",
            params={
                "email": "alice@example.com",
                "name": "Alice Johnson",
                "role": "admin"
            },
            expected_fields=["user_id", "email", "name"],
        ),
        TestCase(
            name="test_user_create_missing_email",
            verb="user.create@v1",
            params={
                "name": "Bob Smith"
            },
            expected_fields=[],
            expect_error=True,
            error_code=-32602,  # Invalid params
        ),
        TestCase(
            name="test_user_get_valid",
            verb="user.get@v1",
            params={
                "user_id": "123"
            },
            expected_fields=["user_id", "email", "name"],
        ),
    ]

    # Run custom tests
    summary = tester.run_integration_tests(test_cases, verbose=True)

    return summary['failed'] == 0


def example_load_testing():
    """Example: Load test a specific verb."""
    print("\n=== Load Testing ===\n")

    tester = AgentTester(AGENT_URL)

    # Load test user.create@v1
    result = tester.run_load_test(
        verb_name="user.create@v1",
        params={
            "email": "loadtest@example.com",
            "name": "Load Test User"
        },
        num_requests=100,
        concurrency=10,
        verbose=True
    )

    # Check results
    success_rate = (result.successful / result.total_requests) * 100
    print(f"\nSuccess rate: {success_rate:.1f}%")

    return success_rate >= 95.0  # 95% success threshold


def example_coverage_report():
    """Example: Export coverage report."""
    print("\n=== Coverage Report ===\n")

    tester = AgentTester(AGENT_URL)

    # Run tests to populate coverage
    tester.discover_verbs()
    tester.run_integration_tests(verbose=False)

    # Export coverage
    tester.export_coverage_report("coverage.json")

    # Display coverage stats
    coverage_pct = (sum(tester.coverage.values()) / len(tester.coverage) * 100) if tester.coverage else 0
    print(f"\nCoverage: {coverage_pct:.1f}%")
    print(f"Tested: {sum(tester.coverage.values())} / {len(tester.coverage)} verbs")


def example_production_workflow():
    """Example: Production testing workflow."""
    print("\n=== Production Testing Workflow ===\n")

    tester = AgentTester(AGENT_URL, timeout=60)

    # Step 1: Health check
    print("1. Health check...")
    if not tester.health_check(verbose=False):
        print("   ✗ Failed - agent not healthy")
        return False
    print("   ✓ Passed")

    # Step 2: Discover verbs
    print("\n2. Verb discovery...")
    verbs = tester.discover_verbs()
    print(f"   ✓ Discovered {len(verbs)} verbs")

    # Step 3: Auto-generate and run tests
    print("\n3. Integration tests...")
    test_cases = tester.generate_test_fixtures()
    summary = tester.run_integration_tests(test_cases, verbose=False)
    print(f"   Passed: {summary['passed']}/{summary['total']}")

    if summary['failed'] > 0:
        print(f"   ✗ {summary['failed']} tests failed")
        return False

    # Step 4: Load test critical verbs
    print("\n4. Load testing critical verbs...")
    critical_verbs = [v['name'] for v in verbs if 'create' in v['name'] or 'update' in v['name']]

    for verb_name in critical_verbs[:3]:  # Test first 3 critical verbs
        verb = next(v for v in verbs if v['name'] == verb_name)
        input_schema = verb.get('inputSchema', {})
        properties = input_schema.get('properties', {})
        test_params = tester._generate_test_data(properties, input_schema.get('required', []))

        result = tester.run_load_test(
            verb_name,
            test_params,
            num_requests=50,
            concurrency=5,
            verbose=False
        )

        success_rate = (result.successful / result.total_requests) * 100
        print(f"   {verb_name}: {success_rate:.1f}% success, {result.avg_latency_ms:.0f}ms avg")

    # Step 5: Export coverage
    print("\n5. Exporting coverage report...")
    tester.export_coverage_report()

    print("\n✨ All production tests passed!")
    return True


if __name__ == "__main__":
    print("AssertLang Agent Testing Examples\n")
    print("Make sure you have an agent running at http://localhost:3000")
    print("Example: python3 examples/demo/python/user_service_server.py\n")
    print("="*60 + "\n")

    try:
        # Run examples
        if not example_health_check():
            print("\n⚠️  Agent not responding - skipping remaining examples")
            exit(1)

        example_verb_discovery()

        # Choose which examples to run
        print("\nSelect examples to run:")
        print("1. Auto-generated tests")
        print("2. Custom tests")
        print("3. Load testing")
        print("4. Coverage report")
        print("5. Full production workflow")
        print("6. All examples")

        choice = input("\nEnter choice (1-6): ").strip()

        if choice == "1":
            example_auto_generated_tests()
        elif choice == "2":
            example_custom_tests()
        elif choice == "3":
            example_load_testing()
        elif choice == "4":
            example_coverage_report()
        elif choice == "5":
            example_production_workflow()
        elif choice == "6":
            example_auto_generated_tests()
            example_custom_tests()
            example_load_testing()
            example_coverage_report()
        else:
            print("Invalid choice")

        print("\n" + "="*60)
        print("Examples complete!")

    except KeyboardInterrupt:
        print("\n\nExamples interrupted by user")
    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()
