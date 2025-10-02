from __future__ import annotations

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from language.executor import execute_pw_file
from schema_utils import assert_events_match_schema


def test_interpreter_events_via_executor(tmp_path):
    pw_path = Path(tmp_path) / "logger.pw"
    pw_path.write_text(
        "tool logger as log\n"
        "parallel:\n"
        "  branch one:\n"
        "    call log message=\"hi\"\n",
        encoding="utf-8",
    )

    payload = execute_pw_file(str(pw_path))

    assert payload.get("mode") == "interpreter"
    assert isinstance(payload.get("responses"), dict)
    events = payload.get("events")
    assert isinstance(events, list) and events
    assert any(evt.get("action") == "parallel" for evt in events)


def test_interpreter_fanout_events_include_cases(tmp_path):
    pw_path = Path(tmp_path) / "fanout.pw"
    pw_path.write_text(
        "tool logger as log\n"
        "call log message=\"hi\"\n"
        "fanout log:\n"
        "case ${log.data.logged}:\n"
        "  let info.hit = true\n",
        encoding="utf-8",
    )

    payload = execute_pw_file(str(pw_path))

    assert payload.get("mode") == "interpreter"
    events = payload.get("events") or []
    fanout = [evt for evt in events if evt.get("action") == "fanout"]
    assert fanout, "expected fanout event"
    event = fanout[0]
    assert event.get("branches") == ["case_log_data_logged"]
    cases = event.get("cases")
    assert cases and cases[0]["label"] == "case_log_data_logged"
    assert cases[0]["condition"] == "${log.data.logged}"


def test_interpreter_events_match_schema(tmp_path):
    pw_path = Path(tmp_path) / "schema_check.pw"
    pw_path.write_text(
        "tool logger as log\n"
        "call log message=\"hi\"\n"
        "fanout log:\n"
        "case ${log.data.logged}:\n"
        "  let info.hit = true\n",
        encoding="utf-8",
    )

    payload = execute_pw_file(str(pw_path))
    events = payload.get("events") or []
    assert_events_match_schema(events)