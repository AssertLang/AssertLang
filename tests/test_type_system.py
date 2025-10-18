"""
Comprehensive tests for the AssertLang Universal Type System.

Tests cover:
- Cross-language type mappings
- Type inference from literals and expressions
- Type compatibility checking
- Type normalization
- Import generation
"""

import pytest

from dsl.ir import (
    BinaryOperator,
    IRAssignment,
    IRBinaryOp,
    IRCall,
    IRFunction,
    IRIdentifier,
    IRLiteral,
    IRModule,
    IRParameter,
    IRPropertyAccess,
    IRType,
    LiteralType,
)
from dsl.type_system import TypeInfo, TypeSystem


# ============================================================================
# Fixtures
# ============================================================================


@pytest.fixture
def type_system():
    """Create a TypeSystem instance."""
    return TypeSystem()


# ============================================================================
# Primitive Type Mapping Tests
# ============================================================================


def test_map_string_to_all_languages(type_system):
    """Test string type mapping to all languages."""
    string_type = IRType(name="string")

    assert type_system.map_to_language(string_type, "python") == "str"
    assert type_system.map_to_language(string_type, "go") == "string"
    assert type_system.map_to_language(string_type, "rust") == "String"
    assert type_system.map_to_language(string_type, "dotnet") == "string"
    assert type_system.map_to_language(string_type, "nodejs") == "string"


def test_map_int_to_all_languages(type_system):
    """Test int type mapping to all languages."""
    int_type = IRType(name="int")

    assert type_system.map_to_language(int_type, "python") == "int"
    assert type_system.map_to_language(int_type, "go") == "int"
    assert type_system.map_to_language(int_type, "rust") == "i32"
    assert type_system.map_to_language(int_type, "dotnet") == "int"
    assert type_system.map_to_language(int_type, "nodejs") == "number"


def test_map_float_to_all_languages(type_system):
    """Test float type mapping to all languages."""
    float_type = IRType(name="float")

    assert type_system.map_to_language(float_type, "python") == "float"
    assert type_system.map_to_language(float_type, "go") == "float64"
    assert type_system.map_to_language(float_type, "rust") == "f64"
    assert type_system.map_to_language(float_type, "dotnet") == "double"
    assert type_system.map_to_language(float_type, "nodejs") == "number"


def test_map_bool_to_all_languages(type_system):
    """Test bool type mapping to all languages."""
    bool_type = IRType(name="bool")

    assert type_system.map_to_language(bool_type, "python") == "bool"
    assert type_system.map_to_language(bool_type, "go") == "bool"
    assert type_system.map_to_language(bool_type, "rust") == "bool"
    assert type_system.map_to_language(bool_type, "dotnet") == "bool"
    assert type_system.map_to_language(bool_type, "nodejs") == "boolean"


def test_map_null_to_all_languages(type_system):
    """Test null type mapping to all languages."""
    null_type = IRType(name="null")

    assert type_system.map_to_language(null_type, "python") == "None"
    assert type_system.map_to_language(null_type, "go") == "nil"
    assert type_system.map_to_language(null_type, "rust") == "None"
    assert type_system.map_to_language(null_type, "dotnet") == "null"
    assert type_system.map_to_language(null_type, "nodejs") == "null"


def test_map_any_to_all_languages(type_system):
    """Test any type mapping to all languages."""
    any_type = IRType(name="any")

    assert type_system.map_to_language(any_type, "python") == "Any"
    assert type_system.map_to_language(any_type, "go") == "interface{}"
    assert type_system.map_to_language(any_type, "rust") == "Box<dyn std::any::Any>"
    assert type_system.map_to_language(any_type, "dotnet") == "object"
    assert type_system.map_to_language(any_type, "nodejs") == "any"


# ============================================================================
# Collection Type Mapping Tests
# ============================================================================


