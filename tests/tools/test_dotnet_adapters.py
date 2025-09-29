"""Smoke tests for generated .NET adapters.

Creates a temporary SDK-style project, compiles the adapter, and executes `Handle`.
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
FIXTURE_DIR = REPO_ROOT / "tests" / "fixtures" / "dotnet_adapters"
DOTNET_BIN = os.environ.get("DOTNET_BIN", "dotnet")
DOTNET_AVAILABLE = shutil.which(DOTNET_BIN) is not None


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
        adapter_path = REPO_ROOT / "tools" / package / "adapters" / "Adapter.cs"
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


def test_dotnet_adapters_smoke() -> None:
    if not DOTNET_AVAILABLE:
        pytest.skip(f"{DOTNET_BIN!r} not available in PATH")
    if not CASES:
        pytest.skip("No .NET adapter fixtures available")
    for case in CASES:
        result = _run_adapter(case.adapter_path, case.payload)
        try:
            _assert_subset(result, case.expected)
        except AssertionError as exc:
            raise AssertionError(f"{case.id}: {exc}") from exc


def _run_adapter(adapter_path: Path, payload: dict) -> dict:
    csproj = """
<Project Sdk=\"Microsoft.NET.Sdk\">
  <PropertyGroup>
    <OutputType>Exe</OutputType>
    <TargetFramework>net8.0</TargetFramework>
    <ImplicitUsings>enable</ImplicitUsings>
    <Nullable>enable</Nullable>
  </PropertyGroup>
</Project>
"""

    program_cs = """
using System;
using System.Collections;
using System.Collections.Generic;
using System.Text.Json;
using System.IO;

static object? ConvertElement(JsonElement element)
{
    return element.ValueKind switch
    {
        JsonValueKind.Object => ConvertObject(element),
        JsonValueKind.Array => ConvertArray(element),
        JsonValueKind.String => element.GetString(),
        JsonValueKind.Number => element.TryGetInt64(out var l) ? l : element.GetDouble(),
        JsonValueKind.True => true,
        JsonValueKind.False => false,
        JsonValueKind.Null => null,
        _ => null,
    };
}

static Dictionary<string, object?> ConvertObject(JsonElement element)
{
    var dict = new Dictionary<string, object?>();
    foreach (var property in element.EnumerateObject())
    {
        dict[property.Name] = ConvertElement(property.Value);
    }
    return dict;
}

static List<object?> ConvertArray(JsonElement element)
{
    var list = new List<object?>();
    foreach (var item in element.EnumerateArray())
    {
        list.Add(ConvertElement(item));
    }
    return list;
}

static Dictionary<string, object> ToRequest(JsonElement element)
{
    var converted = ConvertElement(element) as Dictionary<string, object?> ?? new Dictionary<string, object?>();
    var result = new Dictionary<string, object>(converted.Count);
    foreach (var pair in converted)
    {
        result[pair.Key] = pair.Value!;
    }
    return result;
}

string? payloadPath = null;
foreach (var arg in args)
{
    if (arg == "--")
    {
        continue;
    }
    payloadPath = arg;
    break;
}

if (payloadPath is null)
{
    Console.Error.WriteLine("missing payload");
    Environment.Exit(1);
}
string payloadJson;
try
{
    payloadJson = File.ReadAllText(payloadPath);
}
catch (Exception ex)
{
    Console.Error.WriteLine($"failed to read payload: {ex.Message}");
    Environment.Exit(1);
    throw;
}

JsonDocument document;
try
{
    document = JsonDocument.Parse(payloadJson);
}
catch (JsonException ex)
{
    Console.Error.WriteLine($"failed to parse payload: {ex.Message}");
    Environment.Exit(1);
    throw;
}
var request = ToRequest(document.RootElement);
var response = Adapter.Handle(request);
var output = JsonSerializer.Serialize(response);
Console.Write(output);
"""

    payload_json = json.dumps(payload)
    with tempfile.TemporaryDirectory(prefix="dotnet_adapter_") as tmpdir:
        tmp_path = Path(tmpdir)
        (tmp_path / "AdapterHarness.csproj").write_text(csproj, encoding="utf-8")
        shutil.copy(adapter_path, tmp_path / "Adapter.cs")
        (tmp_path / "Program.cs").write_text(program_cs, encoding="utf-8")
        payload_path = tmp_path / "payload.json"
        payload_path.write_text(payload_json, encoding="utf-8")
        completed = subprocess.run(
            [
                DOTNET_BIN,
                "run",
                "--configuration",
                "Release",
                "--",
                str(payload_path),
            ],
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
