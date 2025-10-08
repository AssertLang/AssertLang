#!/usr/bin/env python3
"""Test type inference for ChoiceString call."""

from language.python_parser_v2 import PythonParserV2
from language.go_generator_v2 import GoGeneratorV2

python_code = '''
import random

def test():
    char = random.choice(["*", "·", "✦"])
    return char
'''

parser = PythonParserV2()
ir = parser.parse_source(python_code)

# Check type inference
from dsl.type_inference import TypeInferenceEngine
engine = TypeInferenceEngine()
engine.infer_module_types(ir)

print("Type environment:")
for var_name, var_type in engine.type_env.items():
    print(f"  {var_name}: {var_type.name}")

# Generate
go_gen = GoGeneratorV2()
go_code = go_gen.generate(ir)

print("\nGenerated Go:")
print(go_code)

if "var char string" in go_code:
    print("\n✅ Type properly inferred as string")
elif "var char interface{}" in go_code:
    print("\n❌ Type is interface{} - inference failed")
