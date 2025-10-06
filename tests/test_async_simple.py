#!/usr/bin/env python3
"""
Simple async/await test without pytest.
Tests all parsers and generators for async support.
"""

import sys
sys.path.insert(0, '/Users/hustlermain/HUSTLER_CONTENT/HSTLR/DEV/Promptware')

from language.python_parser_v2 import PythonParserV2
from language.nodejs_parser_v2 import NodeJSParserV2
from language.rust_parser_v2 import RustParserV2
from language.dotnet_parser_v2 import DotNetParserV2

from language.python_generator_v2 import PythonGeneratorV2
from language.nodejs_generator_v2 import NodeJSGeneratorV2
from language.rust_generator_v2 import RustGeneratorV2
from language.dotnet_generator_v2 import DotNetGeneratorV2

from dsl.ir import IRAwait


def test_python_async():
    """Test Python async/await parsing."""
    print("Testing Python async/await...")

    code = """
async def fetch_user(url: str) -> dict:
    result = await http_get(url)
    data = await result.json()
    return data
"""

    parser = PythonParserV2()
    ir = parser.parse_source(code)

    # Check function is async
    assert len(ir.functions) == 1, "Expected 1 function"
    func = ir.functions[0]
    assert func.is_async, "Function should be marked as async"

    # Check for await expressions
    await_count = 0
    for stmt in func.body:
        if hasattr(stmt, 'value') and isinstance(stmt.value, IRAwait):
            await_count += 1

    assert await_count >= 1, f"Expected at least 1 await, got {await_count}"

    print("✓ Python async/await parsing works")
    return ir


def test_javascript_async():
    """Test JavaScript async/await parsing."""
    print("Testing JavaScript async/await...")

    code = """
async function fetchUser(url) {
    const result = await httpGet(url);
    const data = await result.json();
    return data;
}
"""

    parser = NodeJSParserV2()
    ir = parser.parse_source(code)

    # Check function is async
    assert len(ir.functions) == 1, "Expected 1 function"
    func = ir.functions[0]
    assert func.is_async, "Function should be marked as async"

    # Check for await expressions
    await_count = 0
    for stmt in func.body:
        if hasattr(stmt, 'value') and isinstance(stmt.value, IRAwait):
            await_count += 1

    assert await_count >= 1, f"Expected at least 1 await, got {await_count}"

    print("✓ JavaScript async/await parsing works")
    return ir


def test_rust_async():
    """Test Rust async/await parsing."""
    print("Testing Rust async/await...")

    code = """
async fn fetch_user(url: String) -> User {
    let result = http_get(url).await;
    let data = result.json().await;
    return data;
}
"""

    parser = RustParserV2()
    ir = parser.parse_source(code)

    # Check function is async
    assert len(ir.functions) == 1, "Expected 1 function"
    func = ir.functions[0]
    assert func.is_async, "Function should be marked as async"

    # Check for await expressions
    await_count = 0
    for stmt in func.body:
        if hasattr(stmt, 'value') and isinstance(stmt.value, IRAwait):
            await_count += 1

    assert await_count >= 1, f"Expected at least 1 await, got {await_count}"

    print("✓ Rust async/await parsing works")
    return ir


def test_csharp_async():
    """Test C# async/await parsing."""
    print("Testing C# async/await...")

    # C# requires class context for methods
    code = """
public class UserService
{
    public async Task<User> FetchUser(string url)
    {
        var result = await HttpGet(url);
        var data = await result.Json();
        return data;
    }
}
"""

    parser = DotNetParserV2()
    ir = parser.parse_source(code)

    # Check class and method
    assert len(ir.classes) == 1, "Expected 1 class"
    cls = ir.classes[0]
    assert len(cls.methods) == 1, "Expected 1 method"

    func = cls.methods[0]
    assert func.is_async, "Method should be marked as async"

    # Check for await expressions
    await_count = 0
    for stmt in func.body:
        if hasattr(stmt, 'value') and isinstance(stmt.value, IRAwait):
            await_count += 1

    assert await_count >= 1, f"Expected at least 1 await, got {await_count}"

    print("✓ C# async/await parsing works")
    return ir


def test_cross_language_generation():
    """Test async code generation across languages."""
    print("\nTesting cross-language async generation...")

    # Parse Python async code
    python_code = """
async def fetch_data(url: str) -> dict:
    result = await http_get(url)
    return await result.json()
"""

    parser = PythonParserV2()
    ir = parser.parse_source(python_code)

    # Test all generators
    generators = {
        "Python": PythonGeneratorV2(),
        "JavaScript": NodeJSGeneratorV2(),
        "Rust": RustGeneratorV2(),
        "C#": DotNetGeneratorV2()
    }

    results = {}
    for lang, gen in generators.items():
        code = gen.generate(ir)
        results[lang] = code
        print(f"✓ Generated {lang} code")

    # Verify async keywords
    assert "async def" in results["Python"], "Python: Missing 'async def'"
    assert "await " in results["Python"], "Python: Missing 'await'"

    assert "async function" in results["JavaScript"], "JavaScript: Missing 'async function'"
    assert "await " in results["JavaScript"], "JavaScript: Missing 'await'"

    assert "async fn" in results["Rust"], "Rust: Missing 'async fn'"
    assert ".await" in results["Rust"], "Rust: Missing '.await'"

    assert "async " in results["C#"], "C#: Missing 'async'"
    assert "await " in results["C#"], "C#: Missing 'await'"

    print("✓ All generators produce correct async code")

    return results


def test_round_trip():
    """Test Python → IR → Python preserves async."""
    print("\nTesting round-trip async preservation...")

    original_code = """
async def process_items(items: list) -> list:
    results = []
    for item in items:
        data = await fetch_item(item)
        results.append(data)
    return results
"""

    # Parse
    parser = PythonParserV2()
    ir1 = parser.parse_source(original_code)

    # Generate
    gen = PythonGeneratorV2()
    generated_code = gen.generate(ir1)

    # Re-parse
    ir2 = parser.parse_source(generated_code)

    # Verify async preserved
    assert ir1.functions[0].is_async == ir2.functions[0].is_async
    assert ir1.functions[0].is_async, "Async flag not preserved"

    print("✓ Round-trip preserves async")


def main():
    """Run all tests."""
    print("=" * 60)
    print("ASYNC/AWAIT COMPREHENSIVE TEST")
    print("=" * 60)

    try:
        # Test each parser
        test_python_async()
        test_javascript_async()
        test_rust_async()
        test_csharp_async()

        # Test cross-language generation
        test_cross_language_generation()

        # Test round-trip
        test_round_trip()

        print("\n" + "=" * 60)
        print("ALL ASYNC/AWAIT TESTS PASSED ✓")
        print("=" * 60)
        return 0

    except AssertionError as e:
        print(f"\n❌ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        return 1
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
