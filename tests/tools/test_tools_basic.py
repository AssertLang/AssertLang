import json
from types import SimpleNamespace

import pytest
from tools.logger.adapters import adapter_py as logger_adapter
from tools.rest.adapters import adapter_py as rest_adapter
from tools.storage.adapters import adapter_py as storage_adapter
from tools.transform.adapters import adapter_py as transform_adapter
from tools.validate_data.adapters import adapter_py as validate_adapter


def test_transform_json_to_yaml():
    res = transform_adapter.handle({"from": "json", "to": "yaml", "content": json.dumps({"a": 1})})
    assert res["ok"] and "a: 1" in res["data"]["content"]


def test_validate_data_jsonschema():
    schema = {"type": "object", "properties": {"a": {"type": "integer"}}, "required": ["a"]}
    content = json.dumps({"a": 1})
    res = validate_adapter.handle({"schema": schema, "content": content, "format": "json"})
    assert res["ok"] and res["data"]["valid"]


def test_storage_fs(tmp_path):
    target = tmp_path / "x.txt"
    put = storage_adapter.handle(
        {"op": "put", "backend": "fs", "params": {"path": str(target), "content": "hi"}}
    )
    assert put["ok"]
    get = storage_adapter.handle({"op": "get", "backend": "fs", "params": {"path": str(target)}})
    assert get["ok"] and get["data"]["content"] == "hi"


def test_logger_tool(capsys):
    res = logger_adapter.handle({"level": "info", "message": "hi", "context": {"user": "a"}})
    assert res["ok"] and res["data"]["logged"] is True
    out = capsys.readouterr().out
    assert "INFO" in out and "hi" in out


@pytest.mark.skip(reason="network-dependent; run manually when network is available")
def test_http_tool_performs_request(monkeypatch):
    dummy = SimpleNamespace(status_code=200, text="ok", json=lambda: None)

    def fake_request(method, url, headers=None, params=None, data=None, timeout=None):
        return dummy

    monkeypatch.setattr(rest_adapter.requests, "request", fake_request)
    res = rest_adapter.handle({"base": "https://example.com", "path": "/", "method": "GET"})
    assert res["ok"]
