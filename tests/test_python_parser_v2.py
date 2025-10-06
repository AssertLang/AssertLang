"""
Tests for Python Parser V2: Arbitrary Python code → IR

Test coverage:
- Simple functions with type hints
- Functions without type hints (type inference)
- Classes with methods and properties
- Control flow: if, for, while, try/except
- Expressions: arithmetic, logical, function calls
- Data structures: lists, dicts
- Edge cases and complex scenarios
"""

import pytest

from language.python_parser_v2 import PythonParserV2, parse_python_source
from dsl.ir import (
    BinaryOperator,
    IRAssignment,
    IRBinaryOp,
    IRCall,
    IRClass,
    IRFor,
    IRFunction,
    IRIdentifier,
    IRIf,
    IRLiteral,
    IRModule,
    IRParameter,
    IRPropertyAccess,
    IRReturn,
    IRTry,
    IRType,
    IRWhile,
    LiteralType,
)


class TestSimpleFunctions:
    """Test parsing of simple functions."""

    def test_function_with_type_hints(self):
        """Test function with full type annotations."""
        source = """
def add(a: int, b: int) -> int:
    return a + b
"""
        module = parse_python_source(source, "test")

        assert len(module.functions) == 1
        func = module.functions[0]
        assert func.name == "add"
        assert len(func.params) == 2
        assert func.params[0].name == "a"
        assert func.params[0].param_type.name == "int"
        assert func.params[1].name == "b"
        assert func.params[1].param_type.name == "int"
        assert func.return_type.name == "int"
        assert len(func.body) == 1
        assert isinstance(func.body[0], IRReturn)

    def test_function_without_type_hints(self):
        """Test function without type annotations (type inference)."""
        source = """
def multiply(x, y):
    return x * y
"""
        module = parse_python_source(source, "test")

        assert len(module.functions) == 1
        func = module.functions[0]
        assert func.name == "multiply"
        assert len(func.params) == 2
        # Should infer 'any' type for unannotated params
        assert func.params[0].param_type.name == "any"
        assert func.params[1].param_type.name == "any"

    def test_function_with_default_arguments(self):
        """Test function with default argument values."""
        source = """
def greet(name: str, greeting: str = "Hello") -> str:
    return greeting + " " + name
"""
        module = parse_python_source(source, "test")

        func = module.functions[0]
        assert func.name == "greet"
        assert len(func.params) == 2
        assert func.params[0].name == "name"
        assert func.params[0].default_value is None
        assert func.params[1].name == "greeting"
        assert func.params[1].default_value is not None
        assert isinstance(func.params[1].default_value, IRLiteral)
        assert func.params[1].default_value.value == "Hello"

    def test_async_function(self):
        """Test async function parsing."""
        source = """
async def fetch_data(url: str) -> dict:
    return {}
"""
        module = parse_python_source(source, "test")

        func = module.functions[0]
        assert func.name == "fetch_data"
        assert func.is_async is True


class TestClasses:
    """Test parsing of classes."""

    def test_simple_class_with_methods(self):
        """Test class with methods."""
        source = """
class Counter:
    def __init__(self):
        self.count = 0

    def increment(self):
        self.count = self.count + 1
        return self.count
"""
        module = parse_python_source(source, "test")

        assert len(module.classes) == 1
        cls = module.classes[0]
        assert cls.name == "Counter"
        assert cls.constructor is not None
        assert cls.constructor.name == "__init__"
        assert len(cls.methods) == 1
        assert cls.methods[0].name == "increment"

    def test_class_with_type_annotated_properties(self):
        """Test class with type-annotated properties."""
        source = """
class User:
    name: str
    age: int
    email: str

    def __init__(self, name: str, age: int):
        self.name = name
        self.age = age
"""
        module = parse_python_source(source, "test")

        cls = module.classes[0]
        assert cls.name == "User"
        assert len(cls.properties) == 3
        assert cls.properties[0].name == "name"
        assert cls.properties[0].prop_type.name == "string"
        assert cls.properties[1].name == "age"
        assert cls.properties[1].prop_type.name == "int"

    def test_class_with_base_class(self):
        """Test class inheritance."""
        source = """
class Animal:
    def speak(self):
        pass

class Dog(Animal):
    def speak(self):
        return "Woof"
"""
        module = parse_python_source(source, "test")

        assert len(module.classes) == 2
        dog_class = module.classes[1]
        assert dog_class.name == "Dog"
        assert len(dog_class.base_classes) == 1
        assert dog_class.base_classes[0] == "Animal"


