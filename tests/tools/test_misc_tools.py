from tools.logger.adapters import adapter_py as logger_adapter
from tools.timing.adapters import adapter_py as timing_adapter


def test_timing_sleep(monkeypatch):
    calls = {'t': 0.0}

    def fake_time():
        return calls['t']

    def fake_sleep(seconds):
        calls['t'] += seconds

    monkeypatch.setattr(timing_adapter.time, 'time', fake_time)
    monkeypatch.setattr(timing_adapter.time, 'sleep', fake_sleep)

    res = timing_adapter.handle({'op': 'sleep', 'ms': 5})
    assert res['ok'] is True
    assert res['data']['elapsed_ms'] == 5


def test_logger():
    res = logger_adapter.handle({'level': 'info', 'message': 'hi', 'context': {'k': 1}})
    assert res['ok'] is True
    assert res['data']['logged']


