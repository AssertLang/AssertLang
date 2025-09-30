# HTTP Server Generator vs stdio Server - Gap Analysis

## Current HTTP Server (`mcp_server_generator.py`)

### ✅ What It Has
1. FastAPI-based HTTP server generation
2. JSON-RPC endpoint at `/mcp`
3. Health check endpoint (`/health`)
4. Verb listing endpoint (`/verbs`)
5. LLM integration (LangChain/Anthropic)
6. Observability (OpenTelemetry, traces, metrics)
7. Temporal workflow support
8. Parameter validation
9. Error handling with MCP error codes

### ❌ What It's Missing (vs stdio)
1. **Tool integration** - No tool registry/executor
2. **Dual-mode architecture** - No IDE vs standalone modes
3. **MCP JSON-RPC protocol** - Uses custom format, not standard MCP
4. **tools/list method** - Missing `initialize` and `tools/list`
5. **tools/call method** - Has `/mcp` but not standard `tools/call`
6. **Tool results structure** - Doesn't return `tool_results` envelope
7. **Metadata tracking** - Missing execution metadata

## stdio Server (`mcp_stdio_server.py`)

### ✅ What It Has
1. Standard MCP JSON-RPC protocol
2. `initialize` method
3. `tools/list` method - Returns tools with JSON schemas
4. `tools/call` method - Executes verbs
5. Tool registry integration
6. Tool executor integration
7. Dual-mode (IDE-integrated vs standalone AI)
8. Metadata in responses (mode, tools_executed, timestamp)
9. Real tool execution (http, storage, etc.)

### Transport Difference
- stdio: Reads/writes JSON-RPC via stdin/stdout
- HTTP: Should read/write JSON-RPC via HTTP POST

## Key Gaps to Fill

### 1. MCP Protocol Compliance
HTTP server needs to implement:
```python
# Currently missing these methods:
POST /mcp with method="initialize"
POST /mcp with method="tools/list"  
POST /mcp with method="tools/call"

# Currently has:
POST /mcp with method="verb.name@v1" (custom format)
```

### 2. Tool Integration
HTTP server needs:
- Import and use `tools.registry.ToolRegistry`
- Import and use `language.tool_executor.ToolExecutor`
- Load agent tools from `.tools` list
- Execute tools before verb execution
- Return tool results in response

### 3. Response Structure
HTTP server returns:
```python
{
    "ok": true,
    "version": "v1",
    "data": {...}  # Direct verb result
}
```

Should return (for MCP compliance):
```python
{
    "jsonrpc": "2.0",
    "id": request_id,
    "result": {
        "input_params": {...},
        "tool_results": {...},  # New!
        "metadata": {...},      # New!
        ...verb returns...
    }
}
```

### 4. Dual-Mode Support
stdio has:
```python
if os.environ.get("ANTHROPIC_API_KEY") and agent.llm:
    # Standalone AI mode
    return AI_processed_result
else:
    # IDE-integrated mode
    return structured_tool_results
```

HTTP server needs same logic.

## Implementation Plan

### Phase 1: Add MCP Protocol Methods (4 hours)

1. Update `_generate_mcp_endpoint()` to handle:
   - `initialize` method
   - `tools/list` method  
   - `tools/call` method (keep existing verb routing)

2. Generate tool schemas from `agent.exposes`

### Phase 2: Add Tool Integration (6 hours)

1. Add imports:
   ```python
   from tools.registry import get_registry
   from language.tool_executor import ToolExecutor
   ```

2. Initialize tool executor in `_generate_app_init()`:
   ```python
   # Tool executor (if agent has tools)
   tool_executor = None
   if agent.tools:
       tool_executor = ToolExecutor(agent.tools)
   ```

3. Update verb handlers to execute tools first:
   ```python
   # Execute tools
   tool_results = {}
   if tool_executor and tool_executor.has_tools():
       tool_results = tool_executor.execute_tools(params)
   
   # Then process with AI or return results
   ```

### Phase 3: Update Response Format (2 hours)

1. Match stdio server response structure:
   ```python
   {
       "jsonrpc": "2.0",
       "id": request_id,
       "result": {
           "input_params": params,
           "tool_results": tool_results,
           "metadata": {
               "mode": "ide_integrated" or "standalone_ai",
               "agent_name": agent.name,
               "timestamp": ...,
               "tools_executed": [...]
           },
           ...verb_returns...
       }
   }
   ```

### Phase 4: Add Dual-Mode Logic (4 hours)

1. Check for API key and prompts
2. Route to IDE mode or standalone mode
3. Match stdio server behavior exactly

## Estimated Effort

- Phase 1: 4 hours
- Phase 2: 6 hours
- Phase 3: 2 hours
- Phase 4: 4 hours
- Testing: 4 hours

**Total: 20 hours (Week 1 of integration plan)**

## Implementation Status

### ✅ Phase 1: MCP Protocol Methods (COMPLETE)

Updated `language/mcp_server_generator.py` to implement:

1. **`initialize` method** - Returns server capabilities
   ```json
   {
     "protocolVersion": "0.1.0",
     "capabilities": {"tools": {}, "prompts": {}},
     "serverInfo": {"name": "agent-name", "version": "v1"}
   }
   ```

2. **`tools/list` method** - Returns tool schemas
   - Generates JSON Schema from .pw expose blocks
   - Includes parameter types, descriptions
   - Converts Promptware types to JSON Schema types

3. **`tools/call` method** - Executes verbs with tool integration
   - Executes tools first via ToolExecutor
   - Routes to appropriate verb handler
   - Returns MCP-compliant response with tool_results and metadata

### ✅ Phase 2: Tool Integration (COMPLETE)

Added tool registry and executor integration:
- Imports `ToolRegistry` and `ToolExecutor`
- Initializes tool executor if agent has tools
- Executes tools before verb handlers
- Returns tool results in response envelope

### ✅ Phase 3: Response Format (COMPLETE)

Updated response structure to match stdio server:
```python
{
    "jsonrpc": "2.0",
    "id": request_id,
    "result": {
        "input_params": {...},
        "tool_results": {...},
        "metadata": {
            "mode": "ide_integrated" or "standalone_ai",
            "agent_name": "...",
            "timestamp": "...",
            "tools_executed": [...]
        },
        ...verb_returns...
    }
}
```

### ✅ Phase 4: Dual-Mode Logic (COMPLETE)

Added mode detection:
- `ide_integrated`: No ANTHROPIC_API_KEY or no LLM configured
- `standalone_ai`: Has API key AND agent.llm configured

### Testing

Created comprehensive test suite (`tests/test_http_server_generation.py`):
- ✅ test_generate_server_with_tools
- ✅ test_mcp_initialize_method
- ✅ test_mcp_tools_list_method
- ✅ test_mcp_tools_call_with_tool_integration
- ✅ test_dual_mode_detection
- ✅ test_health_endpoint

All 6 tests passing.

## Next Steps

Phase 1 complete! HTTP server generator now has feature parity with stdio server.

Next up (Phase 2): Build Python MCP client library for service-to-service communication.
