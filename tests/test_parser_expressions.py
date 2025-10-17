"""
Test PW parser with complex expressions.

Tests:
1. Chained binary operations (10, 50, 100 operations)
2. Deeply nested parentheses
3. Mixed operators and precedence
4. String concatenation chains
5. Complex mathematical expressions
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
sys.path.insert(0, str(Path(__file__).parent.parent / 'pw-syntax-mcp-server'))

from dsl.al_parser import Lexer, Parser
from translators.ir_converter import ir_to_mcp
from translators.python_bridge import pw_to_python


def test_chained_additions(n: int):
    """Test chained addition operations."""
    print(f"\n{'='*60}")
    print(f"Testing {n} chained additions")
    print(f"{'='*60}")

    # Generate: a + b + c + d + ... (n terms)
    terms = " + ".join(f"param{i}" for i in range(n))
    params = ", ".join(f"param{i}: int" for i in range(n))

    pw_code = f"""function chain_add_{n}({params}) -> int {{
    return {terms};
}}"""

    try:
        print(f"Expression length: {len(terms)} chars")

        lexer = Lexer(pw_code)
        tokens = lexer.tokenize()
        print(f"  ✅ Lexer: {len(tokens)} tokens")

        parser = Parser(tokens)
        ir = parser.parse()
        print(f"  ✅ Parser: parsed successfully")

        mcp_tree = ir_to_mcp(ir)
        python_code = pw_to_python(mcp_tree)
        print(f"  ✅ Python: {len(python_code)} chars")

        print(f"\n✅ SUCCESS: {n} chained additions!")
        return {"count": n, "success": True}

    except Exception as e:
        print(f"\n❌ FAILED with {n} additions")
        print(f"   Error: {type(e).__name__}: {e}")
        return {"count": n, "success": False, "error": str(e)}


def test_deeply_nested_parens(depth: int):
    """Test deeply nested parentheses."""
    print(f"\n{'='*60}")
    print(f"Testing {depth} levels of nested parentheses")
    print(f"{'='*60}")

    # Generate: ((((a + b) + c) + d) + e)
    expr = "a"
    for i in range(depth):
        expr = f"({expr} + b)"

    pw_code = f"""function nested_parens_{depth}(a: int, b: int) -> int {{
    return {expr};
}}"""

    try:
        print(f"Expression: {expr[:50]}{'...' if len(expr) > 50 else ''}")

        lexer = Lexer(pw_code)
        tokens = lexer.tokenize()
        print(f"  ✅ Lexer: {len(tokens)} tokens")

        parser = Parser(tokens)
        ir = parser.parse()
        print(f"  ✅ Parser: parsed successfully")

        mcp_tree = ir_to_mcp(ir)
        python_code = pw_to_python(mcp_tree)
        print(f"  ✅ Python: {len(python_code)} chars")

        print(f"\n✅ SUCCESS: {depth} nested parentheses!")
        return {"depth": depth, "success": True}

    except Exception as e:
        print(f"\n❌ FAILED with {depth} nested parentheses")
        print(f"   Error: {type(e).__name__}: {e}")
        return {"depth": depth, "success": False, "error": str(e)}


def test_mixed_operators():
    """Test mixed operators and precedence."""
    print(f"\n{'='*60}")
    print("Testing mixed operators and precedence")
    print(f"{'='*60}")

    pw_code = """
function mixed_ops(a: int, b: int, c: int, d: int) -> int {
    return a + b * c - d / 2;
}

function complex_expr(x: int, y: int) -> int {
    return (x + y) * (x - y) + x / y - y * 2;
}

