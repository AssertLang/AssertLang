"""Debug Bug #4 test failure"""

import sys
from pathlib import Path

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from dsl.ir import IRModule, IRFunction, IRParameter, IRType, IRReturn, IRCall, IRIdentifier
from language.javascript_generator import generate_javascript

# Test str() mapping
module = IRModule(
    name="test",
    functions=[
        IRFunction(
            name="test_str",
            params=[IRParameter(name="x", param_type=IRType(name="int"))],
            return_type=IRType(name="string"),
            body=[
                IRReturn(
                    value=IRCall(
                        function=IRIdentifier(name="str"),
                        args=[IRIdentifier(name="x")]
                    )
                )
            ]
        )
    ]
)

js_code = generate_javascript(module)
print("Generated JavaScript:")
print("="*80)
print(js_code)
print("="*80)

print("\nChecking for str():")
if "str(" in js_code:
    print("❌ FAIL: Contains 'str(' - Python function not mapped!")
    # Find where it appears
    for i, line in enumerate(js_code.split('\n'), 1):
        if 'str(' in line:
            print(f"  Line {i}: {line}")
else:
    print("✓ PASS: Does not contain 'str('")

print("\nChecking for String():")
if "String(" in js_code:
    print("✓ PASS: Contains 'String(' - correctly mapped!")
    for i, line in enumerate(js_code.split('\n'), 1):
        if 'String(' in line:
            print(f"  Line {i}: {line}")
else:
    print("❌ FAIL: Does not contain 'String(' - mapping failed!")
