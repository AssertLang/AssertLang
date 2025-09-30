# Promptware Execution Plan

**Vision**: Universal agent communication protocol for cloud-native AI systems

Promptware enables autonomous agents written in any language (Python, Node, Go, Rust, .NET, Java, C++, Next.js) to coordinate via a shared `.pw` protocol based on MCP verbs. Agents expose capabilities as MCP verbs and call other agents' verbs for bidirectional, language-agnostic coordination.

---

## Wave 1 — Foundation (✅ COMPLETE)

**Goal**: Core DSL parsing, interpretation, and file generation

| Milestone | Description | Status |
| --- | --- | --- |
| DSL grammar | Finalize syntax for `lang`, `file`, `tool`, `call`, `if`, `parallel`, `let`, `state` | ✅ |
| DSL parser | Parse `.pw` files into execution plans | ✅ |
| DSL interpreter | Execute plans with control flow (if/parallel/fanout/merge) | ✅ |
| Timeline events | Emit structured events for observability | ✅ |
| Python runner | File generation, process spawning (apply/start/stop/health) | ✅ |

**Validation**:
- `python3 -m pytest tests/test_dsl_parser.py` — 17 tests passing
- `python3 -m pytest tests/test_dsl_interpreter.py` — 19 tests passing

---

## Wave 2 — Multi-Language Infrastructure (✅ COMPLETE)

**Goal**: Extend runners and tool adapters to multiple languages

| Milestone | Description | Status |
| --- | --- | --- |
| Node.js runner | File generation, process spawning | ✅ |
| Go runner | File generation, process spawning | ✅ |
| Rust runner | File generation, process spawning | ✅ |
| Tool adapters (38 tools × 5 languages) | 190 adapters for Python/Node/Go/Rust/.NET | ✅ |
| Toolgen templates | Code generation for all languages | ✅ |

**Validation**:
- 38 tools each have 5 adapters (Python, Node, Go, Rust, .NET)
- All runners tested: apply/start/stop/health methods working
- 100% adapter coverage achieved

**Note**: This infrastructure supports file generation and process spawning, but does NOT yet enable agent-to-agent communication (the core vision). Wave 2 built plumbing, not the product.

---

## Wave 2.5 — Agent Communication Pivot (🔨 IN PROGRESS)

**Goal**: Enable bidirectional agent-to-agent communication via MCP

**Core Vision**: Agents expose MCP verbs and call other agents' verbs at runtime.

### Week 1-2: MCP Server Generation

| Task | Description | Status |
| --- | --- | --- |
| `expose` syntax | Extend DSL parser to handle `expose` blocks defining MCP verbs | ☐ |
| Python MCP server generator | `.pw` → FastAPI/Flask MCP server on port 23456 | ☐ |
| Verb routing | Map incoming MCP calls to handler functions | ☐ |
| Error handling | Return MCP-formatted errors (E_ARGS, E_RUNTIME, etc.) | ☐ |
| Basic demo | Agent exposes `status@v1`, responds to calls | ☐ |

**Example `.pw` file**:
```pw
lang python
agent task-executor
port 23456

expose task.execute@v1:
  params:
    task_id string
    priority int
  returns:
    status string
    result object

expose task.status@v1:
  params:
    task_id string
  returns:
    status string
    progress int
```

**Generated output**: Python MCP server running on port 23456

### Week 3: MCP Client Library

| Task | Description | Status |
| --- | --- | --- |
| Python MCP client | Library for calling MCP verbs on other agents | ☐ |
| `call` statement for agents | Extend DSL: `call agent-name verb@v1 params=...` | ☐ |
| HTTP transport | JSON-RPC over HTTP/WebSocket | ☐ |
| Error handling | Timeouts, retries, connection failures | ☐ |
| Basic demo | Agent A calls Agent B's verb | ☐ |

**Example usage in `.pw`**:
```pw
lang python
agent orchestrator

call task-executor task.execute@v1 task_id="abc123" priority=1
call task-executor task.status@v1 task_id="abc123"
```

### Week 4: Two-Agent Coordination Demo

| Task | Description | Status |
| --- | --- | --- |
| Agent 1: Code Reviewer | Exposes `review.submit@v1`, `review.status@v1` | ☐ |
| Agent 2: Orchestrator | Calls reviewer, polls status, reports results | ☐ |
| End-to-end demo | Video showing two agents coordinating via `.pw` | ☐ |
| Error scenarios | Test timeout, agent down, invalid params | ☐ |

**Demo flow**:
1. Start code-reviewer agent (port 23456)
2. Start orchestrator agent (port 23457)
3. Send webhook to orchestrator
4. Orchestrator calls reviewer's `review.submit@v1`
5. Orchestrator polls `review.status@v1` until complete
6. Orchestrator prints results

### Week 5-6: Polish & Documentation

| Task | Description | Status |
| --- | --- | --- |
| Service discovery | Hardcoded addresses for now (localhost:23456, :23457) | ☐ |
| Authentication | Token-based agent-to-agent auth | ☐ |
| Logging/tracing | Log all inter-agent calls | ☐ |
| Error recovery | Retry logic, circuit breakers | ☐ |
| Documentation | Agent communication guide, examples, deployment | ☐ |

**Deliverables**:
- `docs/agent-communication-guide.md`
- 3-5 example agents
- Working demo video

---

## Wave 3 — Cross-Language Agents (📋 PLANNED)

**Goal**: Agents in different languages coordinating via `.pw`

