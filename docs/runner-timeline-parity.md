# Runner Timeline & Envelope Parity Analysis

Wave 2 task: Compare timeline payloads for Python vs Node runners and log deltas.

---

## Executive Summary

**Runner envelope parity**: ✅ **COMPLETE**
Python and Node runners implement identical response envelope schemas across all four methods (`apply`, `start`, `stop`, `health`).

**Timeline event parity**: ⚠️ **GAP IDENTIFIED**
Timeline events are emitted by the Python interpreter (`language/interpreter.py`), not by runners. No Node interpreter exists yet, so timeline event parity cannot be evaluated until Wave 4.

---

## Runner Envelope Comparison

### Envelope Schema

Both runners return responses in the MCP v1 envelope format:

**Success**:
```json
{
  "ok": true,
  "version": "v1",
  "data": { ... }
}
```

**Error**:
```json
{
  "ok": false,
  "version": "v1",
  "error": {
    "code": "E_*",
    "message": "..."
  }
}
```

**Differences**: None. Python uses `True`/`False` (serialized to JSON `true`/`false`), Node uses `true`/`false` natively.

---

## Method-by-Method Comparison

### 1. `apply`

**Purpose**: Write files to the target directory.

**Request Schema** (both):
```json
{
  "method": "apply",
  "target_dir": "path",
  "files": [
    {
      "path": "relative/path",
      "content": "...",
      "mode": 493  // optional: octal file mode
    }
  ]
}
```

**Success Response** (both):
```json
{
  "ok": true,
  "version": "v1",
  "data": {
    "writes": 3,
    "target": "/abs/path"
  }
}
```

**Error Codes** (both):
- `E_JSON` — Invalid JSON request
- `E_FS` — File system operation failed

**Parity**: ✅ Identical

---

### 2. `start`

**Purpose**: Spawn a background process.

**Request Schema** (both):
```json
{
  "method": "start",
  "cmd": "command to execute",
  "cwd": "working/directory",
  "port": 8080,
  "env": {
    "KEY": "value"
  },
  "log_path": "logs/run.log"
}
```

**Success Response** (both):
```json
{
  "ok": true,
  "version": "v1",
  "data": {
    "pid": 12345
  }
}
```

**Error Codes** (both):
- `E_RUNTIME` — Process spawn failed

**Parity**: ✅ Identical

**Implementation Differences**:

| Aspect | Python | Node |
| --- | --- | --- |
| Shell | `bash -lc` | `bash -lc` |
| Process group | `start_new_session=True` | `detached: true` |
| Stdout/stderr capture | Background threads via `pump()` | Stream event handlers |
| Log header | None | Prepends `[runner] starting cmd: ...` to log |
| PATH augmentation | None | Adds `/opt/homebrew/bin:/usr/local/bin` to `PATH` |

**Notes**:
- Node runner adds Homebrew paths to `PATH` for macOS compatibility.
- Node runner logs start/exit events; Python runner doesn't.
- Both unref/detach child processes so runner can exit.

---

### 3. `stop`

**Purpose**: Terminate a process by PID.

**Request Schema** (both):
```json
{
  "method": "stop",
  "pid": 12345
}
```

**Success Response** (both):
```json
{
  "ok": true,
  "version": "v1",
  "data": {
    "stopped": true
  }
}
```

**Error Codes** (both):
- `E_RUNTIME` — Kill signal failed

**Parity**: ✅ Identical

**Implementation Differences**:

| Aspect | Python | Node |
| --- | --- | --- |
| Signal | `os.kill(pid, 15)` (SIGTERM) | `process.kill(pid, 'SIGTERM')` |

---

### 4. `health`

**Purpose**: Check if a port is accepting connections.

**Request Schema** (both):
```json
{
  "method": "health",
  "host": "127.0.0.1",
  "port": 8080
}
```

**Success Response** (both):
```json
{
  "ok": true,
  "version": "v1",
  "data": {
    "ready": true  // or false
  }
}
```

**Error Codes** (both):
- None — Health checks always return `ok: true` with `ready: true/false`

**Parity**: ✅ Identical

**Implementation Differences**:

| Aspect | Python | Node |
| --- | --- | --- |
| TCP connection | `socket.create_connection(..., timeout=1.0)` | `net.createConnection(...)` with `setTimeout(1000)` |
| Timeout behavior | Exception caught, returns `ready: false` | Timeout event handler, returns `ready: false` |

---

## Error Code Coverage

| Code | Python | Node | Meaning |
| --- | --- | --- | --- |
| `E_JSON` | ✅ | ✅ | Request parsing failed |
| `E_FS` | ✅ | ✅ | File system operation failed |
| `E_RUNTIME` | ✅ | ✅ | Process spawn/kill failed |
| `E_METHOD` | ✅ | ✅ | Unknown method |

