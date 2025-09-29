# Promptware Execution Plan

This playbook captures the path from today’s foundation to the full agent-native Promptware platform. It is intended for any agent or human contributor picking up the work.

---

## Wave 1 — Language Surface & Telemetry

| Milestone | Description | Status |
| --- | --- | --- |
| DSL grammar refinement | Finalise syntax for dataflow (`alias.input.from`), state, expressions, and error taxonomy; update parser/formatter/linter/golden tests. | ✅ |
| Interpreter orchestration | Replace auto-generated Python with AST-driven execution supporting state/retries/fan-in/out. Ensure interpreter timeline events align with daemon traces. | ✅ |
| Timeline documentation | Publish the event schema (phases, fields, status codes) and add CLI contract tests for interpreter output. | ✅ |

Validation: `python3 -m pytest tests/test_dsl_parser.py tests/test_dsl_interpreter.py tests/test_cli_run.py` (passes via LibreSSL-hosted Python 3.9 environment).

---

## Wave 2 — Cross-Language Tooling

| Milestone | Description | Status |
| --- | --- | --- |
| Toolgen templates | Finish Node/Go/Rust/.NET adapter templates for the 36 tools, with smoke tests per runtime. | ☐ |
| Runner parity | Ensure run/start/health/stop instrumentation works identically across Python/Node/Go/.NET (timeline events, policy hooks). | ☐ |
| Host SDK shims | Publish Python/Node SDKs wrapping MCP verbs + timeline helpers so external apps/agents can integrate. | ☐ |
| CI batching | Add sequential test batches (`tools`, `verbs`, `runners`, `e2e`) once the pytest shim supports heavy suites. | ☐ |

### Wave 2 Kickoff Plan

**Focus** — Align toolgen, runners, and SDKs so non-Python adapters reach parity without regressing existing pipelines.

**Immediate tasks**
- Draft language-specific adapter template specs (Node/Go/Rust/.NET) and document smoke-test expectations for each runtime.
- Inventory runner timeline/policy hook gaps across languages; record actionable items in `STATUS.md`.
- Outline Python/Node SDK packages (namespaces, MCP verb coverage, timeline helper API) and flag open questions on publishing.
- Extend CI wiring so `scripts/run_test_batches.sh` runs inside Make/CI workflows to replace the long-running `pytest` invocation.

**Risks & dependencies**
- Template packaging conventions for non-Python languages still pending confirmation beyond the shared adapter file layout noted below.
- SDK docs will live under `docs/sdk/`; ensure cross-links back to runner internals so the two sources stay in sync.

### Adapter Packaging Notes

- Generated adapters land in `tools/<package>/adapters/` using `_package_name(tool_id)` (e.g., `api-auth` → `api_auth`).
- Filenames follow `ADAPTER_FILENAMES` in `cli/toolgen.py` (`adapter_node.js`, `adapter_go.go`, `adapter_rust.rs`, `Adapter.cs`).
- Current language stubs export a synchronous `handle` entry point: CommonJS (`module.exports`) for Node, `package main` with `Handle` for Go, `pub fn handle` returning `serde_json::Value` for Rust, and a static `Adapter.Handle` method for .NET.
- Smoke tests should validate these entry points without additional build tooling (no bundlers, default `go test`, `cargo test`, `dotnet test`).
- Node adapters stay dependency-free (no per-tool `package.json`); daemon-managed bootstrap installs any declared `dep node ...` packages.
- Go adapters compile via ephemeral modules provided by the daemon (no per-tool `go.mod`).
- Rust adapters rely on daemon-generated Cargo manifests that vend allowed crates (`serde_json`, `reqwest`, etc.); templates should not commit `Cargo.toml`.
- .NET adapters run inside daemon-created SDK-style projects targeting `net7.0`; no per-tool `.csproj` files yet—documented templates assume a static `Adapter` class.
- Open questions: codify manifest strategy for Rust/.NET once we introduce shared helper crates and decide how to expose reusable validation utilities.

### Wave 2 Task Tracker

