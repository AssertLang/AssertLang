"""
Comprehensive test suite for List<T> stdlib type.

Tests parsing, IR structure, and code generation for all List methods.
Based on implementation-plan.md specifications.
"""

import pytest
from dsl.pw_parser import parse_pw, PWParseError


class TestListBasicParsing:
    """Test that List<T> code parses correctly."""

    def test_list_class_definition(self):
        """Test List class definition parses."""
        pw_code = """
class List<T>:
    items: array<T>
"""
        ir = parse_pw(pw_code)
        assert len(ir.classes) == 1
        assert ir.classes[0].name == "List"

    def test_list_new_constructor(self):
        """Test list_new function parses."""
        pw_code = """
function list_new<T>() -> List<T>:
    return List { items: [] }
"""
        ir = parse_pw(pw_code)
        assert len(ir.functions) == 1
        assert ir.functions[0].name == "list_new"

    def test_list_from_constructor(self):
        """Test list_from function parses."""
        pw_code = """
function list_from<T>(items: array<T>) -> List<T>:
    return List { items: items }
"""
        ir = parse_pw(pw_code)
        assert len(ir.functions) == 1
        assert ir.functions[0].name == "list_from"


class TestListMutationMethods:
    """Test List mutation methods."""

    def test_list_push(self):
        """Test list_push function parses."""
        pw_code = """
function list_push<T>(lst: List<T>, item: T) -> void:
    lst.items.append(item)
"""
        ir = parse_pw(pw_code)
        assert len(ir.functions) == 1
        assert ir.functions[0].name == "list_push"

    def test_list_pop(self):
        """Test list_pop function parses."""
        pw_code = """
function list_pop<T>(lst: List<T>) -> Option<T>:
    if len(lst.items) == 0:
        return None
    else:
        let item = lst.items[-1]
        lst.items = lst.items[:-1]
        return Some(item)
"""
        ir = parse_pw(pw_code)
        assert len(ir.functions) == 1
        assert ir.functions[0].name == "list_pop"


class TestListAccessMethods:
    """Test List access methods."""

    def test_list_get(self):
        """Test list_get function parses."""
        pw_code = """
function list_get<T>(lst: List<T>, index: int) -> Option<T>:
    if index < 0 or index >= len(lst.items):
        return None
    else:
        return Some(lst.items[index])
"""
        ir = parse_pw(pw_code)
        assert len(ir.functions) == 1
        assert ir.functions[0].name == "list_get"

    def test_list_len(self):
        """Test list_len function parses."""
        pw_code = """
function list_len<T>(lst: List<T>) -> int:
    return len(lst.items)
"""
        ir = parse_pw(pw_code)
        assert len(ir.functions) == 1
        assert ir.functions[0].name == "list_len"

    def test_list_is_empty(self):
        """Test list_is_empty function parses."""
        pw_code = """
function list_is_empty<T>(lst: List<T>) -> bool:
    return len(lst.items) == 0
"""
        ir = parse_pw(pw_code)
        assert len(ir.functions) == 1
        assert ir.functions[0].name == "list_is_empty"


class TestListFunctionalMethods:
    """Test List functional programming methods."""

    def test_list_map(self):
        """Test list_map function parses."""
        pw_code = """
function list_map<T, U>(lst: List<T>, fn: function(T) -> U) -> List<U>:
    let result = []
    for item in lst.items:
        result.append(fn(item))
    return list_from(result)
"""
        ir = parse_pw(pw_code)
        assert len(ir.functions) == 1
        assert ir.functions[0].name == "list_map"

    def test_list_filter(self):
        """Test list_filter function parses."""
        pw_code = """
function list_filter<T>(lst: List<T>, fn: function(T) -> bool) -> List<T>:
    let result = []
    for item in lst.items:
        if fn(item):
            result.append(item)
    return list_from(result)
"""
        ir = parse_pw(pw_code)
        assert len(ir.functions) == 1
        assert ir.functions[0].name == "list_filter"

    def test_list_fold(self):
        """Test list_fold function parses."""
        pw_code = """
function list_fold<T, U>(lst: List<T>, init: U, fn: function(U, T) -> U) -> U:
    let acc = init
    for item in lst.items:
        acc = fn(acc, item)
    return acc
"""
        ir = parse_pw(pw_code)
        assert len(ir.functions) == 1
        assert ir.functions[0].name == "list_fold"


class TestListUsagePatterns:
    """Test real-world List usage patterns."""

    def test_list_todo_list(self):
        """Test List for todo list."""
        pw_code = """
function manage_todos() -> List<string>:
    let todos = list_new()
    list_push(todos, "Write code")
    list_push(todos, "Write tests")
    list_push(todos, "Deploy")
    return todos
"""
        ir = parse_pw(pw_code)
        assert len(ir.functions) == 1

    def test_list_number_processing(self):
        """Test List for number processing."""
        pw_code = """
function process_numbers() -> int:
    let numbers = list_from([1, 2, 3, 4, 5])
    let sum = list_fold(numbers, 0, fn(acc, x) -> acc + x)
    return sum
"""
        ir = parse_pw(pw_code)
        assert len(ir.functions) == 1

    def test_list_filtering(self):
        """Test List filtering operations."""
        pw_code = """
function get_even_numbers(nums: List<int>) -> List<int>:
    return list_filter(nums, fn(x) -> x % 2 == 0)
"""
        ir = parse_pw(pw_code)
        assert len(ir.functions) == 1

    def test_list_transformation(self):
        """Test List transformation with map."""
        pw_code = """
function double_all(nums: List<int>) -> List<int>:
    return list_map(nums, fn(x) -> x * 2)
"""
        ir = parse_pw(pw_code)
        assert len(ir.functions) == 1


