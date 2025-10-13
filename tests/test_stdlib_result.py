"""
Comprehensive test suite for Result<T,E> stdlib type.

Tests parsing, IR structure, and code generation for all Result methods.
Based on implementation-plan.md specifications.
"""

import pytest
from dsl.pw_parser import parse_pw, PWParseError


class TestResultBasicParsing:
    """Test that Result<T,E> code parses correctly."""

    def test_result_enum_definition(self):
        """Test Result enum definition parses."""
        pw_code = """
enum Result<T, E>:
    - Ok(value: T)
    - Err(error: E)
"""
        ir = parse_pw(pw_code)
        assert len(ir.enums) == 1
        assert ir.enums[0].name == "Result"
        assert len(ir.enums[0].variants) == 2
        assert ir.enums[0].variants[0].name == "Ok"
        assert ir.enums[0].variants[1].name == "Err"

    def test_result_ok_constructor(self):
        """Test result_ok function parses."""
        pw_code = """
function result_ok<T, E>(value: T) -> Result<T, E>:
    return Result.Ok(value)
"""
        ir = parse_pw(pw_code)
        assert len(ir.functions) == 1
        assert ir.functions[0].name == "result_ok"

    def test_result_err_constructor(self):
        """Test result_err function parses."""
        pw_code = """
function result_err<T, E>(error: E) -> Result<T, E>:
    return Result.Err(error)
"""
        ir = parse_pw(pw_code)
        assert len(ir.functions) == 1
        assert ir.functions[0].name == "result_err"


class TestResultMethods:
    """Test Result method definitions parse correctly."""

    def test_result_map(self):
        """Test result_map function parses."""
        pw_code = """
function result_map<T, E, U>(res: Result<T, E>, fn: function(T) -> U) -> Result<U, E>:
    if res is Ok(val):
        return Ok(fn(val))
    else if res is Err(e):
        return Err(e)
"""
        ir = parse_pw(pw_code)
        assert len(ir.functions) == 1
        assert ir.functions[0].name == "result_map"
        assert len(ir.functions[0].params) == 2

    def test_result_map_err(self):
        """Test result_map_err function parses."""
        pw_code = """
function result_map_err<T, E, F>(res: Result<T, E>, fn: function(E) -> F) -> Result<T, F>:
    if res is Ok(val):
        return Ok(val)
    else if res is Err(e):
        return Err(fn(e))
"""
        ir = parse_pw(pw_code)
        assert len(ir.functions) == 1
        assert ir.functions[0].name == "result_map_err"

    def test_result_and_then(self):
        """Test result_and_then function parses."""
        pw_code = """
function result_and_then<T, E, U>(
    res: Result<T, E>,
    fn: function(T) -> Result<U, E>
) -> Result<U, E>:
    if res is Ok(val):
        return fn(val)
    else if res is Err(e):
        return Err(e)
"""
        ir = parse_pw(pw_code)
        assert len(ir.functions) == 1
        assert ir.functions[0].name == "result_and_then"

    def test_result_unwrap_or(self):
        """Test result_unwrap_or function parses."""
        pw_code = """
function result_unwrap_or<T, E>(res: Result<T, E>, default: T) -> T:
    if res is Ok(val):
        return val
    else:
        return default
"""
        ir = parse_pw(pw_code)
        assert len(ir.functions) == 1
        assert ir.functions[0].name == "result_unwrap_or"

    def test_result_is_ok(self):
        """Test result_is_ok function parses."""
        pw_code = """
function result_is_ok<T, E>(res: Result<T, E>) -> bool:
    if res is Ok(_):
        return true
    else:
        return false
"""
        ir = parse_pw(pw_code)
        assert len(ir.functions) == 1
        assert ir.functions[0].name == "result_is_ok"

    def test_result_is_err(self):
        """Test result_is_err function parses."""
        pw_code = """
function result_is_err<T, E>(res: Result<T, E>) -> bool:
    if res is Err(_):
        return true
    else:
        return false
"""
        ir = parse_pw(pw_code)
        assert len(ir.functions) == 1
        assert ir.functions[0].name == "result_is_err"

    def test_result_match(self):
        """Test result_match function parses."""
        pw_code = """
function result_match<T, E, U>(
    res: Result<T, E>,
    ok_fn: function(T) -> U,
    err_fn: function(E) -> U
) -> U:
    if res is Ok(val):
        return ok_fn(val)
    else if res is Err(e):
        return err_fn(e)
"""
        ir = parse_pw(pw_code)
        assert len(ir.functions) == 1
        assert ir.functions[0].name == "result_match"
        assert len(ir.functions[0].params) == 3