- Toolgen templates
  - [x] Draft Node adapter template spec and outline smoke test approach (`docs/toolgen-node-adapter-template.md`).
  - [x] Define Go adapter template (module layout, build, tests) (`docs/toolgen-go-adapter-template.md`).
  - [x] Define Rust adapter template (Cargo integration notes, blocking clients) (`docs/toolgen-rust-adapter-template.md`).
  - [x] Define .NET adapter template (SDK-style build, testing) (`docs/toolgen-dotnet-adapter-template.md`).
  - [ ] Update toolgen CLI docs to cover multi-language flags and template selection.

- Runner parity
  - [ ] Compare timeline payloads for Python vs Node runners and log deltas.
  - [ ] Verify health/stop semantics for Go/.NET envelopes; align error codes.
  - [ ] Document required policy hooks per runner (network/filesystem/secrets).
  - [ ] Capture outstanding work items in `STATUS.md` for follow-up sprints.

- Host SDK shims
  - [x] Decide documentation home (`docs/sdk/`) and seed structure.
  - [ ] Nail down package names and versioning strategy for Python/Node SDKs.
  - [ ] Prototype MCP verb wrappers with timeline helper utilities.
  - [ ] Draft quick-start docs and examples for integrating the SDKs.
  - [ ] Decide on distribution (PyPI/npm) and establish publish checklists.

- CI batching
  - [ ] Integrate `scripts/run_test_batches.sh` into `make test`.
  - [ ] Update CI config to call the batch script sequentially.
  - [ ] Add documentation on interpreting batch outputs and reruns.
  - [ ] Measure runtime vs full `pytest` and capture results in the README.
  - [x] Implement Node adapter smoke-test harness (`tests/tools/test_node_adapters.py`).
  - [x] Implement Go adapter smoke-test harness (`tests/tools/test_go_adapters.py`).
  - [x] Implement Rust adapter smoke-test harness (`tests/tools/test_rust_adapters.py`).
  - [x] Implement .NET adapter smoke-test harness (`tests/tools/test_dotnet_adapters.py`).

---

## Wave 3 — Orchestration & Marketplace

| Milestone | Description | Status |
| --- | --- | --- |
| Daemon policy enforcement | Enforce network/filesystem/secrets policies in `run_start_v1`, logging decisions in the timeline. | ☐ |
| Marketplace CLI | Implement `promptware marketplace ...` commands using the existing tool suite. | ☐ |
| Developer onboarding | Publish runner protocol docs, dependency policy guidelines, Promptware DSL design doc, and cross-language examples. | ☐ |

---

## Wave 4 — Natural-Language Compiler & Agent SDKs

| Milestone | Description | Status |
| --- | --- | --- |
| Prompt compiler | Build the natural-language → `.pw` compiler and surface compiler events in timelines. | ☐ |
| Agent SDKs & samples | Deliver multi-language SDKs, sample agent integrations, and marketplace workflows showing bidirectional communication. | ☐ |

---

## Cross-Cutting Tasks

- Remove committed build artifacts (`runners/dotnet/bin`, `runners/dotnet/obj`) and codify language-specific build steps.
- Expand test coverage for `httpcheck_assert_v1` and `report_finish_v1` using mocked gateway ports (assert timeline output).
- Extend stop/cleanup auditing (shim shutdown, port release) and ensure corresponding events appear in task timelines.
- Track open issues/backlog in `TODO.md` and update this document as milestones ship.

---

### Quick Status Snapshot

- **DSL & interpreter**: sequential calls, `let`, `if/else`, `parallel`, `fanout`/`merge` (with slugified `case_*` labels + `cases` timeline metadata), list indexing, and timeline output are in place.
- **Daemon lifecycle**: plan apply/deps/build/start/ready/route plus httpcheck/report/stop now emit timeline events.
- **Tool adapters**: Python templates shipped; cross-language templates/smoke tests still outstanding.
- **Docs**: roadmap and execution notes updated; runner protocol + DSL design doc still pending.

Keep this file in sync with `agents.md` so handoffs remain seamless.
