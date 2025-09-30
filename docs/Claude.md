# Claude Code Agent Guide

This document provides guidance for Claude Code (and other AI agents) working on the Promptware codebase.

---

## Getting Started

When you first engage with Promptware:

1. **Read execution-plan.md** — Understand the current Wave, completed milestones, and active tasks.
2. **Check test status** — Run `python3 -m pytest tests/ -q` to validate the environment.
3. **Review recent commits** — `git log --oneline -10` shows recent work and active development areas.
4. **Identify your focus**:
   - DSL/language work → `language/`, `docs/promptware-dsl-*.md`
   - Tool adapters → `tools/`, `docs/toolgen-*.md`, `tests/tools/`
   - Runner protocol → `runners/`, `docs/development-guide.md`
   - SDK design → `docs/sdk/`

---

## Core Principles for AI Agents

### 1. Context Before Action

- Always read relevant files before editing.
- Understand the existing architecture before proposing changes.
- Check test coverage for the area you're modifying.

### 2. Test-Driven Development

- Run tests before making changes to establish baseline.
- Run tests after changes to verify correctness.
- Add new tests when introducing new functionality.
- Language-specific smoke tests:
  ```bash
  python3 -m pytest tests/tools/test_node_adapters.py
  python3 -m pytest tests/tools/test_go_adapters.py
  python3 -m pytest tests/tools/test_rust_adapters.py
  python3 -m pytest tests/tools/test_dotnet_adapters.py
  ```

### 3. Documentation Hygiene

- Update docs when changing APIs, protocols, or DSL syntax.
- Keep `execution-plan.md` task tracker current.
- Document trade-offs and design decisions in commit messages.

### 4. Incremental Progress

- Make focused, atomic changes.
- Complete one task fully before moving to the next.
- Don't leave code in a broken state between commits.

---

## Communication Protocol

### With Human Developers

- **Ask before breaking changes** — DSL syntax changes, runner protocol modifications, or public SDK APIs require approval.
- **Explain architectural decisions** — When you choose one approach over another, document why.
- **Report blockers immediately** — Missing specs, unclear requirements, or contradictory constraints should surface early.
- **Summarize completed work** — Provide clear status updates showing what was done, what passed/failed, and what's next.

### With Other AI Agents

- **Declare your scope** — State what you're working on to avoid conflicts (e.g., "Working on Rust adapter fixtures for tools 10-15").
- **Share test results** — Always report pass/fail status and error details.
- **Update shared state** — Mark completed tasks in `execution-plan.md` task tracker.
- **Document assumptions** — If you're inferring behavior from code, state that explicitly.

---

## Development Workflow

### Before You Code

1. Locate the relevant files:
   ```bash
   # Find files by pattern
   find . -name "*adapter*" -type f

   # Search for specific content
   grep -r "runner protocol" docs/
   ```

2. Read the current implementation:
   - Use full file reads, not partial snippets.
   - Check for related test files.
   - Look for existing documentation.

3. Understand dependencies:
   - What other components depend on what you're changing?
   - Are there cascading effects?

### During Development

1. **Make minimal, focused edits**:
   - Change only what's necessary.
   - Preserve existing style and conventions.
   - Don't refactor unrelated code.

2. **Validate incrementally**:
   - Test after each logical change.
   - Don't accumulate multiple untested changes.

3. **Handle errors gracefully**:
   - If a test fails, understand why before proceeding.
   - Don't suppress errors; fix root causes.

### After Coding

1. **Run the full test suite**:
   ```bash
   python3 -m pytest tests/ -v
   ```

2. **Update documentation**:
   - Modified runner protocol? → Update `docs/development-guide.md`
   - Added DSL syntax? → Update `docs/promptware-dsl-spec.md`
   - New toolgen template? → Document in `docs/toolgen-*-adapter-template.md`

3. **Update task tracker**:
   - Mark completed items in `execution-plan.md`
   - Add newly discovered tasks

4. **Commit with clear messages**:
   ```bash
   git add <files>
   git commit -m "Brief summary of change

   - Detailed point 1
   - Detailed point 2
   - Fixes/implements: <reference to task>"
   ```

---

## Wave 2 Specifics (Current Focus)

### Goal
Multi-language adapter parity across Node/Go/Rust/.NET.

### Key Areas

**Adapter Templates**:
- Location: `docs/toolgen-{node,go,rust,dotnet}-adapter-template.md`
- Generated adapters: `tools/<tool>/adapters/`
- Entry points must match language conventions:
  - Node: `module.exports = { handle }`
  - Go: `package main; func Handle(...) { }`
  - Rust: `pub fn handle(...) -> serde_json::Value { }`
  - .NET: `public static class Adapter { public static object Handle(...) { } }`