def test_map_array_to_all_languages(type_system):
    """Test array<string> mapping to all languages."""
    array_type = IRType(
        name="array",
        generic_args=[IRType(name="string")]
    )

    assert type_system.map_to_language(array_type, "python") == "List[str]"
    assert type_system.map_to_language(array_type, "go") == "[]string"
    assert type_system.map_to_language(array_type, "rust") == "Vec<String>"
    assert type_system.map_to_language(array_type, "dotnet") == "List[string]"
    assert type_system.map_to_language(array_type, "nodejs") == "Array[string]"


def test_map_map_to_all_languages(type_system):
    """Test map<string, int> mapping to all languages."""
    map_type = IRType(
        name="map",
        generic_args=[IRType(name="string"), IRType(name="int")]
    )

    assert type_system.map_to_language(map_type, "python") == "Dict[str, int]"
    assert type_system.map_to_language(map_type, "go") == "map[string]int"
    assert type_system.map_to_language(map_type, "rust") == "HashMap<String, i32>"
    assert type_system.map_to_language(map_type, "dotnet") == "Dictionary[string, int]"
    assert type_system.map_to_language(map_type, "nodejs") == "Map[string, number]"


def test_map_nested_collections(type_system):
    """Test nested collection types: array<array<int>>."""
    nested_type = IRType(
        name="array",
        generic_args=[
            IRType(
                name="array",
                generic_args=[IRType(name="int")]
            )
        ]
    )

    assert type_system.map_to_language(nested_type, "python") == "List[List[int]]"
    assert type_system.map_to_language(nested_type, "go") == "[][]int"
    assert type_system.map_to_language(nested_type, "rust") == "Vec<Vec<i32>>"


# ============================================================================
# Optional Type Mapping Tests
# ============================================================================


def test_map_optional_int_to_all_languages(type_system):
    """Test int? mapping to all languages."""
    optional_type = IRType(name="int", is_optional=True)

    assert type_system.map_to_language(optional_type, "python") == "Optional[int]"
    assert type_system.map_to_language(optional_type, "go") == "*int"
    assert type_system.map_to_language(optional_type, "rust") == "Option<i32>"
    assert type_system.map_to_language(optional_type, "dotnet") == "int?"
    assert type_system.map_to_language(optional_type, "nodejs") == "number | null"


def test_map_optional_string_to_all_languages(type_system):
    """Test string? mapping to all languages."""
    optional_type = IRType(name="string", is_optional=True)

    assert type_system.map_to_language(optional_type, "python") == "Optional[str]"
    assert type_system.map_to_language(optional_type, "go") == "*string"
    assert type_system.map_to_language(optional_type, "rust") == "Option<String>"
    assert type_system.map_to_language(optional_type, "dotnet") == "string"  # Reference types already nullable
    assert type_system.map_to_language(optional_type, "nodejs") == "string | null"


# ============================================================================
# Union Type Mapping Tests
# ============================================================================


def test_map_union_to_all_languages(type_system):
    """Test string|int union mapping to all languages."""
    union_type = IRType(
        name="string",
        union_types=[IRType(name="int")]
    )

    assert type_system.map_to_language(union_type, "python") == "Union[str, int]"
    assert type_system.map_to_language(union_type, "go") == "interface{}"  # Go doesn't have unions
    assert "Union" in type_system.map_to_language(union_type, "rust")  # Rust uses comments for now
    assert type_system.map_to_language(union_type, "dotnet") == "object"  # C# doesn't have unions
    assert type_system.map_to_language(union_type, "nodejs") == "string | number"


# ============================================================================
# Reverse Mapping Tests
# ============================================================================


def test_map_from_python_types(type_system):
    """Test mapping Python types back to PW types."""
    assert type_system.map_from_language("str", "python").name == "string"
    assert type_system.map_from_language("int", "python").name == "int"
    assert type_system.map_from_language("float", "python").name == "float"
    assert type_system.map_from_language("bool", "python").name == "bool"


