"""
Test suite for generic type parameter parsing.

Tests parser support for:
- enum Option<T>:
- function foo<T>()
- class List<T>:
- Nested generics: List<Option<int>>
"""

import pytest
from dsl.al_parser import parse_al, ALParseError


def test_parse_generic_enum_single_param():
    """Test parsing enum with single type parameter."""
    code = """
enum Option<T>:
    - Some(value: T)
    - None
"""
    ir = parse_al(code)
    assert len(ir.enums) == 1
    assert ir.enums[0].name == "Option"
    assert ir.enums[0].generic_params == ["T"]
    assert len(ir.enums[0].variants) == 2
    assert ir.enums[0].variants[0].name == "Some"
    assert ir.enums[0].variants[1].name == "None"


def test_parse_generic_enum_multiple_params():
    """Test parsing enum with multiple type parameters."""
    code = """
enum Result<T, E>:
    - Ok(value: T)
    - Err(error: E)
"""
    ir = parse_al(code)
    assert len(ir.enums) == 1
    assert ir.enums[0].name == "Result"
    assert ir.enums[0].generic_params == ["T", "E"]
    assert len(ir.enums[0].variants) == 2


def test_parse_generic_function_single():
    """Test parsing function with single type parameter."""
    code = """
function foo<T>(x: T) -> T {
    return x
}
"""
    ir = parse_al(code)
    assert len(ir.functions) == 1
    assert ir.functions[0].name == "foo"
    assert ir.functions[0].generic_params == ["T"]
    assert ir.functions[0].params[0].param_type.name == "T"
    assert ir.functions[0].return_type.name == "T"


def test_parse_generic_function_multiple():
    """Test parsing function with multiple type parameters."""
    code = """
function map<T, U>(opt: Option<T>, fn: function(T) -> U) -> Option<U> {
    return None
}
"""
    ir = parse_al(code)
    assert len(ir.functions) == 1
    assert ir.functions[0].name == "map"
    assert ir.functions[0].generic_params == ["T", "U"]


def test_parse_generic_class_single():
    """Test parsing class with single type parameter."""
    code = """
class List<T> {
    items: array<T>
}
"""
    ir = parse_al(code)
    assert len(ir.classes) == 1
    assert ir.classes[0].name == "List"
    assert ir.classes[0].generic_params == ["T"]
    assert ir.classes[0].properties[0].name == "items"


def test_parse_generic_class_multiple():
    """Test parsing class with multiple type parameters."""
    code = """
class Map<K, V> {
    entries: map<K, V>
}
"""
    ir = parse_al(code)
    assert len(ir.classes) == 1
    assert ir.classes[0].name == "Map"
    assert ir.classes[0].generic_params == ["K", "V"]


def test_parse_nested_generics():
    """Test parsing nested generic types."""
    code = """
function foo(x: List<Option<int>>) -> void {
    pass
}
"""
    ir = parse_al(code)
    assert len(ir.functions) == 1
    param_type = ir.functions[0].params[0].param_type
    assert param_type.name == "List"
    assert len(param_type.generic_args) == 1
    assert param_type.generic_args[0].name == "Option"
    assert param_type.generic_args[0].generic_args[0].name == "int"


def test_ir_stores_generic_params():
    """Test that IR correctly stores generic parameters."""
    code = """
enum Status<T>:
    - Pending
    - Complete(value: T)

function process<T>(x: T) -> Status<T> {
    return Status.Pending
}

class Container<T> {
    value: T
}
"""
    ir = parse_al(code)

    # Check enum
    assert ir.enums[0].generic_params == ["T"]

    # Check function
    assert ir.functions[0].generic_params == ["T"]

    # Check class
    assert ir.classes[0].generic_params == ["T"]


def test_generic_function_with_type_params():
    """Test generic function with parameters using type parameters."""
    code = """
function swap<T, U>(a: T, b: U) -> map<U, T> {
    return {first: b, second: a}
}
"""
    ir = parse_al(code)
    assert ir.functions[0].generic_params == ["T", "U"]
    assert ir.functions[0].params[0].param_type.name == "T"
    assert ir.functions[0].params[1].param_type.name == "U"
    assert ir.functions[0].return_type.name == "map"


def test_reject_empty_generic():
    """Test that empty generic parameters are rejected."""
    code = """
enum Foo<>:
    - Bar
"""
    with pytest.raises(ALParseError) as exc_info:
        parse_al(code)
    assert "Expected IDENTIFIER" in str(exc_info.value) or "Expected" in str(exc_info.value)


def test_less_than_not_confused_with_generic():
    """Test that < in expressions is not confused with generic start."""
    code = """
function foo() -> bool {
    let x = 5
    if (x < 10) {
        return true
    }
    return false
}
"""
    ir = parse_al(code)
    assert len(ir.functions) == 1
    assert ir.functions[0].name == "foo"
    assert ir.functions[0].generic_params == []  # No generics


def test_generic_in_return_type():
    """Test generic type in return type."""
    code = """
function create<T>() -> Option<T> {
    return None
}
"""
    ir = parse_al(code)
    assert ir.functions[0].return_type.name == "Option"
    assert ir.functions[0].return_type.generic_args[0].name == "T"


def test_generic_in_parameter_type():
    """Test generic type in parameter."""
    code = """
function process<T>(items: List<T>) -> void {
    pass
}
"""
    ir = parse_al(code)
    param_type = ir.functions[0].params[0].param_type
    assert param_type.name == "List"
    assert param_type.generic_args[0].name == "T"


def test_generic_whitespace_handling():
    """Test that whitespace around generic brackets is handled correctly."""
    code1 = """
enum Option<T>:
    - Some(value: T)
    - None
"""
    code2 = """
enum Option < T > :
    - Some(value: T)
    - None
"""
    # Both should parse (whitespace around < > is allowed)
    ir1 = parse_al(code1)
    ir2 = parse_al(code2)

    assert ir1.enums[0].generic_params == ["T"]
    assert ir2.enums[0].generic_params == ["T"]


def test_complex_nested_generics():
    """Test complex nested generic structures."""
    code = """
function transform<T, U>(data: Map<string, List<T>>, fn: function(T) -> U) -> Map<string, List<U>> {
    return {}
}
"""
    ir = parse_al(code)

    # Check input parameter type: Map<string, List<T>>
    input_type = ir.functions[0].params[0].param_type
    assert input_type.name == "Map"
    assert input_type.generic_args[0].name == "string"
    assert input_type.generic_args[1].name == "List"
    assert input_type.generic_args[1].generic_args[0].name == "T"

    # Check return type: Map<string, List<U>>
    return_type = ir.functions[0].return_type
    assert return_type.name == "Map"
    assert return_type.generic_args[0].name == "string"
    assert return_type.generic_args[1].name == "List"
    assert return_type.generic_args[1].generic_args[0].name == "U"


def test_enum_variant_with_generic_type():
    """Test enum variant with associated type using generic parameter."""
    code = """
enum Container<T>:
    - Empty
    - Single(item: T)
    - Multiple(items: List<T>)
"""
    ir = parse_al(code)
    assert ir.enums[0].generic_params == ["T"]
    assert ir.enums[0].variants[1].name == "Single"
    assert ir.enums[0].variants[1].associated_types[0].name == "T"
    assert ir.enums[0].variants[2].associated_types[0].name == "List"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
