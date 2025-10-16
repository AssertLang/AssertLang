# Phase 5: Full MCP Architecture Implementation

**Goal**: Replace simplified Python runtime with full MCP multi-language system

**Timeline**: 1.5-2 weeks (44-60 hours)

---

## Architecture Overview

```
┌──────────────┐
│  PW Code     │  #lang python / #lang javascript
│  (.al file)  │  str.split(text, " ")
└──────┬───────┘
       │
       ├─> Parse syntax header → Target language
       │
       ├─> Parse PW code → IR
       │
       ├─> CharCNN identifies operations (100% accuracy)
       │
       ├─> MCP Client queries servers for implementations
       │   ┌────────────────────────────────┐
       │   │ MCP Server (Python)            │
       │   │ - str.split → text.split(delim)│
       │   │ - file.read → Path().read_text│
       │   └────────────────────────────────┘
       │   ┌────────────────────────────────┐
       │   │ MCP Server (JavaScript)        │
       │   │ - str.split → text.split(delim)│
       │   │ - file.read → fs.readFileSync  │
       │   └────────────────────────────────┘
       │
       ├─> Code Generator creates target code
       │   Python:     text.split(" ")
       │   JavaScript: text.split(" ")
       │   Go:         strings.Split(text, " ")
       │
       ├─> Executor runs generated code
       │   subprocess.run(['python3', '-c', code])
       │   subprocess.run(['node', '-e', code])
       │
       └─> Return result
```

---

## Phase 5.1: MCP Protocol Foundation (Week 1, 20-24 hours)

### Day 1-2: MCP Client (6-8 hours)

**File**: `dsl/mcp_client.py`

```python
class MCPClient:
    """Client for communicating with MCP servers"""
    
    def __init__(self, server_configs: dict):
        self.servers = {}  # language → server connection
        for lang, config in server_configs.items():
            self.servers[lang] = self._connect(config['url'])
    
    def get_operation(self, operation_id: str, target_lang: str) -> dict:
        """
        Query MCP server for operation implementation
        
        Returns: {
            "code_template": "text.split(delimiter)",
            "imports": ["from pathlib import Path"],
            "arg_mapping": {"text": 0, "delimiter": 1}
        }
        """
        server = self.servers[target_lang]
        response = self._rpc_call(server, "tools/call", {
            "name": operation_id,
            "target_language": target_lang
        })
        return response['result']
    
    def list_operations(self, target_lang: str) -> list:
        """List all operations available from MCP server"""
        pass
```

**Test**: Create simple MCP server that responds with hardcoded implementations
- Test str.split, file.read, math.sqrt
- Verify JSON-RPC communication works

**Deliverable**: MCP client that can query test server ✅

---

### Day 3-4: Language Header Parser (4-5 hours)

**File**: `dsl/language_header.py`

```python
def parse_header(code: str) -> tuple[str, str]:
    """
    Parse #lang directive from PW code
    
    Examples:
        "#lang python\ncode" → ("python", "code")
        "#lang javascript\ncode" → ("javascript", "code")
        "code" → ("python", "code")  # default
    
    Supports:
        #lang python
        #lang javascript
        #lang go
        #lang rust
    """
    pass
```

**Update**: `dsl/runtime.py` to use language header
```python
def execute(self, code: str):
    target_lang, clean_code = parse_header(code)
    # ... use target_lang for MCP query
```

**Test**: Parse different headers, validate defaults

**Deliverable**: Header parser integrated into runtime ✅

---

### Day 5: Code Generator Foundation (6-8 hours)

**File**: `dsl/code_generator.py`

```python
class CodeGenerator:
    """Generate target language code from IR + MCP implementations"""
    
    def generate(self, ir: IRModule, target_lang: str, 
                 mcp_implementations: dict) -> str:
        """
        Convert IR to executable target code
        
        Args:
            ir: Parsed IR from PW code
            target_lang: "python" | "javascript" | "go" | "rust"
            mcp_implementations: {operation_id: code_template}
        
        Returns:
            Executable code in target language
        """
        if target_lang == "python":
            return PythonGenerator(mcp_implementations).generate(ir)
        elif target_lang == "javascript":
            return JavaScriptGenerator(mcp_implementations).generate(ir)
        # etc
```

**Test**: Generate Python code from simple IR

**Deliverable**: Python code generator working ✅

---

## Phase 5.2: MCP Servers (Week 2, 24-36 hours)

### Day 6-7: Python MCP Server (8-10 hours)

**File**: `servers/python_mcp_server.py`

```python
class PythonMCPServer:
    """MCP server providing Python implementations"""
    
    operations = {
        "str.split": {
            "code": "{{arg0}}.split({{arg1}})",
            "imports": [],
            "returns": "list"
        },
        "file.read": {
            "code": "Path({{arg0}}).read_text()",
            "imports": ["from pathlib import Path"],
            "returns": "str"
        },
        # ... all 84 operations
    }
    
    def handle_tools_call(self, operation_id, args):
        if operation_id in self.operations:
            return self.operations[operation_id]
        raise OperationNotFound(operation_id)
```

**Implement all 84 operations** from CharCNN training data:
- String operations (8)
- File operations (7)
- Array operations (10)
- Math operations (12)
- JSON operations (5)
- HTTP operations (8)
- etc.

