# Promptware: Pivot to Agent Communication Architecture

**Date**: 2025-09-30
**Status**: Wave 2.5 in progress

---

## What Changed

### OLD Vision (Pre-Pivot)
**Problem we tried to solve**: "Write code once in `.pw`, deploy to multiple languages"

**Implementation (Wave 1-2)**:
- DSL parser for `.pw` files
- File generation system
- Process spawning (runners)
- 190 tool adapters (38 tools × 5 languages)

**Reality check**: This is just a template system. Not compelling. Why would someone use `.pw` instead of writing Python/Node/Go directly?

---

### NEW Vision (Post-Pivot)
**Problem we actually solve**: "Autonomous agents in different languages need to coordinate"

**Core idea**: Agents expose and call MCP verbs via `.pw` for bidirectional, language-agnostic communication.

**Example**:
```pw
# Agent A (Python)
lang python
agent code-reviewer
port 23456

expose review.submit@v1:
  params:
    pr_url string
  returns:
    review_id string

# Agent B (Node.js) calls Agent A
call code-reviewer review.submit@v1 pr_url="https://..."
```

**Why this matters**: As AI agents proliferate, they need a common protocol. `.pw` becomes the universal language for agent coordination—like HTTP for web services.

---

## What We Keep from Wave 1-2

### ✅ Still Valuable
- **DSL parser** — Now parses `expose` and `call` for agents
- **Multi-language code generation** — Now generates MCP servers, not just files
- **Tool adapters** — Agents can use tools internally
- **Runners** — Now run MCP servers, not just one-off scripts

**The infrastructure we built isn't wasted.** It's the foundation, just redirected toward a better goal.

---

## What We're Building (Wave 2.5+)

### Wave 2.5: Agent Communication (6 weeks)
**Goal**: Two Python agents coordinating via `.pw`

**Deliverables**:
1. `expose` syntax in DSL parser
2. Python MCP server generator (FastAPI/Flask)
3. Python MCP client library
4. Demo: Agent A calls Agent B's verbs
5. Documentation: how to write agents

### Wave 3: Cross-Language Agents (8 weeks)
**Goal**: Agents in 4 languages (Py/Node/Go/Rust) interoperating

**Deliverables**:
1. Node.js MCP server generator
2. Go MCP server generator
3. Rust MCP server generator
4. Demo: Python agent → Node agent → Rust agent

### Wave 4: Agent Registry (12 weeks)
**Goal**: 10+ agents with discovery and health monitoring

**Deliverables**:
1. Agent registry service
2. Service discovery protocol
3. CLI tools: `pw registry register/discover/call`
4. 2-3 real-world use cases validated

---

## The Vision: Agent Coordination at Scale

### Use Case: 50 Specialized Agents

**Scenario**: Platform team running multiple AI agents for DevOps automation

**Agents**:
- `code-reviewer` (Python) — Reviews PRs
- `test-runner` (Node.js) — Runs tests
- `deployer` (Go) — Manages deployments
- `monitor` (Rust) — Tracks metrics
- `notifier` (Python) — Sends alerts

**Coordination**:
```pw
# Orchestrator agent coordinates workflow
call code-reviewer review.submit@v1 pr="123"
wait for code-reviewer review.status@v1 == "approved"

call test-runner test.execute@v1 branch="main"
wait for test-runner test.results@v1 == "passed"

call deployer deploy.start@v1 version="1.2.3"
call monitor metrics.current@v1

if monitor metrics.error_rate@v1 > 0.05:
  call deployer deploy.rollback@v1
  call notifier send.slack@v1 message="Rollback triggered"
```

**All agents speak `.pw`. All coordinate via MCP verbs. Language-agnostic.**

---

## Why This Is Novel

### What Exists Today
- **LangGraph** — Agent orchestration, Python-only
- **AutoGen** — Multi-agent systems, Python-only
- **Agent Protocol** — Standardization attempt, not widely adopted
- **gRPC** — Universal RPC, but not agent-specific

### Promptware's Advantage
1. **Language-agnostic from day one** — Python, Node, Go, Rust, .NET, Java, C++
2. **MCP-native** — Built on Anthropic's Model Context Protocol
3. **Code generation** — Write `.pw`, get MCP server in any language
4. **Cloud-native** — Port 23456, discovery, health monitoring, Kubernetes-ready

**Positioning**: "HTTP for AI agents. One protocol, every language."

---

## Market & Timing

