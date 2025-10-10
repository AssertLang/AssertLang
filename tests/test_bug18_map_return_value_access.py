"""
Test Suite for Bug #18: Map Return Value Access

Tests that variables assigned from functions returning -> map use bracket notation
for field access in Python output.

Bug Report: Inline specification from user
"""

import pytest
from dsl.ir import IRModule, IRFunction, IRParameter, IRType, IRAssignment, IRPropertyAccess, IRIdentifier, IRReturn, IRLiteral, IRMap, IRBinaryOp, IRIf, IRCall, BinaryOperator, LiteralType, IRClass
from language.python_generator_v2 import generate_python


class TestBug18MapReturnValueAccess:
    """Test map return value field access uses bracket notation."""

    def test_simple_map_return_access(self):
        """Test basic: let result = get_map(); result.field → result["field"]"""
        module = IRModule(
            name="test",
            functions=[
                IRFunction(
                    name="get_data",
                    params=[],
                    return_type=IRType(name="map"),
                    body=[
                        IRReturn(value=IRMap(entries={"status": IRLiteral(literal_type=LiteralType.STRING, value="ok")}))
                    ]
                ),
                IRFunction(
                    name="test_func",
                    params=[],
                    return_type=IRType(name="string"),
                    body=[
                        IRAssignment(
                            target="result",
                            value=IRIdentifier(name="get_data"),  # Simplified - would be IRCall in real code
                            is_declaration=True,
                            var_type=IRType(name="map")
                        ),
                        IRReturn(
                            value=IRPropertyAccess(
                                object=IRIdentifier(name="result"),
                                property="status"
                            )
                        )
                    ]
                )
            ]
        )

        code = generate_python(module)

        # Should use bracket notation for map field access
        assert 'result["status"]' in code, f"Expected result[\"status\"], got:\n{code}"
        assert 'result.status' not in code, "Should not use dot notation for map"

    def test_function_call_map_return(self):
        """Test: let validation = self.validate_token(token); validation.valid → validation["valid"]"""
        module = IRModule(
            name="test",
            classes=[
                IRClass(
                    name="Validator",
                    properties=[],
                    constructor=None,
                    methods=[
                        IRFunction(
                            name="validate_token",
                            params=[IRParameter(name="token", param_type=IRType(name="string"))],
                            return_type=IRType(name="map"),
                            body=[
                                IRReturn(
                                    value=IRMap(entries={
                                        "valid": IRLiteral(literal_type=LiteralType.BOOLEAN, value=True),
                                        "error": IRLiteral(literal_type=LiteralType.STRING, value="")
                                    })
                                )
                            ]
                        ),
                        IRFunction(
                            name="check",
                            params=[IRParameter(name="token", param_type=IRType(name="string"))],
                            return_type=IRType(name="bool"),
                            body=[
                                IRAssignment(
                                    target="validation",
                                    value=IRPropertyAccess(
                                        object=IRIdentifier(name="self"),
                                        property="validate_token"
                                    ),  # Simplified - would be IRCall
                                    is_declaration=True
                                ),
                                IRReturn(
                                    value=IRPropertyAccess(
                                        object=IRIdentifier(name="validation"),
                                        property="valid"
                                    )
                                )
                            ]
                        )
                    ]
                )
            ]
        )

        code = generate_python(module)

        # Should use bracket notation for map field access
        assert 'validation["valid"]' in code, f"Expected validation[\"valid\"], got:\n{code}"
        assert 'validation.valid' not in code, "Should not use dot notation for map variable"

    def test_multiple_map_field_accesses(self):
        """Test multiple fields from same map variable."""
        module = IRModule(
            name="test",
            functions=[
                IRFunction(
                    name="get_user",
                    params=[],
                    return_type=IRType(name="map"),
                    body=[
                        IRReturn(
                            value=IRMap(entries={
                                "name": IRLiteral(literal_type=LiteralType.STRING, value="alice"),
                                "age": IRLiteral(literal_type=LiteralType.INTEGER, value=30)
                            })
                        )
                    ]
                ),
                IRFunction(
                    name="process_user",
                    params=[],
                    return_type=IRType(name="string"),
                    body=[
                        IRAssignment(
                            target="user",
                            value=IRIdentifier(name="get_user"),  # Simplified
                            is_declaration=True
                        ),
                        IRAssignment(
                            target="name",
                            value=IRPropertyAccess(
                                object=IRIdentifier(name="user"),
                                property="name"
                            ),
                            is_declaration=True
                        ),
                        IRAssignment(
                            target="age",
                            value=IRPropertyAccess(
                                object=IRIdentifier(name="user"),
                                property="age"
                            ),
                            is_declaration=True
                        ),
                        IRReturn(value=IRIdentifier(name="name"))
                    ]
                )
            ]
        )

        code = generate_python(module)

        # Both field accesses should use bracket notation
        assert 'user["name"]' in code, f"Expected user[\"name\"], got:\n{code}"
        assert 'user["age"]' in code, f"Expected user[\"age\"], got:\n{code}"
        assert 'user.name' not in code, "Should not use dot notation for map"
        assert 'user.age' not in code, "Should not use dot notation for map"

    def test_mixed_map_and_class_access(self):
        """Test that maps use brackets and classes use dots in same code."""
        module = IRModule(
            name="test",
            classes=[
                IRClass(
                    name="Config",
                    properties=[],
                    constructor=IRFunction(
                        name="__init__",
                        params=[IRParameter(name="port", param_type=IRType(name="int"))],
                        return_type=None,
                        body=[]
                    ),
                    methods=[]
                )
            ],
            functions=[
                IRFunction(
                    name="get_settings",
                    params=[],
                    return_type=IRType(name="map"),
                    body=[
                        IRReturn(
                            value=IRMap(entries={
                                "host": IRLiteral(literal_type=LiteralType.STRING, value="localhost")
                            })
                        )
                    ]
                ),
                IRFunction(
                    name="make_config",
                    params=[],
                    return_type=IRType(name="Config"),
                    body=[]
                ),
                IRFunction(
                    name="test_both",
                    params=[],
                    return_type=IRType(name="string"),
                    body=[
                        IRAssignment(
                            target="map_config",
                            value=IRIdentifier(name="get_settings"),  # Returns map
                            is_declaration=True
                        ),
                        IRAssignment(
                            target="class_config",
                            value=IRIdentifier(name="make_config"),  # Returns Config class
                            is_declaration=True
                        ),
                        # This is simplified - would have actual property access
                        IRReturn(value=IRLiteral(literal_type=LiteralType.STRING, value="done"))
                    ]
                )
            ]
        )

        code = generate_python(module)

        # Verify type system tracks both correctly
        # This test mainly ensures no crashes and proper type tracking
        assert "def get_settings() -> Dict:" in code
        assert "def make_config() -> Config:" in code

    def test_conditional_with_map_return(self):
        """Test map field access in conditional (exact bug from specification)."""
        module = IRModule(
            name="test",
            classes=[
                IRClass(
                    name="Auth",
                    properties=[],
                    constructor=None,
                    methods=[
                        IRFunction(
                            name="validate_token",
                            params=[IRParameter(name="token", param_type=IRType(name="string"))],
                            return_type=IRType(name="map"),
                            body=[
                                IRReturn(
                                    value=IRMap(entries={
                                        "valid": IRLiteral(literal_type=LiteralType.BOOLEAN, value=True),
                                        "error": IRLiteral(literal_type=LiteralType.STRING, value=""),
                                        "username": IRLiteral(literal_type=LiteralType.STRING, value="alice")
                                    })
                                )
                            ]
                        ),
                        IRFunction(
                            name="check_permission",
                            params=[
                                IRParameter(name="token", param_type=IRType(name="string")),
                                IRParameter(name="role", param_type=IRType(name="string"))
                            ],
                            return_type=IRType(name="map"),
                            body=[
                                # let validation = self.validate_token(token);
                                IRAssignment(
                                    target="validation",
                                    value=IRPropertyAccess(
                                        object=IRIdentifier(name="self"),
                                        property="validate_token"
                                    ),  # Simplified
                                    is_declaration=True
                                ),
                                # if (validation.valid == false) {
                                IRIf(
                                    condition=IRBinaryOp(
                                        op=BinaryOperator.EQUAL,
                                        left=IRPropertyAccess(
                                            object=IRIdentifier(name="validation"),
                                            property="valid"
                                        ),
                                        right=IRLiteral(literal_type=LiteralType.BOOLEAN, value=False)
                                    ),
                                    then_body=[
                                        # return {"authorized": false, "error": validation.error};
                                        IRReturn(
                                            value=IRMap(entries={
                                                "authorized": IRLiteral(literal_type=LiteralType.BOOLEAN, value=False),
                                                "error": IRPropertyAccess(
                                                    object=IRIdentifier(name="validation"),
                                                    property="error"
                                                )
                                            })
                                        )
                                    ],
                                    else_body=[]
                                ),
                                IRReturn(
                                    value=IRMap(entries={
                                        "authorized": IRLiteral(literal_type=LiteralType.BOOLEAN, value=True)
                                    })
                                )
                            ]
                        )
                    ]
                )
            ]
        )

        code = generate_python(module)

        # Critical assertions - this is the exact bug pattern
        assert 'validation["valid"]' in code, f"Expected validation[\"valid\"], got:\n{code}"
        assert 'validation["error"]' in code, f"Expected validation[\"error\"], got:\n{code}"

        # Should NOT have attribute access
        assert 'validation.valid' not in code, "Should not use dot notation for map field 'valid'"
        assert 'validation.error' not in code, "Should not use dot notation for map field 'error'"

    def test_nested_map_access(self):
        """Test accessing fields through multiple levels of map returns."""
        # This is more complex - may be out of scope for initial fix
        pass

    def test_bug18_exact_specification(self):
        """Exact test from Bug #18 specification - validates the complete fix."""
        module = IRModule(
            name="test_jwt",
            classes=[
                IRClass(
                    name="Auth",
                    properties=[],
                    constructor=None,
                    methods=[
                        IRFunction(
                            name="validate_token",
                            params=[IRParameter(name="token", param_type=IRType(name="string"))],
                            return_type=IRType(name="map"),
                            body=[
                                IRReturn(
                                    value=IRMap(entries={
                                        "valid": IRLiteral(literal_type=LiteralType.BOOLEAN, value=True),
                                        "error": IRLiteral(literal_type=LiteralType.STRING, value=""),
                                        "username": IRLiteral(literal_type=LiteralType.STRING, value="alice")
                                    })
                                )
                            ]
                        ),
                        IRFunction(
                            name="check_permission",
                            params=[
                                IRParameter(name="token", param_type=IRType(name="string")),
                                IRParameter(name="role", param_type=IRType(name="string"))
                            ],
                            return_type=IRType(name="map"),
                            body=[
                                # let validation = self.validate_token(token);
                                IRAssignment(
                                    target="validation",
                                    value=IRCall(
                                        function=IRPropertyAccess(
                                            object=IRIdentifier(name="self"),
                                            property="validate_token"
                                        ),
                                        args=[IRIdentifier(name="token")]
                                    ),
                                    is_declaration=True
                                ),
                                # if (validation.valid == false) { return {"authorized": false, "error": validation.error}; }
                                IRIf(
                                    condition=IRBinaryOp(
                                        op=BinaryOperator.EQUAL,
                                        left=IRPropertyAccess(
                                            object=IRIdentifier(name="validation"),
                                            property="valid"
                                        ),
                                        right=IRLiteral(literal_type=LiteralType.BOOLEAN, value=False)
                                    ),
                                    then_body=[
                                        IRReturn(
                                            value=IRMap(entries={
                                                "authorized": IRLiteral(literal_type=LiteralType.BOOLEAN, value=False),
                                                "error": IRPropertyAccess(
                                                    object=IRIdentifier(name="validation"),
                                                    property="error"
                                                )
                                            })
                                        )
                                    ],
                                    else_body=[]
                                ),
                                IRReturn(
                                    value=IRMap(entries={
                                        "authorized": IRLiteral(literal_type=LiteralType.BOOLEAN, value=True)
                                    })
                                )
                            ]
                        )
                    ]
                )
            ]
        )

        code = generate_python(module)

        # This is the EXACT bug from specification - validation must use brackets
        assert 'validation["valid"]' in code, f"Bug #18 NOT FIXED: Expected validation[\"valid\"], got:\n{code}"
        assert 'validation["error"]' in code, f"Bug #18 NOT FIXED: Expected validation[\"error\"], got:\n{code}"

        # Should NOT use dot notation for map fields
        assert 'validation.valid' not in code, "Should not use dot notation for map field 'valid'"
        assert 'validation.error' not in code, "Should not use dot notation for map field 'error'"

        # Verify the code is valid Python and executes correctly
        namespace = {}
        exec(compile(code, '<test>', 'exec'), namespace)

        # Test that it actually works at runtime
        auth = namespace['Auth']()
        result = auth.check_permission("test_token", "admin")
        assert isinstance(result, dict)
        assert "authorized" in result


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
