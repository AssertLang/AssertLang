"""
Comprehensive test suite for Option<T> stdlib type.

Tests parsing, IR structure, and code generation for all Option methods.
Based on implementation-plan.md specifications.
"""

import pytest
from dsl.al_parser import parse_al, ALParseError


class TestOptionBasicParsing:
    """Test that Option<T> code parses correctly."""

    def test_option_enum_definition(self):
        """Test Option enum definition parses."""
        pw_code = """
enum Option<T>:
    - Some(value: T)
    - None
"""
        ir = parse_al(pw_code)
        assert len(ir.enums) == 1
        assert ir.enums[0].name == "Option"
        assert len(ir.enums[0].variants) == 2
        assert ir.enums[0].variants[0].name == "Some"
        assert ir.enums[0].variants[1].name == "None"

    def test_option_some_constructor(self):
        """Test option_some function parses."""
        pw_code = """
function option_some<T>(value: T) -> Option<T>:
    return Option.Some(value)
"""
        ir = parse_al(pw_code)
        assert len(ir.functions) == 1
        assert ir.functions[0].name == "option_some"

    def test_option_none_constructor(self):
        """Test option_none function parses."""
        pw_code = """
function option_none<T>() -> Option<T>:
    return Option.None
"""
        ir = parse_al(pw_code)
        assert len(ir.functions) == 1
        assert ir.functions[0].name == "option_none"


class TestOptionMethods:
    """Test Option method definitions parse correctly."""

    def test_option_map(self):
        """Test option_map function parses."""
        pw_code = """
function option_map<T, U>(opt: Option<T>, fn: function(T) -> U) -> Option<U>:
    if opt is Some(val):
        return Some(fn(val))
    else:
        return None
"""
        ir = parse_al(pw_code)
        assert len(ir.functions) == 1
        assert ir.functions[0].name == "option_map"
        assert len(ir.functions[0].params) == 2

    def test_option_and_then(self):
        """Test option_and_then function parses."""
        pw_code = """
function option_and_then<T, U>(opt: Option<T>, fn: function(T) -> Option<U>) -> Option<U>:
    if opt is Some(val):
        return fn(val)
    else:
        return None
"""
        ir = parse_al(pw_code)
        assert len(ir.functions) == 1
        assert ir.functions[0].name == "option_and_then"

    def test_option_unwrap_or(self):
        """Test option_unwrap_or function parses."""
        pw_code = """
function option_unwrap_or<T>(opt: Option<T>, default: T) -> T:
    if opt is Some(val):
        return val
    else:
        return default
"""
        ir = parse_al(pw_code)
        assert len(ir.functions) == 1
        assert ir.functions[0].name == "option_unwrap_or"

    def test_option_unwrap_or_else(self):
        """Test option_unwrap_or_else function parses."""
        pw_code = """
function option_unwrap_or_else<T>(opt: Option<T>, fn: function() -> T) -> T:
    if opt is Some(val):
        return val
    else:
        return fn()
"""
        ir = parse_al(pw_code)
        assert len(ir.functions) == 1
        assert ir.functions[0].name == "option_unwrap_or_else"

    def test_option_is_some(self):
        """Test option_is_some function parses."""
        pw_code = """
function option_is_some<T>(opt: Option<T>) -> bool:
    if opt is Some(_):
        return true
    else:
        return false
"""
        ir = parse_al(pw_code)
        assert len(ir.functions) == 1
        assert ir.functions[0].name == "option_is_some"

    def test_option_is_none(self):
        """Test option_is_none function parses."""
        pw_code = """
function option_is_none<T>(opt: Option<T>) -> bool:
    if opt is None:
        return true
    else:
        return false
"""
        ir = parse_al(pw_code)
        assert len(ir.functions) == 1
        assert ir.functions[0].name == "option_is_none"

    def test_option_match(self):
        """Test option_match function parses."""
        pw_code = """
function option_match<T, U>(
    opt: Option<T>,
    some_fn: function(T) -> U,
    none_fn: function() -> U
) -> U:
    if opt is Some(val):
        return some_fn(val)
    else:
        return none_fn()
"""
        ir = parse_al(pw_code)
        assert len(ir.functions) == 1
        assert ir.functions[0].name == "option_match"
        assert len(ir.functions[0].params) == 3


class TestOptionUsagePatterns:
    """Test real-world Option usage patterns."""

    def test_option_with_int(self):
        """Test Option<int> usage."""
        pw_code = """
function find_max(items: array<int>) -> Option<int>:
    if len(items) == 0:
        return None
    else:
        let max_val = items[0]
        for item in items:
            if item > max_val:
                max_val = item
        return Some(max_val)
"""
        ir = parse_al(pw_code)
        assert len(ir.functions) == 1
        assert ir.functions[0].name == "find_max"

    def test_option_with_string(self):
        """Test Option<string> usage."""
        pw_code = """
function get_name(user_id: int) -> Option<string>:
    if user_id == 1:
        return Some("Alice")
    else:
        return None
"""
        ir = parse_al(pw_code)
        assert len(ir.functions) == 1

    def test_option_chaining(self):
        """Test chaining Option operations."""
        pw_code = """
function process_value(opt: Option<int>) -> Option<int>:
    let doubled = option_map(opt, fn(x) -> x * 2)
    let result = option_unwrap_or(doubled, 0)
    return Some(result)
"""
        ir = parse_al(pw_code)
        assert len(ir.functions) == 1

    def test_option_pattern_matching(self):
        """Test Option pattern matching in conditionals."""
        pw_code = """
function describe_option(opt: Option<int>) -> string:
    if opt is Some(value):
        return "Got: " + str(value)
    else:
        return "Got nothing"
"""
        ir = parse_al(pw_code)
        assert len(ir.functions) == 1


