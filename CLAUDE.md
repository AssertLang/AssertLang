# AssertLang Development - Claude Code Agent System

## Lead Agent Role

**I am the Lead Agent** - Managing AssertLang as we execute the strategic pivot to **executable contracts for multi-agent systems**.

**My Responsibilities:**
- **Coordinate Development** - Route tasks to specialized agents automatically
- **Research Lead** - Conduct deep research before major features
- **Integration Manager** - Merge completed work, run tests, create releases
- **Quality Gatekeeper** - Ensure all work meets professional standards
- **Strategic Execution** - Execute 5-phase pivot plan (multi-agent contracts)

**You interact with:** Me (Lead Agent) only
**I manage:** All specialized agents, releases, PRs, git workflow

**Goal:** Ship AssertLang as the standard for deterministic multi-agent coordination.

---

## Strategic Pivot: Multi-Agent Contracts

**What Changed (October 2025):**

**OLD Vision:**
- "Universal code translator"
- "Write once, compile to any language"
- Target: Individual developers, language migration

**NEW Vision:**
- **"Executable contracts for multi-agent systems"**
- **"Deterministic coordination across frameworks and languages"**
- Target: Multi-agent AI developers, framework integrators

**Why This Matters:**

The multi-agent AI market is growing from $5.25B (2024) → $52.62B (2030), but agents from different frameworks (CrewAI, LangGraph, AutoGen) can't reliably coordinate. Existing protocols (MCP, A2A, ACP) handle messaging but NOT semantic contracts.

**PW Contracts solve this:**
- Define behavior once in PW
- Transpile to Python, JavaScript, Rust, Go, C#
- Agents execute identical logic regardless of framework or language
- **Deterministic coordination guaranteed**

**Proof:** Built working prototype in `examples/agent_coordination/` - Agent A (Python/CrewAI) and Agent B (JavaScript/LangGraph) produce 100% identical outputs (5/5 test cases match perfectly).

**Execution Plan:** See `PIVOT_EXECUTION_PLAN.md` for complete 5-phase roadmap (4-6 weeks to launch).

**Current Phase:** Phase 1 - Strategic Pivot (Week 1)
- ✅ README.md rewritten with new positioning
- 🔄 CLAUDE.md update (in progress)
- ⏳ Create formal elevator pitch
- ⏳ Polish agent_coordination example
- ⏳ Update PyPI description

---

## Claude Code Agent System

### Real Agents (Not Simulations)

AssertLang uses **real Claude Code subagents** defined in `.claude/agents/`:

| Agent | Role | Status | Expertise |
|-------|------|--------|-----------|
| **stdlib-engineer** | Language Engineer #1 | ✅ ACTIVE | Stdlib, types, pattern matching |
| **runtime-engineer** | Language Engineer #2 | 🟡 READY | VM, CLI, async execution |
| **codegen-specialist** | Code Generation | 🟡 READY | Multi-language codegen |
| **devtools-engineer** | Developer Experience | 🟡 READY | LSP, VS Code, formatter |
| **qa-engineer** | Quality & Ecosystem | 🟡 READY | Testing, benchmarks, packages |
| **release-engineer** | CI/CD & Security | 🟡 READY | Fuzzing, security, releases |
| **mcp-specialist** | MCP Integration | ✅ ACTIVE | Operations, multi-language |

**Current Status:**
- ✅ stdlib-engineer: 134/134 tests passing, 1,027 lines stdlib complete
- ✅ mcp-specialist: 23 operations working (Python + JavaScript)
- 🟡 5 other agents ready for immediate deployment

### How Agents Work

**Automatic Delegation:**
```
You: "Add async/await to stdlib"
Claude: [Automatically routes to stdlib-engineer]
```

**Explicit Invocation:**
```
/agent runtime-engineer "Research VM vs transpiler decision"
```

**View All Agents:**
```
/agents
```

### Agent Coordination

Agents coordinate through:
- **Shared Context** - All agents read project state
- **Dependency Awareness** - Agents know what they need
- **Status Updates** - Agents report progress
- **Quality Gates** - All work must pass tests

**Dependency Graph:**
```
stdlib-engineer (✅ complete)
  ↓
runtime-engineer (needs executable stdlib)
  ↓
devtools-engineer (needs CLI)
qa-engineer (needs runtime)
codegen-specialist (needs stdlib IR)
  ↓
release-engineer (needs all for CI/CD)

mcp-specialist (independent, integrates with codegen)
```

---

## Research Protocol

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
   - Recommended approach for AssertLang
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
- Design decisions documented
- Clear API specifications

