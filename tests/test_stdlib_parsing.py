"""
Test suite for stdlib file parsing.

Verifies that stdlib files with generic types parse correctly.
"""

import pytest
from pathlib import Path
from dsl.pw_parser import parse_pw


STDLIB_DIR = Path(__file__).parent.parent / "stdlib"


def test_parse_stdlib_core_pw():
    """Test that stdlib/core.pw parses without errors."""
    core_file = STDLIB_DIR / "core.pw"
    with open(core_file, "r") as f:
        code = f.read()

    ir = parse_pw(code)

    # Verify Option enum exists with generic parameter
    option_enums = [e for e in ir.enums if e.name == "Option"]
    assert len(option_enums) == 1
    option = option_enums[0]
    assert option.generic_params == ["T"]
    assert any(v.name == "Some" for v in option.variants)
    assert any(v.name == "None" for v in option.variants)

    # Verify Result enum exists with generic parameters
    result_enums = [e for e in ir.enums if e.name == "Result"]
    assert len(result_enums) == 1
    result = result_enums[0]
    assert result.generic_params == ["T", "E"]
    assert any(v.name == "Ok" for v in result.variants)
    assert any(v.name == "Err" for v in result.variants)


def test_parse_stdlib_types_pw():
    """Test that stdlib/types.pw parses without errors."""
    types_file = STDLIB_DIR / "types.pw"
    with open(types_file, "r") as f:
        code = f.read()

    ir = parse_pw(code)

    # Verify List class exists with generic parameter
    list_classes = [c for c in ir.classes if c.name == "List"]
    assert len(list_classes) == 1
    list_class = list_classes[0]
    assert list_class.generic_params == ["T"]

    # Verify Map class exists with generic parameters
    map_classes = [c for c in ir.classes if c.name == "Map"]
    assert len(map_classes) == 1
    map_class = map_classes[0]
    assert map_class.generic_params == ["K", "V"]

    # Verify Set class exists with generic parameter
    set_classes = [c for c in ir.classes if c.name == "Set"]
    assert len(set_classes) == 1
    set_class = set_classes[0]
    assert set_class.generic_params == ["T"]


def test_option_methods_parse():
    """Test that all Option<T> methods parse correctly."""
    core_file = STDLIB_DIR / "core.pw"
    with open(core_file, "r") as f:
        code = f.read()

    ir = parse_pw(code)

    # Check for key Option functions with generics
    option_funcs = [
        "option_some",
        "option_none",
        "option_map",
        "option_and_then",
        "option_unwrap_or",
        "option_is_some",
        "option_is_none"
    ]

    for func_name in option_funcs:
        funcs = [f for f in ir.functions if f.name == func_name]
        assert len(funcs) >= 1, f"Missing function: {func_name}"

    # Verify option_map has correct generic parameters
    option_map = [f for f in ir.functions if f.name == "option_map"][0]
    assert option_map.generic_params == ["T", "U"]


def test_result_methods_parse():
    """Test that all Result<T,E> methods parse correctly."""
    core_file = STDLIB_DIR / "core.pw"
    with open(core_file, "r") as f:
        code = f.read()

    ir = parse_pw(code)

    # Check for key Result functions with generics
    result_funcs = [
        "result_ok",
        "result_err",
        "result_map",
        "result_map_err",
        "result_and_then",
        "result_unwrap_or",
        "result_is_ok",
        "result_is_err"
    ]

    for func_name in result_funcs:
        funcs = [f for f in ir.functions if f.name == func_name]
        assert len(funcs) >= 1, f"Missing function: {func_name}"

    # Verify result_map has correct generic parameters
    result_map = [f for f in ir.functions if f.name == "result_map"][0]
    assert result_map.generic_params == ["T", "E", "U"]


def test_collection_methods_parse():
    """Test that List/Map/Set methods parse correctly."""
    types_file = STDLIB_DIR / "types.pw"
    with open(types_file, "r") as f:
        code = f.read()

    ir = parse_pw(code)

    # Check for key collection functions
    list_funcs = ["list_new", "list_push", "list_pop", "list_map", "list_filter"]
    map_funcs = ["map_new", "map_insert", "map_get", "map_remove"]
    set_funcs = ["set_new", "set_insert", "set_remove", "set_contains"]

    all_funcs = list_funcs + map_funcs + set_funcs

    for func_name in all_funcs:
        funcs = [f for f in ir.functions if f.name == func_name]
        assert len(funcs) >= 1, f"Missing function: {func_name}"

    # Verify list_map has correct generic parameters
    list_map = [f for f in ir.functions if f.name == "list_map"][0]
    assert list_map.generic_params == ["T", "U"]


def test_stdlib_files_syntax_valid():
    """Test that all stdlib files have valid syntax (no parse errors)."""
    stdlib_files = [
        STDLIB_DIR / "core.pw",
        STDLIB_DIR / "types.pw",
    ]

    for stdlib_file in stdlib_files:
        if stdlib_file.exists():
            with open(stdlib_file, "r") as f:
                code = f.read()
            # Should not raise PWParseError
            ir = parse_pw(code)
            assert ir is not None, f"Failed to parse {stdlib_file.name}"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
