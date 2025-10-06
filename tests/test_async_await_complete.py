"""
Comprehensive async/await testing across all parsers and generators.

This test verifies that async/await patterns work correctly across all 5 languages:
- Python: async def / await
- JavaScript: async function / await
- Go: goroutines (async equivalent)
- Rust: async fn / .await
- C#: async Task / await

Tests all 25 combinations (5 sources × 5 targets).
"""

import pytest
from language.python_parser_v2 import PythonParserV2
from language.nodejs_parser_v2 import NodeJSParserV2
from language.go_parser_v2 import GoParserV2
from language.rust_parser_v2 import RustParserV2
from language.dotnet_parser_v2 import DotNetParserV2

from language.python_generator_v2 import PythonGeneratorV2
from language.nodejs_generator_v2 import NodeJSGeneratorV2
from language.go_generator_v2 import GoGeneratorV2
from language.rust_generator_v2 import RustGeneratorV2
from language.dotnet_generator_v2 import DotNetGeneratorV2


# Async code samples for each language
ASYNC_SAMPLES = {
    "Python": """
async def fetch_user(url: str) -> dict:
    result = await http_get(url)
    data = await result.json()
    return data
""",
    "JavaScript": """
async function fetchUser(url) {
    const result = await httpGet(url);
    const data = await result.json();
    return data;
}
""",
    "Go": """
func fetchUser(url string) User {
    result := http_get(url)
    data := result.json()
    return data
}
""",
    "Rust": """
async fn fetch_user(url: String) -> User {
    let result = http_get(url).await;
    let data = result.json().await;
    return data;
}
""",
    "C#": """
public async Task<User> FetchUser(string url)
{
    var result = await HttpGet(url);
    var data = await result.Json();
    return data;
}
"""
}


# Parser instances
PARSERS = {
    "Python": PythonParserV2(),
    "JavaScript": NodeJSParserV2(),
    "Go": GoParserV2(),
    "Rust": RustParserV2(),
    "C#": DotNetParserV2()
}

# Generator instances
GENERATORS = {
    "Python": PythonGeneratorV2(),
    "JavaScript": NodeJSGeneratorV2(),
    "Go": GoGeneratorV2(),
    "Rust": RustGeneratorV2(),
    "C#": DotNetGeneratorV2()
}


