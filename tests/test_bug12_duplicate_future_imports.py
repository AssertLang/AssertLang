"""
Test Bug #12: Duplicate 'from __future__ import annotations' in generated Python.

Verifies that Python code generated via CLI build command has only ONE
future import at the top of the file, not duplicates.
"""

import sys
from pathlib import Path

# Add pw-syntax-mcp-server to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'pw-syntax-mcp-server'))

import pytest
from dsl.al_parser import parse_al
from translators.ir_converter import ir_to_mcp
from translators.python_bridge import pw_to_python


def test_no_duplicate_future_imports_simple_class():
    """Test simple class generates only one future import."""
    pw_code = """
class User {
    id: int;
    name: string;

    constructor(id: int, name: string) {
        self.id = id;
        self.name = name;
    }
}
"""
    ir = parse_al(pw_code)
    mcp_tree = ir_to_mcp(ir)
    python_code = pw_to_python(mcp_tree)

    lines = python_code.split('\n')
    future_import_lines = [
        i for i, line in enumerate(lines)
        if 'from __future__ import annotations' in line
    ]

    # Should have exactly ONE future import
    assert len(future_import_lines) == 1, \
        f"Expected 1 future import, found {len(future_import_lines)} at lines {future_import_lines}"

    # Should be at the very top (line 0)
    assert future_import_lines[0] == 0, \
        f"Future import should be at line 0, found at line {future_import_lines[0]}"


def test_no_duplicate_future_imports_with_typing():
    """Test code with typing imports has only one future import."""
    pw_code = """
function process_items(items: array) -> array {
    let result = [];
    return result;
}
"""
    ir = parse_al(pw_code)
    mcp_tree = ir_to_mcp(ir)
    python_code = pw_to_python(mcp_tree)

    lines = python_code.split('\n')
    future_import_lines = [
        i for i, line in enumerate(lines)
        if 'from __future__ import annotations' in line
    ]

    # Should have exactly ONE future import
    assert len(future_import_lines) == 1, \
        f"Expected 1 future import, found {len(future_import_lines)} at lines {future_import_lines}"

    # Should be at the very top (line 0)
    assert future_import_lines[0] == 0, \
        f"Future import should be at line 0, found at line {future_import_lines[0]}"

    # Should have typing import AFTER future import
    typing_import_exists = any('from typing import' in line for line in lines)
    assert typing_import_exists, "Should have typing import for List type"


def test_generated_python_runs_without_syntax_error():
    """Test that generated Python code can be executed without SyntaxError."""
    pw_code = """
class Request {
    method: string;
    path: string;
    body: map;

    constructor(method: string, path: string, body: map) {
        self.method = method;
        self.path = path;
        self.body = body;
    }

    function get_method() -> string {
        return self.method;
    }
}
"""
    ir = parse_al(pw_code)
    mcp_tree = ir_to_mcp(ir)
    python_code = pw_to_python(mcp_tree)

    # Should compile without SyntaxError
    try:
        compile(python_code, '<string>', 'exec')
    except SyntaxError as e:
        pytest.fail(f"Generated Python has SyntaxError: {e}")


def test_future_import_before_typing_imports():
    """Test that future import appears before any typing imports."""
    pw_code = """
function transform_data(data: array, mapper: map) -> array {
    return data;
}
"""
    ir = parse_al(pw_code)
    mcp_tree = ir_to_mcp(ir)
    python_code = pw_to_python(mcp_tree)

    lines = [line.strip() for line in python_code.split('\n') if line.strip()]

    # Find indices
    future_idx = None
    typing_idx = None

    for i, line in enumerate(lines):
        if 'from __future__ import annotations' in line:
            future_idx = i
        if 'from typing import' in line:
            typing_idx = i

    # Both should exist
    assert future_idx is not None, "Future import not found"

    # If typing import exists, future should come first
    if typing_idx is not None:
        assert future_idx < typing_idx, \
            f"Future import (line {future_idx}) must come before typing import (line {typing_idx})"