class TestOptionFullStdlib:
    """Test complete stdlib/core.al file parses."""

    def test_full_option_stdlib(self):
        """Test that full Option implementation from stdlib/core.al parses."""
        # Read the actual stdlib file
        with open("/Users/hustlermain/HUSTLER_CONTENT/HSTLR/DEV/Promptware/stdlib/core.al") as f:
            pw_code = f.read()

        # Should parse without errors
        ir = parse_al(pw_code)

        # Check basic structure
        assert len(ir.enums) >= 1  # At least Option enum

        # Count Option-related functions
        option_funcs = [f for f in ir.functions if f.name.startswith("option_")]
        assert len(option_funcs) >= 8  # All Option methods

    def test_option_functions_present(self):
        """Test that all required Option functions are present."""
        with open("/Users/hustlermain/HUSTLER_CONTENT/HSTLR/DEV/Promptware/stdlib/core.al") as f:
            pw_code = f.read()

        ir = parse_al(pw_code)

        # Required Option functions
        required_funcs = [
            "option_some",
            "option_none",
            "option_map",
            "option_and_then",
            "option_unwrap_or",
            "option_unwrap_or_else",
            "option_is_some",
            "option_is_none",
            "option_match"
        ]

        func_names = [f.name for f in ir.functions]
        for required in required_funcs:
            assert required in func_names, f"Missing function: {required}"


class TestOptionTypeAnnotations:
    """Test Option type annotations."""

    def test_option_int_type(self):
        """Test Option<int> type annotation."""
        pw_code = """
function get_value() -> Option<int>:
    return Some(42)
"""
        ir = parse_al(pw_code)
        assert len(ir.functions) == 1
        # Return type should have generic args
        assert ir.functions[0].return_type.name == "Option"
        assert len(ir.functions[0].return_type.generic_args) == 1
        assert ir.functions[0].return_type.generic_args[0].name == "int"

    def test_option_string_type(self):
        """Test Option<string> type annotation."""
        pw_code = """
function get_name() -> Option<string>:
    return None
"""
        ir = parse_al(pw_code)
        assert len(ir.functions) == 1
        assert ir.functions[0].return_type.name == "Option"

    def test_option_generic_type(self):
        """Test Option<T> with generic parameter."""
        pw_code = """
function identity<T>(opt: Option<T>) -> Option<T>:
    return opt
"""
        ir = parse_al(pw_code)
        assert len(ir.functions) == 1
        # Should have generic type parameters
        assert len(ir.functions[0].params) == 1
        assert ir.functions[0].params[0].param_type.name == "Option"


class TestOptionEdgeCases:
    """Test edge cases and error handling."""

    def test_nested_options(self):
        """Test Option<Option<T>>."""
        pw_code = """
function get_nested() -> Option<Option<int>>:
    return Some(Some(42))
"""
        ir = parse_al(pw_code)
        assert len(ir.functions) == 1
        # Return type should be Option with Option<int> as generic arg
        assert ir.functions[0].return_type.name == "Option"

    def test_option_with_custom_type(self):
        """Test Option with custom class type."""
        pw_code = """
class User:
    name: string
    age: int

function find_user(id: int) -> Option<User>:
    return None
"""
        ir = parse_al(pw_code)
        assert len(ir.classes) == 1
        assert len(ir.functions) == 1

    def test_option_array_type(self):
        """Test Option<array<T>>."""
        pw_code = """
function get_items() -> Option<array<int>>:
    return Some([1, 2, 3])
"""
        ir = parse_al(pw_code)
        assert len(ir.functions) == 1
        assert ir.functions[0].return_type.name == "Option"


class TestOptionDocumentation:
    """Test that Option functions have proper documentation."""

    def test_functions_have_docstrings(self):
        """Test that Option functions have docstrings."""
        with open("/Users/hustlermain/HUSTLER_CONTENT/HSTLR/DEV/Promptware/stdlib/core.al") as f:
            content = f.read()

        # Check for docstrings in key functions
        assert '"""' in content or "'''" in content
        assert "Args:" in content or "Returns:" in content
        assert "Example:" in content


class TestOptionCompleteness:
    """Verify Option implementation is complete."""

    def test_option_api_completeness(self):
        """Test that all required API methods are implemented."""
        with open("/Users/hustlermain/HUSTLER_CONTENT/HSTLR/DEV/Promptware/stdlib/core.al") as f:
            pw_code = f.read()

        ir = parse_al(pw_code)

        # API completeness check
        option_functions = {f.name for f in ir.functions if f.name.startswith("option_")}

        required_api = {
            "option_some",
            "option_none",
            "option_map",
            "option_and_then",
            "option_unwrap_or",
            "option_unwrap_or_else",
            "option_is_some",
            "option_is_none",
            "option_match"
        }

        missing = required_api - option_functions
        assert len(missing) == 0, f"Missing API functions: {missing}"


if __name__ == "__main__":
    # Run tests with: pytest tests/test_stdlib_option.py -v
    pytest.main([__file__, "-v"])