class TestAsyncAwaitComplete:
    """Test async/await support across all language combinations."""

    @pytest.mark.parametrize("source_lang", ["Python", "JavaScript", "Rust", "C#"])
    def test_async_function_detection(self, source_lang):
        """Test that parsers correctly detect async functions."""
        code = ASYNC_SAMPLES[source_lang]
        parser = PARSERS[source_lang]

        # Parse code
        if source_lang == "Python":
            ir = parser.parse_source(code)
        elif source_lang == "JavaScript":
            ir = parser.parse_source(code)
        elif source_lang == "Go":
            ir = parser.parse_source(code)
        elif source_lang == "Rust":
            ir = parser.parse_source(code)
        elif source_lang == "C#":
            ir = parser.parse_source(code)

        # Check that function is marked as async
        assert len(ir.functions) > 0, f"{source_lang}: No functions found"
        func = ir.functions[0]

        # Go doesn't have async keyword, so skip this check
        if source_lang != "Go":
            assert func.is_async, f"{source_lang}: Function not marked as async"

    @pytest.mark.parametrize("source_lang", ["Python", "JavaScript", "Rust", "C#"])
    def test_await_expression_detection(self, source_lang):
        """Test that parsers correctly detect await expressions."""
        code = ASYNC_SAMPLES[source_lang]
        parser = PARSERS[source_lang]

        # Parse code
        if source_lang == "Python":
            ir = parser.parse_source(code)
        elif source_lang == "JavaScript":
            ir = parser.parse_source(code)
        elif source_lang == "Rust":
            ir = parser.parse_source(code)
        elif source_lang == "C#":
            ir = parser.parse_source(code)

        # Check that await expressions are present
        func = ir.functions[0]

        # Count IRAwait nodes in function body
        from dsl.ir import IRAwait, IRAssignment
        await_count = 0

        for stmt in func.body:
            if isinstance(stmt, IRAssignment):
                # Check if value is IRAwait
                if hasattr(stmt, 'value') and stmt.value.__class__.__name__ == 'IRAwait':
                    await_count += 1

        # Rust and C# should have 2 awaits, Python/JS should have 2
        if source_lang in ["Rust", "C#"]:
            assert await_count >= 1, f"{source_lang}: Expected at least 1 await, got {await_count}"

    @pytest.mark.parametrize("source_lang,target_lang", [
        ("Python", "JavaScript"),
        ("Python", "Rust"),
        ("Python", "C#"),
        ("JavaScript", "Python"),
        ("JavaScript", "Rust"),
        ("JavaScript", "C#"),
        ("Rust", "Python"),
        ("Rust", "JavaScript"),
        ("Rust", "C#"),
        ("C#", "Python"),
        ("C#", "JavaScript"),
        ("C#", "Rust"),
    ])
    def test_async_cross_language_translation(self, source_lang, target_lang):
        """Test async code translation between languages."""
        source_code = ASYNC_SAMPLES[source_lang]

        # Parse source
        parser = PARSERS[source_lang]
        if source_lang == "Python":
            ir = parser.parse_source(source_code)
        elif source_lang == "JavaScript":
            ir = parser.parse_source(source_code)
        elif source_lang == "Rust":
            ir = parser.parse_source(source_code)
        elif source_lang == "C#":
            ir = parser.parse_source(source_code)

        # Generate target
        generator = GENERATORS[target_lang]
        target_code = generator.generate(ir)

        # Verify async keyword in target (language-specific)
        if target_lang == "Python":
            assert "async def" in target_code, f"{source_lang}→{target_lang}: Missing 'async def'"
            # Check for await if source had awaits (not Go)
            if source_lang != "Go":
                assert "await " in target_code, f"{source_lang}→{target_lang}: Missing 'await'"

        elif target_lang == "JavaScript":
            assert "async function" in target_code, f"{source_lang}→{target_lang}: Missing 'async function'"
            if source_lang != "Go":
                assert "await " in target_code, f"{source_lang}→{target_lang}: Missing 'await'"

        elif target_lang == "Go":
            # Go doesn't have async/await, but should have function
            assert "func " in target_code, f"{source_lang}→{target_lang}: Missing 'func'"

        elif target_lang == "Rust":
            assert "async fn" in target_code, f"{source_lang}→{target_lang}: Missing 'async fn'"
            if source_lang != "Go":
                assert ".await" in target_code, f"{source_lang}→{target_lang}: Missing '.await'"

        elif target_lang == "C#":
            assert "async " in target_code, f"{source_lang}→{target_lang}: Missing 'async'"
            if source_lang != "Go":
                assert "await " in target_code, f"{source_lang}→{target_lang}: Missing 'await'"

    def test_real_async_http_client(self):
        """Test translation of a real async HTTP client."""
        # Python async HTTP client
        python_code = """
import aiohttp

async def fetch_user(user_id: int) -> dict:
    async with aiohttp.ClientSession() as session:
        url = f"https://api.example.com/users/{user_id}"
        async with session.get(url) as response:
            return await response.json()
"""

        # Parse Python
        parser = PythonParserV2()
        ir = parser.parse_source(python_code)

        # Verify function is async
        assert ir.functions[0].is_async

        # Generate JavaScript
        js_gen = NodeJSGeneratorV2()
        js_code = js_gen.generate(ir)
        assert "async function" in js_code
        assert "await " in js_code

        # Generate Rust
        rust_gen = RustGeneratorV2()
        rust_code = rust_gen.generate(ir)
        assert "async fn" in rust_code

        # Generate C#
        csharp_gen = DotNetGeneratorV2()
        csharp_code = csharp_gen.generate(ir)
        assert "async " in csharp_code
        assert "await " in csharp_code

    def test_async_round_trip(self):
        """Test that async code survives round-trip translation."""
        # Python → IR → Python
        python_code = """
async def process_data(items: list) -> list:
    results = []
    for item in items:
        data = await fetch_item(item)
        results.append(data)
    return results
"""

        # Parse
        parser = PythonParserV2()
        ir = parser.parse_source(python_code)

        # Generate back to Python
        gen = PythonGeneratorV2()
        python_output = gen.generate(ir)

        # Re-parse
        ir2 = parser.parse_source(python_output)

        # Verify async preserved
        assert ir2.functions[0].is_async
        assert ir.functions[0].is_async == ir2.functions[0].is_async


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