**Parity**: ✅ Identical

---

## Timeline Events

Timeline events are emitted by **interpreters**, not runners. Runners are stateless protocol adapters that execute methods and return envelopes.

### Python Interpreter Timeline Events

Location: `language/interpreter.py` → `ActionExecutor.events`

Event structure:
```python
{
  "phase": "call" | "let" | "if" | "parallel" | "fanout" | "merge" | "state",
  "action": "...",  # same as phase
  "status": "ok" | "error",
  "duration_ms": 123.45,
  ...  # phase-specific fields
}
```

#### Event Types

**1. `call` (tool invocation)**:
```python
{
  "phase": "call",
  "action": "call",
  "alias": "http_client",
  "result_alias": "http_response",
  "status": "ok",
  "attempt": 1,
  "duration_ms": 456.78
}
```

Error variant:
```python
{
  "phase": "call",
  "action": "call",
  "alias": "http_client",
  "status": "error",
  "error": "call http_client failed (attempt 3)",
  "code": "E_RUNTIME",
  "attempt": 3,
  "duration_ms": 1234.56
}
```

**2. `let` (variable assignment)**:
```python
{
  "phase": "let",
  "action": "let",
  "target": "user_id",
  "status": "ok",
  "duration_ms": 0.12
}
```

**3. `if` (conditional branch)**:
```python
{
  "phase": "if",
  "action": "if",
  "condition": "user.role == 'admin'",
  "branch": "then" | "else",
  "status": "ok",
  "duration_ms": 12.34
}
```

**4. `parallel` (concurrent execution)**:
```python
{
  "phase": "parallel",
  "action": "parallel",
  "branches": ["branch_0", "branch_1"],
  "status": "ok",
  "duration_ms": 234.56
}
```

**5. `fanout` (conditional multi-branch)**:
```python
{
  "phase": "fanout",
  "action": "fanout",
  "source": "results",
  "branches": ["case_success", "case_failure"],
  "cases": [
    {"label": "case_success", "condition": "result.ok == true"},
    {"label": "case_failure", "condition": "result.ok == false"}
  ],
  "status": "ok",
  "duration_ms": 345.67
}
```

**6. `merge` (combine results)**:
```python
{
  "phase": "merge",
  "action": "merge",
  "target": "combined",
  "mode": "dict" | "append" | "collect" | None,
  "append_key": "items",  # for append/collect modes
  "sources": [
    {"path": "branch_0.result", "alias": "first"},
    {"path": "branch_1.result", "alias": "second"}
  ],
  "status": "ok",
  "duration_ms": 56.78
}
```

**7. `state` (scoped execution)**:
```python
{
  "phase": "state",
  "action": "state",
  "name": "auth_state",
  "status": "ok",
  "duration_ms": 123.45
}
```

### Node Interpreter Timeline Events

**Status**: ❌ **NOT IMPLEMENTED**

No Node.js interpreter exists (`language/` contains only Python files). Timeline event emission is interpreter-specific, not runner-specific.

---

## Go and .NET Runners

**Status**: No Go or .NET runner implementations found in repository.

Expected locations:
- `runners/go/runner.go`
- `runners/dotnet/Runner.cs`

Wave 2 smoke tests (`tests/tools/test_go_adapters.py`, `tests/tools/test_dotnet_adapters.py`) test **tool adapters**, not runners.

---

## Parity Gaps & Recommendations

### Runner Envelope Parity: ✅ Complete

Python and Node runners have identical envelope schemas and method coverage.

**Minor implementation differences**:
1. **Node adds logging metadata** — Logs process start/exit events; Python doesn't.
2. **Node augments PATH** — Adds Homebrew paths for macOS; Python uses system default.

**Recommendation**: Document these differences but no action required — behavior is correct for each platform.

### Timeline Event Parity: ⚠️ Blocked

Timeline events are emitted by interpreters, not runners. Since no Node interpreter exists:

1. **Short-term** (Wave 2/3): Document that timeline events are Python-only.
2. **Long-term** (Wave 4): Implement Node interpreter (`language/interpreter.js`) with equivalent event emission.

**Action items**:
- [ ] Document in `docs/development-guide.md` that timeline events require Python interpreter.
- [ ] Add Wave 4 task: "Implement Node interpreter with timeline event parity."

### Health/Stop Semantics: ✅ Aligned

Both runners implement health checks and process termination identically:
- Health always returns `ok: true` with `ready: true/false` (no exceptions).
- Stop sends SIGTERM to PID.
- Error codes match (`E_RUNTIME` for process failures).

**Recommendation**: No action required.

---

## Runner Protocol Compliance

Both runners comply with the MCP v1 runner protocol:

