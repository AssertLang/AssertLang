from tools.timing.adapters import adapter_py


def test_timing_sleep(monkeypatch):
    calls = {"t": 0.0}

    def fake_time():
        return calls["t"]

    def fake_sleep(seconds):
        calls["t"] += seconds

    monkeypatch.setattr(adapter_py.time, "time", fake_time)
    monkeypatch.setattr(adapter_py.time, "sleep", fake_sleep)

    res = adapter_py.handle({"op": "sleep", "ms": 10})
    assert res["ok"] is True
    assert res["data"]["elapsed_ms"] == 10
