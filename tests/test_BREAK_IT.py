"""
EXTREME STRESS TESTS - Try to break PW parser completely

These tests are designed to BREAK the parser:
1. 1000 levels of nesting
2. 10,000 parameters
3. 100,000-character strings
4. Massive files (100,000 lines)
5. Pathological cases
6. Malformed input
7. Resource exhaustion
"""

import sys
from pathlib import Path
import time

sys.path.insert(0, str(Path(__file__).parent.parent))
sys.path.insert(0, str(Path(__file__).parent.parent / 'pw-syntax-mcp-server'))

from dsl.pw_parser import Lexer, Parser
from translators.ir_converter import ir_to_mcp
from translators.python_bridge import pw_to_python


def test_extreme_nesting(depth: int):
    """Test EXTREME nesting - try to cause stack overflow."""
    print(f"\n{'='*60}")
    print(f"🔥 EXTREME TEST: {depth} levels of nesting")
    print(f"{'='*60}")

    # Generate extremely deep nesting
    code = [f"function extreme_{depth}(x: int) -> int {{"]
    indent = "    "

    for i in range(depth):
        code.append(f"{indent * (i + 1)}if (x > {i}) {{")

    code.append(f"{indent * (depth + 1)}return {depth};")

    for i in range(depth - 1, -1, -1):
        code.append(f"{indent * (i + 1)}}} else {{")
        code.append(f"{indent * (i + 2)}return {i};")
        code.append(f"{indent * (i + 1)}}}")

    code.append("}")
    pw_code = "\n".join(code)

    print(f"Generated: {len(pw_code):,} chars, {len(code):,} lines")

    try:
        start = time.time()

        lexer = Lexer(pw_code)
        tokens = lexer.tokenize()
        lex_time = time.time() - start
        print(f"  ✅ Lexer: {len(tokens):,} tokens ({lex_time:.2f}s)")

        start = time.time()
        parser = Parser(tokens)
        ir = parser.parse()
        parse_time = time.time() - start
        print(f"  ✅ Parser: Success ({parse_time:.2f}s)")

        start = time.time()
        mcp_tree = ir_to_mcp(ir)
        python_code = pw_to_python(mcp_tree)
        gen_time = time.time() - start
        print(f"  ✅ Python: {len(python_code):,} chars ({gen_time:.2f}s)")

        total_time = lex_time + parse_time + gen_time
        print(f"\n✅ SURVIVED: {depth} nesting levels! Total time: {total_time:.2f}s")
        return True

    except RecursionError as e:
        print(f"\n💥 STACK OVERFLOW at {depth} levels!")
        print(f"   Max recursion depth exceeded")
        return False
    except MemoryError as e:
        print(f"\n💥 OUT OF MEMORY at {depth} levels!")
        return False
    except Exception as e:
        print(f"\n💥 CRASHED: {type(e).__name__}: {str(e)[:100]}")
        return False


def test_massive_parameters(count: int):
    """Test MASSIVE parameter lists - try to exhaust memory."""
    print(f"\n{'='*60}")
    print(f"🔥 EXTREME TEST: {count:,} parameters")
    print(f"{'='*60}")

    params = ", ".join(f"p{i}: int" for i in range(count))
    body = " + ".join(f"p{i}" for i in range(count))

    pw_code = f"function massive_{count}({params}) -> int {{\n    return {body};\n}}"

    print(f"Generated: {len(pw_code):,} chars")

    try:
        start = time.time()

        lexer = Lexer(pw_code)
        tokens = lexer.tokenize()
        lex_time = time.time() - start
        print(f"  ✅ Lexer: {len(tokens):,} tokens ({lex_time:.2f}s)")

        start = time.time()
        parser = Parser(tokens)
        ir = parser.parse()
        parse_time = time.time() - start
        print(f"  ✅ Parser: {len(ir.functions[0].params):,} params ({parse_time:.2f}s)")

        start = time.time()
        mcp_tree = ir_to_mcp(ir)
        python_code = pw_to_python(mcp_tree)
        gen_time = time.time() - start
        print(f"  ✅ Python: {len(python_code):,} chars ({gen_time:.2f}s)")

        total_time = lex_time + parse_time + gen_time
        print(f"\n✅ SURVIVED: {count:,} parameters! Total time: {total_time:.2f}s")
        return True

    except MemoryError:
        print(f"\n💥 OUT OF MEMORY at {count:,} parameters!")
        return False
    except Exception as e:
        print(f"\n💥 CRASHED: {type(e).__name__}: {str(e)[:100]}")
        return False


