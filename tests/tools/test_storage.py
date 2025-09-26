import os
from pathlib import Path

import pytest

from tools.storage.adapters import adapter_py


def test_storage_requires_path(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    res = adapter_py.handle({'backend': 'fs', 'op': 'put', 'params': {}})
    assert res['ok'] is False
    assert res['error']['code'] == 'E_ARGS'


def test_storage_put_get_delete(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    path = tmp_path / 'data.txt'

    res_put = adapter_py.handle({'backend': 'fs', 'op': 'put', 'params': {'path': str(path), 'content': 'hello'}})
    assert res_put['ok'] is True
    assert res_put['data']['written'] is True

    res_get = adapter_py.handle({'backend': 'fs', 'op': 'get', 'params': {'path': str(path)}})
    assert res_get['ok'] is True
    assert res_get['data']['content'] == 'hello'

    res_del = adapter_py.handle({'backend': 'fs', 'op': 'delete', 'params': {'path': str(path)}})
    assert res_del['ok'] is True
    assert res_del['data']['deleted'] is True
    assert not path.exists()


@pytest.mark.parametrize('glob', ['*', '*.txt'])
def test_storage_list(tmp_path, monkeypatch, glob):
    monkeypatch.chdir(tmp_path)
    (tmp_path / 'a.txt').write_text('hi', encoding='utf-8')
    (tmp_path / 'b.log').write_text('log', encoding='utf-8')
    res = adapter_py.handle({'backend': 'fs', 'op': 'list', 'params': {'path': str(tmp_path), 'glob': glob}})
    assert res['ok'] is True
    items = res['data']['items']
    assert all(Path(item).exists() for item in items)
