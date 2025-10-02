from __future__ import annotations

import pytest
from language.interpreter import ActionExecutor, PWExecutionError
from language.parser import parse_pw


def fake_runner(tool_id: str, payload: dict) -> dict:
    message = payload.get("message", "")
    return {
        "ok": True,
        "data": {
            "message": message,
            "count": len(message),
            "payload": payload,
        },
    }


def fake_identity_runner(tool_id: str, payload: dict) -> dict:
    return {"ok": True, "data": payload}


def test_executor_handles_call_let_and_expectations():
    text = """
lang python

tool echo as send
call send message="hello" expect.data.message="hello"
let echoed = ${send.data.message}
"""
    plan = parse_pw(text).plan
    assert plan is not None
    executor = ActionExecutor(plan["tools"], runner=fake_runner)
    responses = executor.execute(plan["actions"])
    assert responses["send"]["data"]["message"] == "hello"
    assert responses["echoed"] == "hello"


def test_executor_conditional_branching():
    text = """
tool echo as send
call send message="hey"
if ${send.data.count} > 2:
  let verdict = "long"
else:
  let verdict = "short"
"""
    plan = parse_pw(text).plan
    assert plan is not None
    executor = ActionExecutor(plan["tools"], runner=fake_runner)
    responses = executor.execute(plan["actions"])
    assert responses["verdict"] == "long"


def test_executor_parallel_branches_share_parent_state():
    text = """
tool echo as send
let greeting = "hi"
parallel:
  branch first:
    call send message=${greeting}
  branch second:
    call send message="bye"
"""
    plan = parse_pw(text).plan
    assert plan is not None
    executor = ActionExecutor(plan["tools"], runner=fake_runner)
    responses = executor.execute(plan["actions"])
    assert responses["first"]["send"]["data"]["message"] == "hi"
    assert responses["second"]["send"]["data"]["message"] == "bye"
    # ensure top-level let remains accessible
    assert responses["greeting"] == "hi"


def test_executor_resolves_list_indices():
    text = """
tool echo as send
call send message="hello" expect.data.payload.message="hello"
let first_char = ${send.data.message[0]}
"""
    plan = parse_pw(text).plan
    assert plan is not None
    executor = ActionExecutor(plan["tools"], runner=fake_runner)
    responses = executor.execute(plan["actions"])
    assert responses["first_char"] == "h"
    events = executor.events
    assert any(evt.get("action") == "call" for evt in events)
    assert any(evt.get("action") == "let" and evt.get("target") == "first_char" for evt in events)


def test_executor_records_parallel_event():
    text = """
tool echo as send
parallel:
  branch one:
    call send message="a"
"""
    plan = parse_pw(text).plan
    assert plan is not None
    executor = ActionExecutor(plan["tools"], runner=fake_runner)
    executor.execute(plan["actions"])
    parallel_events = [evt for evt in executor.events if evt.get("action") == "parallel"]
    assert parallel_events and parallel_events[0]["branches"] == ["one"]


def test_executor_resolves_payload_from_references():
    text = """
tool logger as log
tool transform as xf
call log message="hi"
call xf config={user: ${log.data.message}, retries: 3, note: "ok"}
"""
    prog = parse_pw(text).plan
    assert prog is not None
    # provide per-tool behaviour
    def runner(tool_id: str, payload: dict) -> dict:
        if tool_id == "logger":
            return fake_runner(tool_id, payload)
        return fake_identity_runner(tool_id, payload)

    executor = ActionExecutor(prog["tools"], runner=runner)
    responses = executor.execute(prog["actions"])
    assert responses["log"]["data"]["message"] == "hi"
    config = responses["xf"]["data"]["config"]
    assert config["user"] == "hi"
    assert config["retries"] == 3
    assert config["note"] == "ok"


def test_executor_handles_state_scope():
    text = """
tool logger as log
state shared:
  call log message="hi"
let summary = ${shared.log.data.message}
"""
    plan = parse_pw(text).plan
    assert plan is not None
    executor = ActionExecutor(plan["tools"], runner=fake_runner)
    responses = executor.execute(plan["actions"])
    assert responses["shared"]["log"]["data"]["message"] == "hi"
    assert responses["summary"] == "hi"
    events = [evt for evt in executor.events if evt.get("action") == "state"]
    assert events and events[0]["name"] == "shared"


