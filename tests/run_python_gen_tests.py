"""
Simple test runner for Python Generator V2 (no pytest required)
"""

import ast
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
    IRBreak,
    IRCall,
    IRCatch,
    IRClass,
    IRContinue,
    IREnum,
    IREnumVariant,
    IRFor,
    IRFunction,
    IRIdentifier,
    IRIf,
    IRImport,
    IRIndex,
    IRLambda,
    IRLiteral,
    IRMap,
    IRModule,
    IRParameter,
    IRPass,
    IRProperty,
    IRPropertyAccess,
    IRReturn,
    IRTernary,
    IRThrow,
    IRTry,
    IRType,
    IRTypeDefinition,
    IRUnaryOp,
    IRWhile,
    LiteralType,
    UnaryOperator,
)
from language.python_generator_v2 import PythonGeneratorV2, generate_python
from language.python_parser_v2 import PythonParserV2


class TestRunner:
    """Simple test runner."""

    def __init__(self):
        self.total = 0
        self.passed = 0
        self.failed = 0
        self.errors = []

    def run_test(self, name, func):
        """Run a single test."""
        self.total += 1
        try:
            func()
            self.passed += 1
            print(f"✓ {name}")
        except AssertionError as e:
            self.failed += 1
            self.errors.append((name, str(e)))
            print(f"✗ {name}: {e}")
        except Exception as e:
            self.failed += 1
            self.errors.append((name, traceback.format_exc()))
            print(f"✗ {name}: ERROR - {e}")

    def report(self):
        """Print test report."""
        print("\n" + "="*60)
        print(f"Test Results: {self.passed}/{self.total} passed")
        print("="*60)

        if self.errors:
            print("\nFailed Tests:")
            for name, error in self.errors:
                print(f"\n{name}:")
                print(f"  {error}")

        pass_rate = (self.passed / self.total * 100) if self.total > 0 else 0
        print(f"\nPass Rate: {pass_rate:.1f}%")
        return self.passed == self.total


# Test Functions

def test_simple_function():
    """Test generating a simple function."""
    module = IRModule(
        name="test",
        functions=[
            IRFunction(
                name="greet",
                params=[
                    IRParameter(name="name", param_type=IRType(name="string"))
                ],
                return_type=IRType(name="string"),
                body=[
                    IRReturn(
                        value=IRBinaryOp(
                            op=BinaryOperator.ADD,
                            left=IRLiteral(value="Hello ", literal_type=LiteralType.STRING),
                            right=IRIdentifier(name="name")
                        )
                    )
                ]
            )
        ]
    )

    code = generate_python(module)
    print(f"\nGenerated code:\n{code}\n")

    # Should parse as valid Python
    ast.parse(code)

    # Check for expected elements
    assert "def greet(name: str) -> str:" in code
    assert "return" in code


def test_async_function():
    """Test async function generation."""
    module = IRModule(
        name="test",
        functions=[
            IRFunction(
                name="fetch_data",
                params=[IRParameter(name="url", param_type=IRType(name="string"))],
                return_type=IRType(name="string"),
                is_async=True,
                body=[
                    IRReturn(value=IRLiteral(value="data", literal_type=LiteralType.STRING))
                ]
            )
        ]
    )

    code = generate_python(module)
    ast.parse(code)
    assert "async def fetch_data" in code


def test_array_type():
    """Test array/list type generation."""
    module = IRModule(
        name="test",
        functions=[
            IRFunction(
                name="process_items",
                params=[
                    IRParameter(
                        name="items",
                        param_type=IRType(
                            name="array",
                            generic_args=[IRType(name="string")]
                        )
                    )
                ],
                return_type=IRType(name="int")
            )
        ]
    )

    code = generate_python(module)
    ast.parse(code)
    assert "items: List[str]" in code
    assert "from typing import List" in code


def test_optional_type():
    """Test optional type generation."""
    module = IRModule(
        name="test",
        functions=[
            IRFunction(
                name="find_user",
                params=[IRParameter(name="id", param_type=IRType(name="int"))],
                return_type=IRType(name="string", is_optional=True)
            )
        ]
    )

    code = generate_python(module)
    ast.parse(code)
    assert "Optional[str]" in code


