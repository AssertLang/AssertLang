"""
Test runner for Node.js Generator V2 (without pytest dependency)
"""

import sys
import traceback
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

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


class TestRunner:
    """Simple test runner."""

    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.errors = []

    def run_test(self, test_name, test_func):
        """Run a single test."""
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
            error_msg = f"{type(e).__name__}: {e}"
            self.errors.append((test_name, error_msg))
            print(f"✗ {test_name}: {error_msg}")

    def print_summary(self):
        """Print test summary."""
        total = self.passed + self.failed
        print(f"\n{'='*60}")
        print(f"Test Results: {self.passed}/{total} passed")
        print(f"{'='*60}")

        if self.errors:
            print("\nFailed Tests:")
            for name, error in self.errors:
                print(f"  - {name}: {error}")

        return self.failed == 0


def test_simple_function_typescript():
    """Test simple function generation in TypeScript."""
    func = IRFunction(
        name="greet",
        params=[IRParameter(name="name", param_type=IRType(name="string"))],
        return_type=IRType(name="string"),
        body=[IRReturn(value=IRLiteral(value="Hello", literal_type=LiteralType.STRING))],
    )

    module = IRModule(name="test", functions=[func])
    generator = NodeJSGeneratorV2(typescript=True)
    result = generator.generate(module)

    assert "export function greet(name: string): string {" in result, "Missing function signature"
    assert 'return "Hello";' in result, "Missing return statement"


def test_simple_function_javascript():
    """Test simple function generation in JavaScript."""
    func = IRFunction(
        name="greet",
        params=[IRParameter(name="name", param_type=IRType(name="string"))],
        return_type=IRType(name="string"),
        body=[IRReturn(value=IRLiteral(value="Hello", literal_type=LiteralType.STRING))],
    )

    module = IRModule(name="test", functions=[func])
    generator = NodeJSGeneratorV2(typescript=False)
    result = generator.generate(module)

    assert "export function greet(name) {" in result, "Missing function signature"
    assert "@param {string} name" in result, "Missing JSDoc param"
    assert "@returns {string}" in result, "Missing JSDoc returns"


def test_async_function():
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


def test_interface_generation():
    """Test TypeScript interface generation."""
    type_def = IRTypeDefinition(
        name="User",
        fields=[
            IRProperty(name="id", prop_type=IRType(name="string")),
            IRProperty(name="name", prop_type=IRType(name="string")),
            IRProperty(name="age", prop_type=IRType(name="int", is_optional=True)),
        ],
    )

    module = IRModule(name="test", types=[type_def])
    generator = NodeJSGeneratorV2(typescript=True)
    result = generator.generate(module)

    assert "export interface User {" in result
    assert "id: string;" in result
    assert "name: string;" in result
    assert "age?: number;" in result


def test_enum_generation_typescript():
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


def test_simple_class():
    """Test simple class generation."""
    cls = IRClass(
        name="UserService",
        properties=[
            IRProperty(name="apiKey", prop_type=IRType(name="string"), is_private=True),
            IRProperty(name="baseUrl", prop_type=IRType(name="string"), is_private=True),
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
    assert "constructor(apiKey: string, baseUrl: string) {" in result


def test_if_else():
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
                        value=IRLiteral(value="positive", literal_type=LiteralType.STRING)
                    )
                ],
                else_body=[
                    IRReturn(
                        value=IRLiteral(value="negative", literal_type=LiteralType.STRING)
                    )
                ],
            )
        ],
    )

    module = IRModule(name="test", functions=[func])
    generator = NodeJSGeneratorV2(typescript=True)
    result = generator.generate(module)

    assert "if ((x > 0)) {" in result
    assert "} else {" in result


def test_while_loop():
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


def test_object_literal():
    """Test object literal generation."""
    func = IRFunction(
        name="createUser",
        params=[],
        return_type=IRType(name="User"),
        body=[
            IRReturn(
                value=IRMap(
                    entries={
                        "name": IRLiteral(value="Alice", literal_type=LiteralType.STRING),
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


def test_array_literal():
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


def test_named_imports():
    """Test named imports."""
    module = IRModule(
        name="test",
        imports=[IRImport(module="http", items=["createServer", "IncomingMessage"])],
    )

    generator = NodeJSGeneratorV2(typescript=True)
    result = generator.generate(module)

    assert "import { createServer, IncomingMessage } from 'http';" in result


def test_roundtrip_simple_function():
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


def test_public_api():
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


def test_comparison_operators():
    """Test comparison operators use === not ==."""
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


def test_property_access():
    """Test property access generation."""
    func = IRFunction(
        name="getName",
        params=[IRParameter(name="user", param_type=IRType(name="User"))],
        return_type=IRType(name="string"),
        body=[
            IRReturn(value=IRPropertyAccess(object=IRIdentifier(name="user"), property="name"))
        ],
    )

    module = IRModule(name="test", functions=[func])
    generator = NodeJSGeneratorV2(typescript=True)
    result = generator.generate(module)

    assert "return user.name;" in result


def test_binary_operations():
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


def test_empty_function():
    """Test function with no body."""
    func = IRFunction(name="noop", params=[], return_type=None, body=[])

    module = IRModule(name="test", functions=[func])
    generator = NodeJSGeneratorV2(typescript=True)
    result = generator.generate(module)

    assert "export function noop(): void {" in result
    assert "// TODO: Implement" in result


def main():
    """Run all tests."""
    runner = TestRunner()

    print("Running Node.js Generator V2 Tests\n")
    print("="*60)

    # Basic generation tests
    runner.run_test("test_simple_function_typescript", test_simple_function_typescript)
    runner.run_test("test_simple_function_javascript", test_simple_function_javascript)
    runner.run_test("test_async_function", test_async_function)

    # Type generation tests
    runner.run_test("test_interface_generation", test_interface_generation)
    runner.run_test("test_enum_generation_typescript", test_enum_generation_typescript)

    # Class generation tests
    runner.run_test("test_simple_class", test_simple_class)

    # Control flow tests
    runner.run_test("test_if_else", test_if_else)
    runner.run_test("test_while_loop", test_while_loop)

    # Expression tests
    runner.run_test("test_object_literal", test_object_literal)
    runner.run_test("test_array_literal", test_array_literal)
    runner.run_test("test_property_access", test_property_access)
    runner.run_test("test_binary_operations", test_binary_operations)
    runner.run_test("test_comparison_operators", test_comparison_operators)

    # Import tests
    runner.run_test("test_named_imports", test_named_imports)

    # Round-trip tests
    runner.run_test("test_roundtrip_simple_function", test_roundtrip_simple_function)

    # API tests
    runner.run_test("test_public_api", test_public_api)

    # Edge case tests
    runner.run_test("test_empty_function", test_empty_function)

    # Print summary
    success = runner.print_summary()
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
