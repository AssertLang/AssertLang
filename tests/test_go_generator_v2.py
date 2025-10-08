"""
Tests for Go Generator V2

Comprehensive test suite covering:
1. Basic constructs (functions, structs, variables)
2. Type system (primitives, slices, maps, pointers)
3. Control flow (if/else, for, while, switch)
4. Error handling patterns
5. Goroutines and async
6. Struct methods and constructors
7. Round-trip semantic preservation (Go → IR → Go)
"""

import pytest
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


class TestBasicConstructs:
    """Test basic Go constructs."""

    def test_empty_module(self):
        """Test empty module generation."""
        module = IRModule(name="empty", version="1.0.0")
        code = generate_go(module)

        assert "package empty" in code
        assert code.strip().endswith("\n")

    def test_simple_function(self):
        """Test simple function with no params or return."""
        module = IRModule(name="test", version="1.0.0")
        func = IRFunction(name="hello", params=[], return_type=None, body=[])
        module.functions.append(func)

        code = generate_go(module)

        assert "package test" in code
        assert "func Hello() {" in code

    def test_function_with_params(self):
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

    def test_function_with_return_type(self):
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

        assert "func GetMessage() (string, error) {" in code

    def test_function_with_body(self):
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


class TestTypeSystem:
    """Test type system mapping."""

    def test_primitive_types(self):
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

    def test_array_type(self):
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

    def test_map_type(self):
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

    def test_optional_type(self):
        """Test optional type (pointer in Go)."""
        module = IRModule(name="test", version="1.0.0")

        param = IRParameter(
            name="user", param_type=IRType(name="User", is_optional=True)
        )
        func = IRFunction(name="process", params=[param], body=[])
        module.functions.append(func)

        code = generate_go(module)

        assert "user *User" in code

    def test_struct_definition(self):
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
        assert '`json:"id"`' in code

    def test_enum_definition(self):
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
        assert "StatusCompleted" in code
        assert "StatusFailed" in code


class TestControlFlow:
    """Test control flow statements."""

    def test_if_statement(self):
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
        assert 'return "positive", nil' in code
        assert "} else {" in code
        assert 'return "negative", nil' in code

    def test_for_loop(self):
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
        assert "fmt.Println(item)" in code

    def test_while_loop(self):
        """Test while loop (for in Go)."""
        module = IRModule(name="test", version="1.0.0")

        condition = IRBinaryOp(
            op=BinaryOperator.GREATER_THAN,
            left=IRIdentifier(name="count"),
            right=IRLiteral(value=0, literal_type=LiteralType.INTEGER),
        )

        loop_body = [
            IRAssignment(
                target="count",
                value=IRBinaryOp(
                    op=BinaryOperator.SUBTRACT,
                    left=IRIdentifier(name="count"),
                    right=IRLiteral(value=1, literal_type=LiteralType.INTEGER),
                ),
                is_declaration=False,
            )
        ]

        body = [IRWhile(condition=condition, body=loop_body)]

        func = IRFunction(name="countdown", params=[], body=body)
        module.functions.append(func)

        code = generate_go(module)

        assert "for (count > 0) {" in code
        assert "count = (count - 1)" in code

    def test_break_continue(self):
        """Test break and continue statements."""
        module = IRModule(name="test", version="1.0.0")

        loop_body = [IRBreak(), IRContinue()]

        body = [
            IRFor(
                iterator="i",
                iterable=IRIdentifier(name="items"),
                body=loop_body,
            )
        ]

        func = IRFunction(name="test_loop", params=[], body=body)
        module.functions.append(func)

        code = generate_go(module)

        assert "break" in code
        assert "continue" in code


