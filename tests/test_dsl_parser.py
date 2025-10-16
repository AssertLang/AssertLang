import json
from pathlib import Path

import pytest
from language.parser import PWParseError, _parse_dsl, parse_pw  # type: ignore[attr-defined]


def test_parse_pw_basic_plan():
    text = """
lang python
start python app.py
file app.py:
    print('hello')

dep python requirements requests
assume responds within 200ms
"""
    prog = parse_pw(text)
    assert prog.plan is not None
    plan = prog.plan
    assert plan["lang"] == "python"
    assert plan["start"] == "python app.py"
    assert plan["files"][0]["path"] == "app.py"
    assert "requests" in plan["deps"]["python"]["requirements"]


def test_parse_dsl_requires_file():
    text = "lang python\nstart python app.py\n"
    try:
        _parse_dsl(text)
    except PWParseError:
        pass
    else:
        assert False, "Expected PWParseError"


def test_parse_pw_fallback_prompt():
    text = "Build hello world"
    prog = parse_pw(text)
    assert prog.plan is None
    assert prog.prompt == "Build hello world"


def test_parse_pw_actions_without_files():
    text = """
tool http as fetch
call fetch method=GET url="https://example.com"
call fetch as fetch_out method=POST url="https://example.com" body="${fetch.data}" expect.data.status=200
"""
    prog = parse_pw(text)
    assert prog.plan is not None
    plan = prog.plan
    assert plan["lang"] == "python"
    assert plan.get("files") in (None, [])
    assert "start" not in plan
    actions = plan["actions"]
    assert len(actions) == 2
    first = actions[0]
    assert first["type"] == "call"
    assert first["alias"] == "fetch"
    second = actions[1]
    assert second["result"] == "fetch_out"
    assert second["expects"]["data.status"] == 200
    assert second["payload"]["body"] == {"__ref__": ["fetch", "data"]}


def test_parse_pw_if_else():
    text = """
tool http as fetch
call fetch method=GET url="https://example.com"
if ${fetch.data.status} == 200:
  call fetch method=POST url="https://example.com" body="${fetch.data}"
else:
  call fetch as fetch_error method=POST url="https://example.com/error"
"""
    prog = parse_pw(text)
    assert prog.plan is not None
    plan = prog.plan
    assert plan.get("files") in (None, [])
    actions = plan["actions"]
    assert actions[1]["type"] == "if"
    node = actions[1]
    assert node["condition"] == "${fetch.data.status} == 200"
    assert node["then"][0]["alias"] == "fetch"
    assert node["else"][0]["result"] == "fetch_error"


def test_parse_pw_retry():
    text = """
tool http as fetch
call fetch method=GET url="https://example.com" retry.max=3 retry.delay=1
"""
    prog = parse_pw(text)
    assert prog.plan is not None
    plan = prog.plan
    action = plan["actions"][0]
    assert action["retry"]["max"] == 3
    assert action["retry"]["delay"] == 1.0


def test_parse_pw_parallel_branches():
    text = """
tool http as fetch
parallel:
  branch primary:
    call fetch method=GET url="https://example.com"
  branch backup:
    call fetch method=GET url="https://backup.example.com"
"""
    prog = parse_pw(text)
    assert prog.plan is not None
    plan = prog.plan
    assert plan["files"] == []
    assert "start" not in plan
    actions = plan["actions"]
    assert actions[0]["type"] == "parallel"
    branches = actions[0]["branches"]
    assert len(branches) == 2
    assert branches[0]["name"] == "primary"
    assert branches[0]["actions"][0]["alias"] == "fetch"


def test_parse_pw_payload_list_index():
    text = """
tool http as fetch
call fetch items[0].name="alpha" items[1].name="beta"
"""
    prog = parse_pw(text)
    assert prog.plan is not None
    payload = prog.plan["actions"][0]["payload"]
    assert payload == {"items": [{"name": "alpha"}, {"name": "beta"}]}


def test_parse_pw_reference_from_syntax():
    text = """
tool http as fetch
call fetch method=GET url="https://example.com"
tool transform as xf
call xf input.from=fetch.data
"""
    prog = parse_pw(text)
    assert prog.plan is not None
    actions = prog.plan["actions"]
    assert actions[1]["payload"]["input"] == {"__ref__": ["fetch", "data"]}


