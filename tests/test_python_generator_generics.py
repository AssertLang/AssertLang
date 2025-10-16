"""
Test Python code generation for generic type parameters.

This test suite verifies that the Python generator correctly handles:
- Generic enums (Option<T>, Result<T,E>)
- Generic functions (function foo<T>())
- Generic classes (class List<T>)
- Nested generics (List<Option<int>>)
"""

import ast
import pytest

from dsl.ir import (
    IRClass,
    IREnum,
    IREnumVariant,
    IRFunction,
    IRModule,
    IRParameter,
    IRProperty,
    IRType,
)
from language.python_generator_v2 import PythonGeneratorV2


class TestGenericEnumGeneration:
    """Test generic enum code generation."""

    def test_generate_option_enum(self):
        """Test Option<T> enum generates correct Python dataclasses."""
        # Create Option<T> enum
        option_enum = IREnum(
            name="Option",
            generic_params=["T"],
            variants=[
                IREnumVariant(
                    name="Some",
                    associated_types=[IRType(name="T")],
                ),
                IREnumVariant(
                    name="None",
                    associated_types=[],
                ),
            ],
            doc="Represents an optional value",
        )

        module = IRModule(
            name="test_option",
            enums=[option_enum],
        )

        generator = PythonGeneratorV2()
        code = generator.generate(module)

        print("\n=== Generated Option<T> Code ===")
        print(code)
        print("=" * 40)

        # Verify TypeVar is defined
        assert "T = TypeVar('T')" in code

        # Verify Some dataclass
        assert "@dataclass" in code
        assert "class Some(Generic[T]):" in code
        assert "value: T" in code

        # Verify None_ dataclass (with underscore to avoid Python keyword)
        assert "class None_:" in code
        assert "pass" in code

        # Verify Union type alias
        assert "Option = Union[Some[T], None_]" in code

        # Verify imports
        assert "from typing import" in code
        assert "TypeVar" in code
        assert "Generic" in code
        assert "Union" in code

        # Verify syntactically valid Python
        ast.parse(code)

    def test_generate_result_enum(self):
        """Test Result<T, E> enum with multiple type parameters."""
        result_enum = IREnum(
            name="Result",
            generic_params=["T", "E"],
            variants=[
                IREnumVariant(
                    name="Ok",
                    associated_types=[IRType(name="T")],
                ),
                IREnumVariant(
                    name="Err",
                    associated_types=[IRType(name="E")],
                ),
            ],
            doc="Represents success or failure",
        )

        module = IRModule(
            name="test_result",
            enums=[result_enum],
        )

        generator = PythonGeneratorV2()
        code = generator.generate(module)

        print("\n=== Generated Result<T, E> Code ===")
        print(code)
        print("=" * 40)

        # Verify TypeVars for both parameters
        assert "T = TypeVar('T')" in code
        assert "E = TypeVar('E')" in code

        # Verify Ok variant
        assert "class Ok(Generic[T, E]):" in code
        assert "value: T" in code

        # Verify Err variant
        assert "class Err(Generic[T, E]):" in code
        # Note: Err also uses Generic[T, E] even though it only uses E
        # This keeps the type signature consistent

        # Verify Union type alias
        assert "Result = Union[Ok[T, E], Err[T, E]]" in code

        # Verify syntactically valid Python
        ast.parse(code)

    def test_generate_non_generic_enum(self):
        """Test that non-generic enums still generate as Enum class."""
        status_enum = IREnum(
            name="Status",
            generic_params=[],
            variants=[
                IREnumVariant(name="Pending", value=1),
                IREnumVariant(name="Active", value=2),
                IREnumVariant(name="Completed", value=3),
            ],
        )

        module = IRModule(
            name="test_status",
            enums=[status_enum],
        )

        generator = PythonGeneratorV2()
        code = generator.generate(module)

        print("\n=== Generated Status Enum Code ===")
        print(code)
        print("=" * 40)

        # Non-generic enums should use standard Enum
        assert "from enum import Enum" in code
        assert "class Status(Enum):" in code
        assert "Pending = 1" in code
        assert "Active = 2" in code
        assert "Completed = 3" in code

        # Should NOT have TypeVar or Generic
        assert "TypeVar" not in code
        assert "Generic" not in code

        # Verify syntactically valid Python
        ast.parse(code)


