from tools.api_auth.adapters import adapter_py


def test_api_auth_header() -> None:
    res = adapter_py.handle({"type": "apiKey", "token": "abc"})
    assert res["ok"] is True
    assert res["data"]["headers"]["Authorization"] == "Bearer abc"


def test_api_auth_custom_header() -> None:
    res = adapter_py.handle({"type": "jwt", "token": "secret", "header": "X-Key", "prefix": ""})
    assert res["ok"] is True
    assert res["data"]["headers"]["X-Key"] == "secret"


def test_api_auth_unsupported() -> None:
    res = adapter_py.handle({"type": "basic", "token": "xyz"})
    assert res["ok"] is False
    assert res["error"]["code"] == "E_UNSUPPORTED"
