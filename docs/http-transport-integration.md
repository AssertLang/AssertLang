# HTTP Transport Integration Plan

**Goal:** Enable service-to-service communication via HTTP MCP transport

**Timeline:** 6 weeks

**Current Status:** stdio transport complete (✅), HTTP transport 80% built but not integrated

---

## Phase 1: Audit & Fix Existing HTTP Server (Week 1)

### What We Have

**File:** `language/mcp_server_generator.py`
- Generates FastAPI-based MCP servers
- Runs on configured port (e.g., 23450)
- Already implements MCP JSON-RPC protocol

**Status:** Built but outdated (before tool integration)

### Tasks

| # | Task | Hours | Dependencies |
| --- | --- | --- | --- |
| 1.1 | Audit `mcp_server_generator.py` | 2 | None |
| 1.2 | Check FastAPI template compliance | 2 | 1.1 |
| 1.3 | Add tool execution to HTTP server | 6 | 1.2, stdio impl |
| 1.4 | Add AI processing to HTTP server | 4 | 1.3 |
| 1.5 | Test HTTP server manually | 2 | 1.4 |
| 1.6 | Write HTTP server unit tests | 4 | 1.5 |

**Total:** 20 hours

### Deliverables

- [ ] Updated `mcp_server_generator.py` with tool integration
- [ ] Working HTTP server generation: `promptware generate --http service.pw`
- [ ] Server runs on specified port
- [ ] Responds to MCP JSON-RPC requests
- [ ] Executes tools correctly
- [ ] AI processing works (with ANTHROPIC_API_KEY)

### Acceptance Criteria

```bash
# Generate HTTP server
promptware generate --http examples/devops_suite/code_reviewer_agent.pw

# Start server
python3 generated/code_reviewer_server.py
# Output: Server listening on http://localhost:23450

# Test with curl
curl -X POST http://localhost:23450/mcp \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "id": 1,
    "method": "tools/list",
    "params": {}
  }'

# Should return: {"jsonrpc":"2.0","id":1,"result":{"tools":[...]}}
```

---

## Phase 2: Python MCP Client Library (Week 2-3)

### What We Need

A Python library for calling MCP verbs over HTTP from other services.

### Design

**File:** `promptware/client.py`

```python
from promptware.client import MCPClient, call_verb

# Option 1: Direct function call (simple)
result = await call_verb(
    service="user-service",
    verb="user.get@v1",
    params={"user_id": "123"},
    address="http://localhost:23450"
)

# Option 2: Client instance (reusable)
client = MCPClient("http://user-service:23450")
result = await client.call("user.get@v1", {"user_id": "123"})

# Option 3: Service registry (future)
from promptware.client import get_service
user_service = await get_service("user-service")
result = await user_service.call("user.get@v1", {"user_id": "123"})
```

### Tasks

| # | Task | Hours | Dependencies |
| --- | --- | --- | --- |
| 2.1 | Design client API | 2 | None |
| 2.2 | Implement MCPClient class | 6 | 2.1 |
| 2.3 | Add HTTP transport (requests/httpx) | 4 | 2.2 |
| 2.4 | Implement call_verb helper | 2 | 2.3 |
| 2.5 | Add error handling | 4 | 2.4 |
| 2.6 | Add retries with backoff | 4 | 2.5 |
| 2.7 | Add timeout configuration | 2 | 2.6 |
| 2.8 | Write client unit tests | 6 | 2.7 |
| 2.9 | Write integration tests | 6 | 2.8, Phase 1 |
| 2.10 | Documentation | 4 | 2.9 |

**Total:** 40 hours

### Error Handling

Client should handle:

```python
from promptware.client import (
    MCPError,
    ConnectionError,
    TimeoutError,
    ServiceUnavailableError,
    InvalidVerbError,
    InvalidParamsError
)

try:
    result = await call_verb(
        service="user-service",
        verb="user.get@v1",
        params={"user_id": "123"},
        address="http://localhost:23450",
        timeout=5.0,  # seconds
        retries=3
    )
except TimeoutError:
    # Service took too long
except ServiceUnavailableError:
    # Service is down or not responding
except InvalidVerbError:
    # Verb doesn't exist
except InvalidParamsError as e:
    # Invalid parameters
    print(e.validation_errors)
```

