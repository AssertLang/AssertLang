"""
Tests for contract runtime validation (Phase 2B).

Tests runtime enforcement of:
- @requires (preconditions)
- @ensures (postconditions)
- old keyword
- Validation modes
"""

import pytest
from dsl.pw_parser import Lexer, Parser
from language.python_generator_v2 import generate_python
from promptware.runtime.contracts import (
    ContractViolationError,
    ValidationMode,
    set_validation_mode,
)


def parse_and_generate(code: str) -> str:
    """Helper to parse PW code and generate Python."""
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    module = parser.parse()
    return generate_python(module)


def execute_generated(python_code: str, func_name: str, *args):
    """Execute generated Python code and call specified function."""
    # Create execution namespace
    namespace = {}
    exec(python_code, namespace)
    # Call the function
    func = namespace[func_name]
    return func(*args)


class TestPreconditionRuntime:
    """Test precondition runtime validation."""

    def test_precondition_success(self):
        """Precondition passes, function executes normally."""
        code = '''
function add(a: int, b: int) -> int {
    @requires both_positive: a > 0 && b > 0
    return a + b
}
'''
        python_code = parse_and_generate(code)
        print("\n=== Generated Python ===")
        print(python_code)
        print("========================")

        # Should succeed
        result = execute_generated(python_code, "add", 5, 3)
        assert result == 8

    def test_precondition_failure(self):
        """Precondition fails, raises ContractViolationError."""
        code = '''
function add(a: int, b: int) -> int {
    @requires both_positive: a > 0 && b > 0
    return a + b
}
'''
        python_code = parse_and_generate(code)
        print("\n=== Generated Python ===")
        print(python_code)
        print("========================")

        # Should fail precondition
        with pytest.raises(ContractViolationError) as exc_info:
            execute_generated(python_code, "add", -1, 3)

        error = exc_info.value
        assert error.type == "precondition"
        assert error.clause == "both_positive"
        assert "both_positive" in str(error)

    def test_multiple_preconditions(self):
        """Multiple preconditions are all checked."""
        code = '''
function divide(a: int, b: int) -> int {
    @requires non_zero: b != 0
    @requires positive: a >= 0
    return a / b
}
'''
        python_code = parse_and_generate(code)

        # Should pass both
        result = execute_generated(python_code, "divide", 10, 2)
        assert result == 5

        # Should fail first precondition
        with pytest.raises(ContractViolationError) as exc_info:
            execute_generated(python_code, "divide", 10, 0)
        assert exc_info.value.clause == "non_zero"

        # Should fail second precondition
        with pytest.raises(ContractViolationError) as exc_info:
            execute_generated(python_code, "divide", -10, 2)
        assert exc_info.value.clause == "positive"


class TestPostconditionRuntime:
    """Test postcondition runtime validation."""

    def test_postcondition_success(self):
        """Postcondition passes, function returns normally."""
        code = '''
function increment(x: int) -> int {
    @ensures result_correct: result > x
    return x + 1
}
'''
        python_code = parse_and_generate(code)
        print("\n=== Generated Python ===")
        print(python_code)
        print("========================")

        result = execute_generated(python_code, "increment", 5)
        assert result == 6

    def test_postcondition_failure(self):
        """Postcondition fails, raises ContractViolationError."""
        code = '''
function bad_increment(x: int) -> int {
    @ensures result_correct: result > x
    return x
}
'''
        python_code = parse_and_generate(code)
        print("\n=== Generated Python ===")
        print(python_code)
        print("========================")

        with pytest.raises(ContractViolationError) as exc_info:
            execute_generated(python_code, "bad_increment", 5)

        error = exc_info.value
        assert error.type == "postcondition"
        assert error.clause == "result_correct"


class TestOldKeywordRuntime:
    """Test 'old' keyword runtime behavior."""

    def test_old_simple_variable(self):
        """Old keyword captures simple variable value."""
        code = '''
function increment(count: int) -> int {
    @ensures increased: result == old count + 1
    return count + 1
}
'''
        python_code = parse_and_generate(code)
        print("\n=== Generated Python ===")
        print(python_code)
        print("========================")

        result = execute_generated(python_code, "increment", 5)
        assert result == 6

    def test_old_keyword_violation(self):
        """Old keyword detects when pre-state isn't preserved."""
        code = '''
function bad_increment(count: int) -> int {
    @ensures increased: result == old count + 1
    return count + 2
}
'''
        python_code = parse_and_generate(code)

        with pytest.raises(ContractViolationError) as exc_info:
            execute_generated(python_code, "bad_increment", 5)

        assert exc_info.value.type == "postcondition"


