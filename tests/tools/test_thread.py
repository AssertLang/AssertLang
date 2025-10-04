from tools.thread.adapters import adapter_py


def test_thread_results():
    res = adapter_py.handle({"tasks": [1, 2, 3]})
    assert res["ok"] is True
    assert res["data"]["results"] == [True, True, True]
    assert res["data"]["duration_ms"] == 0
