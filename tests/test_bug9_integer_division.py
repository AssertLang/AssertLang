"""
Test Suite for Bug #9: Integer Division Translation

Verifies that integer division in PW correctly generates:
- `//` in Python for int/int
- `/` in Python for float divisions

Bug: When dividing two integers, the generator used `/` (float division)
instead of `//` (integer division), causing TypeErrors when the result
was used as an array index.

Example: mid = (left + right) / 2  →  mid = 3.0 (TypeError for arr[mid])
Fixed:   mid = (left + right) // 2  →  mid = 3 (Works!)
"""

import pytest
from dsl.pw_parser import Lexer, Parser
from language.python_generator_v2 import generate_python


def parse_and_generate(pw_code: str) -> str:
    """Helper: Parse PW code and generate Python."""
    lexer = Lexer(pw_code)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ir = parser.parse()
    return generate_python(ir)


class TestIntegerDivision:
    """Test integer division generates // in Python."""

    def test_binary_search_with_mid_calculation(self):
        """Test the original bug case: binary search with mid calculation."""
        pw_code = """
        function binary_search(arr: array, target: int) -> int {
            let left = 0;
            let right = arr.length - 1;

            while (left <= right) {
                let mid = (left + right) / 2;
                let val = arr[mid];

                if (val == target) {
                    return mid;
                }

                if (val < target) {
                    left = mid + 1;
                } else {
                    right = mid - 1;
                }
            }

            return -1;
        }
        """
        python_code = parse_and_generate(pw_code)

        # Verify integer division is used
        assert "((left + right) // 2)" in python_code
        assert "((left + right) / 2)" not in python_code

        # Verify the generated code executes correctly
        exec_globals = {}
        exec(python_code, exec_globals)
        binary_search = exec_globals['binary_search']

        # Test the function
        arr = [1, 3, 5, 7, 9, 11, 13]
        assert binary_search(arr, 7) == 3
        assert binary_search(arr, 1) == 0
        assert binary_search(arr, 13) == 6
        assert binary_search(arr, 99) == -1

    def test_int_divided_by_int_params(self):
        """Test int/int division with typed parameters."""
        pw_code = """
        function divide_ints(a: int, b: int) -> int {
            return a / b;
        }
        """
        python_code = parse_and_generate(pw_code)

        # Should use integer division
        assert "(a // b)" in python_code
        assert "return (a // b)" in python_code

    def test_int_literal_divided_by_int_literal(self):
        """Test literal int / literal int."""
        pw_code = """
        function test() -> int {
            let result = 10 / 3;
            return result;
        }
        """
        python_code = parse_and_generate(pw_code)

        # Should use integer division
        assert "(10 // 3)" in python_code

    def test_expression_result_divided_by_int(self):
        """Test (int + int) / int."""
        pw_code = """
        function average_of_two(a: int, b: int) -> int {
            return (a + b) / 2;
        }
        """
        python_code = parse_and_generate(pw_code)

        # Should use integer division
        assert "// 2" in python_code
        assert "/ 2" not in python_code or "// 2" in python_code


class TestFloatDivision:
    """Test float division generates / in Python."""

    def test_float_divided_by_int(self):
        """Test float / int → uses /"""
        pw_code = """
        function divide_float(a: float, b: int) -> float {
            return a / b;
        }
        """
        python_code = parse_and_generate(pw_code)

        # Should use regular division (not //)
        assert "(a / b)" in python_code
        assert "//" not in python_code

    def test_int_divided_by_float(self):
        """Test int / float → uses /"""
        pw_code = """
        function divide_by_float(a: int, b: float) -> float {
            return a / b;
        }
        """
        python_code = parse_and_generate(pw_code)

        # Should use regular division
        assert "(a / b)" in python_code
        assert "//" not in python_code

    def test_float_divided_by_float(self):
        """Test float / float → uses /"""
        pw_code = """
        function divide_floats(a: float, b: float) -> float {
            return a / b;
        }
        """
        python_code = parse_and_generate(pw_code)

        # Should use regular division
        assert "(a / b)" in python_code
        assert "//" not in python_code

    def test_literal_float_division(self):
        """Test 10.0 / 3.0 → uses /"""
        pw_code = """
        function test() -> float {
            return 10.0 / 3.0;
        }
        """
        python_code = parse_and_generate(pw_code)

        # Should use regular division
        assert "(10.0 / 3.0)" in python_code


