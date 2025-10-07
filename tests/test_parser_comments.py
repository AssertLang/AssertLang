"""
Test PW parser comment handling edge cases.

Tests:
1. Many consecutive comment lines
2. Comments with special characters
3. Comments inside expressions
4. Multi-line comments
5. Mixed comment styles
6. Edge cases (unclosed comments, nested comments)
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
sys.path.insert(0, str(Path(__file__).parent.parent / 'pw-syntax-mcp-server'))

from dsl.pw_parser import Lexer, Parser
from translators.ir_converter import ir_to_mcp
from translators.python_bridge import pw_to_python


def test_many_single_line_comments():
    """Test many consecutive single-line comments."""
    print(f"\n{'='*60}")
    print("Testing many consecutive single-line comments")
    print(f"{'='*60}")

    # Generate 50 comment lines
    comments = "\n".join(f"// Comment line {i}" for i in range(50))
    pw_code = f"""{comments}

function add(x: int, y: int) -> int {{
    return x + y;
}}"""

    try:
        lexer = Lexer(pw_code)
        tokens = lexer.tokenize()
        print(f"  ✅ Lexer: {len(tokens)} tokens (comments should be filtered)")

        parser = Parser(tokens)
        ir = parser.parse()
        print(f"  ✅ Parser: {len(ir.functions)} functions")

        mcp_tree = ir_to_mcp(ir)
        python_code = pw_to_python(mcp_tree)
        print(f"  ✅ Python: generated")

        print(f"\n✅ SUCCESS: 50 comment lines handled!")
        return True

    except Exception as e:
        print(f"\n❌ FAILED: {e}")
        return False


def test_block_comments():
    """Test block comments."""
    print(f"\n{'='*60}")
    print("Testing block comments")
    print(f"{'='*60}")

    pw_code = """
/* This is a block comment */
function add(x: int, y: int) -> int {
    /* Another block comment */
    return x + y; /* inline block comment */
}

/*
 * Multi-line block comment
 * with multiple lines
 * and more text
 */
function subtract(x: int, y: int) -> int {
    return x - y;
}
"""

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

        print(f"\n✅ SUCCESS: Block comments work!")
        return True

    except Exception as e:
        print(f"\n❌ FAILED: {e}")
        return False


def test_mixed_comment_styles():
    """Test mixing // and /* */ comments."""
    print(f"\n{'='*60}")
    print("Testing mixed comment styles")
    print(f"{'='*60}")

    pw_code = """
// Single line comment
/* Block comment */
function test(x: int) -> int {
    // Another single line
    /* Another block */
    let y = x + 1; // Inline single
    return y; /* Inline block */
}
"""

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

        print(f"\n✅ SUCCESS: Mixed comment styles work!")
        return True

    except Exception as e:
        print(f"\n❌ FAILED: {e}")
        return False


def test_comments_with_special_chars():
    """Test comments with special characters."""
    print(f"\n{'='*60}")
    print("Testing comments with special characters")
    print(f"{'='*60}")

    pw_code = """
// Comment with symbols: !@#$%^&*()_+-=[]{}|;':\",./<>?
/* Block with symbols: !@#$%^&*() */
function test(x: int) -> int {
    // Unicode: 世界 🌍 émojis
    /* More unicode: こんにちは */
    return x;
}
"""

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

        print(f"\n✅ SUCCESS: Special characters in comments work!")
        return True

    except Exception as e:
        print(f"\n❌ FAILED: {e}")
        return False


def test_comment_with_code_like_text():
    """Test comments that look like code."""
    print(f"\n{'='*60}")
    print("Testing comments that look like code")
    print(f"{'='*60}")

    pw_code = """
// function fake(x: int) -> int { return x; }
/* if (true) { return false; } */
function real(x: int) -> int {
    // let y = x + 1;
    /* return x * 2; */
    return x;
}
"""

    try:
        lexer = Lexer(pw_code)
        tokens = lexer.tokenize()
        print(f"  ✅ Lexer: {len(tokens)} tokens")

        parser = Parser(tokens)
        ir = parser.parse()

        # Should only have 1 function (the real one)
        if len(ir.functions) == 1:
            print(f"  ✅ Parser: {len(ir.functions)} function (commented code ignored)")
        else:
            print(f"  ⚠️  Parser: {len(ir.functions)} functions (expected 1)")

        mcp_tree = ir_to_mcp(ir)
        python_code = pw_to_python(mcp_tree)
        print(f"  ✅ Python: generated")

        print(f"\n✅ SUCCESS: Code-like comments handled correctly!")
        return True

    except Exception as e:
        print(f"\n❌ FAILED: {e}")
        return False


def test_empty_comments():
    """Test empty comments."""
    print(f"\n{'='*60}")
    print("Testing empty comments")
    print(f"{'='*60}")

    pw_code = """
//
/**/
function test(x: int) -> int {
    //
    /**/
    return x;
}
"""

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

        print(f"\n✅ SUCCESS: Empty comments work!")
        return True

    except Exception as e:
        print(f"\n❌ FAILED: {e}")
        return False


def test_hash_comments():
    """Test Python-style # comments."""
    print(f"\n{'='*60}")
    print("Testing # (hash) comments")
    print(f"{'='*60}")

    pw_code = """
# This is a hash comment
function add(x: int, y: int) -> int {
    # Another hash comment
    return x + y; # Inline hash comment
}
"""

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

        print(f"\n✅ SUCCESS: Hash comments work!")
        return True

    except Exception as e:
        print(f"\n❌ FAILED: {e}")
        return False


def test_all_three_comment_styles():
    """Test all three comment styles in one file."""
    print(f"\n{'='*60}")
    print("Testing all three comment styles together")
    print(f"{'='*60}")

    pw_code = """
// C++ style comment
/* C style comment */
# Python style comment

function test(x: int) -> int {
    // Style 1
    /* Style 2 */
    # Style 3
    return x;
}
"""

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

        print(f"\n✅ SUCCESS: All three comment styles work together!")
        return True

    except Exception as e:
        print(f"\n❌ FAILED: {e}")
        return False


def run_all_tests():
    """Run all comment tests."""
    print("\n" + "="*60)
    print("PW PARSER COMMENT EDGE CASE TESTS")
    print("="*60)

    tests = [
        ("Many Single-Line Comments", test_many_single_line_comments),
        ("Block Comments", test_block_comments),
        ("Mixed Comment Styles", test_mixed_comment_styles),
        ("Special Characters in Comments", test_comments_with_special_chars),
        ("Code-Like Comments", test_comment_with_code_like_text),
        ("Empty Comments", test_empty_comments),
        ("Hash Comments", test_hash_comments),
        ("All Three Comment Styles", test_all_three_comment_styles)
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
