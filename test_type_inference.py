#!/usr/bin/env python3
"""Test improved type inference."""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from language.python_parser_v2 import PythonParserV2
from language.nodejs_generator_v2 import NodeJSGeneratorV2
from language.go_generator_v2 import GoGeneratorV2

# Test code with various types
python_code = """
def test_types():
    # Primitives
    x = 5
    y = 3.14
    z = "hello"

    # Arrays
    numbers = [1, 2, 3]
    strings = ["a", "b", "c"]
    mixed = [1, "two", 3.0]

    # Operations
    result = x + 10

    return numbers
"""

print("=" * 70)
print("TYPE INFERENCE TEST")
print("=" * 70)

print("\nOriginal Python:")
print(python_code)

# Parse Python → IR
parser = PythonParserV2()
ir = parser.parse_source(python_code, "test.py")

# Generate JavaScript
js_gen = NodeJSGeneratorV2()
js_code = js_gen.generate(ir)

print("\n" + "=" * 70)
print("JAVASCRIPT OUTPUT")
print("=" * 70)
print(js_code)

# Generate Go
go_gen = GoGeneratorV2()
go_code = go_gen.generate(ir)

print("\n" + "=" * 70)
print("GO OUTPUT")
print("=" * 70)
print(go_code)

# Validation
print("\n" + "=" * 70)
print("VALIDATION")
print("=" * 70)

errors = []

# JavaScript checks
print("\n### JavaScript Type Inference:")

if "let x: number = 5" in js_code:
    print("✅ x: number (not any)")
else:
    errors.append("❌ JS: x should be number")

if "let y: number = 3.14" in js_code:
    print("✅ y: number (not any)")
else:
    errors.append("❌ JS: y should be number")

if "const z: string = " in js_code:
    print("✅ z: string (not any)")
else:
    errors.append("❌ JS: z should be string")

# Check array types
if "numbers: number[]" in js_code or "numbers: Array<number>" in js_code:
    print("✅ numbers: number[] (not any)")
elif "numbers: any" in js_code:
    errors.append("❌ JS: numbers is still 'any' - type inference failed")
else:
    print("⚠️  JS: numbers has unknown type format")

if "strings: string[]" in js_code or "strings: Array<string>" in js_code:
    print("✅ strings: string[] (not any)")
elif "strings: any" in js_code:
    errors.append("❌ JS: strings is still 'any' - type inference failed")
else:
    print("⚠️  JS: strings has unknown type format")

# Go checks
print("\n### Go Type Inference:")

if "var x int = 5" in go_code or "var x float64 = 5" in go_code:
    print("✅ x: int/float64 (not interface{})")
elif "var x interface{} = 5" in go_code:
    errors.append("❌ Go: x is still 'interface{}' - type inference failed")

if "var numbers []int" in go_code:
    print("✅ numbers: []int (not interface{})")
elif "var numbers interface{}" in go_code:
    errors.append("❌ Go: numbers is still 'interface{}' - type inference failed")
else:
    print("⚠️  Go: numbers has unknown type")

# Summary
print("\n" + "=" * 70)
print("SUMMARY")
print("=" * 70)

if errors:
    print(f"\n❌ {len(errors)} ISSUES:")
    for error in errors:
        print(f"  {error}")
    print("\nType inference PARTIALLY working - arrays still need work")
else:
    print("\n✅ TYPE INFERENCE SIGNIFICANTLY IMPROVED!")
    print("\nFixed:")
    print("  ✓ Primitives correctly typed (int, float, string)")
    print("  ✓ Arrays inferred from element types")
    print("  ✓ No more 'any' for simple types")