class TestMixedDivisionScenarios:
    """Test complex division scenarios."""

    def test_all_division_types_in_one_function(self):
        """Test function with multiple division types."""
        pw_code = """
        function test_divisions(a: int, b: int, c: float) -> map {
            let int_div = a / b;           // int / int → //
            let float_div1 = c / b;        // float / int → /
            let float_div2 = a / c;        // int / float → /
            let float_div3 = c / 3.14;     // float / float → /
            let int_literal = 10 / 3;      // int literal / int literal → //

            return {
                int_div: int_div,
                float_div1: float_div1,
                float_div2: float_div2,
                float_div3: float_div3,
                int_literal: int_literal
            };
        }
        """
        python_code = parse_and_generate(pw_code)

        # Check integer divisions
        assert "(a // b)" in python_code
        assert "(10 // 3)" in python_code

        # Check float divisions
        assert "(c / b)" in python_code
        assert "(a / c)" in python_code
        assert "(c / 3.14)" in python_code

        # Execute and verify types
        exec_globals = {}
        exec(python_code, exec_globals)
        test_divisions = exec_globals['test_divisions']

        result = test_divisions(10, 3, 7.5)
        assert isinstance(result['int_div'], int)
        assert result['int_div'] == 3
        assert isinstance(result['float_div1'], float)
        assert isinstance(result['float_div2'], float)
        assert isinstance(result['float_div3'], float)
        assert isinstance(result['int_literal'], int)

    def test_nested_divisions(self):
        """Test nested division expressions."""
        pw_code = """
        function nested_div(a: int, b: int, c: int) -> int {
            return (a / b) / c;
        }
        """
        python_code = parse_and_generate(pw_code)

        # Both divisions should be integer division
        assert "// b) // c" in python_code

    def test_division_in_array_index(self):
        """Test division used as array index."""
        pw_code = """
        function get_middle_element(arr: array) -> int {
            let index = arr.length / 2;
            return arr[index];
        }
        """
        python_code = parse_and_generate(pw_code)

        # Should use integer division
        assert "len(arr) // 2" in python_code

        # Verify it executes
        exec_globals = {}
        exec(python_code, exec_globals)
        get_middle = exec_globals['get_middle_element']

        assert get_middle([1, 2, 3, 4, 5]) == 3


class TestTypeInference:
    """Test type inference for division."""

    def test_infers_len_returns_int(self):
        """Test that len() result is inferred as int."""
        pw_code = """
        function test(arr: array) -> int {
            let size = arr.length;
            let half = size / 2;
            return half;
        }
        """
        python_code = parse_and_generate(pw_code)

        # size is int (from .length), so size / 2 should be //
        assert "// 2" in python_code

    def test_infers_binary_op_result_type(self):
        """Test binary operation result type inference."""
        pw_code = """
        function sum_and_divide(a: int, b: int, c: int) -> int {
            let sum = a + b;  // int + int = int
            return sum / c;   // int / int = //
        }
        """
        python_code = parse_and_generate(pw_code)

        # sum is int, c is int, so sum / c should be //
        assert "(sum // c)" in python_code


def test_regression_no_breaks():
    """Ensure the fix doesn't break other operators."""
    pw_code = """
    function test_ops(a: int, b: int) -> map {
        let add = a + b;
        let sub = a - b;
        let mul = a * b;
        let div = a / b;
        let mod = a % b;
        return {add: add, sub: sub, mul: mul, div: div, mod: mod};
    }
    """
    python_code = parse_and_generate(pw_code)

    # Other operators unchanged
    assert "(a + b)" in python_code
    assert "(a - b)" in python_code
    assert "(a * b)" in python_code
    assert "(a % b)" in python_code

    # Division uses //
    assert "(a // b)" in python_code
