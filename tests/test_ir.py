"""
Tests for AssertLang IR (Intermediate Representation)

This test suite validates:
1. IR node creation and initialization
2. IR node properties and metadata
3. Type system functionality
4. IR tree construction
5. Semantic validation
"""

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
    IRProperty,
    IRPropertyAccess,
    IRReturn,
    IRThrow,
    IRTry,
    IRType,
    IRTypeDefinition,
    IRUnaryOp,
    IRWhile,
    LiteralType,
    NodeType,
    SourceLocation,
    UnaryOperator,
)
from dsl.validator import IRValidator, ValidationError, validate_ir


# ============================================================================
# Test Basic Node Creation
# ============================================================================


def test_source_location():
    """Test SourceLocation creation and representation."""
    loc = SourceLocation(file="test.py", line=10, column=5)
    assert loc.file == "test.py"
    assert loc.line == 10
    assert loc.column == 5
    assert "test.py:10:5" in str(loc)

    loc2 = SourceLocation(line=20)
    assert "line 20" in str(loc2)


def test_ir_type_basic():
    """Test basic IRType creation."""
    # Primitive type
    str_type = IRType(name="string")
    assert str_type.name == "string"
    assert str_type.type == NodeType.TYPE
    assert str(str_type) == "string"

    # Optional type
    opt_int = IRType(name="int", is_optional=True)
    assert str(opt_int) == "int?"

    # Generic type
    array_str = IRType(
        name="array",
        generic_args=[IRType(name="string")]
    )
    assert str(array_str) == "array<string>"

    # Complex generic
    map_str_int = IRType(
        name="map",
        generic_args=[
            IRType(name="string"),
            IRType(name="int")
        ]
    )
    assert str(map_str_int) == "map<string, int>"


def test_ir_literal():
    """Test IRLiteral creation."""
    # String literal
    str_lit = IRLiteral(value="hello", literal_type=LiteralType.STRING)
    assert str_lit.value == "hello"
    assert str_lit.literal_type == LiteralType.STRING
    assert str_lit.type == NodeType.LITERAL

    # Integer literal
    int_lit = IRLiteral(value=42, literal_type=LiteralType.INTEGER)
    assert int_lit.value == 42

    # Boolean literal
    bool_lit = IRLiteral(value=True, literal_type=LiteralType.BOOLEAN)
    assert bool_lit.value is True

    # Null literal
    null_lit = IRLiteral(value=None, literal_type=LiteralType.NULL)
    assert null_lit.value is None


def test_ir_identifier():
    """Test IRIdentifier creation."""
    ident = IRIdentifier(name="user")
    assert ident.name == "user"
    assert ident.type == NodeType.IDENTIFIER


def test_ir_binary_op():
    """Test IRBinaryOp creation."""
    left = IRLiteral(value=1, literal_type=LiteralType.INTEGER)
    right = IRLiteral(value=2, literal_type=LiteralType.INTEGER)
    add_op = IRBinaryOp(op=BinaryOperator.ADD, left=left, right=right)

    assert add_op.op == BinaryOperator.ADD
    assert add_op.left == left
    assert add_op.right == right
    assert add_op.type == NodeType.BINARY_OP


def test_ir_unary_op():
    """Test IRUnaryOp creation."""
    operand = IRIdentifier(name="x")
    not_op = IRUnaryOp(op=UnaryOperator.NOT, operand=operand)

    assert not_op.op == UnaryOperator.NOT
    assert not_op.operand == operand
    assert not_op.type == NodeType.UNARY_OP


# ============================================================================
# Test Function and Class Nodes
# ============================================================================


def test_ir_parameter():
    """Test IRParameter creation."""
    param = IRParameter(
        name="amount",
        param_type=IRType(name="float"),
        default_value=IRLiteral(value=0.0, literal_type=LiteralType.FLOAT)
    )
    assert param.name == "amount"
    assert param.param_type.name == "float"
    assert param.default_value.value == 0.0
    assert param.type == NodeType.PARAMETER


