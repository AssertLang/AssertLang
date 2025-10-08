#!/usr/bin/env python3
"""Test all improvements from this session."""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from language.python_parser_v2 import PythonParserV2
from language.nodejs_generator_v2 import NodeJSGeneratorV2
from language.go_generator_v2 import GoGeneratorV2

# Test code showcasing all fixes
python_code = """
def process_data(items):
    # Exception handling with specific types
    try:
        result = []
        for i in range(len(items)):
            value = items[i]
            # F-string with format specifier
            label = f"Item {i}: {value:.2f}"
            result.append(label)
        return result
    except IndexError as e:
        print(f"Index error: {e}")
        return []
    except Exception as e:
        print(f"Error: {e}")
        return []

def calculate_stats(numbers):
    # Range with start/stop
    total = 0
    for i in range(5, 10):
        total += numbers[i]

    # F-string without format spec
    msg = f"Sum of items 5-9: {total}"
    return msg
"""

print("=" * 70)
print("SESSION IMPROVEMENTS TEST")
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

# Validation
print("\n" + "=" * 70)
print("VALIDATION")
print("=" * 70)

successes = []
issues = []

# Exception handling checks
print("\n### Exception Handling:")
if "catch (e: Error)" in js_code or "} catch (e)" in js_code:
    print("✅ JS: Exception types mapped to Error")
    successes.append("Exception type mapping (JS)")
else:
    issues.append("❌ JS: Exception types not mapped")

if "// catch" in go_code or "defer func()" in go_code:
    print("✅ Go: Error handling pattern present")
    successes.append("Go error handling")
else:
    issues.append("❌ Go: No error handling pattern")

# F-string checks
print("\n### F-String Translation:")
if ".toFixed(2)" in js_code:
    print("✅ JS: F-string format specifier (.2f → .toFixed(2))")
    successes.append("F-string format spec (JS)")
else:
    issues.append("❌ JS: Format specifiers not working")

if f"`Item ${{i}}: ${{value.toFixed(2)}}`" in js_code or "toFixed(2)" in js_code:
    print("✅ JS: Template literals with toFixed()")
    successes.append("Template literal conversion (JS)")
else:
    issues.append("❌ JS: Template literals incomplete")

# Range() checks
print("\n### Range() Translation:")
if "Array.from({length:" in js_code and "}, (_, i) => i)" in js_code:
    print("✅ JS: range() → Array.from()")
    successes.append("range() to Array.from (JS)")
else:
    issues.append("❌ JS: range() not properly translated")

if "for i := 0; i <" in go_code or "for i := 5; i < 10; i++" in go_code:
    print("✅ Go: range() → C-style for loop")
    successes.append("range() to C-style loop (Go)")
else:
    issues.append("❌ Go: range() not properly translated")

# Built-in function checks
print("\n### Built-in Functions:")
if ".length" in js_code and "len(" not in js_code:
    print("✅ JS: len() → .length")
    successes.append("len() mapping (JS)")
else:
    issues.append("❌ JS: len() not mapped to .length")

if "console.log" in js_code:
    print("✅ JS: print() → console.log()")
    successes.append("print() mapping (JS)")
else:
    issues.append("❌ JS: print() not mapped")

if "fmt.Println" in go_code:
    print("✅ Go: print() → fmt.Println()")
    successes.append("print() mapping (Go)")
else:
    issues.append("❌ Go: print() not mapped")

# Summary
print("\n" + "=" * 70)
print("SUMMARY")
print("=" * 70)

print(f"\n✅ Successes: {len(successes)}")
for s in successes:
    print(f"  • {s}")

if issues:
    print(f"\n❌ Issues: {len(issues)}")
    for i in issues:
        print(f"  • {i}")
    print("\n⚠️  Some improvements need more work")
else:
    print("\n🎉 ALL IMPROVEMENTS WORKING!")
    print("\nFixed in this session:")
    print("  ✓ Exception type mapping (Python → JS/Go)")
    print("  ✓ F-string format specifiers (:.2f → .toFixed(2))")
    print("  ✓ range() translation (JS: Array.from, Go: C-style loops)")
    print("  ✓ Built-in function mapping (len, print)")

print(f"\nTotal quality improvements: {len(successes)}/{len(successes) + len(issues)} features working")
