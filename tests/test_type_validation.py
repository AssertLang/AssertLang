"""
PW Parser Type Validation Tests

Tests that the parser correctly validates:
1. Return types match declarations
2. Type mismatches are caught
3. Missing return types are rejected
4. Type inference works for 'let' statements
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
sys.path.insert(0, str(Path(__file__).parent.parent / 'pw-syntax-mcp-server'))

from dsl.pw_parser import parse_pw


def test_type_mismatch_string_to_int():
    """Should FAIL - returning string when int expected."""
    print(f"\n{'='*60}")
    print("Test: Type mismatch - string to int")
    print(f"{'='*60}")

    pw_code = '''
function bad() -> int {
    return "string";
}
'''

    try:
        ir = parse_pw(pw_code)

        print(f"  ❌ SHOULD HAVE FAILED - accepted string as int")
        return False
    except Exception as e:
        if "type" in str(e).lower() or "mismatch" in str(e).lower():
            print(f"  ✅ Correctly rejected: {type(e).__name__}: {e}")
            return True
        else:
            print(f"  ⚠️  Failed but wrong error: {type(e).__name__}: {e}")
            return False


def test_type_mismatch_int_to_string():
    """Should FAIL - returning int when string expected."""
    print(f"\n{'='*60}")
    print("Test: Type mismatch - int to string")
    print(f"{'='*60}")

    pw_code = '''
function bad() -> string {
    return 42;
}
'''

    try:
        ir = parse_pw(pw_code)

        print(f"  ❌ SHOULD HAVE FAILED - accepted int as string")
        return False
    except Exception as e:
        if "type" in str(e).lower() or "mismatch" in str(e).lower():
            print(f"  ✅ Correctly rejected: {type(e).__name__}: {e}")
            return True
        else:
            print(f"  ⚠️  Failed but wrong error: {type(e).__name__}: {e}")
            return False


def test_missing_return_type():
    """Should FAIL - function missing return type."""
    print(f"\n{'='*60}")
    print("Test: Missing return type")
    print(f"{'='*60}")

    pw_code = '''
function bad(x: int) {
    return x;
}
'''

    try:
        ir = parse_pw(pw_code)

        print(f"  ❌ SHOULD HAVE FAILED - accepted missing return type")
        return False
    except Exception as e:
        if "return type" in str(e).lower() or "expected" in str(e).lower():
            print(f"  ✅ Correctly rejected: {type(e).__name__}: {e}")
            return True
        else:
            print(f"  ⚠️  Failed but wrong error: {type(e).__name__}: {e}")
            return False


def test_correct_type_int():
    """Should PASS - correct int return type."""
    print(f"\n{'='*60}")
    print("Test: Correct int return type")
    print(f"{'='*60}")

    pw_code = '''
function good() -> int {
    return 42;
}
'''

    try:
        ir = parse_pw(pw_code)

        print(f"  ✅ Correctly accepted int return")
        return True
    except Exception as e:
        print(f"  ❌ Should have passed: {type(e).__name__}: {e}")
        return False


def test_correct_type_string():
    """Should PASS - correct string return type."""
    print(f"\n{'='*60}")
    print("Test: Correct string return type")
    print(f"{'='*60}")

    pw_code = '''
function good() -> string {
    return "hello";
}
'''

    try:
        ir = parse_pw(pw_code)

        print(f"  ✅ Correctly accepted string return")
        return True
    except Exception as e:
        print(f"  ❌ Should have passed: {type(e).__name__}: {e}")
        return False


def test_correct_type_float():
    """Should PASS - correct float return type."""
    print(f"\n{'='*60}")
    print("Test: Correct float return type")
    print(f"{'='*60}")

    pw_code = '''
function good() -> float {
    return 3.14;
}
'''

    try:
        ir = parse_pw(pw_code)

        print(f"  ✅ Correctly accepted float return")
        return True
    except Exception as e:
        print(f"  ❌ Should have passed: {type(e).__name__}: {e}")
        return False


def test_correct_type_bool():
    """Should PASS - correct bool return type."""
    print(f"\n{'='*60}")
    print("Test: Correct bool return type")
    print(f"{'='*60}")

    pw_code = '''
function good() -> bool {
    return true;
}
'''

    try:
        ir = parse_pw(pw_code)

        print(f"  ✅ Correctly accepted bool return")
        return True
    except Exception as e:
        print(f"  ❌ Should have passed: {type(e).__name__}: {e}")
        return False


def test_type_inference_let_int():
    """Should PASS - infer int type for let statement."""
    print(f"\n{'='*60}")
    print("Test: Type inference - let x = 42 (int)")
    print(f"{'='*60}")

    pw_code = '''
function good() -> int {
    let x = 42;
    return x;
}
'''

    try:
        ir = parse_pw(pw_code)

        print(f"  ✅ Correctly inferred int type")
        return True
    except Exception as e:
        print(f"  ❌ Should have passed: {type(e).__name__}: {e}")
        return False


def test_type_inference_let_string():
    """Should PASS - infer string type for let statement."""
    print(f"\n{'='*60}")
    print("Test: Type inference - let x = \"hello\" (string)")
    print(f"{'='*60}")

    pw_code = '''
function good() -> string {
    let x = "hello";
    return x;
}
'''

    try:
        ir = parse_pw(pw_code)

        print(f"  ✅ Correctly inferred string type")
        return True
    except Exception as e:
        print(f"  ❌ Should have passed: {type(e).__name__}: {e}")
        return False


def test_type_inference_mismatch():
    """Should FAIL - inferred type doesn't match return type."""
    print(f"\n{'='*60}")
    print("Test: Type inference mismatch")
    print(f"{'='*60}")

    pw_code = '''
function bad() -> string {
    let x = 42;
    return x;
}
'''

    try:
        ir = parse_pw(pw_code)

        print(f"  ❌ SHOULD HAVE FAILED - returned int when string expected")
        return False
    except Exception as e:
        if "type" in str(e).lower() or "mismatch" in str(e).lower():
            print(f"  ✅ Correctly rejected: {type(e).__name__}: {e}")
            return True
        else:
            print(f"  ⚠️  Failed but wrong error: {type(e).__name__}: {e}")
            return False


