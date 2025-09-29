# Promptware TODO

## 1. Gateway & Networking
- [x] Support a "no-gateway" mode for sandboxed CI where TCP bind is prohibited; mock httpcheck/report responses accordingly.
- [x] Surface gateway port in `report_finish_v1` payload so clients don’t rely on CLI output alone.

## 2. Runner Ecosystem
- [x] Apply the single-envelope cleanup and regression tests to the Go runner.
- [x] Add regression tests for the .NET runner envelope (skipped if dotnet is unavailable).
- [x] Add readiness hooks (`health`) to Go/.NET runners and integrate into `run_start_v1` before routing traffic.
- [x] Complete per-language dependency bootstrap (Go/.NET/Rust) and enforce allowlists.
- [x] Add cache reuse (hashed env dirs) for dependency downloads once policy gating is in place.
- [x] Extend dependency allowlist with explicit private registry configuration (npm registries, NuGet feeds, Cargo registries) and policy controls.
- [x] Trim dependency caches automatically on daemon startup (respect allowlist TTL hints).
- [ ] Add cross-language templates (Node, Go, Rust, .NET) so toolgen can emit adapters beyond Python (auth/api-auth/http/rest/storage/conditional/branch/async/loop/output/transform complete; extend remaining specs).
- [ ] Ship official host SDKs that wrap MCP verbs for Python/Node/Go/.NET consumers.

## 3. Daemon Enhancements
- [ ] Differentiate runner failures: bubble up `E_BUILD` vs `E_RUNTIME` based on runner output.
- [ ] Streamline manifest/run responses with capabilities, readiness, and policy metadata.
- [ ] Add graceful shutdown & cleanup of shim processes in `stop_task`, ensuring leased ports release on errors.
- [ ] Implement policy enforcement hooks (network/filesystem/secrets) during `run_start_v1` execution.

## 4. Tooling & Tests
- [ ] Expand test coverage for `httpcheck_assert_v1` and `report_finish_v1` using a mocked gateway port.
- [x] Audit tool implementations against schemas, adding adapter-focused tests per tool family.
- [ ] Remove committed build artifacts (`runners/dotnet/bin`, `runners/dotnet/obj`) and add build steps instead.
- [ ] Add CI job that runs test batches sequentially (`tools`, `verbs`, `runners`, `e2e`).
- [x] Build smoke tests for generated adapters in other languages once templates land (Node/Go/Rust/.NET harnesses implemented; docs under `docs/testing-*-adapter-smoke-tests.md`).

## 5. Documentation & DX
- [ ] Update `/docs` to reflect dynamic port behavior and the refined plan/start pipeline.
- [ ] Document the runner protocol (methods, expected envelopes, error codes) in developer guides.
- [x] Provide instructions for configuring dependency allowlists and plan policies (see `docs/dependency-management.md`).
- [x] Document available toolgen templates & `_package_name` behaviour.
- [x] Document CLI helpers for dependency inspection and cache trimming (`promptware deps ...`).
- [ ] Author a “Promptware DSL” design doc outlining syntax → plan compilation.

## 6. Promptware Language Roadmap
- [ ] Design the Promptware DSL/grammar and compiler into MCP plans.
- [ ] Implement orchestration primitives (state, retries, fan-in/fan-out) on top of tools.
- [ ] Integrate marketplace flows (upload/list/install) with the CLI using generated tools.
- [ ] Publish developer onboarding guides and examples for writing cross-language Promptware programs.

Maintain this list as tasks complete; keep items small and actionable.