class TestGenericFunctionGeneration:
    """Test generic function code generation."""

    def test_generate_generic_function_single_param(self):
        """Test function with single type parameter."""
        func = IRFunction(
            name="option_some",
            generic_params=["T"],
            params=[
                IRParameter(
                    name="value",
                    param_type=IRType(name="T"),
                ),
            ],
            return_type=IRType(
                name="Option",
                generic_args=[IRType(name="T")],
            ),
            body=[],
            doc="Create an Option with a value",
        )

        module = IRModule(
            name="test_func",
            functions=[func],
        )

        generator = PythonGeneratorV2()
        code = generator.generate(module)

        print("\n=== Generated Generic Function Code ===")
        print(code)
        print("=" * 40)

        # Verify function signature
        assert "def option_some(value: T) -> Option[T]:" in code

        # Verify docstring
        assert '"""Create an Option with a value"""' in code

        # Verify TypeVar import
        assert "from typing import" in code
        assert "TypeVar" in code

        # Verify syntactically valid Python
        ast.parse(code)

    def test_generate_generic_function_multiple_params(self):
        """Test function with multiple type parameters."""
        func = IRFunction(
            name="option_map",
            generic_params=["T", "U"],
            params=[
                IRParameter(
                    name="opt",
                    param_type=IRType(
                        name="Option",
                        generic_args=[IRType(name="T")],
                    ),
                ),
                IRParameter(
                    name="fn",
                    param_type=IRType(
                        name="function",
                        generic_args=[IRType(name="T"), IRType(name="U")],
                    ),
                ),
            ],
            return_type=IRType(
                name="Option",
                generic_args=[IRType(name="U")],
            ),
            body=[],
            doc="Transform the value inside Some",
        )

        module = IRModule(
            name="test_func",
            functions=[func],
        )

        generator = PythonGeneratorV2()
        code = generator.generate(module)

        print("\n=== Generated option_map Code ===")
        print(code)
        print("=" * 40)

        # Verify function signature with generic types
        assert "def option_map(opt: Option[T], fn: function[T, U]) -> Option[U]:" in code

        # Verify TypeVar import
        assert "TypeVar" in code

        # Verify syntactically valid Python
        ast.parse(code)


class TestGenericClassGeneration:
    """Test generic class code generation."""

    def test_generate_generic_class_single_param(self):
        """Test class with single type parameter."""
        list_class = IRClass(
            name="List",
            generic_params=["T"],
            properties=[
                IRProperty(
                    name="items",
                    prop_type=IRType(
                        name="array",
                        generic_args=[IRType(name="T")],
                    ),
                ),
            ],
            doc="A generic list container",
        )

        module = IRModule(
            name="test_class",
            classes=[list_class],
        )

        generator = PythonGeneratorV2()
        code = generator.generate(module)

        print("\n=== Generated List<T> Class Code ===")
        print(code)
        print("=" * 40)

        # Verify class signature
        assert "class List(Generic[T]):" in code

        # Verify docstring
        assert '"""A generic list container"""' in code

        # Verify property with generic type
        assert "items: List[T]" in code or "items: array[T]" in code

        # Verify imports
        assert "TypeVar" in code
        assert "Generic" in code

        # Verify syntactically valid Python
        ast.parse(code)

    def test_generate_generic_class_multiple_params(self):
        """Test class with multiple type parameters."""
        map_class = IRClass(
            name="Map",
            generic_params=["K", "V"],
            properties=[
                IRProperty(
                    name="entries",
                    prop_type=IRType(
                        name="dict",
                        generic_args=[IRType(name="K"), IRType(name="V")],
                    ),
                ),
            ],
            doc="A generic map container",
        )

        module = IRModule(
            name="test_class",
            classes=[map_class],
        )

        generator = PythonGeneratorV2()
        code = generator.generate(module)

        print("\n=== Generated Map<K, V> Class Code ===")
        print(code)
        print("=" * 40)

        # Verify class signature with multiple type params
        assert "class Map(Generic[K, V]):" in code

        # Verify property with generic types
        assert "entries:" in code
        assert "Dict[K, V]" in code or "dict[K, V]" in code

        # Verify TypeVars
        assert "TypeVar" in code
        assert "Generic" in code

        # Verify syntactically valid Python
        ast.parse(code)

    def test_generate_non_generic_class(self):
        """Test that non-generic classes don't inherit from Generic."""
        user_class = IRClass(
            name="User",
            generic_params=[],
            properties=[
                IRProperty(
                    name="name",
                    prop_type=IRType(name="string"),
                ),
                IRProperty(
                    name="age",
                    prop_type=IRType(name="int"),
                ),
            ],
        )

        module = IRModule(
            name="test_class",
            classes=[user_class],
        )

        generator = PythonGeneratorV2()
        code = generator.generate(module)

        print("\n=== Generated User Class Code ===")
        print(code)
        print("=" * 40)

        # Verify class doesn't inherit from Generic
        assert "class User:" in code
        assert "Generic" not in code

        # Verify properties
        assert "name: str" in code
        assert "age: int" in code

        # Verify syntactically valid Python
        ast.parse(code)


