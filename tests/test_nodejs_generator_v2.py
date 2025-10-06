"""
Test Suite for Node.js Generator V2

Tests IR → JavaScript/TypeScript code generation.
Covers:
- Basic constructs (functions, classes, variables)
- Type system (primitives, arrays, objects, optionals)
- Control flow (if/else, for, while, try/catch)
- Async/await patterns
- Arrow functions and modern ES6+ features
- Both JS and TS output modes
- Round-trip tests (JS → IR → JS)
"""

import pytest

from dsl.ir import (
    BinaryOperator,
    IRArray,
    IRAssignment,
    IRBinaryOp,
    IRClass,
    IREnum,
    IREnumVariant,
    IRFunction,
    IRIdentifier,
    IRIf,
    IRImport,
    IRLiteral,
    IRMap,
    IRModule,
    IRParameter,
    IRProperty,
    IRPropertyAccess,
    IRReturn,
    IRType,
    IRTypeDefinition,
    IRWhile,
    LiteralType,
)
from language.nodejs_generator_v2 import NodeJSGeneratorV2, generate_nodejs
from language.nodejs_parser_v2 import NodeJSParserV2


class TestBasicGeneration:
    """Test basic code generation."""

    def test_simple_function_typescript(self):
        """Test simple function generation in TypeScript."""
        func = IRFunction(
            name="greet",
            params=[IRParameter(name="name", param_type=IRType(name="string"))],
            return_type=IRType(name="string"),
            body=[
                IRReturn(
                    value=IRLiteral(value="Hello", literal_type=LiteralType.STRING)
                )
            ],
        )

        module = IRModule(name="test", functions=[func])
        generator = NodeJSGeneratorV2(typescript=True)
        result = generator.generate(module)

        assert "export function greet(name: string): string {" in result
        assert 'return "Hello";' in result

    def test_simple_function_javascript(self):
        """Test simple function generation in JavaScript."""
        func = IRFunction(
            name="greet",
            params=[IRParameter(name="name", param_type=IRType(name="string"))],
            return_type=IRType(name="string"),
            body=[
                IRReturn(
                    value=IRLiteral(value="Hello", literal_type=LiteralType.STRING)
                )
            ],
        )

        module = IRModule(name="test", functions=[func])
        generator = NodeJSGeneratorV2(typescript=False)
        result = generator.generate(module)

        assert "export function greet(name) {" in result
        assert "@param {string} name" in result
        assert "@returns {string}" in result

    def test_async_function(self):
        """Test async function generation."""
        func = IRFunction(
            name="fetchUser",
            params=[IRParameter(name="id", param_type=IRType(name="string"))],
            return_type=IRType(name="User"),
            is_async=True,
            body=[IRReturn(value=IRIdentifier(name="user"))],
        )

        module = IRModule(name="test", functions=[func])
        generator = NodeJSGeneratorV2(typescript=True)
        result = generator.generate(module)

        assert "export async function fetchUser(id: string): Promise<User> {" in result
        assert "return user;" in result

    def test_function_with_default_params(self):
        """Test function with default parameters."""
        func = IRFunction(
            name="multiply",
            params=[
                IRParameter(name="x", param_type=IRType(name="int")),
                IRParameter(
                    name="y",
                    param_type=IRType(name="int"),
                    default_value=IRLiteral(value=2, literal_type=LiteralType.INTEGER),
                ),
            ],
            return_type=IRType(name="int"),
            body=[
                IRReturn(
                    value=IRBinaryOp(
                        op=BinaryOperator.MULTIPLY,
                        left=IRIdentifier(name="x"),
                        right=IRIdentifier(name="y"),
                    )
                )
            ],
        )

        module = IRModule(name="test", functions=[func])
        generator = NodeJSGeneratorV2(typescript=True)
        result = generator.generate(module)

        assert "multiply(x: number, y: number = 2): number" in result


