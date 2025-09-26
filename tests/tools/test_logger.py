from tools.logger.adapters import adapter_py


def test_logger_stdout(capsys):
    res = adapter_py.handle({'level': 'info', 'message': 'hello', 'context': {'user': 'a'}})
    assert res['ok'] is True
    assert res['data']['logged'] is True
    out = capsys.readouterr().out
    assert 'INFO' in out and 'hello' in out