1. ✅ Accept JSON request on stdin (Node also supports `--json` arg).
2. ✅ Emit JSON response on stdout.
3. ✅ Use standard envelope: `{ok, version, data/error}`.
4. ✅ Implement 4 required methods: `apply`, `start`, `stop`, `health`.
5. ✅ Use error codes: `E_JSON`, `E_FS`, `E_RUNTIME`, `E_METHOD`.

**Additional runner protocol requirements** (from `docs/development-guide.md`):
- [ ] **Telemetry** — Runners don't emit telemetry events directly; daemon should capture runner invocations.
- [ ] **Policy hooks** — Runners don't enforce policies; daemon enforces at orchestration layer (Wave 3).

---

## Testing Coverage

### Existing Tests

**Runner smoke tests**: None found for runners themselves.

**Adapter smoke tests** (Wave 2):
- `tests/tools/test_node_adapters.py` — Tests **tool adapters**, not runner protocol.
- `tests/tools/test_go_adapters.py`
- `tests/tools/test_rust_adapters.py`
- `tests/tools/test_dotnet_adapters.py`

### Recommended Tests

Create runner protocol compliance tests:

**`tests/runners/test_python_runner.py`**:
```python
def test_apply_writes_files():
    result = run_runner("python", {"method": "apply", "target_dir": tmp, "files": [...]})
    assert result["ok"] is True
    assert result["data"]["writes"] == 1

def test_start_spawns_process():
    result = run_runner("python", {"method": "start", "cmd": "sleep 1", ...})
    assert result["ok"] is True
    assert "pid" in result["data"]

def test_health_checks_port():
    result = run_runner("python", {"method": "health", "port": 8080})
    assert result["ok"] is True
    assert "ready" in result["data"]

def test_stop_terminates_process():
    result = run_runner("python", {"method": "stop", "pid": 12345})
    assert result["ok"] is True
```

**`tests/runners/test_node_runner.py`**: Mirror tests for Node runner.

**`tests/runners/test_runner_parity.py`**: Cross-runner validation:
```python
@pytest.mark.parametrize("runner", ["python", "node"])
def test_envelope_schema(runner):
    # Verify all runners return identical envelope structure
    pass
```

---

## Summary Table

| Aspect | Python | Node | Go | .NET | Parity |
| --- | --- | --- | --- | --- | --- |
| **Runner Protocol** | | | | | |
| Envelope schema | ✅ | ✅ | ❌ | ❌ | ✅ |
| `apply` method | ✅ | ✅ | ❌ | ❌ | ✅ |
| `start` method | ✅ | ✅ | ❌ | ❌ | ✅ |
| `stop` method | ✅ | ✅ | ❌ | ❌ | ✅ |
| `health` method | ✅ | ✅ | ❌ | ❌ | ✅ |
| Error codes | ✅ | ✅ | ❌ | ❌ | ✅ |
| **Timeline Events** | | | | | |
| Interpreter exists | ✅ | ❌ | ❌ | ❌ | ❌ |
| `call` events | ✅ | ❌ | ❌ | ❌ | N/A |
| `let` events | ✅ | ❌ | ❌ | ❌ | N/A |
| `if` events | ✅ | ❌ | ❌ | ❌ | N/A |
| `parallel` events | ✅ | ❌ | ❌ | ❌ | N/A |
| `fanout` events | ✅ | ❌ | ❌ | ❌ | N/A |
| `merge` events | ✅ | ❌ | ❌ | ❌ | N/A |
| `state` events | ✅ | ❌ | ❌ | ❌ | N/A |

---

## Next Steps

### Wave 2 (Current)

- [x] Document runner envelope parity (this file).
- [ ] Update `docs/execution-plan.md` to mark "Compare timeline payloads for Python vs Node runners" complete.
- [ ] Create runner protocol compliance tests (`tests/runners/`).

### Wave 3

- [ ] Document policy hook expectations per runner in `docs/development-guide.md`.
- [ ] Implement policy enforcement in daemon (network/filesystem/secrets).

### Wave 4

- [ ] Implement Node interpreter (`language/interpreter.js`) with timeline event parity.
- [ ] Implement Go runner (`runners/go/runner.go`).
- [ ] Implement .NET runner (`runners/dotnet/Runner.cs`).
- [ ] Implement Rust runner (`runners/rust/runner.rs`).

---

## References

- **Python runner**: `runners/python/runner.py`
- **Node runner**: `runners/node/runner.js`
- **Python interpreter**: `language/interpreter.py`
- **Execution plan**: `docs/execution-plan.md`
- **Runner protocol**: `docs/development-guide.md` (§ Runner Protocol)
- **Adapter smoke tests**: `tests/tools/test_*_adapters.py`