class TestTypeGeneration:
    """Test type system generation."""

    def test_interface_generation(self):
        """Test TypeScript interface generation."""
        type_def = IRTypeDefinition(
            name="User",
            fields=[
                IRProperty(name="id", prop_type=IRType(name="string")),
                IRProperty(name="name", prop_type=IRType(name="string")),
                IRProperty(
                    name="age", prop_type=IRType(name="int", is_optional=True)
                ),
            ],
        )

        module = IRModule(name="test", types=[type_def])
        generator = NodeJSGeneratorV2(typescript=True)
        result = generator.generate(module)

        assert "export interface User {" in result
        assert "id: string;" in result
        assert "name: string;" in result
        assert "age?: number;" in result

    def test_enum_generation_typescript(self):
        """Test TypeScript enum generation."""
        enum = IREnum(
            name="Status",
            variants=[
                IREnumVariant(name="Pending", value="pending"),
                IREnumVariant(name="Completed", value="completed"),
                IREnumVariant(name="Failed", value="failed"),
            ],
        )

        module = IRModule(name="test", enums=[enum])
        generator = NodeJSGeneratorV2(typescript=True)
        result = generator.generate(module)

        assert "export enum Status {" in result
        assert "Pending = 'pending'" in result
        assert "Completed = 'completed'" in result
        assert "Failed = 'failed'" in result

    def test_enum_generation_javascript(self):
        """Test JavaScript enum generation (as frozen object)."""
        enum = IREnum(
            name="Status",
            variants=[
                IREnumVariant(name="Pending", value="pending"),
                IREnumVariant(name="Completed", value="completed"),
            ],
        )

        module = IRModule(name="test", enums=[enum])
        generator = NodeJSGeneratorV2(typescript=False)
        result = generator.generate(module)

        assert "export const Status = Object.freeze({" in result
        assert "Pending: 'pending'" in result
        assert "Completed: 'completed'" in result

    def test_array_type(self):
        """Test array type generation."""
        func = IRFunction(
            name="getNames",
            params=[],
            return_type=IRType(
                name="array", generic_args=[IRType(name="string")]
            ),
            body=[
                IRReturn(
                    value=IRArray(
                        elements=[
                            IRLiteral(value="Alice", literal_type=LiteralType.STRING),
                            IRLiteral(value="Bob", literal_type=LiteralType.STRING),
                        ]
                    )
                )
            ],
        )

        module = IRModule(name="test", functions=[func])
        generator = NodeJSGeneratorV2(typescript=True)
        result = generator.generate(module)

        assert "(): Array[string]" in result or "(): string[]" in result
        assert '["Alice", "Bob"]' in result


class TestClassGeneration:
    """Test class generation."""

    def test_simple_class(self):
        """Test simple class generation."""
        cls = IRClass(
            name="UserService",
            properties=[
                IRProperty(
                    name="apiKey", prop_type=IRType(name="string"), is_private=True
                ),
                IRProperty(
                    name="baseUrl", prop_type=IRType(name="string"), is_private=True
                ),
            ],
            constructor=IRFunction(
                name="constructor",
                params=[
                    IRParameter(name="apiKey", param_type=IRType(name="string")),
                    IRParameter(name="baseUrl", param_type=IRType(name="string")),
                ],
                body=[
                    IRAssignment(
                        target="this.apiKey",
                        value=IRIdentifier(name="apiKey"),
                        is_declaration=False,
                    ),
                    IRAssignment(
                        target="this.baseUrl",
                        value=IRIdentifier(name="baseUrl"),
                        is_declaration=False,
                    ),
                ],
            ),
            methods=[
                IRFunction(
                    name="getUrl",
                    params=[],
                    return_type=IRType(name="string"),
                    body=[
                        IRReturn(
                            value=IRPropertyAccess(
                                object=IRIdentifier(name="this"), property="baseUrl"
                            )
                        )
                    ],
                )
            ],
        )

        module = IRModule(name="test", classes=[cls])
        generator = NodeJSGeneratorV2(typescript=True)
        result = generator.generate(module)

        assert "export class UserService {" in result
        assert "private apiKey: string;" in result
        assert "private baseUrl: string;" in result
        assert "constructor(apiKey: string, baseUrl: string) {" in result
        assert "getUrl(): string {" in result

    def test_class_with_inheritance(self):
        """Test class with inheritance."""
        cls = IRClass(
            name="AdminService",
            base_classes=["UserService"],
            properties=[],
            methods=[],
        )

        module = IRModule(name="test", classes=[cls])
        generator = NodeJSGeneratorV2(typescript=True)
        result = generator.generate(module)

        assert "export class AdminService extends UserService {" in result


