"""
Test Bug #10: Reserved keywords as class property names.

Tests that common words like 'method', 'body', 'name', 'type' can be used
as class property names without causing parser errors.
"""

import pytest
from dsl.al_parser import parse_al, ALParseError


def test_method_as_property():
    """Test 'method' can be used as property name."""
    pw_code = """
class Request {
    method: string;
    path: string;

    constructor(method: string, path: string) {
        self.method = method;
        self.path = path;
    }
}
"""
    # Should compile without errors
    ir = parse_al(pw_code)
    assert ir is not None
    assert len(ir.classes) == 1
    assert ir.classes[0].name == "Request"
    assert len(ir.classes[0].properties) == 2
    assert ir.classes[0].properties[0].name == "method"
    assert ir.classes[0].properties[1].name == "path"


def test_body_as_property():
    """Test 'body' can be used as property name."""
    pw_code = """
class HttpRequest {
    body: map;
    headers: map;

    constructor(body: map, headers: map) {
        self.body = body;
        self.headers = headers;
    }
}
"""
    ir = parse_al(pw_code)
    assert ir is not None
    assert len(ir.classes) == 1
    assert ir.classes[0].name == "HttpRequest"
    assert len(ir.classes[0].properties) == 2
    assert ir.classes[0].properties[0].name == "body"
    assert ir.classes[0].properties[1].name == "headers"


def test_name_as_property():
    """Test 'name' can be used as property name."""
    pw_code = """
class User {
    name: string;
    email: string;
}
"""
    ir = parse_al(pw_code)
    assert ir is not None
    assert len(ir.classes) == 1
    assert ir.classes[0].name == "User"
    assert len(ir.classes[0].properties) == 2
    assert ir.classes[0].properties[0].name == "name"
    assert ir.classes[0].properties[1].name == "email"


def test_type_as_property():
    """Test 'type' can be used as property name."""
    pw_code = """
class Message {
    type: string;
    payload: string;
}
"""
    ir = parse_al(pw_code)
    assert ir is not None
    assert len(ir.classes) == 1
    assert ir.classes[0].name == "Message"
    assert len(ir.classes[0].properties) == 2
    assert ir.classes[0].properties[0].name == "type"
    assert ir.classes[0].properties[1].name == "payload"


def test_all_keywords_as_properties():
    """Test class with many keyword-named properties."""
    pw_code = """
class ComplexObject {
    method: string;
    body: map;
    name: string;
    type: string;
    params: array;
    returns: string;
    throws: array;
}
"""
    ir = parse_al(pw_code)
    assert ir is not None
    assert len(ir.classes) == 1
    assert ir.classes[0].name == "ComplexObject"
    assert len(ir.classes[0].properties) == 7

    # Verify all property names
    prop_names = [prop.name for prop in ir.classes[0].properties]
    assert "method" in prop_names
    assert "body" in prop_names
    assert "name" in prop_names
    assert "type" in prop_names
    assert "params" in prop_names
    assert "returns" in prop_names
    assert "throws" in prop_names


def test_keywords_still_work_as_keywords():
    """Ensure 'function', 'class', 'if' etc still work as keywords."""
    pw_code = """
class TestClass {
    data: string;

    function process() -> bool {
        if (self.data == "test") {
            return true;
        }
        return false;
    }
}
"""
    ir = parse_al(pw_code)
    assert ir is not None
    assert len(ir.classes) == 1
    assert len(ir.classes[0].methods) == 1
    assert ir.classes[0].methods[0].name == "process"


def test_generated_python_uses_property_names():
    """Test that generated Python code uses reserved keyword property names correctly."""
    from language.python_generator_v2 import PythonGeneratorV2

    pw_code = """
class Request {
    method: string;
    path: string;
    body: map;

    constructor(method: string, path: string, body: map) {
        self.method = method;
        self.path = path;
        self.body = body;
    }

    function get_method() -> string {
        return self.method;
    }
}
"""
    ir = parse_al(pw_code)
    generator = PythonGeneratorV2()
    python_code = generator.generate(ir)

    # Verify property names are in generated code
    assert "method: str" in python_code or "self.method" in python_code
    assert "path: str" in python_code or "self.path" in python_code
    assert "body: Dict" in python_code or "self.body" in python_code
