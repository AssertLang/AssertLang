from types import SimpleNamespace

import pytest

from tools.http.adapters import adapter_py


def test_http_adapter_requires_url():
    res = adapter_py.handle({})
    assert res["ok"] is False
    assert res["error"]["code"] == "E_ARGS"


def test_http_adapter_success(monkeypatch):
    dummy_response = SimpleNamespace(
        status_code=200,
        headers={"Content-Type": "text/plain"},
        text="hello",
    )

    def fake_request(method, url, headers=None, data=None, timeout=None):  # noqa: D401
        assert method == "GET"
        assert url == "https://example.com"
        return dummy_response

    monkeypatch.setattr(adapter_py.requests, "request", fake_request)

    res = adapter_py.handle({"url": "https://example.com"})
    assert res["ok"] is True
    assert res["data"]["status"] == 200
    assert res["data"]["body"] == "hello"
    assert res["data"]["headers"]["Content-Type"] == "text/plain"


def test_http_adapter_propagates_errors(monkeypatch):
    class Boom(Exception):
        pass

    def fake_request(*_args, **_kwargs):
        raise Boom("boom")

    monkeypatch.setattr(adapter_py.requests, "request", fake_request)

    res = adapter_py.handle({"url": "https://example.com", "method": "GET"})
    assert res["ok"] is False
    assert res["error"]["code"] == "E_NETWORK"
