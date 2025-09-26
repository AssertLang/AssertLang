from tools.input.adapters import adapter_py


def test_input_file(tmp_path):
    path = tmp_path / 'in.txt'
    path.write_text('hello', encoding='utf-8')
    res = adapter_py.handle({'source': 'file', 'path': str(path)})
    assert res['ok'] is True
    assert res['data']['content'] == 'hello'
