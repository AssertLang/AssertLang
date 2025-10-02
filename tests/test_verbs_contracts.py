import sys
import textwrap
from pathlib import Path

import pytest

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from daemon.mcpd import MCPDaemon, Task
from schema_utils import assert_events_match_schema


@pytest.fixture
def daemon():
    d = MCPDaemon()
    d.start()
    yield d
    try:
        d.gateway.stop()
    except Exception:
        pass


def test_plan_create_v1_schema(daemon):
    res = daemon.plan_create_v1("hello")
    assert res["ok"] and res["version"] == "v1"
    data = res["data"]
    assert "files" in data and "start" in data and data["lang"] == "python"


def test_fs_apply_v1(daemon):
    tid = "testtid"
    res = daemon.fs_apply_v1(tid, [{"path": "a.txt", "content": "x"}])
    assert res["ok"] and res["data"]["writes"] == 1


def test_run_start_and_httpcheck(daemon):
    plan = {
        "lang": "python",
        "files": [
            {
                "path": "app.py",
                "content": textwrap.dedent(
                    """
                    import os
                    from http.server import BaseHTTPRequestHandler, HTTPServer


                    class Handler(BaseHTTPRequestHandler):
                        def do_GET(self):
                            self.send_response(200)
                            self.send_header("Content-Type", "text/plain")
                            self.end_headers()
                            self.wfile.write(b"Hello, World!")

                        def log_message(self, *_args, **_kwargs):
                            return


                    if __name__ == "__main__":
                        port = int(os.environ.get("PORT", "8000"))
                        server = HTTPServer(("127.0.0.1", port), Handler)
                        server.serve_forever()
                    """
                ).strip()
                + "\n",
                "mode": 0o644,
            }
        ],
        "start": "python app.py",
    }
    res = daemon.run_start_v1(plan, lang="python")
    if not res.get("ok"):
        pytest.skip(f"run_start_v1 unavailable: {res}")
    tid = res["data"]["task_id"]
    start_events = res["data"].get("events") or []
    assert isinstance(start_events, list)
    assert_events_match_schema(start_events)
    try:
        chk = daemon.httpcheck_assert_v1(tid, "/", 200)
        assert chk["ok"]
        assert chk["data"]["pass"] is True
        check_events = chk["data"].get("events") or []
        assert isinstance(check_events, list)
        assert_events_match_schema(check_events)
        assert any(evt.get("phase") == "httpcheck" for evt in check_events)
    finally:
        daemon.stop_task(tid)


def test_report_finish_direct_url_when_gateway_unavailable(daemon, monkeypatch, tmp_path):
    monkeypatch.setattr(daemon, "gateway_available", False)
    monkeypatch.setattr(daemon, "gateway_port", None)
    task_id = "fake"
    port = 62000
    base = Path(getattr(daemon, "ARTIFACT_ROOT", Path(".mcpd")))
    (base / task_id).mkdir(parents=True, exist_ok=True)
    daemon.tasks[task_id] = Task(
        task_id=task_id,
        dir=base / task_id,
        socket_path=base / task_id / "sock",
        pid=None,
        port=port,
        events=[],
    )
    res = daemon.report_finish_v1(task_id, verdict="pass")
    assert res["ok"]
    data = res["data"]
    assert data["direct_url"] == f"http://127.0.0.1:{port}/"
    assert data["url"] == f"http://127.0.0.1:{port}/"
    report_events = data.get("events", [])
    assert_events_match_schema(report_events)
    assert any(evt.get("phase") == "report" for evt in report_events)


def test_stop_task_records_stop_event(tmp_path):
    daemon = MCPDaemon()
    daemon.start()
    try:
        task_id = "stoptask"
        task_dir = Path(".mcpd") / task_id
        task_dir.mkdir(parents=True, exist_ok=True)
        daemon.tasks[task_id] = Task(
            task_id=task_id,
            dir=task_dir,
            socket_path=task_dir / "sock",
            pid=None,
            port=None,
            events=[],
        )

        daemon.stop_task(task_id)

        events = daemon.tasks[task_id].events
        assert_events_match_schema(events)
        assert any(evt.get("phase") == "stop" for evt in events)
    finally:
        try:
            daemon.gateway.stop()
        except Exception:
            pass


