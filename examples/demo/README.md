# Two-Service Demo

Demonstrates service-to-service communication using AssertLang MCP over HTTP.

## Architecture

```
┌─────────────────┐         ┌─────────────────┐
│  Order Service  │────────>│  User Service   │
│   (Python)      │  HTTP   │   (Python)      │
│   Port 23451    │  MCP    │   Port 23450    │
└─────────────────┘         └─────────────────┘
        │                            │
        │ Tools: storage, http       │ Tools: storage
        │                            │
        v                            v
   Creates orders              Manages users
   Validates users first       CRUD operations
```

## Services

### User Service (Port 23450)

Manages user data and provides CRUD operations.

**Verbs:**
- `user.create@v1` - Create a new user
- `user.get@v1` - Get user by ID
- `user.list@v1` - List users with pagination

**Tools:** storage

### Order Service (Port 23451)

Manages orders and validates users by calling the User Service.

**Verbs:**
- `order.create@v1` - Create order (calls user.get@v1 internally)
- `order.get@v1` - Get order by ID
- `order.list@v1` - List orders for a user

**Tools:** storage, http

## Running the Demo

### Quick Start

```bash
cd examples/demo
python3 demo_runner.py
```

This will:
1. Start both services in background processes
2. Wait for services to be ready
3. Run 4 demonstrations:
   - User service operations
   - Order service operations
   - Service-to-service communication
   - Metadata inspection
4. Clean up and stop services

### Manual Start (for development)

**Terminal 1 - User Service:**
```bash
cd examples/demo
python3 user_service_server.py
```

**Terminal 2 - Order Service:**
```bash
cd examples/demo
python3 order_service_server.py
```

**Terminal 3 - Test:**
```bash
# Test user service
curl -X POST http://localhost:23450/mcp \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "id": 1,
    "method": "tools/call",
    "params": {
      "name": "user.get@v1",
      "arguments": {"user_id": "123"}
    }
  }'

# Test order service
curl -X POST http://localhost:23451/mcp \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "id": 2,
    "method": "tools/call",
    "params": {
      "name": "order.create@v1",
      "arguments": {
        "user_id": "123",
        "items": ["item1", "item2"],
        "total_amount": "99.99"
      }
    }
  }'
```

## Using the Python Client

```python
from promptware import MCPClient

# Call user service
with MCPClient("http://localhost:23450") as user_client:
    user = user_client.call("user.get@v1", {"user_id": "123"})
    print(f"User: {user['name']}")

# Call order service (which internally calls user service)
with MCPClient("http://localhost:23451") as order_client:
    order = order_client.call("order.create@v1", {
        "user_id": "123",
        "items": ["laptop", "mouse"],
        "total_amount": "1299.99"
    })
    print(f"Order created: {order['order_id']}")
    print(f"User validated: {order['user_name']}")
```

## What This Demonstrates

### 1. MCP Protocol Compliance

Both services implement the full MCP JSON-RPC protocol:
- `initialize` - Returns server capabilities
- `tools/list` - Lists available verbs with JSON schemas
- `tools/call` - Executes verbs with tool integration

### 2. Tool Integration

Services use tools before executing verbs:
- **storage tool** - Data persistence (simulated)
- **http tool** - Service-to-service calls

### 3. Service-to-Service Communication

Order service calls user service:
1. Client calls `order.create@v1` on order service
2. Order service uses `http` tool to call `user.get@v1` on user service
3. Order service validates user before creating order
4. Response includes both tool results and verb results

### 4. Metadata Tracking

Every response includes metadata:
```json
{
  "metadata": {
    "mode": "ide_integrated",
    "agent_name": "order-service",
    "timestamp": "2025-09-30T...",
    "tools_executed": ["storage", "http"]
  }
}
```

### 5. Code Generation

Both services are generated from `.al` files:
- `user_service.al` → `user_service_server.py`
- `order_service.al` → `order_service_server.py`

Generated code includes:
- FastAPI application
- MCP protocol handlers
- Tool integration
- Parameter validation
- Error handling

## Generated Files

```
examples/demo/
├── user_service.al              # User service definition
├── order_service.al             # Order service definition
├── user_service_server.py       # Generated HTTP server (273 lines)
├── order_service_server.py      # Generated HTTP server (366 lines)
├── demo_runner.py               # Automated demo script
└── README.md                    # This file
```

## Key Features Demonstrated

✅ **Polyglot-Ready** - Same .al definition works for any language
✅ **MCP Protocol** - Standard JSON-RPC 2.0 communication
✅ **Tool Integration** - Real tool execution (storage, http)
✅ **Service Mesh** - Services discover and call each other
✅ **Type Safety** - JSON Schema validation for parameters
✅ **Observability** - Metadata tracking for all operations
✅ **Error Handling** - Proper MCP error codes
✅ **Dual Mode** - IDE-integrated or standalone AI mode

## Next Steps

### Add Real Business Logic

Currently, the generated handlers return mock data. To add real logic:

1. **Implement handler bodies** in generated servers
2. **Use storage tool** to persist to database
3. **Add validation logic** before calling other services
4. **Handle errors** from tool execution

Example:
```python
def handle_order_create_v1(params: Dict[str, Any]) -> Dict[str, Any]:
    # Real implementation
    user_id = params["user_id"]

    # Call user service to validate
    user_response = tool_executor.execute_tools({
        "url": f"http://localhost:23450/mcp",
        "method": "POST",
        "body": {...}
    })

    if not user_response["ok"]:
        return {"error": {"code": "E_USER_NOT_FOUND", "message": "User not found"}}

    # Create order
    order_id = generate_order_id()
    save_to_database(order_id, user_id, params["items"])

    return {
        "order_id": order_id,
        "user_id": user_id,
        "user_name": user_response["data"]["name"],
        "status": "pending"
    }
```

### Cross-Language Services

The demo uses Python for both services, but AssertLang supports:
- Python ↔ Node.js
- Python ↔ Go
- Node.js ↔ Rust
- Any combination!

Same `.al` definition, different runtime.

### Production Features

To make this production-ready, add:
- Service discovery (Consul, etcd)
- Load balancing
- Circuit breakers
- Distributed tracing
- Authentication/authorization
- Rate limiting
- Health checks with dependencies

## Troubleshooting

**Port already in use:**
```bash
# Find and kill processes
lsof -ti:23450,23451 | xargs kill -9
```

**Services not starting:**
- Check that ports 23450 and 23451 are available
- Verify Python dependencies are installed
- Check server logs for errors

**Tool execution fails:**
- Tools return mock data by default
- Check tool registry is loaded correctly
- Verify tool schemas match parameters

## Learn More

- **Client API:** `docs/client-api.md`
- **HTTP Transport:** `docs/http-transport-integration.md`
- **MCP Protocol:** MCP specification
- **More Examples:** `examples/client_examples.py`
