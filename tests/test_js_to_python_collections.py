"""
Test JavaScript → Python Collection Translation

Tests that JavaScript array methods translate correctly to Python comprehensions.
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from language.nodejs_parser_v2 import NodeJSParserV2
from language.python_generator_v2 import PythonGeneratorV2


def test_js_map_to_python():
    """Test JavaScript .map() → Python list comprehension"""
    js_code = """
function transform(numbers) {
    const doubled = numbers.map(x => x * 2);
    return doubled;
}
"""
    parser = NodeJSParserV2()
    generator = PythonGeneratorV2()

    # Parse JavaScript
    ir = parser.parse_source(js_code, "test")

    # Generate Python
    python_code = generator.generate(ir)

    # Verify
    assert "[" in python_code and "for" in python_code and "in" in python_code, \
        "Should translate to list comprehension"
    assert "x * 2" in python_code, "Should preserve transformation"

    print("✅ JavaScript .map() → Python list comprehension")
    print(f"Generated:\n{python_code}\n")
    return True


def test_js_filter_to_python():
    """Test JavaScript .filter() → Python filtered comprehension"""
    js_code = """
function filterPositive(numbers) {
    const positive = numbers.filter(x => x > 0);
    return positive;
}
"""
    parser = NodeJSParserV2()
    generator = PythonGeneratorV2()

    # Parse JavaScript
    ir = parser.parse_source(js_code, "test")

    # Generate Python
    python_code = generator.generate(ir)

    # Verify
    assert "if x > 0" in python_code, "Should preserve filter condition"
    assert "[" in python_code and "for" in python_code, "Should be a comprehension"

    print("✅ JavaScript .filter() → Python filtered comprehension")
    print(f"Generated:\n{python_code}\n")
    return True


def test_js_filter_map_to_python():
    """Test JavaScript .filter().map() → Python comprehension"""
    js_code = """
function processNumbers(numbers) {
    const result = numbers.filter(x => x > 0).map(x => x * 2);
    return result;
}
"""
    parser = NodeJSParserV2()
    generator = PythonGeneratorV2()

    # Parse JavaScript
    ir = parser.parse_source(js_code, "test")

    # Generate Python
    python_code = generator.generate(ir)

    # Verify
    assert "for x in" in python_code, "Should have iterator"
    assert "if x > 0" in python_code, "Should preserve filter"
    assert "x * 2" in python_code, "Should preserve transformation"

    print("✅ JavaScript .filter().map() → Python comprehension")
    print(f"Generated:\n{python_code}\n")
    return True


def run_all_tests():
    """Run all JavaScript → Python collection translation tests"""
    tests = [
        (".map() → list comprehension", test_js_map_to_python),
        (".filter() → filtered comprehension", test_js_filter_to_python),
        (".filter().map() → filtered+transformed comprehension", test_js_filter_map_to_python),
    ]

    print("=" * 80)
    print("JavaScript → Python Collection Translation Test")
    print("=" * 80)
    print()

    passed = 0
    failed = 0

    for name, test_func in tests:
        try:
            test_func()
            passed += 1
        except Exception as e:
            print(f"❌ {name} FAILED: {e}")
            import traceback
            traceback.print_exc()
            failed += 1

    print()
    print("=" * 80)
    print(f"Results: {passed} passed, {failed} failed")
    print("=" * 80)

    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