def test_map_from_python_collections(type_system):
    """Test mapping Python collection types back to PW types."""
    list_type = type_system.map_from_language("List[str]", "python")
    assert list_type.name == "array"
    assert len(list_type.generic_args) == 1
    assert list_type.generic_args[0].name == "string"

    dict_type = type_system.map_from_language("Dict[str, int]", "python")
    assert dict_type.name == "map"
    assert len(dict_type.generic_args) == 2
    assert dict_type.generic_args[0].name == "string"
    assert dict_type.generic_args[1].name == "int"


def test_map_from_python_optional(type_system):
    """Test mapping Python Optional types back to PW types."""
    opt_type = type_system.map_from_language("Optional[int]", "python")
    assert opt_type.name == "int"
    assert opt_type.is_optional is True


# ============================================================================
# Type Inference Tests
# ============================================================================


def test_infer_from_string_literal(type_system):
    """Test type inference from string literal."""
    literal = IRLiteral(value="hello", literal_type=LiteralType.STRING)
    type_info = type_system.infer_from_literal(literal)

    assert type_info.pw_type == "string"
    assert type_info.confidence == 1.0
    assert type_info.source == "literal"


def test_infer_from_int_literal(type_system):
    """Test type inference from int literal."""
    literal = IRLiteral(value=42, literal_type=LiteralType.INTEGER)
    type_info = type_system.infer_from_literal(literal)

    assert type_info.pw_type == "int"
    assert type_info.confidence == 1.0


def test_infer_from_float_literal(type_system):
    """Test type inference from float literal."""
    literal = IRLiteral(value=3.14, literal_type=LiteralType.FLOAT)
    type_info = type_system.infer_from_literal(literal)

    assert type_info.pw_type == "float"
    assert type_info.confidence == 1.0


def test_infer_from_bool_literal(type_system):
    """Test type inference from bool literal."""
    literal = IRLiteral(value=True, literal_type=LiteralType.BOOLEAN)
    type_info = type_system.infer_from_literal(literal)

    assert type_info.pw_type == "bool"
    assert type_info.confidence == 1.0


def test_infer_from_null_literal(type_system):
    """Test type inference from null literal."""
    literal = IRLiteral(value=None, literal_type=LiteralType.NULL)
    type_info = type_system.infer_from_literal(literal)

    assert type_info.pw_type == "null"
    assert type_info.nullable is True


def test_infer_from_arithmetic_expression(type_system):
    """Test type inference from arithmetic expression (a + b)."""
    # Context: a: int, b: int
    context = {
        "a": TypeInfo(pw_type="int", confidence=1.0, source="explicit"),
        "b": TypeInfo(pw_type="int", confidence=1.0, source="explicit"),
    }

    expr = IRBinaryOp(
        op=BinaryOperator.ADD,
        left=IRIdentifier(name="a"),
        right=IRIdentifier(name="b")
    )

    type_info = type_system.infer_from_expression(expr, context)
    assert type_info.pw_type == "int"
    assert type_info.confidence == 0.9


def test_infer_from_float_arithmetic(type_system):
    """Test type inference from float arithmetic (a + b where a is float)."""
    context = {
        "a": TypeInfo(pw_type="float", confidence=1.0, source="explicit"),
        "b": TypeInfo(pw_type="int", confidence=1.0, source="explicit"),
    }

    expr = IRBinaryOp(
        op=BinaryOperator.ADD,
        left=IRIdentifier(name="a"),
        right=IRIdentifier(name="b")
    )

    type_info = type_system.infer_from_expression(expr, context)
    assert type_info.pw_type == "float"  # Float takes precedence


def test_infer_from_comparison_expression(type_system):
    """Test type inference from comparison (a > b)."""
    context = {
        "a": TypeInfo(pw_type="int", confidence=1.0, source="explicit"),
        "b": TypeInfo(pw_type="int", confidence=1.0, source="explicit"),
    }

    expr = IRBinaryOp(
        op=BinaryOperator.GREATER_THAN,
        left=IRIdentifier(name="a"),
        right=IRIdentifier(name="b")
    )

    type_info = type_system.infer_from_expression(expr, context)
    assert type_info.pw_type == "bool"
    assert type_info.confidence == 1.0