class TestControlFlow:
    """Test parsing of control flow statements."""

    def test_if_statement(self):
        """Test if/else statement."""
        source = """
def check_value(x: int) -> str:
    if x > 0:
        return "positive"
    else:
        return "non-positive"
"""
        module = parse_python_source(source, "test")

        func = module.functions[0]
        assert len(func.body) == 1
        if_stmt = func.body[0]
        assert isinstance(if_stmt, IRIf)
        assert isinstance(if_stmt.condition, IRBinaryOp)
        assert if_stmt.condition.op == BinaryOperator.GREATER_THAN
        assert len(if_stmt.then_body) == 1
        assert len(if_stmt.else_body) == 1

    def test_for_loop(self):
        """Test for loop."""
        source = """
def sum_list(numbers: list) -> int:
    total = 0
    for num in numbers:
        total = total + num
    return total
"""
        module = parse_python_source(source, "test")

        func = module.functions[0]
        # Find the for loop in body
        for_loop = None
        for stmt in func.body:
            if isinstance(stmt, IRFor):
                for_loop = stmt
                break

        assert for_loop is not None
        assert for_loop.iterator == "num"
        assert isinstance(for_loop.iterable, IRIdentifier)
        assert len(for_loop.body) == 1

    def test_while_loop(self):
        """Test while loop."""
        source = """
def countdown(n: int) -> int:
    while n > 0:
        n = n - 1
    return n
"""
        module = parse_python_source(source, "test")

        func = module.functions[0]
        while_loop = None
        for stmt in func.body:
            if isinstance(stmt, IRWhile):
                while_loop = stmt
                break

        assert while_loop is not None
        assert isinstance(while_loop.condition, IRBinaryOp)
        assert len(while_loop.body) == 1

    def test_try_except(self):
        """Test try/except statement."""
        source = """
def safe_divide(a: int, b: int) -> float:
    try:
        return a / b
    except ZeroDivisionError as e:
        return 0.0
"""
        module = parse_python_source(source, "test")

        func = module.functions[0]
        try_stmt = None
        for stmt in func.body:
            if isinstance(stmt, IRTry):
                try_stmt = stmt
                break

        assert try_stmt is not None
        assert len(try_stmt.try_body) == 1
        assert len(try_stmt.catch_blocks) == 1
        assert try_stmt.catch_blocks[0].exception_type == "ZeroDivisionError"
        assert try_stmt.catch_blocks[0].exception_var == "e"


class TestExpressions:
    """Test parsing of expressions."""

    def test_arithmetic_operations(self):
        """Test arithmetic binary operations."""
        source = """
def calculate(a: int, b: int) -> int:
    return a + b - a * b / 2
"""
        module = parse_python_source(source, "test")

        func = module.functions[0]
        ret_stmt = func.body[0]
        assert isinstance(ret_stmt, IRReturn)
        assert isinstance(ret_stmt.value, IRBinaryOp)

    def test_comparison_operations(self):
        """Test comparison operations."""
        source = """
def compare(a: int, b: int) -> bool:
    return a < b
"""
        module = parse_python_source(source, "test")

        func = module.functions[0]
        ret_stmt = func.body[0]
        assert isinstance(ret_stmt, IRReturn)
        assert isinstance(ret_stmt.value, IRBinaryOp)
        assert ret_stmt.value.op == BinaryOperator.LESS_THAN

    def test_function_call(self):
        """Test function call expression."""
        source = """
def process():
    result = calculate(10, 20)
    return result
"""
        module = parse_python_source(source, "test")

        func = module.functions[0]
        # First statement should be assignment with call
        assign = func.body[0]
        assert isinstance(assign, IRAssignment)
        assert isinstance(assign.value, IRCall)
        call = assign.value
        assert isinstance(call.function, IRIdentifier)
        assert call.function.name == "calculate"
        assert len(call.args) == 2

    def test_property_access(self):
        """Test property/attribute access."""
        source = """
def get_name(user):
    return user.name
"""
        module = parse_python_source(source, "test")

        func = module.functions[0]
        ret_stmt = func.body[0]
        assert isinstance(ret_stmt, IRReturn)
        assert isinstance(ret_stmt.value, IRPropertyAccess)
        assert ret_stmt.value.property == "name"