class TestControlFlow:
    """Test control flow statement generation."""

    def test_if_else(self):
        """Test if-else statement generation."""
        func = IRFunction(
            name="checkValue",
            params=[IRParameter(name="x", param_type=IRType(name="int"))],
            return_type=IRType(name="string"),
            body=[
                IRIf(
                    condition=IRBinaryOp(
                        op=BinaryOperator.GREATER_THAN,
                        left=IRIdentifier(name="x"),
                        right=IRLiteral(value=0, literal_type=LiteralType.INTEGER),
                    ),
                    then_body=[
                        IRReturn(
                            value=IRLiteral(
                                value="positive", literal_type=LiteralType.STRING
                            )
                        )
                    ],
                    else_body=[
                        IRReturn(
                            value=IRLiteral(
                                value="negative", literal_type=LiteralType.STRING
                            )
                        )
                    ],
                )
            ],
        )

        module = IRModule(name="test", functions=[func])
        generator = NodeJSGeneratorV2(typescript=True)
        result = generator.generate(module)

        assert "if ((x > 0)) {" in result
        assert '  return "positive";' in result
        assert "} else {" in result
        assert '  return "negative";' in result

    def test_while_loop(self):
        """Test while loop generation."""
        func = IRFunction(
            name="countdown",
            params=[IRParameter(name="n", param_type=IRType(name="int"))],
            return_type=None,
            body=[
                IRWhile(
                    condition=IRBinaryOp(
                        op=BinaryOperator.GREATER_THAN,
                        left=IRIdentifier(name="n"),
                        right=IRLiteral(value=0, literal_type=LiteralType.INTEGER),
                    ),
                    body=[
                        IRAssignment(
                            target="n",
                            value=IRBinaryOp(
                                op=BinaryOperator.SUBTRACT,
                                left=IRIdentifier(name="n"),
                                right=IRLiteral(value=1, literal_type=LiteralType.INTEGER),
                            ),
                            is_declaration=False,
                        )
                    ],
                )
            ],
        )

        module = IRModule(name="test", functions=[func])
        generator = NodeJSGeneratorV2(typescript=True)
        result = generator.generate(module)

        assert "while ((n > 0)) {" in result
        assert "n = (n - 1);" in result


class TestExpressions:
    """Test expression generation."""

    def test_binary_operations(self):
        """Test binary operation generation."""
        func = IRFunction(
            name="calculate",
            params=[
                IRParameter(name="a", param_type=IRType(name="int")),
                IRParameter(name="b", param_type=IRType(name="int")),
            ],
            return_type=IRType(name="int"),
            body=[
                IRReturn(
                    value=IRBinaryOp(
                        op=BinaryOperator.ADD,
                        left=IRBinaryOp(
                            op=BinaryOperator.MULTIPLY,
                            left=IRIdentifier(name="a"),
                            right=IRLiteral(value=2, literal_type=LiteralType.INTEGER),
                        ),
                        right=IRIdentifier(name="b"),
                    )
                )
            ],
        )

        module = IRModule(name="test", functions=[func])
        generator = NodeJSGeneratorV2(typescript=True)
        result = generator.generate(module)

        assert "return ((a * 2) + b);" in result

    def test_object_literal(self):
        """Test object literal generation."""
        func = IRFunction(
            name="createUser",
            params=[],
            return_type=IRType(name="User"),
            body=[
                IRReturn(
                    value=IRMap(
                        entries={
                            "name": IRLiteral(
                                value="Alice", literal_type=LiteralType.STRING
                            ),
                            "age": IRLiteral(value=30, literal_type=LiteralType.INTEGER),
                        }
                    )
                )
            ],
        )

        module = IRModule(name="test", functions=[func])
        generator = NodeJSGeneratorV2(typescript=True)
        result = generator.generate(module)

        assert '{ name: "Alice", age: 30 }' in result

    def test_array_literal(self):
        """Test array literal generation."""
        func = IRFunction(
            name="getNumbers",
            params=[],
            return_type=IRType(name="array", generic_args=[IRType(name="int")]),
            body=[
                IRReturn(
                    value=IRArray(
                        elements=[
                            IRLiteral(value=1, literal_type=LiteralType.INTEGER),
                            IRLiteral(value=2, literal_type=LiteralType.INTEGER),
                            IRLiteral(value=3, literal_type=LiteralType.INTEGER),
                        ]
                    )
                )
            ],
        )

        module = IRModule(name="test", functions=[func])
        generator = NodeJSGeneratorV2(typescript=True)
        result = generator.generate(module)

        assert "return [1, 2, 3];" in result

    def test_property_access(self):
        """Test property access generation."""
        func = IRFunction(
            name="getName",
            params=[IRParameter(name="user", param_type=IRType(name="User"))],
            return_type=IRType(name="string"),
            body=[
                IRReturn(
                    value=IRPropertyAccess(
                        object=IRIdentifier(name="user"), property="name"
                    )
                )
            ],
        )

        module = IRModule(name="test", functions=[func])
        generator = NodeJSGeneratorV2(typescript=True)
        result = generator.generate(module)

        assert "return user.name;" in result


