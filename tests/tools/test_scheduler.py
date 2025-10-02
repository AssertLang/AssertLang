from tools.scheduler.adapters import adapter_py


def test_scheduler_sim():
    res = adapter_py.handle({"job": "deploy"})
    assert res["ok"] is True
    assert res["data"]["scheduled"] is True
    assert res["data"]["id"] == "sch-deploy"
