## Mission: Deliver Tooling & Developer Experience Stack

**Assigned branch:** `feature/pw-tooling-devex` (create from `upstream/main`)  
**Primary objective:** Ship first-class editor support, formatter/linter, and testing harness so Promptware feels production-ready.

### Scope & Priorities
1. **VS Code Extension Upgrade**
   - Extend existing `.vscode/extensions/pw-language` package into full LSP client.
   - Wire to a new `tools/lsp/pw-language-server` (Python or Node) that provides:
     - Syntax diagnostics (parse/type errors)
     - Hover type info + documentation
     - Go-to-definition / find references
     - Auto-import suggestions
   - Publish beta on VS Marketplace once stable.
2. **Formatter & Linter**
   - Implement `pwfmt` (canonical formatting rules) and `pwlint` (style + best-practice checks).
   - Integrate with `pw` CLI (`pw fmt`, `pw lint`) defined by TA2.
   - Provide fix-it suggestions for common lint rules.
3. **Test Runner & Bench Harness**
   - Build `pwtest` framework: fixtures, parametrized tests, mocks, fake clock + seedable RNG.
   - Add `pw bench` command for micro/macro benchmarks with JSON output.
4. **Developer Onboarding**
   - Author "First 10 Minutes" tutorial (`docs/getting-started.md`) demonstrating:
     - `pw new app`
     - Running tests, formatting, and debugging
     - Using VS Code extension
   - Produce screencast-friendly script for marketing/demo use.
5. **Quality Gates**
   - CI pipeline for tooling (lint + unit tests) under `.github/workflows/tooling-ci.yml` (or document manual steps if automation pending).

### Exit Criteria
- VS Code extension delivers hover, go-to-def, inline errors, rename, auto-format on save.
- `pw fmt`, `pw lint`, `pw test`, and `pw bench` commands operate via `pw` CLI.
- Getting-started tutorial verified by running commands end-to-end on a clean machine.
- Tooling CI passes with reproducible snapshots (formatter tests use golden files).

### Coordination
- Consume CLI hooks from **TA2** (pw command contract) and ensure consistent UX.
- Expose LSP APIs consumed by **TA1** stdlib docs/examples for inline metadata.
- Log progress in `.claude/Task Agent 3/ta3-current-progress.md` after each major deliverable (LSP alpha, formatter beta, onboarding doc launch).
