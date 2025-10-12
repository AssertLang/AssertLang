# Multi-Agent Workflow Documentation

**Purpose:** Define how lead agent and sub-agents coordinate asynchronously across GitHub silos.

---

## 🏗️ Architecture Overview

```
┌─────────────────────────────────────────────────────────┐
│                    LEAD AGENT (You're Here)             │
│  - Reads CLAUDE.md (playbook)                          │
│  - Spawns sub-agents via Task tool                     │
│  - Manages cross-TA dependencies                       │
│  - Coordinates integration & releases                   │
│  - Updates strategic files (context, dependencies)      │
└─────────────────────────────────────────────────────────┘
                          │
            ┌─────────────┴─────────────┐
            ▼                           ▼
   ┌──────────────────┐        ┌──────────────────┐
   │   SUB-AGENT 1    │        │   SUB-AGENT 2    │
   │  (Bug Fixes)     │        │  (Stdlib Core)   │
   │                  │        │                  │
   │ - Pinned to TA1  │        │ - Pinned to TA1  │
   │ - Updates files  │        │ - Updates files  │
   │ - Reports back   │        │ - Reports back   │
   └──────────────────┘        └──────────────────┘
            │                           │
            └─────────────┬─────────────┘
                          ▼
            ┌──────────────────────────────┐
            │  feature/pw-standard-librarian│
            │  (GitHub branch - origin)     │
            └──────────────────────────────┘
                          │
                          ▼
            ┌──────────────────────────────┐
            │    integration/nightly       │
            │  (merge all TAs)             │
            └──────────────────────────────┘
                          │
                          ▼
            ┌──────────────────────────────┐
            │     upstream/main            │
            │  (production)                │
            └──────────────────────────────┘
```

---

## 📁 File Ownership Model

### Lead Agent Owns (Strategic Coordination):

| File | Purpose | Update Trigger |
|------|---------|---------------|
| `context.json` | Mission status, blockers, completion % | After sub-agent reports, daily sync |
| `dependencies.yml` | Cross-TA deps, critical path | When dependencies change |
| `decisions.md` | Architecture decisions | Major design choices |
| `CLAUDE.md` roster | Agent assignments | When agent spawned/completed |
| `Current_Work.md` | Project status | After major milestones |

**Why lead agent owns:**
- Requires cross-TA visibility (only lead sees all 6 TAs)
- Strategic coordination (not tactical execution)
- Prevents conflicts between sub-agents

### Sub-Agents Own (Tactical Execution):

| File | Purpose | Update Trigger |
|------|---------|---------------|
| `ta{N}-current-progress.md` | Work log | Via `agent_sync.py log` (frequent) |
| `tests.yml` (status fields) | Test pass/fail status | After running tests |
| `ta{N}-completion-criteria.md` | Task checklist | As tasks complete |
| `release-checklist.md` | Release readiness | As items complete |
| Code files | Implementation | While coding |
| Test files | Test suites | While testing |
| Docs | Documentation | While documenting |

**Why sub-agents own:**
- They know their work best (self-documenting)
- Real-time updates (no lead agent bottleneck)
- Accountability (each agent tracks own progress)

### Shared (Both Can Update):

| File | Lead Agent Updates | Sub-Agent Updates |
|------|-------------------|-------------------|
| `decisions.md` | Major architectural choices | Task-specific design decisions |
| `context.json` | Overall status, blocker coordination | Remove blockers they fixed |

---

## 🔄 Daily Workflow Cycle

### Morning (Lead Agent):
```bash
1. Read all context.json files (TA1-TA6)
2. Check dependencies.yml for blockers
3. Review planning/master-plan progress logs
4. Identify critical path items
5. Spawn sub-agents for urgent work
6. Update CLAUDE.md roster
```

### During Day (Sub-Agents):
```bash
1. Read context files (understand state)
2. Execute assigned tasks
3. Log progress frequently (agent_sync.py log)
4. Update test/completion status
5. Commit code regularly
6. Report completion to lead
```

### Evening (Lead Agent):
```bash
1. Collect sub-agent reports
2. Update context.json (status, completion %)
3. Run integration checks (scripts/integration_run.sh)
4. Update Current_Work.md
5. Prepare next day's assignments
```

---

