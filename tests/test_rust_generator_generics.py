"""
Test Suite for Rust Generator Generic Type Parameters

Tests the generation of generic enums, functions, and structs/classes
to verify that stdlib code (Option<T>, Result<T,E>, List<T>, etc.)
can be correctly transpiled to Rust.
"""

import pytest
from language.rust_generator_v2 import RustGeneratorV2, generate_rust
from dsl.ir import (
    IRModule,
    IREnum,
    IREnumVariant,
    IRFunction,
    IRParameter,
    IRType,
    IRClass,
    IRProperty,
    IRReturn,
    IRIdentifier,
    IRLiteral,
    LiteralType,
)


class TestGenericEnums:
    """Test generic enum generation."""

    def test_generic_enum_single_param(self):
        """Test enum Option<T> generation."""
        enum = IREnum(
            name="Option",
            generic_params=["T"],
            variants=[
                IREnumVariant(name="Some", associated_types=[IRType(name="T")]),
                IREnumVariant(name="None"),
            ]
        )

        module = IRModule(name="test", version="1.0.0", enums=[enum])
        code = generate_rust(module)

        # Should generate: pub enum Option<T> {
        assert "pub enum Option<T> {" in code
        assert "Some(T)," in code
        assert "None," in code

    def test_generic_enum_multiple_params(self):
        """Test enum Result<T, E> generation."""
        enum = IREnum(
            name="Result",
            generic_params=["T", "E"],
            variants=[
                IREnumVariant(name="Ok", associated_types=[IRType(name="T")]),
                IREnumVariant(name="Err", associated_types=[IRType(name="E")]),
            ]
        )

        module = IRModule(name="test", version="1.0.0", enums=[enum])
        code = generate_rust(module)

        # Should generate: pub enum Result<T, E> {
        assert "pub enum Result<T, E> {" in code
        assert "Ok(T)," in code
        assert "Err(E)," in code

    def test_generic_enum_with_derives(self):
        """Test that generic enums still get proper derives."""
        enum = IREnum(
            name="Option",
            generic_params=["T"],
            variants=[
                IREnumVariant(name="Some", associated_types=[IRType(name="T")]),
                IREnumVariant(name="None"),
            ]
        )

        module = IRModule(name="test", version="1.0.0", enums=[enum])
        code = generate_rust(module)

        # Should have derives above the enum
        assert "#[derive(Debug, Clone, PartialEq)]" in code


class TestGenericFunctions:
    """Test generic function generation."""

    def test_generic_function_single_param(self):
        """Test function identity<T>(x: T) -> T."""
        func = IRFunction(
            name="identity",
            generic_params=["T"],
            params=[IRParameter(name="x", param_type=IRType(name="T"))],
            return_type=IRType(name="T"),
            body=[IRReturn(value=IRIdentifier(name="x"))]
        )

        module = IRModule(name="test", version="1.0.0", functions=[func])
        code = generate_rust(module)

        # Should generate: pub fn identity<T>(x: &T) -> T {
        assert "pub fn identity<T>" in code
        assert "-> T" in code

    def test_generic_function_multiple_params(self):
        """Test function map<T, U>(x: T) -> U."""
        func = IRFunction(
            name="option_map",
            generic_params=["T", "U"],
            params=[
                IRParameter(name="opt", param_type=IRType(name="Option", generic_args=[IRType(name="T")])),
                IRParameter(
                    name="fn",
                    param_type=IRType(
                        name="function",
                        # Function type (T) -> U
                    )
                ),
            ],
            return_type=IRType(name="Option", generic_args=[IRType(name="U")]),
            body=[
                IRReturn(
                    value=IRLiteral(value=None, literal_type=LiteralType.NULL)
                )
            ]
        )

        module = IRModule(name="test", version="1.0.0", functions=[func])
        code = generate_rust(module)

        # Should generate: pub fn option_map<T, U>(...) -> Option<U>
        assert "pub fn option_map<T, U>" in code
        assert "-> Option<U>" in code

    def test_generic_function_with_generic_return(self):
        """Test that generic type parameters work in return types."""
        func = IRFunction(
            name="make_list",
            generic_params=["T"],
            params=[],
            return_type=IRType(name="List", generic_args=[IRType(name="T")]),
            body=[]
        )

        module = IRModule(name="test", version="1.0.0", functions=[func])
        code = generate_rust(module)

        assert "pub fn make_list<T>" in code
        assert "-> List<T>" in code


