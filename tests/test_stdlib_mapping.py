#!/usr/bin/env python3
"""Test standard library function mapping."""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from language.python_parser_v2 import PythonParserV2
from language.nodejs_generator_v2 import NodeJSGeneratorV2
from language.go_generator_v2 import GoGeneratorV2
from language.rust_generator_v2 import RustGeneratorV2
from language.dotnet_generator_v2 import DotNetGeneratorV2

# Test code with stdlib calls
python_code = """
import math
import random

def calculate():
    x = math.sqrt(16)
    y = math.sin(3.14)
    z = math.atan2(1, 2)
    r = random.random()
    return x, y, z, r
"""

print("=== Test: Standard Library Mapping ===")
print("\nOriginal Python:")
print(python_code)

# Parse Python → IR
py_parser = PythonParserV2()
ir = py_parser.parse_source(python_code, "test.py")

# Generate JavaScript
js_gen = NodeJSGeneratorV2()
js_code = js_gen.generate(ir)
print("\nGenerated JavaScript:")
print(js_code[:400] + "...")

# Generate Go
go_gen = GoGeneratorV2()
go_code = go_gen.generate(ir)
print("\nGenerated Go:")
print(go_code[:400] + "...")

# Validate mappings
print("\n=== Validation ===")

js_mappings = [
    ("Math.sqrt", "JS: math.sqrt → Math.sqrt"),
    ("Math.sin", "JS: math.sin → Math.sin"),
    ("Math.atan2", "JS: math.atan2 → Math.atan2"),
    ("Math.random", "JS: random.random → Math.random"),
]

go_mappings = [
    ("math.Sqrt", "Go: math.sqrt → math.Sqrt"),
    ("math.Sin", "Go: math.sin → math.Sin"),
    ("math.Atan2", "Go: math.atan2 → math.Atan2"),
    ("rand.Float64", "Go: random.random → rand.Float64"),
]

all_good = True

for expected, desc in js_mappings:
    if expected in js_code:
        print(f"✅ {desc}")
    else:
        print(f"❌ FAILED: {desc}")
        all_good = False

for expected, desc in go_mappings:
    if expected in go_code:
        print(f"✅ {desc}")
    else:
        print(f"❌ FAILED: {desc}")
        all_good = False

if not all_good:
    print("\n❌ Some mappings failed")
    sys.exit(1)

print("\n✅ ALL STDLIB MAPPINGS WORK!")
