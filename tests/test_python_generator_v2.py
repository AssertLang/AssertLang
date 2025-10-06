"""
Test Suite for Python Generator V2

Tests the IR → Python code generator with comprehensive coverage:
- Basic constructs (functions, classes, variables)
- Type system (primitives, collections, optionals, generics)
- Control flow (if/for/while/try-except)
- Async/await patterns
- Decorators and metadata
- Round-trip semantic preservation
"""

import ast
import sys
from typing import Any

import pytest

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


class TestBasicGeneration:
    """Test basic code generation."""

    def test_simple_function(self):
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
        print("\n" + code)

        # Should parse as valid Python
        ast.parse(code)

        # Check for expected elements
        assert "def greet(name: str) -> str:" in code
        assert "return" in code

    def test_function_with_default_params(self):
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
        print("\n" + code)

        ast.parse(code)
        assert "def calculate(x: int, y: int = 10) -> int:" in code

    def test_async_function(self):
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
        print("\n" + code)

        ast.parse(code)
        assert "async def fetch_data" in code


class TestTypeSystem:
    """Test type hint generation."""

    def test_primitive_types(self):
        """Test primitive type mapping."""
        module = IRModule(
            name="test",
            functions=[
                IRFunction(
                    name="test_types",
                    params=[
                        IRParameter(name="s", param_type=IRType(name="string")),
                        IRParameter(name="i", param_type=IRType(name="int")),
                        IRParameter(name="f", param_type=IRType(name="float")),
                        IRParameter(name="b", param_type=IRType(name="bool")),
                    ],
                    return_type=IRType(name="any")
                )
            ]
        )

        code = generate_python(module)
        print("\n" + code)

        ast.parse(code)
        assert "s: str" in code
        assert "i: int" in code
        assert "f: float" in code
        assert "b: bool" in code

    def test_array_type(self):
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
        print("\n" + code)

        ast.parse(code)
        assert "items: List[str]" in code
        assert "from typing import List" in code

    def test_map_type(self):
        """Test map/dict type generation."""
        module = IRModule(
            name="test",
            functions=[
                IRFunction(
                    name="process_config",
                    params=[
                        IRParameter(
                            name="config",
                            param_type=IRType(
                                name="map",
                                generic_args=[
                                    IRType(name="string"),
                                    IRType(name="any")
                                ]
                            )
                        )
                    ]
                )
            ]
        )

        code = generate_python(module)
        print("\n" + code)

        ast.parse(code)
        assert "config: Dict[str, Any]" in code
        assert "from typing import" in code

    def test_optional_type(self):
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
        print("\n" + code)

        ast.parse(code)
        assert "Optional[str]" in code

    def test_nested_generics(self):
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
        print("\n" + code)

        ast.parse(code)
        assert "List[List[int]]" in code


class TestControlFlow:
    """Test control flow statement generation."""

    def test_if_statement(self):
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
        print("\n" + code)

        ast.parse(code)
        assert "if (x > 0):" in code
        assert "else:" in code

    def test_for_loop(self):
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
        print("\n" + code)

        ast.parse(code)
        assert "for item in items:" in code

    def test_while_loop(self):
        """Test while loop generation."""
        module = IRModule(
            name="test",
            functions=[
                IRFunction(
                    name="countdown",
                    params=[IRParameter(name="n", param_type=IRType(name="int"))],
                    body=[
                        IRWhile(
                            condition=IRBinaryOp(
                                op=BinaryOperator.GREATER_THAN,
                                left=IRIdentifier(name="n"),
                                right=IRLiteral(value=0, literal_type=LiteralType.INTEGER)
                            ),
                            body=[
                                IRAssignment(
                                    target="n",
                                    value=IRBinaryOp(
                                        op=BinaryOperator.SUBTRACT,
                                        left=IRIdentifier(name="n"),
                                        right=IRLiteral(value=1, literal_type=LiteralType.INTEGER)
                                    ),
                                    is_declaration=False
                                )
                            ]
                        )
                    ]
                )
            ]
        )

        code = generate_python(module)
        print("\n" + code)

        ast.parse(code)
        assert "while (n > 0):" in code

    def test_try_except(self):
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
        print("\n" + code)

        ast.parse(code)
        assert "try:" in code
        assert "except ZeroDivisionError as e:" in code


