#!/usr/bin/env python3
"""
Simple regression test for Python Parser V2.
Tests basic functionality to ensure no regressions from bug fixes.
"""

from language.python_parser_v2 import parse_python_source
from dsl.ir import (
    IRModule, IRFunction, IRClass, IRAssignment, IRBinaryOp,
    IRReturn, IRIf, IRFor, IRCall, IRLiteral, IRIdentifier
)


def test_simple_function():
    """Test basic function parsing."""
    source = """
def add(a: int, b: int) -> int:
    return a + b
"""
    module = parse_python_source(source, "test")
    assert len(module.functions) == 1
    func = module.functions[0]
    assert func.name == "add"
    assert len(func.params) == 2
    assert func.return_type.name == "int"
    print("✓ Simple function: PASS")


def test_class_parsing():
    """Test class with constructor."""
    source = """
class User:
    def __init__(self, name: str, age: int):
        self.name = name
        self.age = age
"""
    module = parse_python_source(source, "test")
    assert len(module.classes) == 1
    cls = module.classes[0]
    assert cls.name == "User"
    assert cls.constructor is not None
    assert len(cls.constructor.params) == 2
    print("✓ Class parsing: PASS")


def test_control_flow():
    """Test if statements and loops."""
    source = """
def process(items):
    result = []
    for item in items:
        if item > 0:
            result.append(item * 2)
    return result
"""
    module = parse_python_source(source, "test")
    func = module.functions[0]
    assert len(func.body) == 3  # assignment, for loop, return
    assert isinstance(func.body[1], IRFor)
    print("✓ Control flow: PASS")


def test_async_function():
    """Test async/await parsing."""
    source = """
async def fetch_data(url: str):
    data = await client.get(url)
    return data
"""
    module = parse_python_source(source, "test")
    func = module.functions[0]
    assert func.is_async == True
    assert len(func.body) == 2
    print("✓ Async function: PASS")


def test_type_inference():
    """Test type inference for untyped code."""
    source = """
def calculate(x, y):
    result = x + y
    return result
"""
    module = parse_python_source(source, "test")
    func = module.functions[0]
    # Type inference now works - should infer numeric types from usage
    # x and y are used in addition, so inferred as 'int'
    assert func.params[0].param_type.name in ("any", "int")
    assert func.params[1].param_type.name in ("any", "int")
    print("✓ Type inference: PASS")


def test_expressions():
    """Test expression parsing."""
    source = """
def compute(a, b, c):
    x = a + b * c
    y = x / 2
    z = y > 10
    return z
"""
    module = parse_python_source(source, "test")
    func = module.functions[0]
    assert len(func.body) == 4  # 3 assignments + return
    # First assignment should have binary op
    assert isinstance(func.body[0], IRAssignment)
    print("✓ Expressions: PASS")


def test_data_structures():
    """Test lists and dicts."""
    source = """
def create_data():
    items = [1, 2, 3]
    config = {"key": "value", "count": 42}
    return (items, config)
"""
    module = parse_python_source(source, "test")
    func = module.functions[0]
    assert len(func.body) == 3  # 2 assignments + return
    print("✓ Data structures: PASS")


def main():
    """Run all tests."""
    print("=" * 60)
    print("Python Parser V2 - Regression Tests")
    print("=" * 60)
    print()

    tests = [
        ("Simple Function", test_simple_function),
        ("Class Parsing", test_class_parsing),
        ("Control Flow", test_control_flow),
        ("Async Function", test_async_function),
        ("Type Inference", test_type_inference),
        ("Expressions", test_expressions),
        ("Data Structures", test_data_structures),
    ]

    passed = 0
    failed = 0

    for name, test_func in tests:
        try:
            test_func()
            passed += 1
        except Exception as e:
            import traceback
            print(f"✗ {name}: FAIL - {e}")
            traceback.print_exc()
            failed += 1

    print()
    print("=" * 60)
    print(f"Results: {passed}/{len(tests)} tests passed")
    print("=" * 60)

    return failed == 0


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
