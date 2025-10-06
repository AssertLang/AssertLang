"""
Test JavaScript Collection Operations

Tests .map() and .filter() parsing and generation.
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from language.nodejs_parser_v2 import NodeJSParserV2
from language.nodejs_generator_v2 import NodeJSGeneratorV2
from dsl.ir import IRComprehension


def test_js_map_parsing():
    """Test parsing array.map(x => x * 2)"""
    code = """
function transform(numbers) {
    const doubled = numbers.map(x => x * 2);
    return doubled;
}
"""
    parser = NodeJSParserV2()
    ir = parser.parse_source(code, "test_map")

    # Check function exists
    assert len(ir.functions) == 1
    func = ir.functions[0]
    assert func.name == "transform"

    # Check comprehension was parsed
    assignment = func.body[0]
    assert hasattr(assignment, 'value')
    comp = assignment.value
    assert isinstance(comp, IRComprehension), f"Expected IRComprehension, got {type(comp)}"

    print("✅ JavaScript .map() parsing works")
    return True


def test_js_filter_parsing():
    """Test parsing array.filter(x => x > 0)"""
    code = """
function filterPositive(numbers) {
    const positive = numbers.filter(x => x > 0);
    return positive;
}
"""
    parser = NodeJSParserV2()
    ir = parser.parse_source(code, "test_filter")

    # Check function exists
    assert len(ir.functions) == 1
    func = ir.functions[0]

    # Check comprehension was parsed
    assignment = func.body[0]
    comp = assignment.value
    assert isinstance(comp, IRComprehension), f"Expected IRComprehension, got {type(comp)}"
    assert comp.condition is not None, "Filter should have condition"

    print("✅ JavaScript .filter() parsing works")
    return True


def test_js_filter_map_parsing():
    """Test parsing array.filter().map()"""
    code = """
function processNumbers(numbers) {
    const result = numbers.filter(x => x > 0).map(x => x * 2);
    return result;
}
"""
    parser = NodeJSParserV2()
    ir = parser.parse_source(code, "test_filter_map")

    # Check function exists
    assert len(ir.functions) == 1
    func = ir.functions[0]

    # Check comprehension was parsed
    assignment = func.body[0]
    comp = assignment.value
    assert isinstance(comp, IRComprehension), f"Expected IRComprehension, got {type(comp)}"
    assert comp.condition is not None, "Should have filter condition"

    print("✅ JavaScript .filter().map() parsing works")
    return True


def test_js_roundtrip():
    """Test JavaScript → IR → JavaScript round-trip"""
    code = """
function processData(items) {
    const filtered = items.filter(x => x > 10);
    const mapped = items.map(y => y * 2);
    const both = items.filter(z => z > 5).map(z => z + 1);
    return both;
}
"""
    parser = NodeJSParserV2()
    generator = NodeJSGeneratorV2(typescript=False)

    # Parse
    ir = parser.parse_source(code, "test_roundtrip")

    # Generate
    generated = generator.generate(ir)

    # Verify output contains array methods
    assert ".filter(" in generated, "Generated code should contain .filter()"
    assert ".map(" in generated, "Generated code should contain .map()"

    print("✅ JavaScript collection round-trip works")
    print("\nGenerated code:")
    print(generated)
    return True


def run_all_tests():
    """Run all JavaScript collection tests"""
    tests = [
        ("Map parsing", test_js_map_parsing),
        ("Filter parsing", test_js_filter_parsing),
        ("Filter+Map parsing", test_js_filter_map_parsing),
        ("Round-trip", test_js_roundtrip),
    ]

    print("=" * 80)
    print("JavaScript Collection Operations Test")
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