**Smoke Tests**:
- Location: `tests/tools/test_{node,go,rust,dotnet}_adapters.py`
- Fixtures: `tests/fixtures/{node,go,rust,dotnet}_adapters/`
- Each test validates adapter entry point can be invoked without errors

**Runner Protocol**:
- Methods: `apply`, `start`, `stop`, `health`
- Envelope format: `{"ok": bool, "version": "v1", ...}`
- Error codes: `E_BUILD`, `E_RUNTIME`, etc.
- Timeline events must align across all languages

### Open Tasks

1. **Expand test fixtures** — Current fixtures only cover `file_reader` and `json_validator`; need more tools.
2. **Runner timeline parity** — Compare Python vs Node/Go/.NET timeline event outputs; document deltas.
3. **SDK prototypes** — Design Python/Node SDK packages with MCP verb wrappers.
4. **CI integration** — Wire `scripts/run_test_batches.sh` into `make test`.

---

## Common Patterns

### Reading Files

Always read complete files before editing:
```python
# Read the file first
with open('path/to/file.py', 'r') as f:
    content = f.read()

# Then edit with full context
```

### Running Tests

Language-specific runtime requirements:
- **Node**: Requires `node` in `$PATH`
- **Go**: Requires `go` in `$PATH`
- **Rust**: Requires `cargo` in `$PATH`
- **.NET**: Requires `dotnet` in `$PATH`; set `DOTNET_BIN` for custom paths

### Generating Adapters

```bash
# Generate adapter for a specific tool and language
python3 cli/toolgen.py tools/file_reader --node
python3 cli/toolgen.py tools/json_validator --go
python3 cli/toolgen.py tools/api_auth --rust
python3 cli/toolgen.py tools/http_client --dotnet
```

### Validating Changes

```bash
# Lint/format DSL files
python3 language/formatter.py examples/hello.pw

# Run parser tests
python3 -m pytest tests/test_dsl_parser.py -v

# Run interpreter tests
python3 -m pytest tests/test_dsl_interpreter.py -v

# Run adapter smoke tests
python3 -m pytest tests/tools/ -v
```

---

## Troubleshooting

| Issue | Diagnosis | Solution |
| --- | --- | --- |
| Tests hang indefinitely | Missing runtime (node/go/cargo/dotnet) | Install runtime or skip: `pytest -k 'not adapter'` |
| Import errors in Python tests | Virtual environment not activated | Activate venv or install dependencies |
| Go module errors | Missing `go.mod` or deps | Check `tools/<tool>/adapters/` for module setup |
| .NET build failures | SDK version mismatch | Set `DOTNET_BIN` or update target framework |
| Timeline events missing fields | Runner envelope mismatch | Compare with Python reference implementation |

---

## Best Practices for Claude Code

### DO:
- ✅ Read files completely before editing
- ✅ Run tests before and after changes
- ✅ Update documentation alongside code changes
- ✅ Make focused, atomic commits
- ✅ Ask for clarification when requirements are ambiguous
- ✅ Report test failures with full context
- ✅ Update `execution-plan.md` task tracker

### DON'T:
- ❌ Make multiple unrelated changes in one commit
- ❌ Skip tests to save time
- ❌ Assume undocumented behavior
- ❌ Leave TODO comments without tracking them
- ❌ Commit commented-out code or debug prints
- ❌ Modify core protocols without discussing trade-offs
- ❌ Create duplicate documentation

---

## Exit Checklist

Before handing off or completing work:

- [ ] All tests pass (`python3 -m pytest tests/`)
- [ ] Documentation updated for any API/protocol changes
- [ ] `execution-plan.md` reflects completed tasks
- [ ] Commit messages explain *why*, not just *what*
- [ ] No build artifacts committed (check `.gitignore`)
- [ ] No debug code or commented sections left behind
- [ ] Test results shared (especially if any failed)

---

## Quick Reference

### Key Files
- **Wave status**: `docs/execution-plan.md`
- **DSL spec**: `docs/promptware-dsl-spec.md`
- **Runner protocol**: `docs/development-guide.md`
- **Adapter templates**: `docs/toolgen-*-adapter-template.md`
- **Smoke tests**: `tests/tools/test_*_adapters.py`

### Useful Commands
```bash
# Run all tests
python3 -m pytest tests/ -v

# Run specific language smoke tests
python3 -m pytest tests/tools/test_node_adapters.py -v

# Generate adapter
python3 cli/toolgen.py tools/<tool_name> --<language>

# Format DSL
python3 language/formatter.py <file.pw>

# Check git status
git status --short
```

---

Keep this file in sync with `execution-plan.md` and `agents.md` so AI agent guidance remains current.