"""
Tests for PW Runtime Interpreter

Tests the core runtime functionality:
- Expression evaluation
- Statement execution
- Function calls
- Control flow (if/for/while)
- Pattern matching
"""

import pytest

from dsl.ir import (
    BinaryOperator,
    IRArray,
    IRAssignment,
    IRBinaryOp,
    IRCall,
    IRFor,
    IRForCStyle,
    IRFunction,
    IRIdentifier,
    IRIf,
    IRLiteral,
    IRModule,
    IRParameter,
    IRReturn,
    IRType,
    IRWhile,
    LiteralType,
)
from dsl.pw_runtime import EnumVariantInstance, PWRuntime, PWRuntimeError


def test_runtime_literal_evaluation():
    """Test evaluation of literal values"""
    runtime = PWRuntime()
    scope = {}

    # Integer
    result = runtime.evaluate_expression(IRLiteral(value=42, literal_type=LiteralType.INTEGER), scope)
    assert result == 42

    # Float
    result = runtime.evaluate_expression(IRLiteral(value=3.14, literal_type=LiteralType.FLOAT), scope)
    assert result == 3.14

    # String
    result = runtime.evaluate_expression(
        IRLiteral(value="hello", literal_type=LiteralType.STRING), scope
    )
    assert result == "hello"

    # Boolean
    result = runtime.evaluate_expression(IRLiteral(value=True, literal_type=LiteralType.BOOLEAN), scope)
    assert result is True

    # Null
    result = runtime.evaluate_expression(IRLiteral(value=None, literal_type=LiteralType.NULL), scope)
    assert result is None


def test_runtime_arithmetic():
    """Test arithmetic operations"""
    runtime = PWRuntime()
    scope = {}

    # Addition
    expr = IRBinaryOp(
        op=BinaryOperator.ADD,
        left=IRLiteral(value=5, literal_type=LiteralType.INTEGER),
        right=IRLiteral(value=3, literal_type=LiteralType.INTEGER),
    )
    result = runtime.evaluate_expression(expr, scope)
    assert result == 8

    # Multiplication
    expr = IRBinaryOp(
        op=BinaryOperator.MULTIPLY,
        left=IRLiteral(value=4, literal_type=LiteralType.INTEGER),
        right=IRLiteral(value=7, literal_type=LiteralType.INTEGER),
    )
    result = runtime.evaluate_expression(expr, scope)
    assert result == 28

    # Division
    expr = IRBinaryOp(
        op=BinaryOperator.DIVIDE,
        left=IRLiteral(value=10, literal_type=LiteralType.INTEGER),
        right=IRLiteral(value=2, literal_type=LiteralType.INTEGER),
    )
    result = runtime.evaluate_expression(expr, scope)
    assert result == 5.0


def test_runtime_comparison():
    """Test comparison operators"""
    runtime = PWRuntime()
    scope = {}

    # Equal
    expr = IRBinaryOp(
        op=BinaryOperator.EQUAL,
        left=IRLiteral(value=5, literal_type=LiteralType.INTEGER),
        right=IRLiteral(value=5, literal_type=LiteralType.INTEGER),
    )
    assert runtime.evaluate_expression(expr, scope) is True

    # Not equal
    expr = IRBinaryOp(
        op=BinaryOperator.NOT_EQUAL,
        left=IRLiteral(value=5, literal_type=LiteralType.INTEGER),
        right=IRLiteral(value=3, literal_type=LiteralType.INTEGER),
    )
    assert runtime.evaluate_expression(expr, scope) is True

    # Less than
    expr = IRBinaryOp(
        op=BinaryOperator.LESS_THAN,
        left=IRLiteral(value=3, literal_type=LiteralType.INTEGER),
        right=IRLiteral(value=5, literal_type=LiteralType.INTEGER),
    )
    assert runtime.evaluate_expression(expr, scope) is True


def test_runtime_assignment():
    """Test variable assignment"""
    runtime = PWRuntime()
    scope = {}

    # Simple assignment
    stmt = IRAssignment(
        target="x",
        value=IRLiteral(value=42, literal_type=LiteralType.INTEGER),
        is_declaration=True,
    )
    runtime.execute_statement(stmt, scope)
    assert scope["x"] == 42

    # Update existing variable
    stmt = IRAssignment(
        target="x",
        value=IRLiteral(value=100, literal_type=LiteralType.INTEGER),
        is_declaration=False,
    )
    runtime.execute_statement(stmt, scope)
    assert scope["x"] == 100


