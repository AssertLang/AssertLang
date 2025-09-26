import json

from tools.transform.adapters import adapter_py


def test_transform_json_to_yaml():
    res = adapter_py.handle({'from': 'json', 'to': 'yaml', 'content': json.dumps({'a': 1})})
    assert res['ok'] is True
    assert 'a: 1' in res['data']['content']


def test_transform_yaml_to_json():
    res = adapter_py.handle({'from': 'yaml', 'to': 'json', 'content': 'a: 1'})
    assert res['ok'] is True
    assert res['data']['content'].strip().startswith('{')
