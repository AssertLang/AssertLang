"""
Test PW parser numeric handling.

Tests:
1. Large integers
2. Small floats
3. Negative numbers
4. Zero variations
5. Numeric operations
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
sys.path.insert(0, str(Path(__file__).parent.parent / 'pw-syntax-mcp-server'))

from dsl.al_parser import Lexer, Parser
from translators.ir_converter import ir_to_mcp
from translators.python_bridge import pw_to_python


def test_large_integers():
    """Test very large integers."""
    print(f"\n{'='*60}")
    print("Testing large integers")
    print(f"{'='*60}")

    pw_code = '''
function large_int() -> int {
    return 999999999;
}

function very_large() -> int {
    return 123456789012345;
}
'''

    try:
        lexer = Lexer(pw_code)
        tokens = lexer.tokenize()
        print(f"  ✅ Lexer: {len(tokens)} tokens")

        parser = Parser(tokens)
        ir = parser.parse()
        print(f"  ✅ Parser: {len(ir.functions)} functions")

        mcp_tree = ir_to_mcp(ir)
        python_code = pw_to_python(mcp_tree)
        print(f"  ✅ Python: generated")

        print(f"\n✅ SUCCESS: Large integers work!")
        return True

    except Exception as e:
        print(f"\n❌ FAILED: {e}")
        return False


def test_floats():
    """Test floating point numbers."""
    print(f"\n{'='*60}")
    print("Testing floating point numbers")
    print(f"{'='*60}")

    pw_code = '''
function small_float() -> float {
    return 0.001;
}

function precise_float() -> float {
    return 3.14159265359;
}

function large_float() -> float {
    return 9999.9999;
}
'''

    try:
        lexer = Lexer(pw_code)
        tokens = lexer.tokenize()
        print(f"  ✅ Lexer: {len(tokens)} tokens")

        parser = Parser(tokens)
        ir = parser.parse()
        print(f"  ✅ Parser: {len(ir.functions)} functions")

        mcp_tree = ir_to_mcp(ir)
        python_code = pw_to_python(mcp_tree)
        print(f"  ✅ Python: generated")

        print(f"\n✅ SUCCESS: Floats work!")
        return True

    except Exception as e:
        print(f"\n❌ FAILED: {e}")
        return False


def test_negative_numbers():
    """Test negative numbers."""
    print(f"\n{'='*60}")
    print("Testing negative numbers")
    print(f"{'='*60}")

    pw_code = '''
function neg_int() -> int {
    return -42;
}

function neg_float() -> float {
    return -3.14;
}

function neg_math(x: int) -> int {
    return -x;
}
'''

    try:
        lexer = Lexer(pw_code)
        tokens = lexer.tokenize()
        print(f"  ✅ Lexer: {len(tokens)} tokens")

        parser = Parser(tokens)
        ir = parser.parse()
        print(f"  ✅ Parser: {len(ir.functions)} functions")

        mcp_tree = ir_to_mcp(ir)
        python_code = pw_to_python(mcp_tree)
        print(f"  ✅ Python: generated")

        print(f"\n✅ SUCCESS: Negative numbers work!")
        return True

    except Exception as e:
        print(f"\n❌ FAILED: {e}")
        return False


def test_zero_variations():
    """Test different representations of zero."""
    print(f"\n{'='*60}")
    print("Testing zero variations")
    print(f"{'='*60}")

    pw_code = '''
function int_zero() -> int {
    return 0;
}

function float_zero() -> float {
    return 0.0;
}

function float_zero2() -> float {
    return 0.00000;
}
'''

    try:
        lexer = Lexer(pw_code)
        tokens = lexer.tokenize()
        print(f"  ✅ Lexer: {len(tokens)} tokens")

        parser = Parser(tokens)
        ir = parser.parse()
        print(f"  ✅ Parser: {len(ir.functions)} functions")

        mcp_tree = ir_to_mcp(ir)
        python_code = pw_to_python(mcp_tree)
        print(f"  ✅ Python: generated")

        print(f"\n✅ SUCCESS: Zero variations work!")
        return True

    except Exception as e:
        print(f"\n❌ FAILED: {e}")
        return False


def test_arithmetic_operations():
    """Test arithmetic with various numbers."""
    print(f"\n{'='*60}")
    print("Testing arithmetic operations")
    print(f"{'='*60}")

    pw_code = '''
function add_nums() -> float {
    return 1.5 + 2.5;
}

function multiply_big() -> int {
    return 1000 * 1000;
}

function divide_precise() -> float {
    return 22.0 / 7.0;
}

function mixed_ops() -> float {
    return 10.0 * 2.5 + 5.0 / 2.0;
}
'''

    try:
        lexer = Lexer(pw_code)
        tokens = lexer.tokenize()
        print(f"  ✅ Lexer: {len(tokens)} tokens")

        parser = Parser(tokens)
        ir = parser.parse()
        print(f"  ✅ Parser: {len(ir.functions)} functions")

        mcp_tree = ir_to_mcp(ir)
        python_code = pw_to_python(mcp_tree)
        print(f"  ✅ Python: generated")

        print(f"\n✅ SUCCESS: Arithmetic operations work!")
        return True

    except Exception as e:
        print(f"\n❌ FAILED: {e}")
        return False


def run_all_tests():
    """Run all numeric tests."""
    print("\n" + "="*60)
    print("PW PARSER NUMERIC HANDLING TESTS")
    print("="*60)

    tests = [
        ("Large Integers", test_large_integers),
        ("Floating Point Numbers", test_floats),
        ("Negative Numbers", test_negative_numbers),
        ("Zero Variations", test_zero_variations),
        ("Arithmetic Operations", test_arithmetic_operations)
    ]

    results = []
    for test_name, test_func in tests:
        try:
            success = test_func()
            results.append((test_name, success))
        except Exception as e:
            print(f"\n❌ Test '{test_name}' crashed: {e}")
            results.append((test_name, False))

    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)

    passed = sum(1 for _, success in results if success)
    total = len(results)

    print(f"\nTotal: {passed}/{total} tests passed")

    for test_name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"  {status}: {test_name}")

    print("\n" + "="*60)

    return results


if __name__ == "__main__":
    results = run_all_tests()
    all_passed = all(success for _, success in results)
    sys.exit(0 if all_passed else 1)
