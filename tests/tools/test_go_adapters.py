"""Smoke tests for generated Go adapters.

Builds a temporary Go workspace per adapter and executes `Handle` using fixture payloads.
"""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
FIXTURE_DIR = REPO_ROOT / "tests" / "fixtures" / "go_adapters"
GO_BIN = os.environ.get("GO_BIN", "go")
GO_AVAILABLE = shutil.which(GO_BIN) is not None


@dataclass
class AdapterCase:
    id: str
    adapter_path: Path
    payload: dict
    expected: dict


def _load_cases() -> List[AdapterCase]:
    cases: List[AdapterCase] = []
    if not FIXTURE_DIR.exists():
        return cases

    for fixture_path in sorted(FIXTURE_DIR.glob("*.json")):
        data = json.loads(fixture_path.read_text())
        package = data.get("adapter") or fixture_path.stem
        adapter_path = REPO_ROOT / "tools" / package / "adapters" / "adapter_go.go"
        if not adapter_path.exists():
            continue
        for idx, case in enumerate(data.get("cases", [])):
            payload = case.get("payload")
            expected = case.get("expected")
            if payload is None or expected is None:
                continue
            name = case.get("name") or f"case_{idx}"
            cases.append(
                AdapterCase(
                    id=f"{package}:{name}",
                    adapter_path=adapter_path,
                    payload=payload,
                    expected=expected,
                )
            )
    return cases


CASES = _load_cases()


def test_go_adapters_smoke() -> None:
    if not GO_AVAILABLE:
        pytest.skip(f"{GO_BIN!r} not available in PATH")
    if not CASES:
        pytest.skip("No Go adapter fixtures available")
    for case in CASES:
        result = _run_adapter(case.adapter_path, case.payload)
        try:
            _assert_subset(result, case.expected)
        except AssertionError as exc:
            raise AssertionError(f"{case.id}: {exc}") from exc


def _run_adapter(adapter_path: Path, payload: dict) -> dict:
    runner_template = """
package main

import (
    "encoding/json"
    "fmt"
    "os"
)

func main() {
    if len(os.Args) < 2 {
        fmt.Fprint(os.Stderr, "missing payload")
        os.Exit(1)
    }
    var payload map[string]interface{}
    if err := json.Unmarshal([]byte(os.Args[1]), &payload); err != nil {
        fmt.Fprintf(os.Stderr, "unmarshal payload: %v", err)
        os.Exit(1)
    }
    result := Handle(payload)
    out, err := json.Marshal(result)
    if err != nil {
        fmt.Fprintf(os.Stderr, "marshal result: %v", err)
        os.Exit(1)
    }
    fmt.Print(string(out))
}
"""
    payload_json = json.dumps(payload)
    with tempfile.TemporaryDirectory(prefix="go_adapter_") as tmpdir:
        tmp_path = Path(tmpdir)
        shutil.copy(adapter_path, tmp_path / "adapter_go.go")
        runner_path = tmp_path / "runner_main.go"
        runner_path.write_text(runner_template, encoding="utf-8")
        completed = subprocess.run(
            [GO_BIN, "run", "adapter_go.go", runner_path.name, payload_json],
            cwd=tmp_path,
            capture_output=True,
            text=True,
            check=False,
        )
    if completed.returncode != 0:
        raise AssertionError(
            "Adapter execution failed",
            {
                "adapter": str(adapter_path),
                "stdout": completed.stdout,
                "stderr": completed.stderr,
                "returncode": completed.returncode,
            },
        )
    stdout_lines = [line for line in completed.stdout.splitlines() if line.strip()]
    if not stdout_lines:
        raise AssertionError("Adapter produced no output", completed.stdout)
    tail = stdout_lines[-1]
    try:
        return json.loads(tail)
    except json.JSONDecodeError as exc:
        raise AssertionError("Adapter output was not valid JSON", tail) from exc


def _assert_subset(actual: dict, expected: dict) -> None:
    if not isinstance(actual, dict):
        raise AssertionError(f"Expected dict response, got {type(actual)}: {actual}")
    _assert_mapping_subset(actual, expected)


def _assert_mapping_subset(actual: dict, expected: dict, path: Iterable[str] | None = None) -> None:
    for key, value in expected.items():
        current_path = list(path or []) + [str(key)]
        if key not in actual:
            raise AssertionError(f"Missing key {'/'.join(current_path)} in {actual}")
        actual_value = actual[key]
        if isinstance(value, dict):
            if not isinstance(actual_value, dict):
                raise AssertionError(
                    f"Expected mapping at {'/'.join(current_path)}, got {type(actual_value)}"
                )
            _assert_mapping_subset(actual_value, value, current_path)
        else:
            if actual_value != value:
                raise AssertionError(
                    f"Value mismatch at {'/'.join(current_path)}: expected {value!r}, got {actual_value!r}"
                )
