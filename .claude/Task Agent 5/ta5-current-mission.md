## Mission: Cross-Language Conformance & Interop Reliability

**Assigned branch:** `feature/pw-interop-parity` (create from `upstream/main`)  
**Primary objective:** Guarantee Promptware’s “universal translator” promise by hardening generators/parsers, expanding the conformance suite, and delivering FFI v2.

### Scope & Deliverables
1. **Conformance Suite v1**
   - Build `tests/conformance/` with canonical PW programs covering control flow, async, error handling, generics/enums.
   - For each target (Python, Node, Go, Rust, C#) generate code, run, and compare outputs against golden fixtures.
   - Automate via `scripts/run_conformance.py` with CI-friendly JSON reports.
2. **Reverse Parsing Reliability**
   - Audit `language/*_parser_v2.py` for feature gaps (enums, async iterators, pattern matching).
   - Add round-trip tests: target source → IR → target to ensure idempotence.
3. **FFI v2**
   - Design type-safe marshalling (zero-copy buffers when possible) between PW runtime and Python/Node/Rust.
   - Create `docs/ffi/FFI_SPEC.md` with ABI details, safety constraints, examples.
   - Publish sample integrations (e.g., call Rust crypto lib from PW).
4. **Performance & Determinism Checks**
   - Benchmark translation overhead and runtime execution per language.
   - Implement deterministic mode (frozen RNG/clock) for reproducible tests.
5. **Tooling Support**
   - Provide CLI command `pw conformance` (coordinate with TA2) to run full suite.
   - Expose summary badges consumable by CI dashboards.

### Exit Criteria
- Conformance suite passes on all official targets with nightly CI runs.
- Round-trip tests above 95% coverage for supported language features.
- FFI v2 demos published with documentation and automated tests.
- Translation performance metrics documented in `docs/benchmarks/INTEROP.md`.

### Coordination
- Work with **TA1** (stdlib) to ensure new types/features have generator coverage.
- Partner with **TA2** (runtime) for runtime ↔ generator alignment.
- Sync with **TA4** to publish conformance results and highlight in roadmap.