def test_ir_function_simple():
    """Test simple IRFunction creation."""
    func = IRFunction(
        name="add",
        params=[
            IRParameter(name="a", param_type=IRType(name="int")),
            IRParameter(name="b", param_type=IRType(name="int"))
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

    assert func.name == "add"
    assert len(func.params) == 2
    assert func.return_type.name == "int"
    assert len(func.body) == 1
    assert func.type == NodeType.FUNCTION


def test_ir_function_with_metadata():
    """Test IRFunction with metadata."""
    func = IRFunction(name="test")
    func.location = SourceLocation(file="test.py", line=10)
    func.comment = "Test function"

    assert func.location.file == "test.py"
    assert func.comment == "Test function"
    assert "test.py" in str(func.location)


def test_ir_property():
    """Test IRProperty creation."""
    prop = IRProperty(
        name="api_key",
        prop_type=IRType(name="string"),
        is_private=True
    )
    assert prop.name == "api_key"
    assert prop.prop_type.name == "string"
    assert prop.is_private is True
    assert prop.type == NodeType.PROPERTY


def test_ir_class():
    """Test IRClass creation."""
    cls = IRClass(
        name="User",
        properties=[
            IRProperty(name="id", prop_type=IRType(name="string")),
            IRProperty(name="name", prop_type=IRType(name="string"))
        ],
        methods=[
            IRFunction(
                name="get_display_name",
                return_type=IRType(name="string"),
                body=[
                    IRReturn(value=IRIdentifier(name="name"))
                ]
            )
        ]
    )

    assert cls.name == "User"
    assert len(cls.properties) == 2
    assert len(cls.methods) == 1
    assert cls.methods[0].name == "get_display_name"
    assert cls.type == NodeType.CLASS


# ============================================================================
# Test Statement Nodes
# ============================================================================


def test_ir_if():
    """Test IRIf statement."""
    if_stmt = IRIf(
        condition=IRBinaryOp(
            op=BinaryOperator.EQUAL,
            left=IRIdentifier(name="x"),
            right=IRLiteral(value=None, literal_type=LiteralType.NULL)
        ),
        then_body=[
            IRReturn(value=IRLiteral(value=0, literal_type=LiteralType.INTEGER))
        ],
        else_body=[
            IRReturn(value=IRIdentifier(name="x"))
        ]
    )

    assert if_stmt.type == NodeType.IF
    assert isinstance(if_stmt.condition, IRBinaryOp)
    assert len(if_stmt.then_body) == 1
    assert len(if_stmt.else_body) == 1


def test_ir_for():
    """Test IRFor loop."""
    for_loop = IRFor(
        iterator="item",
        iterable=IRIdentifier(name="items"),
        body=[
            IRCall(
                function=IRIdentifier(name="process"),
                args=[IRIdentifier(name="item")]
            )
        ]
    )

    assert for_loop.type == NodeType.FOR
    assert for_loop.iterator == "item"
    assert len(for_loop.body) == 1


def test_ir_while():
    """Test IRWhile loop."""
    while_loop = IRWhile(
        condition=IRBinaryOp(
            op=BinaryOperator.GREATER_THAN,
            left=IRIdentifier(name="count"),
            right=IRLiteral(value=0, literal_type=LiteralType.INTEGER)
        ),
        body=[
            IRAssignment(
                target="count",
                value=IRBinaryOp(
                    op=BinaryOperator.SUBTRACT,
                    left=IRIdentifier(name="count"),
                    right=IRLiteral(value=1, literal_type=LiteralType.INTEGER)
                )
            )
        ]
    )

    assert while_loop.type == NodeType.WHILE
    assert isinstance(while_loop.condition, IRBinaryOp)
    assert len(while_loop.body) == 1


def test_ir_try_catch():
    """Test IRTry/IRCatch statement."""
    try_stmt = IRTry(
        try_body=[
            IRCall(
                function=IRIdentifier(name="risky_operation"),
                args=[]
            )
        ],
        catch_blocks=[
            IRCatch(
                exception_type="NetworkError",
                exception_var="e",
                body=[
                    IRCall(
                        function=IRIdentifier(name="log"),
                        args=[IRIdentifier(name="e")]
                    )
                ]
            )
        ]
    )

    assert try_stmt.type == NodeType.TRY
    assert len(try_stmt.try_body) == 1
    assert len(try_stmt.catch_blocks) == 1
    assert try_stmt.catch_blocks[0].exception_type == "NetworkError"


def test_ir_assignment():
    """Test IRAssignment statement."""
    assignment = IRAssignment(
        target="user",
        value=IRCall(
            function=IRPropertyAccess(
                object=IRIdentifier(name="database"),
                property="get_user"
            ),
            args=[IRIdentifier(name="user_id")]
        ),
        is_declaration=True
    )

    assert assignment.type == NodeType.ASSIGNMENT
    assert assignment.target == "user"
    assert assignment.is_declaration is True


# ============================================================================
# Test Expression Nodes
# ============================================================================


def test_ir_call():
    """Test IRCall expression."""
    call = IRCall(
        function=IRIdentifier(name="process"),
        args=[
            IRLiteral(value=1, literal_type=LiteralType.INTEGER),
            IRLiteral(value=2, literal_type=LiteralType.INTEGER)
        ],
        kwargs={
            "debug": IRLiteral(value=True, literal_type=LiteralType.BOOLEAN)
        }
    )

    assert call.type == NodeType.CALL
    assert len(call.args) == 2
    assert "debug" in call.kwargs


def test_ir_property_access():
    """Test IRPropertyAccess expression."""
    access = IRPropertyAccess(
        object=IRIdentifier(name="user"),
        property="name"
    )

    assert access.type == NodeType.PROPERTY_ACCESS
    assert access.property == "name"


def test_ir_index():
    """Test IRIndex expression."""
    index = IRIndex(
        object=IRIdentifier(name="arr"),
        index=IRLiteral(value=0, literal_type=LiteralType.INTEGER)
    )

    assert index.type == NodeType.INDEX
    assert isinstance(index.index, IRLiteral)


def test_ir_array():
    """Test IRArray expression."""
    arr = IRArray(
        elements=[
            IRLiteral(value=1, literal_type=LiteralType.INTEGER),
            IRLiteral(value=2, literal_type=LiteralType.INTEGER),
            IRLiteral(value=3, literal_type=LiteralType.INTEGER)
        ]
    )

    assert arr.type == NodeType.ARRAY
    assert len(arr.elements) == 3


def test_ir_map():
    """Test IRMap expression."""
    map_expr = IRMap(
        entries={
            "name": IRLiteral(value="John", literal_type=LiteralType.STRING),
            "age": IRLiteral(value=30, literal_type=LiteralType.INTEGER)
        }
    )

    assert map_expr.type == NodeType.MAP
    assert len(map_expr.entries) == 2
    assert "name" in map_expr.entries


def test_ir_lambda():
    """Test IRLambda expression."""
    lambda_expr = IRLambda(
        params=[IRParameter(name="x", param_type=IRType(name="int"))],
        body=IRBinaryOp(
            op=BinaryOperator.ADD,
            left=IRIdentifier(name="x"),
            right=IRLiteral(value=1, literal_type=LiteralType.INTEGER)
        )
    )

    assert lambda_expr.type == NodeType.LAMBDA
    assert len(lambda_expr.params) == 1
    assert isinstance(lambda_expr.body, IRBinaryOp)


# ============================================================================
# Test Type Nodes
# ============================================================================


def test_ir_type_definition():
    """Test IRTypeDefinition."""
    type_def = IRTypeDefinition(
        name="User",
        fields=[
            IRProperty(name="id", prop_type=IRType(name="string")),
            IRProperty(name="name", prop_type=IRType(name="string")),
            IRProperty(name="age", prop_type=IRType(name="int", is_optional=True))
        ]
    )

    assert type_def.type == NodeType.TYPE_DEFINITION
    assert type_def.name == "User"
    assert len(type_def.fields) == 3
    assert type_def.fields[2].prop_type.is_optional


def test_ir_enum():
    """Test IREnum."""
    enum = IREnum(
        name="Status",
        variants=[
            IREnumVariant(name="pending"),
            IREnumVariant(name="completed"),
            IREnumVariant(name="failed")
        ]
    )

    assert enum.type == NodeType.ENUM
    assert enum.name == "Status"
    assert len(enum.variants) == 3
    assert enum.variants[0].name == "pending"


# ============================================================================
# Test Module Construction
# ============================================================================


def test_ir_module_simple():
    """Test simple IRModule creation."""
    module = IRModule(
        name="test_module",
        version="1.0.0",
        functions=[
            IRFunction(
                name="hello",
                return_type=IRType(name="string"),
                body=[
                    IRReturn(
                        value=IRLiteral(value="Hello, World!", literal_type=LiteralType.STRING)
                    )
                ]
            )
        ]
    )

    assert module.type == NodeType.MODULE
    assert module.name == "test_module"
    assert module.version == "1.0.0"
    assert len(module.functions) == 1


def test_ir_module_complex():
    """Test complex IRModule with multiple components."""
    module = IRModule(
        name="payment_processor",
        version="2.0.0",
        imports=[
            IRImport(module="http_client"),
            IRImport(module="storage", items=["database"])
        ],
        types=[
            IRTypeDefinition(
                name="Payment",
                fields=[
                    IRProperty(name="amount", prop_type=IRType(name="float")),
                    IRProperty(name="currency", prop_type=IRType(name="string"))
                ]
            )
        ],
        enums=[
            IREnum(
                name="PaymentStatus",
                variants=[
                    IREnumVariant(name="pending"),
                    IREnumVariant(name="completed")
                ]
            )
        ],
        functions=[
            IRFunction(
                name="process_payment",
                params=[
                    IRParameter(name="amount", param_type=IRType(name="float"))
                ],
                return_type=IRType(name="string"),
                body=[
                    IRReturn(
                        value=IRLiteral(value="processed", literal_type=LiteralType.STRING)
                    )
                ]
            )
        ]
    )

    assert len(module.imports) == 2
    assert len(module.types) == 1
    assert len(module.enums) == 1
    assert len(module.functions) == 1


# ============================================================================
# Test IR Validation
# ============================================================================


def test_validator_valid_module():
    """Test validator accepts valid module."""
    module = IRModule(
        name="valid_module",
        functions=[
            IRFunction(
                name="add",
                params=[
                    IRParameter(name="a", param_type=IRType(name="int")),
                    IRParameter(name="b", param_type=IRType(name="int"))
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

    # Should not raise
    validate_ir(module)


def test_validator_missing_module_name():
    """Test validator rejects module without name."""
    module = IRModule(name="")

    with pytest.raises(ValidationError, match="must have a name"):
        validate_ir(module)


def test_validator_duplicate_function():
    """Test validator rejects duplicate function names."""
    module = IRModule(
        name="test",
        functions=[
            IRFunction(name="foo", body=[]),
            IRFunction(name="foo", body=[])
        ]
    )

    with pytest.raises(ValidationError, match="Duplicate function"):
        validate_ir(module)


def test_validator_duplicate_type():
    """Test validator rejects duplicate type names."""
    module = IRModule(
        name="test",
        types=[
            IRTypeDefinition(name="User", fields=[]),
            IRTypeDefinition(name="User", fields=[])
        ]
    )

    with pytest.raises(ValidationError, match="Duplicate type"):
        validate_ir(module)


def test_validator_return_outside_function():
    """Test validator rejects return outside function."""
    module = IRModule(
        name="test",
        module_vars=[
            IRReturn(value=IRLiteral(value=42, literal_type=LiteralType.INTEGER))
        ]
    )

    with pytest.raises(ValidationError, match="Return outside of function"):
        validate_ir(module)


def test_validator_break_outside_loop():
    """Test validator rejects break outside loop."""
    module = IRModule(
        name="test",
        functions=[
            IRFunction(
                name="test",
                body=[IRBreak()]
            )
        ]
    )

    with pytest.raises(ValidationError, match="Break outside of loop"):
        validate_ir(module)


def test_validator_continue_outside_loop():
    """Test validator rejects continue outside loop."""
    module = IRModule(
        name="test",
        functions=[
            IRFunction(
                name="test",
                body=[IRContinue()]
            )
        ]
    )

    with pytest.raises(ValidationError, match="Continue outside of loop"):
        validate_ir(module)


def test_validator_valid_loop_control():
    """Test validator accepts break/continue inside loops."""
    module = IRModule(
        name="test",
        functions=[
            IRFunction(
                name="test",
                body=[
                    IRFor(
                        iterator="i",
                        iterable=IRIdentifier(name="items"),
                        body=[
                            IRIf(
                                condition=IRBinaryOp(
                                    op=BinaryOperator.EQUAL,
                                    left=IRIdentifier(name="i"),
                                    right=IRLiteral(value=0, literal_type=LiteralType.INTEGER)
                                ),
                                then_body=[IRContinue()],
                                else_body=[]
                            ),
                            IRIf(
                                condition=IRBinaryOp(
                                    op=BinaryOperator.GREATER_THAN,
                                    left=IRIdentifier(name="i"),
                                    right=IRLiteral(value=10, literal_type=LiteralType.INTEGER)
                                ),
                                then_body=[IRBreak()],
                                else_body=[]
                            )
                        ]
                    )
                ]
            )
        ]
    )

    # Should not raise
    validate_ir(module)


def test_validator_warnings():
    """Test validator generates warnings for undefined identifiers."""
    module = IRModule(
        name="test",
        functions=[
            IRFunction(
                name="test",
                body=[
                    IRCall(
                        function=IRIdentifier(name="undefined_function"),
                        args=[]
                    )
                ]
            )
        ]
    )

    validator = IRValidator()
    validator.validate(module, strict=False)

    # Should have warnings about undefined function
    assert len(validator.warnings) > 0


# ============================================================================
# Test Complete IR Tree
# ============================================================================


def test_complete_ir_tree():
    """Test building a complete IR tree for a realistic example."""
    # Build a module that implements a simple user service
    module = IRModule(
        name="user_service",
        version="1.0.0",
        imports=[
            IRImport(module="database"),
            IRImport(module="validation")
        ],
        types=[
            IRTypeDefinition(
                name="User",
                fields=[
                    IRProperty(name="id", prop_type=IRType(name="string")),
                    IRProperty(name="email", prop_type=IRType(name="string")),
                    IRProperty(name="age", prop_type=IRType(name="int", is_optional=True))
                ]
            )
        ],
        enums=[
            IREnum(
                name="UserRole",
                variants=[
                    IREnumVariant(name="admin"),
                    IREnumVariant(name="user"),
                    IREnumVariant(name="guest")
                ]
            )
        ],
        functions=[
            IRFunction(
                name="get_user",
                params=[
                    IRParameter(name="user_id", param_type=IRType(name="string"))
                ],
                return_type=IRType(name="User", is_optional=True),
                throws=["ValidationError", "DatabaseError"],
                body=[
                    # Validate input
                    IRIf(
                        condition=IRBinaryOp(
                            op=BinaryOperator.EQUAL,
                            left=IRIdentifier(name="user_id"),
                            right=IRLiteral(value="", literal_type=LiteralType.STRING)
                        ),
                        then_body=[
                            IRThrow(
                                exception=IRCall(
                                    function=IRIdentifier(name="ValidationError"),
                                    args=[
                                        IRLiteral(
                                            value="User ID cannot be empty",
                                            literal_type=LiteralType.STRING
                                        )
                                    ]
                                )
                            )
                        ]
                    ),
                    # Try to fetch user
                    IRTry(
                        try_body=[
                            IRAssignment(
                                target="user",
                                value=IRCall(
                                    function=IRPropertyAccess(
                                        object=IRIdentifier(name="database"),
                                        property="query"
                                    ),
                                    args=[IRIdentifier(name="user_id")]
                                )
                            ),
                            IRReturn(value=IRIdentifier(name="user"))
                        ],
                        catch_blocks=[
                            IRCatch(
                                exception_type="DatabaseError",
                                exception_var="e",
                                body=[
                                    IRCall(
                                        function=IRIdentifier(name="log_error"),
                                        args=[IRIdentifier(name="e")]
                                    ),
                                    IRReturn(
                                        value=IRLiteral(value=None, literal_type=LiteralType.NULL)
                                    )
                                ]
                            )
                        ]
                    )
                ]
            )
        ]
    )

    # Validate the module
    validate_ir(module)

    # Assertions
    assert module.name == "user_service"
    assert len(module.imports) == 2
    assert len(module.types) == 1
    assert len(module.enums) == 1
    assert len(module.functions) == 1

    # Check function structure
    func = module.functions[0]
    assert func.name == "get_user"
    assert len(func.params) == 1
    assert func.return_type.is_optional
    assert "ValidationError" in func.throws
    assert len(func.body) == 2  # if statement + try/catch


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