def test_binary_op_type_checking():
    """Should PASS - binary operations preserve types."""
    print(f"\n{'='*60}")
    print("Test: Binary operation type checking")
    print(f"{'='*60}")

    pw_code = '''
function good(a: int, b: int) -> int {
    return a + b;
}
'''

    try:
        ir = parse_pw(pw_code)

        print(f"  ✅ Correctly validated binary operation types")
        return True
    except Exception as e:
        print(f"  ❌ Should have passed: {type(e).__name__}: {e}")
        return False


def test_binary_op_type_mismatch():
    """Should FAIL - binary operation with mismatched types."""
    print(f"\n{'='*60}")
    print("Test: Binary operation type mismatch")
    print(f"{'='*60}")

    pw_code = '''
function bad(a: int, b: string) -> int {
    return a + b;
}
'''

    try:
        ir = parse_pw(pw_code)

        print(f"  ❌ SHOULD HAVE FAILED - added int + string")
        return False
    except Exception as e:
        if "type" in str(e).lower() or "mismatch" in str(e).lower():
            print(f"  ✅ Correctly rejected: {type(e).__name__}: {e}")
            return True
        else:
            print(f"  ⚠️  Failed but wrong error: {type(e).__name__}: {e}")
            return False


def test_conditional_type_checking():
    """Should PASS - conditionals with correct types."""
    print(f"\n{'='*60}")
    print("Test: Conditional type checking")
    print(f"{'='*60}")

    pw_code = '''
function good(x: int) -> int {
    if (x > 0) {
        return x;
    } else {
        return 0;
    }
}
'''

    try:
        ir = parse_pw(pw_code)

        print(f"  ✅ Correctly validated conditional types")
        return True
    except Exception as e:
        print(f"  ❌ Should have passed: {type(e).__name__}: {e}")
        return False


def test_conditional_return_type_mismatch():
    """Should FAIL - conditional branches return different types."""
    print(f"\n{'='*60}")
    print("Test: Conditional return type mismatch")
    print(f"{'='*60}")

    pw_code = '''
function bad(x: int) -> int {
    if (x > 0) {
        return x;
    } else {
        return "zero";
    }
}
'''

    try:
        ir = parse_pw(pw_code)

        print(f"  ❌ SHOULD HAVE FAILED - else returns string when int expected")
        return False
    except Exception as e:
        if "type" in str(e).lower() or "mismatch" in str(e).lower():
            print(f"  ✅ Correctly rejected: {type(e).__name__}: {e}")
            return True
        else:
            print(f"  ⚠️  Failed but wrong error: {type(e).__name__}: {e}")
            return False


