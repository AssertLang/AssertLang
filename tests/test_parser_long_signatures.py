"""
Test PW parser with very long function signatures.

Tests:
1. Functions with many parameters (10, 50, 100)
2. Very long parameter names
3. Complex type annotations
4. Edge cases with parameter lists
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
sys.path.insert(0, str(Path(__file__).parent.parent / 'pw-syntax-mcp-server'))

from dsl.pw_parser import Lexer, Parser
from translators.ir_converter import ir_to_mcp
from translators.python_bridge import pw_to_python


def generate_function_with_n_params(n: int) -> str:
    """Generate a function with N parameters."""
    params = ", ".join(f"param{i}: int" for i in range(n))
    body_sum = " + ".join(f"param{i}" for i in range(n))

    return f"""function test_with_{n}_params({params}) -> int {{
    return {body_sum};
}}"""


def generate_function_with_long_param_names(name_length: int) -> str:
    """Generate a function with very long parameter names."""
    param1 = "a" * name_length
    param2 = "b" * name_length
    param3 = "c" * name_length

    return f"""function test_long_names({param1}: int, {param2}: int, {param3}: int) -> int {{
    return {param1} + {param2} + {param3};
}}"""


def test_n_parameters(n: int):
    """Test function with N parameters."""
    print(f"\n{'='*60}")
    print(f"Testing function with {n} parameters")
    print(f"{'='*60}")

    try:
        pw_code = generate_function_with_n_params(n)
        print(f"Generated code: {len(pw_code)} chars")

        # Show preview
        lines = pw_code.splitlines()
        if len(lines[0]) > 100:
            print(f"Signature preview: {lines[0][:100]}...")
        else:
            print(f"Signature: {lines[0]}")

        lexer = Lexer(pw_code)
        tokens = lexer.tokenize()
        print(f"  ✅ Lexer: {len(tokens)} tokens")

        parser = Parser(tokens)
        ir = parser.parse()
        print(f"  ✅ Parser: {len(ir.functions)} functions, {len(ir.functions[0].params)} parameters")

        mcp_tree = ir_to_mcp(ir)
        print(f"  ✅ MCP JSON created")

        python_code = pw_to_python(mcp_tree)
        print(f"  ✅ Python: {len(python_code)} chars")

        print(f"\n✅ SUCCESS: {n} parameters handled!")

        return {
            "params": n,
            "success": True,
            "pw_chars": len(pw_code),
            "tokens": len(tokens),
            "python_chars": len(python_code)
        }

    except Exception as e:
        print(f"\n❌ FAILED with {n} parameters")
        print(f"   Error: {type(e).__name__}: {e}")

        return {
            "params": n,
            "success": False,
            "error": str(e),
            "error_type": type(e).__name__
        }


def test_long_param_names(name_length: int):
    """Test function with very long parameter names."""
    print(f"\n{'='*60}")
    print(f"Testing parameter names of length {name_length}")
    print(f"{'='*60}")

    try:
        pw_code = generate_function_with_long_param_names(name_length)
        print(f"Generated code: {len(pw_code)} chars")

        lexer = Lexer(pw_code)
        tokens = lexer.tokenize()
        print(f"  ✅ Lexer: {len(tokens)} tokens")

        parser = Parser(tokens)
        ir = parser.parse()
        print(f"  ✅ Parser: {len(ir.functions)} functions")

        mcp_tree = ir_to_mcp(ir)
        python_code = pw_to_python(mcp_tree)
        print(f"  ✅ Python generated: {len(python_code)} chars")

        print(f"\n✅ SUCCESS: Parameter names of length {name_length}!")

        return {
            "name_length": name_length,
            "success": True
        }

    except Exception as e:
        print(f"\n❌ FAILED with name length {name_length}")
        print(f"   Error: {type(e).__name__}: {e}")

        return {
            "name_length": name_length,
            "success": False,
            "error": str(e)
        }


def test_mixed_types():
    """Test function with mixed parameter types."""
    print(f"\n{'='*60}")
    print("Testing mixed parameter types")
    print(f"{'='*60}")

    pw_code = """function mixed_types(a: int, b: float, c: string, d: bool, e: int, f: float) -> string {
    return c;
}"""

    try:
        lexer = Lexer(pw_code)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ir = parser.parse()
        mcp_tree = ir_to_mcp(ir)
        python_code = pw_to_python(mcp_tree)

        print(f"✅ Mixed types compiled successfully!")
        print(f"   Parameters: {len(ir.functions[0].params)}")
        print(f"   Types: int, float, string, bool, int, float")

        return True

    except Exception as e:
        print(f"❌ Mixed types failed: {e}")
        return False


def run_all_tests():
    """Run all long signature tests."""
    print("\n" + "="*60)
    print("PW PARSER LONG SIGNATURE STRESS TESTS")
    print("="*60)

    results = []

    # Test increasing parameter counts
    param_counts = [5, 10, 25, 50, 100, 200]

    for n in param_counts:
        result = test_n_parameters(n)
        results.append(result)

        if not result["success"]:
            print(f"\n⚠️  Stopping at {n} parameters due to failure")
            break

    # Test long parameter names
    name_length_results = []
    name_lengths = [10, 50, 100, 500]

    for length in name_lengths:
        result = test_long_param_names(length)
        name_length_results.append(result)

        if not result["success"]:
            break

    # Test mixed types
    mixed_success = test_mixed_types()

    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)

    successful = [r for r in results if r["success"]]
    failed = [r for r in results if not r["success"]]

    print(f"\nParameter Count Tests:")
    print(f"  ✅ Passed: {len(successful)}/{len(results)}")
    print(f"  ❌ Failed: {len(failed)}/{len(results)}")

    if successful:
        max_params = max(r["params"] for r in successful)
        print(f"\n  Maximum successful parameter count: {max_params}")

    name_successful = [r for r in name_length_results if r["success"]]
    print(f"\nLong Parameter Name Tests:")
    print(f"  ✅ Passed: {len(name_successful)}/{len(name_length_results)}")

    if name_successful:
        max_name_length = max(r["name_length"] for r in name_successful)
        print(f"  Maximum parameter name length: {max_name_length}")

    print(f"\nMixed Types Test: {'✅ PASSED' if mixed_success else '❌ FAILED'}")

    # Detailed results
    if results:
        print("\n" + "="*60)
        print("DETAILED RESULTS - Parameter Count")
        print("="*60)
        print(f"\n{'Params':<8} {'Status':<10} {'PW Chars':<12} {'Tokens':<10} {'Python':<10}")
        print("-" * 50)

        for r in results:
            if r["success"]:
                print(f"{r['params']:<8} {'✅ PASS':<10} {r['pw_chars']:<12} {r['tokens']:<10} {r['python_chars']:<10}")
            else:
                print(f"{r['params']:<8} {'❌ FAIL':<10} {r.get('error_type', 'Unknown')}")

    print("\n" + "="*60)
    print("Tests complete!")
    print("="*60)

    return results, name_length_results, mixed_success


if __name__ == "__main__":
    results, name_results, mixed_success = run_all_tests()

    all_passed = (all(r["success"] for r in results) and
                  all(r["success"] for r in name_results) and
                  mixed_success)

    sys.exit(0 if all_passed else 1)
