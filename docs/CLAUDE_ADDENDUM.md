# Claude Code Agent Guide - Addendum (Session 10)

**IMPORTANT:** Read this addendum FIRST before reading `CLAUDE.md`

This document clarifies the product vision and corrects terminology after Session 10 discussion.

---

## Product Vision Clarification

### What Is Promptware?

**Promptware = Universal polyglot service protocol for AI-native systems**

Think: "gRPC for the AI era"

### NOT Building

❌ "Agent coordination platform" like LangGraph/AutoGen  
❌ Just "IDE tools"  
❌ Template system for code generation

### Actually Building

✅ **Service protocol with dual transports:**
- stdio transport → IDE tools (Cursor, VSCode, etc.)
- HTTP transport → Microservices (Python ↔ Node ↔ Go)

✅ **Same .pw definition, multiple deployment modes**

---

## Terminology Corrections

### OLD (Wrong)

- `.pw` files = "agents"
- HTTP servers = "agent coordination"
- Cursor integration = "agent tools"

### NEW (Correct)

- `.pw` files = **services** or **tools**
- stdio transport = **IDE integration** (tools for IDEs)
- HTTP transport = **microservices** (service-to-service)
- Real agents = **Cursor's AI** (uses our tools)

**Example:**
```pw
service user-service  # ← NOT "agent"
lang python

expose user.get@v1:  # ← This is a SERVICE VERB or TOOL
  params: user_id string
  returns: name string, email string
```

---

## The Two Transports

### stdio Transport (Wave 2) - ✅ COMPLETE

**Purpose:** IDE tools, CLI applications  
**Status:** Production-ready  
**File:** `language/mcp_stdio_server.py`

**How it works:**
```
Cursor IDE → spawns subprocess → mcp_stdio_server.py
          → writes JSON-RPC to stdin
          → reads JSON-RPC from stdout
          → Tools available in Cursor
```

**What we built:**
- Native stdio MCP server
- Tool registry & executor  
- 11 working tools in Cursor
- Dual-mode (IDE-integrated + standalone AI)
- 104+ tests passing

### HTTP Transport (Wave 3) - 🔨 NEXT

**Purpose:** Microservices, distributed systems  
**Status:** 80% built, needs integration  
**File:** `language/mcp_server_generator.py` (exists, needs updating)

**How it works:**
```
Service A (Python) → HTTP POST → Service B (Node.js)
                   → JSON-RPC over HTTP
                   → MCP verb call
                   → Response
```

**What we need:**
- Update HTTP server generator
- Build Python MCP client library
- Service-to-service demos
- Cross-language support

---

## Current Architecture

### What We Have (Sessions 1-9)

```
┌──────────────┐
│  Cursor IDE  │ ← The real "agent"
│  (GPT/Claude)│
└──────┬───────┘
       │ stdio
       v
┌─────────────────────┐
│ mcp_stdio_server.py │
│ (.pw tool servers)  │
└─────────────────────┘
       │
       v
 ┌─────────────┐
 │ Tool Registry│
 │ Tool Executor│
 └─────────────┘
       │
       v
 Real tools: http,
 storage, logger, etc.
```

**Key points:**
- Cursor's AI is the agent
- Our `.pw` servers provide tools
- Tools execute real functionality
- stdio = local communication

### What We're Building (Sessions 10+)

```
┌────────────┐  HTTP   ┌────────────┐  HTTP   ┌────────────┐
│  Service A │────────>│  Service B │────────>│  Service C │
│  (Python)  │  MCP    │  (Node.js) │  MCP    │    (Go)    │
│  port 23450│<────────│  port 23451│<────────│  port 23452│
└────────────┘         └────────────┘         └────────────┘

Same .pw verb definitions
Different transport (HTTP instead of stdio)
Polyglot service communication
```

**Key points:**
- Services call each other over network
- HTTP = distributed communication
- Same MCP protocol, different transport
- Cross-language by design

---

## Implementation Priorities

### ✅ Completed (Wave 2)

1. stdio MCP server working
2. Tool integration complete
3. 11 tools tested in Cursor
4. Dual-mode architecture
5. Comprehensive tests

### 🔨 In Progress (Wave 3 - HTTP Transport)

**Phase 1 (Week 1):** Audit & update HTTP server generator  
**Phase 2 (Week 2-3):** Build Python MCP client library  
**Phase 3 (Week 4):** Two-service demo (Python ↔ Python)  
**Phase 4 (Week 5-6):** Cross-language support (Python ↔ Node)

