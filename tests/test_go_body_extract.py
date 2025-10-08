#!/usr/bin/env python3
"""Debug Go function body extraction"""

import sys
import os
import re
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

go_code = """
package main

func filterPositive(items []interface{}) []interface{} {
	result := []interface{}{}
	for _, x := range items {
		if x > 0 {
			result = append(result, x * 2)
		}
	}
	return result
}
"""

# Try to extract function body manually
func_pattern = r'func\s+(?:\([^)]+\)\s+)?(\w+)\s*\(([^)]*)\)(?:\s+([^{]+))?\s*\{'
match = re.search(func_pattern, go_code)

if match:
    func_name = match.group(1)
    func_start = match.start()

    print(f"Function: {func_name}")
    print(f"Match: {match.group(0)}")
    print(f"Start index: {func_start}")

    # Extract body
    brace_start = go_code.find('{', func_start)
    print(f"Opening brace at: {brace_start}")

    # Find matching closing brace
    depth = 0
    i = brace_start

    while i < len(go_code):
        if go_code[i] == '{':
            depth += 1
        elif go_code[i] == '}':
            depth -= 1
            if depth == 0:
                body = go_code[brace_start + 1:i]
                print(f"Closing brace at: {i}")
                print(f"\nExtracted body ({len(body)} chars):")
                print(repr(body))
                print("\nFormatted body:")
                print(body)
                break
        i += 1
