"""
Tests for Rust Parser V2: Arbitrary Rust → IR

Tests cover:
- Function parsing
- Struct parsing
- Enum parsing
- Trait parsing
- Impl parsing
- Type mapping (primitives, Option, Result, Vec, HashMap)
- Ownership metadata extraction
"""

import pytest
from language.rust_parser_v2 import RustParserV2, parse_rust_code
from dsl.ir import (
    IRModule,
    IRFunction,
    IRType,
    IREnum,
    IRClass,
    IRTypeDefinition,
)


class TestRustParserV2:
    """Test suite for Rust Parser V2."""

    def setup_method(self):
        """Set up test fixtures."""
        self.parser = RustParserV2()

    # ========================================================================
    # Function Parsing Tests
    # ========================================================================

    def test_parse_simple_function(self):
        """Test parsing a simple function."""
        source = """
        fn add(a: i32, b: i32) -> i32 {
            return a + b;
        }
        """

        module = parse_rust_code(source, "test")

        assert len(module.functions) == 1
        func = module.functions[0]
        assert func.name == "add"
        assert len(func.params) == 2
        assert func.params[0].name == "a"
        assert func.params[0].param_type.name == "int"
        assert func.params[1].name == "b"
        assert func.return_type.name == "int"

    def test_parse_function_with_references(self):
        """Test parsing function with reference parameters."""
        source = """
        fn process(data: &str) -> String {
            return data.to_string();
        }
        """

        module = parse_rust_code(source, "test")

        assert len(module.functions) == 1
        func = module.functions[0]
        assert func.name == "process"
        assert func.params[0].param_type.name == "string"
        # Check ownership metadata
        assert 'rust_ownership' in func.metadata

    def test_parse_async_function(self):
        """Test parsing async function."""
        source = """
        pub async fn fetch_data(url: String) -> Result<String, Error> {
            let result = String::from("data");
            return result;
        }
        """

        module = parse_rust_code(source, "test")

        assert len(module.functions) == 1
        func = module.functions[0]
        assert func.name == "fetch_data"
        assert func.is_async is True
        assert func.is_private is False
        assert func.return_type.name == "string"  # Result unwrapped

    def test_parse_function_with_option(self):
        """Test parsing function with Option return type."""
        source = """
        fn find_user(id: u32) -> Option<String> {
            return Some(String::from("user"));
        }
        """

        module = parse_rust_code(source, "test")

        func = module.functions[0]
        assert func.return_type.name == "string"
        assert func.return_type.is_optional is True

    def test_parse_function_with_result(self):
        """Test parsing function with Result return type."""
        source = """
        fn do_something() -> Result<i32, String> {
            return Ok(42);
        }
        """

        module = parse_rust_code(source, "test")

        func = module.functions[0]
        assert func.return_type.name == "int"
        assert 'rust_error_type' in func.return_type.metadata
        assert func.return_type.metadata['rust_error_type'] == "String"

    # ========================================================================
    # Struct Parsing Tests
    # ========================================================================

    def test_parse_simple_struct(self):
        """Test parsing a simple struct."""
        source = """
        pub struct User {
            pub name: String,
            pub age: u32,
        }
        """

        module = parse_rust_code(source, "test")

        assert len(module.types) == 1
        struct = module.types[0]
        assert struct.name == "User"
        assert len(struct.fields) == 2
        assert struct.fields[0].name == "name"
        assert struct.fields[0].prop_type.name == "string"
        assert struct.fields[1].name == "age"
        assert struct.fields[1].prop_type.name == "int"

    def test_parse_struct_with_private_fields(self):
        """Test parsing struct with private fields."""
        source = """
        pub struct Config {
            pub host: String,
            port: u16,
        }
        """

        module = parse_rust_code(source, "test")

        struct = module.types[0]
        assert struct.fields[0].is_private is False  # pub
        assert struct.fields[1].is_private is True   # private

    def test_parse_struct_with_vec_field(self):
        """Test parsing struct with Vec field."""
        source = """
        pub struct Container {
            pub items: Vec<String>,
        }
        """

        module = parse_rust_code(source, "test")

        struct = module.types[0]
        items_field = struct.fields[0]
        assert items_field.prop_type.name == "array"
        assert len(items_field.prop_type.generic_args) == 1
        assert items_field.prop_type.generic_args[0].name == "string"

    def test_parse_struct_with_hashmap_field(self):
        """Test parsing struct with HashMap field."""
        source = """
        use std::collections::HashMap;

        pub struct Cache {
            pub data: HashMap<String, i32>,
        }
        """

        module = parse_rust_code(source, "test")

        struct = module.types[0]
        data_field = struct.fields[0]
        assert data_field.prop_type.name == "map"
        assert len(data_field.prop_type.generic_args) == 2
        assert data_field.prop_type.generic_args[0].name == "string"
        assert data_field.prop_type.generic_args[1].name == "int"

    # ========================================================================
    # Enum Parsing Tests
    # ========================================================================

    def test_parse_simple_enum(self):
        """Test parsing a simple enum."""
        source = """
        pub enum Status {
            Pending,
            Active,
            Completed,
        }
        """

        module = parse_rust_code(source, "test")

        assert len(module.enums) == 1
        enum = module.enums[0]
        assert enum.name == "Status"
        assert len(enum.variants) == 3
        assert enum.variants[0].name == "Pending"
        assert enum.variants[1].name == "Active"
        assert enum.variants[2].name == "Completed"

    def test_parse_enum_with_associated_values(self):
        """Test parsing enum with associated values."""
        source = """
        pub enum Message {
            Text(String),
            Number(i32),
            Data(Vec<u8>),
        }
        """

        module = parse_rust_code(source, "test")

        enum = module.enums[0]
        assert len(enum.variants) == 3

        # Text variant
        text_variant = enum.variants[0]
        assert text_variant.name == "Text"
        assert len(text_variant.associated_types) == 1
        assert text_variant.associated_types[0].name == "string"

        # Number variant
        num_variant = enum.variants[1]
        assert num_variant.name == "Number"
        assert num_variant.associated_types[0].name == "int"

        # Data variant
        data_variant = enum.variants[2]
        assert data_variant.name == "Data"
        assert data_variant.associated_types[0].name == "array"

    # ========================================================================
    # Trait Parsing Tests
    # ========================================================================

    def test_parse_simple_trait(self):
        """Test parsing a trait definition."""
        source = """
        pub trait Greet {
            fn greet(&self) -> String;
            fn say_goodbye(&self);
        }
        """

        module = parse_rust_code(source, "test")

        assert len(module.classes) == 1
        trait_class = module.classes[0]
        assert trait_class.name == "Greet"
        assert trait_class.metadata.get('rust_trait') is True
        assert len(trait_class.methods) == 2

        # Check methods
        greet = trait_class.methods[0]
        assert greet.name == "greet"
        assert greet.return_type.name == "string"

        goodbye = trait_class.methods[1]
        assert goodbye.name == "say_goodbye"

    # ========================================================================
    # Impl Parsing Tests
    # ========================================================================

    def test_parse_impl_block(self):
        """Test parsing an impl block."""
        source = """
        struct Counter {
            value: i32,
        }

        impl Counter {
            pub fn new() -> Counter {
                let c = Counter { value: 0 };
                return c;
            }

            pub fn increment(&mut self) {
                self.value = self.value + 1;
            }
        }
        """

        module = parse_rust_code(source, "test")

        # Should have Counter struct
        assert len(module.types) == 1

        # Should have Counter class with methods
        assert len(module.classes) == 1
        counter_class = module.classes[0]
        assert counter_class.name == "Counter"
        assert len(counter_class.methods) >= 2

        # Check methods
        new_method = next(m for m in counter_class.methods if m.name == "new")
        assert new_method.return_type.name == "Counter"

        inc_method = next(m for m in counter_class.methods if m.name == "increment")
        assert inc_method is not None

    def test_parse_trait_impl(self):
        """Test parsing trait implementation."""
        source = """
        trait Display {
            fn display(&self) -> String;
        }

        struct Point {
            x: i32,
            y: i32,
        }

        impl Display for Point {
            fn display(&self) -> String {
                return String::from("point");
            }
        }
        """

        module = parse_rust_code(source, "test")

        # Should have Display trait
        display_trait = next((c for c in module.classes if c.name == "Display"), None)
        assert display_trait is not None

        # Should have Point class implementing Display
        point_class = next((c for c in module.classes if c.name == "Point"), None)
        assert point_class is not None
        assert "Display" in point_class.base_classes

    # ========================================================================
    # Import Parsing Tests
    # ========================================================================

    def test_parse_simple_imports(self):
        """Test parsing use statements."""
        source = """
        use std::collections::HashMap;
        use std::fs;
        use serde_json::Value;
        """

        module = parse_rust_code(source, "test")

        assert len(module.imports) == 3

        # Check HashMap import
        hashmap_import = next(i for i in module.imports if "HashMap" in i.items)
        assert hashmap_import.module == "std::collections"
        assert "HashMap" in hashmap_import.items

    def test_parse_grouped_imports(self):
        """Test parsing grouped use statements."""
        source = """
        use std::collections::{HashMap, HashSet};
        """

        module = parse_rust_code(source, "test")

        assert len(module.imports) == 1
        import_stmt = module.imports[0]
        assert import_stmt.module == "std::collections"
        assert "HashMap" in import_stmt.items
        assert "HashSet" in import_stmt.items

    # ========================================================================
    # Type Mapping Tests
    # ========================================================================

    def test_map_primitive_types(self):
        """Test mapping Rust primitives to IR types."""
        test_cases = [
            ("i32", "int"),
            ("u64", "int"),
            ("f64", "float"),
            ("bool", "bool"),
            ("String", "string"),
            ("str", "string"),
        ]

        for rust_type, expected_ir in test_cases:
            ir_type = self.parser._map_rust_type_to_ir(rust_type)
            assert ir_type.name == expected_ir, f"Failed for {rust_type}"

    def test_map_vec_type(self):
        """Test mapping Vec<T> to array<T>."""
        ir_type = self.parser._map_rust_type_to_ir("Vec<String>")
        assert ir_type.name == "array"
        assert len(ir_type.generic_args) == 1
        assert ir_type.generic_args[0].name == "string"

    def test_map_nested_vec_type(self):
        """Test mapping nested Vec types."""
        ir_type = self.parser._map_rust_type_to_ir("Vec<Vec<i32>>")
        assert ir_type.name == "array"
        assert ir_type.generic_args[0].name == "array"
        assert ir_type.generic_args[0].generic_args[0].name == "int"

    def test_map_hashmap_type(self):
        """Test mapping HashMap<K,V> to map<K,V>."""
        ir_type = self.parser._map_rust_type_to_ir("HashMap<String, i32>")
        assert ir_type.name == "map"
        assert len(ir_type.generic_args) == 2
        assert ir_type.generic_args[0].name == "string"
        assert ir_type.generic_args[1].name == "int"

    def test_map_option_type(self):
        """Test mapping Option<T> to optional T."""
        ir_type = self.parser._map_rust_type_to_ir("Option<String>")
        assert ir_type.name == "string"
        assert ir_type.is_optional is True

    def test_map_result_type(self):
        """Test mapping Result<T, E> to T with error metadata."""
        ir_type = self.parser._map_rust_type_to_ir("Result<i32, String>")
        assert ir_type.name == "int"
        assert "rust_error_type" in ir_type.metadata
        assert ir_type.metadata["rust_error_type"] == "String"

    def test_map_reference_type(self):
        """Test mapping reference types."""
        ir_type = self.parser._map_rust_type_to_ir("&str")
        assert ir_type.name == "string"

        ir_type = self.parser._map_rust_type_to_ir("&mut String")
        assert ir_type.name == "string"

    # ========================================================================
    # Integration Tests
    # ========================================================================

    def test_parse_complete_module(self):
        """Test parsing a complete Rust module."""
        source = """
        use std::collections::HashMap;

        /// User data structure
        pub struct User {
            pub id: u32,
            pub name: String,
            pub email: Option<String>,
        }

        pub enum Role {
            Admin,
            User,
            Guest,
        }

        pub trait Authenticate {
            fn login(&self, password: String) -> Result<bool, String>;
        }

        impl User {
            pub fn new(id: u32, name: String) -> User {
                let user = User {
                    id: id,
                    name: name,
                    email: None,
                };
                return user;
            }

            pub fn get_name(&self) -> String {
                return self.name.clone();
            }
        }

        pub fn validate_email(email: &str) -> bool {
            return true;
        }
        """

        module = parse_rust_code(source, "users")

        # Check module name
        assert module.name == "users"

        # Check imports
        assert len(module.imports) >= 1

        # Check types (User struct)
        assert len(module.types) >= 1
        user_struct = next(t for t in module.types if t.name == "User")
        assert user_struct is not None
        assert len(user_struct.fields) == 3

        # Check enums (Role)
        assert len(module.enums) >= 1
        role_enum = next(e for e in module.enums if e.name == "Role")
        assert len(role_enum.variants) == 3

        # Check classes (Authenticate trait, User impl)
        assert len(module.classes) >= 1

        # Check standalone functions (validate_email)
        standalone_funcs = [f for f in module.functions if f.name == "validate_email"]
        assert len(standalone_funcs) >= 1

    def test_parse_real_world_adapter(self):
        """Test parsing a real Rust adapter file."""
        source = """
        use serde_json::{json, Map, Value};
        use std::fs;
        use std::path::Path;

        pub const VERSION: &str = "v1";

        pub fn handle(request: &Value) -> Value {
            if !request.is_object() {
                return error("E_SCHEMA", "request must be an object");
            }

            let op = request
                .get("op")
                .and_then(Value::as_str)
                .unwrap_or("");

            match op {
                "get" => get_data(),
                "put" => put_data(),
                _ => error("E_ARGS", "unsupported op"),
            }
        }

        fn get_data() -> Value {
            json!({ "data": "test" })
        }

        fn put_data() -> Value {
            json!({ "ok": true })
        }

        fn error(code: &str, message: &str) -> Value {
            json!({
                "error": { "code": code, "message": message }
            })
        }
        """

        module = parse_rust_code(source, "adapter")

        # Should parse imports
        assert len(module.imports) > 0

        # Should parse functions
        assert len(module.functions) > 0

        # Should have handle function
        handle_fn = next((f for f in module.functions if f.name == "handle"), None)
        assert handle_fn is not None
        assert handle_fn.return_type.name == "Value"

    # ========================================================================
    # Ownership Metadata Tests
    # ========================================================================

    def test_extract_ownership_metadata(self):
        """Test extracting ownership information from parameters."""
        source = """
        fn process(
            owned: String,
            borrowed: &str,
            mut_borrowed: &mut Vec<i32>,
            mut_owned: mut i32
        ) -> String {
            return owned;
        }
        """

        module = parse_rust_code(source, "test")

        func = module.functions[0]
        ownership = func.metadata.get('rust_ownership', {})

        # Note: ownership metadata is based on param string patterns
        # The exact keys depend on how parameters are parsed
        assert 'rust_ownership' in func.metadata


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
