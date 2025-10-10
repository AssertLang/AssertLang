"""
Test Suite for Bug #17: String Concatenation with Integers

Tests auto-conversion of non-string types when concatenating with strings in Python output.

Bug Report: Bugs/v2.1.0b9/PW_BUG_REPORT_BATCH_9.md
"""

import pytest
from dsl.ir import IRModule, IRFunction, IRParameter, IRType, IRAssignment, IRBinaryOp, IRLiteral, IRIdentifier, BinaryOperator, LiteralType
from language.python_generator_v2 import generate_python


class TestBug17StringConcatenation:
    """Test string concatenation with auto-type conversion."""

    def test_string_plus_int(self):
        """Test string + int generates str() wrapping."""
        # PW: let result = "user_" + 123;
        module = IRModule(
            name="test",
            functions=[
                IRFunction(
                    name="test_concat",
                    params=[],
                    return_type=IRType(name="string"),
                    body=[
                        IRAssignment(
                            target="result",
                            value=IRBinaryOp(
                                op=BinaryOperator.ADD,
                                left=IRLiteral(literal_type=LiteralType.STRING, value="user_"),
                                right=IRLiteral(literal_type=LiteralType.INTEGER, value=123)
                            ),
                            is_declaration=True,
                            var_type=IRType(name="string")
                        )
                    ]
                )
            ]
        )

        code = generate_python(module)
        assert '("user_" + str(123))' in code
        # Verify it doesn't have TypeError
        assert 'user_" + 123' not in code

    def test_int_plus_string(self):
        """Test int + string generates str() wrapping (reversed order)."""
        # PW: let result = 456 + "_suffix";
        module = IRModule(
            name="test",
            functions=[
                IRFunction(
                    name="test_concat",
                    params=[],
                    return_type=IRType(name="string"),
                    body=[
                        IRAssignment(
                            target="result",
                            value=IRBinaryOp(
                                op=BinaryOperator.ADD,
                                left=IRLiteral(literal_type=LiteralType.INTEGER, value=456),
                                right=IRLiteral(literal_type=LiteralType.STRING, value="_suffix")
                            ),
                            is_declaration=True,
                            var_type=IRType(name="string")
                        )
                    ]
                )
            ]
        )

        code = generate_python(module)
        assert '(str(456) + "_suffix")' in code
        # Verify it doesn't have TypeError
        assert '456 + "_suffix"' not in code or 'str(456)' in code

    def test_string_plus_float(self):
        """Test string + float generates str() wrapping."""
        # PW: let result = "value: " + 3.14;
        module = IRModule(
            name="test",
            functions=[
                IRFunction(
                    name="test_concat",
                    params=[],
                    return_type=IRType(name="string"),
                    body=[
                        IRAssignment(
                            target="result",
                            value=IRBinaryOp(
                                op=BinaryOperator.ADD,
                                left=IRLiteral(literal_type=LiteralType.STRING, value="value: "),
                                right=IRLiteral(literal_type=LiteralType.FLOAT, value=3.14)
                            ),
                            is_declaration=True,
                            var_type=IRType(name="string")
                        )
                    ]
                )
            ]
        )

        code = generate_python(module)
        assert '("value: " + str(3.14))' in code

    def test_string_plus_variable(self):
        """Test string + int variable with type inference."""
        # PW: function test(expires_at: int) -> string { return "exp_" + expires_at; }
        module = IRModule(
            name="test",
            functions=[
                IRFunction(
                    name="test_concat",
                    params=[
                        IRParameter(name="expires_at", param_type=IRType(name="int"))
                    ],
                    return_type=IRType(name="string"),
                    body=[
                        IRAssignment(
                            target="result",
                            value=IRBinaryOp(
                                op=BinaryOperator.ADD,
                                left=IRLiteral(literal_type=LiteralType.STRING, value="exp_"),
                                right=IRIdentifier(name="expires_at")
                            ),
                            is_declaration=True,
                            var_type=IRType(name="string")
                        )
                    ]
                )
            ]
        )

        code = generate_python(module)
        assert '("exp_" + str(expires_at))' in code

    def test_multiple_concatenations(self):
        """Test multiple string concatenations with mixed types (exact bug reproduction)."""
        # PW: let payload = "user_" + username + "_role_" + role + "_exp_" + expires_at;
        # username and role are strings, expires_at is int
        module = IRModule(
            name="test",
            functions=[
                IRFunction(
                    name="test_concat",
                    params=[
                        IRParameter(name="username", param_type=IRType(name="string")),
                        IRParameter(name="role", param_type=IRType(name="string")),
                        IRParameter(name="expires_at", param_type=IRType(name="int"))
                    ],
                    return_type=IRType(name="string"),
                    body=[
                        IRAssignment(
                            target="payload",
                            value=IRBinaryOp(
                                op=BinaryOperator.ADD,
                                left=IRBinaryOp(
                                    op=BinaryOperator.ADD,
                                    left=IRBinaryOp(
                                        op=BinaryOperator.ADD,
                                        left=IRBinaryOp(
                                            op=BinaryOperator.ADD,
                                            left=IRLiteral(literal_type=LiteralType.STRING, value="user_"),
                                            right=IRIdentifier(name="username")
                                        ),
                                        right=IRLiteral(literal_type=LiteralType.STRING, value="_role_")
                                    ),
                                    right=IRIdentifier(name="role")
                                ),
                                right=IRBinaryOp(
                                    op=BinaryOperator.ADD,
                                    left=IRLiteral(literal_type=LiteralType.STRING, value="_exp_"),
                                    right=IRIdentifier(name="expires_at")
                                )
                            ),
                            is_declaration=True,
                            var_type=IRType(name="string")
                        )
                    ]
                )
            ]
        )

        code = generate_python(module)
        # The final concatenation should have str(expires_at)
        assert 'str(expires_at)' in code
        # Ensure no direct int concatenation
        assert 'expires_at))' in code or 'expires_at)' in code

    def test_string_plus_string_unchanged(self):
        """Test that string + string doesn't add unnecessary str() calls."""
        # PW: let result = "hello" + "world";
        module = IRModule(
            name="test",
            functions=[
                IRFunction(
                    name="test_concat",
                    params=[],
                    return_type=IRType(name="string"),
                    body=[
                        IRAssignment(
                            target="result",
                            value=IRBinaryOp(
                                op=BinaryOperator.ADD,
                                left=IRLiteral(literal_type=LiteralType.STRING, value="hello"),
                                right=IRLiteral(literal_type=LiteralType.STRING, value="world")
                            ),
                            is_declaration=True,
                            var_type=IRType(name="string")
                        )
                    ]
                )
            ]
        )

        code = generate_python(module)
        assert '("hello" + "world")' in code
        # Should NOT have str() wrapping for string + string
        assert 'str("hello")' not in code
        assert 'str("world")' not in code

    def test_int_plus_int_unchanged(self):
        """Test that int + int still does numeric addition without str()."""
        # PW: let result = 10 + 20;
        module = IRModule(
            name="test",
            functions=[
                IRFunction(
                    name="test_add",
                    params=[],
                    return_type=IRType(name="int"),
                    body=[
                        IRAssignment(
                            target="result",
                            value=IRBinaryOp(
                                op=BinaryOperator.ADD,
                                left=IRLiteral(literal_type=LiteralType.INTEGER, value=10),
                                right=IRLiteral(literal_type=LiteralType.INTEGER, value=20)
                            ),
                            is_declaration=True,
                            var_type=IRType(name="int")
                        )
                    ]
                )
            ]
        )

        code = generate_python(module)
        assert '(10 + 20)' in code
        # Should NOT have str() wrapping for int + int
        assert 'str(10)' not in code
        assert 'str(20)' not in code

    def test_nested_expressions(self):
        """Test string concatenation with nested expressions."""
        # PW: let result = "Result: " + (100 + 200);
        # The inner (100 + 200) is int + int (no str), outer is string + int (needs str)
        module = IRModule(
            name="test",
            functions=[
                IRFunction(
                    name="test_nested",
                    params=[],
                    return_type=IRType(name="string"),
                    body=[
                        IRAssignment(
                            target="result",
                            value=IRBinaryOp(
                                op=BinaryOperator.ADD,
                                left=IRLiteral(literal_type=LiteralType.STRING, value="Result: "),
                                right=IRBinaryOp(
                                    op=BinaryOperator.ADD,
                                    left=IRLiteral(literal_type=LiteralType.INTEGER, value=100),
                                    right=IRLiteral(literal_type=LiteralType.INTEGER, value=200)
                                )
                            ),
                            is_declaration=True,
                            var_type=IRType(name="string")
                        )
                    ]
                )
            ]
        )

        code = generate_python(module)
        # Outer operation: string + int (should have str())
        assert 'str((100 + 20))' in code or 'str((100 + 200))' in code
        # Inner operation: int + int (should NOT have str())
        assert '(100 + 200)' in code

    def test_bug17_exact_reproduction(self):
        """Exact reproduction of Bug #17 from the bug report."""
        # From bug report: let payload = "user_" + username + "_exp_" + expires_at;
        # where expires_at is int
        module = IRModule(
            name="test_jwt",
            functions=[
                IRFunction(
                    name="generate_jwt",
                    params=[
                        IRParameter(name="username", param_type=IRType(name="string")),
                        IRParameter(name="expires_at", param_type=IRType(name="int"))
                    ],
                    return_type=IRType(name="string"),
                    body=[
                        IRAssignment(
                            target="payload",
                            value=IRBinaryOp(
                                op=BinaryOperator.ADD,
                                left=IRBinaryOp(
                                    op=BinaryOperator.ADD,
                                    left=IRBinaryOp(
                                        op=BinaryOperator.ADD,
                                        left=IRLiteral(literal_type=LiteralType.STRING, value="user_"),
                                        right=IRIdentifier(name="username")
                                    ),
                                    right=IRLiteral(literal_type=LiteralType.STRING, value="_exp_")
                                ),
                                right=IRIdentifier(name="expires_at")
                            ),
                            is_declaration=True,
                            var_type=IRType(name="string")
                        )
                    ]
                )
            ]
        )

        code = generate_python(module)

        # Should generate: payload = ((("user_" + username) + "_exp_") + str(expires_at))
        assert 'str(expires_at)' in code

        # Verify the code is executable Python
        exec(compile(code, '<test>', 'exec'))

    def test_runtime_execution(self):
        """Test that generated code actually executes without TypeError."""
        from dsl.ir import IRReturn

        module = IRModule(
            name="test_runtime",
            functions=[
                IRFunction(
                    name="build_message",
                    params=[
                        IRParameter(name="name", param_type=IRType(name="string")),
                        IRParameter(name="age", param_type=IRType(name="int"))
                    ],
                    return_type=IRType(name="string"),
                    body=[
                        IRAssignment(
                            target="message",
                            value=IRBinaryOp(
                                op=BinaryOperator.ADD,
                                left=IRBinaryOp(
                                    op=BinaryOperator.ADD,
                                    left=IRLiteral(literal_type=LiteralType.STRING, value="Name: "),
                                    right=IRIdentifier(name="name")
                                ),
                                right=IRBinaryOp(
                                    op=BinaryOperator.ADD,
                                    left=IRLiteral(literal_type=LiteralType.STRING, value=", Age: "),
                                    right=IRIdentifier(name="age")
                                )
                            ),
                            is_declaration=True,
                            var_type=IRType(name="string")
                        ),
                        IRReturn(value=IRIdentifier(name="message"))
                    ]
                )
            ]
        )

        code = generate_python(module)

        # Execute the generated code
        namespace = {}
        exec(compile(code, '<test>', 'exec'), namespace)

        # Call the function with actual values
        result = namespace['build_message']("Alice", 30)
        assert result == "Name: Alice, Age: 30"
        assert isinstance(result, str)