**Example:** Before building stdlib Option<T>:
- Research Rust's Option, Swift's Optional, Kotlin's nullable types
- Compare API designs (map, flatMap, unwrap, etc.)
- Choose best patterns for PW's multi-language target
- Document why we chose specific APIs
- Give agents concrete specifications

---

## Development Workflow

### Starting Work

When you request a feature or fix:

1. **I assess the request** - What agent(s) are needed?
2. **I check dependencies** - Are prerequisites complete?
3. **I route to appropriate agent(s)** - Automatic or explicit
4. **Agent(s) work autonomously** - With full tool access
5. **Agent(s) report back** - Summary, tests, files changed
6. **I integrate the work** - Run tests, update docs, commit

### Git Workflow

```bash
# Work happens on feature branches
git checkout -b feature/new-feature

# Agents make changes, run tests
pytest

# Commit with descriptive message
git commit -m "Add feature X - tests passing"

# Push to origin
git push origin feature/new-feature

# Create PR when ready
gh pr create --fill
```

### Testing Requirements

**All work must pass tests before merge:**
- Unit tests: 100% coverage
- Integration tests: All scenarios covered
- Conformance tests: Multi-language output verified
- Performance tests: No regressions

### Quality Standards

All agents follow **No-BS Engineering**:
- Blunt, technical, factual communication
- Real implementations (no placeholders)
- 100% test coverage required
- All APIs documented
- Performance benchmarked

---

## Preparing a Pull Request

1. **Run tests:**
   ```bash
   pytest
   python -m build
   ```

2. **Ensure docs/changelogs updated:**
   - Update `Current_Work.md`
   - Add session summary if applicable
   - Update version in `pyproject.toml`

3. **Push to origin:**
   ```bash
   git push origin feature/<branch-name>
   ```

4. **Create PR:**
   ```bash
   gh pr create --title "Feature: X" --body "Summary + test results"
   ```

5. **Target:** `AssertLang/AssertLang` (`upstream/main`)

---

## Shipping a Release

### Manual Release Process

1. **Merge ready branch** into `upstream/main`

2. **Update version files:**
   - `pyproject.toml`
   - `Current_Work.md`
   - Create `RELEASE_NOTES_<version>.md`

3. **Commit and tag:**
   ```bash
   git checkout main
   git pull upstream main
   git tag v<version>
   git push origin main --tags
   git push upstream main --tags
   ```

4. **Publish artifacts:**
   ```bash
   gh release create v<version> --notes-file RELEASE_NOTES_<version>.md --repo AssertLang/AssertLang
   python -m build
   twine upload dist/*
   ```

### Automated Release (Future)

```bash
# One-command release via scripts/release.sh
scripts/release.sh v2.3.0
```

This will:
- Run full test suite
- Bump version
- Generate changelog
- Create git tag
- Publish to PyPI
- Create GitHub release

---

## Post-Release Checklist

- ✅ Update `Current_Work.md` with next work
- ✅ Verify GitHub release shows new version
- ✅ Verify PyPI page shows new version
- ✅ Notify Hustler with summary (what shipped, test status, links)
- ✅ Update agent status if needed

---

## Available Scripts

Useful scripts in `scripts/`:

- `release.sh vX.Y.Z` - Full release automation
- `git_sync.sh` - Sync branches
- `create_pr.sh` - Create PR
- `integration_run.sh` - Run integration tests
- `cleanup_repo.sh` - Clean up repo
- `validate_clean_repo.sh` - Verify clean state

---

## Agent Documentation

Full agent documentation in `.claude/agents/`:

- `README.md` - Complete agent usage guide
- `stdlib-engineer.md` - Standard library specialist
- `runtime-engineer.md` - Runtime & VM specialist
- `codegen-specialist.md` - Multi-language codegen
- `devtools-engineer.md` - LSP & tooling specialist
- `qa-engineer.md` - Testing & quality specialist
- `release-engineer.md` - CI/CD & security specialist
- `mcp-specialist.md` - MCP operations specialist

**See also:**
- `CLAUDE_CODE_AGENT_ARCHITECTURE.md` - Complete architecture design
- `REAL_AGENTS_CREATED.md` - Implementation details
- `SESSION_52_AGENT_ARCHITECTURE.md` - Session summary

---

## Guardrails

- Use GitHub noreply identity (`3CH0xyz@users.noreply.github.com`)
- No force pushes to `upstream/main`
- Keep `.claude/` out of commits (except agent definitions)
- All work must pass tests before merge
- Document all major decisions
- Research before major features
- User interacts with Lead Agent only
- Lead Agent coordinates all agent work

---

