from tools.tracer.adapters import adapter_py


def test_tracer_builds_id():
    res = adapter_py.handle({"op": "start", "kind": "task"})
    assert res["ok"] is True
    assert res["data"]["trace_id"] == "task-start"
