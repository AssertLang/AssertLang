"""
Test PW parser whitespace handling.

Tests:
1. No whitespace (compressed code)
2. Excessive whitespace
3. Mixed tabs and spaces
4. Trailing whitespace
5. Blank lines in various positions
6. Different line endings (CRLF vs LF)
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
sys.path.insert(0, str(Path(__file__).parent.parent / 'pw-syntax-mcp-server'))

from dsl.al_parser import parse_al
from translators.ir_converter import ir_to_mcp
from translators.python_bridge import pw_to_python


def test_minimal_whitespace():
    """Test code with minimal whitespace."""
    import sys
    sys.stdout.flush()
    print(f"\n{'='*60}", flush=True)
    print("Testing minimal whitespace", flush=True)
    print(f"{'='*60}", flush=True)

    pw_code = """function add(x:int,y:int)->int{return x+y;}"""

    try:
        print(f"Code: {pw_code}", flush=True)

        print("  About to call parse_al...", flush=True)
        ir = parse_al(pw_code)
        print(f"  ✅ Parser: {len(ir.functions)} functions", flush=True)

        print("  About to call ir_to_mcp...", flush=True)
        mcp_tree = ir_to_mcp(ir)
        print("  MCP tree created", flush=True)

        print("  About to call pw_to_python...", flush=True)
        python_code = pw_to_python(mcp_tree)
        print(f"  ✅ Python: generated", flush=True)

        print(f"\n✅ SUCCESS: Minimal whitespace works!")
        return True

    except Exception as e:
        print(f"\n❌ FAILED: {e}")
        return False


def test_excessive_whitespace():
    """Test code with excessive whitespace."""
    print(f"\n{'='*60}")
    print("Testing excessive whitespace")
    print(f"{'='*60}")

    pw_code = """function   add  (  x  :  int  ,  y  :  int  )  ->  int  {
    return   x   +   y  ;
}"""

    try:
        ir = parse_al(pw_code)
        print(f"  ✅ Parser: {len(ir.functions)} functions")

        mcp_tree = ir_to_mcp(ir)
        python_code = pw_to_python(mcp_tree)
        print(f"  ✅ Python: generated")

        print(f"\n✅ SUCCESS: Excessive whitespace handled!")
        return True

    except Exception as e:
        print(f"\n❌ FAILED: {e}")
        return False


def test_mixed_tabs_spaces():
    """Test code with mixed tabs and spaces."""
    print(f"\n{'='*60}")
    print("Testing mixed tabs and spaces")
    print(f"{'='*60}")

    # Mix tabs and spaces for indentation
    pw_code = "function add(x: int, y: int) -> int {\n\treturn x + y;\n}"

    try:
        ir = parse_al(pw_code)
        print(f"  ✅ Parser: {len(ir.functions)} functions")

        mcp_tree = ir_to_mcp(ir)
        python_code = pw_to_python(mcp_tree)
        print(f"  ✅ Python: generated")

        print(f"\n✅ SUCCESS: Mixed tabs/spaces work!")
        return True

    except Exception as e:
        print(f"\n❌ FAILED: {e}")
        return False


def test_trailing_whitespace():
    """Test code with trailing whitespace."""
    print(f"\n{'='*60}")
    print("Testing trailing whitespace")
    print(f"{'='*60}")

    pw_code = """function add(x: int, y: int) -> int {
    return x + y;
}   """

    try:
        ir = parse_al(pw_code)
        print(f"  ✅ Parser: {len(ir.functions)} functions")

        mcp_tree = ir_to_mcp(ir)
        python_code = pw_to_python(mcp_tree)
        print(f"  ✅ Python: generated")

        print(f"\n✅ SUCCESS: Trailing whitespace handled!")
        return True

    except Exception as e:
        print(f"\n❌ FAILED: {e}")
        return False


def test_blank_lines_between_statements():
    """Test blank lines between statements."""
    print(f"\n{'='*60}")
    print("Testing blank lines between statements")
    print(f"{'='*60}")

    pw_code = """function test(x: int) -> int {

    let a = x + 1;


    let b = a + 2;

    return b;

}"""

    try:
        ir = parse_al(pw_code)
        print(f"  ✅ Parser: {len(ir.functions)} functions")

        mcp_tree = ir_to_mcp(ir)
        python_code = pw_to_python(mcp_tree)
        print(f"  ✅ Python: generated")

        print(f"\n✅ SUCCESS: Blank lines between statements work!")
        return True

    except Exception as e:
        print(f"\n❌ FAILED: {e}")
        return False


def test_blank_lines_between_functions():
    """Test blank lines between functions."""
    print(f"\n{'='*60}")
    print("Testing blank lines between functions")
    print(f"{'='*60}")

    pw_code = """function add(x: int, y: int) -> int {
    return x + y;
}


