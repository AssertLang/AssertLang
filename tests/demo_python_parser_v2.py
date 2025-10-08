#!/usr/bin/env python3
"""
Demo: Python Parser V2 in Action

Shows how arbitrary Python code is parsed into IR.
"""

from language.python_parser_v2 import parse_python_source
from dsl.ir import *


def demo_simple_function():
    """Demo 1: Simple function parsing."""
    print("=" * 70)
    print("DEMO 1: Simple Function Parsing")
    print("=" * 70)

    source = """
def calculate_discount(price: float, discount_percent: int) -> float:
    '''Calculate discounted price.'''
    if discount_percent < 0 or discount_percent > 100:
        raise ValueError("Discount must be between 0 and 100")

    discount_amount = price * (discount_percent / 100)
    final_price = price - discount_amount
    return final_price
"""

    print("Python Source:")
    print(source)
    print("\n" + "-" * 70)

    module = parse_python_source(source, "discount_calculator")

    print("IR Output:\n")
    func = module.functions[0]
    print(f"Function: {func.name}")
    print(f"Parameters:")
    for param in func.params:
        print(f"  - {param.name}: {param.param_type.name}")
    print(f"Return Type: {func.return_type.name}")
    print(f"Throws: {func.throws}")
    print(f"Body Statements: {len(func.body)}")
    print(f"Docstring: {func.doc}")


def demo_class_parsing():
    """Demo 2: Class parsing."""
    print("\n" + "=" * 70)
    print("DEMO 2: Class Parsing")
    print("=" * 70)

    source = """
class ShoppingCart:
    items: list
    total: float

    def __init__(self):
        self.items = []
        self.total = 0.0

    def add_item(self, item: str, price: float) -> None:
        self.items.append(item)
        self.total = self.total + price

    def get_total(self) -> float:
        return self.total
"""

    print("Python Source:")
    print(source)
    print("\n" + "-" * 70)

    module = parse_python_source(source, "shopping")

    print("IR Output:\n")
    cls = module.classes[0]
    print(f"Class: {cls.name}")
    print(f"Properties:")
    for prop in cls.properties:
        print(f"  - {prop.name}: {prop.prop_type.name}")
    print(f"Constructor: {cls.constructor.name if cls.constructor else 'None'}")
    print(f"Methods:")
    for method in cls.methods:
        params = ', '.join(f"{p.name}: {p.param_type.name}" for p in method.params)
        ret = method.return_type.name if method.return_type else "None"
        print(f"  - {method.name}({params}) -> {ret}")


def demo_type_inference():
    """Demo 3: Type inference for untyped code."""
    print("\n" + "=" * 70)
    print("DEMO 3: Type Inference")
    print("=" * 70)

    source = """
def process_data(data):
    # Parser infers types from usage
    results = []           # Inferred as array
    count = 0              # Inferred as int
    message = "Processing" # Inferred as string
    enabled = True         # Inferred as bool

    for item in data:
        if item > 0:       # item inferred as numeric
            count = count + 1
            results.append(item * 2)

    return results
"""

    print("Python Source:")
    print(source)
    print("\n" + "-" * 70)

    module = parse_python_source(source, "processor")

    print("IR Output with Type Inference:\n")
    func = module.functions[0]
    print(f"Function: {func.name}")
    print(f"Parameters:")
    for param in func.params:
        print(f"  - {param.name}: {param.param_type.name} (inferred)")

    print(f"\nVariable Assignments (with inferred types):")
    for stmt in func.body:
        if isinstance(stmt, IRAssignment):
            print(f"  - {stmt.target}: {stmt.var_type.name}")


def demo_complete_module():
    """Demo 4: Complete module with imports, classes, and functions."""
    print("\n" + "=" * 70)
    print("DEMO 4: Complete Module")
    print("=" * 70)

    source = """
from typing import List, Optional

class User:
    name: str
    age: int
    email: str

    def __init__(self, name: str, age: int, email: str):
        self.name = name
        self.age = age
        self.email = email

    def is_adult(self) -> bool:
        return self.age >= 18

def find_user_by_email(users: List[User], email: str) -> Optional[User]:
    for user in users:
        if user.email == email:
            return user
    return None

def main():
    users = [
        User("Alice", 30, "alice@example.com"),
        User("Bob", 17, "bob@example.com")
    ]

    alice = find_user_by_email(users, "alice@example.com")
    if alice and alice.is_adult():
        print(f"{alice.name} is an adult")
"""

    print("Python Source:")
    print(source)
    print("\n" + "-" * 70)

    module = parse_python_source(source, "user_management")

    print("IR Module Structure:\n")
    print(f"Module Name: {module.name}")
    print(f"Version: {module.version}")
    print(f"\nImports: {len(module.imports)}")
    for imp in module.imports:
        if imp.items:
            print(f"  - from {imp.module} import {', '.join(imp.items)}")
        else:
            print(f"  - import {imp.module}")

    print(f"\nClasses: {len(module.classes)}")
    for cls in module.classes:
        print(f"  - {cls.name}")
        print(f"    Properties: {len(cls.properties)}")
        print(f"    Methods: {len(cls.methods)}")

    print(f"\nFunctions: {len(module.functions)}")
    for func in module.functions:
        params = ', '.join(f"{p.name}: {p.param_type.name}" for p in func.params)
        ret = func.return_type.name if func.return_type else "None"
        opt = "?" if func.return_type and func.return_type.is_optional else ""
        print(f"  - {func.name}({params}) -> {ret}{opt}")


def main():
    """Run all demos."""
    print("\n")
    print("*" * 70)
    print("*" + " " * 68 + "*")
    print("*" + "  Python Parser V2 - Live Demo".center(68) + "*")
    print("*" + " " * 68 + "*")
    print("*" * 70)

    demo_simple_function()
    demo_class_parsing()
    demo_type_inference()
    demo_complete_module()

    print("\n" + "=" * 70)
    print("Demo Complete!")
    print("=" * 70)
    print("\nThe Python Parser V2 successfully converts arbitrary Python code")
    print("into language-agnostic IR, enabling universal code translation.")
    print("\nNext: This IR can be translated to Go, Rust, .NET, Node.js, etc.")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    main()