| Milestone | Description | Status |
| --- | --- | --- |
| Node.js MCP server generator | `.pw` → Express/Fastify MCP server | ☐ |
| Cross-language demo | Python agent calls Node agent | ☐ |
| Go MCP server generator | `.pw` → Go net/http MCP server | ☐ |
| Rust MCP server generator | `.pw` → Actix/Axum MCP server | ☐ |
| Multi-language coordination | 4 agents (Py/Node/Go/Rust) coordinating | ☐ |

**Success criteria**: Same `.pw` verb definitions generate working MCP servers in 4 languages, all interoperable.

---

## Wave 4 — Agent Registry & Discovery (📋 PLANNED)

**Goal**: Dynamic agent discovery and coordination at scale

| Milestone | Description | Status |
| --- | --- | --- |
| Agent registry service | Central registry of available agents and their verbs | ☐ |
| Service discovery | Agents register on startup, discover peers dynamically | ☐ |
| Health monitoring | Registry tracks agent availability | ☐ |
| Load balancing | Route calls to healthy agent replicas | ☐ |
| CLI tools | `pw registry register/discover/call` commands | ☐ |

**Example**:
```bash
# Register agent
pw registry register code-reviewer http://localhost:23456

# Discover agents
pw registry discover "code-review"

# Call agent
pw registry call code-reviewer review.submit@v1 pr_url="..."
```

---

## Wave 5 — Production-Ready Infrastructure (📋 PLANNED)

**Goal**: Deploy and manage agents at scale

| Milestone | Description | Status |
| --- | --- | --- |
| Kubernetes deployment | Deploy agents as pods, expose via services | ☐ |
| Observability | Metrics, tracing, logging for agent communication | ☐ |
| Security | mTLS, authentication, authorization between agents | ☐ |
| Performance | Connection pooling, caching, optimization | ☐ |
| Agent marketplace | Public registry of reusable agents | ☐ |

---

## Wave 6 — Natural Language Compiler (🔮 FUTURE)

**Goal**: Optional natural language → `.pw` compilation

| Milestone | Description | Status |
| --- | --- | --- |
| NL → .pw compiler | "Create a code review agent" → generates agent.pw | ☐ |
| LLM integration | Claude/GPT generates .pw definitions | ☐ |
| Validation | Ensure generated .pw is correct and secure | ☐ |

**Note**: This is optional. The core vision is `.pw` as a programming language, not NL magic.

---

## What Changed (Pivot Summary)

### OLD Vision (Pre-Pivot)
- Focus: File generation and process spawning
- Use case: "Write .pw once, deploy to multiple languages"
- Problem: Not compelling — just a template system

### NEW Vision (Post-Pivot)
- Focus: Agent-to-agent communication via MCP
- Use case: "Autonomous agents coordinate via shared protocol"
- Problem solved: Language-agnostic agent infrastructure for cloud systems

### What Stays from Wave 1-2
- ✅ DSL parser (still needed for `expose`/`call` syntax)
- ✅ Multi-language code generation (now generates MCP servers)
- ✅ Tool adapters (agents can use tools internally)
- ✅ Runners (now run MCP servers, not just scripts)

### What's New in Wave 2.5+
- 🆕 `expose` blocks (define MCP verbs)
- 🆕 MCP server generation (agents as first-class citizens)
- 🆕 MCP client library (agents call each other)
- 🆕 Bidirectional coordination (not just one-way execution)

---

## Success Metrics

### Wave 2.5 (6 weeks)
- [ ] Two agents coordinating via `.pw` in Python
- [ ] Working demo video showing bidirectional communication
- [ ] Documentation: how to write agents, deploy them, connect them

### Wave 3 (8 weeks)
- [ ] Agents in 4 languages (Python/Node/Go/Rust) interoperating
- [ ] Cross-language demo: Python agent calls Node agent calls Rust agent

### Wave 4 (12 weeks)
- [ ] 10+ agents deployed and coordinating
- [ ] Registry with discovery and health monitoring
- [ ] 2-3 real-world use cases validated

---

## Current Status (2025-09-30)

**Completed**:
- Wave 1: DSL parser, interpreter, Python runner (✅)
- Wave 2: Multi-language runners, 190 tool adapters (✅)

**In Progress**:
- Wave 2.5: Agent communication architecture (🔨)
  - Updating documentation and roadmap
  - Next: Build MCP server generator for Python

**Blocked**: None

**Risks**:
- MCP spec suitability for agent-to-agent communication (need to validate)
- Anthropic's roadmap for MCP (are they supportive of this use case?)
- Market adoption (need to find early users/partners)

---

## Quick Reference

### Key Concepts
- **Agent**: Autonomous program that exposes and calls MCP verbs
- **MCP verb**: Typed operation (e.g., `task.execute@v1`) with params/returns
- **`.pw` file**: Defines agent's exposed verbs and coordination logic
- **Port 23456**: Standard port for Promptware agent MCP servers
- **Bidirectional**: Agents can both expose verbs AND call other agents' verbs

### Example Agent

```pw
lang python
agent code-reviewer
port 23456

expose review.submit@v1:
  params:
    pr_url string
  returns:
    review_id string
    status string

on review_complete:
  # Agent can call other agents
  call notifier send.slack@v1 message="Review complete"
```

This generates a Python MCP server that:
- Runs on port 23456
- Exposes `review.submit@v1` verb
- Can call other agents' verbs (like `notifier`)

---

Keep this file in sync with `docs/agents.md` and `docs/Claude.md` for seamless handoffs.