def test_parse_pw_reference_from_requires_alias():
    text = """
tool transform as xf
call xf input.from=123
"""
    try:
        _parse_dsl(text)
    except PWParseError as exc:
        assert exc.code == "E_PLAN_REF"
    else:
        pytest.fail("expected E_PLAN_REF for invalid reference")


def test_parse_pw_let_assignment():
    text = """
tool http as fetch
call fetch method=GET url="https://example.com"
let snapshot = ${fetch.data}
let retries = 5
"""
    prog = parse_pw(text)
    assert prog.plan is not None
    plan = prog.plan
    actions = plan["actions"]
    assert actions[1] == {
        "type": "let",
        "target": "snapshot",
        "value": {"__ref__": ["fetch", "data"]},
    }
    assert actions[2] == {
        "type": "let",
        "target": "retries",
        "value": 5,
    }
    assert plan.get("files") in (None, [])


def test_parse_pw_fanout_case_labels():
    text = """
tool echo as send
call send message="hi"
fanout send:
case ${send.data.ok}:
  let info.status = "ready"
case:
  let info.status = "fallback"
merge into summary send.case_send_data_ok send.case_1
"""
    prog = parse_pw(text)
    assert prog.plan is not None
    plan = prog.plan
    fanout = plan["actions"][1]
    cases = fanout["cases"]
    assert cases[0]["label"] == "case_send_data_ok"
    assert cases[0]["when"] == "${send.data.ok}"
    assert cases[1]["label"] == "case_1"


def test_parse_pw_inline_object_literal():
    text = """
tool logger as log
tool transform as xf
call log message="hi"
call xf config={user: ${log.data.message}, retries: 3, note: "ok"}
"""
    prog = parse_pw(text)
    assert prog.plan is not None
    actions = prog.plan["actions"]
    payload = actions[1]["payload"]["config"]
    assert payload["retries"] == 3
    assert payload["note"] == "ok"
    assert payload["user"] == {"__ref__": ["log", "data", "message"]}


def test_parse_pw_merge_with_custom_aliases():
    text = """
merge into summary send.case_0 as first send.case_1 as second
"""
    prog = parse_pw(text)
    assert prog.plan is not None
    action = prog.plan["actions"][0]
    assert action["type"] == "merge"
    assert action["sources"] == [
        {"path": "send.case_0", "alias": "first"},
        {"path": "send.case_1", "alias": "second"},
    ]


def test_parse_pw_merge_modes():
    plan = parse_pw("merge append into summary send.case").plan
    assert plan is not None
    action = plan["actions"][0]
    assert action["mode"] == "append"
    assert "append_key" not in action

    plan = parse_pw("merge append items into summary send.case").plan
    assert plan is not None
    action = plan["actions"][0]
    assert action["mode"] == "append"
    assert action["append_key"] == "items"

    plan = parse_pw("merge dict into summary send.case").plan
    assert plan is not None
    action = plan["actions"][0]
    assert action["mode"] == "dict"

    plan = parse_pw("merge collect totals into summary send.case").plan
    assert plan is not None
    action = plan["actions"][0]
    assert action["mode"] == "collect"
    assert action["append_key"] == "totals"


def test_parse_pw_state_block():
    text = """
tool logger as log
state shared:
  call log message="hi"
"""
    prog = parse_pw(text)
    assert prog.plan is not None
    action = prog.plan["actions"][0]
    assert action["type"] == "state"
    assert action["name"] == "shared"
    inner = action["actions"][0]
    assert inner["type"] == "call"
    assert inner["alias"] == "log"


@pytest.mark.parametrize(
    "fixture",
    sorted(Path("tests/dsl_fixtures").glob("*.plan.json")),
    ids=lambda p: p.stem.replace(".plan", ""),
)
def test_parse_pw_golden_fixtures(fixture: Path) -> None:
    source = fixture.with_name(fixture.name.replace(".plan.json", ".al"))
    expected = json.loads(fixture.read_text())
    prog = parse_pw(source.read_text())
    assert prog.plan is not None
    assert prog.plan == expected


def test_parse_pw_bad_indentation_sets_error_code():
    text = """
tool http as fetch
 call fetch method=GET
"""
    try:
        _parse_dsl(text)
    except PWParseError as exc:
        assert exc.code == "E_SYNTAX"
    else:
        pytest.fail("expected PWParseError")
