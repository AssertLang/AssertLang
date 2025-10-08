#!/usr/bin/env python3
"""
Test: Constructor Property Extraction

This test verifies that the Python parser correctly extracts properties
from constructor (self.property = value) assignments.

Issue: Previously, class properties were only detected from class-level
annotations, not from constructor assignments.

Fix: Added logic in _convert_class() to scan constructor body for
self.property assignments and add them to the properties list.
"""

from language.python_parser_v2 import parse_python_source


def test_basic_constructor_properties():
    """Test that basic constructor property assignments are detected."""
    code = """
class UserService:
    def __init__(self, database):
        self.db = database
        self.cache = {}
"""
    module = parse_python_source(code, "test")
    cls = module.classes[0]

    assert len(cls.properties) == 2
    prop_names = {p.name for p in cls.properties}
    assert 'db' in prop_names
    assert 'cache' in prop_names


def test_constructor_properties_with_types():
    """Test that constructor properties have correct inferred types."""
    code = """
class UserService:
    def __init__(self, db, cache=None):
        self.database = db
        self.cache = cache or {}
        self.count = 0
        self.active = True
        self.name = "service"
"""
    module = parse_python_source(code, "test")
    cls = module.classes[0]

    assert len(cls.properties) == 5

    props = {p.name: p.prop_type.name for p in cls.properties}
    assert props['count'] == 'int'
    assert props['active'] == 'bool'
    assert props['name'] == 'string'
    # cache is bool because of 'or' operator (BoolOp in AST)
    assert props['cache'] == 'bool'


def test_mixed_annotated_and_constructor_properties():
    """Test that both annotated and constructor properties are detected."""
    code = """
class UserService:
    name: str = "default"
    version: int = 1

    def __init__(self, database):
        self.db = database
        self.cache = {}
"""
    module = parse_python_source(code, "test")
    cls = module.classes[0]

    # Should have: name, version (annotated) + db, cache (constructor)
    assert len(cls.properties) == 4
    prop_names = {p.name for p in cls.properties}
    assert 'name' in prop_names
    assert 'version' in prop_names
    assert 'db' in prop_names
    assert 'cache' in prop_names


def test_no_duplicate_properties():
    """Test that properties are not duplicated if defined in both places."""
    code = """
class UserService:
    db: str

    def __init__(self, database):
        self.db = database
        self.cache = {}
"""
    module = parse_python_source(code, "test")
    cls = module.classes[0]

    # Should have: db (annotated, NOT duplicated) + cache (constructor)
    assert len(cls.properties) == 2
    prop_names = [p.name for p in cls.properties]

    # Check no duplicates
    assert len(prop_names) == len(set(prop_names))
    assert 'db' in prop_names
    assert 'cache' in prop_names


def test_class_without_constructor():
    """Test that classes without constructors still work."""
    code = """
class UserService:
    name: str = "default"

    def get_name(self):
        return self.name
"""
    module = parse_python_source(code, "test")
    cls = module.classes[0]

    # Should have only the annotated property
    assert len(cls.properties) == 1
    assert cls.properties[0].name == 'name'


def test_constructor_with_complex_assignments():
    """Test constructor with various assignment patterns."""
    code = """
class Service:
    def __init__(self, config):
        self.config = config
        self.data = []
        self.mapping = {}
        self.enabled = True
        self.timeout = 30
        self.factor = 1.5
"""
    module = parse_python_source(code, "test")
    cls = module.classes[0]

    assert len(cls.properties) == 6

    props = {p.name: p.prop_type.name for p in cls.properties}
    assert props['data'] == 'array'
    assert props['mapping'] == 'map'
    assert props['enabled'] == 'bool'
    assert props['timeout'] == 'int'
    assert props['factor'] == 'float'


def test_constructor_properties_in_generated_code():
    """Test that extracted properties appear in generated code."""
    from language.python_generator_v2 import PythonGeneratorV2

    code = """
class UserService:
    def __init__(self, database):
        self.db = database
        self.cache = {}
        self.count = 0
"""
    module = parse_python_source(code, "test")
    generator = PythonGeneratorV2()
    generated = generator.generate(module)

    # All properties should be in generated code
    assert 'self.db' in generated
    assert 'self.cache' in generated
    assert 'self.count' in generated


if __name__ == '__main__':
    # Run tests directly
    test_basic_constructor_properties()
    print("✅ test_basic_constructor_properties")

    test_constructor_properties_with_types()
    print("✅ test_constructor_properties_with_types")

    test_mixed_annotated_and_constructor_properties()
    print("✅ test_mixed_annotated_and_constructor_properties")

    test_no_duplicate_properties()
    print("✅ test_no_duplicate_properties")

    test_class_without_constructor()
    print("✅ test_class_without_constructor")

    test_constructor_with_complex_assignments()
    print("✅ test_constructor_with_complex_assignments")

    test_constructor_properties_in_generated_code()
    print("✅ test_constructor_properties_in_generated_code")

    print("\n🎉 All tests passed!")
