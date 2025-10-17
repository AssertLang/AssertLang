# Claude Code Native Agent Architecture

**Date**: 2025-10-14
**Context**: Professional development team mapped to Claude Code automation
**Team Size**: 7 specialized agents (6 core + 1 MCP specialist)

## Overview

This document defines a production-ready Claude Code agent system based on professional software development team structure. Each agent is a specialized Claude instance with specific expertise, mission scope, and coordination dependencies.

## Agent Roster

| Agent ID | Professional Role | Mission Focus | Branch Pattern | Expertise Domain |
|----------|------------------|---------------|----------------|------------------|
| **Lead Agent** | Compiler Architect | Orchestration, Architecture, Integration | `main` | Full-stack coordination, research, releases |
| **TA1** | Language Engineer #1 | Standard Library & Language Features | `feature/pw-standard-*` | Type systems, stdlib design, API design |
| **TA2** | Language Engineer #2 | Runtime & Execution Model | `feature/pw-runtime-*` | VM architecture, capability model, async |
| **TA3** | DevTools Engineer | Developer Experience & Tooling | `feature/pw-tooling-*` | LSP, IDE integration, CLI UX |
| **TA4** | Test/QA Engineer | Quality, Ecosystem, Governance | `feature/pw-ecosystem-*` | Testing frameworks, benchmarking, QA |
| **TA5** | Codegen Specialist | Cross-Language Code Generation | `feature/pw-interop-*` | Multi-target codegen, FFI, conformance |
| **TA6** | Release Engineer | Safety, CI/CD, Automation | `feature/pw-safety-*` | Security auditing, fuzzing, release pipelines |
| **TA7** | MCP Specialist | Operations Discovery & Integration | `feature/pw-mcp-*` | MCP protocol, operation binding, multi-language ops |

---

## Lead Agent (Compiler Architect)

**Role**: Full-stack engineering lead managing all development work

**Responsibilities**:
- Coordinate all 7 task agents (spawn, monitor, integrate)
- Conduct deep research before major features (stdlib, type systems, VM design)
- Make architectural decisions (transpiler vs VM, type system design)
- Integrate work from isolated agent branches
- Manage releases, versioning, changelogs
- Maintain master plan and dependency graphs
- Quality gatekeeper (all work must pass tests + docs + benchmarks)

**Tools**:
- `scripts/check_status.sh` - Check all TA agent status
- `scripts/check_deps.sh` - Analyze critical path
- `scripts/update_status.py` - Sync status files
- `scripts/create_ta.sh` - Bootstrap new agents
- `scripts/release.sh` - Full release automation

**Files Owned**:
- `CLAUDE.md` (agent roster)
- `Current_Work.md` (project status)
- `.claude/dependencies.yml` (dependency graph)
- `.claude/decisions.md` (architecture decisions)
- `missions/*/mission.md` (mission definitions)

**Interaction Pattern**:
- User interacts ONLY with Lead Agent
- Lead Agent spawns Task Agents with full context
- Task Agents report back to Lead Agent
- Lead Agent merges work and updates user

**Knowledge Base**:
- Programming language design (Rust, Swift, Kotlin, TypeScript patterns)
- Compiler architecture (parser, IR, codegen, optimization)
- Type theory (generics, traits, inference)
- Standard library design (collections, error handling, async)
- Project management (critical path, blocking dependencies)

---

## TA1: Language Engineer #1 (Standard Library & Syntax)

**Mission**: Design and implement AssertLang's standard library and core language features

**Branch**: `feature/pw-standard-librarian`

**Status**: ✅ **COMPLETED** (Session 51 - 134/134 tests passing)

**Expertise**:
- Type system design (generics, enums, traits)
- Standard library API design (Rust patterns)
- Pattern matching implementation
- Language syntax design (ergonomic APIs)
- World-class documentation (docstrings, examples)

