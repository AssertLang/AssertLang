"""
Test f-string parsing and code generation fix.

This test ensures that Python f-strings are properly converted to:
- JavaScript template literals (`...`)
- NOT str() function calls
"""

import pytest
from language.python_parser_v2 import PythonParserV2
from language.nodejs_generator_v2 import generate_nodejs
from dsl.ir import IRFString


def test_simple_fstring_parsing():
    """Test that f-strings are parsed into IRFString nodes."""
    code = '''
def greet(name):
    message = f"Hello, {name}!"
    return message
'''
    parser = PythonParserV2()
    ir = parser.parse_source(code, "test")

    # Check we have a function
    assert len(ir.functions) == 1
    func = ir.functions[0]

    # Check assignment to message
    assert len(func.body) >= 1
    assignment = func.body[0]

    # Check that the value is an IRFString
    assert isinstance(assignment.value, IRFString)
    assert len(assignment.value.parts) == 3
    assert assignment.value.parts[0] == "Hello, "
    # parts[1] is the IRIdentifier for 'name'
    assert assignment.value.parts[2] == "!"


def test_fstring_to_javascript():
    """Test f-string converts to template literal, not str() calls."""
    code = '''
def greet(name):
    message = f"Hello, {name}!"
    return message
'''
    parser = PythonParserV2()
    ir = parser.parse_source(code, "test")
    js_code = generate_nodejs(ir, typescript=False)

    # Should use template literal
    assert '`Hello, ${name}!`' in js_code

    # Should NOT have str() calls
    assert 'str(' not in js_code


def test_fstring_to_typescript():
    """Test f-string converts to template literal in TypeScript."""
    code = '''
def greet(name):
    message = f"Hello, {name}!"
    return message
'''
    parser = PythonParserV2()
    ir = parser.parse_source(code, "test")
    ts_code = generate_nodejs(ir, typescript=True)

    # Should use template literal
    assert '`Hello, ${name}!`' in ts_code

    # Should NOT have str() calls
    assert 'str(' not in ts_code


def test_complex_fstring():
    """Test f-string with multiple interpolations."""
    code = '''
def format_user(user_id, username, email):
    result = f"User {user_id}: {username} ({email})"
    return result
'''
    parser = PythonParserV2()
    ir = parser.parse_source(code, "test")
    js_code = generate_nodejs(ir, typescript=False)

    # Should use template literal with all interpolations
    assert '`User ${user_id}: ${username} (${email})`' in js_code

    # Should NOT have str() calls
    assert 'str(' not in js_code


def test_fstring_with_expression():
    """Test f-string with complex expressions."""
    code = '''
def calculate(a, b):
    result = f"The sum of {a} and {b} is {a + b}"
    return result
'''
    parser = PythonParserV2()
    ir = parser.parse_source(code, "test")
    js_code = generate_nodejs(ir, typescript=False)

    # Should use template literal
    assert '`The sum of ${a} and ${b} is ${' in js_code
    assert 'a + b' in js_code

    # Should NOT have str() calls
    assert 'str(' not in js_code


def test_fstring_with_property_access():
    """Test f-string with property access."""
    code = '''
def format_user(user):
    message = f"Hello, {user.name}! Your ID is {user.id}."
    return message
'''
    parser = PythonParserV2()
    ir = parser.parse_source(code, "test")
    js_code = generate_nodejs(ir, typescript=False)

    # Should use template literal with property access
    assert '`Hello, ${user.name}! Your ID is ${user.id}.`' in js_code

    # Should NOT have str() calls
    assert 'str(' not in js_code


def test_empty_fstring():
    """Test empty f-string."""
    code = '''
def empty():
    message = f""
    return message
'''
    parser = PythonParserV2()
    ir = parser.parse_source(code, "test")
    js_code = generate_nodejs(ir, typescript=False)

    # Should generate empty string
    assert '""' in js_code


def test_fstring_with_special_chars():
    """Test f-string with special characters that need escaping."""
    code = r'''
def special(name):
    message = f"Hello, {name}! This has a `backtick` in it."
    return message
'''
    parser = PythonParserV2()
    ir = parser.parse_source(code, "test")
    js_code = generate_nodejs(ir, typescript=False)

    # Should escape backticks
    assert r'\`backtick\`' in js_code

    # Should NOT have str() calls
    assert 'str(' not in js_code


if __name__ == "__main__":
    # Run tests
    test_simple_fstring_parsing()
    print("✅ test_simple_fstring_parsing passed")

    test_fstring_to_javascript()
    print("✅ test_fstring_to_javascript passed")

    test_fstring_to_typescript()
    print("✅ test_fstring_to_typescript passed")

    test_complex_fstring()
    print("✅ test_complex_fstring passed")

    test_fstring_with_expression()
    print("✅ test_fstring_with_expression passed")

    test_fstring_with_property_access()
    print("✅ test_fstring_with_property_access passed")

    test_empty_fstring()
    print("✅ test_empty_fstring passed")

    test_fstring_with_special_chars()
    print("✅ test_fstring_with_special_chars passed")

    print("\n🎉 All f-string tests passed!")
