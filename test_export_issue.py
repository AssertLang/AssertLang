#!/usr/bin/env python3
"""Test if 'export' keyword breaks parsing."""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from language.nodejs_parser_v2 import NodeJSParserV2

# Test 1: WITH export keyword
js_with_export = """
export function process(items: any): void {
  const result: any = items.filter(x => (x > 0)).map(x => (x * 2));
  return result;
}
"""

# Test 2: WITHOUT export keyword
js_without_export = """
function process(items: any): void {
  const result: any = items.filter(x => (x > 0)).map(x => (x * 2));
  return result;
}
"""

parser = NodeJSParserV2()

for code, label in [(js_with_export, "WITH export"), (js_without_export, "WITHOUT export")]:
    print("=" * 70)
    print(label)
    print("=" * 70)
    print("Code:")
    print(code)
    print()

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