**Responsibilities**:
- Design stdlib modules (Option<T>, Result<T,E>, List<T>, Map<K,V>, Set<T>)
- Implement pattern matching syntax and codegen
- Create comprehensive test suites (parsing + codegen)
- Write production-quality documentation
- Ensure stdlib matches industry standards (Rust std)

**Deliverables**:
- `stdlib/core.pw` (Option, Result)
- `stdlib/types.pw` (List, Map, Set)
- `stdlib/async.pw` (Future, Stream, async/await)
- `tests/test_stdlib_*.py` (comprehensive test coverage)
- `docs/stdlib/` (API documentation)

**Testing Requirements**:
- 100% test coverage for all stdlib functions
- Parsing tests (validate IR generation)
- Codegen tests (validate executable output for Python/Rust/Go)
- Usage pattern tests (real-world examples)
- Edge case tests (empty collections, None handling)

**Dependencies**:
- **Requires**: TA7 (parser support for generics)
- **Enables**: TA2 (executable stdlib), TA3 (LSP completion), TA4 (package distribution)

**Coordination**:
- Reports parser blockers to Lead Agent
- Coordinates with TA5 for multi-language codegen
- Provides stdlib specs to TA3 for LSP integration

**Files Owned**:
- `.claude/Task Agent 1/context.json`
- `.claude/Task Agent 1/release-checklist.md`
- `.claude/Task Agent 1/tests.yml`
- All `stdlib/*.pw` files
- All `tests/test_stdlib_*.py` files

**Success Criteria**:
- ✅ 100% test coverage (134/134 tests passing)
- ✅ Pattern matching working in Python codegen
- ✅ Stdlib parses and generates valid Python
- ⏳ Rust/Go codegen (future work)
- ⏳ Async/await syntax (future work)

---

## TA2: Language Engineer #2 (Runtime & Execution Model)

**Mission**: Build AssertLang's execution runtime and CLI tooling

**Branch**: `feature/pw-runtime-core`

**Status**: 🔴 **NOT STARTED** (unblocked by TA1 completion)

**Expertise**:
- Virtual machine architecture (bytecode, stack, heap)
- Capability-based security (sandboxing, permissions)
- Async/await execution model (schedulers, futures)
- CLI design (commands, args, output formats)
- Runtime performance optimization

**Responsibilities**:
- Decide: Bytecode VM vs transpiler-only (research + benchmark)
- Implement bytecode VM with capability sandbox (if VM chosen)
- Create async scheduler for Future/Stream execution
- Build `pw` CLI tool (build, run, test, fmt, lint)
- Integrate executable stdlib from TA1

**Deliverables**:
- `dsl/pw_runtime.py` (VM implementation)
- `dsl/bytecode.py` (instruction set)
- `dsl/capability_model.py` (security sandbox)
- `dsl/async_scheduler.py` (Future execution)
- `cli/pw.py` (main CLI entry point)
- `cli/commands/` (build, run, test, fmt)
- Benchmarks (vm_performance.md)

**CLI Commands**:
```bash
pw build input.al -o output.py --lang python
pw run program.al --watch --debug
pw test tests/ --coverage --parallel
pw fmt src/ --check
pw lint src/ --fix
```

**Testing Requirements**:
- VM instruction tests (100% coverage)
- Capability model tests (permission violations)
- Async scheduler tests (concurrency, cancellation)
- CLI integration tests (end-to-end workflows)
- Performance benchmarks (vs native Python/Rust)

**Dependencies**:
- **Requires**: TA1 (executable stdlib)
- **Enables**: TA3 (CLI integration), TA4 (benchmarking), TA6 (fuzzing target)

**Coordination**:
- Provides VM specs to TA6 for fuzzing
- Coordinates with TA3 for CLI UX
- Reports performance data to TA4 for benchmarks

**Files Owned**:
- `.claude/Task Agent 2/context.json`
- `dsl/pw_runtime.py`
- `dsl/bytecode.py`
- `dsl/capability_model.py`
- `cli/pw.py`
- `cli/commands/*.py`

