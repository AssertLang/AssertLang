# MCP Architecture Implementation Roadmap

## Current State: Simplified Python Runtime
- Direct Python stdlib calls
- 30 operations hardcoded
- No multi-language support
- Works but not extensible

## Full MCP Vision Requires:

### 1. MCP Client Integration (4-6 hours)
**File:** `dsl/mcp_client.py`

```python
class MCPClient:
    def call_operation(self, server_url: str, operation: str, args: list):
        """
        Call MCP server to get code implementation
        
        Request:
        {
            "jsonrpc": "2.0",
            "method": "tools/call",
            "params": {
                "name": "str.split",
                "arguments": {"text": "hello world", "delimiter": " "}
            }
        }
        
        Response:
        {
            "result": {
                "python": "text.split(delimiter)",
                "javascript": "text.split(delimiter)",
                "go": "strings.Split(text, delimiter)",
                "rust": "text.split(delimiter).collect()"
            }
        }
        """
```

### 2. Code Generator (6-8 hours)
**File:** `dsl/code_generator.py`

```python
class CodeGenerator:
    def generate(self, ir: IRModule, target_lang: str) -> str:
        """
        Convert IR to target language code
        
        IR → Python/JS/Go/Rust code
        
        Uses MCP responses to implement operations
        """
```

### 3. Language Header Parser (2-3 hours)
**File:** `dsl/language_parser.py`

```python
def parse_language_header(code: str) -> tuple[str, str]:
    """
    Parse #lang directive
    
    #lang python    → ("python", code)
    #lang javascript → ("javascript", code)
    #lang go         → ("go", code)
    """
```

### 4. Multi-Language Executor (4-5 hours)
**File:** `dsl/executor.py`

```python
class MultiLangExecutor:
    def execute(self, code: str, target: str):
        """
        Execute generated code in subprocess
        
        Python: subprocess.run(['python3', '-c', generated_code])
        JavaScript: subprocess.run(['node', '-e', generated_code])
        Go: write to file, go build, ./binary
        """
```

### 5. MCP Server Implementations (20+ hours)
**Files:** `servers/python_mcp.py`, `servers/javascript_mcp.py`, etc.

Each server needs:
- JSON-RPC server implementation
- Operation registry for that language
- Code generation for each operation
- Testing for each operation

### 6. Integration (8-10 hours)
**File:** `dsl/runtime_mcp.py`

Replace simplified runtime with full MCP pipeline:
```python
class PWRuntimeMCP:
    def execute_operation(self, op_id, args):
        # 1. Query MCP server for code
        mcp_response = self.mcp_client.call(op_id, args)
        
        # 2. Generate target language code
        code = self.generator.generate(ir, target_lang)
        
        # 3. Execute in subprocess
        result = self.executor.execute(code, target_lang)
        
        return result
```

## Total Effort: 44-52 hours (1-1.5 weeks)

## Comparison:

### Phase 4.2 Simplified Runtime (Current):
- Time: 3 hours
- Capability: Python execution only, 30 ops
- Extensibility: Limited (hardcoded ops)
- Multi-language: No

### Full MCP Architecture (Not Built):
- Time: 44-52 hours
- Capability: Multi-language, unlimited ops
- Extensibility: Full (MCP server ecosystem)
- Multi-language: Yes (Python, JS, Go, Rust)

## Decision Point:

The Phase 4.2 implementation chose speed over architecture:
- Got working runtime in 3 hours vs 50+ hours
- Proved PW syntax works
- Demonstrated 30 operations
- Can iterate on MCP later if needed

Trade-off: Lost multi-language capability and extensibility.
