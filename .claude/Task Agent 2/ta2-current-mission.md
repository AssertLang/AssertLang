## Mission: Establish Promptware Runtime & CLI Experience

**Assigned branch:** `feature/pw-runtime-core` (create from `upstream/main`)  
**Primary objective:** Deliver a runnable Promptware runtime with capability-aware execution and the first unified `pw` CLI commands.

### Scope & Priorities
1. **Runtime Architecture**
   - Author `docs/runtime/ARCHITECTURE.md` comparing bytecode VM vs. transpiler. Recommend and fix on one approach (likely bytecode VM with capability sandbox).
   - Define bytecode instruction set, frame layout, and value representation.
2. **Execution Engine**
   - Implement minimal interpreter in `runtime/` (parser already emits IR; add lowering to bytecode).
   - Wire capability gating layer (fs/net/time/crypto). Expose guard API for stdlib modules (coordination with TA1).
   - Add cooperative async scheduler: tasks, futures, timers, cancellation tokens, backpressure hooks.
3. **CLI Bootstrap**
   - Create `pw` CLI (Python entrypoint acceptable initially) with subcommands: `pw run`, `pw build`, `pw fmt`, `pw lint`, `pw test`.
   - Ensure `pw run examples/hello-world.pw` executes through the new runtime with colored output + structured logs.
4. **Testing & Observability**
   - Build runtime smoke tests under `tests/runtime/` (cover capability enforcement, async scheduling, error propagation).
   - Implement stack-trace mapping: errors should report `.pw` line/column using source maps.
5. **Deliverables**
   - Runtime crate/module with docs.
   - CLI package ready for installation (document `pip install -e .` flow).
   - Sample programs showcasing timers, async HTTP via stubbed stdlib functions (in coordination with TA1).

### Exit Criteria
- `pw run` executes sample `.pw` files directly (no transpile backends).
- Capability checks fail closed by default; tests confirm enforcement.
- Async scheduler supports sleep/cancel; cooperative cancellation works in demo.
- Stack traces map to `.pw` lines with helpful diagnostics.
- Documentation (`docs/runtime/ARCHITECTURE.md`, `docs/cli/README.md`) published.

### Coordination
- Sync with **TA1** on capability API and async primitives used by stdlib.
- Provide command contract to **TA3** so LSP/formatter invoke CLI seamlessly.
- Update `.claude/Task Agent 2/ta2-current-progress.md` after each milestone (architecture draft, VM prototype, CLI release).
