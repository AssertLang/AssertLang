import os
import shutil
import subprocess

import pytest
from cli import toolgen


def test_auth_header_node_template_has_helpers():
    code = toolgen._adapter_content("api-auth", "node", "auth_header")
    assert "function ok" in code
    assert "module.exports" in code
    assert "unsupported auth type" in code


def test_auth_header_go_template_returns_helpers():
    code = toolgen._adapter_content("api-auth", "go", "auth_header")
    assert "func Handle" in code
    assert "errResp" in code
    assert "Authorization" in code


def test_auth_header_rust_template_uses_serde_json():
    code = toolgen._adapter_content("api-auth", "rust", "auth_header")
    assert "serde_json" in code
    assert "unsupported auth type" in code


def test_auth_header_dotnet_template_wraps_responses():
    code = toolgen._adapter_content("api-auth", "dotnet", "auth_header")
    assert "public static class Adapter" in code
    assert 'Error("E_UNSUPPORTED"' in code
    assert "headers" in code


def test_rest_node_template_uses_fetch_and_timeout():
    code = toolgen._adapter_content("rest", "node", "rest_client")
    assert "async function handle" in code
    assert "AbortController" in code
    assert "url.searchParams" in code


def test_rest_go_template_imports_net_url():
    code = toolgen._adapter_content("rest", "go", "rest_client")
    assert "net/url" in code
    assert "resolved := baseURL.ResolveReference" in code


def test_rest_rust_template_uses_reqwest():
    code = toolgen._adapter_content("rest", "rust", "rest_client")
    assert "reqwest::blocking::Client" in code
    assert "value_to_string" in code


def test_rest_dotnet_template_sends_requests():
    code = toolgen._adapter_content("rest", "dotnet", "rest_client")
    assert "HttpClient" in code
    assert "UriBuilder" in code


def test_json_validator_node_template_uses_ajv():
    code = toolgen._adapter_content("validate-data", "node", "json_validator")
    assert "require('ajv')" in code
    assert "module.exports" in code
    assert "valid: true" in code


def test_http_rust_template_uses_reqwest():
    code = toolgen._adapter_content("http", "rust", "http_client")
    assert "reqwest::blocking::Client" in code
    assert "value_to_string" in code


def test_http_dotnet_template_handles_headers():
    code = toolgen._adapter_content("http", "dotnet", "http_client")
    assert "HttpRequestMessage" in code
    assert "HttpClient" in code


def test_storage_rust_template_handles_put():
    code = toolgen._adapter_content("storage", "rust", "storage_fs")
    assert "fs::write" in code
    assert "unsupported backend" in code


def test_storage_dotnet_template_handles_directory():
    code = toolgen._adapter_content("storage", "dotnet", "storage_fs")
    assert "Directory.CreateDirectory" in code
    assert "File.WriteAllText" in code


def test_conditional_node_template_handles_regex():
    code = toolgen._adapter_content("conditional", "node", "conditional_eval")
    assert "new RegExp" in code
    assert "unsupported operator" in code


def test_conditional_rust_template_uses_regex_crate():
    code = toolgen._adapter_content("conditional", "rust", "conditional_eval")
    assert "use regex::Regex" in code
    assert "E_RUNTIME" in code


def test_branch_node_template_checks_cases():
    code = toolgen._adapter_content("branch", "node", "branch_select")
    assert "Object.prototype.hasOwnProperty" in code
    assert "selected" in code


def test_branch_rust_template_returns_default():
    code = toolgen._adapter_content("branch", "rust", "branch_select")
    assert "contains_key" in code
    assert "default" in code


def test_async_node_template_builds_results():
    code = toolgen._adapter_content("async", "node", "async_simulator")
    assert "tasks.map" in code
    assert "status: 'done'" in code


def test_async_rust_template_collects_results():
    code = toolgen._adapter_content("async", "rust", "async_simulator")
    assert "collect" in code
    assert "results" in code


def test_loop_node_template_counts_items():
    code = toolgen._adapter_content("loop", "node", "loop_counter")
    assert "items.length" in code
    assert "E_ARGS" in code


