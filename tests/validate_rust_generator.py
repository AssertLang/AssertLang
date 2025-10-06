"""
Quick validation script for Rust Generator V2
Runs without pytest dependency
"""

import sys
sys.path.insert(0, '/Users/hustlermain/HUSTLER_CONTENT/HSTLR/DEV/Promptware')

from language.rust_generator_v2 import generate_rust
from dsl.ir import (
    IRModule,
    IRFunction,
    IRParameter,
    IRType,
    IRReturn,
    IRLiteral,
    IRIdentifier,
    IRBinaryOp,
    IRTypeDefinition,
    IRProperty,
    IREnum,
    IREnumVariant,
    IRClass,
    BinaryOperator,
    LiteralType,
)


def test_simple_function():
    """Test 1: Simple function generation."""
    print("Test 1: Simple function...")

    func = IRFunction(
        name="greet",
        params=[IRParameter(name="name", param_type=IRType(name="string"))],
        return_type=IRType(name="string"),
        body=[
            IRReturn(
                value=IRLiteral(value="Hello", literal_type=LiteralType.STRING)
            )
        ]
    )

    module = IRModule(name="test", version="1.0.0", functions=[func])
    code = generate_rust(module)

    assert "pub fn greet" in code
    assert "-> String" in code
    assert "return" in code
    print("✓ PASS")
    return code


def test_struct():
    """Test 2: Struct generation."""
    print("\nTest 2: Struct generation...")

    struct = IRTypeDefinition(
        name="User",
        fields=[
            IRProperty(name="id", prop_type=IRType(name="string")),
            IRProperty(name="name", prop_type=IRType(name="string")),
            IRProperty(name="age", prop_type=IRType(name="int")),
        ]
    )

    module = IRModule(name="test", version="1.0.0", types=[struct])
    code = generate_rust(module)

    assert "#[derive(Debug, Clone)]" in code
    assert "pub struct User {" in code
    assert "pub id: String," in code
    assert "pub age: i32," in code
    print("✓ PASS")
    return code


def test_enum():
    """Test 3: Enum generation."""
    print("\nTest 3: Enum generation...")

    enum = IREnum(
        name="Status",
        variants=[
            IREnumVariant(name="Pending"),
            IREnumVariant(name="Completed"),
            IREnumVariant(name="Failed"),
        ]
    )

    module = IRModule(name="test", version="1.0.0", enums=[enum])
    code = generate_rust(module)

    assert "#[derive(Debug, Clone, PartialEq)]" in code
    assert "pub enum Status {" in code
    assert "Pending," in code
    assert "Completed," in code
    print("✓ PASS")
    return code


def test_optional_type():
    """Test 4: Optional type (T?) → Option<T>."""
    print("\nTest 4: Optional type...")

    func = IRFunction(
        name="find_user",
        params=[IRParameter(name="id", param_type=IRType(name="string"))],
        return_type=IRType(name="string", is_optional=True),
        body=[IRReturn(value=IRLiteral(value=None, literal_type=LiteralType.NULL))]
    )

    module = IRModule(name="test", version="1.0.0", functions=[func])
    code = generate_rust(module)

    assert "Option<String>" in code
    print("✓ PASS")
    return code


def test_result_type():
    """Test 5: Function with throws → Result<T, E>."""
    print("\nTest 5: Result type...")

    func = IRFunction(
        name="risky_operation",
        params=[IRParameter(name="value", param_type=IRType(name="int"))],
        return_type=IRType(name="string"),
        throws=["Box<dyn Error>"],
        body=[
            IRReturn(
                value=IRLiteral(value="success", literal_type=LiteralType.STRING)
            )
        ]
    )

    module = IRModule(name="test", version="1.0.0", functions=[func])
    code = generate_rust(module)

    assert "Result<String, Box<dyn Error>>" in code
    assert "use std::error::Error;" in code
    print("✓ PASS")
    return code