**Test**: Query each operation, verify code templates

**Deliverable**: Python MCP server with 84 operations ✅

---

### Day 8-9: JavaScript MCP Server (8-10 hours)

**File**: `servers/javascript_mcp_server.js`

Same structure, JavaScript implementations:
```javascript
{
    "str.split": {
        "code": "{{arg0}}.split({{arg1}})",
        "imports": [],
        "returns": "Array"
    },
    "file.read": {
        "code": "fs.readFileSync({{arg0}}, 'utf8')",
        "imports": ["const fs = require('fs');"],
        "returns": "string"
    }
    // ... all 84 operations
}
```

**Deliverable**: JavaScript MCP server with 84 operations ✅

---

### Day 10: Go MCP Server (8-10 hours)

**File**: `servers/go_mcp_server.go`

Go implementations:
```go
operations := map[string]Operation{
    "str.split": {
        Code: "strings.Split({{arg0}}, {{arg1}})",
        Imports: []string{"strings"},
        Returns: "[]string",
    },
    "file.read": {
        Code: "ioutil.ReadFile({{arg0}})",
        Imports: []string{"io/ioutil"},
        Returns: "[]byte, error",
    },
    // ... 84 operations
}
```

**Deliverable**: Go MCP server with 84 operations ✅

---

## Phase 5.3: Integration (3-4 days, 12-16 hours)

### Day 11: Multi-Language Code Generation (6-8 hours)

**Files**:
- `dsl/generators/python_generator.py`
- `dsl/generators/javascript_generator.py`
- `dsl/generators/go_generator.py`

Each generator converts IR → target code using MCP templates

**Test**: Same PW file generates Python, JS, Go code

**Deliverable**: 3 working code generators ✅

---

### Day 12: Executor Integration (4-5 hours)

**File**: `dsl/executor.py`

```python
class MultiLangExecutor:
    def execute(self, code: str, target: str) -> Any:
        if target == "python":
            result = subprocess.run(
                ['python3', '-c', code],
                capture_output=True, text=True
            )
        elif target == "javascript":
            result = subprocess.run(
                ['node', '-e', code],
                capture_output=True, text=True
            )
        elif target == "go":
            # Write temp file, compile, run
            pass
        
        return parse_result(result.stdout)
```

**Deliverable**: Multi-language executor ✅

---

### Day 13: Full MCP Runtime (2-3 hours)

**File**: `dsl/runtime_mcp.py`

Replace `dsl/runtime.py` with MCP-powered version:

```python
class PWRuntimeMCP:
    def __init__(self, target_lang=None):
        self.mcp_client = MCPClient(load_server_configs())
        self.generator = CodeGenerator()
        self.executor = MultiLangExecutor()
        self.default_lang = target_lang or "python"
    
    def execute(self, code: str):
        # 1. Parse header
        target, clean_code = parse_header(code)
        if not target:
            target = self.default_lang
        
        # 2. Parse to IR
        ir = parse_pw(clean_code)
        
        # 3. Get MCP implementations
        implementations = {}
        for op_id in extract_operations(ir):
            implementations[op_id] = self.mcp_client.get_operation(
                op_id, target
            )
        
        # 4. Generate code
        generated = self.generator.generate(ir, target, implementations)
        
        # 5. Execute
        result = self.executor.execute(generated, target)
        
        return result
```

**Deliverable**: Full MCP runtime replacing simplified version ✅

---

## Phase 5.4: Testing & Polish (2 days, 8-12 hours)

### Day 14: Comprehensive Testing

Test every operation across all languages:
```bash
# Same PW code, different targets
bin/pw run --lang python example.al
bin/pw run --lang javascript example.al
bin/pw run --lang go example.al

# Or via header
#lang python
str.split("hello world", " ")
```

**Test matrix**: 84 operations × 3 languages = 252 tests

**Deliverable**: Test suite with >95% pass rate ✅

---

### Day 15: Documentation & Examples

- Update documentation with multi-language examples
- Create example programs in each language
- Document MCP server API
- Write server creation guide

**Deliverable**: Complete documentation ✅

---

## Timeline Summary

| Phase | Days | Hours | Deliverable |
|-------|------|-------|-------------|
| 5.1: MCP Foundation | 5 | 20-24 | Client, header, generator |
| 5.2: MCP Servers | 5 | 24-36 | Python, JS, Go servers |
| 5.3: Integration | 3 | 12-16 | Full runtime |
| 5.4: Testing | 2 | 8-12 | Production ready |
| **Total** | **15** | **64-88** | **Full MCP system** |

---

## Success Criteria

✅ Single PW file generates Python, JavaScript, Go code
✅ Header syntax `#lang <target>` works
✅ All 84 operations work in all 3 languages
✅ MCP servers queryable via JSON-RPC
✅ CharCNN still provides operation identification
✅ LSP server works with multi-language targets
✅ CLI supports: `pw run --lang python file.pw`
✅ Test coverage >95%

---

## What This Unlocks

1. **Multi-language capability** - Write once, run in any language
2. **Extensibility** - Add new operations via MCP servers
3. **Ecosystem** - Third-party MCP servers for Rust, C++, etc.
4. **Innovation** - The core differentiator of AssertLang

---

## Next Immediate Action

Start Phase 5.1 with MCP client implementation?