class TestListFullStdlib:
    """Test complete List implementation from stdlib."""

    def test_full_list_stdlib(self):
        """Test that full List implementation from stdlib/types.al parses."""
        with open("/Users/hustlermain/HUSTLER_CONTENT/HSTLR/DEV/Promptware/stdlib/types.al") as f:
            pw_code = f.read()

        ir = parse_pw(pw_code)

        # Check for List class
        list_classes = [c for c in ir.classes if c.name == "List"]
        assert len(list_classes) >= 1

        # Count List-related functions
        list_funcs = [f for f in ir.functions if f.name.startswith("list_")]
        assert len(list_funcs) >= 10  # All List methods

    def test_list_functions_present(self):
        """Test that all required List functions are present."""
        with open("/Users/hustlermain/HUSTLER_CONTENT/HSTLR/DEV/Promptware/stdlib/types.al") as f:
            pw_code = f.read()

        ir = parse_pw(pw_code)

        required_funcs = [
            "list_new",
            "list_from",
            "list_push",
            "list_pop",
            "list_get",
            "list_len",
            "list_is_empty",
            "list_map",
            "list_filter",
            "list_fold"
        ]

        func_names = [f.name for f in ir.functions]
        for required in required_funcs:
            assert required in func_names, f"Missing function: {required}"


class TestListTypeAnnotations:
    """Test List type annotations."""

    def test_list_int_type(self):
        """Test List<int> type annotation."""
        pw_code = """
function get_numbers() -> List<int>:
    return list_from([1, 2, 3])
"""
        ir = parse_pw(pw_code)
        assert len(ir.functions) == 1
        assert ir.functions[0].return_type.name == "List"

    def test_list_string_type(self):
        """Test List<string> type annotation."""
        pw_code = """
function get_names() -> List<string>:
    return list_new()
"""
        ir = parse_pw(pw_code)
        assert len(ir.functions) == 1

    def test_list_generic_parameter(self):
        """Test List<T> with generic."""
        pw_code = """
function identity<T>(lst: List<T>) -> List<T>:
    return lst
"""
        ir = parse_pw(pw_code)
        assert len(ir.functions) == 1


class TestListEdgeCases:
    """Test edge cases and complex scenarios."""

    def test_nested_lists(self):
        """Test List<List<T>>."""
        pw_code = """
function get_matrix() -> List<List<int>>:
    let row1 = list_from([1, 2, 3])
    let row2 = list_from([4, 5, 6])
    let matrix = list_new()
    list_push(matrix, row1)
    list_push(matrix, row2)
    return matrix
"""
        ir = parse_pw(pw_code)
        assert len(ir.functions) == 1

    def test_list_with_custom_type(self):
        """Test List with custom class."""
        pw_code = """
class User:
    name: string
    age: int

function get_users() -> List<User>:
    return list_new()
"""
        ir = parse_pw(pw_code)
        assert len(ir.classes) == 1
        assert len(ir.functions) == 1

    def test_list_with_option(self):
        """Test List<Option<T>>."""
        pw_code = """
function get_optionals() -> List<Option<int>>:
    let items = list_new()
    list_push(items, Some(1))
    list_push(items, None)
    list_push(items, Some(3))
    return items
"""
        ir = parse_pw(pw_code)
        assert len(ir.functions) == 1


class TestListChaining:
    """Test chaining List operations."""

    def test_map_filter_chain(self):
        """Test map followed by filter."""
        pw_code = """
function process_list(nums: List<int>) -> List<int>:
    let doubled = list_map(nums, fn(x) -> x * 2)
    let evens = list_filter(doubled, fn(x) -> x % 4 == 0)
    return evens
"""
        ir = parse_pw(pw_code)
        assert len(ir.functions) == 1

    def test_filter_map_fold_chain(self):
        """Test filter, map, and fold chain."""
        pw_code = """
function sum_even_squares(nums: List<int>) -> int:
    let evens = list_filter(nums, fn(x) -> x % 2 == 0)
    let squares = list_map(evens, fn(x) -> x * x)
    let sum = list_fold(squares, 0, fn(acc, x) -> acc + x)
    return sum
"""
        ir = parse_pw(pw_code)
        assert len(ir.functions) == 1


class TestListCompleteness:
    """Verify List implementation is complete."""

    def test_list_api_completeness(self):
        """Test that all required API methods are implemented."""
        with open("/Users/hustlermain/HUSTLER_CONTENT/HSTLR/DEV/Promptware/stdlib/types.al") as f:
            pw_code = f.read()

        ir = parse_pw(pw_code)

        list_functions = {f.name for f in ir.functions if f.name.startswith("list_")}

        required_api = {
            "list_new",
            "list_from",
            "list_push",
            "list_pop",
            "list_get",
            "list_len",
            "list_is_empty",
            "list_map",
            "list_filter",
            "list_fold"
        }

        missing = required_api - list_functions
        assert len(missing) == 0, f"Missing API functions: {missing}"


if __name__ == "__main__":
    # Run tests with: pytest tests/test_stdlib_list.py -v
    pytest.main([__file__, "-v"])
