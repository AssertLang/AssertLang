#!/usr/bin/env python3
"""
Test: Go Struct Literal Fix

Verifies that Go struct literals are correctly parsed and generated
with named fields, not as function calls.

Issue: User{Name: "Alice", Age: 30} was being generated as User("Alice", 30)
Fix: Generator now detects IRCall with kwargs and generates struct literal syntax
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from language.go_parser_v2 import GoParserV2
from language.go_generator_v2 import generate_go


def test_go_struct_literal_basic():
    """Test basic struct literal with named fields."""
    print("\n" + "="*70)
    print("TEST 1: Basic Struct Literal")
    print("="*70)

    code = '''
package main

type User struct {
    Name string
    Age  int
}

func NewUser() User {
    return User{Name: "Alice", Age: 30}
}
'''
    parser = GoParserV2()
    ir = parser.parse_source(code, "main")
    generated = generate_go(ir)

    print("Input:")
    print(code)
    print("\nGenerated:")
    print(generated)

    # Assertions
    assert 'User{' in generated, "❌ Missing struct literal opening brace"
    assert 'Name:' in generated, "❌ Missing 'Name:' field"
    assert 'Age:' in generated, "❌ Missing 'Age:' field"

    # Check that we don't have tuple-style initialization in the return statement
    # Extract just the function body to avoid matching type signatures
    lines = generated.split('\n')
    for i, line in enumerate(lines):
        if 'return User(' in line and 'User{}' not in line and 'User{Name' not in line:
            raise AssertionError(f"❌ FAIL: Found function call syntax in return: {line.strip()}")

    print("\n✅ PASS: Struct literal correctly generated with named fields")
    return True


def test_go_struct_literal_in_assignment():
    """Test struct literal in variable assignment."""
    print("\n" + "="*70)
    print("TEST 2: Struct Literal in Assignment")
    print("="*70)

    code = '''
package main

type User struct {
    Name string
    Age  int
}

func GetUser(id int) (User, error) {
    user := User{Name: "Alice", Age: 30}
    return user, nil
}
'''
    parser = GoParserV2()
    ir = parser.parse_source(code, "main")
    generated = generate_go(ir)

    print("Input:")
    print(code)
    print("\nGenerated:")
    print(generated)

    # Find the assignment line (skip type declarations)
    lines = generated.split('\n')
    assignment_lines = []
    for line in lines:
        stripped = line.strip()
        # Look for actual usage: assignments or returns with User
        if ('user :=' in stripped or 'return user' in stripped or 'User{' in stripped) and 'type User' not in stripped and 'func ' not in stripped:
            assignment_lines.append(stripped)

    # Should have assignment with struct literal
    has_struct_literal = any('User{' in line for line in assignment_lines)
    assert has_struct_literal, f"❌ No struct literal found in: {assignment_lines}"

    # Should NOT have User() in assignments/returns
    has_func_call = any('User(' in line and 'User{}' not in line and 'User{' not in line for line in assignment_lines)
    assert not has_func_call, f"❌ FAIL: Found function call syntax User() in: {assignment_lines}"

    print("\n✅ PASS: Struct literal in assignment is correct")
    return True


def test_go_struct_literal_multiple_types():
    """Test multiple struct types."""
    print("\n" + "="*70)
    print("TEST 3: Multiple Struct Types")
    print("="*70)

    code = '''
package main

type User struct {
    Name string
    Age  int
}

type Address struct {
    Street string
    City   string
}

func CreateData() (User, Address) {
    u := User{Name: "Bob", Age: 25}
    a := Address{Street: "Main St", City: "NYC"}
    return u, a
}
'''
    parser = GoParserV2()
    ir = parser.parse_source(code, "main")
    generated = generate_go(ir)

    print("Input:")
    print(code)
    print("\nGenerated:")
    print(generated)

    # Both should use struct literal syntax
    assert 'User{' in generated, "❌ Missing User struct literal"
    assert 'Address{' in generated, "❌ Missing Address struct literal"
    assert 'Name:' in generated, "❌ Missing Name field"
    assert 'Street:' in generated, "❌ Missing Street field"

    # Check actual usage (not type signatures)
    lines = generated.split('\n')
    usage_lines = [l.strip() for l in lines if (':=' in l or 'return' in l) and ('User' in l or 'Address' in l)]

    # Should NOT have function call syntax in usage
    for line in usage_lines:
        if 'User(' in line and 'User{' not in line:
            raise AssertionError(f"❌ FAIL: User() function call found in: {line}")
        if 'Address(' in line and 'Address{' not in line:
            raise AssertionError(f"❌ FAIL: Address() function call found in: {line}")

    print("\n✅ PASS: Multiple struct types handled correctly")
    return True


def test_go_struct_literal_empty():
    """Test empty struct literal."""
    print("\n" + "="*70)
    print("TEST 4: Empty Struct Literal")
    print("="*70)

    code = '''
package main

type User struct {
    Name string
    Age  int
}

func NewEmptyUser() User {
    return User{}
}
'''
    parser = GoParserV2()
    ir = parser.parse_source(code, "main")
    generated = generate_go(ir)

    print("Input:")
    print(code)
    print("\nGenerated:")
    print(generated)

    # Empty struct should still use {} not ()
    # Check in actual usage, not type signatures
    lines = generated.split('\n')
    usage_lines = [l.strip() for l in lines if ('return' in l or ':=' in l) and 'User' in l and 'func ' not in l]

    # Should have User{}
    has_empty_struct = any('User{}' in line for line in usage_lines)
    assert has_empty_struct, f"❌ Missing User{{}} in: {usage_lines}"

    # Should NOT have User()
    has_func_call = any('User()' in line for line in usage_lines)
    assert not has_func_call, f"❌ FAIL: Empty struct using function call syntax User() in: {usage_lines}"

    print("\n✅ PASS: Empty struct literal is correct")
    return True


def test_go_function_call_vs_struct_literal():
    """Test that actual function calls are still generated correctly."""
    print("\n" + "="*70)
    print("TEST 5: Function Call vs Struct Literal Distinction")
    print("="*70)

    code = '''
package main

type User struct {
    Name string
}

func DoSomething(name string, age int) {
    // This is a function call, not a struct
    fmt.Println(name, age)
}

func Main() {
    // This is a struct literal
    u := User{Name: "Alice"}

    // This is a function call
    DoSomething("Bob", 30)
}
'''
    parser = GoParserV2()
    ir = parser.parse_source(code, "main")
    generated = generate_go(ir)

    print("Input:")
    print(code)
    print("\nGenerated:")
    print(generated)

    # Struct literal should use {}
    assert 'User{' in generated, "❌ Struct literal should use {}"

    # Function call should use ()
    # Note: DoSomething should be a function call
    assert 'DoSomething(' in generated or 'fmt.Println(' in generated, "❌ Function calls should use ()"

    print("\n✅ PASS: Function calls and struct literals are correctly distinguished")
    return True


def main():
    print("\n" + "="*70)
    print("GO STRUCT LITERAL FIX - VALIDATION TESTS")
    print("="*70)

    tests = [
        ("Basic Struct Literal", test_go_struct_literal_basic),
        ("Struct in Assignment", test_go_struct_literal_in_assignment),
        ("Multiple Struct Types", test_go_struct_literal_multiple_types),
        ("Empty Struct Literal", test_go_struct_literal_empty),
        ("Function vs Struct", test_go_function_call_vs_struct_literal),
    ]

    results = []
    for name, test_func in tests:
        try:
            passed = test_func()
            results.append((name, True))
        except AssertionError as e:
            print(f"\n❌ ASSERTION FAILED: {e}")
            results.append((name, False))
        except Exception as e:
            print(f"\n❌ ERROR: {e}")
            import traceback
            traceback.print_exc()
            results.append((name, False))

    # Summary
    print("\n" + "="*70)
    print("TEST SUMMARY")
    print("="*70)

    passed = sum(1 for _, p in results if p)
    total = len(results)

    for name, p in results:
        status = "✅ PASS" if p else "❌ FAIL"
        print(f"{status}: {name}")

    print(f"\nTotal: {passed}/{total} tests passed ({100*passed//total}%)")

    return 0 if passed == total else 1


if __name__ == "__main__":
    exit(main())
