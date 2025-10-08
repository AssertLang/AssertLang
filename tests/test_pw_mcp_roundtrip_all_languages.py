#!/usr/bin/env python3
"""
Test PW MCP server round-trip translation across all 5 languages.

Tests:
1. Python → PW → Python
2. Go → PW → Go
3. Rust → PW → Rust
4. TypeScript → PW → TypeScript
5. C# → PW → C#
6. Cross-language: Python → PW → Go/Rust/TypeScript/C#
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))
sys.path.insert(0, str(Path(__file__).parent.parent / "pw-syntax-mcp-server"))

from translators.python_bridge import python_to_pw, pw_to_python
from translators.go_bridge import go_to_pw, pw_to_go
from translators.rust_bridge import rust_to_pw, pw_to_rust
from translators.typescript_bridge import typescript_to_pw, pw_to_typescript
from translators.csharp_bridge import csharp_to_pw, pw_to_csharp


# Test code samples (simple function with control flow)
test_samples = {
    "python": '''
def calculate(x, y):
    if x > y:
        result = x + y
        return result * 2
    else:
        return x - y
''',
    "go": '''
package main

func calculate(x int, y int) int {
    if x > y {
        result := x + y
        return result * 2
    } else {
        return x - y
    }
}
''',
    "rust": '''
pub fn calculate(x: i32, y: i32) -> i32 {
    if x > y {
        let result = x + y;
        result * 2
    } else {
        x - y
    }
}
''',
    "typescript": '''
function calculate(x: number, y: number): number {
    if (x > y) {
        const result = x + y;
        return result * 2;
    } else {
        return x - y;
    }
}
''',
    "csharp": '''
public class Calculator {
    public int Calculate(int x, int y) {
        if (x > y) {
            int result = x + y;
            return result * 2;
        } else {
            return x - y;
        }
    }
}
'''
}


def test_python_roundtrip():
    """Test Python → PW → Python"""
    print("\n" + "="*70)
    print("TEST: Python → PW → Python")
    print("="*70)

    code = test_samples["python"]
    print(f"\nOriginal Python:\n{code}")

    # Python → PW
    pw_tree = python_to_pw(code)
    print(f"\nPW Tree generated: {len(str(pw_tree))} chars")

    # PW → Python
    result = pw_to_python(pw_tree)
    print(f"\nGenerated Python:\n{result}")

    print("\n✅ Python round-trip complete")
    return True


def test_go_roundtrip():
    """Test Go → PW → Go"""
    print("\n" + "="*70)
    print("TEST: Go → PW → Go")
    print("="*70)

    code = test_samples["go"]
    print(f"\nOriginal Go:\n{code}")

    # Go → PW
    pw_tree = go_to_pw(code)
    print(f"\nPW Tree generated: {len(str(pw_tree))} chars")

    # PW → Go
    result = pw_to_go(pw_tree)
    print(f"\nGenerated Go:\n{result}")

    print("\n✅ Go round-trip complete")
    return True


def test_rust_roundtrip():
    """Test Rust → PW → Rust"""
    print("\n" + "="*70)
    print("TEST: Rust → PW → Rust")
    print("="*70)

    code = test_samples["rust"]
    print(f"\nOriginal Rust:\n{code}")

    # Rust → PW
    pw_tree = rust_to_pw(code)
    print(f"\nPW Tree generated: {len(str(pw_tree))} chars")

    # PW → Rust
    result = pw_to_rust(pw_tree)
    print(f"\nGenerated Rust:\n{result}")

    print("\n✅ Rust round-trip complete")
    return True


def test_typescript_roundtrip():
    """Test TypeScript → PW → TypeScript"""
    print("\n" + "="*70)
    print("TEST: TypeScript → PW → TypeScript")
    print("="*70)

    code = test_samples["typescript"]
    print(f"\nOriginal TypeScript:\n{code}")

    # TypeScript → PW
    pw_tree = typescript_to_pw(code)
    print(f"\nPW Tree generated: {len(str(pw_tree))} chars")

    # PW → TypeScript
    result = pw_to_typescript(pw_tree)
    print(f"\nGenerated TypeScript:\n{result}")

    print("\n✅ TypeScript round-trip complete")
    return True


def test_csharp_roundtrip():
    """Test C# → PW → C#"""
    print("\n" + "="*70)
    print("TEST: C# → PW → C#")
    print("="*70)

    code = test_samples["csharp"]
    print(f"\nOriginal C#:\n{code}")

    # C# → PW
    pw_tree = csharp_to_pw(code)
    print(f"\nPW Tree generated: {len(str(pw_tree))} chars")

    # PW → C#
    result = pw_to_csharp(pw_tree)
    print(f"\nGenerated C#:\n{result}")

    print("\n✅ C# round-trip complete")
    return True


