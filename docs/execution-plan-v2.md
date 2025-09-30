# Promptware Execution Plan v2

**Vision**: Universal polyglot service protocol for AI-native systems

Promptware is a DSL for defining typed service interfaces (MCP verbs) that work across any programming language. Write `.pw` once, deploy as IDE tools (stdio) or microservices (HTTP).

**The Core Idea:**
```pw
service user-service
lang python

expose user.get@v1:
  params: user_id string
  returns: name string, email string
```

Generates:
- **stdio MCP server** → IDE tool (Cursor, VSCode, etc.)
- **HTTP MCP server** → Microservice backend
- **Client libraries** → Call from any language

Same interface definition. Multiple deployment modes.

---

## Current Status (2025-09-30)

### ✅ Completed

**Wave 1 - Foundation**
- DSL parser, interpreter, runners
- Tool adapters (190 adapters across 5 languages)

**Wave 2 - stdio Transport (IDE Integration)**
- ✅ Native stdio MCP server (`language/mcp_stdio_server.py`)
- ✅ Tool registry and executor
- ✅ Dual-mode architecture (IDE-integrated + standalone AI)
- ✅ 11 working MCP tools in Cursor
- ✅ Real tool execution with http, storage, etc.
- ✅ Comprehensive test coverage (33+ tests)
- ✅ JSON-RPC protocol over stdio
- ✅ Automatic tool loading from schemas

**Results:**
- stdio transport fully working
- Production-ready IDE integration
- Tested with Cursor (50k+ potential users)

### 🔨 In Progress

**Wave 3 - HTTP Transport (Microservices)**
- HTTP MCP server generator exists but not integrated
- Need: MCP client library for service-to-service calls
- Need: Integration tests for HTTP transport
- Need: 2-service coordination demo

---

## The Two Transports (Same Protocol)

### stdio Transport - IDE Integration
**Status:** ✅ Complete and Working

**Use case:** IDE tools, CLI applications, local integrations

**How it works:**
```
Cursor IDE → starts subprocess → mcp_stdio_server.py
          → writes JSON-RPC to stdin
          → reads JSON-RPC from stdout
```

**Example:**
```bash
# Cursor starts this automatically
python3 mcp_stdio_server.py examples/code_reviewer.pw

# Cursor writes to stdin:
{"jsonrpc":"2.0","id":1,"method":"tools/list"}

# Server writes to stdout:
{"jsonrpc":"2.0","id":1,"result":{"tools":[...]}}
```

**Advantages:**
- ✅ No network ports needed
- ✅ Automatic lifecycle management
- ✅ Simple security (local only)
- ✅ Direct process communication

**Limitations:**
- ❌ Single client per server
- ❌ Local machine only
- ❌ Can't scale horizontally

### HTTP Transport - Microservices
**Status:** 🔨 In Progress (80% complete)

**Use case:** Backend services, distributed systems, polyglot architectures

**How it works:**
```
Service A (Python) → HTTP POST → Service B (Node.js)
                   → JSON-RPC over HTTP
                   → Response
```

**Example:**
```python
# Service A calls Service B
response = await call_verb(
    service="user-service",
    verb="user.get@v1",
    params={"user_id": "123"},
    address="http://localhost:23450"
)
```

**Advantages:**
- ✅ Network-accessible
- ✅ Multiple concurrent clients
- ✅ Horizontal scaling
- ✅ Standard microservice patterns

**Limitations:**
- ❌ Need port management
- ❌ Network security considerations
- ❌ Manual lifecycle management

---

## Wave 3 - HTTP Transport Implementation

**Goal:** Enable service-to-service communication via HTTP MCP

### Week 1-2: HTTP Server Integration

| Task | Description | Status | Effort |
| --- | --- | --- | --- |
| Review existing generator | Audit `mcp_server_generator.py` | ☐ | 2h |
| Update HTTP server template | Ensure MCP JSON-RPC compliance | ☐ | 4h |
| Add tool execution to HTTP | Port stdio tool integration to HTTP | ☐ | 6h |
| Generate working HTTP server | `promptware generate --http service.pw` | ☐ | 4h |
| Test HTTP server manually | Start server, call with curl | ☐ | 2h |

**Deliverable:** Working HTTP MCP server generation

### Week 3: MCP Client Library (Python)

