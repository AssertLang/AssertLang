import json

from tools.validate_data.adapters import adapter_py


def test_validate_data_jsonschema():
    schema = {"type": "object", "properties": {"a": {"type": "integer"}}, "required": ["a"]}
    content = json.dumps({"a": 1})
    res = adapter_py.handle({"schema": schema, "content": content, "format": "json"})
    assert res["ok"] is True
    assert res["data"]["valid"] is True


def test_validate_data_invalid():
    schema = {"type": "object", "properties": {"a": {"type": "integer"}}, "required": ["a"]}
    content = json.dumps({"b": 2})
    res = adapter_py.handle({"schema": schema, "content": content, "format": "json"})
    assert res["ok"] is True
    assert res["data"]["valid"] is False