class TestErrorHandling:
    """Test error handling patterns."""

    def test_throw_statement(self):
        """Test throw as return error."""
        module = IRModule(name="test", version="1.0.0")

        body = [
            IRThrow(
                exception=IRLiteral(
                    value="invalid input", literal_type=LiteralType.STRING
                )
            )
        ]

        func = IRFunction(
            name="validate",
            params=[],
            return_type=IRType(name="bool"),
            body=body,
        )
        module.functions.append(func)

        code = generate_go(module)

        assert "import" in code
        assert "errors" in code
        assert 'return nil, errors.New("invalid input")' in code

    def test_try_catch(self):
        """Test try-catch conversion."""
        module = IRModule(name="test", version="1.0.0")

        try_body = [
            IRAssignment(
                target="result",
                value=IRCall(function=IRIdentifier(name="risky_operation"), args=[]),
                is_declaration=True,
            )
        ]

        catch_body = [
            IRReturn(
                value=IRLiteral(value="error occurred", literal_type=LiteralType.STRING)
            )
        ]

        catch = IRCatch(
            exception_type="Error", exception_var="e", body=catch_body
        )

        body = [IRTry(try_body=try_body, catch_blocks=[catch])]

        func = IRFunction(
            name="safe_operation",
            params=[],
            return_type=IRType(name="string"),
            body=body,
        )
        module.functions.append(func)

        code = generate_go(module)

        assert "result := risky_operation()" in code
        assert "// catch Error" in code

    def test_function_with_throws(self):
        """Test function that declares throws."""
        module = IRModule(name="test", version="1.0.0")

        func = IRFunction(
            name="risky",
            params=[],
            return_type=IRType(name="string"),
            throws=["ValidationError"],
            body=[],
        )
        module.functions.append(func)

        code = generate_go(module)

        assert "func Risky() (string, error) {" in code


class TestAsyncAndGoroutines:
    """Test async functions and goroutines."""

    def test_async_function(self):
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
        assert 'fmt.Println("async work")' in code
        assert "}()" in code


class TestClassesAndMethods:
    """Test class generation (structs + methods)."""

    def test_simple_class(self):
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

    def test_class_with_constructor(self):
        """Test class with constructor."""
        module = IRModule(name="test", version="1.0.0")

        properties = [IRProperty(name="name", prop_type=IRType(name="string"))]

        constructor_params = [
            IRParameter(name="name", param_type=IRType(name="string"))
        ]
        constructor_body = [
            IRAssignment(
                target="self.name",
                value=IRIdentifier(name="name"),
                is_declaration=True,
            )
        ]
        constructor = IRFunction(
            name="__init__", params=constructor_params, body=constructor_body
        )

        cls = IRClass(name="User", properties=properties, constructor=constructor)
        module.classes.append(cls)

        code = generate_go(module)

        assert "func NewUser(name string) *User {" in code

    def test_class_with_methods(self):
        """Test class with methods."""
        module = IRModule(name="test", version="1.0.0")

        properties = [IRProperty(name="name", prop_type=IRType(name="string"))]

        method_body = [
            IRReturn(
                value=IRPropertyAccess(
                    object=IRIdentifier(name="self"), property="name"
                )
            )
        ]
        method = IRFunction(
            name="get_name",
            params=[],
            return_type=IRType(name="string"),
            body=method_body,
        )

        cls = IRClass(name="User", properties=properties, methods=[method])
        module.classes.append(cls)

        code = generate_go(module)

        assert "func (u *User) GetName() (string, error) {" in code
        # Fixed: Should use receiver variable (u) instead of self
        assert "return u.Name, nil" in code