See `docs/http-transport-integration.md` for full plan.

### 📋 Future (Wave 4+)

- Production features (discovery, auth, observability)
- Go/Rust client libraries
- Service mesh integration
- Enterprise features

---

## Key Files to Know

### stdio Transport (Current)

- `language/mcp_stdio_server.py` - Main stdio server
- `tools/registry.py` - Tool discovery/loading
- `language/tool_executor.py` - Tool orchestration
- `tests/test_mcp_integration.py` - End-to-end tests

### HTTP Transport (Next)

- `language/mcp_server_generator.py` - HTTP server generator (needs update)
- `promptware/client.py` - Client library (TO BUILD)
- `examples/demo/user_service.pw` - Demo service (TO CREATE)
- `examples/demo/order_service.pw` - Demo service (TO CREATE)

### Documentation

- `docs/execution-plan-v2.md` - Master roadmap (NEW)
- `docs/http-transport-integration.md` - Implementation plan (NEW)
- `docs/SESSION_SUMMARY.md` - All session notes (UPDATED)

---

## When Working on HTTP Transport

### Remember:

1. **HTTP server generator exists** but outdated
   - Audit it first before starting fresh
   - It has FastAPI boilerplate already
   - Needs tool integration added

2. **Client library is critical**
   - This is NEW code, no existing impl
   - Design API carefully (will be public)
   - Python first, then Node.js

3. **Same protocol, different transport**
   - stdio = pipes (stdin/stdout)
   - HTTP = network (POST requests)
   - JSON-RPC in both cases
   - MCP spec is the same

4. **Test cross-language early**
   - Don't assume Python → Node "just works"
   - JSON serialization differences
   - Type coercion issues
   - Test with real services

---

## Competing Products

### We're Competing With:

- **gRPC** - Google's protobuf-based RPC
- **Thrift** - Facebook's cross-language RPC
- **Cap'n Proto** - Protobuf successor

### Our Advantages:

1. **Simpler DSL** - .pw is easier than protobuf
2. **AI-native** - Prompts built into protocol
3. **MCP standard** - Growing ecosystem
4. **Tool integration** - Services can use tools
5. **Dual transport** - stdio + HTTP from same definition

---

## Quick Start for HTTP Work

### Step 1: Audit Existing HTTP Generator

```bash
# Check current implementation
cat language/mcp_server_generator.py

# Look for:
# - FastAPI setup
# - MCP endpoint handlers
# - Verb routing logic
# - What's missing vs stdio server
```

### Step 2: Design Client API

```python
# Target API for Python client
from promptware.client import call_verb, MCPClient

# Simple function call
result = await call_verb(
    service="user-service",
    verb="user.get@v1",
    params={"user_id": "123"},
    address="http://localhost:23450"
)

# Reusable client instance
client = MCPClient("http://user-service:23450")
result = await client.call("user.get@v1", {"user_id": "123"})
```

### Step 3: Build Demo Services

```bash
# Create two .pw files
examples/demo/user_service.pw
examples/demo/order_service.pw

# Order service calls user service
# Proves service-to-service communication
```

---

## Common Pitfalls to Avoid

1. **Don't confuse stdio and HTTP**
   - They're different transports
   - Don't mix code between them
   - Keep them separate but parallel

2. **Don't ignore existing HTTP code**
   - We have 80% of HTTP server done
   - Audit before rewriting
   - Reuse what works

3. **Don't skip client library design**
   - API will be public
   - Hard to change later
   - Get it right first time

4. **Don't forget cross-language**
   - Python → Python is easy
   - Python → Node is the real test
   - Plan for it from start

---

## Success Criteria

### Wave 2 (stdio) - ✅ DONE

- [x] 11 working IDE tools
- [x] Real tool execution
- [x] AI integration
- [x] Comprehensive tests
- [x] Production-ready

### Wave 3 (HTTP) - Target

- [ ] Two Python services communicating
- [ ] Python → Node cross-language call
- [ ] Client library in 2+ languages
- [ ] Working demo video
- [ ] Documentation complete

---

**Last Updated:** 2025-09-30 Session 10  
**Read This First:** Before working on HTTP transport  
**Then Read:** `docs/CLAUDE.md` for general guidelines