| Task | Description | Status | Effort |
| --- | --- | --- | --- |
| Design client API | `call_verb(service, verb, params)` | ☐ | 2h |
| Implement HTTP transport | JSON-RPC over HTTP POST | ☐ | 6h |
| Add error handling | Timeouts, retries, connection errors | ☐ | 4h |
| Add service discovery | Hardcoded addresses for v1 | ☐ | 2h |
| Write client tests | Unit + integration tests | ☐ | 4h |

**Deliverable:** Python client library for calling MCP verbs

### Week 4: Two-Service Demo

| Task | Description | Status | Effort |
| --- | --- | --- | --- |
| Service A: User service (Python) | Expose user.create@v1, user.get@v1 | ☐ | 4h |
| Service B: Order service (Python) | Calls user service, exposes order.create@v1 | ☐ | 4h |
| Integration test | Service B → Service A communication | ☐ | 4h |
| Error scenarios | Test timeouts, service down, invalid params | ☐ | 4h |
| Documentation | How to build/deploy two services | ☐ | 4h |

**Deliverable:** Working Python ↔ Python service communication

### Week 5-6: Cross-Language Support

| Task | Description | Status | Effort |
| --- | --- | --- | --- |
| Node.js HTTP server generator | Express-based MCP server | ☐ | 8h |
| Node.js MCP client | TypeScript client library | ☐ | 8h |
| Python → Node demo | Python service calls Node service | ☐ | 6h |
| Go HTTP server generator | net/http MCP server | ☐ | 8h |
| Go MCP client | Go client library | ☐ | 8h |
| 3-language demo | Python ↔ Node ↔ Go | ☐ | 8h |

**Deliverable:** Full polyglot service communication

---

## Architecture Overview

### Unified .pw Definition

```pw
service user-service
lang python
port 23450

# Optional: AI processing
llm anthropic claude-3-5-sonnet-20241022
prompt_template: You are a user management expert...

# Optional: Tool integration
tools:
  - http
  - storage

expose user.create@v1:
  params:
    email string
    name string
  returns:
    user_id string
    created_at string
  prompt_template: Create user with email {email}

expose user.get@v1:
  params:
    user_id string
  returns:
    email string
    name string
    created_at string
```

### Deployment Options

**Option 1: IDE Tool (stdio)**
```bash
# Add to .cursor/mcp.json
promptware mcp-config

# Cursor automatically starts:
python3 mcp_stdio_server.py user-service.pw
```

**Option 2: Microservice (HTTP)**
```bash
# Generate HTTP server
promptware generate --http user-service.pw

# Start service
python3 generated/user_service_server.py
# Listening on http://localhost:23450
```

**Option 3: Both**
```bash
# Same .pw file, different transports
promptware serve --stdio user-service.pw    # For IDE
promptware serve --http user-service.pw     # For backend
```

### Service-to-Service Communication

```python
# Service A (Python)
from promptware.client import call_verb

async def create_order(user_id: str, items: list):
    # Call user-service to validate user
    user = await call_verb(
        service="user-service",
        verb="user.get@v1",
        params={"user_id": user_id},
        address="http://user-service:23450"
    )

    if not user["ok"]:
        raise ValueError("User not found")

    # Create order...
    return {"order_id": "abc123", "user": user["data"]}
```

---

## Wave 4 - Production Features

**Goal:** Make HTTP transport production-ready

### Service Discovery

| Feature | Description | Status |
| --- | --- | --- |
| Static addresses | Hardcoded service URLs | ✅ (v1) |
| Environment variables | SERVICE_URL from env | ☐ |
| Consul integration | Service registry | ☐ |
| Kubernetes services | K8s DNS discovery | ☐ |

### Observability

| Feature | Description | Status |
| --- | --- | --- |
| Structured logging | JSON logs for all calls | ☐ |
| Distributed tracing | OpenTelemetry integration | ☐ |
| Metrics | Prometheus metrics | ☐ |
| Health checks | /health endpoint | ☐ |

### Security

| Feature | Description | Status |
| --- | --- | --- |
| API key auth | Simple token-based auth | ☐ |
| mTLS | Certificate-based mutual auth | ☐ |
| Rate limiting | Per-service rate limits | ☐ |
| Input validation | JSON schema validation | ☐ |

### Reliability