def test_massive_string(length: int):
    """Test MASSIVE strings - try to exhaust memory."""
    print(f"\n{'='*60}")
    print(f"🔥 EXTREME TEST: {length:,}-character string")
    print(f"{'='*60}")

    big_string = "a" * length
    pw_code = f'function massive_string() -> string {{\n    return "{big_string}";\n}}'

    print(f"Generated: {len(pw_code):,} chars")

    try:
        start = time.time()

        lexer = Lexer(pw_code)
        tokens = lexer.tokenize()
        lex_time = time.time() - start
        print(f"  ✅ Lexer: {len(tokens)} tokens ({lex_time:.2f}s)")

        start = time.time()
        parser = Parser(tokens)
        ir = parser.parse()
        parse_time = time.time() - start
        print(f"  ✅ Parser: Success ({parse_time:.2f}s)")

        start = time.time()
        mcp_tree = ir_to_mcp(ir)
        python_code = pw_to_python(mcp_tree)
        gen_time = time.time() - start
        print(f"  ✅ Python: {len(python_code):,} chars ({gen_time:.2f}s)")

        total_time = lex_time + parse_time + gen_time
        print(f"\n✅ SURVIVED: {length:,}-char string! Total time: {total_time:.2f}s")
        return True

    except MemoryError:
        print(f"\n💥 OUT OF MEMORY at {length:,} chars!")
        return False
    except Exception as e:
        print(f"\n💥 CRASHED: {type(e).__name__}: {str(e)[:100]}")
        return False


def test_massive_file(function_count: int):
    """Test MASSIVE file with many functions."""
    print(f"\n{'='*60}")
    print(f"🔥 EXTREME TEST: {function_count:,} functions")
    print(f"{'='*60}")

    functions = []
    for i in range(function_count):
        functions.append(f"""function func_{i}(x: int) -> int {{
    return x + {i};
}}
""")

    pw_code = "\n".join(functions)

    print(f"Generated: {len(pw_code):,} chars, ~{len(pw_code.splitlines()):,} lines")

    try:
        start = time.time()

        lexer = Lexer(pw_code)
        tokens = lexer.tokenize()
        lex_time = time.time() - start
        print(f"  ✅ Lexer: {len(tokens):,} tokens ({lex_time:.2f}s)")

        start = time.time()
        parser = Parser(tokens)
        ir = parser.parse()
        parse_time = time.time() - start
        print(f"  ✅ Parser: {len(ir.functions):,} functions ({parse_time:.2f}s)")

        start = time.time()
        mcp_tree = ir_to_mcp(ir)
        python_code = pw_to_python(mcp_tree)
        gen_time = time.time() - start
        print(f"  ✅ Python: {len(python_code):,} chars ({gen_time:.2f}s)")

        total_time = lex_time + parse_time + gen_time
        print(f"\n✅ SURVIVED: {function_count:,} functions! Total time: {total_time:.2f}s")
        return True

    except MemoryError:
        print(f"\n💥 OUT OF MEMORY at {function_count:,} functions!")
        return False
    except Exception as e:
        print(f"\n💥 CRASHED: {type(e).__name__}: {str(e)[:100]}")
        return False


def test_pathological_cases():
    """Test pathological/malicious cases."""
    print(f"\n{'='*60}")
    print(f"🔥 PATHOLOGICAL CASES")
    print(f"{'='*60}")

    cases = [
        ("Unclosed string", 'function bad() -> string { return "unclosed'),
        ("Unclosed brace", 'function bad() -> int { return 1;'),
        ("Invalid operator", 'function bad(x: int) -> int { return x @@ y; }'),
        ("Missing semicolon in required spot", 'function bad() -> int { let x = 1 let y = 2; return x; }'),
        ("Reserved word as name", 'function return() -> int { return 1; }'),
        ("Empty function name", 'function (x: int) -> int { return x; }'),
        ("No return type", 'function bad(x: int) { return x; }'),
        ("Type mismatch", 'function bad() -> int { return "string"; }'),
    ]

    results = []
    for test_name, code in cases:
        print(f"\n  Testing: {test_name}")
        try:
            lexer = Lexer(code)
            tokens = lexer.tokenize()
            parser = Parser(tokens)
            ir = parser.parse()
            print(f"    ⚠️  SHOULD HAVE FAILED but didn't!")
            results.append((test_name, "passed_unexpectedly"))
        except Exception as e:
            print(f"    ✅ Correctly errored: {type(e).__name__}")
            results.append((test_name, "correctly_failed"))

    print(f"\n{'='*60}")
    correctly_failed = sum(1 for _, r in results if r == "correctly_failed")
    print(f"Pathological cases: {correctly_failed}/{len(cases)} correctly rejected")

    return results