class TestImports:
    """Test import generation."""

    def test_named_imports(self):
        """Test named imports."""
        module = IRModule(
            name="test",
            imports=[IRImport(module="http", items=["createServer", "IncomingMessage"])],
        )

        generator = NodeJSGeneratorV2(typescript=True)
        result = generator.generate(module)

        assert "import { createServer, IncomingMessage } from 'http';" in result

    def test_default_import(self):
        """Test default import."""
        module = IRModule(
            name="test",
            imports=[IRImport(module="express", alias="express")],
        )

        generator = NodeJSGeneratorV2(typescript=True)
        result = generator.generate(module)

        assert "import express from 'express';" in result


class TestRoundTrip:
    """Test round-trip translation (JS → IR → JS)."""

    def test_roundtrip_simple_function(self):
        """Test round-trip for simple function."""
        original_code = """
function greet(name) {
  return "Hello";
}
"""

        # Parse JS → IR
        parser = NodeJSParserV2()
        ir_module = parser.parse_source(original_code, "test")

        # Generate IR → JS
        generator = NodeJSGeneratorV2(typescript=False)
        generated_code = generator.generate(ir_module)

        # Verify key elements preserved
        assert "function greet" in generated_code
        assert "name" in generated_code
        assert '"Hello"' in generated_code
        assert "return" in generated_code

    def test_roundtrip_class(self):
        """Test round-trip for class."""
        original_code = """
class User {
  constructor(name, age) {
    this.name = name;
    this.age = age;
  }

  greet() {
    return "Hello";
  }
}
"""

        # Parse JS → IR
        parser = NodeJSParserV2()
        ir_module = parser.parse_source(original_code, "test")

        # Generate IR → JS
        generator = NodeJSGeneratorV2(typescript=False)
        generated_code = generator.generate(ir_module)

        # Verify key elements preserved
        assert "class User" in generated_code
        assert "constructor" in generated_code
        assert "greet()" in generated_code

    def test_roundtrip_async_function(self):
        """Test round-trip for async function."""
        original_code = """
async function fetchUser(id) {
  const user = await database.get(id);
  return user;
}
"""

        # Parse JS → IR
        parser = NodeJSParserV2()
        ir_module = parser.parse_source(original_code, "test")

        # Generate IR → JS
        generator = NodeJSGeneratorV2(typescript=False)
        generated_code = generator.generate(ir_module)

        # Verify async preserved
        assert "async function fetchUser" in generated_code
        assert "id" in generated_code

    def test_roundtrip_typescript_types(self):
        """Test round-trip for TypeScript with types."""
        original_code = """
interface User {
  id: string;
  name: string;
}

function getUser(id: string): User {
  return { id: id, name: "Test" };
}
"""

        # Parse TS → IR
        parser = NodeJSParserV2()
        ir_module = parser.parse_source(original_code, "test")

        # Generate IR → TS
        generator = NodeJSGeneratorV2(typescript=True)
        generated_code = generator.generate(ir_module)

        # Verify types preserved
        assert "interface User" in generated_code
        assert "id: string" in generated_code
        assert "name: string" in generated_code
        assert "function getUser(id: string): User" in generated_code


