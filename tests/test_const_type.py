#!/usr/bin/env python3
"""Test if type annotation on const breaks parsing."""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from language.nodejs_parser_v2 import NodeJSParserV2

# Test 1: const WITH type annotation
js_with_type = """
function process(items) {
  const result: any = items.filter(x => (x > 0)).map(x => (x * 2));
  return result;
}
"""

# Test 2: const WITHOUT type annotation
js_without_type = """
function process(items) {
  const result = items.filter(x => (x > 0)).map(x => (x * 2));
  return result;
}
"""

parser = NodeJSParserV2()

for code, label in [(js_with_type, "const WITH type"), (js_without_type, "const WITHOUT type")]:
    print("=" * 70)
    print(label)
    print("=" * 70)

    ir = parser.parse_source(code, "test.js")
    if ir.functions:
        func = ir.functions[0]
        print(f"Function: {func.name}")
        print(f"Statements: {len(func.body)}")
        for i, stmt in enumerate(func.body):
            print(f"  {i+1}. {type(stmt).__name__}")
    else:
        print("NO FUNCTIONS FOUND!")
    print()
