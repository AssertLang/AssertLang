# Programming Language Engineering Notes

## 1. Core Building Blocks
- **Grammar & Syntax**: Most languages formalise syntax with context-free grammars (BNF/EBNF). Surface design choices include statement vs. expression orientation (C vs. Lisp), significant whitespace (Python), and block delimiters (`{}` in C, `end` in Ruby). Harden grammar via parser generators (ANTLR, YACC), hand-written recursive descent, or Pratt parsers for operator precedence.
- **Lexing**: Tokenise input into a uniform stream. Robust lexers handle whitespace/comments, string escapes, numeric literals, and provide line/column info for diagnostics. Incremental lexers (e.g., TypeScript) enable IDE features.
- **Parsing**: Convert tokens into AST. Error recovery is critical—providing expected token hints, resynchronisation rules (consume until `;`/`}`) and context-aware messages (Rust’s “consider borrowing”).
- **AST Representation**: Immutable node structures ease analysis/transforms. Many languages segregate high-level AST (syntax) from typed IR (semantic). Serialization (e.g., Swift’s libSyntax) supports tooling.
- **Type & Semantic Analysis**: Build symbol tables, resolve identifiers, enforce type rules, and perform flow analysis. Languages like TypeScript implement structural typing; Rust executes borrow checkers over control-flow graphs. Improve diagnostics via suggestion engines (`did you mean ...`).
- **IR & Code Generation**: Lower AST into IR (LLVM IR, bytecode). Modern implementations (Rust, Swift) lean on LLVM for optimisation/backends, while dynamic langs (Python) target VM bytecode. For interpreters, evaluate AST/bytecode directly.

## 2. Robust Typable Syntax Patterns
- **Consistency & Predictability**: Reserve keywords, uniform statement termination, clear scoping. Go’s formatter (`gofmt`) enforces canonical layout. TypeScript extends JavaScript carefully—new syntax (interfaces, generics) but remains a superset.
- **Expressive Literals & Collections**: JSON-esque object literals (JavaScript, Swift) ease configuration; pattern matching (Rust, Kotlin) enrich expressiveness while ensuring exhaustiveness.
- **Modularity**: Namespaces/modules prevent collisions (Python packages, Rust crates). Support flexible import semantics (`import {foo}` vs `import foo as alias`).
- **Error-Tolerant Parsing**: IDE-friendly languages (TypeScript, Swift) retain partial AST even with syntax errors, enabling inline diagnostics.
- **Tooling Contract**: Formatters, linters, language servers (LSP) make syntax “sticky” and consistent. Provide canonical formatting to reduce diff noise (Rustfmt).

## 3. Learnings from Notable Languages
- **Rust**: Ownership model embedded in type system; borrow checker runs over MIR (mid-level IR). Syntax emphasises explicitness (`let mut`, `match`). Compiler invests heavily in friendly errors and suggestions.
- **TypeScript**: Superset strategy ensures existing JS runs unmodified; gradual typing relies on structural type system and extensive AST transforms. Compiler emits source maps for tooling.
- **Go**: Minimal syntax, built-in formatter, straightforward compilation pipeline (lex→parse→AST→SSA→machine). Emphasis on fast builds, deterministic layout, simple error model (`error` interface).
- **Swift**: Multi-phase pipeline (Parse → Sema → SIL → LLVM). grammar supports modern constructs (optionals, pattern matching). Syntax is expression-oriented; type inference combined with explicit annotation heuristics.
- **Python**: Significant whitespace, dynamic typing. CPython tokenizes, builds AST, converts to bytecode executed by VM. Error recovery historically weak but improved (PEP 617 new PEG parser). Extensive introspection support.

## 4. Hardening Strategies
- **Design for Tooling**: Provide machine-readable AST (JSON/protobuf), stable formatting, and LSP integration.
- **Diagnostics**: Multi-line caret hints (Rust), suggestion engines, context-specific messages. Provide remedial actions (“try adding …”).
- **Testing**: Parser “golden” tests (language snippets ↔ AST), fuzzing to uncover crashes, property-based tests for transformations.
- **Versioning & Compatibility**: Stabilize syntax once published; gate experimental features behind flags. Document breaking changes with migration tooling.
- **Performance**: Profile parse/analyse phases to avoid O(n²) behaviours. Use incremental compilation/caching when possible.
- **Security/Safety**: Sandboxing (browser JS), memory safety (Rust), deterministic builds (Go).

## 5. Applicability to Promptware DSL
- Start with a formal grammar covering directives, tool calls, dataflow expressions, and eventual branching constructs.
- Build an autoformatter so `.pw` programs stay consistent (Python-like significant indentation or explicit delimiters—choose early).
- Provide resilient parser error recovery (e.g., resynchronise at directive boundaries) with actionable diagnostics.
- Expose AST/plan JSON to tooling (LSP server) for completions, go-to-definition (tool alias), inline docs.
- Introduce linting rules: undefined aliases, unused tool outputs, circular dependencies.
- Plan for extension versioning (e.g., `dsl_version: 1`).
- Adopt golden tests and fuzzing to harden the parser; emit plan snapshots for regression.

## 6. DSL Archetypes & Inspirations
- **Starlark / Bazel**: Deterministic, sandboxed build DSL embedded in Go. Highlights: hermetic evaluation, explicit deps, restricted side effects. Good reference for tool invocation semantics and reproducibility guarantees.
- **CUE**: Data validation/config language that merges JSON-like structure with constraints. Demonstrates how schema + evaluation can coexist and how structural typing can drive validation prior to execution.
- **Nix**: Lazy, pure functional language for environment provisioning. Useful for describing reproducible dependency graphs and layering evaluation (attribute sets, derivations). Its approach to immutability and caching maps to Promptware’s per-task sandboxes.
- **Elm**: Strong emphasis on compiler-assisted guarantees (no runtime exceptions) and friendly error messages. Borrow its style guide for diagnostic phrasing and helpful “hint” blocks.
- **Pulumi / Terraform HCL**: Infrastructure DSLs with strong schema-driven validation and planning/execution phases. Offer patterns for diff previews, policy enforcement, and dependency graphs between resources (tools).
- **Make / Ninja**: Minimal build languages with explicit targets and prerequisites—illustrate simple DAG execution semantics and incremental rebuild strategies.

