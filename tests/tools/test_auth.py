from tools.auth.adapters import adapter_py


def test_auth_header():
    res = adapter_py.handle({'type': 'apiKey', 'token': 'abc'})
    assert res['ok'] is True
    assert res['data']['headers']['Authorization'] == 'Bearer abc'


def test_auth_custom_header():
    res = adapter_py.handle({'type': 'jwt', 'token': 'secret', 'header': 'X-Key', 'prefix': ''})
    assert res['ok'] is True
    assert res['data']['headers']['X-Key'] == 'secret'