function string_and_math(price: float, tax: float) -> string {
    return "Total: " + (price + tax);
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
        print(f"  ✅ Python: {len(python_code)} chars")

        print(f"\n✅ SUCCESS: Mixed operators work!")
        return True

    except Exception as e:
        print(f"\n❌ FAILED: {e}")
        return False


def test_string_concatenation_chain(n: int):
    """Test chained string concatenation."""
    print(f"\n{'='*60}")
    print(f"Testing {n} chained string concatenations")
    print(f"{'='*60}")

    # Generate: "a" + "b" + "c" + ...
    strings = " + ".join(f'"str{i}"' for i in range(n))

    pw_code = f"""function concat_chain_{n}() -> string {{
    return {strings};
}}"""

    try:
        print(f"Expression length: {len(strings)} chars")

        lexer = Lexer(pw_code)
        tokens = lexer.tokenize()
        print(f"  ✅ Lexer: {len(tokens)} tokens")

        parser = Parser(tokens)
        ir = parser.parse()
        print(f"  ✅ Parser: parsed successfully")

        mcp_tree = ir_to_mcp(ir)
        python_code = pw_to_python(mcp_tree)
        print(f"  ✅ Python: {len(python_code)} chars")

        print(f"\n✅ SUCCESS: {n} string concatenations!")
        return {"count": n, "success": True}

    except Exception as e:
        print(f"\n❌ FAILED with {n} concatenations")
        print(f"   Error: {type(e).__name__}: {e}")
        return {"count": n, "success": False, "error": str(e)}


def test_comparison_chains():
    """Test comparison operators."""
    print(f"\n{'='*60}")
    print("Testing comparison operators")
    print(f"{'='*60}")

    pw_code = """
function test_comparisons(a: int, b: int) -> bool {
    if (a > b) {
        return true;
    } else if (a < b) {
        return false;
    } else if (a == b) {
        return true;
    } else if (a != b) {
        return false;
    } else if (a >= b) {
        return true;
    } else if (a <= b) {
        return false;
    } else {
        return true;
    }
}
"""

    try:
        lexer = Lexer(pw_code)
        tokens = lexer.tokenize()
        print(f"  ✅ Lexer: {len(tokens)} tokens")

        parser = Parser(tokens)
        ir = parser.parse()
        print(f"  ✅ Parser: parsed successfully")

        mcp_tree = ir_to_mcp(ir)
        python_code = pw_to_python(mcp_tree)
        print(f"  ✅ Python: {len(python_code)} chars")

        print(f"\n✅ SUCCESS: All comparison operators work!")
        return True

    except Exception as e:
        print(f"\n❌ FAILED: {e}")
        return False


def test_complex_mathematical_expr():
    """Test complex mathematical expressions."""
    print(f"\n{'='*60}")
    print("Testing complex mathematical expressions")
    print(f"{'='*60}")

    pw_code = """
function quadratic(a: float, b: float, c: float, x: float) -> float {
    return a * x * x + b * x + c;
}

function compound_interest(principal: float, rate: float, years: int) -> float {
    return principal * (1.0 + rate) * (1.0 + rate) * (1.0 + rate);
}

function distance(x1: float, y1: float, x2: float, y2: float) -> float {
    let dx = x2 - x1;
    let dy = y2 - y1;
    return dx * dx + dy * dy;
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
        print(f"  ✅ Python: {len(python_code)} chars")

        print(f"\n✅ SUCCESS: Complex math expressions work!")
        return True

    except Exception as e:
        print(f"\n❌ FAILED: {e}")
        return False


def run_all_tests():
    """Run all expression tests."""
    print("\n" + "="*60)
    print("PW PARSER COMPLEX EXPRESSION TESTS")
    print("="*60)

    results = []

    # Test chained additions
    for n in [5, 10, 25, 50, 100]:
        result = test_chained_additions(n)
        results.append(("chained_add", result))
        if not result["success"]:
            break

    # Test nested parentheses
    paren_results = []
    for depth in [5, 10, 20, 50]:
        result = test_deeply_nested_parens(depth)
        paren_results.append(result)
        if not result["success"]:
            break

    # Test mixed operators
    mixed_result = test_mixed_operators()
    results.append(("mixed_ops", {"success": mixed_result}))

    # Test string concatenation
    for n in [5, 10, 25, 50]:
        result = test_string_concatenation_chain(n)
        results.append(("string_concat", result))
        if not result["success"]:
            break

    # Test comparisons
    comp_result = test_comparison_chains()
    results.append(("comparisons", {"success": comp_result}))

    # Test complex math
    math_result = test_complex_mathematical_expr()
    results.append(("complex_math", {"success": math_result}))

    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)

    total = len(results) + len(paren_results)
    passed = sum(1 for _, r in results if r.get("success", False)) + \
             sum(1 for r in paren_results if r.get("success", False))

    print(f"\nTotal: {passed}/{total} tests passed")

    # Chained additions
    add_results = [r for cat, r in results if cat == "chained_add"]
    if add_results:
        max_add = max(r["count"] for r in add_results if r["success"])
        print(f"\nChained Additions: Max {max_add} operations")

    # Nested parentheses
    if paren_results:
        successful_parens = [r for r in paren_results if r["success"]]
        if successful_parens:
            max_parens = max(r["depth"] for r in successful_parens)
            print(f"Nested Parentheses: Max {max_parens} levels")

    # String concatenations
    concat_results = [r for cat, r in results if cat == "string_concat"]
    if concat_results:
        max_concat = max(r["count"] for r in concat_results if r["success"])
        print(f"String Concatenations: Max {max_concat} operations")

    print("\n" + "="*60)

    return results, paren_results


if __name__ == "__main__":
    results, paren_results = run_all_tests()

    all_passed = (all(r.get("success", False) for _, r in results) and
                  all(r.get("success", False) for r in paren_results))

    sys.exit(0 if all_passed else 1)
