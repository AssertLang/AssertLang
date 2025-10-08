#!/usr/bin/env python3
"""Debug type inference."""

from language.python_parser_v2 import PythonParserV2
from dsl.type_inference import TypeInferenceEngine

python_code = '''
import math

def test():
    r = math.sqrt(16.0)
    a = math.atan2(1.0, 2.0)
    return r
'''

print("Parsing Python → IR...")
parser = PythonParserV2()
ir = parser.parse_source(python_code)

# Check assignment types
print("\nAssignments in IR:")
for func in ir.functions:
    print(f"Function: {func.name}")
    for stmt in func.body:
        if hasattr(stmt, 'target'):
            print(f"  Assignment target: {stmt.target}, type: {type(stmt.target)}")
            print(f"  Assignment value: {type(stmt.value)}")

print("\nRunning type inference...")
type_engine = TypeInferenceEngine()
type_engine.infer_module_types(ir)

print(f"\ntype_env contents: {type_engine.type_env}")
print(f"function_types contents: {type_engine.function_types}")

# Check what types were inferred
for var_name, var_type in type_engine.type_env.items():
    print(f"  {var_name}: {var_type.name}")