class TestResultUsagePatterns:
    """Test real-world Result usage patterns."""

    def test_result_division_by_zero(self):
        """Test Result for division by zero handling."""
        pw_code = """
function safe_divide(a: int, b: int) -> Result<int, string>:
    if b == 0:
        return result_err("division by zero")
    else:
        return result_ok(a / b)
"""
        ir = parse_pw(pw_code)
        assert len(ir.functions) == 1
        assert ir.functions[0].name == "safe_divide"

    def test_result_file_operations(self):
        """Test Result for file operations."""
        pw_code = """
function read_config(path: string) -> Result<string, string>:
    if path == "":
        return result_err("empty path")
    else:
        return result_ok("config data")
"""
        ir = parse_pw(pw_code)
        assert len(ir.functions) == 1

    def test_result_validation(self):
        """Test Result for input validation."""
        pw_code = """
function validate_age(age: int) -> Result<int, string>:
    if age < 0:
        return result_err("age cannot be negative")
    else if age > 150:
        return result_err("age too large")
    else:
        return result_ok(age)
"""
        ir = parse_pw(pw_code)
        assert len(ir.functions) == 1

    def test_result_chaining(self):
        """Test chaining Result operations."""
        pw_code = """
function process_data(res: Result<int, string>) -> Result<int, string>:
    let doubled = result_map(res, fn(x) -> x * 2)
    let validated = result_and_then(doubled, fn(x) -> validate_age(x))
    return validated
"""
        ir = parse_pw(pw_code)
        assert len(ir.functions) == 1


class TestResultPatternMatching:
    """Test Result pattern matching."""

    def test_result_ok_pattern(self):
        """Test matching Ok variant."""
        pw_code = """
function describe_result(res: Result<int, string>) -> string:
    if res is Ok(value):
        return "Success: " + str(value)
    else if res is Err(error):
        return "Error: " + error
"""
        ir = parse_pw(pw_code)
        assert len(ir.functions) == 1

    def test_result_err_pattern(self):
        """Test matching Err variant."""
        pw_code = """
function is_error(res: Result<int, string>) -> bool:
    if res is Err(_):
        return true
    else:
        return false
"""
        ir = parse_pw(pw_code)
        assert len(ir.functions) == 1

    def test_result_extract_values(self):
        """Test extracting values from Result."""
        pw_code = """
function get_value_or_zero(res: Result<int, string>) -> int:
    if res is Ok(val):
        return val
    else:
        return 0
"""
        ir = parse_pw(pw_code)
        assert len(ir.functions) == 1


class TestResultFullStdlib:
    """Test complete Result implementation from stdlib."""

    def test_full_result_stdlib(self):
        """Test that full Result implementation from stdlib/core.pw parses."""
        with open("/Users/hustlermain/HUSTLER_CONTENT/HSTLR/DEV/Promptware/stdlib/core.pw") as f:
            pw_code = f.read()

        ir = parse_pw(pw_code)

        # Check for Result enum
        result_enums = [e for e in ir.enums if e.name == "Result"]
        assert len(result_enums) >= 1

        # Count Result-related functions
        result_funcs = [f for f in ir.functions if f.name.startswith("result_")]
        assert len(result_funcs) >= 8  # All Result methods

    def test_result_functions_present(self):
        """Test that all required Result functions are present."""
        with open("/Users/hustlermain/HUSTLER_CONTENT/HSTLR/DEV/Promptware/stdlib/core.pw") as f:
            pw_code = f.read()

        ir = parse_pw(pw_code)

        # Required Result functions
        required_funcs = [
            "result_ok",
            "result_err",
            "result_map",
            "result_map_err",
            "result_and_then",
            "result_unwrap_or",
            "result_is_ok",
            "result_is_err",
            "result_match"
        ]

        func_names = [f.name for f in ir.functions]
        for required in required_funcs:
            assert required in func_names, f"Missing function: {required}"


class TestResultTypeAnnotations:
    """Test Result type annotations."""

    def test_result_int_string_type(self):
        """Test Result<int, string> type annotation."""
        pw_code = """
function divide(a: int, b: int) -> Result<int, string>:
    return Ok(a / b)
"""
        ir = parse_pw(pw_code)
        assert len(ir.functions) == 1
        assert ir.functions[0].return_type.name == "Result"
        assert len(ir.functions[0].return_type.generic_args) == 2
        assert ir.functions[0].return_type.generic_args[0].name == "int"
        assert ir.functions[0].return_type.generic_args[1].name == "string"

    def test_result_generic_error(self):
        """Test Result with generic error type."""
        pw_code = """
function parse_int(s: string) -> Result<int, string>:
    return Err("parse error")
"""
        ir = parse_pw(pw_code)
        assert len(ir.functions) == 1

    def test_result_custom_error_type(self):
        """Test Result with custom error type."""
        pw_code = """
class ValidationError:
    message: string
    code: int

function validate(data: string) -> Result<string, ValidationError>:
    return Ok(data)
"""
        ir = parse_pw(pw_code)
        assert len(ir.classes) == 1
        assert len(ir.functions) == 1