def test_hashmap_import():
    """Test 6: HashMap import detection."""
    print("\nTest 6: HashMap import...")

    func = IRFunction(
        name="process_map",
        params=[
            IRParameter(
                name="data",
                param_type=IRType(
                    name="map",
                    generic_args=[
                        IRType(name="string"),
                        IRType(name="int")
                    ]
                )
            )
        ],
        return_type=IRType(name="int"),
        body=[IRReturn(value=IRLiteral(value=0, literal_type=LiteralType.INTEGER))]
    )

    module = IRModule(name="test", version="1.0.0", functions=[func])
    code = generate_rust(module)

    assert "HashMap<String, i32>" in code
    assert "use std::collections::HashMap;" in code
    print("✓ PASS")
    return code


def test_async_function():
    """Test 7: Async function."""
    print("\nTest 7: Async function...")

    func = IRFunction(
        name="fetch_data",
        params=[IRParameter(name="url", param_type=IRType(name="string"))],
        return_type=IRType(name="string"),
        is_async=True,
        body=[
            IRReturn(
                value=IRLiteral(value="data", literal_type=LiteralType.STRING)
            )
        ]
    )

    module = IRModule(name="test", version="1.0.0", functions=[func])
    code = generate_rust(module)

    assert "pub async fn fetch_data" in code
    print("✓ PASS")
    return code


def test_binary_operations():
    """Test 8: Binary operations."""
    print("\nTest 8: Binary operations...")

    func = IRFunction(
        name="add",
        params=[
            IRParameter(name="a", param_type=IRType(name="int")),
            IRParameter(name="b", param_type=IRType(name="int")),
        ],
        return_type=IRType(name="int"),
        body=[
            IRReturn(
                value=IRBinaryOp(
                    op=BinaryOperator.ADD,
                    left=IRIdentifier(name="a"),
                    right=IRIdentifier(name="b")
                )
            )
        ]
    )

    module = IRModule(name="test", version="1.0.0", functions=[func])
    code = generate_rust(module)

    assert "a + b" in code or "(a + b)" in code
    print("✓ PASS")
    return code


def test_impl_block():
    """Test 9: Impl block with methods."""
    print("\nTest 9: Impl block...")

    cls = IRClass(
        name="Calculator",
        methods=[
            IRFunction(
                name="add",
                params=[
                    IRParameter(name="a", param_type=IRType(name="int")),
                    IRParameter(name="b", param_type=IRType(name="int")),
                ],
                return_type=IRType(name="int"),
                body=[
                    IRReturn(
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

    module = IRModule(name="test", version="1.0.0", classes=[cls])
    code = generate_rust(module)

    assert "impl Calculator {" in code
    assert "pub fn add" in code
    print("✓ PASS")
    return code


def test_enum_with_data():
    """Test 10: Enum with associated data."""
    print("\nTest 10: Enum with associated data...")

    enum = IREnum(
        name="Message",
        variants=[
            IREnumVariant(name="Text", associated_types=[IRType(name="string")]),
            IREnumVariant(
                name="Image",
                associated_types=[
                    IRType(name="string"),
                    IRType(name="int")
                ]
            ),
            IREnumVariant(name="Disconnect"),
        ]
    )

    module = IRModule(name="test", version="1.0.0", enums=[enum])
    code = generate_rust(module)

    assert "Text(String)," in code
    assert "Image(String, i32)," in code
    assert "Disconnect," in code
    print("✓ PASS")
    return code


def main():
    """Run all tests."""
    print("=" * 60)
    print("Rust Generator V2 - Validation Tests")
    print("=" * 60)

    tests = [
        test_simple_function,
        test_struct,
        test_enum,
        test_optional_type,
        test_result_type,
        test_hashmap_import,
        test_async_function,
        test_binary_operations,
        test_impl_block,
        test_enum_with_data,
    ]

    passed = 0
    failed = 0

    for test in tests:
        try:
            test()
            passed += 1
        except Exception as e:
            print(f"✗ FAIL: {e}")
            failed += 1

    print("\n" + "=" * 60)
    print(f"Results: {passed}/{len(tests)} tests passed")
    if failed > 0:
        print(f"         {failed} tests failed")
    print("=" * 60)

    # Show sample output
    print("\n" + "=" * 60)
    print("Sample Generated Code (Test 1):")
    print("=" * 60)
    code = test_simple_function()
    print(code)

    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
