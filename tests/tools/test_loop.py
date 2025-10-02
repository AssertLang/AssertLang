from tools.loop.adapters import adapter_py


def test_loop_iterations():
    res = adapter_py.handle({"items": [1, 2, 3]})
    assert res["ok"] is True
    assert res["data"]["iterations"] == 3


def test_loop_requires_list():
    res = adapter_py.handle({"items": "oops"})
    assert res["ok"] is False
    assert res["error"]["code"] == "E_ARGS"
