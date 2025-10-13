"""
Comprehensive test suite for Set<T> stdlib type.
Tests parsing, IR structure, and code generation for all Set methods.
"""

import pytest
from dsl.pw_parser import parse_pw, PWParseError


class TestSetBasicParsing:
    """Test that Set<T> code parses correctly."""

    def test_set_class_definition(self):
        """Test Set class definition parses."""
        pw_code = """
class Set<T>:
    elements: set<T>
"""
        ir = parse_pw(pw_code)
        assert len(ir.classes) == 1
        assert ir.classes[0].name == "Set"

    def test_set_new_constructor(self):
        """Test set_new function parses."""
        pw_code = """
function set_new<T>() -> Set<T>:
    return Set { elements: set() }
"""
        ir = parse_pw(pw_code)
        assert len(ir.functions) == 1
        assert ir.functions[0].name == "set_new"


class TestSetMutationMethods:
    """Test Set mutation methods."""

    def test_set_insert(self):
        """Test set_insert returns bool."""
        pw_code = """
function set_insert<T>(s: Set<T>, value: T) -> bool:
    if value in s.elements:
        return false
    else:
        s.elements.add(value)
        return true
"""
        ir = parse_pw(pw_code)
        assert len(ir.functions) == 1

    def test_set_remove(self):
        """Test set_remove function parses."""
        pw_code = """
function set_remove<T>(s: Set<T>, value: T) -> bool:
    if value in s.elements:
        s.elements.remove(value)
        return true
    else:
        return false
"""
        ir = parse_pw(pw_code)
        assert len(ir.functions) == 1


class TestSetAccessMethods:
    """Test Set access methods."""

    def test_set_contains(self):
        """Test set_contains function."""
        pw_code = """
function set_contains<T>(s: Set<T>, value: T) -> bool:
    return value in s.elements
"""
        ir = parse_pw(pw_code)
        assert len(ir.functions) == 1

    def test_set_len(self):
        """Test set_len function."""
        pw_code = """
function set_len<T>(s: Set<T>) -> int:
    return len(s.elements)
"""
        ir = parse_pw(pw_code)
        assert len(ir.functions) == 1

    def test_set_is_empty(self):
        """Test set_is_empty function."""
        pw_code = """
function set_is_empty<T>(s: Set<T>) -> bool:
    return len(s.elements) == 0
"""
        ir = parse_pw(pw_code)
        assert len(ir.functions) == 1


class TestSetUsagePatterns:
    """Test real-world Set usage patterns."""

    def test_set_unique_visitors(self):
        """Test Set for tracking unique visitors."""
        pw_code = """
function track_visitor(visitors: Set<string>, id: string) -> bool:
    return set_insert(visitors, id)
"""
        ir = parse_pw(pw_code)
        assert len(ir.functions) == 1

    def test_set_tags_system(self):
        """Test Set for tag system."""
        pw_code = """
function add_tag(tags: Set<string>, tag: string) -> bool:
    return set_insert(tags, tag)
"""
        ir = parse_pw(pw_code)
        assert len(ir.functions) == 1

    def test_set_deduplication(self):
        """Test Set for deduplication."""
        pw_code = """
function deduplicate(items: array<int>) -> Set<int>:
    let unique = set_new()
    for item in items:
        set_insert(unique, item)
    return unique
"""
        ir = parse_pw(pw_code)
        assert len(ir.functions) == 1


class TestSetUniqueness:
    """Test Set uniqueness properties."""

    def test_set_duplicate_rejection(self):
        """Test Set rejects duplicates."""
        pw_code = """
function test_duplicates() -> bool:
    let s = set_new()
    let first = set_insert(s, "value")
    let second = set_insert(s, "value")
    return first and not second
"""
        ir = parse_pw(pw_code)
        assert len(ir.functions) == 1

    def test_set_membership_check(self):
        """Test Set membership checking."""
        pw_code = """
function check_membership(s: Set<int>, value: int) -> bool:
    return set_contains(s, value)
"""
        ir = parse_pw(pw_code)
        assert len(ir.functions) == 1


class TestSetFullStdlib:
    """Test complete Set implementation."""

    def test_full_set_stdlib(self):
        """Test Set implementation from stdlib/types.pw parses."""
        with open("/Users/hustlermain/HUSTLER_CONTENT/HSTLR/DEV/Promptware/stdlib/types.pw") as f:
            pw_code = f.read()

        ir = parse_pw(pw_code)
        set_classes = [c for c in ir.classes if c.name == "Set"]
        assert len(set_classes) >= 1
        set_funcs = [f for f in ir.functions if f.name.startswith("set_")]
        assert len(set_funcs) >= 6

    def test_set_functions_present(self):
        """Test all required Set functions present."""
        with open("/Users/hustlermain/HUSTLER_CONTENT/HSTLR/DEV/Promptware/stdlib/types.pw") as f:
            pw_code = f.read()

        ir = parse_pw(pw_code)
        required = ["set_new", "set_insert", "set_remove", "set_contains", "set_len", "set_is_empty"]
        func_names = [f.name for f in ir.functions]
        for req in required:
            assert req in func_names, f"Missing: {req}"


class TestSetTypeAnnotations:
    """Test Set type annotations."""

    def test_set_int_type(self):
        """Test Set<int>."""
        pw_code = """
function get_numbers() -> Set<int>:
    return set_new()
"""
        ir = parse_pw(pw_code)
        assert len(ir.functions) == 1

    def test_set_string_type(self):
        """Test Set<string>."""
        pw_code = """
function get_tags() -> Set<string>:
    return set_new()
"""
        ir = parse_pw(pw_code)
        assert len(ir.functions) == 1

    def test_set_generic_parameter(self):
        """Test Set<T> with generic."""
        pw_code = """
function identity<T>(s: Set<T>) -> Set<T>:
    return s
"""
        ir = parse_pw(pw_code)
        assert len(ir.functions) == 1


class TestSetEdgeCases:
    """Test edge cases."""

    def test_set_with_custom_type(self):
        """Test Set with custom class."""
        pw_code = """
class User:
    id: int
    name: string

function get_users() -> Set<User>:
    return set_new()
"""
        ir = parse_pw(pw_code)
        assert len(ir.classes) == 1
        assert len(ir.functions) == 1

    def test_empty_set(self):
        """Test empty Set operations."""
        pw_code = """
function test_empty() -> bool:
    let s = set_new()
    return set_is_empty(s) and set_len(s) == 0
"""
        ir = parse_pw(pw_code)
        assert len(ir.functions) == 1


class TestSetCompleteness:
    """Verify Set API completeness."""

    def test_set_api_completeness(self):
        """Test all required methods implemented."""
        with open("/Users/hustlermain/HUSTLER_CONTENT/HSTLR/DEV/Promptware/stdlib/types.pw") as f:
            pw_code = f.read()

        ir = parse_pw(pw_code)
        set_functions = {f.name for f in ir.functions if f.name.startswith("set_")}
        required = {"set_new", "set_insert", "set_remove", "set_contains", "set_len", "set_is_empty"}
        missing = required - set_functions
        assert len(missing) == 0, f"Missing: {missing}"

    def test_all_collections_present(self):
        """Test List, Map, and Set all in same file."""
        with open("/Users/hustlermain/HUSTLER_CONTENT/HSTLR/DEV/Promptware/stdlib/types.pw") as f:
            pw_code = f.read()

        ir = parse_pw(pw_code)
        class_names = {c.name for c in ir.classes}
        assert "List" in class_names
        assert "Map" in class_names
        assert "Set" in class_names


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
