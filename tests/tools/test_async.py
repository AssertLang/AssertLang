from tools.async_tool.adapters import adapter_py


def test_async_results():
    res = adapter_py.handle({"tasks": [1, 2]})
    assert res["ok"] is True
    results = res["data"]["results"]
    assert isinstance(results, list)
    assert results[0]["index"] == 0 and results[0]["status"] == "done" and results[0]["result"] == 1
    assert results[1]["index"] == 1 and results[1]["status"] == "done" and results[1]["result"] == 2