### Target Market
**Not**: Individual developers building apps (too broad, no pain point)

**Yes**: Platform teams building agent infrastructure
- Companies running 10+ agents
- Need coordination, discovery, monitoring
- Polyglot teams (Python ML, Node APIs, Go services, Rust performance)
- Cloud-native deployment (Kubernetes, service meshes)

### Timing
**2025-2026**: Agent explosion happening now
- Every company building agents
- No standard for agent communication
- Fragmentation is a real problem
- Early but not too early

---

## Success Criteria

### Wave 2.5 (6 weeks) — Validation
- [ ] Two Python agents coordinating via `.pw`
- [ ] Working demo video
- [ ] Documentation published

**If this works, vision is validated. If not, pivot or stop.**

### Wave 3 (8 weeks) — Cross-Language
- [ ] 4 languages (Py/Node/Go/Rust) interoperating
- [ ] Cross-language demo
- [ ] 5+ example agents

### Wave 4 (12 weeks) — Production-Ready
- [ ] 10+ agents deployed
- [ ] Registry with discovery
- [ ] 2-3 real customers using it

---

## Risks & Mitigations

### Risk 1: MCP Not Suited for Agent-to-Agent
**Risk**: MCP designed for AI ↔ tools, not agent ↔ agent

**Mitigation**:
- Read MCP spec thoroughly
- Prototype early
- Talk to Anthropic about use case

### Risk 2: No One Cares
**Risk**: Build it and developers don't use it

**Mitigation**:
- Find 2-3 potential users NOW
- Build for them specifically
- Validate demand before scaling

### Risk 3: Someone Else Builds This First
**Risk**: LangGraph/AutoGen add multi-language support

**Mitigation**:
- Move fast (6-week cycles)
- Focus on cross-language (their weakness)
- Build community early

---

## What NOT To Do

### ❌ Don't Expand Languages Yet
- Focus on Python for Wave 2.5
- Add languages only after agent communication works

### ❌ Don't Build More Tools
- 190 adapters is enough
- Focus on MCP server/client, not tools

### ❌ Don't Build Marketplace/Registry Yet
- Hardcode addresses for Wave 2.5
- Build discovery in Wave 4 when you have 10+ agents

### ❌ Don't Optimize Prematurely
- No Kubernetes integration yet
- No fancy scheduling
- Just HTTP calls between agents

---

## Next Steps (Immediate)

### This Week
1. ✅ Update execution plan and manifesto
2. ✅ Create pivot summary (this doc)
3. ⏭️ Extend DSL parser for `expose` syntax
4. ⏭️ Build basic Python MCP server generator
5. ⏭️ Demo: Single agent exposes one verb

### Next Week
- Build Python MCP client library
- Demo: Agent A calls Agent B

### Week 3-4
- Build two-agent coordination example
- Polish error handling, logging
- Create demo video

---

## Key Concepts (Quick Reference)

### Agent
Autonomous program that exposes and calls MCP verbs

### MCP Verb
Typed operation (e.g., `task.execute@v1`) with params/returns

### `.pw` File
Defines agent's exposed verbs and coordination logic

### Port 23456
Standard port for Promptware agent MCP servers

### Bidirectional
Agents can both expose verbs AND call other agents' verbs

---

## Example Agent (Reference)

```pw
lang python
agent code-reviewer
port 23456

# Expose verbs for other agents to call
expose review.submit@v1:
  params:
    pr_url string
  returns:
    review_id string
    status string

expose review.status@v1:
  params:
    review_id string
  returns:
    status string
    comments array

# Call other agents' verbs
on review_complete:
  call notifier send.slack@v1 message="Review complete"
  call test-runner test.execute@v1 branch={pr.branch}
```

**This generates**:
- Python MCP server on port 23456
- Exposes `review.submit@v1` and `review.status@v1`
- Can call `notifier` and `test-runner` agents
- Fully autonomous coordination

---

## Bottom Line

**Old vision**: Template system for multi-language code generation (not compelling)

**New vision**: Universal protocol for agent communication (actually novel)

**What changed**: Focus shifted from "generate files" to "agents coordinate"

**What didn't change**: The infrastructure (DSL, runners, adapters) still useful, just repurposed

**Path forward**: Prove agent communication works in Python (6 weeks), then scale to other languages

**Success metric**: Two agents coordinating via `.pw` by end of Wave 2.5

---

This pivot saves the project by focusing on a real problem with a real market at the right time.