| Feature | Description | Status |
| --- | --- | --- |
| Retries | Automatic retry with backoff | ☐ |
| Circuit breakers | Fail fast when service down | ☐ |
| Timeouts | Configurable request timeouts | ☐ |
| Load balancing | Round-robin, least-conn | ☐ |

---

## Success Metrics

### Wave 2 (stdio) - ✅ ACHIEVED
- [x] 10+ working IDE tools
- [x] Real tool execution (not mocks)
- [x] AI integration working
- [x] Comprehensive test coverage
- [x] Production-ready for IDE use

### Wave 3 (HTTP) - Target: 6 weeks
- [ ] Two Python services communicating
- [ ] Python → Node cross-language call
- [ ] Client library in 2+ languages
- [ ] Working demo video
- [ ] Documentation complete

### Wave 4 (Production) - Target: 12 weeks
- [ ] 5+ production deployments
- [ ] Multi-language demo (Python/Node/Go)
- [ ] Service discovery working
- [ ] Observability stack integrated
- [ ] Security features enabled

---

## Market Positioning

### We Compete With:

**gRPC**
- Theirs: Protobuf-based, Google-backed, mature
- Ours: Simpler DSL, AI-native, MCP standard, tool integration

**Thrift**
- Theirs: Facebook-backed, battle-tested
- Ours: Modern, AI-first, better DX

**REST APIs**
- Theirs: Universal, simple, no special tools
- Ours: Typed contracts, code generation, better reliability

**GraphQL**
- Theirs: Flexible queries, frontend-focused
- Ours: Backend-focused, simpler, RPC not query

### Our Unique Value Props:

1. **AI-native**: Built-in prompt templates and LLM integration
2. **Dual transport**: Same .pw works for IDE tools AND microservices
3. **Tool integration**: Services can use tools (http, storage, etc.)
4. **Simple DSL**: Easier than protobuf, clearer than REST
5. **MCP standard**: Leverage growing Anthropic ecosystem

---

## Roadmap Summary

**✅ Q4 2024**
- stdio transport complete
- IDE integration working
- 11 example tools
- Comprehensive tests

**🔨 Q1 2025 (Current)**
- HTTP transport complete
- Python client library
- 2-service demo
- Cross-language (Python/Node)

**📋 Q2 2025**
- Production features (discovery, observability, security)
- Go/Rust client libraries
- 5+ language support
- Documentation complete

**🔮 Q3 2025**
- Service mesh integration
- Agent marketplace
- Enterprise features
- Scale to 100+ services

---

## Quick Start Guide

### For IDE Tools (stdio)

```bash
# 1. Define your tool
cat > my_tool.pw <<EOF
tool my-tool
expose do.something@v1:
  params: input string
  returns: output string
EOF

# 2. Generate config
promptware mcp-config

# 3. Restart IDE
# Tool automatically available in Cursor/VSCode
```

### For Microservices (HTTP)

```bash
# 1. Define your service
cat > user_service.pw <<EOF
service user-service
lang python
port 23450

expose user.get@v1:
  params: user_id string
  returns: name string, email string
EOF

# 2. Generate server
promptware generate --http user_service.pw

# 3. Start service
python3 generated/user_service_server.py

# 4. Call from another service
from promptware.client import call_verb
result = await call_verb(
    "user-service",
    "user.get@v1",
    {"user_id": "123"},
    "http://localhost:23450"
)
```

---

## Open Questions

1. **Service naming**: Should services auto-register with DNS/consul, or manual config?
2. **Versioning**: How do we handle breaking changes in verb definitions?
3. **Schemas**: Should we generate OpenAPI/Swagger docs from .pw files?
4. **Monitoring**: Which observability stack to standardize on?
5. **Deployment**: Docker, K8s, both, or deployment-agnostic?

---

## Next Session Priorities

1. **Immediate (This week):**
   - Review HTTP server generator
   - Design Python client library API
   - Create 2-service demo plan

2. **Short-term (Next 2 weeks):**
   - Implement Python client library
   - Build working Python ↔ Python demo
   - Write integration tests

3. **Medium-term (Next month):**
   - Add Node.js support
   - Cross-language demo
   - Production features planning

---

**Last Updated**: 2025-09-30
**Status**: Wave 2 complete (stdio), Wave 3 in progress (HTTP)
**Branch**: CC45
**Team**: Ready for Wave 3 kickoff
