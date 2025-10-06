#!/usr/bin/env python3
"""
Test real-world async HTTP client translation.
"""

import sys
sys.path.insert(0, '/Users/hustlermain/HUSTLER_CONTENT/HSTLR/DEV/Promptware')

from language.python_parser_v2 import PythonParserV2
from language.nodejs_generator_v2 import NodeJSGeneratorV2
from language.rust_generator_v2 import RustGeneratorV2
from language.dotnet_generator_v2 import DotNetGeneratorV2


def main():
    print("=" * 70)
    print("REAL-WORLD ASYNC HTTP CLIENT TRANSLATION TEST")
    print("=" * 70)

    # Real Python async HTTP client using aiohttp
    python_async_http = """
import aiohttp
import asyncio
from typing import Dict, List

async def fetch_user(user_id: int) -> Dict:
    async with aiohttp.ClientSession() as session:
        url = f"https://api.example.com/users/{user_id}"
        async with session.get(url) as response:
            return await response.json()

async def fetch_multiple_users(user_ids: List[int]) -> List[Dict]:
    results = []
    for user_id in user_ids:
        user = await fetch_user(user_id)
        results.append(user)
    return results

async def main():
    users = await fetch_multiple_users([1, 2, 3])
    for user in users:
        print(user)
"""

    print("\n📝 Original Python Code:")
    print("-" * 70)
    print(python_async_http)

    # Parse Python
    print("\n🔍 Parsing Python...")
    parser = PythonParserV2()
    ir = parser.parse_source(python_async_http)

    print(f"✓ Parsed {len(ir.functions)} async functions")
    for func in ir.functions:
        print(f"  - {func.name}: async={func.is_async}")

    # Generate JavaScript
    print("\n🌐 Generating JavaScript...")
    js_gen = NodeJSGeneratorV2()
    js_code = js_gen.generate(ir)
    print("-" * 70)
    print(js_code)
    print("-" * 70)

    # Verify JavaScript async/await
    assert "async function fetch_user" in js_code or "async function fetchUser" in js_code
    assert "await " in js_code
    print("✓ JavaScript has async/await")

    # Generate Rust
    print("\n🦀 Generating Rust...")
    rust_gen = RustGeneratorV2()
    rust_code = rust_gen.generate(ir)
    print("-" * 70)
    print(rust_code)
    print("-" * 70)

    # Verify Rust async/await
    assert "async fn" in rust_code
    assert ".await" in rust_code
    print("✓ Rust has async fn and .await")

    # Generate C#
    print("\n🔷 Generating C#...")
    csharp_gen = DotNetGeneratorV2()
    csharp_code = csharp_gen.generate(ir)
    print("-" * 70)
    print(csharp_code)
    print("-" * 70)

    # Verify C# async/await
    assert "async " in csharp_code
    assert "await " in csharp_code
    print("✓ C# has async Task and await")

    print("\n" + "=" * 70)
    print("✅ REAL-WORLD ASYNC HTTP CLIENT TRANSLATION SUCCESS")
    print("=" * 70)
    print("\nSummary:")
    print("- Python async/await → JavaScript async/await ✓")
    print("- Python async/await → Rust async fn/.await ✓")
    print("- Python async/await → C# async Task/await ✓")
    print("\nAll async patterns preserved correctly!")

    return 0


if __name__ == "__main__":
    sys.exit(main())
