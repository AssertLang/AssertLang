"""
Test PW parser string handling.

Tests:
1. Empty strings
2. Very long strings
3. Strings with escape sequences
4. Strings with unicode
5. Strings with special characters
6. Single vs double quotes
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
sys.path.insert(0, str(Path(__file__).parent.parent / 'pw-syntax-mcp-server'))

from dsl.pw_parser import Lexer, Parser
from translators.ir_converter import ir_to_mcp
from translators.python_bridge import pw_to_python


def test_empty_strings():
    """Test empty strings."""
    print(f"\n{'='*60}")
    print("Testing empty strings")
    print(f"{'='*60}")

    pw_code = '''
function empty() -> string {
    return "";
}

function empty2() -> string {
    let x = "";
    return x;
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

        print(f"\n✅ SUCCESS: Empty strings work!")
        return True

    except Exception as e:
        print(f"\n❌ FAILED: {e}")
        return False


def test_long_strings():
    """Test very long strings."""
    print(f"\n{'='*60}")
    print("Testing very long strings")
    print(f"{'='*60}")

    # Generate a 1000-character string
    long_string = "a" * 1000

    pw_code = f'''function long_str() -> string {{
    return "{long_string}";
}}'''

    try:
        print(f"String length: {len(long_string)} chars")

        lexer = Lexer(pw_code)
        tokens = lexer.tokenize()
        print(f"  ✅ Lexer: {len(tokens)} tokens")

        parser = Parser(tokens)
        ir = parser.parse()
        print(f"  ✅ Parser: {len(ir.functions)} functions")

        mcp_tree = ir_to_mcp(ir)
        python_code = pw_to_python(mcp_tree)
        print(f"  ✅ Python: generated")

        print(f"\n✅ SUCCESS: 1000-char string works!")
        return True

    except Exception as e:
        print(f"\n❌ FAILED: {e}")
        return False


def test_escape_sequences():
    """Test strings with escape sequences."""
    print(f"\n{'='*60}")
    print("Testing escape sequences")
    print(f"{'='*60}")

    pw_code = r'''
function escapes() -> string {
    return "Line 1\nLine 2\tTabbed\rReturn\\Backslash\"Quote";
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

        print(f"\n✅ SUCCESS: Escape sequences work!")
        return True

    except Exception as e:
        print(f"\n❌ FAILED: {e}")
        return False


def test_unicode_strings():
    """Test strings with unicode characters."""
    print(f"\n{'='*60}")
    print("Testing unicode strings")
    print(f"{'='*60}")

    pw_code = '''
function unicode() -> string {
    return "Hello 世界 🌍 émoji café";
}

function more_unicode() -> string {
    return "こんにちは привет مرحبا";
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

        print(f"\n✅ SUCCESS: Unicode strings work!")
        return True

    except Exception as e:
        print(f"\n❌ FAILED: {e}")
        return False


def test_special_characters():
    """Test strings with special characters."""
    print(f"\n{'='*60}")
    print("Testing special characters in strings")
    print(f"{'='*60}")

    pw_code = '''
function special() -> string {
    return "!@#$%^&*()_+-=[]{}|;:,.<>?/";
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

        print(f"\n✅ SUCCESS: Special characters work!")
        return True

    except Exception as e:
        print(f"\n❌ FAILED: {e}")
        return False


def test_string_concatenation():
    """Test string concatenation."""
    print(f"\n{'='*60}")
    print("Testing string concatenation")
    print(f"{'='*60}")

    pw_code = '''
function concat(a: string, b: string) -> string {
    return a + b;
}

function complex_concat() -> string {
    return "Hello" + " " + "World" + "!";
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

        print(f"\n✅ SUCCESS: String concatenation works!")
        return True

    except Exception as e:
        print(f"\n❌ FAILED: {e}")
        return False


def test_strings_in_conditionals():
    """Test strings in conditional expressions."""
    print(f"\n{'='*60}")
    print("Testing strings in conditionals")
    print(f"{'='*60}")

    pw_code = '''
function check_string(s: string) -> bool {
    if (s == "hello") {
        return true;
    } else if (s == "world") {
        return false;
    } else {
        return true;
    }
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

        print(f"\n✅ SUCCESS: Strings in conditionals work!")
        return True

    except Exception as e:
        print(f"\n❌ FAILED: {e}")
        return False


def run_all_tests():
    """Run all string tests."""
    print("\n" + "="*60)
    print("PW PARSER STRING HANDLING TESTS")
    print("="*60)

    tests = [
        ("Empty Strings", test_empty_strings),
        ("Long Strings (1000 chars)", test_long_strings),
        ("Escape Sequences", test_escape_sequences),
        ("Unicode Strings", test_unicode_strings),
        ("Special Characters", test_special_characters),
        ("String Concatenation", test_string_concatenation),
        ("Strings in Conditionals", test_strings_in_conditionals)
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
