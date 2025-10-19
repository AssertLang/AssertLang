"""
Test suite for transpiler bug fixes in v0.1.1

Tests all 6 critical bugs:
1. JavaScript module.exports missing
2. JavaScript __init__ not converted to constructor (handled by IR)
3. JavaScript self not converted to this
4. JavaScript Python builtins not mapped
5. JavaScript missing 'new' keyword for constructors
6. Python constructor calls using field_0= instead of positional args
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from dsl.ir import (
    IRModule, IRClass, IRFunction, IRParameter, IRType, IRProperty,
    IRReturn, IRAssignment, IRPropertyAccess, IRIdentifier, IRCall,
    IRBinaryOp, BinaryOperator, IRLiteral, LiteralType
)
from language.javascript_generator import generate_javascript
from language.python_generator_v2 import generate_python


def test_bug_3_self_to_this():
    """Bug #3: JavaScript should convert 'self' to 'this'"""
    # Create a simple class with property access
    module = IRModule(
        name="test",
        classes=[
            IRClass(
                name="VideoSpec",
                properties=[
                    IRProperty(name="width", prop_type=IRType(name="int"))
                ],
                constructor=IRFunction(
                    name="__init__",
                    params=[IRParameter(name="width", param_type=IRType(name="int"))],
                    body=[
                        IRAssignment(
                            target=IRPropertyAccess(
                                object=IRIdentifier(name="self"),
                                property="width"
                            ),
                            value=IRIdentifier(name="width")
                        )
                    ]
                ),
                methods=[
                    IRFunction(
                        name="getWidth",
                        params=[],
                        return_type=IRType(name="int"),
                        body=[
                            IRReturn(
                                value=IRPropertyAccess(
                                    object=IRIdentifier(name="self"),
                                    property="width"
                                )
                            )
                        ]
                    )
                ]
            )
        ]
    )

    js_code = generate_javascript(module)

    # Bug #3 check: Should use 'this.width' not 'self.width'
    assert "this.width" in js_code, "Bug #3 FAILED: JavaScript should use 'this', not 'self'"
    assert "self.width" not in js_code, "Bug #3 FAILED: JavaScript contains 'self' instead of 'this'"
    print("✓ Bug #3 FIXED: JavaScript correctly uses 'this' instead of 'self'")


def test_bug_4_builtin_mapping():
    """Bug #4: JavaScript should map Python builtins (str, int, float, len)"""
    # Create function that uses Python builtins
    module = IRModule(
        name="test",
        functions=[
            IRFunction(
                name="testBuiltins",
                params=[
                    IRParameter(name="x", param_type=IRType(name="int")),
                    IRParameter(name="text", param_type=IRType(name="string"))
                ],
                return_type=IRType(name="string"),
                body=[
                    IRReturn(
                        value=IRCall(
                            function=IRIdentifier(name="str"),
                            args=[
                                IRCall(
                                    function=IRIdentifier(name="int"),
                                    args=[
                                        IRCall(
                                            function=IRIdentifier(name="float"),
                                            args=[IRIdentifier(name="x")]
                                        )
                                    ]
                                )
                            ]
                        )
                    )
                ]
            )
        ]
    )

    js_code = generate_javascript(module)

    # Bug #4 checks
    assert "String(" in js_code, "Bug #4 FAILED: str() should map to String()"
    assert "Math.floor(" in js_code, "Bug #4 FAILED: int() should map to Math.floor()"
    assert "Number(" in js_code, "Bug #4 FAILED: float() should map to Number()"
    assert "str(" not in js_code, "Bug #4 FAILED: Python 'str()' should be converted"
    assert "int(" not in js_code, "Bug #4 FAILED: Python 'int()' should be converted"
    print("✓ Bug #4 FIXED: JavaScript correctly maps Python builtins (str→String, int→Math.floor, float→Number)")


