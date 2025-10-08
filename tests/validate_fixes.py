#!/usr/bin/env python3
"""
Quick validation script to verify all bug fixes.
"""

from language.python_parser_v2 import PythonParserV2
from language.nodejs_parser_v2 import NodeJSParserV2
from language.go_parser_v2 import GoParserV2
from language.rust_parser_v2 import RustParserV2
from language.dotnet_parser_v2 import DotNetParserV2

from language.python_generator_v2 import generate_python
from language.nodejs_generator_v2 import generate_nodejs
from language.go_generator_v2 import generate_go
from language.rust_generator_v2 import generate_rust
from language.dotnet_generator_v2 import generate_csharp

def test_rust_parser_api():
    """Test that Rust parser has parse_source() method."""
    print("Testing Rust parser API...")
    parser = RustParserV2()

    # Test parse_source method exists
    assert hasattr(parser, 'parse_source'), "Rust parser missing parse_source()"
    assert hasattr(parser, 'parse_file'), "Rust parser missing parse_file()"

    # Test parse_source works
    rust_code = """
    fn greet(name: &str) -> String {
        format!("Hello {}", name)
    }
    """
    module = parser.parse_source(rust_code, "test")
    assert module.name == "test"
    assert len(module.functions) == 1
    assert module.functions[0].name == "greet"

    print("✅ Rust parser API: PASSED")
    return True

def test_nodejs_class_methods():
    """Test that Node.js parser correctly detects class methods."""
    print("Testing Node.js class method detection...")
    parser = NodeJSParserV2()

    js_code = """
    class UserService {
      constructor(db) {
        this.db = db;
      }

      async getUser(id) {
        return await this.db.findUser(id);
      }

      deleteUser(id) {
        this.db.remove(id);
      }
    }
    """

    module = parser.parse_source(js_code, "test")

    # Should have 1 class, not standalone functions
    assert len(module.classes) == 1, f"Expected 1 class, got {len(module.classes)}"
    assert len(module.functions) == 0, f"Expected 0 standalone functions, got {len(module.functions)}"

    cls = module.classes[0]
    assert cls.name == "UserService"
    assert len(cls.methods) == 2, f"Expected 2 methods, got {len(cls.methods)}"

    method_names = [m.name for m in cls.methods]
    assert "getUser" in method_names
    assert "deleteUser" in method_names

    print("✅ Node.js class methods: PASSED")
    return True

def test_python_generator():
    """Test that Python generator doesn't produce <unknown> placeholders."""
    print("Testing Python generator...")

    from dsl.ir import IRModule, IRFunction, IRParameter, IRType, IRReturn, IRLiteral, LiteralType

    # Create simple IR
    module = IRModule(name="test", version="1.0.0")
    func = IRFunction(
        name="greet",
        params=[IRParameter(name="name", param_type=IRType(name="string"))],
        return_type=IRType(name="string"),
        body=[
            IRReturn(value=IRLiteral(literal_type=LiteralType.STRING, value="Hello"))
        ]
    )
    module.functions.append(func)

    # Generate Python code
    code = generate_python(module)

    # Check for unknown placeholders
    assert "<unknown" not in code, f"Generated code contains <unknown> placeholder:\n{code}"
    assert "def greet" in code
    assert 'return "Hello"' in code

    print("✅ Python generator: PASSED")
    return True

def test_all_parsers_have_parse_source():
    """Test that all parsers have consistent API."""
    print("Testing parser API consistency...")

    parsers = [
        ("Python", PythonParserV2()),
        ("Node.js", NodeJSParserV2()),
        ("Go", GoParserV2()),
        ("Rust", RustParserV2()),
        (".NET", DotNetParserV2()),
    ]

    for name, parser in parsers:
        assert hasattr(parser, 'parse_source'), f"{name} parser missing parse_source()"
        assert hasattr(parser, 'parse_file'), f"{name} parser missing parse_file()"
        print(f"  ✅ {name} parser has both parse_source() and parse_file()")

    print("✅ Parser API consistency: PASSED")
    return True

def main():
    print("=" * 60)
    print("VALIDATION: Bug Fixes")
    print("=" * 60)
    print()

    tests = [
        test_rust_parser_api,
        test_nodejs_class_methods,
        test_python_generator,
        test_all_parsers_have_parse_source,
    ]

    passed = 0
    failed = 0

    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"❌ {test.__name__}: FAILED - {e}")
            failed += 1
        print()

    print("=" * 60)
    print(f"RESULTS: {passed} passed, {failed} failed")
    print("=" * 60)

    if failed == 0:
        print("\n🎉 All bug fixes validated successfully!")
        return 0
    else:
        print(f"\n⚠️  {failed} test(s) failed")
        return 1

if __name__ == "__main__":
    exit(main())
