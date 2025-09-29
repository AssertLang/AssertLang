from tools.input.adapters import adapter_py as input_adapter
from tools.output.adapters import adapter_py as output_adapter
from tools.encryption.adapters import adapter_py as encryption_adapter


def test_input_output_file(tmp_path):
    p = tmp_path / 'in.txt'
    p.write_text('abc', encoding='utf-8')
    res_in = input_adapter.handle({'source': 'file', 'path': str(p)})
    assert res_in['ok'] and res_in['data']['content'] == 'abc'

    out = tmp_path / 'out.txt'
    res_out = output_adapter.handle({'target': 'file', 'path': str(out), 'content': 'xyz'})
    assert res_out['ok']
    assert out.read_text(encoding='utf-8') == 'xyz'


def test_encryption_hash():
    res = encryption_adapter.handle({'op': 'hash', 'alg': 'sha256', 'data': 'abc'})
    assert res['ok'] and len(res['data']['result']) == 64


