from tools.branch.adapters import adapter_py


def test_branch_match():
    res = adapter_py.handle({"key": "k", "value": "A", "cases": {"A": [], "B": []}})
    assert res["ok"] is True
    assert res["data"]["selected"] == "A"


def test_branch_default():
    res = adapter_py.handle({"key": "k", "value": "Z", "cases": {"A": [], "B": []}})
    assert res["ok"] is True
    assert res["data"]["selected"] == "default"