class TestValidationModes:
    """Test validation mode switching."""

    def test_disabled_mode_skips_checks(self):
        """In DISABLED mode, contracts are not checked."""
        code = '''
function add(a: int, b: int) -> int {
    @requires both_positive: a > 0 && b > 0
    return a + b
}
'''
        python_code = parse_and_generate(code)

        # Set to disabled mode
        set_validation_mode(ValidationMode.DISABLED)

        try:
            # Should NOT raise error even though precondition fails
            result = execute_generated(python_code, "add", -1, 3)
            assert result == 2
        finally:
            # Restore full mode
            set_validation_mode(ValidationMode.FULL)

    def test_preconditions_only_mode(self):
        """In PRECONDITIONS_ONLY mode, only preconditions are checked."""
        code = '''
function bad_function(x: int) -> int {
    @requires positive: x > 0
    @ensures wrong_postcondition: result == 999
    return x + 1
}
'''
        python_code = parse_and_generate(code)

        # Set to preconditions-only mode
        set_validation_mode(ValidationMode.PRECONDITIONS_ONLY)

        try:
            # Precondition should still be checked
            with pytest.raises(ContractViolationError):
                execute_generated(python_code, "bad_function", -1)

            # Postcondition should NOT be checked (would fail if checked)
            result = execute_generated(python_code, "bad_function", 5)
            assert result == 6  # Not 999, so postcondition would have failed
        finally:
            # Restore full mode
            set_validation_mode(ValidationMode.FULL)


class TestContractErrorMessages:
    """Test that contract errors provide helpful messages."""

    def test_error_includes_clause_name(self):
        """Error message includes clause name."""
        code = '''
function test(x: int) -> int {
    @requires value_positive: x > 0
    return x
}
'''
        python_code = parse_and_generate(code)

        with pytest.raises(ContractViolationError) as exc_info:
            execute_generated(python_code, "test", -1)

        error_msg = str(exc_info.value)
        assert "value_positive" in error_msg

    def test_error_includes_expression(self):
        """Error message includes expression."""
        code = '''
function test(x: int) -> int {
    @requires value_positive: x > 0
    return x
}
'''
        python_code = parse_and_generate(code)

        with pytest.raises(ContractViolationError) as exc_info:
            execute_generated(python_code, "test", -1)

        error_msg = str(exc_info.value)
        assert "x > 0" in error_msg or ">" in error_msg

    def test_error_includes_function_name(self):
        """Error message includes function name."""
        code = '''
function myFunction(x: int) -> int {
    @requires positive: x > 0
    return x
}
'''
        python_code = parse_and_generate(code)

        with pytest.raises(ContractViolationError) as exc_info:
            execute_generated(python_code, "myFunction", -1)

        error_msg = str(exc_info.value)
        assert "myFunction" in error_msg


class TestBackwardCompatibility:
    """Ensure functions without contracts still work."""

    def test_function_without_contracts(self):
        """Functions without contracts work normally."""
        code = '''
function add(a: int, b: int) -> int {
    return a + b
}
'''
        python_code = parse_and_generate(code)

        result = execute_generated(python_code, "add", 5, 3)
        assert result == 8

    def test_mixed_functions(self):
        """Mix of functions with and without contracts."""
        code = '''
function with_contract(x: int) -> int {
    @requires positive: x > 0
    return x + 1
}

function without_contract(x: int) -> int {
    return x + 1
}
'''
        python_code = parse_and_generate(code)

        # With contract should enforce
        with pytest.raises(ContractViolationError):
            execute_generated(python_code, "with_contract", -1)

        # Without contract should not enforce
        result = execute_generated(python_code, "without_contract", -1)
        assert result == 0


if __name__ == "__main__":
    # Run a quick smoke test
    code = """
function test(x: int) -> int {
    @requires positive: x > 0
    @ensures result_correct: result > x
    return x + 1
}
"""
    python_code = parse_and_generate(code)
    print("\n=== Generated Python Code ===")
    print(python_code)
    print("=" * 40)

    print("\nTesting with valid input (x=5)...")
    try:
        result = execute_generated(python_code, "test", 5)
        print(f"✓ Success: result = {result}")
    except Exception as e:
        print(f"✗ Failed: {e}")

    print("\nTesting with invalid input (x=-1)...")
    try:
        result = execute_generated(python_code, "test", -1)
        print(f"✗ Should have failed but got: {result}")
    except ContractViolationError as e:
        print(f"✓ Correctly raised ContractViolationError:")
        print(f"  {e}")

    print("\nAll basic tests passed!")
