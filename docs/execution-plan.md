# Promptware Execution Plan

This playbook captures the path from today’s foundation to the full agent-native Promptware platform. It is intended for any agent or human contributor picking up the work.

---

## Wave 1 — Language Surface & Telemetry

| Milestone | Description | Status |
| --- | --- | --- |
| DSL grammar refinement | Finalise syntax for dataflow (`alias.input.from`), state, expressions, and error taxonomy; update parser/formatter/linter/golden tests. | ✅ |
| Interpreter orchestration | Replace auto-generated Python with AST-driven execution supporting state/retries/fan-in/out. Ensure interpreter timeline events align with daemon traces. | ✅ |
| Timeline documentation | Publish the event schema (phases, fields, status codes) and add CLI contract tests for interpreter output. | ✅ |

---

## Wave 2 — Cross-Language Tooling

| Milestone | Description | Status |
| --- | --- | --- |
| Toolgen templates | Finish Node/Go/Rust/.NET adapter templates for the 36 tools, with smoke tests per runtime. | ☐ |
| Runner parity | Ensure run/start/health/stop instrumentation works identically across Python/Node/Go/.NET (timeline events, policy hooks). | ☐ |
| Host SDK shims | Publish Python/Node SDKs wrapping MCP verbs + timeline helpers so external apps/agents can integrate. | ☐ |
| CI batching | Add sequential test batches (`tools`, `verbs`, `runners`, `e2e`) once the pytest shim supports heavy suites. | ☐ |

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