def test_infer_from_logical_expression(type_system):
    """Test type inference from logical expression (a and b)."""
    context = {
        "a": TypeInfo(pw_type="bool", confidence=1.0, source="explicit"),
        "b": TypeInfo(pw_type="bool", confidence=1.0, source="explicit"),
    }

    expr = IRBinaryOp(
        op=BinaryOperator.AND,
        left=IRIdentifier(name="a"),
        right=IRIdentifier(name="b")
    )

    type_info = type_system.infer_from_expression(expr, context)
    assert type_info.pw_type == "bool"
    assert type_info.confidence == 1.0


def test_infer_from_usage_in_function(type_system):
    """Test type inference from variable usage in function."""
    # Function: def test(x: int) -> int: y = x + 1; return y
    func = IRFunction(
        name="test",
        params=[
            IRParameter(name="x", param_type=IRType(name="int"))
        ],
        return_type=IRType(name="int"),
        body=[
            IRAssignment(
                target="y",
                value=IRBinaryOp(
                    op=BinaryOperator.ADD,
                    left=IRIdentifier(name="x"),
                    right=IRLiteral(value=1, literal_type=LiteralType.INTEGER)
                )
            )
        ]
    )

    type_info = type_system.infer_from_usage("y", func)
    assert type_info.pw_type == "int"


def test_propagate_types_through_module(type_system):
    """Test type propagation through entire module."""
    module = IRModule(
        name="test",
        functions=[
            IRFunction(
                name="add",
                params=[
                    IRParameter(name="a", param_type=IRType(name="int")),
                    IRParameter(name="b", param_type=IRType(name="int"))
                ],
                body=[
                    IRAssignment(
                        target="result",
                        value=IRBinaryOp(
                            op=BinaryOperator.ADD,
                            left=IRIdentifier(name="a"),
                            right=IRIdentifier(name="b")
                        )
                    )
                ]
            )
        ]
    )

    type_map = type_system.propagate_types(module)

    # Check parameter types
    assert "add.a" in type_map
    assert type_map["add.a"].pw_type == "int"
    assert type_map["add.a"].confidence == 1.0

    # Check inferred variable type
    assert "add.result" in type_map
    assert type_map["add.result"].pw_type == "int"


# ============================================================================
# Type Compatibility Tests
# ============================================================================


def test_same_type_compatible(type_system):
    """Test that same types are compatible."""
    assert type_system.is_compatible("string", "string") is True
    assert type_system.is_compatible("int", "int") is True
    assert type_system.is_compatible("bool", "bool") is True


def test_any_type_compatible_with_all(type_system):
    """Test that 'any' is compatible with all types."""
    assert type_system.is_compatible("any", "string") is True
    assert type_system.is_compatible("string", "any") is True
    assert type_system.is_compatible("any", "int") is True
    assert type_system.is_compatible("int", "any") is True


def test_null_compatible_with_all(type_system):
    """Test that null is compatible with all types."""
    assert type_system.is_compatible("null", "string") is True
    assert type_system.is_compatible("null", "int") is True
    assert type_system.is_compatible("null", "bool") is True


def test_int_to_float_widening(type_system):
    """Test int -> float widening conversion."""
    assert type_system.is_compatible("int", "float") is True


def test_float_to_int_not_compatible(type_system):
    """Test float -> int narrowing not compatible."""
    assert type_system.is_compatible("float", "int") is False


def test_incompatible_types(type_system):
    """Test incompatible types."""
    assert type_system.is_compatible("string", "int") is False
    assert type_system.is_compatible("bool", "string") is False
    assert type_system.is_compatible("int", "bool") is False


def test_needs_cast_for_narrowing(type_system):
    """Test that narrowing conversions need cast."""
    assert type_system.needs_cast("float", "int") is True