class TestGenericClasses:
    """Test generic struct/class generation."""

    def test_generic_struct_single_param(self):
        """Test struct List<T> generation."""
        cls = IRClass(
            name="List",
            generic_params=["T"],
            properties=[
                IRProperty(
                    name="items",
                    prop_type=IRType(name="array", generic_args=[IRType(name="T")])
                )
            ]
        )

        module = IRModule(name="test", version="1.0.0", classes=[cls])
        code = generate_rust(module)

        # Should generate: pub struct List<T> {
        assert "pub struct List<T> {" in code
        assert "pub items: Vec<T>," in code
        # Should generate: impl<T> List<T> {
        assert "impl<T> List<T> {" in code

    def test_generic_struct_multiple_params(self):
        """Test struct Map<K, V> generation."""
        cls = IRClass(
            name="Map",
            generic_params=["K", "V"],
            properties=[
                IRProperty(
                    name="entries",
                    prop_type=IRType(name="map", generic_args=[IRType(name="K"), IRType(name="V")])
                )
            ]
        )

        module = IRModule(name="test", version="1.0.0", classes=[cls])
        code = generate_rust(module)

        # Should generate: pub struct Map<K, V> {
        assert "pub struct Map<K, V> {" in code
        assert "pub entries: HashMap<K, V>," in code
        # Should generate: impl<K, V> Map<K, V> {
        assert "impl<K, V> Map<K, V> {" in code

    def test_generic_struct_with_methods(self):
        """Test that generic structs can have methods."""
        cls = IRClass(
            name="List",
            generic_params=["T"],
            properties=[
                IRProperty(
                    name="items",
                    prop_type=IRType(name="array", generic_args=[IRType(name="T")])
                )
            ],
            methods=[
                IRFunction(
                    name="len",
                    params=[],
                    return_type=IRType(name="int"),
                    body=[
                        IRReturn(
                            value=IRLiteral(value=0, literal_type=LiteralType.INTEGER)
                        )
                    ]
                )
            ]
        )

        module = IRModule(name="test", version="1.0.0", classes=[cls])
        code = generate_rust(module)

        # Struct and impl should both have generics
        assert "pub struct List<T> {" in code
        assert "impl<T> List<T> {" in code
        assert "pub fn len() -> i32 {" in code


class TestNestedGenerics:
    """Test nested generic types."""

    def test_nested_generic_in_function_param(self):
        """Test function with Option<List<T>>."""
        func = IRFunction(
            name="process",
            generic_params=["T"],
            params=[
                IRParameter(
                    name="data",
                    param_type=IRType(
                        name="Option",
                        generic_args=[
                            IRType(
                                name="List",
                                generic_args=[IRType(name="T")]
                            )
                        ]
                    )
                )
            ],
            return_type=IRType(name="int"),
            body=[]
        )

        module = IRModule(name="test", version="1.0.0", functions=[func])
        code = generate_rust(module)

        # Should handle nested generics
        assert "pub fn process<T>" in code
        assert "Option<List<T>>" in code

    def test_nested_generic_in_struct_field(self):
        """Test struct with field Vec<Option<T>>."""
        cls = IRClass(
            name="Container",
            generic_params=["T"],
            properties=[
                IRProperty(
                    name="items",
                    prop_type=IRType(
                        name="array",
                        generic_args=[
                            IRType(
                                name="Option",
                                generic_args=[IRType(name="T")]
                            )
                        ]
                    )
                )
            ]
        )

        module = IRModule(name="test", version="1.0.0", classes=[cls])
        code = generate_rust(module)

        # Should handle nested generics in struct fields
        assert "pub struct Container<T> {" in code
        assert "Vec<Option<T>>" in code


