"""
Test Bug #2: Verify that JavaScript uses 'constructor' not '__init__'
"""

from dsl.ir import (
    IRModule, IRClass, IRFunction, IRParameter, IRType, IRProperty,
    IRAssignment, IRPropertyAccess, IRIdentifier
)
from language.javascript_generator import generate_javascript


def test_javascript_constructor_naming():
    """Verify that JavaScript uses 'constructor' keyword, not '__init__' method name."""

    # Create a simple class with constructor
    module = IRModule(
        name="test",
        classes=[
            IRClass(
                name="VideoSpec",
                properties=[
                    IRProperty(name="width", prop_type=IRType(name="int")),
                    IRProperty(name="height", prop_type=IRType(name="int"))
                ],
                constructor=IRFunction(
                    name="__init__",
                    params=[
                        IRParameter(name="width", param_type=IRType(name="int")),
                        IRParameter(name="height", param_type=IRType(name="int"))
                    ],
                    body=[
                        IRAssignment(
                            target=IRPropertyAccess(object=IRIdentifier(name="self"), property="width"),
                            value=IRIdentifier(name="width")
                        ),
                        IRAssignment(
                            target=IRPropertyAccess(object=IRIdentifier(name="self"), property="height"),
                            value=IRIdentifier(name="height")
                        )
                    ]
                )
            )
        ]
    )

    js_code = generate_javascript(module)

    # Verify it uses 'constructor' keyword
    assert "constructor(width, height)" in js_code, (
        "JavaScript should use 'constructor' keyword, not '__init__'"
    )

    # Verify it does NOT use '__init__' method name
    assert "__init__(width, height)" not in js_code, (
        "JavaScript should NOT use '__init__' method name"
    )
    assert "__init__ (width, height)" not in js_code, (
        "JavaScript should NOT use '__init__' method name (with space)"
    )