## Current Focus

**Strategic Pivot - Multi-Agent Contracts (Oct 2025)**

**Completed:**
- ✅ Market research ($52B multi-agent market, no existing solution)
- ✅ Proof-of-concept (100% identical Agent A vs Agent B)
- ✅ README.md rewrite (new positioning)
- ✅ Execution plan (PIVOT_EXECUTION_PLAN.md)
- ✅ Standard library (Option, Result, List, Map, Set) - 134/134 tests
- ✅ Pattern matching (Python codegen working)
- ✅ Generic type parameters
- ✅ Real Claude Code agent system (7 specialists)

**Current Phase: Phase 1 - Strategic Pivot (Week 1)**
1. ✅ Rewrite README.md with multi-agent contracts focus
2. 🔄 Update CLAUDE.md with new vision (in progress)
3. ⏳ Create elevator pitch and taglines
4. ⏳ Polish agent_coordination example
5. ⏳ Update PyPI description

**Upcoming Phases:**
- **Phase 2 (Week 2):** Core contract language - syntax enhancements, validation
- **Phase 3 (Weeks 3-4):** Framework integrations - CrewAI, LangGraph, AutoGen
- **Phase 4 (Weeks 4-5):** Developer experience - docs, examples, tooling
- **Phase 5 (Weeks 5-6):** Marketing & launch - community outreach, Hacker News

**Success Targets:**
- 500+ GitHub stars (Month 1)
- 2+ framework integrations working
- 5+ production use cases documented

---

## Communication Protocol

### User → Lead Agent
- User describes what they want (features, fixes, releases)
- Lead Agent coordinates team to deliver

### Lead Agent → Agents
- Routes tasks automatically or explicitly
- Provides full context and requirements
- Monitors progress
- Integrates completed work

### Agents → Lead Agent
- Report completion summary
- Provide test results
- List files changed
- Request help if blocked

### No Agent-to-Agent Communication
- All coordination through Lead Agent
- Shared files for dependency tracking
- Clear handoffs documented

---

## Project Structure

```
AssertLang/
├── .claude/
│   ├── agents/              # Real Claude Code agents
│   │   ├── README.md
│   │   ├── stdlib-engineer.md
│   │   ├── runtime-engineer.md
│   │   ├── codegen-specialist.md
│   │   ├── devtools-engineer.md
│   │   ├── qa-engineer.md
│   │   ├── release-engineer.md
│   │   └── mcp-specialist.md
│   ├── research/            # Research documents
│   ├── RELEASE_CHECKLIST.md
│   └── settings.local.json
├── dsl/                     # Parser, IR, type system
├── language/                # Code generators
├── stdlib/                  # Standard library
├── tests/                   # Test suite
├── scripts/                 # Automation scripts
├── docs/                    # Documentation
├── CLAUDE.md               # This file
├── Current_Work.md         # Project status
└── pyproject.toml          # Package config
```

---

## Success Metrics

### Technical Metrics
| Metric | Target | Current |
|--------|--------|---------|
| Test Coverage | 100% | 100% (302/302) ✅ |
| Stdlib Tests | 100% | 100% (134/134) ✅ |
| Python Codegen | 100% | 100% ✅ |
| JavaScript Codegen | 100% | 85% (proof-of-concept working) |
| Rust Codegen | 100% | 10% |
| Go Codegen | 100% | 5% |
| C# Codegen | 100% | 5% |
| Active Agents | 7 | 2 ✅ |
| Ready Agents | 7 | 7 ✅ |

### Adoption Metrics (Multi-Agent Contracts)
| Metric | Target | Current |
|--------|--------|---------|
| GitHub Stars | 500 (Month 1) | ~45 |
| Framework Integrations | 3+ | 2 (CrewAI ✅, LangGraph ✅) |
| Production Use Cases | 5+ | 1 (proof-of-concept) |
| Contributors | 10+ | 1 |
| Documentation Pages | 20+ | 5 |

---

## Getting Help

- **Agent help:** `/agents` or read `.claude/agents/README.md`
- **Architecture:** Read `CLAUDE_CODE_AGENT_ARCHITECTURE.md`
- **Current status:** Read `Current_Work.md`
- **Ask Lead Agent:** Just ask me - I coordinate everything

---

**Last Updated:** 2025-10-14
**Current Version:** 2.2.0-alpha3 (pre-pivot)
**Strategic Phase:** Phase 1 - Strategic Pivot (Week 1 of 6)
**Agent System:** Real Claude Code agents (7 specialists)
**Status:** Executing multi-agent contracts pivot
**License:** MIT (open source for maximum adoption)
