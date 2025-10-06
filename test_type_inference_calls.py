#!/usr/bin/env python3
"""Test type inference for function calls."""

from language.python_parser_v2 import PythonParserV2
from language.go_generator_v2 import GoGeneratorV2

python_code = '''
import math

def test():
    r = math.sqrt(16.0)
    a = math.atan2(1.0, 2.0)
    bright = math.pow(0.5, 2.0)
    return r
'''

print("=" * 80)
print("Python Code:")
print("=" * 80)
print(python_code)

# Parse Python → IR
parser = PythonParserV2()
ir = parser.parse_source(python_code)

# Generate Go
go_gen = GoGeneratorV2()
go_code = go_gen.generate(ir)

print("\n" + "=" * 80)
print("Generated Go:")
print("=" * 80)
print(go_code)

# Check for interface{} usage
interface_count = go_code.count("interface{}")
print(f"\n{'❌' if interface_count > 0 else '✅'} interface{{}} count: {interface_count}")

# Check for specific types
has_float64 = "var r float64" in go_code
has_a_float64 = "var a float64" in go_code
has_bright_float64 = "var bright float64" in go_code

print(f"{'✅' if has_float64 else '❌'} r typed as float64: {has_float64}")
print(f"{'✅' if has_a_float64 else '❌'} a typed as float64: {has_a_float64}")
print(f"{'✅' if has_bright_float64 else '❌'} bright typed as float64: {has_bright_float64}")

if has_float64 and has_a_float64 and has_bright_float64:
    print("\n🎉 SUCCESS! Type inference working for math function calls")
else:
    print("\n❌ FAILURE: Type inference not working")
