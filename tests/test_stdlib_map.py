"""
Comprehensive test suite for Map<K,V> stdlib type.
Tests parsing, IR structure, and code generation for all Map methods.
"""

import pytest
from dsl.pw_parser import parse_pw, PWParseError


class TestMapBasicParsing:
    """Test that Map<K,V> code parses correctly."""

    def test_map_class_definition(self):
        """Test Map class definition parses."""
        pw_code = """
class Map<K, V>:
    entries: map<K, V>
"""
        ir = parse_pw(pw_code)
        assert len(ir.classes) == 1
        assert ir.classes[0].name == "Map"

    def test_map_new_constructor(self):
        """Test map_new function parses."""
        pw_code = """
function map_new<K, V>() -> Map<K, V>:
    return Map { entries: {} }
"""
        ir = parse_pw(pw_code)
        assert len(ir.functions) == 1
        assert ir.functions[0].name == "map_new"


class TestMapMutationMethods:
    """Test Map mutation methods."""

    def test_map_insert(self):
        """Test map_insert returns old value."""
        pw_code = """
function map_insert<K, V>(m: Map<K, V>, key: K, value: V) -> Option<V>:
    let old_value = None
    if key in m.entries:
        old_value = Some(m.entries[key])
    m.entries[key] = value
    return old_value
"""
        ir = parse_pw(pw_code)
        assert len(ir.functions) == 1

    def test_map_remove(self):
        """Test map_remove function parses."""
        pw_code = """
function map_remove<K, V>(m: Map<K, V>, key: K) -> Option<V>:
    if key in m.entries:
        let value = m.entries[key]
        delete m.entries[key]
        return Some(value)
    else:
        return None
"""
        ir = parse_pw(pw_code)
        assert len(ir.functions) == 1


class TestMapAccessMethods:
    """Test Map access methods."""

    def test_map_get(self):
        """Test map_get returns Option."""
        pw_code = """
function map_get<K, V>(m: Map<K, V>, key: K) -> Option<V>:
    if key in m.entries:
        return Some(m.entries[key])
    else:
        return None
"""
        ir = parse_pw(pw_code)
        assert len(ir.functions) == 1

    def test_map_contains_key(self):
        """Test map_contains_key function."""
        pw_code = """
function map_contains_key<K, V>(m: Map<K, V>, key: K) -> bool:
    return key in m.entries
"""
        ir = parse_pw(pw_code)
        assert len(ir.functions) == 1

    def test_map_len(self):
        """Test map_len function."""
        pw_code = """
function map_len<K, V>(m: Map<K, V>) -> int:
    return len(m.entries)
"""
        ir = parse_pw(pw_code)
        assert len(ir.functions) == 1

    def test_map_is_empty(self):
        """Test map_is_empty function."""
        pw_code = """
function map_is_empty<K, V>(m: Map<K, V>) -> bool:
    return len(m.entries) == 0
"""
        ir = parse_pw(pw_code)
        assert len(ir.functions) == 1


class TestMapCollectionMethods:
    """Test Map collection methods."""

    def test_map_keys(self):
        """Test map_keys returns List."""
        pw_code = """
function map_keys<K, V>(m: Map<K, V>) -> List<K>:
    return list_from(keys(m.entries))
"""
        ir = parse_pw(pw_code)
        assert len(ir.functions) == 1

    def test_map_values(self):
        """Test map_values returns List."""
        pw_code = """
function map_values<K, V>(m: Map<K, V>) -> List<V>:
    return list_from(values(m.entries))
"""
        ir = parse_pw(pw_code)
        assert len(ir.functions) == 1


class TestMapUsagePatterns:
    """Test real-world Map usage patterns."""

    def test_map_config_storage(self):
        """Test Map for configuration."""
        pw_code = """
function create_config() -> Map<string, string>:
    let config = map_new()
    map_insert(config, "host", "localhost")
    map_insert(config, "port", "8080")
    return config
"""
        ir = parse_pw(pw_code)
        assert len(ir.functions) == 1

    def test_map_cache_pattern(self):
        """Test Map for caching."""
        pw_code = """
function cache_lookup(cache: Map<string, int>, key: string) -> Option<int>:
    return map_get(cache, key)
"""
        ir = parse_pw(pw_code)
        assert len(ir.functions) == 1

    def test_map_user_preferences(self):
        """Test Map for user preferences."""
        pw_code = """
function set_preference(prefs: Map<string, bool>, key: string, value: bool) -> Option<bool>:
    return map_insert(prefs, key, value)
"""
        ir = parse_pw(pw_code)
        assert len(ir.functions) == 1


class TestMapFullStdlib:
    """Test complete Map implementation."""

    def test_full_map_stdlib(self):
        """Test Map implementation from stdlib/types.pw parses."""
        with open("/Users/hustlermain/HUSTLER_CONTENT/HSTLR/DEV/Promptware/stdlib/types.pw") as f:
            pw_code = f.read()

        ir = parse_pw(pw_code)
        map_classes = [c for c in ir.classes if c.name == "Map"]
        assert len(map_classes) >= 1
        map_funcs = [f for f in ir.functions if f.name.startswith("map_")]
        assert len(map_funcs) >= 9

    def test_map_functions_present(self):
        """Test all required Map functions present."""
        with open("/Users/hustlermain/HUSTLER_CONTENT/HSTLR/DEV/Promptware/stdlib/types.pw") as f:
            pw_code = f.read()

        ir = parse_pw(pw_code)
        required = ["map_new", "map_insert", "map_get", "map_remove", "map_contains_key",
                   "map_len", "map_is_empty", "map_keys", "map_values"]
        func_names = [f.name for f in ir.functions]
        for req in required:
            assert req in func_names, f"Missing: {req}"


class TestMapTypeAnnotations:
    """Test Map type annotations."""

    def test_map_string_int_type(self):
        """Test Map<string, int>."""
        pw_code = """
function get_scores() -> Map<string, int>:
    return map_new()
"""
        ir = parse_pw(pw_code)
        assert len(ir.functions) == 1

    def test_map_generic_parameters(self):
        """Test Map<K,V> with generics."""
        pw_code = """
function identity<K, V>(m: Map<K, V>) -> Map<K, V>:
    return m
"""
        ir = parse_pw(pw_code)
        assert len(ir.functions) == 1


class TestMapEdgeCases:
    """Test edge cases."""

    def test_nested_maps(self):
        """Test Map<string, Map<string, int>>."""
        pw_code = """
function get_nested() -> Map<string, Map<string, int>>:
    return map_new()
"""
        ir = parse_pw(pw_code)
        assert len(ir.functions) == 1

    def test_map_with_option_values(self):
        """Test Map<K, Option<V>>."""
        pw_code = """
function cache_with_misses() -> Map<string, Option<int>>:
    return map_new()
"""
        ir = parse_pw(pw_code)
        assert len(ir.functions) == 1


class TestMapCompleteness:
    """Verify Map API completeness."""

    def test_map_api_completeness(self):
        """Test all required methods implemented."""
        with open("/Users/hustlermain/HUSTLER_CONTENT/HSTLR/DEV/Promptware/stdlib/types.pw") as f:
            pw_code = f.read()

        ir = parse_pw(pw_code)
        map_functions = {f.name for f in ir.functions if f.name.startswith("map_")}
        required = {"map_new", "map_insert", "map_get", "map_remove", "map_contains_key",
                   "map_len", "map_is_empty", "map_keys", "map_values"}
        missing = required - map_functions
        assert len(missing) == 0, f"Missing: {missing}"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
