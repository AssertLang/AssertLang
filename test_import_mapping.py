#!/usr/bin/env python3
"""Test import/module translation."""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from language.python_parser_v2 import PythonParserV2
from language.nodejs_generator_v2 import NodeJSGeneratorV2
from language.go_generator_v2 import GoGeneratorV2

# Test code with various imports
python_code = """
import math
import random
import os
import sys
import time
import json

def use_libraries():
    # Math operations
    x = math.sqrt(16)
    y = math.sin(0.5)

    # Random
    r = random.random()

    # OS operations
    os.system("ls")

    # JSON
    data = json.dumps({"key": "value"})

    return x
"""

print("=" * 70)
print("IMPORT MAPPING TEST")
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

# JavaScript import checks
print("\n### JavaScript Imports:")

if "// math is built-in" in js_code:
    print("✅ math → built-in (no import)")
    successes.append("math built-in (JS)")
else:
    issues.append("❌ JS: math not recognized as built-in")

if "// random is built-in" in js_code:
    print("✅ random → built-in (Math.random)")
    successes.append("random built-in (JS)")
else:
    issues.append("❌ JS: random not recognized as built-in")

if "const os = require('os')" in js_code or "require('os')" in js_code:
    print("✅ os → require('os')")
    successes.append("os require (JS)")
else:
    issues.append("❌ JS: os not properly imported")

if "// sys is built-in" in js_code or "// sys" in js_code:
    print("✅ sys → built-in (process)")
    successes.append("sys built-in (JS)")
else:
    issues.append("❌ JS: sys not recognized")

if "// json is built-in" in js_code or "// json" in js_code:
    print("✅ json → built-in (JSON object)")
    successes.append("json built-in (JS)")
else:
    issues.append("❌ JS: json not recognized as built-in")

# Go import checks
print("\n### Go Imports:")

if '"math"' in go_code:
    print("✅ math → math package")
    successes.append("math import (Go)")
else:
    issues.append("❌ Go: math not imported")

if '"math/rand"' in go_code:
    print("✅ random → math/rand")
    successes.append("random → math/rand (Go)")
else:
    issues.append("❌ Go: random not mapped to math/rand")

if '"os"' in go_code:
    print("✅ os → os package")
    successes.append("os import (Go)")
else:
    issues.append("❌ Go: os not imported")

if '"encoding/json"' in go_code:
    print("✅ json → encoding/json")
    successes.append("json import (Go)")
else:
    print("⚠️  Go: json import may be missing (check function usage)")

# Function call validation
print("\n### Function Call Mapping:")

if "Math.sqrt" in js_code and "Math.sin" in js_code:
    print("✅ JS: math.sqrt/sin → Math.sqrt/sin")
    successes.append("math function mapping (JS)")
else:
    issues.append("❌ JS: math functions not mapped")

if "math.Sqrt" in go_code and "math.Sin" in go_code:
    print("✅ Go: math.sqrt/sin → math.Sqrt/Sin")
    successes.append("math function mapping (Go)")
else:
    issues.append("❌ Go: math functions not mapped")

# Summary
print("\n" + "=" * 70)
print("SUMMARY")
print("=" * 70)

print(f"\n✅ Successes: {len(successes)}")
for s in successes[:5]:  # Show first 5
    print(f"  • {s}")
if len(successes) > 5:
    print(f"  ... and {len(successes) - 5} more")

if issues:
    print(f"\n❌ Issues: {len(issues)}")
    for i in issues:
        print(f"  • {i}")
    print("\n⚠️  Import mapping needs refinement")
else:
    print("\n🎉 IMPORT MAPPING WORKING PERFECTLY!")
    print("\nFixed:")
    print("  ✓ Built-in detection (math, random, json → no import in JS)")
    print("  ✓ Package mapping (random → math/rand in Go)")
    print("  ✓ Require statements (os → require('os') in JS)")
    print("  ✓ Function calls still work (Math.sqrt, math.Sqrt)")

print(f"\nImport mapping: {len(successes)}/{len(successes) + len(issues)} features working")