def test_if_statement():
    """Test if/else generation."""
    module = IRModule(
        name="test",
        functions=[
            IRFunction(
                name="check_value",
                params=[IRParameter(name="x", param_type=IRType(name="int"))],
                body=[
                    IRIf(
                        condition=IRBinaryOp(
                            op=BinaryOperator.GREATER_THAN,
                            left=IRIdentifier(name="x"),
                            right=IRLiteral(value=0, literal_type=LiteralType.INTEGER)
                        ),
                        then_body=[
                            IRReturn(value=IRLiteral(value="positive", literal_type=LiteralType.STRING))
                        ],
                        else_body=[
                            IRReturn(value=IRLiteral(value="non-positive", literal_type=LiteralType.STRING))
                        ]
                    )
                ]
            )
        ]
    )

    code = generate_python(module)
    ast.parse(code)
    assert "if (x > 0):" in code
    assert "else:" in code


def test_for_loop():
    """Test for loop generation."""
    module = IRModule(
        name="test",
        functions=[
            IRFunction(
                name="sum_items",
                params=[
                    IRParameter(
                        name="items",
                        param_type=IRType(name="array", generic_args=[IRType(name="int")])
                    )
                ],
                body=[
                    IRAssignment(
                        target="total",
                        value=IRLiteral(value=0, literal_type=LiteralType.INTEGER),
                        var_type=IRType(name="int")
                    ),
                    IRFor(
                        iterator="item",
                        iterable=IRIdentifier(name="items"),
                        body=[
                            IRAssignment(
                                target="total",
                                value=IRBinaryOp(
                                    op=BinaryOperator.ADD,
                                    left=IRIdentifier(name="total"),
                                    right=IRIdentifier(name="item")
                                ),
                                is_declaration=False
                            )
                        ]
                    ),
                    IRReturn(value=IRIdentifier(name="total"))
                ]
            )
        ]
    )

    code = generate_python(module)
    ast.parse(code)
    assert "for item in items:" in code


def test_try_except():
    """Test try/except generation."""
    module = IRModule(
        name="test",
        functions=[
            IRFunction(
                name="safe_divide",
                params=[
                    IRParameter(name="a", param_type=IRType(name="float")),
                    IRParameter(name="b", param_type=IRType(name="float"))
                ],
                body=[
                    IRTry(
                        try_body=[
                            IRReturn(
                                value=IRBinaryOp(
                                    op=BinaryOperator.DIVIDE,
                                    left=IRIdentifier(name="a"),
                                    right=IRIdentifier(name="b")
                                )
                            )
                        ],
                        catch_blocks=[
                            IRCatch(
                                exception_type="ZeroDivisionError",
                                exception_var="e",
                                body=[
                                    IRReturn(value=IRLiteral(value=0.0, literal_type=LiteralType.FLOAT))
                                ]
                            )
                        ]
                    )
                ]
            )
        ]
    )

    code = generate_python(module)
    ast.parse(code)
    assert "try:" in code
    assert "except ZeroDivisionError as e:" in code


def test_simple_class():
    """Test simple class with properties and methods."""
    module = IRModule(
        name="test",
        classes=[
            IRClass(
                name="Person",
                properties=[
                    IRProperty(name="name", prop_type=IRType(name="string")),
                    IRProperty(name="age", prop_type=IRType(name="int"))
                ],
                constructor=IRFunction(
                    name="__init__",
                    params=[
                        IRParameter(name="name", param_type=IRType(name="string")),
                        IRParameter(name="age", param_type=IRType(name="int"))
                    ],
                    body=[
                        IRAssignment(
                            target="self.name",
                            value=IRIdentifier(name="name"),
                            is_declaration=False
                        ),
                        IRAssignment(
                            target="self.age",
                            value=IRIdentifier(name="age"),
                            is_declaration=False
                        )
                    ]
                ),
                methods=[
                    IRFunction(
                        name="greet",
                        return_type=IRType(name="string"),
                        body=[
                            IRReturn(
                                value=IRBinaryOp(
                                    op=BinaryOperator.ADD,
                                    left=IRLiteral(value="Hello, ", literal_type=LiteralType.STRING),
                                    right=IRPropertyAccess(
                                        object=IRIdentifier(name="self"),
                                        property="name"
                                    )
                                )
                            )
                        ]
                    )
                ]
            )
        ]
    )

    code = generate_python(module)
    print(f"\nGenerated class:\n{code}\n")
    ast.parse(code)
    assert "class Person:" in code
    assert "def __init__(self, name: str, age: int) -> None:" in code
    assert "def greet(self) -> str:" in code


