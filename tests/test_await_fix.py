#!/usr/bin/env python3
"""
Test Await Keyword Preservation Fix

Validates that await keywords are properly:
1. Parsed from JavaScript/TypeScript into IRAwait nodes
2. Generated correctly in all target languages
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from language.nodejs_parser_v2 import NodeJSParserV2
from language.python_generator_v2 import generate_python
from language.nodejs_generator_v2 import generate_nodejs
from language.go_generator_v2 import generate_go
from language.rust_generator_v2 import generate_rust
from language.dotnet_generator_v2 import generate_csharp


def test_js_await_to_python():
    """Test JavaScript await → Python await"""
    code = '''
async function fetchData(url) {
    const response = await fetch(url);
    const data = await response.json();
    return data;
}
'''
    parser = NodeJSParserV2()
    ir = parser.parse_source(code, "test")
    python_code = generate_python(ir)

    # Should have 2 await keywords
    await_count = python_code.count('await ')
    assert await_count >= 2, f"Expected 2+ awaits, found {await_count}"
    assert 'await fetch(url)' in python_code or 'await ' in python_code
    print(f"✅ JavaScript → Python: {await_count} await keywords preserved")
    print(f"Generated Python:\n{python_code}\n")
    return True


def test_js_await_to_javascript():
    """Test JavaScript await → JavaScript await (round-trip)"""
    code = '''
async function fetchData(url) {
    const response = await fetch(url);
    const data = await response.json();
    return data;
}
'''
    parser = NodeJSParserV2()
    ir = parser.parse_source(code, "test")
    js_code = generate_nodejs(ir, typescript=False)

    # Should have 2 await keywords
    await_count = js_code.count('await ')
    assert await_count >= 2, f"Expected 2+ awaits, found {await_count}"
    print(f"✅ JavaScript → JavaScript: {await_count} await keywords preserved")
    print(f"Generated JavaScript:\n{js_code}\n")
    return True


def test_js_await_to_typescript():
    """Test JavaScript await → TypeScript await"""
    code = '''
async function fetchData(url) {
    const response = await fetch(url);
    const data = await response.json();
    return data;
}
'''
    parser = NodeJSParserV2()
    ir = parser.parse_source(code, "test")
    ts_code = generate_nodejs(ir, typescript=True)

    # Should have 2 await keywords
    await_count = ts_code.count('await ')
    assert await_count >= 2, f"Expected 2+ awaits, found {await_count}"
    print(f"✅ JavaScript → TypeScript: {await_count} await keywords preserved")
    print(f"Generated TypeScript:\n{ts_code}\n")
    return True


def test_js_await_to_rust():
    """Test JavaScript await → Rust .await (postfix syntax)"""
    code = '''
async function fetchData(url) {
    const response = await fetch(url);
    const data = await response.json();
    return data;
}
'''
    parser = NodeJSParserV2()
    ir = parser.parse_source(code, "test")
    rust_code = generate_rust(ir)

    # Rust uses postfix .await syntax
    await_count = rust_code.count('.await')
    assert await_count >= 2, f"Expected 2+ .awaits, found {await_count}"
    print(f"✅ JavaScript → Rust: {await_count} .await keywords preserved")
    print(f"Generated Rust:\n{rust_code}\n")
    return True


def test_js_await_to_csharp():
    """Test JavaScript await → C# await"""
    code = '''
async function fetchData(url) {
    const response = await fetch(url);
    const data = await response.json();
    return data;
}
'''
    parser = NodeJSParserV2()
    ir = parser.parse_source(code, "test")
    csharp_code = generate_csharp(ir)

    # Should have 2 await keywords
    await_count = csharp_code.count('await ')
    assert await_count >= 2, f"Expected 2+ awaits, found {await_count}"
    print(f"✅ JavaScript → C#: {await_count} await keywords preserved")
    print(f"Generated C#:\n{csharp_code}\n")
    return True


def test_js_await_to_go():
    """Test JavaScript await → Go (no direct equivalent)"""
    code = '''
async function fetchData(url) {
    const response = await fetch(url);
    const data = await response.json();
    return data;
}
'''
    parser = NodeJSParserV2()
    ir = parser.parse_source(code, "test")
    go_code = generate_go(ir)

    # Go doesn't have await - should have comments noting this
    # Just verify it generates without error
    assert len(go_code) > 0, "Go code should be generated"
    print(f"✅ JavaScript → Go: Generated (Go uses goroutines, not await)")
    print(f"Generated Go:\n{go_code}\n")
    return True


def test_complex_await_patterns():
    """Test complex await patterns with chained calls"""
    code = '''
async function processUser(userId) {
    const user = await db.users.findById(userId);
    const posts = await db.posts.findByUser(user.id);
    const comments = await Promise.all(posts.map(async (post) => {
        return await db.comments.findByPost(post.id);
    }));
    return { user, posts, comments };
}
'''
    parser = NodeJSParserV2()
    ir = parser.parse_source(code, "test")
    python_code = generate_python(ir)

    # Should have at least 3 await keywords
    await_count = python_code.count('await ')
    assert await_count >= 3, f"Expected 3+ awaits, found {await_count}"
    print(f"✅ Complex await patterns: {await_count} await keywords preserved")
    print(f"Generated Python:\n{python_code}\n")
    return True


def main():
    print("\n" + "=" * 70)
    print("AWAIT KEYWORD PRESERVATION FIX - COMPREHENSIVE TESTS")
    print("=" * 70)
    print()

    tests = [
        ("JavaScript → Python", test_js_await_to_python),
        ("JavaScript → JavaScript", test_js_await_to_javascript),
        ("JavaScript → TypeScript", test_js_await_to_typescript),
        ("JavaScript → Rust", test_js_await_to_rust),
        ("JavaScript → C#", test_js_await_to_csharp),
        ("JavaScript → Go", test_js_await_to_go),
        ("Complex await patterns", test_complex_await_patterns),
    ]

    results = []
    for name, test_func in tests:
        print(f"\n{'─' * 70}")
        print(f"Test: {name}")
        print('─' * 70)
        try:
            passed = test_func()
            results.append((name, passed))
        except Exception as e:
            print(f"❌ FAILED: {e}")
            import traceback
            traceback.print_exc()
            results.append((name, False))

    # Summary
    print("\n" + "=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)

    passed = sum(1 for _, p in results if p)
    total = len(results)

    for name, p in results:
        status = "✅ PASS" if p else "❌ FAIL"
        print(f"{status}: {name}")

    print(f"\nTotal: {passed}/{total} tests passed ({100 * passed // total}%)")

    if passed == total:
        print("\n🎉 All tests passed! Await keyword preservation is working correctly.")
        return 0
    else:
        print(f"\n⚠️  {total - passed} test(s) failed.")
        return 1


if __name__ == "__main__":
    exit(main())
