from tools.conditional.adapters import adapter_py


def test_conditional_eq():
    res = adapter_py.handle({"left": "a", "op": "==", "right": "a"})
    assert res["ok"] is True
    assert res["data"]["pass"] is True


def test_conditional_regex_false():
    res = adapter_py.handle({"left": "abc", "op": "regex", "right": "^z"})
    assert res["ok"] is True
    assert res["data"]["pass"] is False
