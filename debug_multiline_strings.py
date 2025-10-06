#!/usr/bin/env python3
"""Debug multiline string literal issue."""

from language.python_parser_v2 import PythonParserV2
from language.go_generator_v2 import GoGeneratorV2

# Test case with f-string containing newline
python_code = '''
def test():
    items = ["a", "b", "c"]
    result = "\\n".join(items)

    # F-string with newline
    msg = f"\\nHello World\\n"

    return result
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

# Check for issues
multiline_breaks = go_code.count('"\n')
print(f"\n{'❌' if multiline_breaks > 0 else '✅'} Multiline string breaks: {multiline_breaks}")

if multiline_breaks > 0:
    print("\nLocations:")
    for i, line in enumerate(go_code.split('\n'), 1):
        if '"\n' in line:
            print(f"  Line {i}: {line.strip()}")