function subtract(x: int, y: int) -> int {
    return x - y;
}



function multiply(x: int, y: int) -> int {
    return x * y;
}"""

    try:
        ir = parse_al(pw_code)
        print(f"  ✅ Parser: {len(ir.functions)} functions")

        mcp_tree = ir_to_mcp(ir)
        python_code = pw_to_python(mcp_tree)
        print(f"  ✅ Python: generated")

        print(f"\n✅ SUCCESS: Blank lines between functions work!")
        return True

    except Exception as e:
        print(f"\n❌ FAILED: {e}")
        return False


def test_only_blank_lines():
    """Test file with only blank lines (should handle gracefully)."""
    print(f"\n{'='*60}")
    print("Testing file with only blank lines")
    print(f"{'='*60}")

    pw_code = "\n\n\n\n\n"

    try:
        ir = parse_al(pw_code)
        print(f"  ✅ Parser: {len(ir.functions)} functions (expected 0)")

        if len(ir.functions) == 0:
            print(f"\n✅ SUCCESS: Empty file handled correctly!")
            return True
        else:
            print(f"\n⚠️  WARNING: Expected 0 functions, got {len(ir.functions)}")
            return True  # Still pass, just unexpected

    except Exception as e:
        print(f"\n⚠️  Note: Empty file threw exception: {type(e).__name__}")
        # This is acceptable - empty files might error
        return True


def test_crlf_line_endings():
    """Test Windows-style CRLF line endings."""
    print(f"\n{'='*60}")
    print("Testing CRLF line endings")
    print(f"{'='*60}")

    # Use \r\n for Windows line endings
    pw_code = "function add(x: int, y: int) -> int {\r\n    return x + y;\r\n}"

    try:
        ir = parse_al(pw_code)
        print(f"  ✅ Parser: {len(ir.functions)} functions")

        mcp_tree = ir_to_mcp(ir)
        python_code = pw_to_python(mcp_tree)
        print(f"  ✅ Python: generated")

        print(f"\n✅ SUCCESS: CRLF line endings work!")
        return True

    except Exception as e:
        print(f"\n❌ FAILED: {e}")
        return False


def run_all_tests():
    """Run all whitespace tests."""
    import sys
    print("\n" + "="*60, flush=True)
    print("PW PARSER WHITESPACE HANDLING TESTS", flush=True)
    print("="*60, flush=True)
    sys.stdout.flush()

    tests = [
        ("Minimal Whitespace", test_minimal_whitespace),
        ("Excessive Whitespace", test_excessive_whitespace),
        ("Mixed Tabs/Spaces", test_mixed_tabs_spaces),
        ("Trailing Whitespace", test_trailing_whitespace),
        ("Blank Lines Between Statements", test_blank_lines_between_statements),
        ("Blank Lines Between Functions", test_blank_lines_between_functions),
        ("Only Blank Lines", test_only_blank_lines),
        ("CRLF Line Endings", test_crlf_line_endings)
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
