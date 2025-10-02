from pathlib import Path

from language.dsl_utils import format_text, lint_text


def test_format_text_roundtrip(tmp_path):
    source = """
lang python
start python app.py
file app.py:
    print('hi')

tool http as fetch
call fetch method=GET url="https://example.com" retry.max=2 retry.delay=1 expect.status=200
"""
    formatted = format_text(source)
    assert "tool http as fetch" in formatted
    assert "retry.max=2" in formatted
    assert "retry.delay=" in formatted
    assert formatted.endswith("\n")


def test_lint_text_prompt_only(tmp_path):
    warnings = lint_text(Path("sample.pw"), "Just a prompt")
    assert any("prompt only" in msg for msg in warnings)


def test_format_text_with_let(tmp_path):
    source = """
tool http as fetch
let result = ${fetch.data}
"""
    formatted = format_text(source)
    assert "let result = ${fetch.data}" in formatted


def test_format_text_with_parallel(tmp_path):
    source = """
tool http as fetch
parallel:
  branch primary:
    call fetch method=GET url="https://example.com"
"""
    formatted = format_text(source)
    assert "parallel:" in formatted
    assert "branch primary:" in formatted


def test_format_text_with_fanout_and_merge():
    source = """
tool echo as send
call send message="hi"
fanout send:
case:
  let info.hit = ${send.data.message}
case:
  let info.miss = "noop"
merge into summary send.case_0 send.case_1
"""
    formatted = format_text(source)
    assert "fanout send:" in formatted
    assert formatted.count("case:") == 2
    assert "merge into summary send.case_0 send.case_1" in formatted


def test_lint_warns_on_empty_fanout_case():
    source = """
tool echo as send
fanout send:
case:
merge into summary send.case_0
"""
    warnings = lint_text(Path("fanout.pw"), source)
    assert any("fanout case has no actions" in msg for msg in warnings)


def test_format_text_with_case_condition():
    source = """
tool echo as send
call send message="hi"
fanout send:
case ${send.data.ok}:
  let info.hit = true
"""
    formatted = format_text(source)
    assert "case ${send.data.ok}:" in formatted


def test_format_text_preserves_from_reference():
    source = """
tool rest.get as fetch
tool transform as xf
call fetch method=GET url="https://example.com"
call xf input.from=fetch.data
"""
    formatted = format_text(source)
    assert "call xf input.from=fetch.data" in formatted


def test_format_text_with_state_block():
    source = """
tool logger as log
state shared:
  call log message="hi"
"""
    formatted = format_text(source)
    assert "state shared:" in formatted
    assert 'call log message="hi"' in formatted


def test_format_text_with_merge_aliases():
    source = """
merge into summary send.case_0 as first send.case_1 as second
"""
    formatted = format_text(source)
    assert "merge into summary send.case_0 as first send.case_1 as second" in formatted


def test_format_text_with_merge_aliases():
    source = """
merge into summary send.case_0 as first send.case_1 as second
"""
    formatted = format_text(source)
    assert "merge into summary send.case_0 as first send.case_1 as second" in formatted


def test_format_text_with_merge_mode():
    source = """
merge append into summary send.case_0 as first send.case_1 as second
"""
    formatted = format_text(source)
    assert "merge append into summary send.case_0 as first send.case_1 as second" in formatted