def test_string_concatenation():
    """Should PASS - string concatenation with + operator."""
    print(f"\n{'='*60}")
    print("Test: String concatenation")
    print(f"{'='*60}")

    pw_code = '''
function good(a: string, b: string) -> string {
    return a + b;
}
'''

    try:
        ir = parse_pw(pw_code)

        print(f"  ✅ Correctly accepted string concatenation")
        return True
    except Exception as e:
        print(f"  ❌ Should have passed: {type(e).__name__}: {e}")
        return False


def test_comparison_returns_bool():
    """Should PASS - comparison operations return bool."""
    print(f"\n{'='*60}")
    print("Test: Comparison returns bool")
    print(f"{'='*60}")

    pw_code = '''
function good(a: int, b: int) -> bool {
    return a < b;
}
'''

    try:
        ir = parse_pw(pw_code)

        print(f"  ✅ Correctly validated comparison returns bool")
        return True
    except Exception as e:
        print(f"  ❌ Should have passed: {type(e).__name__}: {e}")
        return False


def test_int_float_compatibility():
    """Should PASS - int can be used where float expected."""
    print(f"\n{'='*60}")
    print("Test: Int to float compatibility")
    print(f"{'='*60}")

    pw_code = '''
function good() -> float {
    return 42;
}
'''

    try:
        ir = parse_pw(pw_code)

        print(f"  ✅ Correctly accepted int as float")
        return True
    except Exception as e:
        print(f"  ❌ Should have passed (int compatible with float): {type(e).__name__}: {e}")
        return False


def test_function_call_type_checking():
    """Should PASS - function call with correct argument types."""
    print(f"\n{'='*60}")
    print("Test: Function call type checking")
    print(f"{'='*60}")

    pw_code = '''
function add(x: int, y: int) -> int {
    return x + y;
}

function caller() -> int {
    return add(1, 2);
}
'''

    try:
        ir = parse_pw(pw_code)

        print(f"  ✅ Correctly validated function call types")
        return True
    except Exception as e:
        print(f"  ❌ Should have passed: {type(e).__name__}: {e}")
        return False


def test_function_call_arg_type_mismatch():
    """Should FAIL - function call with wrong argument type."""
    print(f"\n{'='*60}")
    print("Test: Function call argument type mismatch")
    print(f"{'='*60}")

    pw_code = '''
function add(x: int, y: int) -> int {
    return x + y;
}

function bad() -> int {
    return add(1, "two");
}
'''

    try:
        ir = parse_pw(pw_code)

        print(f"  ❌ SHOULD HAVE FAILED - passed string to int parameter")
        return False
    except Exception as e:
        if "type" in str(e).lower() or "argument" in str(e).lower():
            print(f"  ✅ Correctly rejected: {type(e).__name__}: {e}")
            return True
        else:
            print(f"  ⚠️  Failed but wrong error: {type(e).__name__}: {e}")
            return False


def test_void_function():
    """Should PASS - function with no return type (void)."""
    print(f"\n{'='*60}")
    print("Test: Void function (no return)")
    print(f"{'='*60}")

    pw_code = '''
function print_hello() -> void {
    let x = 1;
}
'''

    try:
        ir = parse_pw(pw_code)

        print(f"  ✅ Correctly accepted void function")
        return True
    except Exception as e:
        print(f"  ❌ Should have passed: {type(e).__name__}: {e}")
        return False


def run_all_tests():
    """Run all type validation tests."""
    print("\n" + "="*60)
    print("PW PARSER TYPE VALIDATION TESTS")
    print("="*60)

    tests = [
        ("Type mismatch - string to int", test_type_mismatch_string_to_int),
        ("Type mismatch - int to string", test_type_mismatch_int_to_string),
        ("Missing return type", test_missing_return_type),
        ("Correct int return", test_correct_type_int),
        ("Correct string return", test_correct_type_string),
        ("Correct float return", test_correct_type_float),
        ("Correct bool return", test_correct_type_bool),
        ("Type inference - let int", test_type_inference_let_int),
        ("Type inference - let string", test_type_inference_let_string),
        ("Type inference mismatch", test_type_inference_mismatch),
        ("Binary operation type checking", test_binary_op_type_checking),
        ("Binary operation type mismatch", test_binary_op_type_mismatch),
        ("Conditional type checking", test_conditional_type_checking),
        ("Conditional return type mismatch", test_conditional_return_type_mismatch),
        ("String concatenation", test_string_concatenation),
        ("Comparison returns bool", test_comparison_returns_bool),
        ("Int to float compatibility", test_int_float_compatibility),
        ("Function call type checking", test_function_call_type_checking),
        ("Function call arg type mismatch", test_function_call_arg_type_mismatch),
        ("Void function", test_void_function),
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
