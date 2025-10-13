# IDE Integration Architecture - CharCNN + MCP Live System

**Goal**: When user types PW code in IDE, it automatically finds operations, provides autocomplete, and enables bidirectional compilation with live execution.

---

## The Complete Picture

```
┌─────────────────────────────────────────────────────────────────┐
│                         USER'S IDE                              │
│  (VSCode/IntelliJ/any editor with LSP support)                 │
└────────────┬────────────────────────────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────────────────────────────┐
│                    PW LANGUAGE SERVER (LSP)                     │
│  - Monitors code changes in real-time                           │
│  - Provides autocomplete, hover info, diagnostics              │
│  - Integrates CharCNN + MCP                                     │
└────────┬────────────────────────────────────────────────────────┘
         │
         ├──────────────┬──────────────┬──────────────┬───────────┐
         │              │              │              │           │
         ▼              ▼              ▼              ▼           ▼
    ┌────────┐    ┌─────────┐   ┌─────────┐   ┌─────────┐  ┌──────┐
    │CharCNN │    │   MCP   │   │ Parser  │   │ Runtime │  │Bidirectional│
    │Lookup  │    │ Server  │   │   IR    │   │Interpreter│ │Transpiler│
    └────────┘    └─────────┘   └─────────┘   └─────────┘  └──────┘
         │              │              │              │           │
         └──────────────┴──────────────┴──────────────┴───────────┘
                                   │
                                   ▼
                    ┌──────────────────────────┐
                    │  LIVE CODE EXECUTION     │
                    │  - Instant feedback      │
                    │  - Inline results        │
                    │  - Interactive debugging │
                    └──────────────────────────┘
```

---

## Phase 4.1: LSP Server with CharCNN Integration

### What User Types
```pw
// User starts typing in IDE:
let content = file.r
//                   ^ cursor here
```

### What Happens (Real-Time)
1. **LSP monitors keystroke** - Detects partial operation `file.r`
2. **CharCNN predicts** - Queries model with context: `"file.r"`
   - Predictions: `file.read` (0.89), `file.rmdir` (0.05), `file.read_lines` (0.04)
3. **Autocomplete appears**:
   ```
   file.read(path: string) -> string
   file.read_lines(path: string) -> List<string>
   file.rmdir(path: string)
   ```
4. **User selects `file.read`**
5. **MCP queried** - LSP asks MCP for operation metadata:
   ```json
   {
     "operation_id": "file.read",
     "signature": "file.read(path: string) -> string",
     "description": "Read entire file contents as string",
     "examples": ["let content = file.read(\"data.txt\")"]
   }
   ```
6. **Hover info shown** - User hovers, sees documentation inline

---

## Architecture Components

### 1. PW Language Server (LSP)

**File**: `lsp/pw_language_server.py` (NEW)

**Capabilities**:
- **Autocomplete** - CharCNN predicts as user types
- **Hover Info** - MCP provides documentation
- **Diagnostics** - Parser validates syntax
- **Go to Definition** - Jump to MCP operation definition
- **Find References** - Show all uses of operation
- **Code Actions** - Quick fixes, refactorings

**Implementation**:
```python
class PWLanguageServer:
    def __init__(self):
        self.charcnn = load_model("ml/charcnn_best.pt")
        self.mcp_client = MCPClient("http://localhost:8080")
        self.parser = PWParser()

    async def on_completion(self, params):
        """User types, provide autocomplete."""
        code_snippet = extract_context(params)

        # CharCNN prediction
        predictions = lookup_operation(code_snippet, top_k=5)

        # Build completion items
        items = []
        for op_id, confidence in predictions:
            # Query MCP for metadata
            metadata = await self.mcp_client.get_operation(op_id)
            items.append(CompletionItem(
                label=op_id,
                detail=metadata['signature'],
                documentation=metadata['description'],
                insertText=generate_snippet(metadata)
            ))

        return items

    async def on_hover(self, params):
        """User hovers, show documentation."""
        operation = identify_operation_at_position(params)
        metadata = await self.mcp_client.get_operation(operation)

        return Hover(
            contents=format_markdown(metadata),
            range=operation_range
        )
```