def test_needs_cast_for_string_conversion(type_system):
    """Test that conversions to string need cast."""
    assert type_system.needs_cast("int", "string") is True
    assert type_system.needs_cast("bool", "string") is True


def test_no_cast_for_compatible_types(type_system):
    """Test that compatible types don't need cast."""
    assert type_system.needs_cast("int", "float") is False
    assert type_system.needs_cast("string", "string") is False


# ============================================================================
# Type Normalization Tests
# ============================================================================


def test_normalize_simple_type(type_system):
    """Test normalization of simple type."""
    ir_type = type_system.normalize_type("string")
    assert ir_type.name == "string"
    assert ir_type.generic_args == []
    assert ir_type.is_optional is False


def test_normalize_optional_type(type_system):
    """Test normalization of optional type (int?)."""
    ir_type = type_system.normalize_type("int?")
    assert ir_type.name == "int"
    assert ir_type.is_optional is True


def test_normalize_array_type(type_system):
    """Test normalization of array type (array<string>)."""
    ir_type = type_system.normalize_type("array<string>")
    assert ir_type.name == "array"
    assert len(ir_type.generic_args) == 1
    assert ir_type.generic_args[0].name == "string"


def test_normalize_map_type(type_system):
    """Test normalization of map type (map<string, int>)."""
    ir_type = type_system.normalize_type("map<string, int>")
    assert ir_type.name == "map"
    assert len(ir_type.generic_args) == 2
    assert ir_type.generic_args[0].name == "string"
    assert ir_type.generic_args[1].name == "int"


def test_normalize_nested_generics(type_system):
    """Test normalization of nested generics (array<array<int>>)."""
    ir_type = type_system.normalize_type("array<array<int>>")
    assert ir_type.name == "array"
    assert len(ir_type.generic_args) == 1
    assert ir_type.generic_args[0].name == "array"
    assert len(ir_type.generic_args[0].generic_args) == 1
    assert ir_type.generic_args[0].generic_args[0].name == "int"


def test_normalize_union_type(type_system):
    """Test normalization of union type (string|int)."""
    ir_type = type_system.normalize_type("string|int")
    assert ir_type.name == "string"
    assert len(ir_type.union_types) == 1
    assert ir_type.union_types[0].name == "int"


def test_normalize_complex_union(type_system):
    """Test normalization of complex union (string|int|bool)."""
    ir_type = type_system.normalize_type("string|int|bool")
    assert ir_type.name == "string"
    assert len(ir_type.union_types) == 2
    assert ir_type.union_types[0].name == "int"
    assert ir_type.union_types[1].name == "bool"


# ============================================================================
# Import Generation Tests
# ============================================================================


def test_get_python_imports_for_list(type_system):
    """Test getting Python imports for List type."""
    types = [
        IRType(
            name="array",
            generic_args=[IRType(name="string")]
        )
    ]

    imports = type_system.get_required_imports(types, "python")
    assert "from typing import List" in imports


def test_get_python_imports_for_dict(type_system):
    """Test getting Python imports for Dict type."""
    types = [
        IRType(
            name="map",
            generic_args=[IRType(name="string"), IRType(name="int")]
        )
    ]

    imports = type_system.get_required_imports(types, "python")
    assert "from typing import Dict" in imports


def test_get_python_imports_for_optional(type_system):
    """Test getting Python imports for Optional type."""
    types = [
        IRType(name="int", is_optional=True)
    ]

    imports = type_system.get_required_imports(types, "python")
    assert "from typing import Optional" in imports


def test_get_python_imports_for_union(type_system):
    """Test getting Python imports for Union type."""
    types = [
        IRType(
            name="string",
            union_types=[IRType(name="int")]
        )
    ]

    imports = type_system.get_required_imports(types, "python")
    assert "from typing import Union" in imports