def test_runtime_if_statement():
    """Test if/else statements"""
    runtime = PWRuntime()
    scope = {"x": 0}

    # If true
    stmt = IRIf(
        condition=IRLiteral(value=True, literal_type=LiteralType.BOOLEAN),
        then_body=[
            IRAssignment(
                target="x",
                value=IRLiteral(value=10, literal_type=LiteralType.INTEGER),
                is_declaration=False,
            )
        ],
        else_body=[],
    )
    runtime.execute_statement(stmt, scope)
    assert scope["x"] == 10

    # If false (with else)
    scope["x"] = 0
    stmt = IRIf(
        condition=IRLiteral(value=False, literal_type=LiteralType.BOOLEAN),
        then_body=[
            IRAssignment(
                target="x",
                value=IRLiteral(value=10, literal_type=LiteralType.INTEGER),
                is_declaration=False,
            )
        ],
        else_body=[
            IRAssignment(
                target="x",
                value=IRLiteral(value=20, literal_type=LiteralType.INTEGER),
                is_declaration=False,
            )
        ],
    )
    runtime.execute_statement(stmt, scope)
    assert scope["x"] == 20


def test_runtime_for_loop():
    """Test for loop"""
    runtime = PWRuntime()
    scope = {"sum": 0}

    # for (i in [1, 2, 3, 4, 5]): sum = sum + i
    stmt = IRFor(
        iterator="i",
        iterable=IRArray(
            elements=[
                IRLiteral(value=1, literal_type=LiteralType.INTEGER),
                IRLiteral(value=2, literal_type=LiteralType.INTEGER),
                IRLiteral(value=3, literal_type=LiteralType.INTEGER),
                IRLiteral(value=4, literal_type=LiteralType.INTEGER),
                IRLiteral(value=5, literal_type=LiteralType.INTEGER),
            ]
        ),
        body=[
            IRAssignment(
                target="sum",
                value=IRBinaryOp(
                    op=BinaryOperator.ADD,
                    left=IRIdentifier(name="sum"),
                    right=IRIdentifier(name="i"),
                ),
                is_declaration=False,
            )
        ],
    )
    runtime.execute_statement(stmt, scope)
    assert scope["sum"] == 15


def test_runtime_while_loop():
    """Test while loop"""
    runtime = PWRuntime()
    scope = {"count": 0}

    # while (count < 5): count = count + 1
    stmt = IRWhile(
        condition=IRBinaryOp(
            op=BinaryOperator.LESS_THAN,
            left=IRIdentifier(name="count"),
            right=IRLiteral(value=5, literal_type=LiteralType.INTEGER),
        ),
        body=[
            IRAssignment(
                target="count",
                value=IRBinaryOp(
                    op=BinaryOperator.ADD,
                    left=IRIdentifier(name="count"),
                    right=IRLiteral(value=1, literal_type=LiteralType.INTEGER),
                ),
                is_declaration=False,
            )
        ],
    )
    runtime.execute_statement(stmt, scope)
    assert scope["count"] == 5


def test_runtime_function_call():
    """Test function definition and call"""
    runtime = PWRuntime()

    # function add(a: int, b: int) -> int { return a + b }
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
                    right=IRIdentifier(name="b"),
                )
            )
        ],
    )

    # Register function
    runtime.globals["add"] = func

    # Call function
    result = runtime.execute_function(func, [5, 7])
    assert result == 12


def test_runtime_array_operations():
    """Test array creation and indexing"""
    runtime = PWRuntime()
    scope = {}

    # Create array
    arr_expr = IRArray(
        elements=[
            IRLiteral(value=10, literal_type=LiteralType.INTEGER),
            IRLiteral(value=20, literal_type=LiteralType.INTEGER),
            IRLiteral(value=30, literal_type=LiteralType.INTEGER),
        ]
    )
    arr = runtime.evaluate_expression(arr_expr, scope)
    assert arr == [10, 20, 30]
    assert len(arr) == 3

    # Array access
    scope["arr"] = arr
    expr = IRBinaryOp(
        op=BinaryOperator.ADD,
        left=IRBinaryOp(
            op=BinaryOperator.ADD,
            left=IRLiteral(value=0, literal_type=LiteralType.INTEGER),  # arr[0]
            right=IRLiteral(value=0, literal_type=LiteralType.INTEGER),  # placeholder
        ),
        right=IRLiteral(value=0, literal_type=LiteralType.INTEGER),
    )
    # This test is incomplete - need IRIndex support