**Success Criteria**:
- VM decision documented (bytecode vs transpiler)
- If VM: Instruction set complete with tests
- Capability model enforces permissions
- Async scheduler runs stdlib Future<T>
- CLI commands all working (build, run, test)

**Research Topics**:
- Lua VM architecture (simple, embeddable)
- Python bytecode format (dis module analysis)
- Rust async runtime (Tokio scheduler design)
- Capability-based security (Joe-E, Emily)

---

## TA3: DevTools Engineer (Developer Experience & Tooling)

**Mission**: Build world-class developer tooling and IDE integration

**Branch**: `feature/pw-tooling-devex`

**Status**: 🔴 **NOT STARTED**

**Expertise**:
- Language Server Protocol (LSP) implementation
- IDE extension development (VS Code, vim, Emacs)
- Code formatting (AST-based pretty printing)
- Static analysis (linting, error messages)
- Developer UX (error messages, diagnostics)

**Responsibilities**:
- Implement LSP server for AssertLang (completion, hover, goto-def)
- Create VS Code extension (syntax highlighting, debugging)
- Build formatter (`pw fmt`) with configurable style
- Build linter (`pw lint`) with fix suggestions
- Design test runner (`pw test`) with coverage reports

**Deliverables**:
- `tooling/lsp_server.py` (LSP implementation)
- `tooling/vscode-promptware/` (VS Code extension)
- `tooling/formatter.py` (AST-based formatter)
- `tooling/linter.py` (static analysis rules)
- `tooling/test_runner.py` (test discovery + execution)
- Documentation (`docs/tooling/`)

**LSP Features**:
- **Completion**: Stdlib functions, imported modules, local variables
- **Hover**: Function signatures, docstrings, type info
- **Goto Definition**: Jump to function/class/import source
- **Diagnostics**: Parse errors, type errors, lint warnings
- **Formatting**: On-save formatting
- **Rename**: Refactor variable/function names

**Testing Requirements**:
- LSP protocol conformance tests
- VS Code extension integration tests
- Formatter idempotency tests (format twice = same result)
- Linter rule tests (detect + fix suggestions)
- Test runner integration tests (JUnit XML output)

**Dependencies**:
- **Requires**: TA1 (stdlib for completion), TA2 (runtime for execution)
- **Enables**: Developer adoption (world-class UX = more users)

**Coordination**:
- Gets stdlib specs from TA1 for completion
- Integrates with TA2 CLI for `pw fmt/lint/test`
- Provides diagnostics format to TA6 for CI/CD

**Files Owned**:
- `.claude/Task Agent 3/context.json`
- `tooling/lsp_server.py`
- `tooling/vscode-promptware/`
- `tooling/formatter.py`
- `tooling/linter.py`

**Success Criteria**:
- LSP server passes conformance tests
- VS Code extension published to marketplace
- Formatter handles all PW syntax correctly
- Linter detects common errors + suggests fixes
- Test runner integrates with CI systems

**Research Topics**:
- rust-analyzer (best-in-class LSP implementation)
- TypeScript LSP (mature, feature-rich)
- Black formatter (opinionated Python formatter)
- ESLint architecture (pluggable rules)

---

## TA4: Test/QA Engineer (Quality, Ecosystem, Governance)

**Mission**: Ensure quality, build package ecosystem, establish governance

**Branch**: `feature/pw-ecosystem-launch`

**Status**: 🔴 **NOT STARTED**

**Expertise**:
- Software testing (unit, integration, fuzzing, property-based)
- Benchmarking (performance measurement, regression detection)
- Package management (registry, versioning, publishing)
- Governance (RFC process, community management)
- Quality metrics (coverage, complexity, maintainability)

**Responsibilities**:
- Create comprehensive test framework
- Build benchmarking suite (vs Python/JS/Go)
- Design package manager (`pwpm` - AssertLang Package Manager)
- Establish RFC process for language changes
- Set up quality gates (coverage, lint, tests all pass)

