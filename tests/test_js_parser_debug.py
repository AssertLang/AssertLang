#!/usr/bin/env python3
"""Debug JavaScript parser issue with type annotations."""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from language.nodejs_parser_v2 import NodeJSParserV2

# Test 1: WITHOUT type annotations (should work)
js_code_no_types = """
export function process(items) {
    const result = items.filter(x => (x > 0)).map(x => (x * 2));
    return result;
}
"""

# Test 2: WITH type annotations (currently broken)
js_code_with_types = """
export function process(items: any): void {
    const result = items.filter(x => (x > 0)).map(x => (x * 2));
    return result;
}
"""

parser = NodeJSParserV2()

print("=" * 70)
print("Test 1: WITHOUT type annotations")
print("=" * 70)
ir1 = parser.parse_source(js_code_no_types, "test.js")
func1 = ir1.functions[0]
print(f"Function: {func1.name}")
print(f"Number of statements in body: {len(func1.body)}")
for i, stmt in enumerate(func1.body):
    print(f"  Statement {i+1}: {type(stmt).__name__}")
print()

print("=" * 70)
print("Test 2: WITH type annotations")
print("=" * 70)
ir2 = parser.parse_source(js_code_with_types, "test.js")
func2 = ir2.functions[0]
print(f"Function: {func2.name}")
print(f"Number of statements in body: {len(func2.body)}")
for i, stmt in enumerate(func2.body):
    print(f"  Statement {i+1}: {type(stmt).__name__}")
print()

print("=" * 70)
print("DEBUGGING: Extract body manually")
print("=" * 70)

# Manually extract what the regex sees
import re

for code, label in [(js_code_no_types, "NO TYPES"), (js_code_with_types, "WITH TYPES")]:
    print(f"\n{label}:")
    pattern = r'(async\s+)?function\s+(\w+)\s*\(([^)]*)\)(?:\s*:\s*([^{]+))?\s*\{'
    match = re.search(pattern, code)
    if match:
        print(f"  Match found: {match.group(0)}")
        print(f"  Params: '{match.group(3)}'")
        print(f"  Return type: '{match.group(4)}'")
        body_start = match.end()
        print(f"  Body starts at index: {body_start}")
        print(f"  Character at body_start-1: '{code[body_start-1]}'")

        # Show what _extract_block_body would see
        remaining = code[body_start-1:]
        print(f"  Remaining code: {repr(remaining[:100])}")