def test_runtime_function_with_default_params():
    """Test function with default parameters"""
    runtime = PWRuntime()

    # function greet(name: string = "World") -> string { return "Hello " + name }
    func = IRFunction(
        name="greet",
        params=[
            IRParameter(
                name="name",
                param_type=IRType(name="string"),
                default_value=IRLiteral(value="World", literal_type=LiteralType.STRING),
            )
        ],
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

    # Call with argument
    result = runtime.execute_function(func, ["Alice"])
    assert result == "Hello Alice"

    # Call without argument (use default)
    result = runtime.execute_function(func, [])
    assert result == "Hello World"


def test_runtime_c_style_for_loop():
    """Test C-style for loop"""
    runtime = PWRuntime()
    scope = {"sum": 0}

    # for (let i = 0; i < 5; i = i + 1): sum = sum + i
    stmt = IRForCStyle(
        init=IRAssignment(
            target="i",
            value=IRLiteral(value=0, literal_type=LiteralType.INTEGER),
            is_declaration=True,
        ),
        condition=IRBinaryOp(
            op=BinaryOperator.LESS_THAN,
            left=IRIdentifier(name="i"),
            right=IRLiteral(value=5, literal_type=LiteralType.INTEGER),
        ),
        increment=IRAssignment(
            target="i",
            value=IRBinaryOp(
                op=BinaryOperator.ADD,
                left=IRIdentifier(name="i"),
                right=IRLiteral(value=1, literal_type=LiteralType.INTEGER),
            ),
            is_declaration=False,
        ),
        body=[
            IRAssignment(
                target="sum",
                value=IRBinaryOp(
                    op=BinaryOperator.ADD,
                    left=IRIdentifier(name="sum"),
                    right=IRIdentifier(name="i"),
                ),
                is_declaration=False,
            )
        ],
    )
    runtime.execute_statement(stmt, scope)
    assert scope["sum"] == 10  # 0 + 1 + 2 + 3 + 4


def test_runtime_enum_variant():
    """Test enum variant creation"""
    runtime = PWRuntime()
    runtime.load_stdlib()

    # Create Some(42)
    some_constructor = runtime.globals["Some"]
    some_value = some_constructor(42)

    assert isinstance(some_value, EnumVariantInstance)
    assert some_value.variant_name == "Some"
    assert some_value.values == [42]

    # Create None
    none_constructor = runtime.globals["None"]
    none_value = none_constructor()

    assert isinstance(none_value, EnumVariantInstance)
    assert none_value.variant_name == "None"
    assert none_value.values == []


def test_runtime_division_by_zero():
    """Test division by zero error"""
    runtime = PWRuntime()
    scope = {}

    expr = IRBinaryOp(
        op=BinaryOperator.DIVIDE,
        left=IRLiteral(value=10, literal_type=LiteralType.INTEGER),
        right=IRLiteral(value=0, literal_type=LiteralType.INTEGER),
    )

    with pytest.raises(PWRuntimeError, match="Division by zero"):
        runtime.evaluate_expression(expr, scope)


def test_runtime_undefined_variable():
    """Test undefined variable error"""
    runtime = PWRuntime()
    scope = {}

    expr = IRIdentifier(name="undefined_var")

    with pytest.raises(PWRuntimeError, match="Undefined variable: undefined_var"):
        runtime.evaluate_expression(expr, scope)


def test_runtime_logical_operators():
    """Test logical AND, OR, NOT"""
    runtime = PWRuntime()
    scope = {}

    # true AND false
    expr = IRBinaryOp(
        op=BinaryOperator.AND,
        left=IRLiteral(value=True, literal_type=LiteralType.BOOLEAN),
        right=IRLiteral(value=False, literal_type=LiteralType.BOOLEAN),
    )
    assert runtime.evaluate_expression(expr, scope) is False

    # true OR false
    expr = IRBinaryOp(
        op=BinaryOperator.OR,
        left=IRLiteral(value=True, literal_type=LiteralType.BOOLEAN),
        right=IRLiteral(value=False, literal_type=LiteralType.BOOLEAN),
    )
    assert runtime.evaluate_expression(expr, scope) is True


def test_runtime_nested_function_calls():
    """Test nested function calls"""
    runtime = PWRuntime()

    # function double(x: int) -> int { return x * 2 }
    double_func = IRFunction(
        name="double",
        params=[IRParameter(name="x", param_type=IRType(name="int"))],
        return_type=IRType(name="int"),
        body=[
            IRReturn(
                value=IRBinaryOp(
                    op=BinaryOperator.MULTIPLY,
                    left=IRIdentifier(name="x"),
                    right=IRLiteral(value=2, literal_type=LiteralType.INTEGER),
                )
            )
        ],
    )

    runtime.globals["double"] = double_func

    # double(double(5)) -> 20
    result = runtime.execute_function(double_func, [5])
    assert result == 10

    result = runtime.execute_function(double_func, [result])
    assert result == 20


def test_runtime_string_concatenation():
    """Test string concatenation"""
    runtime = PWRuntime()
    scope = {}

    expr = IRBinaryOp(
        op=BinaryOperator.ADD,
        left=IRLiteral(value="Hello ", literal_type=LiteralType.STRING),
        right=IRLiteral(value="World", literal_type=LiteralType.STRING),
    )
    result = runtime.evaluate_expression(expr, scope)
    assert result == "Hello World"