def test_loop_rust_template_counts_len():
    code = toolgen._adapter_content("loop", "rust", "loop_counter")
    assert "items.len()" in code
    assert "E_ARGS" in code


def test_output_node_template_handles_stdout_and_file():
    code = toolgen._adapter_content("output", "node", "output_writer")
    assert "console.log" in code
    assert "fs.writeFileSync" in code


def test_output_rust_template_handles_file_path():
    code = toolgen._adapter_content("output", "rust", "output_writer")
    assert "fs::write" in code
    assert "path.parent" in code


def test_transform_node_template_uses_js_yaml():
    code = toolgen._adapter_content("transform", "node", "transform_convert")
    assert "js-yaml" in code
    assert "JSON.parse" in code


def test_transform_rust_template_uses_serde_yaml():
    code = toolgen._adapter_content("transform", "rust", "transform_convert")
    assert "serde_yaml" in code
    assert "E_RUNTIME" in code


def test_transform_dotnet_template_handles_json_and_yaml():
    code = toolgen._adapter_content("transform", "dotnet", "transform_convert")
    assert "JsonSerializer" in code
    assert "SerializerBuilder" in code
    assert "YamlException" in code


def test_error_log_dotnet_template_reads_run_log():
    code = toolgen._adapter_content("log", "dotnet", "error_log_collector")
    assert "Path.Combine" in code
    assert "File.ReadAllLines" in code
    assert "errors.Count" in code


def test_conditional_dotnet_template_uses_regex_switch():
    code = toolgen._adapter_content("conditional", "dotnet", "conditional_eval")
    assert "Regex" in code
    assert "switch" in code
    assert "E_ARGS" in code


def test_branch_dotnet_template_defaults_to_fallback():
    code = toolgen._adapter_content("branch", "dotnet", "branch_select")
    assert "cases" in code
    assert "selected" in code
    assert "default" in code


def test_async_dotnet_template_collects_results():
    code = toolgen._adapter_content("async", "dotnet", "async_simulator")
    assert "results" in code
    assert "tasks" in code
    assert "status" in code


def test_loop_dotnet_template_counts_items():
    code = toolgen._adapter_content("loop", "dotnet", "loop_counter")
    assert "foreach" in code
    assert "count" in code
    assert "E_ARGS" in code


def test_output_dotnet_template_handles_file_target():
    code = toolgen._adapter_content("output", "dotnet", "output_writer")
    assert "Directory.CreateDirectory" in code
    assert "File.WriteAllText" in code
    assert "target" in code


def test_error_toggle_dotnet_template_returns_bool():
    code = toolgen._adapter_content("error", "dotnet", "error_toggle")
    assert "thrown" in code
    assert 'Error("E_SCHEMA"' in code
    assert 'Error("E_ARGS"' not in code  # only schema guard


@pytest.mark.skipif(shutil.which("dotnet") is None, reason="dotnet CLI not available")
@pytest.mark.skipif(
    os.environ.get("ASSERTLANG_RUN_DOTNET_SMOKE") != "1", reason="dotnet smoke test disabled"
)
def test_error_toggle_dotnet_template_compiles(tmp_path):
    project_dir = tmp_path / "dotnet_adapter"
    project_dir.mkdir()

    env = {
        **os.environ,
        "DOTNET_SKIP_FIRST_TIME_EXPERIENCE": "1",
        "DOTNET_CLI_TELEMETRY_OPTOUT": "1",
        "DOTNET_NOLOGO": "1",
    }

    # bootstrap a class library project
    subprocess.run(
        ["dotnet", "new", "classlib", "--force"],
        cwd=project_dir,
        env=env,
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )

    code = toolgen._adapter_content("error", "dotnet", "error_toggle")
    adapter_path = project_dir / "Adapter.cs"
    adapter_path.write_text(code, encoding="utf-8")

    class1 = project_dir / "Class1.cs"
    if class1.exists():
        class1.unlink()

    build = subprocess.run(
        ["dotnet", "build", "-c", "Release"],
        cwd=project_dir,
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )
    assert build.returncode == 0, build.stdout
