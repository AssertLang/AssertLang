#!/usr/bin/env python3
"""Test with literal append (simpler case)."""

from language.python_parser_v2 import PythonParserV2
from dsl.type_inference import TypeInferenceEngine

python_code = '''
def test():
    output = []
    output.append("item")
    return output
'''

parser = PythonParserV2()
ir = parser.parse_source(python_code)

engine = TypeInferenceEngine()
engine.infer_module_types(ir)

print("Array element types collected:")
for array_name, types in engine.array_element_types.items():
    print(f"  {array_name}: {types}")

print("\nType environment:")
for var_name, var_type in engine.type_env.items():
    print(f"  {var_name}: {var_type.name}")
    if hasattr(var_type, 'generic_args') and var_type.generic_args:
        print(f"    Generic args: {[arg.name for arg in var_type.generic_args]}")
