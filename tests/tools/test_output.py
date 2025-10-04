from pathlib import Path

from tools.output.adapters import adapter_py


def test_output_stdout(capsys):
    res = adapter_py.handle({"target": "stdout", "content": "hello"})
    assert res["ok"] is True
    assert res["data"]["written"] is True
    assert "hello" in capsys.readouterr().out


def test_output_file(tmp_path: Path):
    target = tmp_path / "out.txt"
    res = adapter_py.handle({"target": "file", "path": str(target), "content": "hi"})
    assert res["ok"] is True
    assert target.read_text(encoding="utf-8") == "hi"


def test_output_requires_path():
    res = adapter_py.handle({"target": "file", "content": "oops"})
    assert res["ok"] is False
    assert res["error"]["code"] == "E_ARGS"


def test_output_requires_valid_target():
    res = adapter_py.handle({"target": "unknown"})
    assert res["ok"] is False
    assert res["error"]["code"] == "E_ARGS"
