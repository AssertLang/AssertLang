#!/usr/bin/env python3
"""
Demo: Rust Parser V2 - Arbitrary Rust → IR

Demonstrates parsing real-world Rust code into Promptware IR.
"""

from language.rust_parser_v2 import parse_rust_code


def demo_simple_library():
    """Demo: Parse a simple Rust library."""
    print("\n" + "=" * 80)
    print("DEMO 1: Simple Rust Library")
    print("=" * 80 + "\n")

    source = """
    use std::collections::HashMap;

    /// User account structure
    pub struct User {
        pub id: u32,
        pub name: String,
        pub email: Option<String>,
        roles: Vec<String>,
    }

    pub enum UserStatus {
        Active,
        Suspended,
        Deleted,
    }

    impl User {
        /// Create a new user
        pub fn new(id: u32, name: String) -> User {
            User {
                id: id,
                name: name,
                email: None,
                roles: Vec::new(),
            }
        }

        /// Add a role to the user
        pub fn add_role(&mut self, role: String) {
            self.roles.push(role);
        }

        /// Check if user has a specific role
        pub fn has_role(&self, role: &str) -> bool {
            return self.roles.contains(&role.to_string());
        }
    }

    /// Validate an email address
    pub fn validate_email(email: &str) -> Result<bool, String> {
        if email.contains("@") {
            return Ok(true);
        } else {
            return Err(String::from("Invalid email"));
        }
    }
    """

    module = parse_rust_code(source, "users")

    print(f"Module: {module.name}")
    print(f"Version: {module.version}\n")

    print(f"Imports: {len(module.imports)}")
    for imp in module.imports:
        items = ', '.join(imp.items) if imp.items else imp.module
        print(f"  - {imp.module} ({items})")

    print(f"\nStructs: {len(module.types)}")
    for struct in module.types:
        print(f"  - {struct.name}")
        for field in struct.fields:
            visibility = "pub" if not field.is_private else "priv"
            print(f"      {visibility} {field.name}: {field.prop_type}")

    print(f"\nEnums: {len(module.enums)}")
    for enum in module.enums:
        print(f"  - {enum.name}")
        for variant in enum.variants:
            if variant.associated_types:
                types = ', '.join(str(t) for t in variant.associated_types)
                print(f"      {variant.name}({types})")
            else:
                print(f"      {variant.name}")

    print(f"\nClasses (Impls): {len(module.classes)}")
    for cls in module.classes:
        print(f"  - {cls.name}")
        for method in cls.methods:
            params = ', '.join(f"{p.name}: {p.param_type}" for p in method.params)
            ret = f" -> {method.return_type}" if method.return_type else ""
            print(f"      fn {method.name}({params}){ret}")

    print(f"\nFunctions: {len(module.functions)}")
    for func in module.functions:
        params = ', '.join(f"{p.name}: {p.param_type}" for p in func.params)
        ret = f" -> {func.return_type}" if func.return_type else ""
        async_marker = "async " if func.is_async else ""
        print(f"  - {async_marker}fn {func.name}({params}){ret}")


def demo_type_mapping():
    """Demo: Type mapping from Rust to IR."""
    print("\n" + "=" * 80)
    print("DEMO 2: Type Mapping - Rust → IR")
    print("=" * 80 + "\n")

    source = """
    pub fn process_data(
        id: u32,
        name: String,
        tags: Vec<String>,
        metadata: HashMap<String, i32>,
        optional_field: Option<f64>,
        result_field: Result<bool, String>,
        borrowed: &str,
    ) -> Vec<u8> {
        let data = Vec::new();
        return data;
    }
    """

    module = parse_rust_code(source, "types_demo")

    print("Function: process_data\n")
    print("Parameters:")
    func = module.functions[0]
    for param in func.params:
        ir_type = str(param.param_type)
        optional = " (optional)" if param.param_type.is_optional else ""
        error_type = f" [throws: {param.param_type.metadata.get('rust_error_type', 'N/A')}]" if 'rust_error_type' in param.param_type.metadata else ""
        print(f"  {param.name: <20} Rust → IR: {ir_type}{optional}{error_type}")

    print(f"\nReturn Type: {func.return_type}")
    print(f"\nOwnership Metadata:")
    ownership = func.metadata.get('rust_ownership', {})
    for param_name, ownership_type in ownership.items():
        print(f"  {param_name}: {ownership_type}")


