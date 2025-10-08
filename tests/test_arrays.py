"""
Test PW parser array support.

Tests:
1. Array literal
2. Array indexing
3. Array assignment
4. Array in for loop
5. Nested arrays
6. Array with different types
7. Empty array
8. Array code generation
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
sys.path.insert(0, str(Path(__file__).parent.parent / 'pw-syntax-mcp-server'))

from dsl.pw_parser import parse_pw
from translators.ir_converter import ir_to_mcp
from translators.python_bridge import pw_to_python


def test_array_literal():
    """Test array literal creation."""
    print(f"\n{'='*60}")
    print("Testing array literal")
    print(f"{'='*60}")

    pw_code = """function create_array() -> array {
    let numbers = [1, 2, 3, 4, 5];
    return numbers;
}"""

    try:
        ir = parse_pw(pw_code)
        print(f"  ✅ Parser: {len(ir.functions)} functions")

        func = ir.functions[0]
        # Check for array in body
        has_array = False
        for stmt in func.body:
            if hasattr(stmt, 'value') and hasattr(stmt.value, 'type'):
                if str(stmt.value.type) == 'NodeType.ARRAY':
                    has_array = True
                    print(f"  ✅ Array literal found with {len(stmt.value.elements)} elements")
                    break

        if has_array:
            print(f"\n✅ SUCCESS: Array literal works!")
            return True
        else:
            print(f"\n❌ FAILED: No array literal found")
            return False

    except Exception as e:
        print(f"\n❌ FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_array_indexing():
    """Test array indexing."""
    print(f"\n{'='*60}")
    print("Testing array indexing")
    print(f"{'='*60}")

    pw_code = """function get_first(arr: array) -> int {
    let first = arr[0];
    return first;
}"""

    try:
        ir = parse_pw(pw_code)
        print(f"  ✅ Parser: {len(ir.functions)} functions")
        print(f"\n✅ SUCCESS: Array indexing works!")
        return True

    except Exception as e:
        print(f"\n❌ FAILED: {e}")
        return False


def test_array_assignment():
    """Test array element assignment."""
    print(f"\n{'='*60}")
    print("Testing array element assignment")
    print(f"{'='*60}")

    pw_code = """function update_array(arr: array, value: int) -> array {
    arr[0] = value;
    return arr;
}"""

    try:
        ir = parse_pw(pw_code)
        print(f"  ✅ Parser: {len(ir.functions)} functions")
        print(f"\n✅ SUCCESS: Array element assignment works!")
        return True

    except Exception as e:
        print(f"\n❌ FAILED: {e}")
        return False


def test_array_in_for_loop():
    """Test array in for loop."""
    print(f"\n{'='*60}")
    print("Testing array in for loop")
    print(f"{'='*60}")

    pw_code = """function sum_array(numbers: array) -> int {
    let total = 0;
    for (num in numbers) {
        total = total + num;
    }
    return total;
}"""

    try:
        ir = parse_pw(pw_code)
        print(f"  ✅ Parser: {len(ir.functions)} functions")
        print(f"\n✅ SUCCESS: Array in for loop works!")
        return True

    except Exception as e:
        print(f"\n❌ FAILED: {e}")
        return False


def test_nested_arrays():
    """Test nested arrays (2D array)."""
    print(f"\n{'='*60}")
    print("Testing nested arrays")
    print(f"{'='*60}")

    pw_code = """function create_matrix() -> array {
    let matrix = [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 9]
    ];
    return matrix;
}"""

    try:
        ir = parse_pw(pw_code)
        print(f"  ✅ Parser: {len(ir.functions)} functions")
        print(f"\n✅ SUCCESS: Nested arrays work!")
        return True

    except Exception as e:
        print(f"\n❌ FAILED: {e}")
        return False


def test_array_different_types():
    """Test array with different literal types."""
    print(f"\n{'='*60}")
    print("Testing array with different types")
    print(f"{'='*60}")

    pw_code = """function create_mixed() -> array {
    let strings = ["Alice", "Bob", "Charlie"];
    let floats = [1.5, 2.5, 3.5];
    let bools = [true, false, true];
    return strings;
}"""

    try:
        ir = parse_pw(pw_code)
        print(f"  ✅ Parser: {len(ir.functions)} functions")
        print(f"\n✅ SUCCESS: Arrays with different types work!")
        return True

    except Exception as e:
        print(f"\n❌ FAILED: {e}")
        return False


def test_empty_array():
    """Test empty array."""
    print(f"\n{'='*60}")
    print("Testing empty array")
    print(f"{'='*60}")

    pw_code = """function create_empty() -> array {
    let empty = [];
    return empty;
}"""

    try:
        ir = parse_pw(pw_code)
        print(f"  ✅ Parser: {len(ir.functions)} functions")
        print(f"\n✅ SUCCESS: Empty array works!")
        return True

    except Exception as e:
        print(f"\n❌ FAILED: {e}")
        return False


def test_array_code_generation():
    """Test that arrays generate correct Python code."""
    print(f"\n{'='*60}")
    print("Testing array code generation")
    print(f"{'='*60}")

    pw_code = """function get_numbers() -> array {
    let numbers = [10, 20, 30];
    return numbers;
}"""

    try:
        ir = parse_pw(pw_code)
        print(f"  ✅ Parser: {len(ir.functions)} functions")

        mcp_tree = ir_to_mcp(ir)
        print(f"  ✅ MCP tree created")

        python_code = pw_to_python(mcp_tree)
        print(f"  ✅ Python generated: {len(python_code)} chars")

        # Verify Python code has array
        if "[10, 20, 30]" in python_code or "[10,20,30]" in python_code:
            print(f"\n✅ SUCCESS: Array generates correct Python!")
            print(f"\nGenerated Python:\n{python_code}")
            return True
        else:
            print(f"\n❌ FAILED: Generated Python doesn't have array literal")
            print(f"Generated:\n{python_code}")
            return False

    except Exception as e:
        print(f"\n❌ FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_array_multi_line():
    """Test multi-line array literal."""
    print(f"\n{'='*60}")
    print("Testing multi-line array literal")
    print(f"{'='*60}")

    pw_code = """function create_list() -> array {
    let items = [
        1,
        2,
        3,
        4,
        5
    ];
    return items;
}"""

    try:
        ir = parse_pw(pw_code)
        print(f"  ✅ Parser: {len(ir.functions)} functions")
        print(f"\n✅ SUCCESS: Multi-line array works!")
        return True

    except Exception as e:
        print(f"\n❌ FAILED: {e}")
        return False


def run_all_tests():
    """Run all array tests."""
    print("\n" + "="*60)
    print("PW PARSER ARRAY TESTS")
    print("="*60)

    tests = [
        ("Array literal", test_array_literal),
        ("Array indexing", test_array_indexing),
        ("Array element assignment", test_array_assignment),
        ("Array in for loop", test_array_in_for_loop),
        ("Nested arrays", test_nested_arrays),
        ("Arrays with different types", test_array_different_types),
        ("Empty array", test_empty_array),
        ("Array code generation", test_array_code_generation),
        ("Multi-line array", test_array_multi_line),
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

    return results


if __name__ == "__main__":
    results = run_all_tests()
    all_passed = all(success for _, success in results)
    sys.exit(0 if all_passed else 1)