def test_get_rust_imports_for_hashmap(type_system):
    """Test getting Rust imports for HashMap type."""
    types = [
        IRType(
            name="map",
            generic_args=[IRType(name="string"), IRType(name="int")]
        )
    ]

    imports = type_system.get_required_imports(types, "rust")
    assert "use std::collections::HashMap;" in imports


def test_get_dotnet_imports_for_collections(type_system):
    """Test getting .NET imports for List/Dictionary types."""
    types = [
        IRType(
            name="array",
            generic_args=[IRType(name="string")]
        ),
        IRType(
            name="map",
            generic_args=[IRType(name="string"), IRType(name="int")]
        )
    ]

    imports = type_system.get_required_imports(types, "dotnet")
    assert "using System.Collections.Generic;" in imports


# ============================================================================
# Custom Type Tests
# ============================================================================


def test_custom_type_preserved(type_system):
    """Test that custom types are preserved across languages."""
    user_type = IRType(name="User")

    assert type_system.map_to_language(user_type, "python") == "User"
    assert type_system.map_to_language(user_type, "go") == "User"
    assert type_system.map_to_language(user_type, "rust") == "User"
    assert type_system.map_to_language(user_type, "dotnet") == "User"
    assert type_system.map_to_language(user_type, "nodejs") == "User"


def test_custom_type_with_generics(type_system):
    """Test custom type with generic arguments."""
    result_type = IRType(
        name="Result",
        generic_args=[IRType(name="string"), IRType(name="Error")]
    )

    # Custom types with generics follow language syntax
    python_result = type_system.map_to_language(result_type, "python")
    assert "Result" in python_result
    assert "str" in python_result


# ============================================================================
# Edge Cases and Error Handling
# ============================================================================


def test_empty_context_inference(type_system):
    """Test type inference with empty context."""
    context = {}
    expr = IRIdentifier(name="unknown_var")

    type_info = type_system.infer_from_expression(expr, context)
    assert type_info.pw_type == "any"
    assert type_info.confidence == 0.0


def test_complex_nested_expression(type_system):
    """Test type inference for complex nested expression."""
    # Expression: (a + b) > (c * d)
    context = {
        "a": TypeInfo(pw_type="int", confidence=1.0, source="explicit"),
        "b": TypeInfo(pw_type="int", confidence=1.0, source="explicit"),
        "c": TypeInfo(pw_type="int", confidence=1.0, source="explicit"),
        "d": TypeInfo(pw_type="int", confidence=1.0, source="explicit"),
    }

    expr = IRBinaryOp(
        op=BinaryOperator.GREATER_THAN,
        left=IRBinaryOp(
            op=BinaryOperator.ADD,
            left=IRIdentifier(name="a"),
            right=IRIdentifier(name="b")
        ),
        right=IRBinaryOp(
            op=BinaryOperator.MULTIPLY,
            left=IRIdentifier(name="c"),
            right=IRIdentifier(name="d")
        )
    )

    type_info = type_system.infer_from_expression(expr, context)
    assert type_info.pw_type == "bool"


def test_property_access_inference(type_system):
    """Test type inference for property access."""
    context = {
        "user": TypeInfo(pw_type="User", confidence=1.0, source="explicit")
    }

    expr = IRPropertyAccess(
        object=IRIdentifier(name="user"),
        property="name"
    )

    type_info = type_system.infer_from_expression(expr, context)
    # Without type definitions, we return 'any' with low confidence
    assert type_info.pw_type == "any"
    assert type_info.confidence == 0.3


def test_function_call_inference(type_system):
    """Test type inference for function calls."""
    context = {
        "database": TypeInfo(pw_type="Database", confidence=1.0, source="explicit")
    }

    expr = IRCall(
        function=IRPropertyAccess(
            object=IRIdentifier(name="database"),
            property="get_user"
        ),
        args=[IRLiteral(value="123", literal_type=LiteralType.STRING)]
    )

    type_info = type_system.infer_from_expression(expr, context)
    # Without function signatures, we return 'any'
    assert type_info.pw_type == "any"
