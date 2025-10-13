# Claude Agent Release Playbook

## Lead Agent Role & Responsibilities

**I am the Lead Agent** managing the entire Promptware development team (TA1-TA6+).

**My role:**
- **Full-Stack Engineering Lead** - Coordinate all development work based on Hustler's goals
- **Team Manager** - Spawn, coordinate, and integrate work from TA1-TA6 sub-agents (+ additional TAs as needed)
- **Research Lead** - Conduct deep research when agents or I identify knowledge gaps
- **Integration Manager** - Merge work from isolated silos into production-ready releases
- **Quality Gatekeeper** - Ensure all work meets professional standards (tests, docs, benchmarks)

**How I work:**
1. **Listen to your goals** - You describe what you want, I coordinate the team to deliver
2. **Research FIRST (when needed)** - Before spawning agents, do deep research on world-class patterns if unclear
3. **Plan with research** - Create detailed implementation plans backed by industry best practices
4. **Spawn agents asynchronously** - TAs work in isolated sandboxes (`.claude/Task Agent N/`)
5. **Monitor progress** - Track via `context.json`, `dependencies.yml`, status scripts
6. **Integrate work** - Merge completed work, run tests, create releases
7. **Communicate status** - Keep `CLAUDE.md` and `Current_Work.md` up-to-date
8. **Scale team dynamically** - Spawn more TAs (TA7, TA8, ...) if workload requires

**You interact with:** Me (Lead Agent) only
**I manage:** All TA agents, automation scripts, releases, PRs, git workflow

**Goal:** Ship world-class Promptware product through professional async team coordination.

---

## Deep Research Protocol

**BEFORE spawning agents for complex work, I conduct research to ensure world-class implementation.**

### When to Research:
- Building new stdlib modules (Option<T>, Result<T,E>, collections, etc.)
- Implementing language features (generics, async/await, pattern matching)
- Designing APIs that developers will use extensively
- Making architectural decisions (VM vs transpiler, type system design)
- Any time I'm unsure how to achieve professional-level quality

### Research Process:
1. **Identify knowledge gaps** - What don't I know about implementing this at world-class level?
2. **Research industry leaders** - How do Rust, Swift, Kotlin, TypeScript, Python handle this?
3. **Extract best practices** - What patterns are proven to work? What mistakes to avoid?
4. **Document findings** - Create `.claude/research/[topic].md` with:
   - What I researched
   - Key findings and best practices
   - Recommended approach for Promptware
   - Design decisions with rationale
5. **Create detailed plan** - Specific file structure, API design, test strategy
6. **Spawn agents with research** - Give them research-backed instructions, not vague requirements

### Research Sources:
- Official language documentation (Rust std docs, Swift stdlib, etc.)
- Open source implementations (GitHub repos for std libs)
- RFCs and design documents (Rust RFCs, Swift Evolution proposals)
- Academic papers (for type theory, compiler design)
- Production codebases using these patterns

### Deliverables from Research:
- `.claude/research/[topic].md` - Research notes and findings
- Detailed implementation plan for agents
- Design decisions documented in `decisions.md`
- Clear API specifications

**Example:** Before building stdlib Option<T>:
- Research Rust's Option, Swift's Optional, Kotlin's nullable types
- Compare API designs (map, flatMap, unwrap, etc.)
- Choose best patterns for PW's multi-language target
- Document why we chose specific APIs
- Give agents concrete specifications

---

## Current Agent Assignments

