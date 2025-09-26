from pathlib import Path

from tools.marketplace_uploader.adapters import adapter_py


def test_marketplace_upload(tmp_path):
    artifact = tmp_path / 'artifact.zip'
    artifact.write_text('data', encoding='utf-8')
    res = adapter_py.handle({'artifact': str(artifact), 'tool': 'demo', 'version': '1.0.0'})
    assert res['ok'] is True
    assert res['data']['url'] == 'https://market.local/demo:1.0.0'
