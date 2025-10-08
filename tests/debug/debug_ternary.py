#!/usr/bin/env python3
"""Debug ternary operator in argument context."""

from language.python_parser_v2 import PythonParserV2
from language.go_generator_v2 import GoGeneratorV2

# Test case: Ternary in function argument
python_code = '''
import os

def test():
    # Ternary as function argument
    cmd = "cls" if os.name == "nt" else "clear"
    return cmd
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

# Check for issues
if "func() interface{}" in go_code:
    print("\n❌ IIFE found - ternary not properly expanded!")
elif "if" in go_code and "else" in go_code:
    print("\n✅ Proper if/else expansion used")
else:
    print("\n⚠️  Unexpected output")