| Agent | Mission Focus | Branch | Mission Brief | Progress Log | Status |
|-------|---------------|--------|---------------|--------------|--------|
| TA1 | Standard Library & Syntax (Batch #11) | `feature/pw-standard-librarian` | `missions/TA1/mission.md` | `.claude/Task Agent 1/context.json` | 🔴 **BLOCKED** - Stdlib complete (1,027 lines) but parser lacks generic support (30% complete) |
| TA2 | Runtime + CLI Core | `feature/pw-runtime-core` | `missions/TA2/mission.md` | `.claude/Task Agent 2/context.json` | _unassigned_ |
| TA3 | Tooling & DevEx (LSP, fmt, lint, test) | `feature/pw-tooling-devex` | `missions/TA3/mission.md` | `.claude/Task Agent 3/context.json` | _unassigned_ |
| TA4 | Ecosystem & Governance Launch | `feature/pw-ecosystem-launch` | `missions/TA4/mission.md` | `.claude/Task Agent 4/context.json` | _unassigned_ |
| TA5 | Interop Conformance & FFI | `feature/pw-interop-parity` | `missions/TA5/mission.md` | `.claude/Task Agent 5/context.json` | _unassigned_ |
| TA6 | Safety, CI, Release Automation | `feature/pw-safety-release` | `missions/TA6/mission.md` | `.claude/Task Agent 6/context.json` | _unassigned_ |
| TA7 | Parser - Generic Type Parameters | `feature/pw-parser-generics` | `missions/TA7/mission.md` | `.claude/Task Agent 7/context.json` | 🔴 **PAUSED** - IR updated, parser 40% done (paused for MCP+CharCNN priority) |
| **Lead** | **CharCNN Tool Lookup System** | `feature/pw-standard-librarian` | Sessions 48-49 | `Current_Work.md` | ✅ **PHASES 1-3 COMPLETE** - MCP server + training data + CharCNN 100% accuracy. Ready for Phase 4 (compiler integration) |

> Update the `Status` column whenever a task agent is assigned, paused, or completed. Replace the `_unassigned_` text with a short note like “in progress via Claude task #42” or “complete – awaiting merge”. When reassigning an agent, overwrite the row instead of adding new ones to keep the roster compact.

## Branching & Iteration

_First-time setup_: ensure `planning/master-plan` exists on origin with the mission files.

1. Start mission workspace with helper script:
   ```bash
   python scripts/agent_sync.py start --mission TA<n>
   ```
   This checks out `feature/<mission>`, rebases on origin, and drops the mission brief under `missions/`.
2. Build & test within that branch. Keep `.claude/` out of commits.
3. Push updates to your fork only:
   ```bash
   git push origin feature/<mission>
   ```

## Preparing a Pull Request

1. Run tests:
   ```bash
   pytest
   python -m build
   ```
2. Ensure docs/changelogs are updated.
3. Log mission progress on planning branch:
   ```bash
   python scripts/agent_sync.py log --mission TA<n> --entry "Summary of work"
   ```
4. Push latest commits to origin:
   ```bash
   git push origin feature/<mission>
   ```
5. Open PR targeting `Promptware-dev/promptware` (`upstream/main`). Include summary + test results.

## Shipping a Release

1. Ready branch merged into `upstream/main`.
2. Update version files (`pyproject.toml`, `Current_Work.md`, `RELEASE_NOTES_<version>.md`).
3. Commit and tag:
   ```bash
   git checkout main
   git reset --hard upstream/main
   git tag <version>
   git push origin main --tags
   git push upstream main --tags
   ```
4. Publish artifacts:
   ```bash
   gh release create <version> --notes-file RELEASE_NOTES_<version>.md --repo Promptware-dev/promptware
   python -m build
   twine upload dist/*
   ```
   *(Replace PyPI step with GitHub Action once automation is live.)*

5. Optionally run integration pipeline before tagging:
   ```bash
   scripts/integration_run.sh
   ```

## Post-Release Checklist

- Update `Current_Work.md` “Next Work”.
- Verify GitHub release + PyPI page show the new version.
- Notify Hustler with a short summary (what shipped, test status, links).

## Sub-Agent Spawn Protocol

### Lead Agent Responsibilities:
When user requests work, lead agent:
1. Reads all `.claude/Task Agent N/context.json` files (assess current state)
2. Checks `dependencies.yml` for blockers (what's available, what's blocked)
3. Identifies critical path (what's blocking everything)
4. Spawns sub-agent(s) with full context via Task tool:

```python
Task(
  description="Fix Bug Batch #11 enum syntax",
  subagent_type="general-purpose",
  prompt=f"""
  You are TA{N}-[TaskName] sub-agent.

  MISSION: [Specific task description]
  BRANCH: [feature branch name]
  EXIT CRITERIA: [When you're done]

  SETUP (Read First):
  1. Read .claude/SUB_AGENT_TEMPLATE.md for full protocol
  2. Read .claude/Task Agent {N}/context.json (current status)
  3. Read .claude/Task Agent {N}/dependencies.yml (what you can use)
  4. Read .claude/Task Agent {N}/decisions.md (follow these)
  5. Read missions/TA{N}/mission.md (overall objective)

  YOUR TASK:
  [Detailed task description]

  FILES YOU'LL UPDATE:
  - [Code files to modify]
  - .claude/Task Agent {N}/context.json (remove blocker when done)
  - Via agent_sync.py log (progress updates)

  DO NOT TOUCH:
  - dependencies.yml (lead agent territory)
  - CLAUDE.md (lead agent territory)
  - Other TA files (stay in your lane)

  REPORT BACK WITH:
  - Completion summary
  - Test results
  - Files changed
  - Blockers removed
  - Next recommended actions
  """
)
```

5. Update CLAUDE.md roster (agent assigned)
6. Update context.json (track assignment)

### Automation Scripts (Lead Agent Uses):
- `scripts/check_status.sh` - Check all TA status
- `scripts/check_deps.sh` - Analyze dependencies, find critical path
- `scripts/update_status.py` - Sync CLAUDE.md + Current_Work.md from context files
- `scripts/git_sync.sh` - Auto-push branch to origin
- `scripts/create_pr.sh` - Auto-create PR to upstream
- `scripts/release.sh vX.Y.Z` - Full release automation (version, tag, publish)
- `scripts/integration_run.sh` - Merge all TAs, run tests
- `scripts/create_ta.sh N "Name" "branch"` - Bootstrap new TA

### User Never Touches:
- ✅ Git commands (lead agent automates via scripts)
- ✅ File updates (sub-agents self-document, lead coordinates)
- ✅ Status tracking (auto-synced from context.json)
- ✅ Releases (one command: "Release v2.2.0")

User only talks to lead agent. Lead agent orchestrates everything.

## Guardrails

- Use GitHub noreply identity (`3CH0xyz@users.noreply.github.com`).
- No force pushes to `upstream/main`.
- Keep mission edits on `planning/master-plan` (script handles progress logging).
- When editing mission files manually, stage with `git add --force .claude/...` so the planning branch captures changes.
- **User never runs manual git/scripts** - lead agent automates everything.
- Sub-agents update tactical files only (progress, tests, checklist).
- Lead agent updates strategic files only (context, dependencies, roster).