def test_executor_merge_with_state_scope():
    text = """
tool logger as log
state shared:
  call log message="hi"
merge into snapshot shared
"""
    plan = parse_pw(text).plan
    assert plan is not None
    executor = ActionExecutor(plan["tools"], runner=fake_runner)
    responses = executor.execute(plan["actions"])
    assert responses["snapshot"]["shared"]["log"]["data"]["message"] == "hi"
    responses["snapshot"]["shared"]["log"]["data"]["message"] = "modified"
    assert responses["shared"]["log"]["data"]["message"] == "hi"


def test_executor_merge_with_aliases():
    text = """
tool logger as log
tool rest.get as fetch
call log message="hi"
call fetch method=GET url="https://example.com"
merge into summary log as logger fetch as http
"""
    plan = parse_pw(text).plan
    assert plan is not None

    def runner(tool_id: str, payload: dict) -> dict:
        if tool_id == "logger":
            return fake_runner(tool_id, payload)
        return {"ok": True, "data": {"payload": payload}}

    executor = ActionExecutor(plan["tools"], runner=runner)
    responses = executor.execute(plan["actions"])
    merged = responses["summary"]
    assert merged["logger"]["data"]["message"] == "hi"
    assert merged["http"]["data"]["payload"]["url"] == "https://example.com"

def test_executor_fanout_runs_matching_cases_only():
    text = """
tool echo as send
call send message="abc"
fanout send:
case ${send.data.count}==3:
  let info.hit = ${send.data.message}
case ${send.data.count}==5:
  let info.miss = "unused"
"""
    plan = parse_pw(text).plan
    assert plan is not None
    executor = ActionExecutor(plan["tools"], runner=fake_runner)
    responses = executor.execute(plan["actions"])
    send_responses = responses["send"]
    label = "case_send_data_count_3"
    assert label in send_responses
    assert send_responses[label]["info"]["hit"] == "abc"
    assert "case_send_data_count_5" not in send_responses
    fanout_events = [evt for evt in executor.events if evt.get("action") == "fanout"]
    assert fanout_events and fanout_events[0]["branches"] == [label]
    cases_meta = fanout_events[0].get("cases") or []
    assert cases_meta and cases_meta[0]["label"] == label
    assert cases_meta[0]["condition"] == "${send.data.count}==3"


def test_executor_merge_combines_fanout_results():
    text = """
tool echo as send
call send message="team"
fanout send:
case:
  let info.value = "first"
case:
  let info.value = "second"
merge into summary send.case_0 send.case_1
"""
    plan = parse_pw(text).plan
    assert plan is not None
    executor = ActionExecutor(plan["tools"], runner=fake_runner)
    responses = executor.execute(plan["actions"])
    summary = responses["summary"]
    assert summary["case_0"]["info"]["value"] == "first"
    assert summary["case_1"]["info"]["value"] == "second"
    merge_events = [evt for evt in executor.events if evt.get("action") == "merge"]
    assert merge_events and merge_events[0]["target"] == "summary"

def test_executor_merge_list_items():
    text = """
tool logger as primary
tool logger as secondary
call primary data={items: [1, 2, 3]}
call secondary data={items: [4]}
merge append totals into combined primary.data.items secondary.data.items
"""
    plan = parse_pw(text).plan
    assert plan is not None

    def runner(tool_id: str, payload: dict) -> dict:
        items = payload.get("data", {}).get("items", [])
        return {"ok": True, "data": {"items": items}}

    executor = ActionExecutor(plan["tools"], runner=runner)
    responses = executor.execute(plan["actions"])
    combined = responses["combined"]
    assert combined["totals"] == [1, 2, 3, 4]
    merge_event = [evt for evt in executor.events if evt.get("phase") == "merge"][0]
    assert merge_event.get("mode") == "append"
    assert merge_event.get("append_key") == "totals"




def test_executor_merge_list_items_alias():
    text = """
tool logger as primary
tool logger as secondary
call primary data={items: [1, 2]}
call secondary data={items: [3, 4]}
merge append into combined primary.data.items as all secondary.data.items as all
"""
    plan = parse_pw(text).plan
    assert plan is not None

    def runner(tool_id: str, payload: dict) -> dict:
        items = payload.get("data", {}).get("items", [])
        return {"ok": True, "data": {"items": items}}

    executor = ActionExecutor(plan["tools"], runner=runner)
    responses = executor.execute(plan["actions"])
    assert responses["combined"]["all"] == [1, 2, 3, 4]