## 🤖 Sub-Agent Spawn Protocol

### Lead Agent Process:

```python
# 1. Prepare context
task_context = read(".claude/Task Agent 1/context.json")
mission = read("missions/TA1/mission.md")
decisions = read(".claude/Task Agent 1/decisions.md")

# 2. Spawn sub-agent with context
Task(
  description="Fix Bug Batch #11 enum syntax",
  subagent_type="general-purpose",
  prompt=f"""
  You are TA1-BugFix sub-agent.

  MISSION: Fix Bug Batch #11 enum syntax issues
  BRANCH: feature/pw-standard-librarian
  EXIT CRITERIA: C-style and YAML-style enum parsing works, all tests pass

  CONTEXT:
  {task_context}

  MISSION BRIEF:
  {mission}

  PRIOR DECISIONS:
  {decisions}

  INSTRUCTIONS:
  1. Read .claude/SUB_AGENT_TEMPLATE.md for full protocol
  2. Test both enum syntaxes (C-style, YAML-style)
  3. Create comprehensive test suite (90%+ coverage)
  4. Update documentation with examples
  5. Report back with completion summary

  FILES YOU'LL UPDATE:
  - dsl/pw_parser.py (if parser needs fixes)
  - tests/test_enums.py (comprehensive test suite)
  - docs/PW_PROGRAMMING_GUIDE.md (syntax examples)
  - .claude/Task Agent 1/context.json (remove blocker when done)
  - Via agent_sync.py log (progress updates)

  DO NOT TOUCH:
  - dependencies.yml (lead agent manages)
  - CLAUDE.md (lead agent manages)
  - Other TA files
  """
)

# 3. Update roster
update_claude_md(agent="TA1-BugFix", status="in_progress")

# 4. Wait for completion report
```

### Sub-Agent Lifecycle:

```
Spawn → Read Context → Execute Task → Update Files → Report Back → Terminate
   ↓         ↓              ↓              ↓              ↓           ↓
 Lead     Context/      Implement      Log progress   Completion   Lead
 Agent    Mission       + Test         via sync.py    summary      Agent
 call     files         + Doc                                      updates
```

---

## 🔀 Git Workflow (Fully Automated)

### Feature Branch Work (Sub-Agents):
```bash
# Sub-agents work here, commit regularly
feature/pw-standard-librarian (origin)
feature/pw-runtime-core (origin)
feature/pw-tooling-devex (origin)
# ... etc
```

### Integration Testing (Lead Agent):
```bash
# Lead agent runs: scripts/integration_run.sh
# Merges all feature branches to:
integration/nightly (origin)

# Runs tests, resolves conflicts
# If clean, proceeds to release
```

### Release to Production (Lead Agent):
```bash
# Lead agent runs: scripts/release.sh v2.2.0
# 1. Merges integration/nightly → upstream/main
# 2. Tags version
# 3. Pushes to both origin and upstream
# 4. Creates GitHub release
# 5. Publishes to PyPI
```

**User never touches git manually.**

---

## 📊 Status Synchronization (Automated)

### Auto-Update CLAUDE.md Roster:
```python
# scripts/update_status.py reads all context.json
# Updates CLAUDE.md table automatically

TA1: context.json completion=75% → CLAUDE.md "75% complete"
TA2: context.json status=blocked → CLAUDE.md "Blocked on TA1"
```

### Auto-Update Current_Work.md:
```python
# Reads all progress logs from planning/master-plan
# Generates "Recent Work" section
# Adds to Current_Work.md automatically
```

### User sees:
- CLAUDE.md always current (agent status)
- Current_Work.md always current (project status)
- Never needs to update manually

---

## 🚀 Release Automation (One Command)

### User says: "Release version 2.2.0"

### Lead agent executes:
```bash
# 1. Verify all TAs ready
./scripts/check_ready.sh  # Reads all context.json, ensures completion

# 2. Run integration
./scripts/integration_run.sh  # Merge all feature branches

# 3. Run full test suite
pytest tests/ -v --cov  # Must be 100% passing

# 4. Release
./scripts/release.sh v2.2.0
  # - Updates version in pyproject.toml, Current_Work.md
  # - Commits version bump
  # - Tags v2.2.0
  # - Pushes to origin + upstream
  # - Creates GitHub release with notes
  # - Publishes to PyPI (twine upload)

# 5. Update status
./scripts/update_status.py  # Sync CLAUDE.md, Current_Work.md

# 6. Notify user
"✅ Released v2.2.0 - PyPI live, GitHub release published"
```

