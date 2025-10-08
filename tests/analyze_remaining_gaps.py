#!/usr/bin/env python3
"""Analyze remaining quality gaps preventing 90%+."""

from language.python_parser_v2 import PythonParserV2
from language.go_generator_v2 import GoGeneratorV2

# Real-world code
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

parser = PythonParserV2()
ir = parser.parse_source(python_code)

go_gen = GoGeneratorV2()
go_code = go_gen.generate(ir)

print("=" * 80)
print("REMAINING QUALITY GAPS ANALYSIS")
print("=" * 80)

# Find all interface{} usage
lines = go_code.split('\n')
interface_lines = []
for i, line in enumerate(lines, 1):
    if 'interface{}' in line and not line.strip().startswith('//'):
        interface_lines.append((i, line.strip()))

print(f"\n📊 interface{{}} Usage: {len(interface_lines)} occurrences")
for line_no, line in interface_lines:
    print(f"  Line {line_no}: {line}")

# Categorize issues
print("\n🔍 Root Causes:")

list_declarations = [l for l in interface_lines if '[]interface{}' in l[1]]
var_declarations = [l for l in interface_lines if 'var ' in l[1] and '[]' not in l[1]]
func_params = [l for l in interface_lines if 'func ' in l[1] and '(' in l[1]]

print(f"\n1. List/Array Type Inference ({len(list_declarations)} issues):")
for line_no, line in list_declarations:
    print(f"   Line {line_no}: {line}")
    print(f"   → Should infer element type from append operations")

print(f"\n2. Variable Assignment Type Inference ({len(var_declarations)} issues):")
for line_no, line in var_declarations:
    print(f"   Line {line_no}: {line}")
    print(f"   → Should infer type from RHS expression")

print(f"\n3. Function Parameters ({len(func_params)} issues):")
for line_no, line in func_params:
    print(f"   Line {line_no}: {line}")
    print(f"   → Helper functions - acceptable")

# Calculate impact
total_interface = len(interface_lines)
fixable = len(list_declarations) + len(var_declarations)

print("\n" + "=" * 80)
print("IMPACT ANALYSIS")
print("=" * 80)
print(f"\nTotal interface{{}} usage: {total_interface}")
print(f"Fixable through type inference: {fixable}")
print(f"Helper functions (acceptable): {len(func_params)}")

potential_reduction = (fixable / max(1, total_interface)) * 100
print(f"\nPotential interface{{}} reduction: {potential_reduction:.1f}%")

# Estimate quality gain
current_quality = 89.6
# Assume each interface{} costs ~2% quality
quality_gain = (fixable * 2)
estimated_quality = min(100, current_quality + quality_gain)

print(f"\nCurrent quality: {current_quality}%")
print(f"Estimated gain: +{quality_gain}%")
print(f"Target quality: {estimated_quality}%")

print("\n" + "=" * 80)
print("RECOMMENDED FIXES")
print("=" * 80)
print("\n1. Enhance array type inference from usage patterns")
print("   - Track append() calls to infer element type")
print("   - Expected gain: ~2-3%")
print("\n2. Improve variable assignment type inference")
print("   - Analyze RHS expression types")
print("   - Expected gain: ~3-4%")
print("\n3. Total expected quality: ~95%")