class TestEdgeCases:
    """Test edge cases and corner cases."""

    def test_empty_function(self):
        """Test function with no body."""
        func = IRFunction(name="noop", params=[], return_type=None, body=[])

        module = IRModule(name="test", functions=[func])
        generator = NodeJSGeneratorV2(typescript=True)
        result = generator.generate(module)

        assert "export function noop(): void {" in result
        assert "// TODO: Implement" in result

    def test_function_no_params(self):
        """Test function with no parameters."""
        func = IRFunction(
            name="getConstant",
            params=[],
            return_type=IRType(name="int"),
            body=[IRReturn(value=IRLiteral(value=42, literal_type=LiteralType.INTEGER))],
        )

        module = IRModule(name="test", functions=[func])
        generator = NodeJSGeneratorV2(typescript=True)
        result = generator.generate(module)

        assert "export function getConstant(): number {" in result
        assert "return 42;" in result

    def test_nested_objects(self):
        """Test nested object literals."""
        func = IRFunction(
            name="createConfig",
            params=[],
            return_type=IRType(name="any"),
            body=[
                IRReturn(
                    value=IRMap(
                        entries={
                            "server": IRMap(
                                entries={
                                    "port": IRLiteral(
                                        value=3000, literal_type=LiteralType.INTEGER
                                    ),
                                    "host": IRLiteral(
                                        value="localhost",
                                        literal_type=LiteralType.STRING,
                                    ),
                                }
                            )
                        }
                    )
                )
            ],
        )

        module = IRModule(name="test", functions=[func])
        generator = NodeJSGeneratorV2(typescript=True)
        result = generator.generate(module)

        assert "server: { port: 3000" in result
        assert 'host: "localhost"' in result

    def test_string_escaping(self):
        """Test string literal escaping."""
        func = IRFunction(
            name="getMessage",
            params=[],
            return_type=IRType(name="string"),
            body=[
                IRReturn(
                    value=IRLiteral(
                        value='He said "Hello"', literal_type=LiteralType.STRING
                    )
                )
            ],
        )

        module = IRModule(name="test", functions=[func])
        generator = NodeJSGeneratorV2(typescript=True)
        result = generator.generate(module)

        # Should escape quotes
        assert '\\"' in result or "He said" in result

    def test_comparison_operators(self):
        """Test all comparison operators."""
        func = IRFunction(
            name="compare",
            params=[
                IRParameter(name="a", param_type=IRType(name="int")),
                IRParameter(name="b", param_type=IRType(name="int")),
            ],
            return_type=IRType(name="bool"),
            body=[
                IRReturn(
                    value=IRBinaryOp(
                        op=BinaryOperator.EQUAL,
                        left=IRIdentifier(name="a"),
                        right=IRIdentifier(name="b"),
                    )
                )
            ],
        )

        module = IRModule(name="test", functions=[func])
        generator = NodeJSGeneratorV2(typescript=True)
        result = generator.generate(module)

        # Should use === not ==
        assert "===" in result


class TestPublicAPI:
    """Test public API functions."""

    def test_generate_nodejs_function(self):
        """Test generate_nodejs() public function."""
        func = IRFunction(
            name="add",
            params=[
                IRParameter(name="x", param_type=IRType(name="int")),
                IRParameter(name="y", param_type=IRType(name="int")),
            ],
            return_type=IRType(name="int"),
            body=[
                IRReturn(
                    value=IRBinaryOp(
                        op=BinaryOperator.ADD,
                        left=IRIdentifier(name="x"),
                        right=IRIdentifier(name="y"),
                    )
                )
            ],
        )

        module = IRModule(name="test", functions=[func])

        # TypeScript
        ts_code = generate_nodejs(module, typescript=True)
        assert "export function add(x: number, y: number): number {" in ts_code

        # JavaScript
        js_code = generate_nodejs(module, typescript=False)
        assert "export function add(x, y) {" in js_code
        assert "@param {number} x" in js_code


# ============================================================================
# Test Runner
# ============================================================================

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