class TestDataStructures:
    """Test parsing of data structures."""

    def test_list_literal(self):
        """Test list literal parsing."""
        source = """
def get_numbers():
    return [1, 2, 3, 4, 5]
"""
        module = parse_python_source(source, "test")

        func = module.functions[0]
        ret_stmt = func.body[0]
        assert isinstance(ret_stmt, IRReturn)
        from dsl.ir import IRArray
        assert isinstance(ret_stmt.value, IRArray)
        assert len(ret_stmt.value.elements) == 5

    def test_dict_literal(self):
        """Test dict literal parsing."""
        source = """
def get_user():
    return {"name": "John", "age": 30}
"""
        module = parse_python_source(source, "test")

        func = module.functions[0]
        ret_stmt = func.body[0]
        assert isinstance(ret_stmt, IRReturn)
        from dsl.ir import IRMap
        assert isinstance(ret_stmt.value, IRMap)
        assert len(ret_stmt.value.entries) == 2
        assert "name" in ret_stmt.value.entries
        assert "age" in ret_stmt.value.entries


class TestTypeAnnotations:
    """Test type annotation parsing."""

    def test_optional_type(self):
        """Test Optional[T] type annotation."""
        source = """
from typing import Optional

def find_user(user_id: str) -> Optional[str]:
    return None
"""
        module = parse_python_source(source, "test")

        func = module.functions[0]
        assert func.return_type is not None
        assert func.return_type.is_optional is True
        assert func.return_type.name == "string"

    def test_list_type(self):
        """Test List[T] type annotation."""
        source = """
from typing import List

def get_names() -> List[str]:
    return []
"""
        module = parse_python_source(source, "test")

        func = module.functions[0]
        assert func.return_type is not None
        assert func.return_type.name == "array"
        assert len(func.return_type.generic_args) == 1
        assert func.return_type.generic_args[0].name == "string"

    def test_dict_type(self):
        """Test Dict[K, V] type annotation."""
        source = """
from typing import Dict

def get_config() -> Dict[str, int]:
    return {}
"""
        module = parse_python_source(source, "test")

        func = module.functions[0]
        assert func.return_type is not None
        assert func.return_type.name == "map"
        assert len(func.return_type.generic_args) == 2
        assert func.return_type.generic_args[0].name == "string"
        assert func.return_type.generic_args[1].name == "int"


class TestTypeInference:
    """Test type inference for unannotated code."""

    def test_infer_int_from_literal(self):
        """Test type inference from integer literal."""
        source = """
def get_count():
    count = 42
    return count
"""
        module = parse_python_source(source, "test")

        func = module.functions[0]
        # First statement is assignment
        assign = func.body[0]
        assert isinstance(assign, IRAssignment)
        assert assign.var_type.name == "int"

    def test_infer_string_from_literal(self):
        """Test type inference from string literal."""
        source = """
def get_name():
    name = "Alice"
    return name
"""
        module = parse_python_source(source, "test")

        func = module.functions[0]
        assign = func.body[0]
        assert isinstance(assign, IRAssignment)
        assert assign.var_type.name == "string"


class TestImports:
    """Test import statement parsing."""

    def test_simple_import(self):
        """Test simple import statement."""
        source = """
import os
import sys
"""
        module = parse_python_source(source, "test")

        assert len(module.imports) == 2
        assert module.imports[0].module == "os"
        assert module.imports[1].module == "sys"

    def test_import_with_alias(self):
        """Test import with alias."""
        source = """
import numpy as np
"""
        module = parse_python_source(source, "test")

        assert len(module.imports) == 1
        assert module.imports[0].module == "numpy"
        assert module.imports[0].alias == "np"

    def test_from_import(self):
        """Test from...import statement."""
        source = """
from typing import List, Dict, Optional
"""
        module = parse_python_source(source, "test")

        assert len(module.imports) == 1
        assert module.imports[0].module == "typing"
        assert len(module.imports[0].items) == 3
        assert "List" in module.imports[0].items
        assert "Dict" in module.imports[0].items
        assert "Optional" in module.imports[0].items


