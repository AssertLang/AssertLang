"""
Test Bug #2: Verify that JavaScript uses 'constructor' not '__init__'
"""

import sys
from pathlib import Path

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from dsl.ir import (
    IRModule, IRClass, IRFunction, IRParameter, IRType, IRProperty,
    IRAssignment, IRPropertyAccess, IRIdentifier
)
from language.javascript_generator import generate_javascript

print("="*80)
print("BUG #2 TEST: JavaScript Constructor Naming")
print("="*80)

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

print("\nGenerated JavaScript:")
print("-"*80)
print(js_code)
print("-"*80)

# Check for the bug
print("\nChecking for Bug #2...")
if "constructor(width, height)" in js_code:
    print("✅ PASS: Uses 'constructor' keyword")
    has_constructor = True
else:
    print("❌ FAIL: Does NOT use 'constructor' keyword")
    has_constructor = False

if "__init__(width, height)" in js_code or "__init__ (width, height)" in js_code:
    print("❌ FAIL: Still uses '__init__' method name")
    has_init = True
else:
    print("✅ PASS: Does NOT use '__init__' method name")
    has_init = False

print("\n" + "="*80)
if has_constructor and not has_init:
    print("✅ BUG #2 FIXED: JavaScript correctly uses 'constructor'")
    sys.exit(0)
else:
    print("❌ BUG #2 PRESENT: JavaScript uses '__init__' instead of 'constructor'")
    print("\nThis means:")
    print("  - new VideoSpec(width, height) creates an empty object")
    print("  - Properties remain undefined")
    print("  - Classes are BROKEN in JavaScript")
    sys.exit(1)
