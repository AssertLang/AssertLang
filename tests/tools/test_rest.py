from types import SimpleNamespace

from tools.rest.adapters import adapter_py


def test_rest_requires_path() -> None:
    res = adapter_py.handle({"base": "https://example.com"})
    assert res["ok"] is False
    assert res["error"]["code"] == "E_PLAN"


def test_rest_success(monkeypatch) -> None:
    dummy = SimpleNamespace(status_code=200, text="ok", json=lambda: None)

    def fake_request(method, url, headers=None, params=None, data=None, timeout=None):
        assert method == "GET"
        assert url == "https://example.com/"
        return dummy

    monkeypatch.setattr(adapter_py.requests, "request", fake_request)

    res = adapter_py.handle({"base": "https://example.com", "path": "/", "method": "GET"})
    assert res["ok"] is True
    assert res["data"]["status"] == 200
    assert res["data"]["json"] is None
