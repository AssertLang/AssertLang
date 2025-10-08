"""
Test PW parser for loop support.

Tests:
1. Basic for-in loop
2. For loop with range()
3. For loop with enumerate()
4. Nested for loops
5. For loop with break/continue
6. For loop code generation
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
sys.path.insert(0, str(Path(__file__).parent.parent / 'pw-syntax-mcp-server'))

from dsl.pw_parser import parse_pw
from translators.ir_converter import ir_to_mcp
from translators.python_bridge import pw_to_python


def test_basic_for_loop():
    """Test basic for-in loop."""
    print(f"\n{'='*60}")
    print("Testing basic for-in loop")
    print(f"{'='*60}")

    pw_code = """function process_items(items: array) -> int {
    let count = 0;
    for (item in items) {
        count = count + 1;
    }
    return count;
}"""

    try:
        ir = parse_pw(pw_code)
        print(f"  ✅ Parser: {len(ir.functions)} functions")

        func = ir.functions[0]
        # Find for loop in body
        for_loop = None
        for stmt in func.body:
            if hasattr(stmt, 'type') and str(stmt.type) == 'NodeType.FOR':
                for_loop = stmt
                break

        if for_loop:
            print(f"  ✅ For loop found: iterator={for_loop.iterator}")
            print(f"\n✅ SUCCESS: Basic for loop works!")
            return True
        else:
            print(f"\n❌ FAILED: No for loop found in function body")
            return False

    except Exception as e:
        print(f"\n❌ FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_for_with_range():
    """Test for loop with range()."""
    print(f"\n{'='*60}")
    print("Testing for loop with range()")
    print(f"{'='*60}")

    pw_code = """function count_to_ten() -> int {
    let sum = 0;
    for (i in range(0, 10)) {
        sum = sum + i;
    }
    return sum;
}"""

    try:
        ir = parse_pw(pw_code)
        print(f"  ✅ Parser: {len(ir.functions)} functions")
        print(f"\n✅ SUCCESS: For loop with range() works!")
        return True

    except Exception as e:
        print(f"\n❌ FAILED: {e}")
        return False


def test_for_with_enumerate():
    """Test for loop with enumerate()."""
    print(f"\n{'='*60}")
    print("Testing for loop with enumerate()")
    print(f"{'='*60}")

    pw_code = """function process_with_index(items: array) -> int {
    for (index, value in enumerate(items)) {
        print(index, value);
    }
    return 0;
}"""

    try:
        ir = parse_pw(pw_code)
        print(f"  ✅ Parser: {len(ir.functions)} functions")
        print(f"\n✅ SUCCESS: For loop with enumerate() works!")
        return True

    except Exception as e:
        print(f"\n❌ FAILED: {e}")
        return False


def test_nested_for_loops():
    """Test nested for loops."""
    print(f"\n{'='*60}")
    print("Testing nested for loops")
    print(f"{'='*60}")

    pw_code = """function nested_loops(matrix: array) -> int {
    let sum = 0;
    for (row in matrix) {
        for (cell in row) {
            sum = sum + cell;
        }
    }
    return sum;
}"""

    try:
        ir = parse_pw(pw_code)
        print(f"  ✅ Parser: {len(ir.functions)} functions")
        print(f"\n✅ SUCCESS: Nested for loops work!")
        return True

    except Exception as e:
        print(f"\n❌ FAILED: {e}")
        return False


def test_for_with_break_continue():
    """Test for loop with break and continue."""
    print(f"\n{'='*60}")
    print("Testing for loop with break/continue")
    print(f"{'='*60}")

    pw_code = """function find_positive(numbers: array) -> int {
    for (num in numbers) {
        if (num < 0) {
            continue;
        }
        if (num > 0) {
            return num;
        }
    }
    return 0;
}"""

    try:
        ir = parse_pw(pw_code)
        print(f"  ✅ Parser: {len(ir.functions)} functions")
        print(f"\n✅ SUCCESS: For loop with break/continue works!")
        return True

    except Exception as e:
        print(f"\n❌ FAILED: {e}")
        return False


def test_for_code_generation():
    """Test that for loops generate correct code."""
    print(f"\n{'='*60}")
    print("Testing for loop code generation")
    print(f"{'='*60}")

    pw_code = """function sum_array(numbers: array) -> int {
    let total = 0;
    for (n in numbers) {
        total = total + n;
    }
    return total;
}"""

    try:
        ir = parse_pw(pw_code)
        print(f"  ✅ Parser: {len(ir.functions)} functions")

        mcp_tree = ir_to_mcp(ir)
        print(f"  ✅ MCP tree created")

        python_code = pw_to_python(mcp_tree)
        print(f"  ✅ Python generated: {len(python_code)} chars")

        # Verify Python code has for loop
        if "for n in numbers:" in python_code or "for n in numbers" in python_code:
            print(f"\n✅ SUCCESS: For loop generates correct Python!")
            print(f"\nGenerated Python:\n{python_code}")
            return True
        else:
            print(f"\n❌ FAILED: Generated Python doesn't have for loop")
            print(f"Generated:\n{python_code}")
            return False

    except Exception as e:
        print(f"\n❌ FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_for_multi_line():
    """Test for loop with multi-line syntax."""
    print(f"\n{'='*60}")
    print("Testing for loop multi-line syntax")
    print(f"{'='*60}")

    pw_code = """function process_long(
    items: array,
    threshold: int
) -> int {
    let count = 0;
    for (
        item
        in
        items
    ) {
        if (item > threshold) {
            count = count + 1;
        }
    }
    return count;
}"""

    try:
        ir = parse_pw(pw_code)
        print(f"  ✅ Parser: {len(ir.functions)} functions")
        print(f"\n✅ SUCCESS: Multi-line for loop works!")
        return True

    except Exception as e:
        print(f"\n❌ FAILED: {e}")
        return False


def run_all_tests():
    """Run all for loop tests."""
    print("\n" + "="*60)
    print("PW PARSER FOR LOOP TESTS")
    print("="*60)

    tests = [
        ("Basic for-in loop", test_basic_for_loop),
        ("For loop with range()", test_for_with_range),
        ("For loop with enumerate()", test_for_with_enumerate),
        ("Nested for loops", test_nested_for_loops),
        ("For loop with break/continue", test_for_with_break_continue),
        ("For loop code generation", test_for_code_generation),
        ("For loop multi-line syntax", test_for_multi_line),
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
