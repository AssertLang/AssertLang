#!/usr/bin/env python3
"""Trace f-string issue."""

from language.python_parser_v2 import PythonParserV2
from language.go_generator_v2 import GoGeneratorV2

python_code = '''
def test():
    # F-string with newline
    msg = f"\\nHello World\\n"
    return msg
'''

print("Python Code:")
print(python_code)

# Parse
parser = PythonParserV2()
ir = parser.parse_source(python_code)

# Check IR
print("\nIR:")
for func in ir.functions:
    for stmt in func.body:
        if hasattr(stmt, 'value'):
            print(f"Statement type: {type(stmt.value)}")
            print(f"Value: {stmt.value}")
            if hasattr(stmt.value, 'parts'):
                print(f"F-string parts: {stmt.value.parts}")
                for i, part in enumerate(stmt.value.parts):
                    print(f"  Part {i}: {repr(part)}")

# Generate
go_gen = GoGeneratorV2()
go_code = go_gen.generate(ir)

print("\nGenerated Go:")
print(go_code)