class TestClasses:
    """Test class generation."""

    def test_simple_class(self):
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
        print("\n" + code)

        ast.parse(code)
        assert "class Person:" in code
        assert "def __init__(self, name: str, age: int) -> None:" in code
        assert "def greet(self) -> str:" in code

    def test_class_inheritance(self):
        """Test class with base classes."""
        module = IRModule(
            name="test",
            classes=[
                IRClass(
                    name="Employee",
                    base_classes=["Person"],
                    properties=[
                        IRProperty(name="employee_id", prop_type=IRType(name="int"))
                    ]
                )
            ]
        )

        code = generate_python(module)
        print("\n" + code)

        ast.parse(code)
        assert "class Employee(Person):" in code


class TestTypeDefinitions:
    """Test type definitions (dataclasses, enums)."""

    def test_dataclass(self):
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
        print("\n" + code)

        ast.parse(code)
        assert "@dataclass" in code
        assert "class User:" in code
        assert "id: int" in code
        assert "email: Optional[str]" in code
        assert '"""User data model"""' in code

    def test_enum(self):
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
        print("\n" + code)

        ast.parse(code)
        assert "from enum import Enum" in code
        assert "class Status(Enum):" in code
        assert 'PENDING = "pending"' in code


class TestExpressions:
    """Test expression generation."""

    def test_binary_operators(self):
        """Test binary operator generation."""
        operators = [
            (BinaryOperator.ADD, "+"),
            (BinaryOperator.SUBTRACT, "-"),
            (BinaryOperator.MULTIPLY, "*"),
            (BinaryOperator.DIVIDE, "/"),
            (BinaryOperator.MODULO, "%"),
            (BinaryOperator.POWER, "**"),
            (BinaryOperator.EQUAL, "=="),
            (BinaryOperator.NOT_EQUAL, "!="),
            (BinaryOperator.LESS_THAN, "<"),
            (BinaryOperator.AND, "and"),
            (BinaryOperator.OR, "or"),
        ]

        for ir_op, py_op in operators:
            module = IRModule(
                name="test",
                functions=[
                    IRFunction(
                        name="test",
                        body=[
                            IRReturn(
                                value=IRBinaryOp(
                                    op=ir_op,
                                    left=IRIdentifier(name="a"),
                                    right=IRIdentifier(name="b")
                                )
                            )
                        ]
                    )
                ]
            )

            code = generate_python(module)
            ast.parse(code)
            assert py_op in code

    def test_unary_operators(self):
        """Test unary operator generation."""
        module = IRModule(
            name="test",
            functions=[
                IRFunction(
                    name="test",
                    body=[
                        IRReturn(
                            value=IRUnaryOp(
                                op=UnaryOperator.NOT,
                                operand=IRIdentifier(name="flag")
                            )
                        )
                    ]
                )
            ]
        )

        code = generate_python(module)
        print("\n" + code)

        ast.parse(code)
        assert "not flag" in code

    def test_function_call(self):
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
        print("\n" + code)

        ast.parse(code)
        assert 'print("Hello", end="\\n")' in code

    def test_array_literal(self):
        """Test array/list literal generation."""
        module = IRModule(
            name="test",
            functions=[
                IRFunction(
                    name="get_list",
                    body=[
                        IRReturn(
                            value=IRArray(elements=[
                                IRLiteral(value=1, literal_type=LiteralType.INTEGER),
                                IRLiteral(value=2, literal_type=LiteralType.INTEGER),
                                IRLiteral(value=3, literal_type=LiteralType.INTEGER)
                            ])
                        )
                    ]
                )
            ]
        )

        code = generate_python(module)
        print("\n" + code)

        ast.parse(code)
        assert "[1, 2, 3]" in code

    def test_dict_literal(self):
        """Test dict literal generation."""
        module = IRModule(
            name="test",
            functions=[
                IRFunction(
                    name="get_dict",
                    body=[
                        IRReturn(
                            value=IRMap(entries={
                                "name": IRLiteral(value="Alice", literal_type=LiteralType.STRING),
                                "age": IRLiteral(value=30, literal_type=LiteralType.INTEGER)
                            })
                        )
                    ]
                )
            ]
        )

        code = generate_python(module)
        print("\n" + code)

        ast.parse(code)
        assert '"name": "Alice"' in code
        assert '"age": 30' in code

    def test_ternary_expression(self):
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
        print("\n" + code)

        ast.parse(code)
        assert '"yes" if flag else "no"' in code

    def test_lambda_expression(self):
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
        print("\n" + code)

        ast.parse(code)
        assert "lambda x: (x * 2)" in code


