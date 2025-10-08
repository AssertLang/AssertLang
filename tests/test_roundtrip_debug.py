#!/usr/bin/env python3
"""Debug Python → JavaScript → Python round-trip."""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from language.python_parser_v2 import PythonParserV2
from language.nodejs_generator_v2 import NodeJSGeneratorV2
from language.nodejs_parser_v2 import NodeJSParserV2
from language.python_generator_v2 import PythonGeneratorV2

python_code = """
def process(items):
    result = [x * 2 for x in items if x > 0]
    return result
"""

print("=" * 70)
print("STEP 1: Parse Python → IR")
print("=" * 70)
py_parser = PythonParserV2()
ir1 = py_parser.parse_source(python_code, "test.py")
func1 = ir1.functions[0]
print(f"Function: {func1.name}")
print(f"Statements: {len(func1.body)}")
for i, stmt in enumerate(func1.body):
    print(f"  {i+1}. {type(stmt).__name__}")
print()

print("=" * 70)
print("STEP 2: Generate IR → JavaScript")
print("=" * 70)
js_gen = NodeJSGeneratorV2()
js_code = js_gen.generate(ir1)
print("Generated JavaScript:")
print(js_code)
print()

print("=" * 70)
print("STEP 3: Parse JavaScript → IR")
print("=" * 70)
js_parser = NodeJSParserV2()
ir2 = js_parser.parse_source(js_code, "test.js")
func2 = ir2.functions[0]
print(f"Function: {func2.name}")
print(f"Statements: {len(func2.body)}")
for i, stmt in enumerate(func2.body):
    print(f"  {i+1}. {type(stmt).__name__}")
print()

print("=" * 70)
print("STEP 4: Generate IR → Python")
print("=" * 70)
py_gen = PythonGeneratorV2()
python_code2 = py_gen.generate(ir2)
print("Generated Python:")
print(python_code2)
print()

print("=" * 70)
print("COMPARISON")
print("=" * 70)
print(f"Original Python statements: {len(func1.body)}")
print(f"After round-trip statements: {len(func2.body)}")
if len(func1.body) == len(func2.body):
    print("✅ Statement count preserved")
else:
    print("❌ Statement count lost!")
