from pathlib import Path

from daemon import mcpd
from daemon.mcpd import MCPDaemon


def _capture_run(calls):
    import subprocess as _subprocess

    def _runner(cmd, **kwargs):
        calls.append((cmd, kwargs))
        return _subprocess.CompletedProcess(cmd, 0)

    return _runner


def _is_relative_to(path: Path, parent: Path) -> bool:
    try:
        path.relative_to(parent)
        return True
    except ValueError:
        return False


def test_prepare_dependencies_go(tmp_path, monkeypatch):
    daemon = MCPDaemon()
    daemon._dependency_allowlist = {
        "go": {"modules": {"allow": ["github.com/prompthub/example@v1"]}}
    }

    calls = []
    monkeypatch.setattr(mcpd.shutil, "which", lambda cmd: f"/usr/bin/{cmd}")
    monkeypatch.setattr(mcpd.subprocess, "run", _capture_run(calls))

    with (tmp_path / "log.txt").open("wb") as log_file:
        updates = daemon._prepare_dependencies(
            tmp_path,
            "go",
            {
                "go": {
                    "modules": ["github.com/prompthub/example@v1"],
                    "module_name": "example.com/app",
                }
            },
            {},
            log_file,
        )

    go_cache_root = (Path(".mcpd") / "cache" / "go").resolve()
    assert "GOMODCACHE" in updates and Path(updates["GOMODCACHE"]).is_absolute()
    assert "GOCACHE" in updates and Path(updates["GOCACHE"]).is_absolute()
    assert "GOPATH" in updates and Path(updates["GOPATH"]).is_absolute()
    assert _is_relative_to(Path(updates["GOMODCACHE"]), go_cache_root)
    assert _is_relative_to(Path(updates["GOCACHE"]), go_cache_root)
    assert _is_relative_to(Path(updates["GOPATH"]), go_cache_root)

    assert any("go get github.com/prompthub/example@v1" in " ".join(cmd) for cmd, _ in calls)
    assert any("go mod tidy" in " ".join(cmd) for cmd, _ in calls)

    for _cmd, kwargs in calls:
        env = kwargs["env"]
        assert env["GOMODCACHE"] == updates["GOMODCACHE"]
        assert env["GOCACHE"] == updates["GOCACHE"]
        assert env["GOPATH"] == updates["GOPATH"]


def test_prepare_dependencies_node(tmp_path, monkeypatch):
    daemon = MCPDaemon()
    daemon._dependency_allowlist = {
        "node": {
            "packages": {"allow": ["left-pad"]},
            "registry": {
                "url": "https://registry.example.com",
                "always_auth": True,
                "token_env": "NPM_TOKEN",
                "cache_ttl_days": 5,
            },
            "env": {"NPM_CONFIG_STRICT_SSL": "false"},
        }
    }

    calls = []
    monkeypatch.setattr(mcpd.shutil, "which", lambda cmd: f"/usr/bin/{cmd}")
    monkeypatch.setattr(mcpd.subprocess, "run", _capture_run(calls))
    monkeypatch.setenv("NPM_TOKEN", "secret")

    deps = {"node": {"packages": ["left-pad"]}}
    with (tmp_path / "log.txt").open("wb") as log_file:
        updates = daemon._prepare_dependencies(tmp_path, "node", deps, {}, log_file)

    cache_root = (Path(".mcpd") / "cache" / "node").resolve()
    assert any("npm install" in " ".join(cmd) for cmd, _ in calls)
    for _cmd, kwargs in calls:
        env = kwargs.get("env", {})
        if env:
            assert env["NPM_CONFIG_REGISTRY"] == "https://registry.example.com"
            assert env["NPM_CONFIG_ALWAYS_AUTH"] == "true"
            assert env["NPM_TOKEN"] == "secret"
            assert env["npm_config_cache"].startswith(str(cache_root))
            assert env["PROMPTWARE_NODE_CACHE_TTL_DAYS"] == "5"
    assert "PATH" in updates
    assert updates["PROMPTWARE_NODE_CACHE_TTL_DAYS"] == "5"