### Retry Logic

```python
# Exponential backoff: 1s, 2s, 4s
retries=3
backoff_factor=2
initial_delay=1.0

# Only retry on:
# - Connection errors
# - 5xx server errors
# - Timeout errors

# Don't retry on:
# - 4xx client errors (bad params, etc.)
# - Successful responses
```

### Deliverables

- [ ] `promptware/client.py` - Main client library
- [ ] `promptware/exceptions.py` - Error classes
- [ ] `promptware/transport.py` - HTTP transport layer
- [ ] Unit tests: `tests/test_client.py`
- [ ] Integration tests: `tests/test_client_integration.py`
- [ ] Documentation: `docs/client-api.md`

---

## Phase 3: Two-Service Demo (Week 4)

### Demo Architecture

```
┌─────────────────┐         ┌─────────────────┐
│  Order Service  │────────>│  User Service   │
│   (Python)      │  HTTP   │   (Python)      │
│   Port 23451    │<────────│   Port 23450    │
└─────────────────┘         └─────────────────┘
        │
        │ Creates order
        │ Validates user first
        │
        v
   PostgreSQL
```

### Service Definitions

**User Service** (`examples/demo/user_service.pw`):
```pw
service user-service
lang python
port 23450

tools:
  - storage

expose user.create@v1:
  params:
    email string
    name string
  returns:
    user_id string
    created_at string

expose user.get@v1:
  params:
    user_id string
  returns:
    email string
    name string
    created_at string

expose user.list@v1:
  params:
    limit int
    offset int
  returns:
    users array
    total int
```

**Order Service** (`examples/demo/order_service.pw`):
```pw
service order-service
lang python
port 23451

tools:
  - storage
  - http

# Calls user-service
expose order.create@v1:
  params:
    user_id string
    items array
    total_amount float
  returns:
    order_id string
    status string
    user_name string

# Implementation calls user.get@v1 to validate user
```

### Implementation

**Order Service Handler** (generated):
```python
from promptware.client import call_verb

async def handle_order_create(params):
    user_id = params["user_id"]
    items = params["items"]
    total_amount = params["total_amount"]

    # Call user-service to validate user exists
    user = await call_verb(
        service="user-service",
        verb="user.get@v1",
        params={"user_id": user_id},
        address="http://localhost:23450",
        timeout=5.0
    )

    if not user["ok"]:
        return {
            "ok": False,
            "error": {
                "code": "E_USER_NOT_FOUND",
                "message": f"User {user_id} not found"
            }
        }

    # Create order in database
    order_id = await create_order_in_db(user_id, items, total_amount)

    return {
        "ok": True,
        "data": {
            "order_id": order_id,
            "status": "created",
            "user_name": user["data"]["name"]
        }
    }
```

### Tasks

| # | Task | Hours | Dependencies |
| --- | --- | --- | --- |
| 3.1 | Create user_service.pw definition | 1 | None |
| 3.2 | Create order_service.pw definition | 1 | None |
| 3.3 | Generate both HTTP servers | 1 | Phase 1 |
| 3.4 | Implement user service handlers | 4 | 3.3 |
| 3.5 | Implement order service handlers | 4 | 3.4, Phase 2 |
| 3.6 | Add in-memory storage (simple) | 2 | 3.5 |
| 3.7 | Write integration tests | 6 | 3.6 |
| 3.8 | Test error scenarios | 4 | 3.7 |
| 3.9 | Create demo script | 2 | 3.8 |
| 3.10 | Documentation | 3 | 3.9 |

**Total:** 28 hours

### Test Scenarios

```python
# Test 1: Happy path
async def test_create_order_success():
    # Create user
    user = await call_verb("user-service", "user.create@v1", {
        "email": "test@example.com",
        "name": "Test User"
    })
    assert user["ok"] is True

    # Create order
    order = await call_verb("order-service", "order.create@v1", {
        "user_id": user["data"]["user_id"],
        "items": [{"id": "item1", "qty": 2}],
        "total_amount": 100.0
    })
    assert order["ok"] is True
    assert order["data"]["user_name"] == "Test User"

# Test 2: User not found
async def test_create_order_user_not_found():
    order = await call_verb("order-service", "order.create@v1", {
        "user_id": "nonexistent",
        "items": [],
        "total_amount": 0
    })
    assert order["ok"] is False
    assert order["error"]["code"] == "E_USER_NOT_FOUND"

# Test 3: User service down
async def test_create_order_service_unavailable():
    # Stop user-service
    with pytest.raises(ServiceUnavailableError):
        await call_verb("order-service", "order.create@v1", {...})

# Test 4: Timeout
async def test_create_order_timeout():
    # User service slow to respond
    with pytest.raises(TimeoutError):
        await call_verb("order-service", "order.create@v1", {
            ...
        }, timeout=0.1)
```

