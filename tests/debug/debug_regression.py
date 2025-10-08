#!/usr/bin/env python3

from language.python_parser_v2 import parse_python_source

# Test 1: Class parsing
source1 = """
class User:
    def __init__(self, name: str, age: int):
        self.name = name
        self.age = age
"""
module1 = parse_python_source(source1, "test")
cls = module1.classes[0]
print(f"Constructor params: {len(cls.constructor.params)}")
for p in cls.constructor.params:
    print(f"  - {p.name}: {p.param_type.name}")

# Test 2: Type inference
source2 = """
def calculate(x, y):
    result = x + y
    return result
"""
module2 = parse_python_source(source2, "test")
func = module2.functions[0]
print(f"\nFunction params:")
for p in func.params:
    print(f"  - {p.name}: {p.param_type.name}")
