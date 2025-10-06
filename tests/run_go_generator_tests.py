#!/usr/bin/env python3
"""
Simple test runner for Go Generator V2 (no pytest dependency)
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import traceback
from dsl.ir import (
    IRModule,
    IRFunction,
    IRParameter,
    IRType,
    IRTypeDefinition,
    IRProperty,
    IRClass,
    IREnum,
    IREnumVariant,
    IRReturn,
    IRAssignment,
    IRIf,
    IRFor,
    IRWhile,
    IRTry,
    IRCatch,
    IRThrow,
    IRBreak,
    IRContinue,
    IRLiteral,
    IRIdentifier,
    IRBinaryOp,
    IRCall,
    IRPropertyAccess,
    IRArray,
    IRMap,
    BinaryOperator,
    LiteralType,
)
from language.go_generator_v2 import GoGeneratorV2, generate_go
from language.go_parser_v2 import GoParserV2


class TestRunner:
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.errors = []

    def run_test(self, test_name, test_func):
        """Run a single test function."""
        try:
            test_func()
            self.passed += 1
            print(f"✓ {test_name}")
        except AssertionError as e:
            self.failed += 1
            self.errors.append((test_name, str(e)))
            print(f"✗ {test_name}: {e}")
        except Exception as e:
            self.failed += 1
            self.errors.append((test_name, traceback.format_exc()))
            print(f"✗ {test_name}: {e}")

    def report(self):
        """Print final test report."""
        print("\n" + "="*60)
        print(f"Tests: {self.passed + self.failed}")
        print(f"Passed: {self.passed}")
        print(f"Failed: {self.failed}")
        print(f"Pass Rate: {self.passed / (self.passed + self.failed) * 100:.1f}%")

        if self.errors:
            print("\nFailed Tests:")
            for test_name, error in self.errors:
                print(f"\n{test_name}:")
                print(error)

        return self.failed == 0


# ============================================================================
# Test Implementations
# ============================================================================


def test_empty_module():
    """Test empty module generation."""
    module = IRModule(name="empty", version="1.0.0")
    code = generate_go(module)
    assert "package empty" in code
    assert code.endswith("\n"), "Code should end with newline"


def test_simple_function():
    """Test simple function with no params or return."""
    module = IRModule(name="test", version="1.0.0")
    func = IRFunction(name="hello", params=[], return_type=None, body=[])
    module.functions.append(func)

    code = generate_go(module)

    assert "package test" in code
    assert "func Hello() {" in code


def test_function_with_params():
    """Test function with parameters."""
    module = IRModule(name="test", version="1.0.0")

    params = [
        IRParameter(name="name", param_type=IRType(name="string")),
        IRParameter(name="age", param_type=IRType(name="int")),
    ]
    func = IRFunction(name="greet", params=params, return_type=None, body=[])
    module.functions.append(func)

    code = generate_go(module)

    assert "func Greet(name string, age int) {" in code


def test_function_with_return():
    """Test function with return type."""
    module = IRModule(name="test", version="1.0.0")

    func = IRFunction(
        name="get_message",
        params=[],
        return_type=IRType(name="string"),
        body=[],
    )
    module.functions.append(func)

    code = generate_go(module)

    # Function with no error handling should return just the type
    assert "func GetMessage() string {" in code


def test_function_with_body():
    """Test function with body statements."""
    module = IRModule(name="test", version="1.0.0")

    body = [
        IRReturn(
            value=IRLiteral(value="Hello, World!", literal_type=LiteralType.STRING)
        )
    ]
    func = IRFunction(
        name="greet",
        params=[],
        return_type=IRType(name="string"),
        body=body,
    )
    module.functions.append(func)

    code = generate_go(module)

    assert 'return "Hello, World!", nil' in code


def test_primitive_types():
    """Test primitive type mapping."""
    module = IRModule(name="test", version="1.0.0")

    params = [
        IRParameter(name="s", param_type=IRType(name="string")),
        IRParameter(name="i", param_type=IRType(name="int")),
        IRParameter(name="f", param_type=IRType(name="float")),
        IRParameter(name="b", param_type=IRType(name="bool")),
    ]
    func = IRFunction(name="test_types", params=params, body=[])
    module.functions.append(func)

    code = generate_go(module)

    assert "s string" in code
    assert "i int" in code
    assert "f float64" in code
    assert "b bool" in code


def test_array_type():
    """Test array/slice type mapping."""
    module = IRModule(name="test", version="1.0.0")

    param = IRParameter(
        name="items",
        param_type=IRType(name="array", generic_args=[IRType(name="string")]),
    )
    func = IRFunction(name="process", params=[param], body=[])
    module.functions.append(func)

    code = generate_go(module)

    assert "items []string" in code


def test_map_type():
    """Test map type mapping."""
    module = IRModule(name="test", version="1.0.0")

    param = IRParameter(
        name="data",
        param_type=IRType(
            name="map",
            generic_args=[IRType(name="string"), IRType(name="int")],
        ),
    )
    func = IRFunction(name="process", params=[param], body=[])
    module.functions.append(func)

    code = generate_go(module)

    assert "data map[string]int" in code


def test_optional_type():
    """Test optional type (pointer in Go)."""
    module = IRModule(name="test", version="1.0.0")

    param = IRParameter(
        name="user", param_type=IRType(name="User", is_optional=True)
    )
    func = IRFunction(name="process", params=[param], body=[])
    module.functions.append(func)

    code = generate_go(module)

    assert "user *User" in code


def test_struct_definition():
    """Test struct type definition."""
    module = IRModule(name="test", version="1.0.0")

    fields = [
        IRProperty(name="id", prop_type=IRType(name="string")),
        IRProperty(name="name", prop_type=IRType(name="string")),
        IRProperty(name="age", prop_type=IRType(name="int")),
    ]
    type_def = IRTypeDefinition(name="User", fields=fields)
    module.types.append(type_def)

    code = generate_go(module)

    assert "type User struct {" in code
    assert "Id string" in code
    assert "Name string" in code
    assert "Age int" in code


def test_enum_definition():
    """Test enum as constants."""
    module = IRModule(name="test", version="1.0.0")

    variants = [
        IREnumVariant(name="pending"),
        IREnumVariant(name="completed"),
        IREnumVariant(name="failed"),
    ]
    enum = IREnum(name="Status", variants=variants)
    module.enums.append(enum)

    code = generate_go(module)

    assert "type Status int" in code
    assert "const (" in code
    assert "StatusPending Status = iota" in code


def test_if_statement():
    """Test if statement."""
    module = IRModule(name="test", version="1.0.0")

    condition = IRBinaryOp(
        op=BinaryOperator.GREATER_THAN,
        left=IRIdentifier(name="x"),
        right=IRLiteral(value=0, literal_type=LiteralType.INTEGER),
    )
    then_body = [
        IRReturn(IRLiteral(value="positive", literal_type=LiteralType.STRING))
    ]
    else_body = [
        IRReturn(IRLiteral(value="negative", literal_type=LiteralType.STRING))
    ]

    body = [IRIf(condition=condition, then_body=then_body, else_body=else_body)]

    func = IRFunction(
        name="check",
        params=[IRParameter(name="x", param_type=IRType(name="int"))],
        return_type=IRType(name="string"),
        body=body,
    )
    module.functions.append(func)

    code = generate_go(module)

    assert "if (x > 0) {" in code
    assert "} else {" in code


def test_for_loop():
    """Test for loop (range)."""
    module = IRModule(name="test", version="1.0.0")

    loop_body = [
        IRCall(
            function=IRPropertyAccess(
                object=IRIdentifier(name="fmt"), property="Println"
            ),
            args=[IRIdentifier(name="item")],
        )
    ]

    body = [
        IRFor(
            iterator="item",
            iterable=IRIdentifier(name="items"),
            body=loop_body,
        )
    ]

    func = IRFunction(
        name="print_all",
        params=[
            IRParameter(
                name="items",
                param_type=IRType(
                    name="array", generic_args=[IRType(name="string")]
                ),
            )
        ],
        body=body,
    )
    module.functions.append(func)

    code = generate_go(module)

    assert "for _, item := range items {" in code


def test_literals():
    """Test literal values."""
    module = IRModule(name="test", version="1.0.0")

    body = [
        IRAssignment(
            target="s",
            value=IRLiteral(value="hello", literal_type=LiteralType.STRING),
            is_declaration=True,
        ),
        IRAssignment(
            target="i",
            value=IRLiteral(value=42, literal_type=LiteralType.INTEGER),
            is_declaration=True,
        ),
        IRAssignment(
            target="b",
            value=IRLiteral(value=True, literal_type=LiteralType.BOOLEAN),
            is_declaration=True,
        ),
        IRAssignment(
            target="n",
            value=IRLiteral(value=None, literal_type=LiteralType.NULL),
            is_declaration=True,
        ),
    ]

    func = IRFunction(name="test_literals", params=[], body=body)
    module.functions.append(func)

    code = generate_go(module)

    assert 's := "hello"' in code
    assert "i := 42" in code
    assert "b := true" in code
    assert "n := nil" in code


def test_binary_operations():
    """Test binary operations."""
    module = IRModule(name="test", version="1.0.0")

    body = [
        IRAssignment(
            target="sum",
            value=IRBinaryOp(
                op=BinaryOperator.ADD,
                left=IRLiteral(value=1, literal_type=LiteralType.INTEGER),
                right=IRLiteral(value=2, literal_type=LiteralType.INTEGER),
            ),
            is_declaration=True,
        ),
    ]

    func = IRFunction(name="test_ops", params=[], body=body)
    module.functions.append(func)

    code = generate_go(module)

    assert "sum := (1 + 2)" in code


def test_simple_class():
    """Test simple class with properties."""
    module = IRModule(name="test", version="1.0.0")

    properties = [
        IRProperty(name="id", prop_type=IRType(name="string")),
        IRProperty(name="name", prop_type=IRType(name="string")),
    ]

    cls = IRClass(name="User", properties=properties)
    module.classes.append(cls)

    code = generate_go(module)

    assert "type User struct {" in code
    assert "Id string" in code
    assert "Name string" in code


def test_async_function():
    """Test async function generates goroutine."""
    module = IRModule(name="test", version="1.0.0")

    body = [
        IRCall(
            function=IRPropertyAccess(
                object=IRIdentifier(name="fmt"), property="Println"
            ),
            args=[IRLiteral(value="async work", literal_type=LiteralType.STRING)],
        )
    ]

    func = IRFunction(name="background_task", params=[], body=body, is_async=True)
    module.functions.append(func)

    code = generate_go(module)

    assert "func BackgroundTask() {" in code
    assert "go func() {" in code


def test_round_trip():
    """Test simple function roundtrip."""
    original_code = """package example

