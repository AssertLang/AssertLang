## Mission: Bootstrap Promptware Standard Library (STDLIB) Foundations

**Assigned branch:** `feature/pw-standard-librarian` (tracked off `upstream/main`)  
**Primary objective:** Translate the research roadmap into concrete deliverables that establish Promptware’s core standard library and supporting infrastructure.

### Context & Constraints
- Promptware DSL parser/IR already exists; this effort focuses on runtime + stdlib layers.
- Keep work stages modular so we can demo incremental capability (CLI, tests) after each phase.
- Always preserve dual-remote workflow: push intermediate work to `origin/feature/pw-standard-librarian`, submit PRs to `upstream/main`.
- Document every milestone in `docs/stdlib/` (create if absent) so future agents inherit clear specs.

### Phase 0 – Language Core Verification (Sanity Pass)
1. **Spec audit** – Confirm grammar + type-system docs cover data structures the stdlib will expose (Option, Result, collections).
2. **Parser golden tests** – Add representative `.pw` programs for upcoming stdlib APIs (e.g., async iterators, map/filter syntax) to `tests/golden/`.
3. **IR coverage** – Extend IR tests to ensure lowering rules exist for pattern matching, option/result usage, async constructs needed later.

**Exit check:** `pytest` passes with new fixtures; docs updated to reference planned stdlib features.

### Phase 1 – Runtime Baseline
1. Choose execution strategy (bytecode VM vs. transpiler) and spike minimal runtime harness in `runtime/`.
2. Implement capability-gated effect system skeleton (fs/net/time) so stdlib modules can request permissions.
3. Add cooperative async scheduler prototype: promise/future objects, cancellation tokens, timers.

**Exit check:** A `.pw` sample using async sleep + capability checks runs via `pw run`.

### Phase 2 – Tooling Preparation
1. Create initial CLI verbs (`pw run`, `pw test`, `pw fmt`, `pw lint`) with stubs calling existing compiler + runtime.
2. Sketch LSP plan (hover/type info) and ensure repo structure supports future integration (place dummy server entry point under `tools/lsp/`).

**Exit check:** CLI commands dispatch without crash (even if some subcommands are stubbed) and are covered by unit tests.

### Phase 3 – Standard Library (P0 scope)
Implement modules under `stdlib/` with clear boundaries and capability enforcement.

| Module | Key APIs | Notes |
| ------ | -------- | ----- |
| `core` | `Option`, `Result`, `assert`, ordering/hashing | Provide trait implementations for equality/ordering |
| `types` | `String`, `Bytes`, `List`, `Map`, `Set`, `Deque`, `Tuple`, `Record` | Include methods for iteration, cloning, slicing |
| `iter` | `Iterator`, `map`, `filter`, `reduce`, `zip`, `window` | Support async iterators |
| `fmt` | Formatting/interpolation, locale-aware numbers/dates | Should integrate with `time/datetime` |
| `time`, `datetime` | Monotonic clock, timers, timezone-aware datetime | Use capability-checked system clock |
| `path`, `fs` | Path ops, read/write/stream, atomic writes | All FS access gated by capability |
| `net`, `http` | TCP/UDP, DNS, TLS client, HTTP client w/ retries/backoff | Async, non-blocking |
| `json`, `base64`, `hex` | DOM + streaming parser/encoder; encode/decode utilities | Performance within 15% of native baseline |
| `hash`, `secrets` | SHA-2/3, BLAKE3, HMAC, CSPRNG, constant-time ops | Zeroize secrets in drop |
| `async` | Task creation, futures, cancellation, timeouts | Integrates with runtime scheduler |
| `log` | Structured logging with leveled sinks (console/file) | Provide default console logger |

**Cross-cutting requirements**
- Deterministic tests: freeze clock/RNG via injected capability mocks.
- Diagnostics: failures surface `.pw` source snippet + fix hint.
- Performance SLA: publish basic benchmarks (p50/p95 latency) comparing to reference native libs.

**Exit check:** `pw test stdlib` passes; sample application (`examples/stdlib/async_http_client.pw`) works end-to-end.

### Phase 4 – Documentation & Examples
1. Generate task-oriented docs under `docs/stdlib/` for each module (usage, capabilities needed).
2. Provide tutorial: “Build a HTTP client with retries in 50 lines of PW”.
3. Update `README.md` / `Current_Work.md` with status + next steps.

### Deliverables & Reporting
- Push code + docs to `feature/pw-standard-librarian`, regularly backing up to `origin`.
- Maintain progress log in `.claude/Task Agent 1/ta1-current-progress.md` (daily updates).
- On completion of each phase, open PR to `upstream/main` referencing this mission and include test results + benchmarks.

### Stretch Goals (if core completed ahead of schedule)
- Begin P1 stdlib modules (http.server, regex, csv, process, concurrency primitives).
- Prototype `pwpm` registry interactions for distributing stdlib as versioned packages.
- Draft CI plan for determinism/performance gates (benchmark runner + threshold checks).
