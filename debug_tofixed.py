#!/usr/bin/env python3
"""Debug toFixed issue."""

from language.python_parser_v2 import PythonParserV2
from language.go_generator_v2 import GoGeneratorV2

# Test case: Number formatting
python_code = '''
def test():
    t = 3.14159
    msg = f"Value: {t:.2f}"  # Python f-string formatting
    return msg
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
if "toFixed" in go_code.lower() or "ToFixed" in go_code:
    print("\n❌ toFixed found - JS method leaked!")
elif "Sprintf" in go_code and "%.2f" in go_code:
    print("\n✅ Proper Go formatting used")
else:
    print(f"\n⚠️  Unexpected output")