**Deliverables**:
- `testing/test_framework.py` (unittest integration)
- `testing/benchmarks/` (performance suite)
- `pwpm/registry.py` (package registry)
- `pwpm/cli.py` (package installation)
- `governance/rfc_template.md` (RFC process)
- Quality dashboard (test coverage, benchmarks)

**Package Manager Commands**:
```bash
pwpm init                    # Create pw.toml
pwpm install promptware/http # Install package
pwpm publish                 # Publish to registry
pwpm search "http client"    # Search packages
pwpm update                  # Update dependencies
```

**Benchmarking Suite**:
- Fibonacci (recursion overhead)
- List operations (map, filter, fold)
- HTTP server (async performance)
- File I/O (system call overhead)
- Pattern matching (vs native Python/Rust match)

**Testing Requirements**:
- Test framework passes all stdlib tests
- Benchmarks run on every PR (regression detection)
- Package manager installs from registry
- RFC process documented and enforced
- Quality dashboard auto-updates

**Dependencies**:
- **Requires**: TA1 (stdlib to test), TA2 (runtime to execute), TA3 (test runner)
- **Enables**: Ecosystem growth (packages), Community governance (RFCs)

**Coordination**:
- Gets runtime specs from TA2 for benchmarks
- Provides test framework to TA6 for CI integration
- Coordinates with Lead Agent on RFCs

**Files Owned**:
- `.claude/Task Agent 4/context.json`
- `testing/test_framework.py`
- `testing/benchmarks/`
- `pwpm/*.py`
- `governance/rfc_template.md`

**Success Criteria**:
- Test framework runs all 302+ tests
- Benchmarks show performance parity with native languages
- Package registry operational (install/publish)
- RFC #1 documented and merged
- Quality dashboard shows 100% coverage

**Research Topics**:
- Cargo (Rust package manager - gold standard)
- npm (JavaScript registry - scale lessons)
- Criterion (Rust benchmarking library)
- Python RFC process (PEPs)

---

## TA5: Codegen Specialist (Cross-Language Code Generation)

**Mission**: Ensure AssertLang generates correct, idiomatic code for all target languages

**Branch**: `feature/pw-interop-parity`

**Status**: 🔴 **NOT STARTED**

**Expertise**:
- Code generation (IR → Python/Rust/Go/JS)
- Language semantics (type systems, memory models)
- FFI (Foreign Function Interface) design
- Conformance testing (cross-language validation)
- Round-trip testing (PW → Lang → PW)

**Responsibilities**:
- Complete Python generator (pattern matching ✅, rest of features)
- Complete Rust generator (stdlib codegen, error handling)
- Complete Go generator (goroutines, interfaces)
- Complete JavaScript generator (Promises, closures)
- Build conformance test suite (same PW → correct output in all langs)
- Implement FFI v2 (call Python/Rust/C from PW)

**Deliverables**:
- `language/python_generator_v2.py` (✅ pattern matching complete)
- `language/rust_generator_v2.py` (needs pattern matching)
- `language/go_generator_v2.py` (needs generics support)
- `language/javascript_generator_v2.py` (needs async/await)
- `testing/conformance_suite/` (cross-language tests)
- `dsl/ffi_v2.py` (FFI bindings)

**Conformance Tests**:
```pw
# Same PW code should produce equivalent output in all languages
function fibonacci(n: int) -> int:
    if n <= 1:
        return n
    else:
        return fibonacci(n-1) + fibonacci(n-2)

assert fibonacci(10) == 55  # Must pass in Python, Rust, Go, JS
```

**Testing Requirements**:
- Pattern matching works in all 4 languages
- Stdlib codegen passes for all languages
- Conformance suite: 100% pass rate per language
- Round-trip tests: PW → Python → IR → Python (identical)
- FFI tests: Call Python stdlib from PW

**Dependencies**:
- **Requires**: TA1 (stdlib to generate), TA7 (parser features)
- **Enables**: Multi-language deployment (Python backend, Go CLI, etc.)

**Coordination**:
- Gets stdlib IR from TA1
- Coordinates with TA7 on parser features
- Provides conformance results to TA4 for benchmarks

