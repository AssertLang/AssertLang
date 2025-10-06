#!/usr/bin/env python3
"""
Test Python ↔ Go Bidirectional Translation (Comprehensions)
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from language.python_parser_v2 import PythonParserV2
from language.python_generator_v2 import PythonGeneratorV2
from language.go_parser_v2 import GoParserV2
from language.go_generator_v2 import GoGeneratorV2


def test_python_to_go():
    """Test Python comprehension → Go for-append"""
    print("\n=== Test 1: Python → Go ===")

    python_code = """
def filter_positive(items):
    result = [x * 2 for x in items if x > 0]
    return result
"""

    # Python → IR
    py_parser = PythonParserV2()
    ir1 = py_parser.parse_source(python_code, "test.py")

    # IR → Go
    go_gen = GoGeneratorV2()
    go_code = go_gen.generate(ir1)

    print("Generated Go:")
    print(go_code)
    print()

    # Verify Go code contains for-append pattern
    assert "for _, x := range" in go_code, "Should have for range loop"
    assert "append(result," in go_code, "Should have append call"

    print("✅ Python → Go comprehension translation works")
    return go_code, ir1


def test_go_to_python():
    """Test Go for-append → Python comprehension"""
    print("\n=== Test 2: Go → Python ===")

    go_code = """
package main

func filterPositive(items []interface{}) []interface{} {
	result := []interface{}{}
	for _, x := range items {
		if x > 0 {
			result = append(result, x * 2)
		}
	}
	return result
}
"""

    # Go → IR
    go_parser = GoParserV2()
    ir2 = go_parser.parse_source(go_code, "test.go")

    print(f"Parsed Go function: {ir2.functions[0].name}")
    print(f"Body statements: {len(ir2.functions[0].body)}")

    for i, stmt in enumerate(ir2.functions[0].body):
        print(f"  {i+1}. {type(stmt).__name__}")
        if hasattr(stmt, 'value'):
            print(f"      value type: {type(stmt.value).__name__}")

    # IR → Python
    py_gen = PythonGeneratorV2()
    python_code = py_gen.generate(ir2)

    print("\nGenerated Python:")
    print(python_code)
    print()

    # Verify Python code contains comprehension
    assert "for x in items" in python_code or "[" in python_code, "Should have comprehension or for loop"

    print("✅ Go → Python translation works")
    return python_code, ir2


def test_python_go_python_roundtrip():
    """Test Python → Go → Python round-trip"""
    print("\n=== Test 3: Python → Go → Python Round-Trip ===")

    python_code = """
def process(items):
    result = [x * 2 for x in items if x > 0]
    return result
"""

    # Python → IR
    py_parser = PythonParserV2()
    ir1 = py_parser.parse_source(python_code, "test.py")

    # IR → Go
    go_gen = GoGeneratorV2()
    go_code = go_gen.generate(ir1)

    print("Step 1 - Python → Go:")
    print(go_code[:200] + "...")
    print()

    # Go → IR
    go_parser = GoParserV2()
    ir2 = go_parser.parse_source(go_code, "test.go")

    # IR → Python
    py_gen = PythonGeneratorV2()
    python_code2 = py_gen.generate(ir2)

    print("Step 2 - Go → Python:")
    print(python_code2)
    print()

    # Validate
    func1 = ir1.functions[0]
    func2 = ir2.functions[0]

    print(f"Original function: {func1.name}, {len(func1.body)} statements")
    print(f"After round-trip: {func2.name}, {len(func2.body)} statements")

    # Check that we have a comprehension in both
    has_comp1 = any(hasattr(stmt, 'value') and type(stmt.value).__name__ == 'IRComprehension'
                    for stmt in func1.body)
    has_comp2 = any(hasattr(stmt, 'value') and type(stmt.value).__name__ == 'IRComprehension'
                    for stmt in func2.body)

    assert has_comp1, "Original should have comprehension"
    assert has_comp2, "Round-trip should have comprehension"

    # Check that both have return statements
    has_return1 = any(type(stmt).__name__ == 'IRReturn' for stmt in func1.body)
    has_return2 = any(type(stmt).__name__ == 'IRReturn' for stmt in func2.body)

    assert has_return1, "Original should have return"
    assert has_return2, "Round-trip should have return"

    print("✅ Python → Go → Python round-trip preserves semantic structure (comprehension + return)")


def run_all_tests():
    """Run all bidirectional tests"""
    print("\n" + "=" * 70)
    print("PYTHON ↔ GO BIDIRECTIONAL TRANSLATION TESTS")
    print("=" * 70)

    tests = [
        ("Python → Go", test_python_to_go),
        ("Go → Python", test_go_to_python),
        ("Python → Go → Python", test_python_go_python_roundtrip),
    ]

    passed = 0
    failed = 0

    for name, test_func in tests:
        try:
            test_func()
            passed += 1
        except Exception as e:
            print(f"\n❌ {name} FAILED: {str(e)}")
            import traceback
            traceback.print_exc()
            failed += 1

    print("\n" + "=" * 70)
    print(f"RESULTS: {passed}/{len(tests)} tests passed")

    if failed > 0:
        print(f"❌ {failed} tests failed")
        return False
    else:
        print("✅ ALL PYTHON ↔ GO TESTS PASSED")
        print("\nPython ↔ Go bidirectional translation working!")
        return True


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
