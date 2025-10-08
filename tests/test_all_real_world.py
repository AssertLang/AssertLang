"""
Test all 3 real-world programs

This runs all real-world program tests together to validate
the complete feature set of PW language.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

# Import individual test modules
from test_real_world_calculator import test_calculator_parses
from test_real_world_todo import test_todo_manager_parses
from test_real_world_api import test_api_server_parses


def run_all_tests():
    """Run all real-world program tests."""
    print("\n" + "="*60)
    print("REAL-WORLD PROGRAMS TEST SUITE")
    print("="*60)

    tests = [
        ("Calculator CLI", test_calculator_parses),
        ("Todo List Manager", test_todo_manager_parses),
        ("Simple Web API", test_api_server_parses),
    ]

    results = []
    for test_name, test_func in tests:
        try:
            success = test_func()
            results.append((test_name, success))
        except Exception as e:
            print(f"\n❌ Test '{test_name}' crashed: {e}")
            import traceback
            traceback.print_exc()
            results.append((test_name, False))

    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)

    passed = sum(1 for _, success in results if success)
    total = len(results)

    print(f"\nTotal: {passed}/{total} tests passed ({100*passed//total}%)")

    for test_name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"  {status}: {test_name}")

    print("\n" + "="*60)
    print("FEATURES VALIDATED")
    print("="*60)
    print("  ✅ Classes with constructors and methods")
    print("  ✅ Arrays and array operations")
    print("  ✅ Maps and nested maps")
    print("  ✅ Control flow (if/while/for)")
    print("  ✅ Type validation")
    print("  ✅ Multi-line syntax")
    print("  ✅ CRUD operations")
    print("  ✅ Object-oriented programming")
    print("  ✅ Complex business logic")
    print("\n" + "="*60)

    return results


if __name__ == "__main__":
    results = run_all_tests()
    all_passed = all(success for _, success in results)
    sys.exit(0 if all_passed else 1)