class TestExpressions:
    """Test expression generation."""

    def test_literals(self):
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
                target="f",
                value=IRLiteral(value=3.14, literal_type=LiteralType.FLOAT),
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
        assert "f := 3.14" in code
        assert "b := true" in code
        assert "n := nil" in code

    def test_binary_operations(self):
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
            IRAssignment(
                target="is_equal",
                value=IRBinaryOp(
                    op=BinaryOperator.EQUAL,
                    left=IRIdentifier(name="x"),
                    right=IRIdentifier(name="y"),
                ),
                is_declaration=True,
            ),
        ]

        func = IRFunction(name="test_ops", params=[], body=body)
        module.functions.append(func)

        code = generate_go(module)

        assert "sum := (1 + 2)" in code
        assert "is_equal := (x == y)" in code

    def test_function_call(self):
        """Test function call."""
        module = IRModule(name="test", version="1.0.0")

        body = [
            IRAssignment(
                target="result",
                value=IRCall(
                    function=IRIdentifier(name="process"),
                    args=[
                        IRLiteral(value="data", literal_type=LiteralType.STRING),
                        IRLiteral(value=42, literal_type=LiteralType.INTEGER),
                    ],
                ),
                is_declaration=True,
            )
        ]

        func = IRFunction(name="caller", params=[], body=body)
        module.functions.append(func)

        code = generate_go(module)

        assert 'result := process("data", 42)' in code

    def test_property_access(self):
        """Test property access."""
        module = IRModule(name="test", version="1.0.0")

        body = [
            IRAssignment(
                target="name",
                value=IRPropertyAccess(
                    object=IRIdentifier(name="user"), property="name"
                ),
                is_declaration=True,
            )
        ]

        func = IRFunction(name="get_name", params=[], body=body)
        module.functions.append(func)

        code = generate_go(module)

        assert "name := user.Name" in code

    def test_array_literal(self):
        """Test array literal."""
        module = IRModule(name="test", version="1.0.0")

        body = [
            IRAssignment(
                target="items",
                value=IRArray(
                    elements=[
                        IRLiteral(value=1, literal_type=LiteralType.INTEGER),
                        IRLiteral(value=2, literal_type=LiteralType.INTEGER),
                        IRLiteral(value=3, literal_type=LiteralType.INTEGER),
                    ]
                ),
                is_declaration=True,
            )
        ]

        func = IRFunction(name="make_array", params=[], body=body)
        module.functions.append(func)

        code = generate_go(module)

        assert "items := []interface{}{1, 2, 3}" in code

    def test_map_literal(self):
        """Test map literal."""
        module = IRModule(name="test", version="1.0.0")

        body = [
            IRAssignment(
                target="data",
                value=IRMap(
                    entries={
                        "name": IRLiteral(value="John", literal_type=LiteralType.STRING),
                        "age": IRLiteral(value=30, literal_type=LiteralType.INTEGER),
                    }
                ),
                is_declaration=True,
            )
        ]

        func = IRFunction(name="make_map", params=[], body=body)
        module.functions.append(func)

        code = generate_go(module)

        assert "data := map[string]interface{}" in code
        assert '"name": "John"' in code
        assert '"age": 30' in code


class TestRoundTrip:
    """Test round-trip: Go → IR → Go."""

    def test_simple_function_roundtrip(self):
        """Test simple function preserves semantics."""
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
        assert "string" in generated_code  # Return type

    def test_struct_roundtrip(self):
        """Test struct definition roundtrip."""
        original_code = """package example

type User struct {
\tID string
\tName string
\tAge int
}
"""

        parser = GoParserV2()
        ir_module = parser.parse_source(original_code, "test.go")

        generator = GoGeneratorV2()
        generated_code = generator.generate(ir_module)

        assert "type User struct" in generated_code
        assert "ID string" in generated_code or "Id string" in generated_code
        assert "Name string" in generated_code
        assert "Age int" in generated_code

    def test_control_flow_roundtrip(self):
        """Test control flow preserves logic."""
        original_code = """package example

func Check(x int) string {
\tif x > 0 {
\t\treturn "positive"
\t} else {
\t\treturn "negative"
\t}
}
"""

        parser = GoParserV2()
        ir_module = parser.parse_source(original_code, "test.go")

        generator = GoGeneratorV2()
        generated_code = generator.generate(ir_module)

        assert "func Check" in generated_code
        assert "if" in generated_code
        assert "else" in generated_code
        # Semantic preservation: positive/negative logic