### Demo Script

```bash
#!/bin/bash
# Start services and demonstrate communication

echo "Starting user-service..."
python3 generated/user_service_server.py &
USER_PID=$!

echo "Starting order-service..."
python3 generated/order_service_server.py &
ORDER_PID=$!

sleep 2

echo "Creating user..."
curl -X POST http://localhost:23450/mcp -d '{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/call",
  "params": {
    "name": "user.create@v1",
    "arguments": {
      "email": "demo@example.com",
      "name": "Demo User"
    }
  }
}'

echo "Creating order (will call user-service internally)..."
curl -X POST http://localhost:23451/mcp -d '{
  "jsonrpc": "2.0",
  "id": 2,
  "method": "tools/call",
  "params": {
    "name": "order.create@v1",
    "arguments": {
      "user_id": "user-123",
      "items": [{"id": "item1", "qty": 2}],
      "total_amount": 100.0
    }
  }
}'

echo "Cleaning up..."
kill $USER_PID $ORDER_PID
```

### Deliverables

- [ ] Working user service (Python HTTP MCP server)
- [ ] Working order service (Python HTTP MCP server)
- [ ] Order service successfully calls user service
- [ ] Integration tests passing
- [ ] Demo script that shows communication
- [ ] Documentation: `docs/two-service-demo.md`

---

## Phase 4: Cross-Language Support (Week 5-6)

### Goal

Demonstrate Python service calling Node.js service.

### Node.js Server Generator

**File:** `language/mcp_server_generator_nodejs.py`

Generate Express-based MCP server:

```javascript
const express = require('express');
const app = express();

app.post('/mcp', async (req, res) => {
  const { jsonrpc, id, method, params } = req.body;

  if (method === 'tools/list') {
    return res.json({
      jsonrpc: '2.0',
      id,
      result: {
        tools: [...]
      }
    });
  }

  if (method === 'tools/call') {
    const { name, arguments: args } = params;
    // Execute verb...
  }
});

app.listen(23450, () => {
  console.log('Server listening on http://localhost:23450');
});
```

### Node.js Client Library

**File:** `promptware-client/index.ts`

```typescript
import { MCPClient } from 'promptware-client';

const client = new MCPClient('http://user-service:23450');

const result = await client.call('user.get@v1', {
  user_id: '123'
});
```

### Tasks

| # | Task | Hours | Dependencies |
| --- | --- | --- | --- |
| 4.1 | Design Node.js server template | 4 | None |
| 4.2 | Implement mcp_server_generator_nodejs.py | 8 | 4.1 |
| 4.3 | Test Node.js server generation | 4 | 4.2 |
| 4.4 | Design Node.js client API | 2 | None |
| 4.5 | Implement Node.js client library | 8 | 4.4 |
| 4.6 | Test Node.js client | 4 | 4.5 |
| 4.7 | Create notification service (Node.js) | 4 | 4.2, 4.5 |
| 4.8 | Python → Node demo | 4 | 4.7, Phase 3 |
| 4.9 | Integration tests | 6 | 4.8 |
| 4.10 | Documentation | 4 | 4.9 |

**Total:** 48 hours

### Three-Service Demo

```
┌────────────┐      ┌────────────┐      ┌──────────────┐
│   Order    │─────>│    User    │      │ Notification │
│  Service   │      │  Service   │<─────│   Service    │
│  (Python)  │      │  (Python)  │      │   (Node.js)  │
└────────────┘      └────────────┘      └──────────────┘
     │                                           ^
     │                                           │
     └───────────────────────────────────────────┘
              Order created → Send notification
```