def test_bug_5_new_keyword():
    """Bug #5: JavaScript should use 'new' keyword for class instantiation"""
    # Create a factory function that instantiates a class
    module = IRModule(
        name="test",
        classes=[
            IRClass(
                name="VideoSpec",
                constructor=IRFunction(
                    name="__init__",
                    params=[IRParameter(name="width", param_type=IRType(name="int"))],
                    body=[]
                )
            )
        ],
        functions=[
            IRFunction(
                name="createVideoSpec",
                params=[IRParameter(name="width", param_type=IRType(name="int"))],
                return_type=IRType(name="VideoSpec"),
                body=[
                    IRReturn(
                        value=IRCall(
                            function=IRIdentifier(name="VideoSpec"),
                            args=[IRIdentifier(name="width")]
                        )
                    )
                ]
            )
        ]
    )

    js_code = generate_javascript(module)

    # Bug #5 check
    assert "new VideoSpec" in js_code, "Bug #5 FAILED: JavaScript should use 'new' keyword for class instantiation"
    assert "return new VideoSpec(width)" in js_code, "Bug #5 FAILED: Constructor call should use 'new'"
    print("✓ Bug #5 FIXED: JavaScript correctly uses 'new' keyword for class instantiation")


def test_bug_1_module_exports():
    """Bug #1: JavaScript should include module.exports statement"""
    # Create module with function and class
    module = IRModule(
        name="test",
        classes=[
            IRClass(name="MyClass", constructor=IRFunction(name="__init__", params=[], body=[]))
        ],
        functions=[
            IRFunction(name="myFunction", params=[], body=[])
        ]
    )

    js_code = generate_javascript(module)

    # Bug #1 checks
    assert "module.exports" in js_code, "Bug #1 FAILED: JavaScript should have module.exports"
    assert "MyClass" in js_code.split("module.exports")[1], "Bug #1 FAILED: MyClass should be exported"
    assert "myFunction" in js_code.split("module.exports")[1], "Bug #1 FAILED: myFunction should be exported"
    print("✓ Bug #1 FIXED: JavaScript correctly includes module.exports with all top-level symbols")


def test_bug_6_python_positional_args():
    """Bug #6: Python should use positional args, not field_0= for constructors"""
    # Create a class and factory function
    module = IRModule(
        name="test",
        classes=[
            IRClass(
                name="VideoSpec",
                constructor=IRFunction(
                    name="__init__",
                    params=[
                        IRParameter(name="width", param_type=IRType(name="int")),
                        IRParameter(name="height", param_type=IRType(name="int"))
                    ],
                    body=[]
                )
            )
        ],
        functions=[
            IRFunction(
                name="createVideoSpec",
                params=[
                    IRParameter(name="width", param_type=IRType(name="int")),
                    IRParameter(name="height", param_type=IRType(name="int"))
                ],
                return_type=IRType(name="VideoSpec"),
                body=[
                    IRReturn(
                        value=IRCall(
                            function=IRIdentifier(name="VideoSpec"),
                            args=[
                                IRIdentifier(name="width"),
                                IRIdentifier(name="height")
                            ]
                        )
                    )
                ]
            )
        ]
    )

    py_code = generate_python(module)

    # Bug #6 checks
    assert "VideoSpec(width, height)" in py_code, "Bug #6 FAILED: Python should use positional arguments"
    assert "field_0=" not in py_code, "Bug #6 FAILED: Python should NOT use field_0= syntax"
    assert "field_1=" not in py_code, "Bug #6 FAILED: Python should NOT use field_1= syntax"
    print("✓ Bug #6 FIXED: Python correctly uses positional arguments for constructors")


def run_all_tests():
    """Run all bug fix tests"""
    print("\n" + "="*80)
    print("ASSERTLANG v0.1.1 BUG FIX TEST SUITE")
    print("="*80 + "\n")

    tests = [
        test_bug_3_self_to_this,
        test_bug_4_builtin_mapping,
        test_bug_5_new_keyword,
        test_bug_1_module_exports,
        test_bug_6_python_positional_args,
    ]

    passed = 0
    failed = 0

    for test in tests:
        try:
            test()
            passed += 1
        except AssertionError as e:
            print(f"✗ {test.__name__} FAILED: {e}")
            failed += 1
        except Exception as e:
            print(f"✗ {test.__name__} ERROR: {e}")
            failed += 1

    print("\n" + "="*80)
    print(f"TEST RESULTS: {passed} passed, {failed} failed")
    print("="*80 + "\n")

    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
