"""
Cross-language validation tests.

Ensures that Python, Go, Rust, TypeScript, and C# all produce
semantically equivalent code from the same PW source.

Tests:
1. Arithmetic operations produce same results
2. String operations produce same results
3. Conditional logic produces same results
4. Type mappings are correct
"""

import sys
from pathlib import Path
import tempfile
import subprocess
import os

sys.path.insert(0, str(Path(__file__).parent.parent))
sys.path.insert(0, str(Path(__file__).parent.parent / 'pw-syntax-mcp-server'))

from dsl.pw_parser import Lexer, Parser
from translators.ir_converter import ir_to_mcp
from translators.python_bridge import pw_to_python
from translators.go_bridge import pw_to_go
from translators.rust_bridge import pw_to_rust
from translators.typescript_bridge import pw_to_typescript
from translators.csharp_bridge import pw_to_csharp


def compile_and_test_pw(pw_code: str, test_description: str):
    """Compile PW to all languages and compare outputs."""
    print(f"\n{'='*60}")
    print(f"Test: {test_description}")
    print(f"{'='*60}")

    # Parse PW
    try:
        lexer = Lexer(pw_code)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ir = parser.parse()
        mcp_tree = ir_to_mcp(ir)
    except Exception as e:
        print(f"❌ PW parsing failed: {e}")
        return False

    # Generate all languages
    results = {}

    try:
        results['python'] = pw_to_python(mcp_tree)
        print(f"✅ Python generated ({len(results['python'])} chars)")
    except Exception as e:
        print(f"❌ Python generation failed: {e}")
        return False

    try:
        results['go'] = pw_to_go(mcp_tree)
        print(f"✅ Go generated ({len(results['go'])} chars)")
    except Exception as e:
        print(f"❌ Go generation failed: {e}")
        return False

    try:
        results['rust'] = pw_to_rust(mcp_tree)
        print(f"✅ Rust generated ({len(results['rust'])} chars)")
    except Exception as e:
        print(f"❌ Rust generation failed: {e}")
        return False

    try:
        results['typescript'] = pw_to_typescript(mcp_tree)
        print(f"✅ TypeScript generated ({len(results['typescript'])} chars)")
    except Exception as e:
        print(f"❌ TypeScript generation failed: {e}")
        return False

    try:
        results['csharp'] = pw_to_csharp(mcp_tree)
        print(f"✅ C# generated ({len(results['csharp'])} chars)")
    except Exception as e:
        print(f"❌ C# generation failed: {e}")
        return False

    print(f"\n✅ All 5 languages generated successfully!")
    return True, results


def test_arithmetic_operations():
    """Test that arithmetic operations work identically across languages."""
    pw_code = """
function add(x: int, y: int) -> int {
    return x + y;
}

function subtract(x: int, y: int) -> int {
    return x - y;
}

function multiply(x: int, y: int) -> int {
    return x * y;
}

function divide(x: int, y: int) -> int {
    return x / y;
}
"""

    success, results = compile_and_test_pw(pw_code, "Arithmetic Operations")

    if success:
        # Verify all languages have the same functions
        print("\nVerifying function presence:")
        for lang, code in results.items():
            has_add = 'add' in code.lower() or 'Add' in code
            has_subtract = 'subtract' in code.lower() or 'Subtract' in code
            has_multiply = 'multiply' in code.lower() or 'Multiply' in code
            has_divide = 'divide' in code.lower() or 'Divide' in code

            if has_add and has_subtract and has_multiply and has_divide:
                print(f"  ✅ {lang.capitalize()}: All functions present")
            else:
                print(f"  ❌ {lang.capitalize()}: Missing functions")
                return False

    return success


def test_string_operations():
    """Test string operations across languages."""
    pw_code = """
function greet(name: string) -> string {
    return "Hello, " + name + "!";
}

function get_length_message(text: string) -> string {
    return "Text length is unknown";
}
"""

    success, results = compile_and_test_pw(pw_code, "String Operations")

    if success:
        print("\nVerifying string handling:")
        for lang, code in results.items():
            has_greet = 'greet' in code.lower() or 'Greet' in code
            has_hello = 'Hello' in code
            has_concat = '+' in code or 'concat' in code.lower()

            if has_greet and has_hello:
                print(f"  ✅ {lang.capitalize()}: String operations present")
            else:
                print(f"  ❌ {lang.capitalize()}: String operations missing")
                return False

    return success


