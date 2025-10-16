# Cross-Language MCP Servers

AssertLang can generate MCP servers in multiple languages from the same `.al` DSL.

## Supported Languages

| Language | Generator | Example |
|----------|-----------|---------|
| Python | `mcp_server_generator.py` | DevOps suite |
| Node.js | `nodejs_server_generator.py` | Data processor |
| Go | `go_server_generator.py` | Cache service |

## Examples

### Node.js Agent (data-processor)

```al
lang nodejs
agent data-processor
port 23500

expose data.transform@v1:
  params:
    input string
    format string
  returns:
    output string
    status string
```

Generates: **data_processor_server.js** (141 lines)

### Go Agent (cache-service)

```al
lang go
agent cache-service
port 23501

expose cache.get@v1:
  params:
    key string
  returns:
    value string
    found bool
```

Generates: **cache_service_server.go** (187 lines)

## Running Examples

### Node.js Server

```bash
# Install dependencies
npm install express

# Run server
node data_processor_server.js
```

### Go Server

```bash
# Build
go build cache_service_server.go

# Run
./cache_service_server
```

## Calling from Any Language

All servers implement the same MCP protocol:

```bash
curl -X POST http://127.0.0.1:23500/mcp \
  -H "Content-Type: application/json" \
  -d '{
    "method": "data.transform@v1",
    "params": {"input": "test", "format": "json"}
  }'
```

## Code Generation Comparison

| Language | Input (.al) | Output | Ratio |
|----------|-------------|--------|-------|
| Python   | 48 lines    | 326 lines | 6.8x |
| Node.js  | 36 lines    | 141 lines | 3.9x |
| Go       | 48 lines    | 187 lines | 3.9x |

## Features

All generated servers include:

- ✅ MCP JSON-RPC endpoint (`POST /mcp`)
- ✅ Health check (`GET /health`)
- ✅ Verb listing (`GET /verbs`)
- ✅ Parameter validation
- ✅ Error handling
- ✅ Production-ready structure

## Language-Specific Notes

### Python (FastAPI)
- Async/await support
- Type hints
- Pydantic models
- LangChain integration
- OpenTelemetry support
- Temporal workflows

### Node.js (Express)
- Callback-based handlers
- Middleware support
- NPM package ecosystem
- Easy deployment (Vercel, Heroku)

### Go
- Strong typing
- Compiled binary
- Native concurrency
- Fast startup
- Low memory footprint
- Ideal for microservices

## Interoperability

Agents in different languages can communicate via MCP:

```python
from language.mcp_client import MCPClient

# Python client → Node.js agent
nodejs_agent = MCPClient("http://127.0.0.1:23500")
result = nodejs_agent.call("data.transform@v1", {
    "input": "data",
    "format": "json"
})

# Python client → Go agent
go_agent = MCPClient("http://127.0.0.1:23501")
result = go_agent.call("cache.get@v1", {"key": "user:123"})
```

## Adding New Languages

To add support for another language:

1. Create `{lang}_server_generator.py` in `language/`
2. Implement `generate_{lang}_mcp_server(agent: AgentDefinition)`
3. Follow the MCP protocol specification
4. Add tests in `tests/test_{lang}_generator.py`

See existing generators for reference.