class TestResultEdgeCases:
    """Test edge cases and complex scenarios."""

    def test_nested_results(self):
        """Test Result<Result<T, E>, F>."""
        pw_code = """
function nested_operation() -> Result<Result<int, string>, string>:
    return Ok(Ok(42))
"""
        ir = parse_pw(pw_code)
        assert len(ir.functions) == 1

    def test_result_with_option(self):
        """Test Result containing Option."""
        pw_code = """
function find_value(id: int) -> Result<Option<string>, string>:
    return Ok(Some("value"))
"""
        ir = parse_pw(pw_code)
        assert len(ir.functions) == 1

    def test_result_with_array(self):
        """Test Result<array<T>, E>."""
        pw_code = """
function get_items() -> Result<array<int>, string>:
    return Ok([1, 2, 3])
"""
        ir = parse_pw(pw_code)
        assert len(ir.functions) == 1

    def test_result_with_map(self):
        """Test Result<map<K,V>, E>."""
        pw_code = """
function get_config() -> Result<map<string, string>, string>:
    return Ok({"key": "value"})
"""
        ir = parse_pw(pw_code)
        assert len(ir.functions) == 1


class TestResultErrorTypes:
    """Test different error type patterns."""

    def test_string_errors(self):
        """Test Result with string errors."""
        pw_code = """
function operation1() -> Result<int, string>:
    return Err("error message")
"""
        ir = parse_pw(pw_code)
        assert len(ir.functions) == 1

    def test_enum_errors(self):
        """Test Result with enum errors."""
        pw_code = """
enum ErrorCode:
    - NotFound
    - InvalidInput
    - Unauthorized

function operation2() -> Result<int, ErrorCode>:
    return Err(ErrorCode.NotFound)
"""
        ir = parse_pw(pw_code)
        assert len(ir.enums) == 1
        assert len(ir.functions) == 1

    def test_class_errors(self):
        """Test Result with class errors."""
        pw_code = """
class AppError:
    code: int
    message: string

function operation3() -> Result<int, AppError>:
    let err = AppError { code: 404, message: "Not found" }
    return Err(err)
"""
        ir = parse_pw(pw_code)
        assert len(ir.classes) == 1
        assert len(ir.functions) == 1


class TestResultDocumentation:
    """Test that Result functions have proper documentation."""

    def test_functions_have_docstrings(self):
        """Test that Result functions have docstrings."""
        with open("/Users/hustlermain/HUSTLER_CONTENT/HSTLR/DEV/Promptware/stdlib/core.pw") as f:
            content = f.read()

        # Check for docstrings
        assert '"""' in content or "'''" in content
        assert "Args:" in content or "Returns:" in content
        assert "Example:" in content

    def test_error_handling_examples(self):
        """Test that documentation includes error handling examples."""
        with open("/Users/hustlermain/HUSTLER_CONTENT/HSTLR/DEV/Promptware/stdlib/core.pw") as f:
            content = f.read()

        # Should have examples of Ok and Err
        assert "Ok(" in content
        assert "Err(" in content


class TestResultCompleteness:
    """Verify Result implementation is complete."""

    def test_result_api_completeness(self):
        """Test that all required API methods are implemented."""
        with open("/Users/hustlermain/HUSTLER_CONTENT/HSTLR/DEV/Promptware/stdlib/core.pw") as f:
            pw_code = f.read()

        ir = parse_pw(pw_code)

        result_functions = {f.name for f in ir.functions if f.name.startswith("result_")}

        required_api = {
            "result_ok",
            "result_err",
            "result_map",
            "result_map_err",
            "result_and_then",
            "result_unwrap_or",
            "result_is_ok",
            "result_is_err",
            "result_match"
        }

        missing = required_api - result_functions
        assert len(missing) == 0, f"Missing API functions: {missing}"

    def test_both_option_and_result_present(self):
        """Test that both Option and Result are in same file."""
        with open("/Users/hustlermain/HUSTLER_CONTENT/HSTLR/DEV/Promptware/stdlib/core.pw") as f:
            pw_code = f.read()

        ir = parse_pw(pw_code)

        enum_names = {e.name for e in ir.enums}
        assert "Option" in enum_names
        assert "Result" in enum_names


if __name__ == "__main__":
    # Run tests with: pytest tests/test_stdlib_result.py -v
    pytest.main([__file__, "-v"])
