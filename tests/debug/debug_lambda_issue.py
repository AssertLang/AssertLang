#!/usr/bin/env python3
"""Debug lambda translation issue."""

from language.python_parser_v2 import PythonParserV2
from language.go_generator_v2 import GoGeneratorV2

# Simple test case
python_code = '''
import random

def test():
    char = random.choice(["*", "·", "✦", ".", "•"])
    return char
'''

print("=" * 80)
print("Python Code:")
print("=" * 80)
print(python_code)

# Parse Python → IR
parser = PythonParserV2()
ir = parser.parse_source(python_code)

print("\n" + "=" * 80)
print("IR (relevant parts):")
print("=" * 80)

for func in ir.functions:
    print(f"Function: {func.name}")
    for i, stmt in enumerate(func.body):
        print(f"  Statement {i}: {stmt.type}")
        print(f"    {stmt}")

# Generate Go
go_gen = GoGeneratorV2()
go_code = go_gen.generate(ir)

print("\n" + "=" * 80)
print("Generated Go:")
print("=" * 80)
print(go_code)

# Check for arrow function
if "=>" in go_code:
    print("\n❌ ERROR: Arrow function detected in Go code!")
    print("   This is invalid Go syntax")
else:
    print("\n✅ No arrow functions found")
