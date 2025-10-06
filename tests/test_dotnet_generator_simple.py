"""
Simple test runner for .NET Generator V2 (no pytest dependency)
"""

from dsl.ir import (
    BinaryOperator,
    IRAssignment,
    IRBinaryOp,
    IRClass,
    IREnum,
    IREnumVariant,
    IRFunction,
    IRIdentifier,
    IRIf,
    IRLiteral,
    IRModule,
    IRParameter,
    IRProperty,
    IRPropertyAccess,
    IRReturn,
    IRType,
    IRTypeDefinition,
    LiteralType,
)
from language.dotnet_generator_v2 import DotNetGeneratorV2, generate_csharp


def test_simple_class():
    """Test generating simple class."""
    print("Testing simple class generation...")

    cls = IRClass(
        name="user",
        properties=[
            IRProperty(name="id", prop_type=IRType(name="string")),
            IRProperty(name="name", prop_type=IRType(name="string")),
        ],
    )

    module = IRModule(name="test", classes=[cls])
    generator = DotNetGeneratorV2()
    code = generator.generate(module)

    assert "public class User" in code, "Class name not found"
    assert "public string Id { get; set; }" in code, "Id property not found"
    assert "public string Name { get; set; }" in code, "Name property not found"

    print("✅ Simple class test passed!")
    return True


def test_simple_method():
    """Test generating simple method."""
    print("Testing simple method generation...")

    method = IRFunction(
        name="greet",
        params=[IRParameter(name="name", param_type=IRType(name="string"))],
        return_type=IRType(name="string"),
        body=[
            IRReturn(
                value=IRBinaryOp(
                    op=BinaryOperator.ADD,
                    left=IRLiteral(value="Hello ", literal_type=LiteralType.STRING),
                    right=IRIdentifier(name="name"),
                )
            )
        ],
    )

    cls = IRClass(name="greeter", methods=[method])
    module = IRModule(name="test", classes=[cls])
    generator = DotNetGeneratorV2()
    code = generator.generate(module)

    assert "public string Greet(string name)" in code, "Method signature not found"
    assert "return" in code, "Return statement not found"

    print("✅ Simple method test passed!")
    return True


def test_enum_generation():
    """Test enum generation."""
    print("Testing enum generation...")

    enum = IREnum(
        name="status",
        variants=[
            IREnumVariant(name="pending"),
            IREnumVariant(name="completed"),
            IREnumVariant(name="failed"),
        ],
    )

    module = IRModule(name="test", enums=[enum])
    generator = DotNetGeneratorV2()
    code = generator.generate(module)

    assert "public enum Status" in code, "Enum name not found"
    assert "Pending," in code, "Pending variant not found"
    assert "Completed," in code, "Completed variant not found"

    print("✅ Enum test passed!")
    return True


def test_async_method():
    """Test async method generation."""
    print("Testing async method generation...")

    method = IRFunction(
        name="fetch_data",
        params=[IRParameter(name="id", param_type=IRType(name="string"))],
        return_type=IRType(name="string"),
        is_async=True,
        body=[
            IRReturn(
                value=IRPropertyAccess(
                    object=IRIdentifier(name="database"),
                    property="get_user",
                )
            )
        ],
    )

    cls = IRClass(name="repository", methods=[method])
    module = IRModule(name="test", classes=[cls])
    generator = DotNetGeneratorV2()
    code = generator.generate(module)

    assert "async Task<string> FetchData" in code, "Async method signature not found"

    print("✅ Async method test passed!")
    return True


def test_nullable_types():
    """Test nullable type generation."""
    print("Testing nullable types...")

    cls = IRClass(
        name="user",
        properties=[
            IRProperty(name="id", prop_type=IRType(name="string")),
            IRProperty(name="age", prop_type=IRType(name="int", is_optional=True)),
        ],
    )

    module = IRModule(name="test", classes=[cls])
    generator = DotNetGeneratorV2()
    code = generator.generate(module)

    assert "public string Id" in code, "Id property not found"
    assert "public int? Age" in code, "Nullable age property not found"

    print("✅ Nullable types test passed!")
    return True


def test_if_statement():
    """Test if statement generation."""
    print("Testing if statement generation...")

    if_stmt = IRIf(
        condition=IRBinaryOp(
            op=BinaryOperator.EQUAL,
            left=IRIdentifier(name="x"),
            right=IRLiteral(value=0, literal_type=LiteralType.INTEGER),
        ),
        then_body=[
            IRReturn(value=IRLiteral(value="zero", literal_type=LiteralType.STRING))
        ],
        else_body=[
            IRReturn(value=IRLiteral(value="non-zero", literal_type=LiteralType.STRING))
        ],
    )

    func = IRFunction(
        name="check",
        params=[IRParameter(name="x", param_type=IRType(name="int"))],
        return_type=IRType(name="string"),
        body=[if_stmt],
    )

    module = IRModule(name="test", functions=[func])
    generator = DotNetGeneratorV2()
    code = generator.generate(module)

    assert "if ((x == 0))" in code, "If condition not found"
    assert "else" in code, "Else clause not found"

    print("✅ If statement test passed!")
    return True


