#!/usr/bin/env python3
"""Test ternary in function call."""

from language.python_parser_v2 import PythonParserV2
from language.go_generator_v2 import GoGeneratorV2

# Test: ternary as function argument
python_code = '''
import os

def clear():
    # Ternary in function argument
    os.system("cls" if os.name == "nt" else "clear")
'''

print("Python Code:")
print(python_code)

parser = PythonParserV2()
ir = parser.parse_source(python_code)

go_gen = GoGeneratorV2()
go_code = go_gen.generate(ir)

print("\nGenerated Go:")
print(go_code)

# Check quality
if "func() string" in go_code:
    print("\n✅ IIFE has proper type (string)")
elif "func() interface{}" in go_code:
    print("\n⚠️  IIFE still using interface{}")
else:
    print("\n❓ No IIFE found")