**Files Owned**:
- `.claude/Task Agent 5/context.json`
- `language/*_generator_v2.py`
- `testing/conformance_suite/`
- `dsl/ffi_v2.py`

**Success Criteria**:
- ✅ Python generator: pattern matching complete
- ⏳ Rust generator: pattern matching + stdlib
- ⏳ Go generator: generics + goroutines
- ⏳ JS generator: Promises + closures
- ⏳ Conformance suite: 100% pass rate
- ⏳ FFI v2: call Python from PW

**Research Topics**:
- Rust match expressions (comprehensive pattern syntax)
- Go generics (constraints, type parameters)
- JavaScript async/await (Promise internals)
- Python C API (FFI implementation)

---

## TA6: Release Engineer (Safety, CI/CD, Automation)

**Mission**: Ensure security, automate releases, prevent disasters

**Branch**: `feature/pw-safety-release`

**Status**: 🔴 **NOT STARTED**

**Expertise**:
- Security auditing (capability violations, injection attacks)
- Fuzzing (AFL, libFuzzer, property-based testing)
- CI/CD pipelines (GitHub Actions, release automation)
- Release management (versioning, changelogs, rollback)
- Disaster prevention (pre-commit hooks, smoke tests)

**Responsibilities**:
- Audit capability model (TA2) for security violations
- Build fuzzing harness for parser + VM
- Create GitHub Actions CI pipeline
- Automate release process (version → tag → publish)
- Set up smoke tests (catch regressions before production)

**Deliverables**:
- `security/capability_audit.py` (automated security checks)
- `security/fuzzing/` (fuzzing harnesses)
- `.github/workflows/ci.yml` (full CI pipeline)
- `scripts/release.sh` (automated release)
- `security/smoke_tests.py` (regression detection)

**CI Pipeline Stages**:
1. **Lint**: Run `pw lint` on all code
2. **Test**: Run 302+ tests (stdlib + parser + codegen)
3. **Benchmark**: Detect performance regressions
4. **Security**: Run capability audits + fuzzing
5. **Build**: Generate Python/Rust/Go output
6. **Smoke Test**: Run example programs
7. **Publish**: If main branch, publish to PyPI

**Fuzzing Targets**:
- Parser (random PW code → should not crash)
- VM (random bytecode → should not crash)
- Capability model (random syscalls → should deny unsafe ops)
- Codegen (random IR → should generate valid code)

**Testing Requirements**:
- Fuzzing runs 1M+ iterations per target
- CI pipeline passes on every PR
- Release automation tested on staging branch
- Smoke tests catch known regressions

**Dependencies**:
- **Requires**: TA2 (VM to fuzz), TA3 (lint/test tools), TA4 (test framework)
- **Enables**: Safe production releases, Disaster prevention

**Coordination**:
- Gets VM specs from TA2 for fuzzing
- Gets test framework from TA4 for CI
- Coordinates with Lead Agent on releases

**Files Owned**:
- `.claude/Task Agent 6/context.json`
- `security/capability_audit.py`
- `security/fuzzing/`
- `.github/workflows/ci.yml`
- `scripts/release.sh`

**Success Criteria**:
- Capability audit finds no violations
- Fuzzing runs 10M iterations without crash
- CI pipeline catches regressions (proof: intentional break)
- Release automation publishes to PyPI
- Smoke tests detect regressions within 5 seconds

**Research Topics**:
- AFL fuzzing (American Fuzzy Lop)
- Hypothesis (property-based testing for Python)
- GitHub Actions best practices
- Semantic versioning (SemVer)

---

## TA7: MCP Specialist (Operations Discovery & Integration)

**Mission**: Build MCP (Model Context Protocol) server for multi-language operations

**Branch**: `feature/pw-mcp-*`

**Status**: 🟢 **OPERATIONAL** (Session 50 - Python/JS tested)

