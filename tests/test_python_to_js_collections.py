"""
Test Python → JavaScript Collection Translation

Tests that Python comprehensions translate correctly to JavaScript array methods.
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from language.python_parser_v2 import PythonParserV2
from language.nodejs_generator_v2 import NodeJSGeneratorV2


def test_python_list_comp_to_js():
    """Test Python list comprehension → JavaScript .map()"""
    python_code = """
def transform(numbers):
    doubled = [x * 2 for x in numbers]
    return doubled
"""
    parser = PythonParserV2()
    generator = NodeJSGeneratorV2(typescript=False)

    # Parse Python
    ir = parser.parse_source(python_code, "test")

    # Generate JavaScript
    js_code = generator.generate(ir)

    # Verify
    assert "numbers.map(" in js_code, "Should translate to .map()"
    assert "x => (x * 2)" in js_code or "x => x * 2" in js_code, "Should preserve transformation"

    print("✅ Python list comprehension → JavaScript .map()")
    print(f"Generated:\n{js_code}\n")
    return True


def test_python_filter_comp_to_js():
    """Test Python filtered comprehension → JavaScript .filter()"""
    python_code = """
def filter_positive(numbers):
    positive = [x for x in numbers if x > 0]
    return positive
"""
    parser = PythonParserV2()
    generator = NodeJSGeneratorV2(typescript=False)

    # Parse Python
    ir = parser.parse_source(python_code, "test")

    # Generate JavaScript
    js_code = generator.generate(ir)

    # Verify
    assert ".filter(" in js_code, "Should translate to .filter()"
    assert "x > 0" in js_code, "Should preserve condition"

    print("✅ Python filtered comprehension → JavaScript .filter()")
    print(f"Generated:\n{js_code}\n")
    return True


def test_python_filter_map_to_js():
    """Test Python comprehension with filter+map → JavaScript .filter().map()"""
    python_code = """
def process_numbers(numbers):
    result = [x * 2 for x in numbers if x > 0]
    return result
"""
    parser = PythonParserV2()
    generator = NodeJSGeneratorV2(typescript=False)

    # Parse Python
    ir = parser.parse_source(python_code, "test")

    # Generate JavaScript
    js_code = generator.generate(ir)

    # Verify
    assert ".filter(" in js_code, "Should have .filter()"
    assert ".map(" in js_code, "Should have .map()"

    print("✅ Python filtered+transformed comprehension → JavaScript .filter().map()")
    print(f"Generated:\n{js_code}\n")
    return True


def run_all_tests():
    """Run all Python → JavaScript collection translation tests"""
    tests = [
        ("List comprehension → .map()", test_python_list_comp_to_js),
        ("Filtered comprehension → .filter()", test_python_filter_comp_to_js),
        ("Filter+Map comprehension → .filter().map()", test_python_filter_map_to_js),
    ]

    print("=" * 80)
    print("Python → JavaScript Collection Translation Test")
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
