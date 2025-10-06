#!/usr/bin/env python3
"""Extract all IR node types and their structure."""

import ast
import sys

with open('dsl/ir.py') as f:
    tree = ast.parse(f.read())

# Find all Enum classes
enums = {}
for node in ast.walk(tree):
    if isinstance(node, ast.ClassDef):
        # Check if it's an Enum
        for base in node.bases:
            if isinstance(base, ast.Name) and base.id == 'Enum':
                enum_values = []
                for item in node.body:
                    if isinstance(item, ast.Assign):
                        for target in item.targets:
                            if isinstance(target, ast.Name):
                                enum_values.append(target.id)
                enums[node.name] = enum_values
                break

# Print results
for enum_name, values in enums.items():
    print(f"\n{enum_name} ({len(values)} values):")
    for val in values:
        print(f"  - {val}")

print(f"\nTotal enum values: {sum(len(v) for v in enums.values())}")