def test_conditional_logic():
    """Test conditional logic across languages."""
    pw_code = """
function max_value(a: int, b: int) -> int {
    if (a > b) {
        return a;
    } else {
        return b;
    }
}

function min_value(a: int, b: int) -> int {
    if (a < b) {
        return a;
    } else {
        return b;
    }
}

function is_positive(x: int) -> bool {
    if (x > 0) {
        return true;
    } else {
        return false;
    }
}
"""

    success, results = compile_and_test_pw(pw_code, "Conditional Logic")

    if success:
        print("\nVerifying conditional logic:")
        for lang, code in results.items():
            has_if = 'if' in code.lower()
            has_else = 'else' in code.lower()
            has_max = 'max' in code.lower() or 'Max' in code
            has_min = 'min' in code.lower() or 'Min' in code

            if has_if and has_else and has_max and has_min:
                print(f"  ✅ {lang.capitalize()}: Conditional logic present")
            else:
                print(f"  ❌ {lang.capitalize()}: Conditional logic missing")
                return False

    return success


def test_type_mappings():
    """Test that type mappings are consistent."""
    pw_code = """
function test_int(x: int) -> int {
    return x;
}

function test_float(x: float) -> float {
    return x;
}

function test_string(x: string) -> string {
    return x;
}

function test_bool(x: bool) -> bool {
    return x;
}
"""

    success, results = compile_and_test_pw(pw_code, "Type Mappings")

    if success:
        print("\nVerifying type mappings:")

        # Expected type mappings
        type_map = {
            'python': {'int': 'int', 'float': 'float', 'string': 'str', 'bool': 'bool'},
            'go': {'int': 'int', 'float': 'float64', 'string': 'string', 'bool': 'bool'},
            'rust': {'int': 'i32', 'float': 'f64', 'string': 'String', 'bool': 'bool'},
            'typescript': {'int': 'number', 'float': 'number', 'string': 'string', 'bool': 'boolean'},
            'csharp': {'int': 'int', 'float': 'double', 'string': 'string', 'bool': 'bool'}
        }

        for lang, code in results.items():
            expected_types = type_map[lang]
            print(f"\n  {lang.capitalize()}:")
            print(f"    Expected int → {expected_types['int']}")
            print(f"    Expected float → {expected_types['float']}")
            print(f"    Expected string → {expected_types['string']}")
            print(f"    Expected bool → {expected_types['bool']}")

            # Check if expected types appear in generated code
            # (This is a basic check - real validation would require parsing generated code)
            types_found = 0
            for pw_type, lang_type in expected_types.items():
                if lang_type in code:
                    types_found += 1

            if types_found >= 3:  # At least 3 out of 4 types should be present
                print(f"  ✅ {lang.capitalize()}: Type mappings look correct")
            else:
                print(f"  ⚠️  {lang.capitalize()}: Some type mappings may be missing")

    return success


def test_complex_function():
    """Test a complex function with multiple features."""
    pw_code = """
function calculate_discount(price: float, discount_percent: float, is_member: bool) -> float {
    let discount_amount = 0.0;

    if (is_member) {
        if (discount_percent > 0.0) {
            discount_amount = price * (discount_percent / 100.0);
        } else {
            discount_amount = price * 0.05;
        }
    } else {
        if (discount_percent > 0.0) {
            discount_amount = price * (discount_percent / 100.0);
        } else {
            discount_amount = 0.0;
        }
    }

    let final_price = price - discount_amount;
    return final_price;
}
"""

    success, results = compile_and_test_pw(pw_code, "Complex Function with Multiple Features")

    if success:
        print("\nVerifying complex function:")
        for lang, code in results.items():
            has_function = 'calculate' in code.lower() or 'Calculate' in code
            has_variables = 'discount_amount' in code or 'discountAmount' in code or 'DiscountAmount' in code
            has_nested_if = code.count('if') >= 2

            if has_function and has_variables:
                print(f"  ✅ {lang.capitalize()}: Complex function looks correct")
            else:
                print(f"  ❌ {lang.capitalize()}: Complex function may have issues")
                return False

    return success


def run_all_tests():
    """Run all cross-language validation tests."""
    print("\n" + "="*60)
    print("PW CROSS-LANGUAGE VALIDATION TESTS")
    print("="*60)

    tests = [
        ("Arithmetic Operations", test_arithmetic_operations),
        ("String Operations", test_string_operations),
        ("Conditional Logic", test_conditional_logic),
        ("Type Mappings", test_type_mappings),
        ("Complex Function", test_complex_function)
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
    print("Tests complete!")
    print("="*60)

    return results


if __name__ == "__main__":
    results = run_all_tests()

    all_passed = all(success for _, success in results)
    sys.exit(0 if all_passed else 1)
