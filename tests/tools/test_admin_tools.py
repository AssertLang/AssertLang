from pathlib import Path

from tools.marketplace_uploader.adapters import adapter_py as uploader
from tools.plugin_manager.adapters import adapter_py as plugin
from tools.custom_tool_template.adapters import adapter_py as template


def test_marketplace_uploader(tmp_path):
    art = tmp_path / "tool.tgz"
    art.write_text("data", encoding='utf-8')
    res = uploader.handle({'tool': 'demo', 'version': 'v1.0.0', 'artifact': str(art)})
    assert res['ok'] is True
    assert res['data']['url'] == 'https://market.local/demo:v1.0.0'


def test_plugin_manager_list():
    res = plugin.handle({'op': 'list'})
    assert res['ok'] is True
    assert res['data']['result'] == 'list'


def test_custom_tool_template(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    (Path('schemas') / 'tools').mkdir(parents=True, exist_ok=True)
    res = template.handle({'name': 'mytool'})
    assert res['ok'] is True
    assert Path('schemas/tools/mytool.v1.json').exists()