**Expertise**:
- Model Context Protocol (MCP) design
- Operation discovery (automatic function binding)
- Multi-language integration (Python/Go/Rust/JS interop)
- API design (RESTful, JSON-RPC, GraphQL patterns)
- Service orchestration (microservices, distributed systems)

**Responsibilities**:
- Maintain MCP server (23 operations for 3 languages)
- Add new operation types (database, HTTP, file I/O)
- Integrate stdlib operations (Option, Result, List ops)
- Build operation registry (discover available ops per language)
- Create MCP client libraries (Python, Go, JS)

**Deliverables**:
- `mcp/server.py` (MCP server implementation)
- `mcp/operations/` (operation definitions)
- `mcp/stdlib_ops.py` (stdlib operations)
- `mcp/clients/` (client libraries)
- `docs/mcp/` (protocol documentation)

**MCP Operations**:
```python
# Python operations
operation("list.map", inputs=["list", "function"], output="list")
operation("option.unwrap_or", inputs=["option", "default"], output="T")
operation("result.is_ok", inputs=["result"], output="bool")

# Cross-language operations
operation("http.get", inputs=["url"], output="Result<string, Error>")
operation("file.read", inputs=["path"], output="Result<string, IOError>")
```

**Testing Requirements**:
- MCP protocol conformance tests
- Operation execution tests (all 23 ops)
- Stdlib integration tests (Option, Result, List)
- Client library tests (Python, Go, JS)
- Cross-language round-trip tests

**Dependencies**:
- **Requires**: TA1 (stdlib operations), TA5 (multi-language codegen)
- **Enables**: Multi-language stdlib, Operation marketplace

**Coordination**:
- Gets stdlib specs from TA1 for operation binding
- Coordinates with TA5 for cross-language execution
- Provides operation registry to TA4 for ecosystem

**Files Owned**:
- `.claude/Task Agent 7/context.json` (reused, was parser agent)
- `mcp/server.py`
- `mcp/operations/`
- `mcp/stdlib_ops.py`
- `mcp/clients/`

**Success Criteria**:
- ✅ MCP server operational (23 ops)
- ✅ Python execution tested
- ✅ JavaScript execution tested
- ⏳ Go execution (needs implementation)
- ⏳ Stdlib operations integrated
- ⏳ Client libraries published

**Research Topics**:
- JSON-RPC 2.0 (MCP uses this protocol)
- OpenAPI/Swagger (API documentation)
- gRPC (alternative protocol)
- Microservices patterns (service mesh, discovery)

---

## Agent Coordination Matrix

| Agent | Spawns | Blocks | Blocked By | Reports To | Coordinates With |
|-------|--------|--------|------------|------------|------------------|
| **Lead** | All TAs | None | None | User | All TAs |
| **TA1** | None | TA2, TA3, TA4 | TA7 (parser) | Lead | TA5 (codegen), TA7 (parser) |
| **TA2** | None | TA3, TA4, TA6 | TA1 (stdlib) | Lead | TA3 (CLI), TA6 (fuzzing) |
| **TA3** | None | None | TA1, TA2 | Lead | TA2 (CLI), TA4 (test runner) |
| **TA4** | None | None | TA1, TA2, TA3 | Lead | TA3 (test runner), TA6 (CI) |
| **TA5** | None | Deployment | TA1 (stdlib) | Lead | TA1 (IR), TA7 (MCP ops) |
| **TA6** | None | Production | TA2 (VM), TA4 (tests) | Lead | TA2 (fuzzing), TA4 (CI) |
| **TA7** | None | TA1, TA5 | None | Lead | TA1 (features), TA5 (codegen) |

**Critical Path**: TA7 (parser) → TA1 (stdlib) → TA2 (runtime) → TA5 (codegen) → Production

**Parallel Tracks**:
- TA3 (tooling) can proceed independently
- TA4 (ecosystem) needs TA2 runtime for benchmarks
- TA6 (safety) needs TA2 VM for fuzzing
- TA7 (MCP) can integrate stdlib ops after TA1

---

## Agent Spawn Protocol

### Lead Agent Spawning a Task Agent