def test_dataclass():
    """Test dataclass generation."""
    module = IRModule(
        name="test",
        types=[
            IRTypeDefinition(
                name="User",
                fields=[
                    IRProperty(name="id", prop_type=IRType(name="int")),
                    IRProperty(name="name", prop_type=IRType(name="string")),
                    IRProperty(
                        name="email",
                        prop_type=IRType(name="string", is_optional=True)
                    )
                ],
                doc="User data model"
            )
        ]
    )

    code = generate_python(module)
    print(f"\nGenerated dataclass:\n{code}\n")
    ast.parse(code)
    assert "@dataclass" in code
    assert "class User:" in code
    assert "id: int" in code
    assert "email: Optional[str]" in code
    assert '"""User data model"""' in code


def test_enum():
    """Test enum generation."""
    module = IRModule(
        name="test",
        enums=[
            IREnum(
                name="Status",
                variants=[
                    IREnumVariant(name="PENDING", value="pending"),
                    IREnumVariant(name="ACTIVE", value="active"),
                    IREnumVariant(name="COMPLETED", value="completed")
                ]
            )
        ]
    )

    code = generate_python(module)
    print(f"\nGenerated enum:\n{code}\n")
    ast.parse(code)
    assert "from enum import Enum" in code
    assert "class Status(Enum):" in code
    assert 'PENDING = "pending"' in code


def test_roundtrip_function():
    """Test round-trip for simple function."""
    original = '''
def add(a: int, b: int) -> int:
    """Add two numbers."""
    return a + b
'''

    # Parse to IR
    parser = PythonParserV2()
    ir_module = parser.parse_source(original, "test")

    # Generate back to Python
    generator = PythonGeneratorV2()
    generated = generator.generate(ir_module)

    print("\nOriginal:")
    print(original)
    print("\nGenerated:")
    print(generated)

    # Both should be valid Python
    ast.parse(original)
    ast.parse(generated)

    # Check semantic equivalence
    assert "def add" in generated
    assert "a: int" in generated
    assert "b: int" in generated
    assert "-> int" in generated
    assert "return" in generated


def test_roundtrip_class():
    """Test round-trip for class."""
    original = '''
class Calculator:
    def __init__(self, name: str):
        self.name = name

    def add(self, a: int, b: int) -> int:
        return a + b
'''

    parser = PythonParserV2()
    ir_module = parser.parse_source(original, "test")

    generator = PythonGeneratorV2()
    generated = generator.generate(ir_module)

    print("\nOriginal:")
    print(original)
    print("\nGenerated:")
    print(generated)

    ast.parse(original)
    ast.parse(generated)

    assert "class Calculator:" in generated
    assert "def __init__" in generated
    assert "def add" in generated


def test_literals():
    """Test various literal types."""
    module = IRModule(
        name="test",
        functions=[
            IRFunction(
                name="test_literals",
                body=[
                    IRReturn(
                        value=IRArray(elements=[
                            IRLiteral(value="string", literal_type=LiteralType.STRING),
                            IRLiteral(value=42, literal_type=LiteralType.INTEGER),
                            IRLiteral(value=3.14, literal_type=LiteralType.FLOAT),
                            IRLiteral(value=True, literal_type=LiteralType.BOOLEAN),
                            IRLiteral(value=None, literal_type=LiteralType.NULL),
                        ])
                    )
                ]
            )
        ]
    )

    code = generate_python(module)
    ast.parse(code)
    assert '"string"' in code
    assert '42' in code
    assert '3.14' in code
    assert 'True' in code
    assert 'None' in code


# Main test runner

def main():
    """Run all tests."""
    runner = TestRunner()

    print("\n" + "="*60)
    print("Python Generator V2 - Test Suite")
    print("="*60 + "\n")

    # Basic generation
    print("Basic Generation:")
    runner.run_test("simple_function", test_simple_function)
    runner.run_test("async_function", test_async_function)

    # Type system
    print("\nType System:")
    runner.run_test("array_type", test_array_type)
    runner.run_test("optional_type", test_optional_type)

    # Control flow
    print("\nControl Flow:")
    runner.run_test("if_statement", test_if_statement)
    runner.run_test("for_loop", test_for_loop)
    runner.run_test("try_except", test_try_except)

    # Classes
    print("\nClasses:")
    runner.run_test("simple_class", test_simple_class)

    # Type definitions
    print("\nType Definitions:")
    runner.run_test("dataclass", test_dataclass)
    runner.run_test("enum", test_enum)

    # Round-trip
    print("\nRound-Trip:")
    runner.run_test("roundtrip_function", test_roundtrip_function)
    runner.run_test("roundtrip_class", test_roundtrip_class)

    # Expressions
    print("\nExpressions:")
    runner.run_test("literals", test_literals)

    # Report
    success = runner.report()
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
