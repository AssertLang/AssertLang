"""
Test Bug #14: Python generator missing FLOOR_DIVIDE operator mapping

Bug discovered when testing Bug #13. The Python generator was missing
BinaryOperator.FLOOR_DIVIDE in its op_map dictionary, causing it to
default to "+" (addition) instead of "//" (floor division).

Fixed in v2.1.0b8 by adding:
1. BinaryOperator.FLOOR_DIVIDE: "//" to op_map
2. Type inference for floor division (always returns int)
"""

import pytest
from pathlib import Path
import tempfile
import subprocess
import sys


def compile_pw_to_python(pw_code: str) -> str:
    """Compile PW code to Python and return the generated code."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.pw', delete=False) as f:
        f.write(pw_code)
        pw_file = f.name

    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        py_file = f.name

    try:
        result = subprocess.run(
            [sys.executable, '-m', 'promptware.cli', 'build', pw_file, '--lang', 'python', '-o', py_file],
            capture_output=True,
            text=True
        )
        if result.returncode != 0:
            raise RuntimeError(f"Compilation failed: {result.stderr}")

        with open(py_file, 'r') as f:
            return f.read()
    finally:
        Path(pw_file).unlink(missing_ok=True)
        Path(py_file).unlink(missing_ok=True)


def compile_and_run_python(pw_code: str, function_name: str):
    """Compile PW code and run a specific function."""
    py_code = compile_pw_to_python(pw_code)

    # Execute the generated Python code
    namespace = {}
    exec(py_code, namespace)

    # Return the function result
    return namespace[function_name]()


def test_floor_division_basic():
    """Test basic floor division: 100 // 50 should be 2."""
    pw_code = """
function calculate_pages() -> int {
    let total_lines = 100;
    let pages = total_lines // 50;
    return pages;
}
"""
    result = compile_and_run_python(pw_code, 'calculate_pages')
    assert result == 2, f"Expected 2, got {result}"


def test_floor_division_in_if_block():
    """Test Bug #13 + Bug #14: Variable reassignment in if block using floor division."""
    pw_code = """
function calculate_pages() -> int {
    let total_lines = 100;
    let pages = total_lines // 50;

    if (pages == 0) {
        pages = 1;
    }

    return pages;
}
"""
    result = compile_and_run_python(pw_code, 'calculate_pages')
    assert result == 2, f"Expected 2, got {result}"


def test_floor_division_zero_case():
    """Test floor division with zero result."""
    pw_code = """
function calculate_pages() -> int {
    let total_lines = 25;
    let pages = total_lines // 50;

    if (pages == 0) {
        pages = 1;
    }

    return pages;
}
"""
    result = compile_and_run_python(pw_code, 'calculate_pages')
    assert result == 1, f"Expected 1, got {result}"


def test_floor_division_complex_expression():
    """Test floor division in complex expression."""
    pw_code = """
function calculate_rows() -> int {
    let row_count = 1000;
    let selectivity = 75;
    let estimated_rows = (row_count * selectivity) // 100;
    return estimated_rows;
}
"""
    result = compile_and_run_python(pw_code, 'calculate_rows')
    assert result == 750, f"Expected 750, got {result}"


def test_floor_division_multiple_operations():
    """Test multiple floor divisions in same function."""
    pw_code = """
function test_multiple() -> int {
    let a = 100 // 3;
    let b = 200 // 7;
    let c = a + b;
    return c;
}
"""
    result = compile_and_run_python(pw_code, 'test_multiple')
    expected = (100 // 3) + (200 // 7)  # 33 + 28 = 61
    assert result == expected, f"Expected {expected}, got {result}"


def test_floor_division_generated_syntax():
    """Test that generated Python uses // not +."""
    pw_code = """
function calculate_pages() -> int {
    let total_lines = 100;
    let pages = total_lines // 50;
    return pages;
}
"""
    py_code = compile_pw_to_python(pw_code)

    # Check that // is present
    assert "//" in py_code, "Generated code should contain //"

    # Check that it's not mistranslated to +
    # Look for the specific line pattern
    lines = py_code.split('\n')
    pages_line = [l for l in lines if 'pages = ' in l and 'total_lines' in l]
    assert len(pages_line) > 0, "Should find pages assignment"
    assert "//" in pages_line[0], f"Should use //, got: {pages_line[0]}"
    assert "+" not in pages_line[0] or "+ " not in pages_line[0], f"Should not use +, got: {pages_line[0]}"


def test_floor_division_negative_numbers():
    """Test floor division with negative numbers."""
    pw_code = """
function test_negative() -> int {
    let result = -10 // 3;
    return result;
}
"""
    result = compile_and_run_python(pw_code, 'test_negative')
    expected = -10 // 3  # Python floor division rounds toward negative infinity
    assert result == expected, f"Expected {expected}, got {result}"


def test_bug14_exact_reproduction():
    """Exact reproduction of Bug #14 discovery scenario."""
    pw_code = """
function test_reassignment() -> int {
    let count = 0;

    if (true) {
        count = 5;
    }

    return count;
}

function calculate_pages() -> int {
    let total_lines = 100;
    let pages = total_lines // 50;

    if (pages == 0) {
        pages = 1;
    }

    return pages;
}
"""
    py_code = compile_pw_to_python(pw_code)

    # Execute both functions
    namespace = {}
    exec(py_code, namespace)

    # Test reassignment (Bug #13)
    assert namespace['test_reassignment']() == 5, "Bug #13 should be fixed"

    # Test floor division (Bug #14)
    result = namespace['calculate_pages']()
    assert result == 2, f"Bug #14: Expected 2, got {result} (was 150 before fix)"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