func Greet(name string) string {
\treturn "Hello, " + name
}
"""

    # Parse to IR
    parser = GoParserV2()
    ir_module = parser.parse_source(original_code, "test.go")

    # Generate back to Go
    generator = GoGeneratorV2()
    generated_code = generator.generate(ir_module)

    # Check semantics preserved
    assert "package example" in generated_code
    assert "func Greet" in generated_code
    assert "name string" in generated_code


# ============================================================================
# Main Test Runner
# ============================================================================


def main():
    """Run all tests."""
    runner = TestRunner()

    print("Running Go Generator V2 Tests")
    print("="*60)

    # Basic constructs
    runner.run_test("test_empty_module", test_empty_module)
    runner.run_test("test_simple_function", test_simple_function)
    runner.run_test("test_function_with_params", test_function_with_params)
    runner.run_test("test_function_with_return", test_function_with_return)
    runner.run_test("test_function_with_body", test_function_with_body)

    # Type system
    runner.run_test("test_primitive_types", test_primitive_types)
    runner.run_test("test_array_type", test_array_type)
    runner.run_test("test_map_type", test_map_type)
    runner.run_test("test_optional_type", test_optional_type)
    runner.run_test("test_struct_definition", test_struct_definition)
    runner.run_test("test_enum_definition", test_enum_definition)

    # Control flow
    runner.run_test("test_if_statement", test_if_statement)
    runner.run_test("test_for_loop", test_for_loop)

    # Expressions
    runner.run_test("test_literals", test_literals)
    runner.run_test("test_binary_operations", test_binary_operations)

    # Classes
    runner.run_test("test_simple_class", test_simple_class)

    # Async
    runner.run_test("test_async_function", test_async_function)

    # Round-trip
    runner.run_test("test_round_trip", test_round_trip)

    # Report
    success = runner.report()

    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