def test_executor_merge_dict_mode():
    text = """
tool logger as primary
tool logger as secondary
call primary value={a: 1}
call secondary value={b: 2}
merge dict into combined primary.data secondary.data
"""
    plan = parse_pw(text).plan
    assert plan is not None

    def runner(tool_id: str, payload: dict) -> dict:
        return {"ok": True, "data": payload.get("value", payload)}

    executor = ActionExecutor(plan["tools"], runner=runner)
    responses = executor.execute(plan["actions"])
    combined = responses["combined"]
    assert combined["a"] == 1
    assert combined["b"] == 2
    merge_event = [evt for evt in executor.events if evt.get("phase") == "merge"][0]
    assert merge_event.get("mode") == "dict"



def test_executor_merge_dict_mode_with_alias():
    text = """
tool logger as primary
tool logger as secondary
call primary value={a: 1}
call secondary value={b: 2}
merge dict into combined primary.data as first secondary.data as second
"""
    plan = parse_pw(text).plan
    assert plan is not None

    def runner(tool_id: str, payload: dict) -> dict:
        return {"ok": True, "data": payload.get("value", payload)}

    executor = ActionExecutor(plan["tools"], runner=runner)
    responses = executor.execute(plan["actions"])
    combined = responses["combined"]
    assert combined["first"]["a"] == 1
    assert combined["second"]["b"] == 2
    merge_event = [evt for evt in executor.events if evt.get("phase") == "merge"][0]
    assert merge_event.get("mode") == "dict"
    assert merge_event["sources"][0]["alias"] == "first"
    assert merge_event["sources"][1]["alias"] == "second"



def test_executor_retry_events():
    text = """
tool logger as log
call log message="hi" retry.max=2
"""
    plan = parse_pw(text).plan
    assert plan is not None
    attempts = []

    def runner(tool_id: str, payload: dict) -> dict:
        attempts.append(1)
        return {"ok": False}

    executor = ActionExecutor(plan["tools"], runner=runner)
    try:
        executor.execute(plan["actions"])
    except PWExecutionError as exc:
        assert exc.code == "E_RUNTIME"
    else:
        pytest.fail("expected PWExecutionError")
    events = [evt for evt in executor.events if evt.get("phase") == "call"]
    assert events
    assert events[-1]["attempt"] == 2
    assert events[-1]["code"] == "E_RUNTIME"


def test_executor_merge_collect_scalars():
    text = """
tool logger as primary
tool logger as secondary
call primary score=1
call secondary score=2
merge collect totals into combined primary.data.score secondary.data.score
"""
    plan = parse_pw(text).plan
    assert plan is not None

    def runner(tool_id: str, payload: dict) -> dict:
        return {"ok": True, "data": payload}

    executor = ActionExecutor(plan["tools"], runner=runner)
    responses = executor.execute(plan["actions"])
    combined = responses["combined"]
    assert combined["totals"] == [1, 2]
    merge_event = [evt for evt in executor.events if evt.get("phase") == "merge"][0]
    assert merge_event.get("mode") == "collect"
    assert merge_event.get("append_key") == "totals"



def test_executor_unknown_reference_raises_plan_ref():
    text = """
let missing = ${unknown.value}
"""
    plan = parse_pw(text).plan
    assert plan is not None
    executor = ActionExecutor(plan["tools"], runner=fake_runner)
    try:
        executor.execute(plan["actions"])
    except PWExecutionError as exc:
        assert exc.code == "E_PLAN_REF"
    else:
        pytest.fail("expected PWExecutionError")



def test_executor_missing_tool_binding_raises_plan_ref():
    text = """
tool echo as send
call send message="hi"
"""
    plan = parse_pw(text).plan
    assert plan is not None
    tools = dict(plan["tools"])
    tools.pop('send', None)
    executor = ActionExecutor(tools, runner=fake_runner)
    try:
        executor.execute(plan["actions"])
    except PWExecutionError as exc:
        assert exc.code == "E_PLAN_REF"
    else:
        pytest.fail("expected PWExecutionError")