## 7. Execution, Scheduling & Interop Considerations
- **Dataflow Representation**: Treat each tool invocation as a node in a DAG. Ensure the DSL has constructs for declaring dependencies (`after`, `requires`, referencing previous aliases). Consider optional fan-out/fan-in syntax (similar to Airflow DAGs or Temporal workflows).
- **Capability Contracts**: Encode tool requirements (runtime, IO, secrets). Provide static validation so the orchestrator can reject plans lacking necessary capabilities—akin to Kubernetes admission controllers.
- **Retry & Circuit Breakers**: Borrow strategies from Temporal/Step Functions (per-step retry policies, exponential backoff, fallback branches). Keep syntax declarative but allow nested retry groups.
- **State Management**: Distinguish between ephemeral outputs (available in-memory for subsequent steps) and persisted artifacts (files, reports). Languages like Spark define transformations vs. actions; similar semantics can help avoid unintended side effects.
- **Interop with Host Languages**: Consider an FFI-like layer so existing Python/TypeScript code can embed `.pw` snippets or vice versa. Study how SQL is embedded in ORMs or how Rust’s `macro_rules!` inject DSL-like syntax.

### Current Interpreter Snapshot (2024-xx draft)
- **Action graph**: `call`, `let`, `if`, and `parallel` now execute in-process (see `language/interpreter.py`). Branch scopes inherit parent state and publish results under the branch name.
- **Retry/expect semantics**: The interpreter reuses the plan’s retry metadata and expectation checks, raising `PWExecutionError` on failure.
- **Auto-file fallback**: Plans containing only sequential actions still auto-generate a Python scaffold; parallel blocks disable that path until multi-branch scaffolds exist.
- **CLI integration**: `promptware run foo.pw` short-circuits to the interpreter when plans omit file blocks, now emitting the same PASS/FAIL banner and `ok` flag as daemon-backed runs while returning JSON responses (both interpreter and daemon paths surface an execution `events` trace for observability).
- **Fanout case naming**: Parser normalises each `case` label to a slugified identifier (`case_<slug>` or `case_<index>`). Interpreter responses and timeline payloads use those stable keys, while the event stream also records the original condition for tooling.
- **Merge fan-in**: `merge append/collect/dict` are implemented with timeline metadata (`mode`, optional `append_key`) and defensive error codes when source shapes mismatch.
- **Next focus**: tighten doc coverage, expand cross-language adapter templates, and surface policy/error taxonomy guidance alongside the interpreter.

### Timeline Events (WIP)
- Every daemon verb that mutates execution now appends to a timeline (`events` array) covering phases such as `port`, `policy`, `apply`, `build`, `deps`, `start`, `ready`, `route`, `httpcheck`, `report`, and `stop`.
- Interpreter runs emit action-level entries (`call`, `let`, `if`, `parallel`) with attempt counts and durations; the CLI surfaces the combined trace in both interpreter and daemon modes.
- Fanout events include both stable branch keys (`branches`) and a `cases` payload of `{label, condition}` entries so consumers can reconcile UI labels with original conditions.
- Downstream consumers can rely on `events[-1]['status']` to determine the latest lifecycle outcome without parsing logs.

## 8. Tooling & Developer Experience Requirements
- **Language Server (LSP)**: Provide completion for tool IDs, schema-aware argument hints, diagnostics for undefined references. Evaluate tree-sitter or a custom parser to feed the LSP.
- **Formatter & Linter**: Mirror `rustfmt`/`gofmt` behaviour—one canonical formatting pass to eliminate style debates. Lint rules should cover unused aliases, unreachable branches, inconsistent retry policies, missing metadata (e.g., summary), and the new merge diagnostics (`merge append/collect` warn when sources are not list-shaped).
- **REPL / Playground**: Offer an interactive shell or web playground where `.pw` snippets translate to plans (with dry-run execution). Use it to iterate on syntax quickly and collect telemetry about confusing errors.
- **Testing Harness**: Provide snapshot tests mapping `.pw` source to emitted plans. Include golden tests for error messages, and property-based fuzzers feeding random constructs to ensure parser resilience.
- **Versioning Strategy**: Keep the DSL versioned separately from runner APIs. Publish deprecation notes and provide migration tooling (auto-fixes) when syntax evolves.

## 9. Immediate Next Steps for Promptware DSL
1. **Cross-language templates**: Finish Node/Go/Rust/.NET adapter scaffolds so toolgen can emit fully-tested envelopes beyond Python.
2. **Host SDKs & docs**: Publish Python/Node shims that wrap MCP verbs, capture timeline helpers, and document runner/network policy expectations.
3. **Policy enforcement**: Thread network/filesystem/secret policy hooks through `run_start_v1`, reusing the error taxonomy now standardised in the interpreter.
4. **Prompt compiler RFC**: Lock the Promptware DSL → MCP plan compilation strategy (grammar, orchestration primitives, retries/fan-in semantics).
5. **Extended testing**: Add gateway mock tests, `merge`/fanout golden fixtures, and sequential pytest batches so CI covers the expanded grammar without tripping sandbox limits.

Keep this document updated as we study additional languages or adopt new engineering practices.
