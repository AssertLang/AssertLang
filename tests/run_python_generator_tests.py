#!/usr/bin/env python3
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
    IRLambda,
    IRLiteral,
    IRMap,
    IRModule,
    IRParameter,
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
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.errors = []

    def run_test(self, name, test_func):
        """Run a single test."""
        try:
            print(f"  {name}...", end=" ")
            test_func()
            print("✓")
            self.passed += 1
        except AssertionError as e:
            print("✗")
            self.failed += 1
            self.errors.append((name, str(e)))
        except Exception as e:
            print("ERROR")
            self.failed += 1
            self.errors.append((name, f"Exception: {e}\n{traceback.format_exc()}"))

    def print_summary(self):
        """Print test summary."""
        total = self.passed + self.failed
        print(f"\n{'='*60}")
        print(f"Test Results: {self.passed}/{total} passed")
        print(f"{'='*60}")

        if self.errors:
            print(f"\nFailures:")
            for name, error in self.errors:
                print(f"\n  {name}:")
                print(f"    {error}")


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
    ast.parse(code)  # Should parse as valid Python
    assert "def greet(name: str) -> str:" in code
    assert "return" in code


def test_function_with_defaults():
    """Test function with default parameters."""
    module = IRModule(
        name="test",
        functions=[
            IRFunction(
                name="calculate",
                params=[
                    IRParameter(name="x", param_type=IRType(name="int")),
                    IRParameter(
                        name="y",
                        param_type=IRType(name="int"),
                        default_value=IRLiteral(value=10, literal_type=LiteralType.INTEGER)
                    )
                ],
                return_type=IRType(name="int"),
                body=[
                    IRReturn(
                        value=IRBinaryOp(
                            op=BinaryOperator.ADD,
                            left=IRIdentifier(name="x"),
                            right=IRIdentifier(name="y")
                        )
                    )
                ]
            )
        ]
    )

    code = generate_python(module)
    ast.parse(code)
    assert "def calculate(x: int, y: int = 10) -> int:" in code


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
                    IRFor(
                        iterator="item",
                        iterable=IRIdentifier(name="items"),
                        body=[
                            IRCall(
                                function=IRIdentifier(name="print"),
                                args=[IRIdentifier(name="item")]
                            )
                        ]
                    )
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
    """Test simple class generation."""
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
                        )
                    ]
                ),
                methods=[
                    IRFunction(
                        name="greet",
                        return_type=IRType(name="string"),
                        body=[
                            IRReturn(value=IRLiteral(value="Hello", literal_type=LiteralType.STRING))
                        ]
                    )
                ]
            )
        ]
    )

    code = generate_python(module)
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
                ],
                doc="User data model"
            )
        ]
    )

    code = generate_python(module)
    ast.parse(code)
    assert "@dataclass" in code
    assert "class User:" in code
    assert "id: int" in code
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
                ]
            )
        ]
    )

    code = generate_python(module)
    ast.parse(code)
    assert "from enum import Enum" in code
    assert "class Status(Enum):" in code
    assert 'PENDING = "pending"' in code


def test_function_call():
    """Test function call generation."""
    module = IRModule(
        name="test",
        functions=[
            IRFunction(
                name="main",
                body=[
                    IRCall(
                        function=IRIdentifier(name="print"),
                        args=[
                            IRLiteral(value="Hello", literal_type=LiteralType.STRING)
                        ],
                        kwargs={
                            "end": IRLiteral(value="\n", literal_type=LiteralType.STRING)
                        }
                    )
                ]
            )
        ]
    )

    code = generate_python(module)
    ast.parse(code)
    assert 'print("Hello", end="\\n")' in code


def test_ternary():
    """Test ternary expression generation."""
    module = IRModule(
        name="test",
        functions=[
            IRFunction(
                name="get_value",
                body=[
                    IRReturn(
                        value=IRTernary(
                            condition=IRIdentifier(name="flag"),
                            true_value=IRLiteral(value="yes", literal_type=LiteralType.STRING),
                            false_value=IRLiteral(value="no", literal_type=LiteralType.STRING)
                        )
                    )
                ]
            )
        ]
    )

    code = generate_python(module)
    ast.parse(code)
    assert '"yes" if flag else "no"' in code


def test_lambda():
    """Test lambda generation."""
    module = IRModule(
        name="test",
        functions=[
            IRFunction(
                name="get_lambda",
                body=[
                    IRReturn(
                        value=IRLambda(
                            params=[IRParameter(name="x", param_type=IRType(name="int"))],
                            body=IRBinaryOp(
                                op=BinaryOperator.MULTIPLY,
                                left=IRIdentifier(name="x"),
                                right=IRLiteral(value=2, literal_type=LiteralType.INTEGER)
                            )
                        )
                    )
                ]
            )
        ]
    )

    code = generate_python(module)
    ast.parse(code)
    assert "lambda x: (x * 2)" in code


def test_round_trip():
    """Test round-trip conversion."""
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

    # Both should be valid Python
    ast.parse(original)
    ast.parse(generated)

    # Check semantic equivalence
    assert "def add" in generated
    assert "a: int" in generated
    assert "b: int" in generated
    assert "-> int" in generated
    assert "return" in generated


def test_nested_generics():
    """Test nested generic types."""
    module = IRModule(
        name="test",
        functions=[
            IRFunction(
                name="get_matrix",
                return_type=IRType(
                    name="array",
                    generic_args=[
                        IRType(
                            name="array",
                            generic_args=[IRType(name="int")]
                        )
                    ]
                )
            )
        ]
    )

    code = generate_python(module)
    ast.parse(code)
    assert "List[List[int]]" in code


def main():
    """Run all tests."""
    print("Python Generator V2 Test Suite")
    print("="*60)

    runner = TestRunner()

    print("\nBasic Generation:")
    runner.run_test("simple_function", test_simple_function)
    runner.run_test("function_with_defaults", test_function_with_defaults)
    runner.run_test("async_function", test_async_function)

    print("\nType System:")
    runner.run_test("array_type", test_array_type)
    runner.run_test("optional_type", test_optional_type)
    runner.run_test("nested_generics", test_nested_generics)

    print("\nControl Flow:")
    runner.run_test("if_statement", test_if_statement)
    runner.run_test("for_loop", test_for_loop)
    runner.run_test("try_except", test_try_except)

    print("\nClasses:")
    runner.run_test("simple_class", test_simple_class)

    print("\nType Definitions:")
    runner.run_test("dataclass", test_dataclass)
    runner.run_test("enum", test_enum)

    print("\nExpressions:")
    runner.run_test("function_call", test_function_call)
    runner.run_test("ternary", test_ternary)
    runner.run_test("lambda", test_lambda)

    print("\nRound-Trip:")
    runner.run_test("round_trip", test_round_trip)

    runner.print_summary()

    # Exit with appropriate code
    sys.exit(0 if runner.failed == 0 else 1)


if __name__ == "__main__":
    main()