**Flow:**
1. Order service creates order
2. Order service validates user via user service
3. Order service sends notification via notification service (Node.js)
4. Notification service sends email/webhook

### Deliverables

- [ ] Node.js HTTP server generator
- [ ] Node.js MCP client library
- [ ] Notification service in Node.js
- [ ] Python → Node communication working
- [ ] 3-service demo with tests
- [ ] Documentation: `docs/cross-language-services.md`

---

## Testing Strategy

### Unit Tests

**Server Generation:**
- `tests/test_http_server_generator.py`
- Verify generated code is valid
- Check all verbs are exposed
- Validate tool integration

**Client Library:**
- `tests/test_mcp_client.py`
- Mock HTTP responses
- Test error handling
- Verify retry logic

### Integration Tests

**Single Service:**
- `tests/integration/test_http_server.py`
- Start actual HTTP server
- Call verbs via HTTP
- Verify responses

**Two Services:**
- `tests/integration/test_service_communication.py`
- Start user and order services
- Test service-to-service calls
- Test error scenarios

**Cross-Language:**
- `tests/integration/test_cross_language.py`
- Python → Node communication
- Node → Python communication
- Mixed 3-service flow

### Performance Tests

- Latency: Single verb call <10ms
- Throughput: 1000 requests/sec per service
- Concurrent connections: 100+ simultaneous clients
- Memory: <100MB per service

---

## Documentation

### Files to Create

1. **docs/http-transport.md**
   - What is HTTP transport
   - When to use stdio vs HTTP
   - How to deploy HTTP services

2. **docs/client-api.md**
   - Complete API reference
   - Examples for each language
   - Error handling guide

3. **docs/two-service-demo.md**
   - Step-by-step tutorial
   - Code walkthrough
   - Deployment instructions

4. **docs/cross-language-services.md**
   - Multi-language setup
   - Language-specific quirks
   - Best practices

5. **docs/production-deployment.md**
   - Docker setup
   - Kubernetes manifests
   - Monitoring & logging
   - Security considerations

---

## Success Criteria

### Phase 1 Complete
- ✅ HTTP server generates and runs
- ✅ Responds to MCP requests correctly
- ✅ Tool execution works
- ✅ AI processing works
- ✅ Tests pass

### Phase 2 Complete
- ✅ Python client library published
- ✅ Can call verbs over HTTP
- ✅ Error handling robust
- ✅ Retry logic working
- ✅ Documentation complete

### Phase 3 Complete
- ✅ Two Python services communicating
- ✅ Order service calls user service
- ✅ Integration tests passing
- ✅ Demo script works
- ✅ Documentation complete

### Phase 4 Complete
- ✅ Node.js server generation working
- ✅ Node.js client library published
- ✅ Python ↔ Node communication proven
- ✅ 3-service demo working
- ✅ Cross-language tests passing

---

## Risk Mitigation

### Technical Risks

| Risk | Impact | Mitigation |
| --- | --- | --- |
| HTTP server generator outdated | High | Audit in week 1, fix immediately |
| MCP protocol changes | Medium | Pin to stable MCP version |
| Performance issues | Medium | Benchmark early, optimize if needed |
| Cross-language serialization | High | Use JSON strictly, validate thoroughly |

### Schedule Risks

| Risk | Impact | Mitigation |
| --- | --- | --- |
| Phase 1 takes longer | High | Timebox to 1 week, cut scope if needed |
| Client library complex | Medium | Start simple, add features iteratively |
| Cross-language issues | Medium | Budget extra time in Phase 4 |

---

## Timeline

```
Week 1:  Phase 1 (HTTP server)
Week 2:  Phase 2 (Python client) - Part 1
Week 3:  Phase 2 (Python client) - Part 2
Week 4:  Phase 3 (Two-service demo)
Week 5:  Phase 4 (Node.js support) - Part 1
Week 6:  Phase 4 (Node.js support) - Part 2
```

**Total Duration:** 6 weeks (120 hours)

---

## Next Steps

1. Review this plan with team
2. Get approval on design decisions
3. Start Phase 1: Audit HTTP server generator
4. Set up project tracking (GitHub issues/project board)
5. Schedule weekly check-ins

---

**Created:** 2025-09-30
**Status:** Ready for implementation
**Owner:** Development team
**Est. Completion:** Q1 2025