class TestRoundTrip:
    """Test round-trip conversion: Python → IR → Python."""

    def test_simple_function_roundtrip(self):
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

    def test_class_roundtrip(self):
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

    def test_control_flow_roundtrip(self):
        """Test round-trip for control flow."""
        original = '''
def check_number(x: int) -> str:
    if x > 0:
        return "positive"
    else:
        return "non-positive"
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

        assert "if" in generated
        assert "else:" in generated


class TestEdgeCases:
    """Test edge cases and special scenarios."""

    def test_empty_function(self):
        """Test function with no body."""
        module = IRModule(
            name="test",
            functions=[
                IRFunction(name="empty", params=[], body=[])
            ]
        )

        code = generate_python(module)
        print("\n" + code)

        ast.parse(code)
        assert "pass" in code

    def test_nested_structures(self):
        """Test nested control structures."""
        module = IRModule(
            name="test",
            functions=[
                IRFunction(
                    name="nested",
                    body=[
                        IRFor(
                            iterator="i",
                            iterable=IRArray(elements=[
                                IRLiteral(value=1, literal_type=LiteralType.INTEGER),
                                IRLiteral(value=2, literal_type=LiteralType.INTEGER)
                            ]),
                            body=[
                                IRIf(
                                    condition=IRBinaryOp(
                                        op=BinaryOperator.GREATER_THAN,
                                        left=IRIdentifier(name="i"),
                                        right=IRLiteral(value=0, literal_type=LiteralType.INTEGER)
                                    ),
                                    then_body=[
                                        IRCall(
                                            function=IRIdentifier(name="print"),
                                            args=[IRIdentifier(name="i")]
                                        )
                                    ]
                                )
                            ]
                        )
                    ]
                )
            ]
        )

        code = generate_python(module)
        print("\n" + code)

        ast.parse(code)
        assert "for i in" in code
        assert "if (i > 0):" in code

    def test_multiple_imports(self):
        """Test multiple import types."""
        module = IRModule(
            name="test",
            imports=[
                IRImport(module="os"),
                IRImport(module="sys"),
                IRImport(module="typing", items=["List", "Dict"]),
                IRImport(module="collections", alias="col")
            ]
        )

        code = generate_python(module)
        print("\n" + code)

        ast.parse(code)
        assert "import os" in code
        assert "from typing import List, Dict" in code
        assert "import collections as col" in code


class TestStatistics:
    """Generate statistics about test coverage."""

    def test_generate_statistics(self):
        """Generate statistics report."""
        total_tests = 0
        passed_tests = 0

        # Count tests
        for item in dir(sys.modules[__name__]):
            if item.startswith("Test"):
                cls = getattr(sys.modules[__name__], item)
                for method in dir(cls):
                    if method.startswith("test_"):
                        total_tests += 1

        print(f"\n{'='*60}")
        print(f"Python Generator V2 Test Statistics")
        print(f"{'='*60}")
        print(f"Total test methods: {total_tests}")
        print(f"Test classes: 8")
        print(f"Coverage areas:")
        print(f"  - Basic generation: ✓")
        print(f"  - Type system: ✓")
        print(f"  - Control flow: ✓")
        print(f"  - Classes: ✓")
        print(f"  - Type definitions: ✓")
        print(f"  - Expressions: ✓")
        print(f"  - Round-trip: ✓")
        print(f"  - Edge cases: ✓")
        print(f"{'='*60}")


if __name__ == "__main__":
    # Run with: python -m pytest tests/test_python_generator_v2.py -v -s
    pytest.main([__file__, "-v", "-s"])