def test_type_definition():
    """Test type definition generation."""
    print("Testing type definition generation...")

    type_def = IRTypeDefinition(
        name="user",
        fields=[
            IRProperty(name="id", prop_type=IRType(name="string")),
            IRProperty(name="name", prop_type=IRType(name="string")),
        ],
    )

    module = IRModule(name="test", types=[type_def])
    generator = DotNetGeneratorV2()
    code = generator.generate(module)

    assert "public class User" in code, "Type class not found"
    assert "public string Id { get; set; }" in code, "Id property not found"

    print("✅ Type definition test passed!")
    return True


def test_naming_conventions():
    """Test naming convention conversions."""
    print("Testing naming conventions...")

    cls = IRClass(
        name="user_repository",
        properties=[
            IRProperty(name="user_id", prop_type=IRType(name="string")),
        ],
    )

    module = IRModule(name="test", classes=[cls])
    generator = DotNetGeneratorV2()
    code = generator.generate(module)

    assert "public class UserRepository" in code, "PascalCase class name not found"
    assert "public string UserId" in code, "PascalCase property name not found"

    print("✅ Naming conventions test passed!")
    return True


def test_public_api():
    """Test public API function."""
    print("Testing public API function...")

    module = IRModule(
        name="simple",
        classes=[
            IRClass(
                name="hello",
                methods=[
                    IRFunction(
                        name="world",
                        return_type=IRType(name="string"),
                        body=[
                            IRReturn(
                                value=IRLiteral(
                                    value="Hello, World!",
                                    literal_type=LiteralType.STRING,
                                )
                            )
                        ],
                    )
                ],
            )
        ],
    )

    code = generate_csharp(module, namespace="MyApp")

    assert "namespace MyApp" in code, "Custom namespace not found"
    assert "public class Hello" in code, "Class not found"

    print("✅ Public API test passed!")
    return True


def test_full_module():
    """Test generating a complete module."""
    print("Testing full module generation...")

    module = IRModule(
        name="user_service",
        types=[
            IRTypeDefinition(
                name="user",
                fields=[
                    IRProperty(name="id", prop_type=IRType(name="string")),
                    IRProperty(name="name", prop_type=IRType(name="string")),
                ],
            )
        ],
        enums=[
            IREnum(
                name="status",
                variants=[
                    IREnumVariant(name="active"),
                    IREnumVariant(name="inactive"),
                ],
            )
        ],
        classes=[
            IRClass(
                name="user_repository",
                methods=[
                    IRFunction(
                        name="get_user",
                        params=[IRParameter(name="id", param_type=IRType(name="string"))],
                        return_type=IRType(name="user"),
                        is_async=True,
                    )
                ],
            )
        ],
    )

    generator = DotNetGeneratorV2()
    code = generator.generate(module)

    assert "namespace UserService" in code, "Namespace not found"
    assert "public class User" in code, "User class not found"
    assert "public enum Status" in code, "Status enum not found"
    assert "public class UserRepository" in code, "UserRepository class not found"
    assert "async Task<User> GetUser" in code, "Async method not found"

    print("✅ Full module test passed!")
    return True


def run_all_tests():
    """Run all tests and report results."""
    print("=" * 60)
    print("Running .NET Generator V2 Tests")
    print("=" * 60)
    print()

    tests = [
        test_simple_class,
        test_simple_method,
        test_enum_generation,
        test_async_method,
        test_nullable_types,
        test_if_statement,
        test_type_definition,
        test_naming_conventions,
        test_public_api,
        test_full_module,
    ]

    passed = 0
    failed = 0

    for test in tests:
        try:
            if test():
                passed += 1
        except AssertionError as e:
            print(f"❌ {test.__name__} failed: {e}")
            failed += 1
        except Exception as e:
            print(f"❌ {test.__name__} error: {e}")
            failed += 1
        print()

    print("=" * 60)
    print(f"Test Results: {passed}/{len(tests)} passed")
    print("=" * 60)

    if failed == 0:
        print("🎉 All tests passed!")
        return True
    else:
        print(f"⚠️  {failed} test(s) failed")
        return False


if __name__ == "__main__":
    success = run_all_tests()
    exit(0 if success else 1)
