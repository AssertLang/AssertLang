# Phase 4.2 Restart - Implementing The ACTUAL Plan

## What Went Wrong

Phase 4.2 was implemented with a "simplified Python-only runtime" that bypassed the MCP architecture entirely. This defeated the core innovation of AssertLang.

**What was skipped:**
- MCP client/server communication
- Operation discovery via MCP tools/call
- Code generation from MCP templates
- Multi-language support
- Language header syntax (#lang)

## What Phase 4.2 ACTUALLY Requires

From the original plan (PHASE4_2_PLAN.md):

### Runtime Architecture
```
PW Code → Parser → IR → CharCNN (identify) → MCP Query → Code Gen → Execute
```

**Not:**
```
PW Code → Parser → IR → Hardcoded Python calls ❌
```

### Key Components

1. **MCP Client** (dsl/mcp_client.py)
   - Query MCP servers via JSON-RPC
   - tools/call for operation implementations
   - tools/list for discovery

2. **MCP Server** (servers/pw_operations_mcp.py)
   - JSON-RPC server
   - 84 operations with implementations
   - Multi-language templates (Python/JS/Go)

3. **Code Generator** (dsl/code_generator.py)
   - Generate target code from IR + MCP responses
   - Template substitution
   - Import management

4. **Language Header Parser** (dsl/language_header.py)
   - Parse #lang directive
   - Route to correct target

5. **Runtime Integration**
   - Use MCP instead of hardcoded calls
   - Execute generated code
   - Multi-language support

## Implementation Plan

### Step 1: MCP Server (4-6 hours)
Build JSON-RPC server with 84 operations

```python
# servers/pw_operations_mcp.py
operations = {
    "str.split": {
        "python": {"code": "{arg0}.split({arg1})", "imports": []},
        "javascript": {"code": "{arg0}.split({arg1})", "imports": []},
        "go": {"code": "strings.Split({arg0}, {arg1})", "imports": ["strings"]}
    },
    # ... 84 operations
}
```

### Step 2: MCP Client (2-3 hours)
Build client to query MCP server

```python
# dsl/mcp_client.py
class MCPClient:
    def get_operation(self, op_id: str, target: str) -> dict:
        response = self._rpc_call("tools/call", {
            "name": op_id,
            "target_language": target
        })
        return response['result']
```

### Step 3: Code Generator (3-4 hours)
Generate target code from IR + MCP

```python
# dsl/code_generator.py
class CodeGenerator:
    def generate(self, ir: IRModule, target: str, mcp_impl: dict) -> str:
        # Convert IR to target code using MCP templates
        pass
```

### Step 4: Language Header (1-2 hours)
Parse #lang directive

```python
# dsl/language_header.py
def parse_header(code: str) -> tuple[str, str]:
    # "#lang python\ncode" → ("python", "code")
    pass
```

### Step 5: Runtime Integration (2-3 hours)
Replace hardcoded runtime with MCP version

```python
# dsl/runtime_mcp.py
class PWRuntimeMCP:
    def execute(self, code: str):
        target, clean = parse_header(code)
        ir = parse_pw(clean)
        impls = mcp_client.get_operations(ir, target)
        generated = generator.generate(ir, target, impls)
        return executor.execute(generated, target)
```

## Timeline

Total: 12-18 hours (original estimate was 12-16)

- MCP Server: 4-6 hours
- MCP Client: 2-3 hours  
- Code Generator: 3-4 hours
- Language Header: 1-2 hours
- Runtime Integration: 2-3 hours

## Success Criteria

✅ Same PW file generates Python, JavaScript, Go code
✅ #lang header switches target language
✅ MCP server queryable via JSON-RPC
✅ CharCNN identifies operations (already working)
✅ All 30 tested operations work in all 3 languages
✅ Can add new operations to MCP without touching runtime

## Next Action

Start with MCP server implementation (servers/pw_operations_mcp.py)?
