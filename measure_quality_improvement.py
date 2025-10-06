#!/usr/bin/env python3
"""
Measure code quality improvements.

Metrics:
1. interface{} usage (lower is better)
2. Type inference success rate
3. Compilation readiness
"""

from language.python_parser_v2 import PythonParserV2
from language.go_generator_v2 import GoGeneratorV2

# Real-world test case
python_code = '''
import math
import random

def galaxy(width=120, height=40, t=0.0):
    output = []
    cx, cy = width / 2, height / 2
    for y in range(height):
        row = ""
        for x in range(width):
            dx, dy = (x - cx) / cx, (y - cy) / cy
            r = math.sqrt(dx**2 + dy**2)
            a = math.atan2(dy, dx)
            bright = math.pow(math.cos(a * 3 + r * 12 - t * 2), 2)
            if bright > 0.5:
                char = random.choice(["*", "·", "✦"])
                row += char
            else:
                row += " "
        output.append(row)
    return "\\n".join(output)
'''

print("=" * 80)
print("Quality Measurement - Python → Go Translation")
print("=" * 80)

# Parse and generate
parser = PythonParserV2()
ir = parser.parse_source(python_code)

go_gen = GoGeneratorV2()
go_code = go_gen.generate(ir)

print(f"\nGenerated Go code ({len(go_code)} chars):\n")
print(go_code)

# Measure metrics
lines = go_code.split('\n')
total_lines = len([l for l in lines if l.strip() and not l.strip().startswith('//')])

# Count interface{} usage
interface_count = go_code.count("interface{}")
interface_lines = [i+1 for i, line in enumerate(lines) if "interface{}" in line]

# Count specific types
float64_count = go_code.count("float64")
int_count = len([l for l in lines if " int " in l or " int=" in l])
string_count = len([l for l in lines if " string " in l or " string=" in l])
bool_count = len([l for l in lines if " bool " in l or " bool=" in l])

# Count problematic patterns
arrow_functions = go_code.count("=>")
multiline_strings = go_code.count('"\n')
placeholders = go_code.count("...")

print("\n" + "=" * 80)
print("METRICS")
print("=" * 80)

print(f"\n📊 Code Size:")
print(f"  Total lines: {total_lines}")
print(f"  Total chars: {len(go_code)}")

print(f"\n🎯 Type Quality:")
print(f"  interface{{}} usage: {interface_count} occurrences")
if interface_lines:
    print(f"  Lines: {interface_lines}")
print(f"  float64: {float64_count}")
print(f"  Specific type ratio: {((float64_count + int_count + string_count + bool_count) / max(1, total_lines)) * 100:.1f}%")

print(f"\n❌ Code Issues:")
print(f"  Arrow functions (=>) [CRITICAL]: {arrow_functions}")
print(f"  Multiline string breaks: {multiline_strings}")
print(f"  Placeholders (...): {placeholders}")

# Calculate quality score
issues = arrow_functions * 10  # Critical
issues += interface_count  # Generic types
issues += multiline_strings * 2  # Syntax errors
issues += placeholders * 5  # Missing implementations

max_issues = total_lines  # Assume 1 issue per line would be 0% quality
quality = max(0, 100 - (issues / max_issues * 100))

print(f"\n🏆 Estimated Quality: {quality:.1f}%")

if arrow_functions == 0:
    print("  ✅ No arrow functions (lambda fix working!)")
if interface_count < 5:
    print(f"  ✅ Low interface{{}} usage (type inference working!)")
elif interface_count < 10:
    print(f"  ⚠️  Moderate interface{{}} usage")
else:
    print(f"  ❌ High interface{{}} usage (type inference needs work)")

print("\n" + "=" * 80)
