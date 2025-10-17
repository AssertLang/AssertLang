"""
Test PW parser with deep nesting to find limits and bugs.

Tests:
1. Deep if/else nesting (5, 10, 20, 50 levels)
2. Mixed nesting patterns
3. Parser stack limits
4. Code generation with deep nesting
"""

import sys
from pathlib import Path

# Add project paths
sys.path.insert(0, str(Path(__file__).parent.parent))
sys.path.insert(0, str(Path(__file__).parent.parent / 'pw-syntax-mcp-server'))

from dsl.al_parser import Lexer, Parser
from translators.ir_converter import ir_to_mcp
from translators.python_bridge import pw_to_python
from translators.go_bridge import pw_to_go
from translators.rust_bridge import pw_to_rust


def generate_nested_if(depth: int) -> str:
    """Generate PW code with nested if/else statements."""
    code = []
    code.append(f"function nested_test_{depth}(x: int) -> int {{")

    # Build nested if/else
    indent = "    "
    for i in range(depth):
        code.append(f"{indent * (i + 1)}if (x > {i}) {{")

    # Innermost return
    code.append(f"{indent * (depth + 1)}return {depth};")

    # Close all if statements with else
    for i in range(depth - 1, -1, -1):
        code.append(f"{indent * (i + 1)}}} else {{")
        code.append(f"{indent * (i + 2)}return {i};")
        code.append(f"{indent * (i + 1)}}}")

    code.append("}")

    return "\n".join(code)


def test_nesting_depth(depth: int):
    """Test parser with specified nesting depth."""
    print(f"\n{'='*60}")
    print(f"Testing nesting depth: {depth}")
    print(f"{'='*60}")

    try:
        # Generate test code
        pw_code = generate_nested_if(depth)
        print(f"\nGenerated PW code ({len(pw_code)} chars, {len(pw_code.splitlines())} lines)")

        # Show first few lines
        lines = pw_code.splitlines()
        preview = "\n".join(lines[:5] + ["    ..."] + lines[-5:])
        print(f"\nPreview:\n{preview}\n")

        # Parse
        print("Parsing...")
        lexer = Lexer(pw_code)
        tokens = lexer.tokenize()
        print(f"  ✅ Lexer: {len(tokens)} tokens")

        parser = Parser(tokens)
        ir = parser.parse()
        print(f"  ✅ Parser: {len(ir.functions)} functions")

        # Convert to MCP
        print("Converting to MCP...")
        mcp_tree = ir_to_mcp(ir)
        print(f"  ✅ MCP JSON created")

        # Generate Python
        print("Generating Python...")
        python_code = pw_to_python(mcp_tree)
        print(f"  ✅ Python: {len(python_code)} chars")

        # Generate Go
        print("Generating Go...")
        go_code = pw_to_go(mcp_tree)
        print(f"  ✅ Go: {len(go_code)} chars")

        # Generate Rust
        print("Generating Rust...")
        rust_code = pw_to_rust(mcp_tree)
        print(f"  ✅ Rust: {len(rust_code)} chars")

        print(f"\n✅ SUCCESS: Depth {depth} compiled to all languages!")

        return {
            "depth": depth,
            "success": True,
            "pw_lines": len(pw_code.splitlines()),
            "tokens": len(tokens),
            "python_chars": len(python_code),
            "go_chars": len(go_code),
            "rust_chars": len(rust_code)
        }

    except Exception as e:
        print(f"\n❌ FAILED at depth {depth}")
        print(f"   Error: {type(e).__name__}: {e}")

        return {
            "depth": depth,
            "success": False,
            "error": str(e),
            "error_type": type(e).__name__
        }


def test_mixed_nesting():
    """Test mixed nesting patterns (if inside if, etc)."""
    print(f"\n{'='*60}")
    print("Testing mixed nesting patterns")
    print(f"{'='*60}")

    # Create a function with mixed nesting
    pw_code = """
function mixed_nesting_test(a: int, b: int, c: int) -> int {
    if (a > 0) {
        if (b > 0) {
            if (c > 0) {
                return a + b + c;
            } else {
                if (c == 0) {
                    return a + b;
                } else {
                    return a;
                }
            }
        } else {
            if (c > 0) {
                return a + c;
            } else {
                return a;
            }
        }
    } else {
        if (b > 0) {
            if (c > 0) {
                return b + c;
            } else {
                return b;
            }
        } else {
            if (c > 0) {
                return c;
            } else {
                return 0;
            }
        }
    }
}
"""

    try:
        lexer = Lexer(pw_code)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ir = parser.parse()
        mcp_tree = ir_to_mcp(ir)

        python_code = pw_to_python(mcp_tree)
        go_code = pw_to_go(mcp_tree)
        rust_code = pw_to_rust(mcp_tree)

        print("✅ Mixed nesting pattern compiled successfully!")
        print(f"   Python: {len(python_code)} chars")
        print(f"   Go: {len(go_code)} chars")
        print(f"   Rust: {len(rust_code)} chars")

        return True

    except Exception as e:
        print(f"❌ Mixed nesting failed: {e}")
        return False


def run_all_tests():
    """Run all nesting tests and report results."""
    print("\n" + "="*60)
    print("PW PARSER NESTING STRESS TESTS")
    print("="*60)

    results = []

    # Test increasing nesting depths
    depths = [5, 10, 15, 20, 30, 50, 100]

    for depth in depths:
        result = test_nesting_depth(depth)
        results.append(result)

        # Stop if we hit a failure
        if not result["success"]:
            print(f"\n⚠️  Stopping at depth {depth} due to failure")
            break

    # Test mixed nesting
    mixed_success = test_mixed_nesting()

    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)

    successful = [r for r in results if r["success"]]
    failed = [r for r in results if not r["success"]]

    print(f"\nNesting Depth Tests:")
    print(f"  ✅ Passed: {len(successful)}/{len(results)}")
    print(f"  ❌ Failed: {len(failed)}/{len(results)}")

    if successful:
        max_depth = max(r["depth"] for r in successful)
        print(f"\n  Maximum successful depth: {max_depth}")

    if failed:
        print(f"\n  First failure at depth: {failed[0]['depth']}")
        print(f"  Error: {failed[0].get('error_type', 'Unknown')}")

    print(f"\nMixed Nesting Test: {'✅ PASSED' if mixed_success else '❌ FAILED'}")

    # Detailed results table
    if results:
        print("\n" + "="*60)
        print("DETAILED RESULTS")
        print("="*60)
        print(f"\n{'Depth':<8} {'Status':<10} {'PW Lines':<12} {'Tokens':<10} {'Python':<10} {'Go':<10} {'Rust':<10}")
        print("-" * 70)

        for r in results:
            if r["success"]:
                print(f"{r['depth']:<8} {'✅ PASS':<10} {r['pw_lines']:<12} {r['tokens']:<10} "
                      f"{r['python_chars']:<10} {r['go_chars']:<10} {r['rust_chars']:<10}")
            else:
                print(f"{r['depth']:<8} {'❌ FAIL':<10} {r.get('error_type', 'Unknown error')}")

    print("\n" + "="*60)
    print("Tests complete!")
    print("="*60)

    return results, mixed_success


if __name__ == "__main__":
    results, mixed_success = run_all_tests()

    # Exit code: 0 if all tests passed, 1 if any failed
    all_passed = all(r["success"] for r in results) and mixed_success
    sys.exit(0 if all_passed else 1)