class TestComplexScenarios:
    """Test complex real-world scenarios."""

    def test_payment_processor(self):
        """Test parsing a complete payment processor class."""
        source = """
from typing import Optional

class PaymentProcessor:
    api_key: str
    base_url: str

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.example.com"

    def process_payment(self, amount: float, user_id: str) -> dict:
        if amount <= 0:
            raise ValueError("Amount must be positive")

        result = {
            "status": "completed",
            "amount": amount,
            "user_id": user_id
        }
        return result
"""
        module = parse_python_source(source, "test")

        assert len(module.classes) == 1
        cls = module.classes[0]
        assert cls.name == "PaymentProcessor"
        assert len(cls.properties) == 2
        assert cls.constructor is not None
        assert len(cls.methods) == 1
        assert cls.methods[0].name == "process_payment"

        # Check method throws
        method = cls.methods[0]
        assert "ValueError" in method.throws

    def test_recursive_function(self):
        """Test recursive function parsing."""
        source = """
def factorial(n: int) -> int:
    if n <= 1:
        return 1
    return n * factorial(n - 1)
"""
        module = parse_python_source(source, "test")

        func = module.functions[0]
        assert func.name == "factorial"
        # Should have if statement in body
        assert isinstance(func.body[0], IRIf)

    def test_nested_control_flow(self):
        """Test nested if/for statements."""
        source = """
def process_items(items: list) -> int:
    count = 0
    for item in items:
        if item > 0:
            count = count + 1
    return count
"""
        module = parse_python_source(source, "test")

        func = module.functions[0]
        # Find for loop
        for_loop = None
        for stmt in func.body:
            if isinstance(stmt, IRFor):
                for_loop = stmt
                break

        assert for_loop is not None
        # For loop should contain if statement
        assert any(isinstance(s, IRIf) for s in for_loop.body)


class TestEdgeCases:
    """Test edge cases and error handling."""

    def test_empty_function(self):
        """Test function with only pass statement."""
        source = """
def do_nothing():
    pass
"""
        module = parse_python_source(source, "test")

        func = module.functions[0]
        assert func.name == "do_nothing"
        # Pass statement should be in body
        from dsl.ir import IRPass
        assert len(func.body) == 1
        assert isinstance(func.body[0], IRPass)

    def test_function_with_docstring(self):
        """Test function with docstring."""
        source = '''
def greet(name: str) -> str:
    """Greet a person by name."""
    return "Hello, " + name
'''
        module = parse_python_source(source, "test")

        func = module.functions[0]
        assert func.doc == "Greet a person by name."

    def test_class_with_docstring(self):
        """Test class with docstring."""
        source = '''
class User:
    """Represents a user in the system."""
    pass
'''
        module = parse_python_source(source, "test")

        cls = module.classes[0]
        assert cls.doc == "Represents a user in the system."


# ============================================================================
# Integration Tests
# ============================================================================


class TestEndToEnd:
    """End-to-end integration tests."""

    def test_complete_module(self):
        """Test parsing a complete module with multiple constructs."""
        source = """
from typing import List, Optional

class User:
    name: str
    age: int

    def __init__(self, name: str, age: int):
        self.name = name
        self.age = age

def find_user(users: List[User], name: str) -> Optional[User]:
    for user in users:
        if user.name == name:
            return user
    return None

def main():
    users = []
    user = User("Alice", 30)
    users.append(user)
    found = find_user(users, "Alice")
    return found
"""
        module = parse_python_source(source, "test_module")

        # Check module structure
        assert module.name == "test_module"
        assert len(module.imports) == 1
        assert len(module.classes) == 1
        assert len(module.functions) == 2

        # Check class
        cls = module.classes[0]
        assert cls.name == "User"
        assert len(cls.properties) == 2

        # Check functions
        find_func = module.functions[0]
        assert find_func.name == "find_user"
        assert find_func.return_type.is_optional is True

        main_func = module.functions[1]
        assert main_func.name == "main"


# ============================================================================
# Run Tests
# ============================================================================

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
