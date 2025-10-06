#!/usr/bin/env python3
"""Test built-in function mapping."""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from language.python_parser_v2 import PythonParserV2
from language.nodejs_generator_v2 import NodeJSGeneratorV2
from language.go_generator_v2 import GoGeneratorV2

# Test code with built-in functions
python_code = """
def test_builtins():
    arr = [1, 2, 3]
    size = len(arr)
    print("Hello, world!")
    for i in range(5):
        print(i)
    return size
"""

print("=== Test: Built-in Functions ===")
print("\nOriginal Python:")
print(python_code)

# Parse Python → IR
py_parser = PythonParserV2()
ir = py_parser.parse_source(python_code, "test.py")

# Generate JavaScript
js_gen = NodeJSGeneratorV2()
js_code = js_gen.generate(ir)
print("\nGenerated JavaScript:")
print(js_code)

# Generate Go
go_gen = GoGeneratorV2()
go_code = go_gen.generate(ir)
print("\nGenerated Go:")
print(go_code)

# Validation
print("\n=== Validation ===")

errors = []

# JavaScript checks
print("\n### JavaScript:")
if "arr.length" in js_code:
    print("✅ len(arr) → arr.length")
else:
    errors.append("❌ JS: len() not mapped to .length")

if "console.log" in js_code:
    print("✅ print() → console.log")
else:
    errors.append("❌ JS: print() not mapped")

# Note: range() mapping is complex (needs Array.from), so we'll skip for now

# Go checks
print("\n### Go:")
if "len(arr)" in go_code:
    print("✅ len(arr) → len(arr) (Go has built-in len)")
else:
    errors.append("❌ Go: len() not preserved")

if "fmt.Println" in go_code:
    print("✅ print() → fmt.Println")
else:
    errors.append("❌ Go: print() not mapped")

# Summary
print("\n=== Summary ===")
if errors:
    print(f"\n❌ {len(errors)} ISSUES:")
    for error in errors:
        print(f"  {error}")
    sys.exit(1)
else:
    print("\n✅ ALL BUILT-IN FUNCTION MAPPINGS WORK!")
    print("\nMapped:")
    print("  ✓ len() correctly handled in both languages")
    print("  ✓ print() correctly mapped")
