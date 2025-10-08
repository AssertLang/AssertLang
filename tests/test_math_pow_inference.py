#!/usr/bin/env python3
"""Test math.pow type inference."""

from language.python_parser_v2 import PythonParserV2
from language.go_generator_v2 import GoGeneratorV2

python_code = '''
import math

def test():
    x = 2.0
    y = 3.0
    result = math.pow(x, y)
    return result
'''

parser = PythonParserV2()
ir = parser.parse_source(python_code)

go_gen = GoGeneratorV2()
go_code = go_gen.generate(ir)

print("Generated Go:")
print(go_code)

if "var result float64" in go_code:
    print("\n✅ Type properly inferred as float64")
elif "var result interface{}" in go_code:
    print("\n❌ Type is interface{} - inference failed")