class TestRealWorldStdlib:
    """Test generation of actual stdlib code patterns."""

    def test_option_enum_complete(self):
        """Test complete Option<T> enum as defined in stdlib/core.pw."""
        enum = IREnum(
            name="Option",
            generic_params=["T"],
            variants=[
                IREnumVariant(name="Some", associated_types=[IRType(name="T")]),
                IREnumVariant(name="None"),
            ],
            doc="Represents an optional value (Some or None)"
        )

        module = IRModule(name="core", version="1.0.0", enums=[enum])
        code = generate_rust(module)

        assert "/// Represents an optional value (Some or None)" in code
        assert "pub enum Option<T> {" in code
        assert "Some(T)," in code
        assert "None," in code

    def test_result_enum_complete(self):
        """Test complete Result<T, E> enum as defined in stdlib/core.pw."""
        enum = IREnum(
            name="Result",
            generic_params=["T", "E"],
            variants=[
                IREnumVariant(name="Ok", associated_types=[IRType(name="T")]),
                IREnumVariant(name="Err", associated_types=[IRType(name="E")]),
            ],
            doc="Represents success (Ok) or failure (Err) with typed errors"
        )

        module = IRModule(name="core", version="1.0.0", enums=[enum])
        code = generate_rust(module)

        assert "/// Represents success (Ok) or failure (Err) with typed errors" in code
        assert "pub enum Result<T, E> {" in code
        assert "Ok(T)," in code
        assert "Err(E)," in code

    def test_list_class_complete(self):
        """Test complete List<T> class as defined in stdlib/types.pw."""
        cls = IRClass(
            name="List",
            generic_params=["T"],
            properties=[
                IRProperty(
                    name="items",
                    prop_type=IRType(name="array", generic_args=[IRType(name="T")])
                )
            ],
            doc="A dynamically sized array that stores elements of type T."
        )

        module = IRModule(name="types", version="1.0.0", classes=[cls])
        code = generate_rust(module)

        assert "/// A dynamically sized array that stores elements of type T." in code
        assert "pub struct List<T> {" in code
        assert "pub items: Vec<T>," in code
        assert "impl<T> List<T> {" in code

    def test_map_class_complete(self):
        """Test complete Map<K, V> class as defined in stdlib/types.pw."""
        cls = IRClass(
            name="Map",
            generic_params=["K", "V"],
            properties=[
                IRProperty(
                    name="entries",
                    prop_type=IRType(name="map", generic_args=[IRType(name="K"), IRType(name="V")])
                )
            ],
            doc="A key-value store that maps keys of type K to values of type V."
        )

        module = IRModule(name="types", version="1.0.0", classes=[cls])
        code = generate_rust(module)

        assert "/// A key-value store that maps keys of type K to values of type V." in code
        assert "pub struct Map<K, V> {" in code
        assert "pub entries: HashMap<K, V>," in code
        assert "impl<K, V> Map<K, V> {" in code


class TestEdgeCases:
    """Test edge cases and error handling."""

    def test_non_generic_enum_still_works(self):
        """Test that regular enums without generics still work."""
        enum = IREnum(
            name="Status",
            variants=[
                IREnumVariant(name="Pending"),
                IREnumVariant(name="Completed"),
            ]
        )

        module = IRModule(name="test", version="1.0.0", enums=[enum])
        code = generate_rust(module)

        # Should NOT have generic parameters
        assert "pub enum Status {" in code
        assert "Status<" not in code

    def test_non_generic_function_still_works(self):
        """Test that regular functions without generics still work."""
        func = IRFunction(
            name="add",
            params=[
                IRParameter(name="a", param_type=IRType(name="int")),
                IRParameter(name="b", param_type=IRType(name="int")),
            ],
            return_type=IRType(name="int"),
            body=[]
        )

        module = IRModule(name="test", version="1.0.0", functions=[func])
        code = generate_rust(module)

        # Should NOT have generic parameters
        assert "pub fn add(" in code
        assert "add<" not in code

    def test_non_generic_struct_still_works(self):
        """Test that regular structs without generics still work."""
        cls = IRClass(
            name="Point",
            properties=[
                IRProperty(name="x", prop_type=IRType(name="int")),
                IRProperty(name="y", prop_type=IRType(name="int")),
            ]
        )

        module = IRModule(name="test", version="1.0.0", classes=[cls])
        code = generate_rust(module)

        # Should NOT have generic parameters
        assert "pub struct Point {" in code
        assert "Point<" not in code
        assert "impl Point {" in code


if __name__ == "__main__":
    # Run tests with pytest
    pytest.main([__file__, "-v", "--tb=short"])