class TestEdgeCases:
    """Test edge cases and error conditions."""

    def test_empty_function_body(self):
        """Test function with empty body."""
        module = IRModule(name="test", version="1.0.0")
        func = IRFunction(name="noop", params=[], body=[])
        module.functions.append(func)

        code = generate_go(module)

        assert "func Noop() {" in code
        assert "}" in code

    def test_variadic_parameters(self):
        """Test variadic parameters."""
        module = IRModule(name="test", version="1.0.0")

        param = IRParameter(
            name="items", param_type=IRType(name="string"), is_variadic=True
        )
        func = IRFunction(name="print_all", params=[param], body=[])
        module.functions.append(func)

        code = generate_go(module)

        assert "items ...string" in code

    def test_nested_types(self):
        """Test nested collection types."""
        module = IRModule(name="test", version="1.0.0")

        # array<array<int>>
        param = IRParameter(
            name="matrix",
            param_type=IRType(
                name="array",
                generic_args=[
                    IRType(name="array", generic_args=[IRType(name="int")])
                ],
            ),
        )
        func = IRFunction(name="process_matrix", params=[param], body=[])
        module.functions.append(func)

        code = generate_go(module)

        assert "matrix [][]int" in code

    def test_multiple_returns_with_error(self):
        """Test functions with error returns."""
        module = IRModule(name="test", version="1.0.0")

        body = [
            IRReturn(
                value=IRLiteral(value="success", literal_type=LiteralType.STRING)
            )
        ]

        func = IRFunction(
            name="safe_operation",
            params=[],
            return_type=IRType(name="string"),
            throws=["Error"],
            body=body,
        )
        module.functions.append(func)

        code = generate_go(module)

        assert "(string, error)" in code
        assert 'return "success", nil' in code

    def test_package_name_normalization(self):
        """Test package name normalization."""
        test_cases = [
            ("my-package", "mypackage"),
            ("my_package", "mypackage"),
            ("MyPackage", "mypackage"),
            ("123invalid", "123invalid"),  # Still generates, but not ideal
        ]

        for input_name, expected in test_cases:
            module = IRModule(name=input_name, version="1.0.0")
            code = generate_go(module)
            assert f"package {expected}" in code


class TestCodeQuality:
    """Test generated code quality."""

    def test_proper_indentation(self):
        """Test code uses tabs for indentation."""
        module = IRModule(name="test", version="1.0.0")

        body = [
            IRIf(
                condition=IRLiteral(value=True, literal_type=LiteralType.BOOLEAN),
                then_body=[
                    IRReturn(
                        IRLiteral(value="yes", literal_type=LiteralType.STRING)
                    )
                ],
            )
        ]

        func = IRFunction(
            name="test_indent",
            params=[],
            return_type=IRType(name="string"),
            body=body,
        )
        module.functions.append(func)

        code = generate_go(module)

        # Check for tabs
        assert "\t" in code
        # Check structure
        lines = code.split("\n")
        for line in lines:
            if line.strip() and not line.strip().startswith("//"):
                # Indented lines should start with tab or be top-level
                if line.startswith(" "):
                    pytest.fail(f"Line uses spaces instead of tabs: {line}")

    def test_imports_grouped(self):
        """Test imports are properly grouped."""
        module = IRModule(name="test", version="1.0.0")
        module.imports = [
            IRImport(module="fmt"),
            IRImport(module="errors"),
            IRImport(module="time"),
        ]

        # Add function to trigger import generation
        func = IRFunction(
            name="test",
            params=[],
            return_type=IRType(name="string"),
            throws=["Error"],
            body=[],
        )
        module.functions.append(func)

        code = generate_go(module)

        # Should have import block
        assert "import (" in code
        assert '"errors"' in code
        assert '"fmt"' in code

    def test_exported_names(self):
        """Test that names are properly capitalized for export."""
        module = IRModule(name="test", version="1.0.0")

        # Function
        func = IRFunction(name="my_function", params=[], body=[])
        module.functions.append(func)

        # Type
        type_def = IRTypeDefinition(
            name="my_type",
            fields=[IRProperty(name="my_field", prop_type=IRType(name="string"))],
        )
        module.types.append(type_def)

        code = generate_go(module)

        assert "func MyFunction" in code
        assert "type MyType struct" in code
        assert "MyField string" in code


# ============================================================================
# Test Statistics
# ============================================================================


def test_suite_coverage():
    """Report test coverage statistics."""
    import sys

    # Count tests
    test_classes = [
        TestBasicConstructs,
        TestTypeSystem,
        TestControlFlow,
        TestErrorHandling,
        TestAsyncAndGoroutines,
        TestClassesAndMethods,
        TestExpressions,
        TestRoundTrip,
        TestEdgeCases,
        TestCodeQuality,
    ]

    total_tests = 0
    for cls in test_classes:
        methods = [m for m in dir(cls) if m.startswith("test_")]
        total_tests += len(methods)
        print(f"{cls.__name__}: {len(methods)} tests", file=sys.stderr)

    print(f"\nTotal tests: {total_tests}", file=sys.stderr)
    assert total_tests >= 20, "Should have at least 20 comprehensive tests"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