def run_break_tests():
    """Run all break tests."""
    print("\n" + "="*60)
    print("🔥 EXTREME STRESS TESTS - BREAK THE PARSER! 🔥")
    print("="*60)

    results = []

    # Test 1: Extreme nesting
    print("\n" + "="*60)
    print("TEST 1: EXTREME NESTING")
    print("="*60)

    for depth in [200, 500, 1000, 2000]:
        result = test_extreme_nesting(depth)
        results.append(("extreme_nesting", depth, result))
        if not result:
            print(f"\n⚠️  BROKE at {depth} nesting levels!")
            break

    # Test 2: Massive parameters
    print("\n" + "="*60)
    print("TEST 2: MASSIVE PARAMETERS")
    print("="*60)

    for count in [500, 1000, 5000, 10000]:
        result = test_massive_parameters(count)
        results.append(("massive_params", count, result))
        if not result:
            print(f"\n⚠️  BROKE at {count:,} parameters!")
            break

    # Test 3: Massive strings
    print("\n" + "="*60)
    print("TEST 3: MASSIVE STRINGS")
    print("="*60)

    for length in [10000, 100000, 1000000]:
        result = test_massive_string(length)
        results.append(("massive_string", length, result))
        if not result:
            print(f"\n⚠️  BROKE at {length:,}-char string!")
            break

    # Test 4: Massive files
    print("\n" + "="*60)
    print("TEST 4: MASSIVE FILES")
    print("="*60)

    for count in [1000, 5000, 10000]:
        result = test_massive_file(count)
        results.append(("massive_file", count, result))
        if not result:
            print(f"\n⚠️  BROKE at {count:,} functions!")
            break

    # Test 5: Pathological cases
    print("\n" + "="*60)
    print("TEST 5: PATHOLOGICAL CASES")
    print("="*60)

    pathological_results = test_pathological_cases()

    # Summary
    print("\n" + "="*60)
    print("🔥 BREAK TEST SUMMARY 🔥")
    print("="*60)

    # Group results by category
    nesting = [(v, r) for cat, v, r in results if cat == "extreme_nesting"]
    params = [(v, r) for cat, v, r in results if cat == "massive_params"]
    strings = [(v, r) for cat, v, r in results if cat == "massive_string"]
    files = [(v, r) for cat, v, r in results if cat == "massive_file"]

    if nesting:
        max_nesting = max(v for v, r in nesting if r)
        print(f"\nExtreme Nesting:")
        print(f"  Maximum depth survived: {max_nesting:,} levels")
        broke_at = next((v for v, r in nesting if not r), None)
        if broke_at:
            print(f"  BROKE at: {broke_at:,} levels 💥")

    if params:
        max_params = max(v for v, r in params if r)
        print(f"\nMassive Parameters:")
        print(f"  Maximum params survived: {max_params:,} parameters")
        broke_at = next((v for v, r in params if not r), None)
        if broke_at:
            print(f"  BROKE at: {broke_at:,} parameters 💥")

    if strings:
        max_string = max(v for v, r in strings if r)
        print(f"\nMassive Strings:")
        print(f"  Maximum length survived: {max_string:,} characters")
        broke_at = next((v for v, r in strings if not r), None)
        if broke_at:
            print(f"  BROKE at: {broke_at:,} characters 💥")

    if files:
        max_funcs = max(v for v, r in files if r)
        print(f"\nMassive Files:")
        print(f"  Maximum functions survived: {max_funcs:,} functions")
        broke_at = next((v for v, r in files if not r), None)
        if broke_at:
            print(f"  BROKE at: {broke_at:,} functions 💥")

    correctly_failed = sum(1 for _, r in pathological_results if r == "correctly_failed")
    total_pathological = len(pathological_results)
    print(f"\nPathological Cases:")
    print(f"  Correctly rejected: {correctly_failed}/{total_pathological}")

    print("\n" + "="*60)

    return results, pathological_results


if __name__ == "__main__":
    print("⚠️  WARNING: These tests will try to BREAK the parser!")
    print("⚠️  May consume significant CPU and memory!")
    print("⚠️  Press Ctrl+C to abort at any time")
    print()

    results, pathological = run_break_tests()
