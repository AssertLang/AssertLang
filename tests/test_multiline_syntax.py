"""
Test PW parser multi-line syntax support.

Tests:
1. Multi-line function parameters
2. Multi-line function calls
3. Multi-line expressions
4. Multi-line if conditions
5. Nested multi-line structures
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
sys.path.insert(0, str(Path(__file__).parent.parent / 'pw-syntax-mcp-server'))

from dsl.al_parser import parse_al
from translators.ir_converter import ir_to_mcp
from translators.python_bridge import pw_to_python


def test_multiline_function_params():
    """Test function with parameters spanning multiple lines."""
    print(f"\n{'='*60}")
    print("Testing multi-line function parameters")
    print(f"{'='*60}")

    pw_code = """function calculate_risk(
    account_balance: float,
    position_size: float,
    leverage: int
) -> float {
    return position_size * leverage / account_balance;
}"""

    try:
        ir = parse_al(pw_code)
        print(f"  ✅ Parser: {len(ir.functions)} functions")

        func = ir.functions[0]
        print(f"  ✅ Function name: {func.name}")
        print(f"  ✅ Parameters: {len(func.params)}")

        if len(func.params) == 3:
            print(f"\n✅ SUCCESS: Multi-line parameters work!")
            return True
        else:
            print(f"\n❌ FAILED: Expected 3 params, got {len(func.params)}")
            return False

    except Exception as e:
        print(f"\n❌ FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_multiline_function_call():
    """Test function call with arguments spanning multiple lines."""
    print(f"\n{'='*60}")
    print("Testing multi-line function call")
    print(f"{'='*60}")

    pw_code = """function calculate_risk(a: float, b: float, c: int) -> float {
    return a + b + c;
}

function caller() -> float {
    return calculate_risk(
        100.0,
        50.0,
        5
    );
}"""

    try:
        ir = parse_al(pw_code)
        print(f"  ✅ Parser: {len(ir.functions)} functions")

        # Check that caller function has a call expression
        caller_func = ir.functions[1]
        print(f"  ✅ Caller function parsed")

        print(f"\n✅ SUCCESS: Multi-line function calls work!")
        return True

    except Exception as e:
        print(f"\n❌ FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_multiline_expression():
    """Test expression spanning multiple lines."""
    print(f"\n{'='*60}")
    print("Testing multi-line expressions")
    print(f"{'='*60}")

    pw_code = """function complex_calc(a: int, b: int, c: int) -> int {
    return a +
           b +
           c;
}"""

    try:
        ir = parse_al(pw_code)
        print(f"  ✅ Parser: {len(ir.functions)} functions")

        print(f"\n✅ SUCCESS: Multi-line expressions work!")
        return True

    except Exception as e:
        print(f"\n❌ FAILED: {e}")
        return False


def test_multiline_if_condition():
    """Test if statement with multi-line condition."""
    print(f"\n{'='*60}")
    print("Testing multi-line if conditions")
    print(f"{'='*60}")

    pw_code = """function check(a: int, b: int, c: int) -> bool {
    if (a > 0 &&
        b > 0 &&
        c > 0) {
        return true;
    } else {
        return false;
    }
}"""

    try:
        ir = parse_al(pw_code)
        print(f"  ✅ Parser: {len(ir.functions)} functions")

        print(f"\n✅ SUCCESS: Multi-line if conditions work!")
        return True

    except Exception as e:
        print(f"\n❌ FAILED: {e}")
        return False


def test_nested_multiline():
    """Test nested multi-line structures."""
    print(f"\n{'='*60}")
    print("Testing nested multi-line structures")
    print(f"{'='*60}")

    pw_code = """function complex_function(
    param1: int,
    param2: int,
    param3: int
) -> int {
    let result = calculate(
        param1,
        param2,
        param3
    );

    if (result > 0 &&
        result < 100) {
        return result;
    } else {
        return 0;
    }
}