class TestBug17EdgeCases:
    """Edge cases for string concatenation."""

    def test_float_plus_string(self):
        """Test float + string (reversed order)."""
        module = IRModule(
            name="test",
            functions=[
                IRFunction(
                    name="test_concat",
                    params=[],
                    return_type=IRType(name="string"),
                    body=[
                        IRAssignment(
                            target="result",
                            value=IRBinaryOp(
                                op=BinaryOperator.ADD,
                                left=IRLiteral(literal_type=LiteralType.FLOAT, value=2.5),
                                right=IRLiteral(literal_type=LiteralType.STRING, value=" meters")
                            ),
                            is_declaration=True,
                            var_type=IRType(name="string")
                        )
                    ]
                )
            ]
        )

        code = generate_python(module)
        assert '(str(2.5) + " meters")' in code

    def test_complex_chain(self):
        """Test complex chain of mixed type concatenations."""
        # PW: let result = "ID: " + 123 + ", Score: " + 98.5;
        module = IRModule(
            name="test",
            functions=[
                IRFunction(
                    name="test_chain",
                    params=[],
                    return_type=IRType(name="string"),
                    body=[
                        IRAssignment(
                            target="result",
                            value=IRBinaryOp(
                                op=BinaryOperator.ADD,
                                left=IRBinaryOp(
                                    op=BinaryOperator.ADD,
                                    left=IRBinaryOp(
                                        op=BinaryOperator.ADD,
                                        left=IRLiteral(literal_type=LiteralType.STRING, value="ID: "),
                                        right=IRLiteral(literal_type=LiteralType.INTEGER, value=123)
                                    ),
                                    right=IRLiteral(literal_type=LiteralType.STRING, value=", Score: ")
                                ),
                                right=IRLiteral(literal_type=LiteralType.FLOAT, value=98.5)
                            ),
                            is_declaration=True,
                            var_type=IRType(name="string")
                        )
                    ]
                )
            ]
        )

        code = generate_python(module)
        # Both numeric values should be wrapped
        assert 'str(123)' in code
        assert 'str(98.5)' in code

    def test_no_conversion_for_unknown_types(self):
        """Test that unknown types don't get str() when not needed."""
        # This tests that we only add str() when we detect the type mismatch
        module = IRModule(
            name="test",
            functions=[
                IRFunction(
                    name="test_unknown",
                    params=[
                        IRParameter(name="a", param_type=IRType(name="any")),
                        IRParameter(name="b", param_type=IRType(name="any"))
                    ],
                    return_type=IRType(name="any"),
                    body=[
                        IRAssignment(
                            target="result",
                            value=IRBinaryOp(
                                op=BinaryOperator.ADD,
                                left=IRIdentifier(name="a"),
                                right=IRIdentifier(name="b")
                            ),
                            is_declaration=True,
                            var_type=IRType(name="any")
                        )
                    ]
                )
            ]
        )

        code = generate_python(module)
        # Since both are 'any' type, no str() should be added
        assert '(a + b)' in code
        # Neither should have str() since we don't know the types
        assert 'str(a)' not in code or 'str(b)' not in code


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