```python
Task(
    description=f"TA{N}: {mission_name}",
    subagent_type="general-purpose",
    prompt=f"""
    You are TA{N}: {role_name} - {professional_role}

    MISSION: {mission_summary}
    BRANCH: feature/{branch_name}
    EXIT CRITERIA: {completion_criteria}

    SETUP (Read First):
    1. Read .claude/SUB_AGENT_TEMPLATE.md (protocol)
    2. Read .claude/Task Agent {N}/context.json (current status)
    3. Read .claude/Task Agent {N}/dependencies.yml (what you can use)
    4. Read .claude/Task Agent {N}/decisions.md (follow these)
    5. Read missions/TA{N}/mission.md (overall objective)

    YOUR EXPERTISE:
    {expertise_list}

    YOUR DELIVERABLES:
    {deliverables_list}

    YOUR TESTING REQUIREMENTS:
    {testing_requirements}

    YOUR DEPENDENCIES:
    - REQUIRES: {blocking_agents}
    - ENABLES: {unblocked_agents}

    COORDINATION:
    {coordination_instructions}

    FILES YOU OWN:
    {file_ownership_list}

    DO NOT TOUCH:
    - dependencies.yml (lead agent territory)
    - CLAUDE.md (lead agent territory)
    - Other TA files (stay in your lane)

    REPORT BACK WITH:
    - Completion summary
    - Test results (all tests must pass)
    - Files changed
    - Blockers removed
    - Next recommended actions

    START BY:
    {first_action}
    """
)
```

### Task Agent Self-Documentation

Each agent updates its own files:
- `.claude/Task Agent {N}/context.json` (progress, status, metrics)
- `.claude/Task Agent {N}/progress.md` (narrative updates)
- Test files (comprehensive coverage)
- Code files (deliverables)

Lead agent updates coordination files:
- `CLAUDE.md` (roster, assignments)
- `Current_Work.md` (project status)
- `.claude/dependencies.yml` (dependency graph)

---

## Research Before Implementation

**Before spawning agents for major features**, Lead Agent conducts research:

### Research Process
1. **Identify knowledge gap**: What don't we know?
2. **Research industry leaders**: How do Rust/Swift/Kotlin/TypeScript handle this?
3. **Extract best practices**: What patterns are proven?
4. **Document findings**: `.claude/research/{topic}.md`
5. **Create detailed plan**: Specific APIs, file structure, test strategy
6. **Spawn agent with research**: Give concrete specifications, not vague requirements

### Research Topics Already Completed
- ✅ Option<T> / Result<T,E> design (Rust std patterns)
- ✅ Pattern matching syntax (Rust match expressions)
- ✅ Generic type parameters (Swift/Kotlin generics)
- ✅ MCP protocol (JSON-RPC 2.0, operation discovery)

### Research Topics Pending
- ⏳ VM architecture (Lua VM, Python bytecode)
- ⏳ Capability-based security (Joe-E, Emily)
- ⏳ Async/await execution (Tokio scheduler, JS event loop)
- ⏳ LSP implementation (rust-analyzer, TypeScript LSP)
- ⏳ Package registry (Cargo, npm scale lessons)

---

## Quality Gates

**All agents must pass before merge**:

1. **Tests**: 100% of tests pass (no skips, no failures)
2. **Documentation**: All public APIs documented (docstrings + examples)
3. **Benchmarks**: No performance regressions (if applicable)
4. **Security**: Capability audit passes (if applicable)
5. **Code Review**: Lead agent approves changes

**CI Pipeline** (TA6 responsibility):
```yaml
on: [push, pull_request]
jobs:
  test:
    - Run pytest (302+ tests)
    - Run conformance suite (4 languages)
    - Run benchmarks (vs baseline)
    - Run security audit
    - Run smoke tests
```

---

## Scaling the Team

**Adding new agents** (TA8, TA9, ...):

```bash
# Lead agent runs:
scripts/create_ta.sh 8 "WebAssembly Specialist" "feature/pw-wasm"
```

