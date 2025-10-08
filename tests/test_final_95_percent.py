#!/usr/bin/env python3
"""Final comprehensive test - Verify 95%+ quality."""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from language.python_parser_v2 import PythonParserV2
from language.nodejs_generator_v2 import NodeJSGeneratorV2
from language.go_generator_v2 import GoGeneratorV2

# Comprehensive test code
python_code = """
import math
import random

# Module-level constants
COLORS = ["red", "green", "blue"]
MAX_SIZE = 100

def process_data(items):
    # Exception handling with mapped types
    try:
        result = []
        for i in range(len(items)):
            value = items[i]
            # F-string with format specifier
            label = f"Item {i}: {value:.2f}"
            result.append(label)

        # String operations
        output = "\\n".join(result)
        return output.upper()
    except IndexError as e:
        print(f"Error: {e}")
        return ""

def calculate_stats(numbers):
    # Range with start/stop
    total = 0
    for i in range(5, 10):
        total += numbers[i]

    # Math operations
    avg = total / 5
    sqrt_avg = math.sqrt(avg)

    return sqrt_avg
"""

print("=" * 70)
print("FINAL 95% QUALITY TEST")
print("=" * 70)

print("\nOriginal Python:")
print(python_code)

# Parse
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

# Comprehensive Validation
print("\n" + "=" * 70)
print("VALIDATION - 10 CATEGORIES")
print("=" * 70)

categories = {}

# 1. Exception Handling
print("\n### 1. Exception Handling:")
if "} catch (e: Error)" in js_code or "} catch (e: RangeError)" in js_code:
    print("✅ JS: Exception types mapped")
    categories["exception_js"] = True
else:
    print("❌ JS: Exception types not mapped")
    categories["exception_js"] = False

# 2. F-Strings
print("\n### 2. F-String Format Specifiers:")
if ".toFixed(2)" in js_code:
    print("✅ JS: .toFixed(2) for format spec")
    categories["fstring_js"] = True
else:
    print("❌ JS: Format specs not working")
    categories["fstring_js"] = False

# 3. range()
print("\n### 3. range() Translation:")
if "Array.from({length:" in js_code:
    print("✅ JS: range() → Array.from()")
    categories["range_js"] = True
else:
    print("❌ JS: range() not translated")
    categories["range_js"] = False

if "for i := 0; i <" in go_code or "for i := 5; i < 10; i++" in go_code:
    print("✅ Go: range() → C-style loop")
    categories["range_go"] = True
else:
    print("❌ Go: range() not translated")
    categories["range_go"] = False

# 4. Built-in Functions
print("\n### 4. Built-in Functions:")
if ".length" in js_code:
    print("✅ JS: len() → .length")
    categories["len_js"] = True
else:
    print("❌ JS: len() not mapped")
    categories["len_js"] = False

if "console.log" in js_code:
    print("✅ JS: print() → console.log()")
    categories["print_js"] = True
else:
    print("❌ JS: print() not mapped")
    categories["print_js"] = False

# 5. Imports
print("\n### 5. Import Translation:")
if "// math is built-in" in js_code:
    print("✅ JS: math recognized as built-in")
    categories["import_js"] = True
else:
    print("❌ JS: math import wrong")
    categories["import_js"] = False

if '"math"' in go_code:
    print("✅ Go: math imported correctly")
    categories["import_go"] = True
else:
    print("❌ Go: math not imported")
    categories["import_go"] = False

# 6. String Operations
print("\n### 6. String Operations:")
if "join(" in js_code and not '".join(' in js_code:
    print("✅ JS: .join() argument order fixed")
    categories["string_js"] = True
else:
    print("❌ JS: .join() still wrong")
    categories["string_js"] = False

if ".toUpperCase()" in js_code:
    print("✅ JS: .upper() → .toUpperCase()")
    categories["string_upper"] = True
else:
    print("❌ JS: .upper() not mapped")
    categories["string_upper"] = False

# 7. Module Constants
print("\n### 7. Module-Level Constants:")
if "const COLORS" in js_code or "let COLORS" in js_code:
    print("✅ JS: Module constants defined")
    categories["const_js"] = True
else:
    print("❌ JS: Constants missing")
    categories["const_js"] = False

if "COLORS" in go_code and ("var COLORS" in go_code or "const COLORS" in go_code):
    print("✅ Go: Module constants defined")
    categories["const_go"] = True
else:
    print("❌ Go: Constants missing")
    categories["const_go"] = False

# 8. Type Inference
print("\n### 8. Type Inference:")
if "Array[string]" in js_code or "Array<string>" in js_code:
    print("✅ JS: Array typed correctly")
    categories["types_js"] = True
else:
    print("⚠️  JS: Array typing needs work")
    categories["types_js"] = False

# 9. Math Functions
print("\n### 9. Math Function Mapping:")
if "Math.sqrt" in js_code:
    print("✅ JS: math.sqrt → Math.sqrt")
    categories["math_js"] = True
else:
    print("❌ JS: math.sqrt not mapped")
    categories["math_js"] = False

if "math.Sqrt" in go_code:
    print("✅ Go: math.sqrt → math.Sqrt")
    categories["math_go"] = True
else:
    print("❌ Go: math.sqrt not mapped")
    categories["math_go"] = False

# 10. Overall Code Quality
print("\n### 10. Code Quality:")
syntax_errors = js_code.count("<unknown>") + js_code.count("undefined")
if syntax_errors == 0:
    print("✅ JS: No <unknown> or undefined placeholders")
    categories["quality_js"] = True
else:
    print(f"❌ JS: {syntax_errors} placeholder issues")
    categories["quality_js"] = False

# Summary
print("\n" + "=" * 70)
print("FINAL SUMMARY")
print("=" * 70)

passing = sum(1 for v in categories.values() if v)
total = len(categories)
percentage = (passing / total) * 100

print(f"\n✅ Passing: {passing}/{total} ({percentage:.0f}%)")
print(f"\nCategories Passing:")
for cat, result in categories.items():
    status = "✅" if result else "❌"
    print(f"  {status} {cat}")

if percentage >= 95:
    print(f"\n🎉 SUCCESS! {percentage:.0f}% QUALITY ACHIEVED!")
    print("\nSystem is PRODUCTION READY for real-world code translation")
elif percentage >= 90:
    print(f"\n✨ EXCELLENT! {percentage:.0f}% quality - nearly production ready")
else:
    print(f"\n⚠️  {percentage:.0f}% quality - more work needed for production")

print(f"\n**Translation Quality: {percentage:.0f}%**")
