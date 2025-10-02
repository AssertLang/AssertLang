from pathlib import Path

from tools.custom_tool_template.adapters import adapter_py


def test_custom_template_creates_schema(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    (Path("schemas") / "tools").mkdir(parents=True, exist_ok=True)
    res = adapter_py.handle({"name": "sample"})
    assert res["ok"] is True
    created = Path("schemas/tools/sample.v1.json")
    assert created.exists()