def test_prepare_dependencies_dotnet(tmp_path, monkeypatch):
    daemon = MCPDaemon()
    daemon._dependency_allowlist = {
        "dotnet": {
            "packages": {"allow": ["Newtonsoft.Json"]},
            "feeds": [
                {"name": "nuget.org", "url": "https://api.nuget.org/v3/index.json"},
                {
                    "name": "internal",
                    "url": "https://nuget.example.com/v3/index.json",
                    "token_env": "NUGET_INTERNAL_TOKEN",
                    "username": "svc-account",
                },
            ],
            "cache_ttl_days": 14,
        }
    }

    calls = []
    monkeypatch.setattr(mcpd.shutil, "which", lambda cmd: f"/usr/bin/{cmd}")
    monkeypatch.setattr(mcpd.subprocess, "run", _capture_run(calls))
    monkeypatch.setenv("NUGET_INTERNAL_TOKEN", "supersecret")

    deps = {"dotnet": {"packages": ["Newtonsoft.Json@13.0.3"]}}
    with (tmp_path / "log.txt").open("wb") as log_file:
        updates = daemon._prepare_dependencies(tmp_path, ".net", deps, {}, log_file)

    assert "NUGET_PACKAGES" in updates
    assert Path(updates["NUGET_PACKAGES"]).is_absolute()
    assert "DOTNET_ROOT" in updates

    restore_calls = [cmd for cmd, _ in calls if cmd[:2] == ["dotnet", "restore"]]
    assert restore_calls, "dotnet restore should be invoked when packages are declared"

    cache_root = (Path(".mcpd") / "cache" / "dotnet").resolve()
    assert _is_relative_to(Path(updates["NUGET_PACKAGES"]), cache_root)

    env_dir = tmp_path / "env" / "dotnet"
    proj_path = env_dir / "deps" / "PromptwareDeps.csproj"
    assert proj_path.exists()
    contents = proj_path.read_text(encoding="utf-8")
    assert "Newtonsoft.Json" in contents
    nuget_config = env_dir / "deps" / "NuGet.Config"
    assert nuget_config.exists()
    config_text = nuget_config.read_text(encoding="utf-8")
    assert "nuget.org" in config_text and "nuget.example.com" in config_text
    assert "packageSourceCredentials" in config_text and "svc-account" in config_text
    assert "supersecret" in config_text
    assert updates["PROMPTWARE_DOTNET_CACHE_TTL_DAYS"] == "14"

    restore_env = next(kwargs["env"] for cmd, kwargs in calls if cmd[:2] == ["dotnet", "restore"])
    assert restore_env["PROMPTWARE_DOTNET_CACHE_TTL_DAYS"] == "14"


def test_prepare_dependencies_rust(tmp_path, monkeypatch):
    daemon = MCPDaemon()
    daemon._dependency_allowlist = {
        "rust": {
            "crates": {"allow": ["serde"]},
            "registries": [
                {"name": "crates-io", "index": "https://github.com/rust-lang/crates.io-index"},
                {
                    "name": "internal",
                    "index": "https://git.example.com/rust/index",
                    "token_env": "CARGO_INTERNAL_TOKEN",
                },
            ],
        }
    }

    calls = []
    monkeypatch.setattr(mcpd.shutil, "which", lambda cmd: f"/usr/bin/{cmd}")
    monkeypatch.setattr(mcpd.subprocess, "run", _capture_run(calls))
    monkeypatch.setenv("CARGO_INTERNAL_TOKEN", "tok123")

    deps = {"rust": {"crates": ["serde@1.0"]}}
    with (tmp_path / "log.txt").open("wb") as log_file:
        updates = daemon._prepare_dependencies(tmp_path, "rust", deps, {}, log_file)

    assert updates["CARGO_HOME"].endswith("cargo")
    assert updates["RUSTUP_HOME"].endswith("rustup")

    fetch_calls = [cmd for cmd, _ in calls if "cargo fetch" in " ".join(cmd)]
    assert fetch_calls, "cargo fetch should be executed for declared crates"

    cache_root = (Path(".mcpd") / "cache" / "rust").resolve()
    assert _is_relative_to(Path(updates["CARGO_HOME"]), cache_root)
    assert _is_relative_to(Path(updates["RUSTUP_HOME"]), cache_root)

    bootstrap_dir = tmp_path / "env" / "rust" / "bootstrap"
    cargo_toml = bootstrap_dir / "Cargo.toml"
    assert cargo_toml.exists()
    assert "serde" in cargo_toml.read_text(encoding="utf-8")
    cargo_config = bootstrap_dir / ".cargo" / "config.toml"
    assert cargo_config.exists()
    cfg = cargo_config.read_text(encoding="utf-8")
    assert "crates-io" in cfg and "internal" in cfg

    fetch_env = next(kwargs["env"] for cmd, kwargs in calls if "cargo fetch" in " ".join(cmd))
    assert fetch_env["CARGO_REGISTRIES_INTERNAL_TOKEN"] == "tok123"