**User never runs git commands. Lead agent orchestrates everything.**

---

## 🛡️ Safety Guardrails

### Pre-Merge Gates (Enforced):
```yaml
quality_gates:
  - all_tests_pass: true
  - coverage_min: 90%
  - no_regressions: true
  - benchmarks_within_sla: true
  - security_scan_clean: true
  - docs_updated: true
```

### Git Safety (Enforced):
```yaml
git_rules:
  - no_force_push: true
  - no_direct_upstream_push: true (sub-agents only push to origin)
  - commits_signed: true (via GitHub noreply)
  - secrets_blocked: true (trufflehog pre-commit)
```

### Conflict Resolution (Automated):
```bash
# If integration/nightly has conflicts:
1. Lead agent identifies conflict source (TA1 vs TA2)
2. Spawns mediator sub-agent
3. Mediator reads both decisions.md
4. Proposes resolution
5. Lead approves and applies
6. Re-runs integration
```

---

## 📈 Scaling to More TAs

### Adding TA7, TA8, etc:
```bash
# Lead agent runs:
./scripts/create_ta.sh TA7 "Web Dashboard" "feature/pw-web-dashboard"

# Creates:
- .claude/Task Agent 7/ (all template files)
- missions/TA7/ (local workspace)
- Updates CLAUDE.md roster
- Updates scripts/integration_run.sh (add branch)
- Updates dependencies tracking
```

**Infrastructure auto-scales. No manual setup.**

---

## 🎯 Success Metrics

### For User:
- ✅ Only talks to lead agent
- ✅ Never runs git commands
- ✅ Always sees current status (CLAUDE.md, Current_Work.md)
- ✅ Releases happen automatically
- ✅ Quality guaranteed (gates enforced)

### For Lead Agent:
- ✅ Spawns sub-agents efficiently
- ✅ Tracks all 6+ TAs simultaneously
- ✅ Detects blockers early (dependencies.yml)
- ✅ Coordinates integration cleanly
- ✅ Ships production releases confidently

### For Sub-Agents:
- ✅ Clear instructions (SUB_AGENT_TEMPLATE.md)
- ✅ Sufficient context (all .claude files)
- ✅ Self-documenting (update own files)
- ✅ Autonomous (no micromanagement)
- ✅ Accountable (progress tracked)

---

## 📚 Key Files Reference

| File | Location | Purpose |
|------|----------|---------|
| CLAUDE.md | Root | Lead agent playbook, roster |
| Current_Work.md | Root | Project status (auto-updated) |
| SUB_AGENT_TEMPLATE.md | .claude/ | Instructions for spawned agents |
| WORKFLOW.md | .claude/ | This document |
| context.json | .claude/Task Agent N/ | Mission status (lead updates) |
| dependencies.yml | .claude/Task Agent N/ | Cross-TA deps (lead updates) |
| decisions.md | .claude/Task Agent N/ | Architecture log (both update) |
| ta{N}-current-progress.md | .claude/Task Agent N/ | Work log (sub-agent updates) |
| tests.yml | .claude/Task Agent N/ | Test status (sub-agent updates) |
| release-checklist.md | .claude/Task Agent N/ | Release gates (sub-agent updates) |

---

## 🔗 Quick Commands (Lead Agent)

```bash
# Check all TA status
./scripts/check_status.sh  # Reads all context.json

# Spawn sub-agent
Task(description="...", subagent_type="general-purpose", prompt="...")

# Sync status docs
./scripts/update_status.py  # Updates CLAUDE.md, Current_Work.md

# Run integration
./scripts/integration_run.sh  # Merge all feature branches

# Release version
./scripts/release.sh v2.2.0  # Full release automation

# Check dependencies
./scripts/check_deps.sh  # Parse all dependencies.yml
```

---

**This workflow enables:** User → Lead Agent → Sub-Agents → Production

**User never touches:** Git, files, coordination, integration, releases

**Lead agent handles:** Everything via automation scripts + sub-agent orchestration
