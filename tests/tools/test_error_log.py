from pathlib import Path

from tools.error_log.adapters import adapter_py


def test_error_log_gathers(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    log_dir = Path('.mcpd/demo')
    log_dir.mkdir(parents=True, exist_ok=True)
    (log_dir / 'run.log').write_text('line1\nline2', encoding='utf-8')

    res = adapter_py.handle({'task_id': 'demo'})
    assert res['ok'] is True
    assert res['data']['logs']