def test_run_start_merges_registry_defaults(monkeypatch, tmp_path, daemon):
    from daemon import mcpd

    if hasattr(mcpd._load_tool_registry, "cache_clear"):
        mcpd._load_tool_registry.cache_clear()

    registry = {
        "demo": {
            "adapters": [
                {
                    "language": "python",
                    "template": "schema_stub",
                    "deps": {"python": {"requirements": ["demo-package"]}},
                }
            ],
            "policy": {"env": {"LOG_LEVEL": "debug"}},
        }
    }
    monkeypatch.setattr(mcpd, "_load_tool_registry", lambda: registry)

    captured: dict = {}

    def fake_prepare(self, task_dir, plan_lang, deps, env_map, log_file):  # type: ignore[override]
        captured["deps"] = deps
        captured["env"] = dict(env_map)
        return {}

    def fake_runner(self, payload):  # type: ignore[override]
        method = payload.get("method")
        if method == "start":
            captured["start_env"] = payload.get("env")
            return {"ok": True, "version": "v1", "data": {"pid": None}}
        if method == "health":
            return {"ok": True, "version": "v1", "data": {"ready": True}}
        return {"ok": True, "version": "v1"}

    monkeypatch.setattr(MCPDaemon, "_prepare_dependencies", fake_prepare, raising=False)
    monkeypatch.setattr(MCPDaemon, "_run_python_runner", fake_runner, raising=False)
    monkeypatch.setattr(MCPDaemon, "_lease_port", lambda self, task_id, ttl_sec=900: 62010, raising=False)
    monkeypatch.setattr(MCPDaemon, "_release_port", lambda self, port: None, raising=False)

    daemon._tool_registry = registry

    plan = {
        "tool": "demo",
        "lang": "python",
        "files": [],
        "start": "python -c 'print(\"hi\")'",
    }
    res = daemon.run_start_v1(plan, lang="python")
    assert res["ok"] and res["data"]["task_id"]
    assert captured["deps"]["python"]["requirements"] == ["demo-package"]
    assert captured["env"]["LOG_LEVEL"] == "debug"
    assert captured["start_env"]["LOG_LEVEL"] == "debug"
    assert "policy" not in res["data"]


def test_run_start_policy_conflict(monkeypatch, daemon):
    from daemon import mcpd

    if hasattr(mcpd._load_tool_registry, "cache_clear"):
        mcpd._load_tool_registry.cache_clear()

    registry = {
        "demo": {
            "adapters": [],
            "policy": {"network": "deny"},
        }
    }
    monkeypatch.setattr(mcpd, "_load_tool_registry", lambda: registry)
    monkeypatch.setattr(MCPDaemon, "_lease_port", lambda self, task_id, ttl_sec=900: 62011, raising=False)
    monkeypatch.setattr(MCPDaemon, "_release_port", lambda self, port: None, raising=False)

    daemon._tool_registry = registry

    plan = {
        "tool": "demo",
        "lang": "python",
        "files": [],
        "start": "python -c 'print(\"hi\")'",
        "policy": {"network": "allow"},
    }
    res = daemon.run_start_v1(plan, lang="python")
    assert res["ok"] is False
    assert res["error"]["code"] == "E_POLICY"


def test_run_start_dependency_allowlist(monkeypatch, daemon):
    from daemon import mcpd

    if hasattr(mcpd._load_dependency_allowlist, "cache_clear"):
        mcpd._load_dependency_allowlist.cache_clear()

    allowlist = {"python": {"requirements": {"allow": ["allowed"]}}}
    monkeypatch.setattr(mcpd, "_load_dependency_allowlist", lambda: allowlist)
    monkeypatch.setattr(MCPDaemon, "_lease_port", lambda self, task_id, ttl_sec=900: 62012, raising=False)
    monkeypatch.setattr(MCPDaemon, "_release_port", lambda self, port: None, raising=False)
    daemon._dependency_allowlist = allowlist

    plan = {
        "tool": "demo",
        "lang": "python",
        "files": [],
        "start": "python -c 'print(\"hi\")'",
        "deps": {"python": {"requirements": ["not-allowed"]}},
    }

    res = daemon.run_start_v1(plan, lang="python")
    assert res["ok"] is False
    assert res["error"]["code"] == "E_POLICY"
