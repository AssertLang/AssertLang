from tools.error.adapters import adapter_py


def test_error_status():
    res = adapter_py.handle({"thrown": True})
    assert res["ok"] is True
    assert res["data"]["thrown"] is True