**New agent types**:
- TA8: WebAssembly Specialist (compile PW → WASM)
- TA9: Documentation Specialist (user guides, tutorials)
- TA10: Performance Engineer (profiling, optimization)
- TA11: Mobile Specialist (iOS/Android targets)

---

## Success Metrics

| Metric | Target | Current | Agent Responsible |
|--------|--------|---------|-------------------|
| Test Coverage | 100% | 100% (302/302) | TA4 |
| Stdlib Tests | 100% | 100% (134/134) | TA1 |
| Python Codegen | 100% | 100% | TA5 |
| Rust Codegen | 100% | 10% | TA5 |
| Go Codegen | 100% | 5% | TA5 |
| JS Codegen | 100% | 15% | TA5 |
| LSP Features | 6/6 | 0/6 | TA3 |
| Package Registry | Operational | Not started | TA4 |
| CI/CD | Automated | Manual | TA6 |
| Security Audit | Passing | Not started | TA6 |
| Fuzzing | 10M iterations | Not started | TA6 |
| MCP Operations | 50+ | 23 | TA7 |

---

## Deployment Strategy

### Phase 1: Core Language (TA1, TA7) ✅ COMPLETE
- ✅ Standard library (Option, Result, List, Map, Set)
- ✅ Generic type parameters
- ✅ Pattern matching
- ✅ Python codegen

### Phase 2: Execution (TA2, TA5)
- ⏳ Runtime VM or transpiler decision
- ⏳ Async/await execution model
- ⏳ CLI tool (`pw build/run/test`)
- ⏳ Multi-language codegen (Rust, Go, JS)

### Phase 3: Developer Experience (TA3)
- ⏳ LSP server
- ⏳ VS Code extension
- ⏳ Formatter + Linter
- ⏳ Test runner

### Phase 4: Ecosystem (TA4, TA7)
- ⏳ Package manager (pwpm)
- ⏳ Benchmarking suite
- ⏳ MCP operation marketplace
- ⏳ RFC process

### Phase 5: Production (TA6)
- ⏳ CI/CD automation
- ⏳ Security auditing + fuzzing
- ⏳ Release automation
- ⏳ Monitoring + alerting

---

## Communication Protocol

### User → Lead Agent
- User describes what they want (features, fixes, releases)
- Lead Agent coordinates team to deliver

### Lead Agent → Task Agents
- Spawns with full context (mission, expertise, dependencies)
- Monitors progress via context.json
- Integrates completed work

### Task Agents → Lead Agent
- Report completion summary (tests, files, blockers removed)
- Update context.json (progress, metrics)
- Request help if blocked

### Task Agents ↔ Task Agents
- **No direct communication** (all through Lead Agent)
- Coordination via shared files (dependencies.yml, decisions.md)

---

## Conclusion

This architecture provides a professional development team structure automated through Claude Code agents. Each agent is a specialist with clear expertise, responsibilities, and coordination dependencies.

**Key Principles**:
1. **Specialization**: Each agent has deep expertise in one domain
2. **Autonomy**: Agents work in isolated branches with clear missions
3. **Coordination**: Lead Agent orchestrates all work through dependency management
4. **Quality**: All work must pass tests + docs + benchmarks before merge
5. **Research-Driven**: Lead Agent researches best practices before major features
6. **User-Focused**: User interacts only with Lead Agent (simple interface)

**Current Status**:
- Phase 1 COMPLETE (TA1 stdlib, TA7 parser)
- Phase 2-5 ready to start (no blockers)
- MCP architecture operational (TA7)

**Next Actions**:
1. Lead Agent: Spawn TA2 (Runtime) now that TA1 is complete
2. TA2: Research VM architecture, implement runtime
3. Lead Agent: Spawn TA5 (Codegen) for Rust/Go/JS generators
4. Lead Agent: Spawn TA3 (DevTools) for LSP server
5. User: Provide feedback on this architecture

This system enables professional-quality software development through automated agent coordination, matching the structure of a 7-person development team.