def test_cross_language_python_to_go():
    """Test Python → PW → Go"""
    print("\n" + "="*70)
    print("TEST: Python → PW → Go (Cross-Language)")
    print("="*70)

    code = test_samples["python"]
    print(f"\nOriginal Python:\n{code}")

    # Python → PW
    pw_tree = python_to_pw(code)

    # PW → Go
    result = pw_to_go(pw_tree)
    print(f"\nGenerated Go:\n{result}")

    print("\n✅ Cross-language Python → Go complete")
    return True


def test_cross_language_go_to_rust():
    """Test Go → PW → Rust"""
    print("\n" + "="*70)
    print("TEST: Go → PW → Rust (Cross-Language)")
    print("="*70)

    code = test_samples["go"]
    print(f"\nOriginal Go:\n{code}")

    # Go → PW
    pw_tree = go_to_pw(code)

    # PW → Rust
    result = pw_to_rust(pw_tree)
    print(f"\nGenerated Rust:\n{result}")

    print("\n✅ Cross-language Go → Rust complete")
    return True


def test_cross_language_rust_to_typescript():
    """Test Rust → PW → TypeScript"""
    print("\n" + "="*70)
    print("TEST: Rust → PW → TypeScript (Cross-Language)")
    print("="*70)

    code = test_samples["rust"]
    print(f"\nOriginal Rust:\n{code}")

    # Rust → PW
    pw_tree = rust_to_pw(code)

    # PW → TypeScript
    result = pw_to_typescript(pw_tree)
    print(f"\nGenerated TypeScript:\n{result}")

    print("\n✅ Cross-language Rust → TypeScript complete")
    return True


def test_cross_language_typescript_to_csharp():
    """Test TypeScript → PW → C#"""
    print("\n" + "="*70)
    print("TEST: TypeScript → PW → C# (Cross-Language)")
    print("="*70)

    code = test_samples["typescript"]
    print(f"\nOriginal TypeScript:\n{code}")

    # TypeScript → PW
    pw_tree = typescript_to_pw(code)

    # PW → C#
    result = pw_to_csharp(pw_tree)
    print(f"\nGenerated C#:\n{result}")

    print("\n✅ Cross-language TypeScript → C# complete")
    return True


def main():
    """Run all tests"""
    print("="*70)
    print("PW MCP Server - All Languages Round-Trip Tests")
    print("="*70)

    tests = [
        ("Python round-trip", test_python_roundtrip),
        ("Go round-trip", test_go_roundtrip),
        ("Rust round-trip", test_rust_roundtrip),
        ("TypeScript round-trip", test_typescript_roundtrip),
        ("C# round-trip", test_csharp_roundtrip),
        ("Python → Go", test_cross_language_python_to_go),
        ("Go → Rust", test_cross_language_go_to_rust),
        ("Rust → TypeScript", test_cross_language_rust_to_typescript),
        ("TypeScript → C#", test_cross_language_typescript_to_csharp),
    ]

    passed = 0
    failed = 0
    errors = []

    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
            else:
                failed += 1
                errors.append(f"{test_name}: Unknown failure")
        except Exception as e:
            failed += 1
            errors.append(f"{test_name}: {str(e)}")
            print(f"\n❌ {test_name} failed: {str(e)}")

    print("\n" + "="*70)
    print("SUMMARY")
    print("="*70)
    print(f"Total tests: {len(tests)}")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")

    if errors:
        print("\nErrors:")
        for error in errors:
            print(f"  - {error}")

    if failed == 0:
        print("\n✅ All tests passed!")
        return 0
    else:
        print(f"\n❌ {failed} test(s) failed")
        return 1


if __name__ == "__main__":
    sys.exit(main())