class TestNestedGenerics:
    """Test nested generic type generation."""

    def test_nested_generic_types(self):
        """Test List<Option<int>> style nested generics."""
        func = IRFunction(
            name="get_items",
            generic_params=[],
            params=[],
            return_type=IRType(
                name="List",
                generic_args=[
                    IRType(
                        name="Option",
                        generic_args=[IRType(name="int")],
                    ),
                ],
            ),
            body=[],
        )

        module = IRModule(
            name="test_nested",
            functions=[func],
        )

        generator = PythonGeneratorV2()
        code = generator.generate(module)

        print("\n=== Generated Nested Generic Code ===")
        print(code)
        print("=" * 40)

        # Verify nested generic type in return annotation
        assert "def get_items() -> List[Option[int]]:" in code

        # Verify syntactically valid Python
        ast.parse(code)


class TestStdlibCodeGeneration:
    """Test that stdlib files generate valid Python."""

    def test_option_type_generates_valid_python(self):
        """Test that Option<T> from stdlib generates valid Python."""
        # This test would parse stdlib/core.al and generate Python
        # For now, we verify the structure matches what we expect
        option_enum = IREnum(
            name="Option",
            generic_params=["T"],
            variants=[
                IREnumVariant(name="Some", associated_types=[IRType(name="T")]),
                IREnumVariant(name="None", associated_types=[]),
            ],
        )

        module = IRModule(name="core", enums=[option_enum])

        generator = PythonGeneratorV2()
        code = generator.generate(module)

        # Must be syntactically valid Python
        ast.parse(code)

        # Verify key components
        assert "T = TypeVar('T')" in code
        assert "class Some(Generic[T]):" in code
        assert "class None_:" in code
        assert "Option = Union[Some[T], None_]" in code

    def test_result_type_generates_valid_python(self):
        """Test that Result<T, E> from stdlib generates valid Python."""
        result_enum = IREnum(
            name="Result",
            generic_params=["T", "E"],
            variants=[
                IREnumVariant(name="Ok", associated_types=[IRType(name="T")]),
                IREnumVariant(name="Err", associated_types=[IRType(name="E")]),
            ],
        )

        module = IRModule(name="core", enums=[result_enum])

        generator = PythonGeneratorV2()
        code = generator.generate(module)

        # Must be syntactically valid Python
        ast.parse(code)

        # Verify key components
        assert "T = TypeVar('T')" in code
        assert "E = TypeVar('E')" in code
        assert "class Ok(Generic[T, E]):" in code
        assert "class Err(Generic[T, E]):" in code
        assert "Result = Union[Ok[T, E], Err[T, E]]" in code


class TestEdgeCases:
    """Test edge cases and error handling."""

    def test_enum_variant_with_multiple_associated_types(self):
        """Test enum variant with multiple associated types."""
        enum = IREnum(
            name="Pair",
            generic_params=["A", "B"],
            variants=[
                IREnumVariant(
                    name="Both",
                    associated_types=[IRType(name="A"), IRType(name="B")],
                ),
            ],
        )

        module = IRModule(name="test", enums=[enum])

        generator = PythonGeneratorV2()
        code = generator.generate(module)

        print("\n=== Generated Pair Enum Code ===")
        print(code)
        print("=" * 40)

        # Verify multiple fields
        assert "class Both(Generic[A, B]):" in code
        assert "field_0: A" in code
        assert "field_1: B" in code

        # Verify syntactically valid Python
        ast.parse(code)

    def test_empty_generic_class(self):
        """Test generic class with no properties."""
        empty_class = IRClass(
            name="Empty",
            generic_params=["T"],
            properties=[],
        )

        module = IRModule(name="test", classes=[empty_class])

        generator = PythonGeneratorV2()
        code = generator.generate(module)

        print("\n=== Generated Empty Generic Class Code ===")
        print(code)
        print("=" * 40)

        # Should still inherit from Generic
        assert "class Empty(Generic[T]):" in code
        assert "pass" in code

        # Verify syntactically valid Python
        ast.parse(code)


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