def demo_trait_and_impl():
    """Demo: Trait and impl parsing."""
    print("\n" + "=" * 80)
    print("DEMO 3: Traits and Implementations")
    print("=" * 80 + "\n")

    source = """
    pub trait Authenticate {
        fn login(&self, password: String) -> Result<bool, String>;
        fn logout(&self);
    }

    pub trait Authorize {
        fn has_permission(&self, resource: &str) -> bool;
    }

    pub struct Admin {
        username: String,
    }

    impl Authenticate for Admin {
        fn login(&self, password: String) -> Result<bool, String> {
            return Ok(true);
        }

        fn logout(&self) {
            // Implementation
        }
    }

    impl Authorize for Admin {
        fn has_permission(&self, resource: &str) -> bool {
            return true;
        }
    }
    """

    module = parse_rust_code(source, "auth")

    print("Traits (as interfaces):")
    for cls in module.classes:
        if cls.metadata.get('rust_trait'):
            print(f"\n  trait {cls.name}:")
            for method in cls.methods:
                params = ', '.join(f"{p.name}: {p.param_type}" for p in method.params)
                ret = f" -> {method.return_type}" if method.return_type else ""
                print(f"      fn {method.name}({params}){ret};")

    print("\n\nImplementations:")
    for cls in module.classes:
        if not cls.metadata.get('rust_trait'):
            implements = f" implements {', '.join(cls.base_classes)}" if cls.base_classes else ""
            print(f"\n  struct {cls.name}{implements}:")
            for method in cls.methods:
                params = ', '.join(f"{p.name}: {p.param_type}" for p in method.params)
                ret = f" -> {method.return_type}" if method.return_type else ""
                print(f"      fn {method.name}({params}){ret}")


def demo_real_world_adapter():
    """Demo: Parse a real Rust adapter file."""
    print("\n" + "=" * 80)
    print("DEMO 4: Real-World Rust Adapter")
    print("=" * 80 + "\n")

    # Read actual adapter file
    adapter_path = "/Users/hustlermain/HUSTLER_CONTENT/HSTLR/DEV/Promptware/tools/storage/adapters/adapter_rust.rs"

    try:
        with open(adapter_path, 'r') as f:
            source = f.read()

        from language.rust_parser_v2 import RustParserV2
        parser = RustParserV2()
        module = parser.parse_file(adapter_path)

        print(f"Module: {module.name}")
        print(f"\nImports: {len(module.imports)}")
        for imp in module.imports:
            items = ', '.join(imp.items) if imp.items else imp.module
            print(f"  use {imp.module}::{{{items}}}")

        print(f"\nFunctions: {len(module.functions)}")
        for func in module.functions:
            params = ', '.join(f"{p.name}: {p.param_type}" for p in func.params)
            ret = f" -> {func.return_type}" if func.return_type else ""
            visibility = "pub " if not func.is_private else ""
            print(f"  {visibility}fn {func.name}({params}){ret}")
            if func.body:
                print(f"      ({len(func.body)} statements in body)")

    except FileNotFoundError:
        print(f"Adapter file not found at {adapter_path}")
        print("Skipping demo...")


def main():
    """Run all demos."""
    print("\n" + "=" * 80)
    print("Rust Parser V2 - Comprehensive Demo")
    print("=" * 80)

    demo_simple_library()
    demo_type_mapping()
    demo_trait_and_impl()
    demo_real_world_adapter()

    print("\n" + "=" * 80)
    print("Demo Complete!")
    print("=" * 80 + "\n")


if __name__ == '__main__':
    main()
