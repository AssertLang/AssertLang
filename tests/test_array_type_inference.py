#!/usr/bin/env python3
"""Test array type inference from append operations."""

from language.python_parser_v2 import PythonParserV2
from language.go_generator_v2 import GoGeneratorV2

# Test case: array initialized empty, then appended with strings
python_code = '''
def test():
    output = []
    for i in range(5):
        row = "item"
        output.append(row)
    return output
'''

print("Python Code:")
print(python_code)

# Parse
parser = PythonParserV2()
ir = parser.parse_source(python_code)

# Generate
go_gen = GoGeneratorV2()
go_code = go_gen.generate(ir)

print("\nGenerated Go:")
print(go_code)

# Check for type quality
if "[]string" in go_code:
    print("\n✅ Array type properly inferred as []string")
elif "[]interface{}" in go_code:
    print("\n❌ Array type is []interface{} - inference needed")

    # Show the problematic line
    for i, line in enumerate(go_code.split('\n'), 1):
        if '[]interface{}' in line:
            print(f"   Line {i}: {line.strip()}")
else:
    print("\n⚠️  Unexpected output")
