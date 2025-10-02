import json
import os
import shutil
import subprocess

import pytest


def _run_python_runner(payload: dict) -> str:
    proc = subprocess.run(
        ["python", "runners/python/runner.py"],
        input=json.dumps(payload),
        text=True,
        capture_output=True,
        check=False,
    )
    return proc.stdout.strip()


def _run_node_runner(payload: dict) -> str:
    proc = subprocess.run(
        [
            "node",
            "runners/node/runner.js",
            "--json",
            json.dumps(payload),
        ],
        text=True,
        capture_output=True,
        check=False,
    )
    return proc.stdout.strip()


def _run_go_runner(payload: dict) -> str:
    proc = subprocess.run(
        [
            "go",
            "run",
            "runners/go/runner.go",
            "--json",
            json.dumps(payload),
        ],
        text=True,
        capture_output=True,
        check=False,
    )
    return proc.stdout.strip()


def _run_dotnet_runner(payload: dict) -> str:
    proc = subprocess.run(
        [
            "dotnet",
            "run",
            "--project",
            "runners/dotnet/Runner.csproj",
            "--",
            "--json",
            json.dumps(payload),
        ],
        text=True,
        capture_output=True,
        check=False,
    )
    return proc.stdout.strip()


def _run_go_health(host: str, port: int) -> dict:
    payload = {"method": "health", "host": host, "port": port}
    stdout = _run_go_runner(payload)
    lines = [line for line in stdout.splitlines() if line]
    return json.loads(lines[0])


def _run_dotnet_health(host: str, port: int) -> dict:
    payload = {"method": "health", "host": host, "port": port}
    stdout = _run_dotnet_runner(payload)
    lines = [line for line in stdout.splitlines() if line]
    return json.loads(lines[0])


GO_AVAILABLE = shutil.which("go") is not None
DOTNET_AVAILABLE = shutil.which("dotnet") is not None and bool(os.environ.get("ENABLE_DOTNET_TESTS"))


def test_python_runner_apply_emits_single_json(tmp_path):
    payload = {
        "method": "apply",
        "target_dir": str(tmp_path),
        "files": [{"path": "a.txt", "content": "hello"}],
    }
    stdout = _run_python_runner(payload)
    lines = [line for line in stdout.splitlines() if line]
    assert len(lines) == 1
    data = json.loads(lines[0])
    assert data["ok"] is True
    assert data["data"]["writes"] == 1
    assert (tmp_path / "a.txt").read_text(encoding="utf-8") == "hello"


def test_node_runner_apply_emits_single_json(tmp_path):
    payload = {
        "method": "apply",
        "target_dir": str(tmp_path),
        "files": [{"path": "b.txt", "content": "world"}],
    }
    stdout = _run_node_runner(payload)
    lines = [line for line in stdout.splitlines() if line]
    assert len(lines) == 1
    data = json.loads(lines[0])
    assert data["ok"] is True
    assert data["data"]["writes"] == 1
    assert (tmp_path / "b.txt").read_text(encoding="utf-8") == "world"


def test_python_runner_unknown_method_returns_error():
    stdout = _run_python_runner({"method": "noop"})
    lines = [line for line in stdout.splitlines() if line]
    assert len(lines) == 1
    data = json.loads(lines[0])
    assert data["ok"] is False
    assert data["error"]["code"] == "E_METHOD"


def test_node_runner_unknown_method_returns_error():
    stdout = _run_node_runner({"method": "noop"})
    lines = [line for line in stdout.splitlines() if line]
    assert len(lines) == 1
    data = json.loads(lines[0])
    assert data["ok"] is False
    assert data["error"]["code"] == "E_METHOD"


@pytest.mark.skipif(not GO_AVAILABLE, reason="go command unavailable")
def test_go_runner_apply_emits_single_json(tmp_path):
    payload = {
        "method": "apply",
        "target_dir": str(tmp_path),
        "files": [{"path": "c.txt", "content": "go go"}],
    }
    stdout = _run_go_runner(payload)
    lines = [line for line in stdout.splitlines() if line]
    assert len(lines) == 1
    data = json.loads(lines[0])
    assert data["ok"] is True
    assert data["data"]["writes"] == 1
    assert (tmp_path / "c.txt").read_text(encoding="utf-8") == "go go"


@pytest.mark.skipif(not GO_AVAILABLE, reason="go command unavailable")
def test_go_runner_unknown_method_returns_error():
    stdout = _run_go_runner({"method": "noop"})
    lines = [line for line in stdout.splitlines() if line]
    assert len(lines) == 1
    data = json.loads(lines[0])
    assert data["ok"] is False
    assert data["error"]["code"] == "E_METHOD"


@pytest.mark.skipif(not GO_AVAILABLE, reason="go command unavailable")
def test_go_runner_health_reports_ready_false():
    res = _run_go_health("127.0.0.1", 65535)
    assert res["ok"] is True
    assert res["data"]["ready"] is False


@pytest.mark.skipif(not DOTNET_AVAILABLE, reason="dotnet command unavailable")
def test_dotnet_runner_apply_emits_single_json(tmp_path):
    payload = {
        "method": "apply",
        "task_id": "test",
        "target_dir": str(tmp_path),
        "files": [{"path": "d.txt", "content": "dotnet"}],
    }
    stdout = _run_dotnet_runner(payload)
    lines = [line for line in stdout.splitlines() if line]
    assert len(lines) == 1
    data = json.loads(lines[0])
    assert data["ok"] is True
    assert data["data"]["writes"] == 1
    assert (tmp_path / "d.txt").read_text(encoding="utf-8") == "dotnet"


@pytest.mark.skipif(not DOTNET_AVAILABLE, reason="dotnet command unavailable")
def test_dotnet_runner_unknown_method_returns_error():
    stdout = _run_dotnet_runner({"method": "noop"})
    lines = [line for line in stdout.splitlines() if line]
    assert len(lines) == 1
    data = json.loads(lines[0])
    assert data["ok"] is False
    assert data["error"]["code"] == "E_METHOD"


@pytest.mark.skipif(not DOTNET_AVAILABLE, reason="dotnet command unavailable")
def test_dotnet_runner_health_reports_ready_false():
    res = _run_dotnet_health("127.0.0.1", 65535)
    assert res["ok"] is True
    assert res["data"]["ready"] is False
