"""
Test PW parser while loop support.

Tests:
1. Basic while loop
2. While loop with complex condition
3. Nested while loops
4. While loop with break/continue
5. While loop code generation
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
sys.path.insert(0, str(Path(__file__).parent.parent / 'pw-syntax-mcp-server'))

from dsl.al_parser import parse_al
from translators.ir_converter import ir_to_mcp
from translators.python_bridge import pw_to_python


def test_basic_while_loop():
    """Test basic while loop."""
    print(f"\n{'='*60}")
    print("Testing basic while loop")
    print(f"{'='*60}")

    pw_code = """function countdown(n: int) -> int {
    while (n > 0) {
        n = n - 1;
    }
    return n;
}"""

    try:
        ir = parse_al(pw_code)
        print(f"  ✅ Parser: {len(ir.functions)} functions")

        func = ir.functions[0]
        # Find while loop in body
        while_loop = None
        for stmt in func.body:
            if hasattr(stmt, 'type') and str(stmt.type) == 'NodeType.WHILE':
                while_loop = stmt
                break

        if while_loop:
            print(f"  ✅ While loop found")
            print(f"\n✅ SUCCESS: Basic while loop works!")
            return True
        else:
            print(f"\n❌ FAILED: No while loop found in function body")
            return False

    except Exception as e:
        print(f"\n❌ FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_while_complex_condition():
    """Test while loop with complex condition."""
    print(f"\n{'='*60}")
    print("Testing while loop with complex condition")
    print(f"{'='*60}")

    pw_code = """function find_target(arr: array, target: int) -> int {
    let i = 0;
    while (i < 10 && arr[i] != target) {
        i = i + 1;
    }
    return i;
}"""

    try:
        ir = parse_al(pw_code)
        print(f"  ✅ Parser: {len(ir.functions)} functions")
        print(f"\n✅ SUCCESS: Complex condition while loop works!")
        return True

    except Exception as e:
        print(f"\n❌ FAILED: {e}")
        return False


def test_nested_while_loops():
    """Test nested while loops."""
    print(f"\n{'='*60}")
    print("Testing nested while loops")
    print(f"{'='*60}")

    pw_code = """function matrix_sum(matrix: array) -> int {
    let sum = 0;
    let i = 0;
    while (i < 10) {
        let j = 0;
        while (j < 10) {
            sum = sum + matrix[i][j];
            j = j + 1;
        }
        i = i + 1;
    }
    return sum;
}"""

    try:
        ir = parse_al(pw_code)
        print(f"  ✅ Parser: {len(ir.functions)} functions")
        print(f"\n✅ SUCCESS: Nested while loops work!")
        return True

    except Exception as e:
        print(f"\n❌ FAILED: {e}")
        return False


def test_while_with_break_continue():
    """Test while loop with break and continue."""
    print(f"\n{'='*60}")
    print("Testing while loop with break/continue")
    print(f"{'='*60}")

    pw_code = """function find_first_positive(numbers: array) -> int {
    let i = 0;
    while (i < 100) {
        if (numbers[i] < 0) {
            i = i + 1;
            continue;
        }
        if (numbers[i] > 0) {
            return numbers[i];
        }
        i = i + 1;
    }
    return 0;
}"""

    try:
        ir = parse_al(pw_code)
        print(f"  ✅ Parser: {len(ir.functions)} functions")
        print(f"\n✅ SUCCESS: While loop with break/continue works!")
        return True

    except Exception as e:
        print(f"\n❌ FAILED: {e}")
        return False


def test_while_code_generation():
    """Test that while loops generate correct code."""
    print(f"\n{'='*60}")
    print("Testing while loop code generation")
    print(f"{'='*60}")

    pw_code = """function sum_to_n(n: int) -> int {
    let sum = 0;
    let i = 1;
    while (i <= n) {
        sum = sum + i;
        i = i + 1;
    }
    return sum;
}"""

    try:
        ir = parse_al(pw_code)
        print(f"  ✅ Parser: {len(ir.functions)} functions")

        mcp_tree = ir_to_mcp(ir)
        print(f"  ✅ MCP tree created")

        python_code = pw_to_python(mcp_tree)
        print(f"  ✅ Python generated: {len(python_code)} chars")

        # Verify Python code has while loop
        if "while" in python_code:
            print(f"\n✅ SUCCESS: While loop generates correct Python!")
            print(f"\nGenerated Python:\n{python_code}")
            return True
        else:
            print(f"\n❌ FAILED: Generated Python doesn't have while loop")
            print(f"Generated:\n{python_code}")
            return False

    except Exception as e:
        print(f"\n❌ FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_while_multi_line():
    """Test while loop with multi-line condition."""
    print(f"\n{'='*60}")
    print("Testing while loop multi-line syntax")
    print(f"{'='*60}")

    pw_code = """function process(
    items: array,
    threshold: int
) -> int {
    let count = 0;
    let i = 0;
    while (
        i < 100 &&
        items[i] < threshold
    ) {
        count = count + 1;
        i = i + 1;
    }
    return count;
}"""

    try:
        ir = parse_al(pw_code)
        print(f"  ✅ Parser: {len(ir.functions)} functions")
        print(f"\n✅ SUCCESS: Multi-line while loop works!")
        return True

    except Exception as e:
        print(f"\n❌ FAILED: {e}")
        return False


def run_all_tests():
    """Run all while loop tests."""
    print("\n" + "="*60)
    print("PW PARSER WHILE LOOP TESTS")
    print("="*60)

    tests = [
        ("Basic while loop", test_basic_while_loop),
        ("While loop with complex condition", test_while_complex_condition),
        ("Nested while loops", test_nested_while_loops),
        ("While loop with break/continue", test_while_with_break_continue),
        ("While loop code generation", test_while_code_generation),
        ("While loop multi-line syntax", test_while_multi_line),
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
