#!/usr/bin/env python3
"""Test tuple unpacking fix."""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from language.python_parser_v2 import PythonParserV2
from language.nodejs_generator_v2 import NodeJSGeneratorV2
from language.go_generator_v2 import GoGeneratorV2

# Test code with tuple unpacking
python_code = """
def galaxy(width=120, height=40):
    cx, cy = width / 2, height / 2
    return cx, cy
"""

print("=== Test: Tuple Unpacking ===")
print("\nOriginal Python:")
print(python_code)

# Parse Python → IR
py_parser = PythonParserV2()
ir = py_parser.parse_source(python_code, "test.py")

print("\nIR (function body statements):")
func = ir.functions[0]
for i, stmt in enumerate(func.body):
    print(f"  {i+1}. {type(stmt).__name__}: {stmt}")

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

# Validate no empty variable names
print("\n=== Validation ===")
if "const  = " in js_code or "let  = " in js_code:
    print("❌ FAILED: JavaScript has empty variable names")
    sys.exit(1)
else:
    print("✅ JavaScript: No empty variable names")

if "var  interface{}" in go_code or "var  =" in go_code:
    print("❌ FAILED: Go has empty variable names")
    sys.exit(1)
else:
    print("✅ Go: No empty variable names")

if ("const cx" in js_code or "let cx" in js_code) and ("const cy" in js_code or "let cy" in js_code):
    print("✅ JavaScript: Both variables declared correctly")
else:
    print("❌ FAILED: JavaScript missing cx or cy")
    sys.exit(1)

if "var cx" in go_code and "var cy" in go_code:
    print("✅ Go: Both variables declared correctly")
else:
    print("❌ FAILED: Go missing cx or cy")
    sys.exit(1)

print("\n✅ ALL TESTS PASSED - Tuple unpacking works!")
