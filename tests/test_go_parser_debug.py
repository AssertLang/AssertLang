#!/usr/bin/env python3
"""Debug Go parser comprehension detection"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from language.go_parser_v2 import GoParserV2

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

parser = GoParserV2()
ir = parser.parse_source(go_code, "test.go")

print(f"Module: {ir.name}")
print(f"Functions: {len(ir.functions)}")

if ir.functions:
    func = ir.functions[0]
    print(f"\nFunction: {func.name}")
    print(f"Params: {len(func.params)}")
    print(f"Body statements: {len(func.body)}")

    for i, stmt in enumerate(func.body):
        print(f"  {i+1}. {type(stmt).__name__}")
        if hasattr(stmt, 'value'):
            print(f"      value: {type(stmt.value).__name__}")
