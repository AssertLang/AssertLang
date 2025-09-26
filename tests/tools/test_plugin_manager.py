from tools.plugin_manager.adapters import adapter_py


def test_plugin_manager_echo():
    res = adapter_py.handle({'op': 'list'})
    assert res['ok'] is True
    assert res['data']['result'] == 'list'
