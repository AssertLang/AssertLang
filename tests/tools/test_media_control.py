from tools.media_control.adapters import adapter_py


def test_media_control_noop():
    res = adapter_py.handle({'op': 'play'})
    assert res['ok'] is True