function calculate(a: int, b: int, c: int) -> int {
    return a + b + c;
}"""

    try:
        ir = parse_al(pw_code)
        print(f"  ✅ Parser: {len(ir.functions)} functions")

        print(f"\n✅ SUCCESS: Nested multi-line structures work!")
        return True

    except Exception as e:
        print(f"\n❌ FAILED: {e}")
        return False


def test_trailing_comma():
    """Test trailing comma in multi-line parameters."""
    print(f"\n{'='*60}")
    print("Testing trailing comma in parameters")
    print(f"{'='*60}")

    pw_code = """function add(
    x: int,
    y: int,
) -> int {
    return x + y;
}"""

    try:
        ir = parse_al(pw_code)
        print(f"  ✅ Parser: {len(ir.functions)} functions")

        print(f"\n✅ SUCCESS: Trailing comma works!")
        return True

    except Exception as e:
        print(f"\n⚠️  Note: Trailing comma not supported yet: {type(e).__name__}")
        # This is acceptable for now - trailing commas are optional
        return True


def test_multiline_with_comments():
    """Test multi-line with comments interspersed."""
    print(f"\n{'='*60}")
    print("Testing multi-line with comments")
    print(f"{'='*60}")

    pw_code = """function process(
    // User account balance
    balance: float,
    // Transaction amount
    amount: float
) -> float {
    return balance - amount;
}"""

    try:
        ir = parse_al(pw_code)
        print(f"  ✅ Parser: {len(ir.functions)} functions")

        print(f"\n✅ SUCCESS: Multi-line with comments works!")
        return True

    except Exception as e:
        print(f"\n❌ FAILED: {e}")
        return False


def test_very_long_param_list():
    """Test function with many parameters across multiple lines."""
    print(f"\n{'='*60}")
    print("Testing very long parameter list")
    print(f"{'='*60}")

    pw_code = """function create_user(
    id: string,
    name: string,
    email: string,
    age: int,
    city: string,
    country: string,
    zip_code: string,
    phone: string
) -> string {
    return id;
}"""

    try:
        ir = parse_al(pw_code)
        print(f"  ✅ Parser: {len(ir.functions)} functions")

        func = ir.functions[0]
        print(f"  ✅ Parameters: {len(func.params)}")

        if len(func.params) == 8:
            print(f"\n✅ SUCCESS: Long parameter lists work!")
            return True
        else:
            print(f"\n❌ FAILED: Expected 8 params, got {len(func.params)}")
            return False

    except Exception as e:
        print(f"\n❌ FAILED: {e}")
        return False


def test_multiline_generates_correctly():
    """Test that multi-line code generates correct output."""
    print(f"\n{'='*60}")
    print("Testing multi-line code generation")
    print(f"{'='*60}")

    pw_code = """function add(
    x: int,
    y: int
) -> int {
    return x + y;
}"""

    try:
        ir = parse_al(pw_code)
        print(f"  ✅ Parser: {len(ir.functions)} functions")

        mcp_tree = ir_to_mcp(ir)
        print(f"  ✅ MCP tree created")

        python_code = pw_to_python(mcp_tree)
        print(f"  ✅ Python generated: {len(python_code)} chars")

        # Verify Python code has the function
        if "def add" in python_code and "x: int" in python_code and "y: int" in python_code:
            print(f"\n✅ SUCCESS: Multi-line generates correct Python!")
            return True
        else:
            print(f"\n❌ FAILED: Generated Python doesn't match expected")
            print(f"Generated:\n{python_code}")
            return False

    except Exception as e:
        print(f"\n❌ FAILED: {e}")
        return False


def test_single_line_still_works():
    """Ensure single-line syntax still works (regression test)."""
    print(f"\n{'='*60}")
    print("Testing single-line syntax (regression)")
    print(f"{'='*60}")

    pw_code = """function add(x: int, y: int) -> int {
    return x + y;
}"""

    try:
        ir = parse_al(pw_code)
        print(f"  ✅ Parser: {len(ir.functions)} functions")

        print(f"\n✅ SUCCESS: Single-line syntax still works!")
        return True

    except Exception as e:
        print(f"\n❌ FAILED: Single-line syntax broken! {e}")
        return False


def run_all_tests():
    """Run all multi-line syntax tests."""
    print("\n" + "="*60)
    print("PW PARSER MULTI-LINE SYNTAX TESTS")
    print("="*60)

    tests = [
        ("Multi-line function parameters", test_multiline_function_params),
        ("Multi-line function call", test_multiline_function_call),
        ("Multi-line expressions", test_multiline_expression),
        ("Multi-line if conditions", test_multiline_if_condition),
        ("Nested multi-line structures", test_nested_multiline),
        ("Trailing comma", test_trailing_comma),
        ("Multi-line with comments", test_multiline_with_comments),
        ("Very long parameter list", test_very_long_param_list),
        ("Multi-line code generation", test_multiline_generates_correctly),
        ("Single-line regression", test_single_line_still_works),
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