**Protocol**: Implements [Language Server Protocol](https://microsoft.github.io/language-server-protocol/)

---

### 2. Bidirectional Transpilation

#### Forward: PW → Target Languages (Phase 4)
```
PW code → Parser → IR → CharCNN → MCP → Target code
```

#### Reverse: Target Languages → PW (Phase 5)
```
Python/JS/Rust code → Language parser → Operation detection → MCP reverse lookup → PW code
```

**Example - Python to PW**:
```python
# Input Python:
import requests
response = requests.get("https://api.example.com/users")
data = response.json()

# Detected operations:
# 1. HTTP GET request
# 2. JSON parsing

# MCP reverse lookup:
# requests.get() → http.get()
# response.json() → json.parse()

# Generated PW:
let response = http.get("https://api.example.com/users")
let data = json.parse(response)
```

**Implementation Strategy**:
1. Parse target language code (use language-specific parsers)
2. Extract function calls, imports, idioms
3. Query MCP with reverse mapping: `Python: requests.get()` → `PW: http.get()`
4. Generate equivalent PW code
5. Validate with CharCNN (does generated PW map back to same operation?)

**File**: `transpilers/reverse_transpiler.py` (NEW)

```python
class ReverseTranspiler:
    def __init__(self, source_language: str):
        self.language = source_language
        self.mcp_client = MCPClient()
        self.operation_mappings = load_reverse_mappings()

    def transpile_to_pw(self, source_code: str) -> str:
        """Convert target language code to PW."""
        # Parse source language
        ast = parse_language(source_code, self.language)

        # Detect operations
        operations = []
        for node in ast.walk():
            if is_operation_call(node):
                # Query MCP reverse mapping
                pw_operation = self.mcp_client.reverse_lookup(
                    language=self.language,
                    code=node.to_code()
                )
                operations.append(pw_operation)

        # Generate PW code
        pw_ast = build_pw_ast(operations)
        return generate_pw_code(pw_ast)
```

---

### 3. Live Execution System

**Three modes of "live"**:

#### Mode 1: REPL (Interactive)
```bash
$ pwenv repl
PW> let x = 5 + 3
8
PW> let data = http.get_json("https://api.example.com/users")
[{"id": 1, "name": "Alice"}, {"id": 2, "name": "Bob"}]
PW> print(data[0].name)
Alice
```

**File**: `cli/repl.py` (exists, enhance with CharCNN)

#### Mode 2: Watch Mode (Auto-recompile)
```bash
$ pwenv watch app.pw --target python
Watching app.pw for changes...
Change detected → Recompiling...
✓ Compiled to app.py (23ms)
✓ Running app.py...
Hello from Promptware!
```

**File**: `cli/watch.py` (NEW)

#### Mode 3: IDE Inline Results
```pw
// User types this in IDE:
let x = 10 + 20
// LSP executes in background, shows inline:
//     ⮕ 30

let users = http.get_json("https://api.example.com/users")
// LSP shows inline preview:
//     ⮕ [3 items] {"id": 1, ...}
```

**Implementation**: LSP runs PW runtime interpreter on code blocks, displays results inline

---

## Phase 4 Enhanced: Full IDE Integration

### Task 4.1: Build LSP Server (4-6 hours)

**Subtasks**:
1. **Basic LSP scaffolding** (1 hour)
   - Initialize LSP server with `pygls` library
   - Implement text document sync
   - Handle initialization, shutdown

2. **CharCNN integration** (1 hour)
   - Load trained model on server start
   - Implement completion provider using CharCNN
   - Cache predictions for performance

3. **MCP integration** (1 hour)
   - Connect LSP to MCP server
   - Implement hover provider with MCP metadata
   - Handle MCP errors gracefully

4. **Diagnostics** (1 hour)
   - Integrate PW parser for syntax checking
   - Report errors in real-time
   - Provide quick fixes

5. **Advanced features** (1-2 hours)
   - Go to definition (jump to MCP operation)
   - Find references (show operation usage)
   - Code actions (refactoring, snippets)

6. **VSCode extension** (1 hour)
   - Package LSP server
   - Create VSCode extension manifest
   - Publish to VSCode marketplace

**Files to create**:
- `lsp/pw_language_server.py` (main LSP server)
- `lsp/completion_provider.py` (autocomplete with CharCNN)
- `lsp/hover_provider.py` (documentation from MCP)
- `lsp/diagnostics_provider.py` (syntax checking)
- `vscode-extension/package.json` (VSCode extension)
- `vscode-extension/extension.js` (VSCode client)

---

### Task 4.2: Bidirectional Transpilation (3-4 hours)

**Subtasks**:
1. **Reverse mapping database** (1 hour)
   - Build Python → PW mappings
   - Build JavaScript → PW mappings
   - Store in `reverse_mappings.json`

2. **Python → PW transpiler** (1 hour)
   - Parse Python AST
   - Detect requests.get(), json.loads(), etc.
   - Map to http.get(), json.parse()

3. **JavaScript → PW transpiler** (1 hour)
   - Parse JavaScript AST
   - Detect axios.get(), JSON.parse(), etc.
   - Map to http.get(), json.parse()

4. **Validation** (1 hour)
   - Round-trip test: PW → Python → PW
   - Verify semantic equivalence
   - CharCNN validation

**Files to create**:
- `transpilers/reverse_transpiler.py` (base class)
- `transpilers/python_to_pw.py` (Python → PW)
- `transpilers/js_to_pw.py` (JavaScript → PW)
- `reverse_mappings.json` (operation mappings)

---

### Task 4.3: Live Execution Modes (2-3 hours)

**Subtasks**:
1. **Enhanced REPL** (1 hour)
   - Integrate CharCNN for command completion
   - Add history, multi-line editing
   - Display inline results

2. **Watch mode** (1 hour)
   - File watcher for .pw files
   - Auto-recompile on change
   - Display compilation errors

3. **LSP inline results** (1 hour)
   - Execute code blocks in runtime
   - Display results as inline annotations
   - Handle long-running operations

**Files to create**:
- `cli/repl_enhanced.py` (CharCNN-powered REPL)
- `cli/watch.py` (auto-recompile daemon)
- `lsp/inline_execution.py` (LSP inline results)

---

## Complete User Experience

### Scenario 1: Writing New Code

```pw
// User types in VSCode:
function fetch_weather(city: string) {
    let url = "https://api.weather.com/v1/current?city=" + city
    let response = http.g
    //                    ^ LSP suggests: http.get(), http.get_json()
}
```

**What happens**:
1. User types `http.g`
2. CharCNN predicts: `http.get` (0.91), `http.get_json` (0.87)
3. LSP shows autocomplete with both options
4. User selects `http.get_json`
5. Signature inserted: `http.get_json(url)`
6. User hovers → MCP shows: "Fetch JSON data from URL, parse automatically"

### Scenario 2: Converting Python to PW

```bash
$ pwenv convert weather_api.py --to pw --output weather_api.pw

Analyzing Python code...
Detected operations:
  requests.get() → http.get()
  response.json() → Inline (http.get_json() recommended)
  json.dumps() → json.stringify()

Generated weather_api.pw
```

### Scenario 3: Live Development

**Terminal 1** (Watch mode):
```bash
$ pwenv watch app.pw --target python --execute
[12:34:56] Watching app.pw...
[12:34:58] Changed detected → Recompiling...
[12:34:58] ✓ Compiled (18ms)
[12:34:58] ✓ Running...
Hello from Promptware!
[12:34:58] Watching...
```

**IDE** (Inline results):
```pw
// User saves file
let x = calculate_fibonacci(10)
//     ⮕ 55 (executed in 2ms)

let users = http.get_json("https://api.example.com/users")
//         ⮕ [{"id": 1, "name": "Alice"}, ...] (3 items, 145ms)
```

---

## Implementation Phases

### Phase 4: Compiler Integration (Current)
- ✅ CharCNN trained
- ✅ MCP server ready
- ⏳ Inference API
- ⏳ Parser integration
- ⏳ End-to-end compilation

### Phase 4.1: LSP Server (Next)
- ⏳ Basic LSP scaffolding
- ⏳ CharCNN autocomplete
- ⏳ MCP hover/documentation
- ⏳ Real-time diagnostics
- ⏳ VSCode extension

### Phase 4.2: Bidirectional Transpilation
- ⏳ Reverse mapping database
- ⏳ Python → PW transpiler
- ⏳ JavaScript → PW transpiler
- ⏳ Round-trip validation

### Phase 4.3: Live Execution
- ⏳ Enhanced REPL with CharCNN
- ⏳ Watch mode (auto-recompile)
- ⏳ LSP inline results

---

## Technical Stack

### Language Server
- **Library**: `pygls` (Python Language Server)
- **Protocol**: LSP 3.17
- **IDE Support**: VSCode, IntelliJ, Sublime, Vim, Emacs

### CharCNN Integration
- **Model**: `ml/charcnn_best.pt`
- **Inference**: <1ms per operation
- **Caching**: LRU cache for frequent patterns

### MCP Communication
- **Protocol**: JSON-RPC 2.0
- **Transport**: HTTP (local server)
- **Caching**: Cache operation metadata

### Bidirectional Transpilation
- **Python Parser**: `ast` module
- **JavaScript Parser**: `esprima` or `acorn`
- **PW Generator**: Existing `dsl/pw_parser.py`

---

## File Structure

```
promptware/
├── lsp/                           # Language Server Protocol
│   ├── pw_language_server.py     # Main LSP server
│   ├── completion_provider.py    # Autocomplete (CharCNN)
│   ├── hover_provider.py         # Documentation (MCP)
│   ├── diagnostics_provider.py   # Syntax checking
│   └── inline_execution.py       # Live results
│
├── transpilers/                   # Bidirectional transpilation
│   ├── reverse_transpiler.py     # Base class
│   ├── python_to_pw.py           # Python → PW
│   ├── js_to_pw.py               # JavaScript → PW
│   └── reverse_mappings.json     # Operation mappings
│
├── cli/                           # Command-line tools
│   ├── repl_enhanced.py          # CharCNN-powered REPL
│   └── watch.py                  # Auto-recompile daemon
│
├── vscode-extension/             # VSCode integration
│   ├── package.json              # Extension manifest
│   ├── extension.js              # VSCode client
│   └── README.md                 # Extension docs
│
└── ml/                           # CharCNN (existing)
    ├── inference.py              # Inference API (Phase 4)
    ├── charcnn_best.pt           # Trained model
    └── ...
```

---

## Timeline

| Phase | Tasks | Time | Status |
|-------|-------|------|--------|
| 4.0 | Compiler integration | 3-4 hours | ⏳ Next |
| 4.1 | LSP server | 4-6 hours | ⏳ After 4.0 |
| 4.2 | Bidirectional transpilation | 3-4 hours | ⏳ After 4.1 |
| 4.3 | Live execution modes | 2-3 hours | ⏳ After 4.2 |
| **Total** | **Full IDE integration** | **12-17 hours** | - |

---

## Success Criteria

### Phase 4.0 (Compiler)
- [ ] PW code compiles to target languages
- [ ] CharCNN correctly identifies operations
- [ ] MCP returns valid implementations

### Phase 4.1 (LSP)
- [ ] Autocomplete works in VSCode
- [ ] Hover shows MCP documentation
- [ ] Diagnostics report syntax errors in real-time
- [ ] VSCode extension published

### Phase 4.2 (Bidirectional)
- [ ] Python code converts to PW
- [ ] JavaScript code converts to PW
- [ ] Round-trip works: PW → Python → PW (semantic equivalence)

### Phase 4.3 (Live)
- [ ] REPL executes PW code interactively
- [ ] Watch mode auto-recompiles on changes
- [ ] LSP shows inline results in IDE

---

## Bottom Line

**The cleanest way forward**:

1. **Phase 4.0** (Now): Basic compiler integration
2. **Phase 4.1** (Next): LSP server for IDE integration
3. **Phase 4.2** (Then): Bidirectional transpilation
4. **Phase 4.3** (Finally): Live execution modes

**Result**: Complete developer experience where:
- PW code feels "live" (auto-complete, inline results)
- Bidirectional compilation works seamlessly
- CharCNN + MCP power everything under the hood
- User just writes code, everything else is automatic

**Start with Phase 4.0** (compiler integration) as planned, then expand to LSP/bidirectional/live in subsequent phases.
