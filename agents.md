# Promptware Agent Guide

## Mission
Deliver Promptware as a reliable, agent-native platform that converts natural-language intent into ephemeral applications exposed through the gateway at port 23456 (or an approved fallback). Code must stay clean, minimal, and production-worthy.

## Current Signal Check
- Tool adapters: all 36 Promptware tools are generated via toolgen and exercised through adapter-focused pytest suites (`tests/tools`).
- Daemon: `run_start_v1` hydrates registry policy/env defaults, prepares Python/Node deps, and exposes fallback direct ports when the gateway cannot bind.
- Runners: Python/Node/Go/.NET envelopes covered by regression tests; Go/.NET health checks integrated. Dependency bootstrap now provisions Python/Node/Go/.NET/Rust caches with allowlist enforcement, hashed cache reuse, registry/feed plumbing, and automatic cache trimming on daemon start.
- Full `pytest` run still hits the macOS sandbox timeout; use `scripts/run_test_batches.sh` to cover `mvp_e2e`, `runners_io`, `verbes_contracts`, and `tools` sequentially.
- DSL/interpreter: fanout/state/merge features all run through the AST interpreter; timeline events expose `phase`, retry attempts, merge `mode`, and append keys so downstream tooling can mirror daemon traces.

### Execution Plan Snapshot (see `docs/execution-plan.md`)
- **Wave 1**: ✅ DSL grammar/error taxonomy complete; AST interpreter + timeline docs/tests are live.
- **Wave 2**: ship cross-language toolgen templates + smoke tests, ensure runner parity, publish Python/Node SDKs, add CI batch runner.
- **Wave 3**: enforce daemon policies, wire marketplace CLI, deliver runner protocol + DSL design documentation.
- **Wave 4**: build prompt→plan compiler, release multi-language agent SDKs + marketplace samples.

Cross-cutting inflight: expand timeline coverage (httpcheck/report/stop done), remove committed build artifacts, add gateway mock tests, audit shim shutdown logging.

Assume cross-language adapters and dependency bootstrap beyond Python/Node are still TODO.

Wave 1 status: DSL grammar, interpreter orchestration, and timeline docs/tests all verified via `python3 -m pytest tests/test_dsl_parser.py tests/test_dsl_interpreter.py tests/test_cli_run.py`.

### Wave 2 Kickoff

Focus: unlock cross-language tooling so toolgen output, runners, and SDKs stay in lockstep.

Immediate next steps:
- Finalise Node/Go/Rust/.NET adapter templates in toolgen, including smoke-test scaffolds and language-specific build notes.
- Audit runner parity (start/stop/timeline/policy hooks) across Python/Node/Go/.NET and capture gaps in `STATUS.md` for follow-up.
- Draft the host SDK surface for Python/Node, covering MCP verb wrappers, timeline helpers, and error taxonomy alignment.
- Wire the `scripts/run_test_batches.sh` workflow into CI/make targets so heavy suites can run without macOS timeouts.

Dependencies & blockers:
- Need confirmation on template packaging conventions for non-Python languages (namespaces, publish flow).
- SDK docs will live under `docs/sdk/`; cross-link to runner docs once they land.

## Implementation Roadmap
1. **Runner Ecosystem (Phase 0)**
   - ✅ Single-envelope cleanup & regression tests for Python/Node/Go/.NET runners.
   - ✅ Health probes wired into `run_start_v1`.
   - ✅ Implement dependency bootstrap + allowlists for Go/.NET/Rust.
   - ⏳ Add non-Python adapter templates so toolgen can emit cross-language adapters.
   - ⏳ Publish host SDKs (Python/Node/Go/.NET) that wrap MCP verbs.

2. **Daemon Runtime (Phase 1)**
   - ✅ `run_start_v1` merges registry env/policy defaults, prepares deps, and exposes fallback ports.
   - ⏳ Differentiate runner failures (`E_BUILD` vs `E_RUNTIME`), enrich manifests with capabilities/health, enforce policy hooks (network/fs/secrets).

3. **Gateway & Networking (Phase 2)**
   - ✅ Fallback direct access when the gateway can’t bind; task stop tears down routes.
   - ⏳ Add per-task shim cleanup auditing and extend tests for UDS/TCP edge cases.

4. **Tooling & Tests (Phase 3)**
   - ✅ Generated adapters + tests for all tools.
   - ⏳ Build cross-language adapter templates; expand CI to run test batches sequentially.
   - ⏳ Remove committed build artifacts and ensure `make test` covers batches.

5. **Docs & DX (Phase 4)**
   - ✅ Document toolgen templates and `_package_name` behaviour.
   - ⏳ Update runner protocol docs, dependency policy guidelines, and port fallback references.
   - ⏳ Draft Promptware DSL design + developer onboarding.

6. **Language Vision (Phase 5)**
   - ⏳ Define the Promptware DSL/grammar → MCP plan compiler.
   - ⏳ Implement orchestration primitives (state, retries, fan-in/out).
   - ⏳ Integrate marketplace flows (upload/list/install).
   - ⏳ Provide examples/SDKs demonstrating cross-language Promptware programs.

Track progress in the repo root (e.g., `STATUS.md`) if needed; avoid duplicating this guide.

## Execution Workflow
1. **Assess** — Review outstanding issues, check git status, confirm no foreign changes.
2. **Plan** — Use `update_plan` (Codex CLI) for multi-step tasks; never start coding without a written plan.
3. **Implement** — Make small, verifiable changes; prefer language-appropriate standards (Black/Ruff, gofmt/go test, etc.).
4. **Validate** — Run targeted tests (`pytest`, custom runner scripts). Document any un-run tests in the final report.
5. **Report** — Summarize changes, reference files with line numbers, suggest next steps if natural.

## Coding Tenets
- Keep code sparse and expressive; add comments only when the intent is non-obvious.
- Fail fast with informative errors (`E_BUILD`, `E_RUNTIME`, etc.).
- Avoid hidden side effects; keep runners pure in/out via JSON.
- Maintain compatibility with macOS/Linux dev environments.

## Tooling Cheat Sheet
- `pytest` / `python -m pytest tests/...` — test suite.
- `python runners/python/runner.py` — direct runner invocation (expects JSON on stdin).
- `node runners/node/runner.js --json '{}'` — Node runner check.
- `make lint`, `make test` — once Makefile targets are wired in.

## Communication & Handoff
- Record partially completed work and blockers in the final AI response.
- Reference files with clickable paths (`path/to/file.py:42`).
- Avoid reverting user edits; call out unexpected repo state before proceeding.

## Known Backlog (keep updated)
- Containerized isolation for runners / sandboxing strategy.
- Private registry configuration & cache policy tuning (base plumbing is live; add auth/rotation policies and retention controls).
- Non-Python adapter templates in toolgen (Node, Go, Rust, .NET).
- Promptware DSL compiler & orchestration runtime.
- Marketplace command surface (`promptware marketplace ...`).
- Long-running CI: replace full `pytest` with `scripts/run_test_batches.sh` or lift the sandbox timeout.

Stay focused, keep everything clean and incremental, and always leave the repo in a better state than you found it.
