# Phase 4.2 Plan: LSP + Runtime Environment

**Status**: Planning
**Prerequisites**: Phase 4.1 complete (CharCNN validated at 100% accuracy)
**Estimated Time**: 12-16 hours
**Goal**: Ship basic developer tooling and runtime for PW

---

## Executive Summary

Build on the validated CharCNN + MCP architecture to deliver:
1. **LSP Server** - Real-time code intelligence in VS Code
2. **Runtime Environment** - Execute PW code directly (`pw run`)

Both components leverage the existing CharCNN (100% accuracy) and MCP server (84 operations).

---

## Component 1: LSP Server (6-8 hours)

### What We're Building

A Language Server Protocol (LSP) server that provides real-time code intelligence for PW files in VS Code.

### Features

1. **Syntax Diagnostics** (2 hours)
   - Parse PW files in real-time
   - Report parse errors with line/column
   - Show type errors from IR validation

2. **Hover Information** (2 hours)
   - Show operation signatures on hover
   - Query MCP for operation documentation
   - Display CharCNN confidence score

3. **Code Completion** (2 hours)
   - Suggest operations based on partial code
   - Use CharCNN to rank suggestions
   - Include MCP documentation in suggestions

4. **Go-to-Definition** (1-2 hours)
   - Jump to function definitions
   - Jump to variable declarations
   - Jump to imported modules

### Architecture

```
┌─────────────────────┐
│   VS Code Client    │
│  (.vscode/extension)│
└──────────┬──────────┘
           │ LSP Protocol (JSON-RPC)
           ▼
┌─────────────────────┐
│   PW Language       │
│   Server            │
│  (tools/lsp/server.py)
└──────────┬──────────┘
           │
           ├─→ dsl/pw_parser.py (parse errors)
           ├─→ ml/inference.py (operation lookup)
           └─→ MCP server (operation docs)
```

### Files to Create

1. **tools/lsp/server.py** (500 lines)
   - LSP server implementation
   - Handles textDocument/* requests
   - Integrates parser + CharCNN + MCP

2. **tools/lsp/__init__.py** (50 lines)
   - LSP protocol types
   - Request/response handlers

3. **.vscode/extensions/pw-language/client/extension.ts** (200 lines)
   - LSP client for VS Code
   - Connects to Python LSP server

4. **tools/lsp/README.md** (documentation)

### Dependencies

- Python LSP libraries: `pygls` or `python-lsp-server`
- VS Code extension API: `vscode-languageclient`
- Existing: `dsl/pw_parser.py`, `ml/inference.py`, MCP server

### Success Criteria

- ✅ VS Code shows red squiggles for parse errors
- ✅ Hover over operation shows signature + docs
- ✅ Typing "file." shows autocomplete suggestions
- ✅ Go-to-definition works for functions
- ✅ Response time <100ms for all operations

---

## Component 2: Runtime Environment (6-8 hours)

### What We're Building

A Python-based runtime that can execute PW code directly without manual transpilation.

### Features

1. **Direct Execution** (3 hours)
   - Parse PW → IR
   - Execute IR using Python backend
   - Use CharCNN + MCP for operation resolution

2. **CLI Command** (2 hours)
   - `pw run <file>` - Execute PW file
   - `pw run --target python <file>` - Transpile + run
   - `pw run --debug <file>` - Show execution trace

3. **Error Handling** (1 hour)
   - Map errors back to PW source lines
   - Show stack traces with PW file context
   - Graceful fallback when CharCNN uncertain

4. **Performance** (1-2 hours)
   - Cache CharCNN predictions
   - Cache MCP queries
   - Target: <100ms startup, <1ms per operation

### Architecture

```
┌─────────────────────┐
│   pw run command    │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│   Runtime Engine    │
│  (dsl/runtime.py)   │
└──────────┬──────────┘
           │
           ├─→ dsl/pw_parser.py (parse)
           ├─→ ml/inference.py (operation lookup)
           ├─→ MCP server (code generation)
           └─→ Python exec (execute)
```

### Files to Create

1. **dsl/runtime.py** (400 lines)
   - Runtime execution engine
   - IR interpreter
   - Operation resolution via CharCNN + MCP

2. **dsl/executor.py** (300 lines)
   - Execute IR nodes
   - Handle control flow (if/while/for)
   - Manage variable scope

3. **cli/pw_run.py** (200 lines)
   - CLI command implementation
   - Argument parsing
   - Error formatting

4. **bin/pw** (50 lines)
   - Shell script wrapper
   - Invokes Python CLI

### Dependencies

- Existing: `dsl/pw_parser.py`, `dsl/ir.py`
- Existing: `ml/inference.py`
- Existing: MCP server
- Existing: Python generators

### Success Criteria

- ✅ `pw run examples/hello.pw` executes successfully
- ✅ All 7 Phase 4.0 test operations work
- ✅ Error messages show PW source location
- ✅ Execution time <100ms for simple programs
- ✅ CharCNN + MCP integration seamless

---

## Integration Points

### CharCNN + MCP Pipeline (Already Working)

From Phase 4.1:
```python
from ml.inference import lookup_operation
from mcp_client import query_mcp_operation

# 1. Parse code
code = "file.read(path)"

# 2. CharCNN prediction (0.458ms, 100% accuracy)
operation_id, confidence = lookup_operation(code)
# Returns: ("file.read", 0.95)

# 3. MCP query (<100ms)
impl = query_mcp_operation(operation_id, target_lang="python")
# Returns: {code: "Path({path}).read_text()", imports: [...]}

# 4. Generate code
generated = impl['code'].format(path='path')
# Returns: Path(path).read_text()
```

### LSP Integration

```python
# LSP hover request
def handle_hover(position):
    code_snippet = get_code_at_position(position)
    operation_id, confidence = lookup_operation(code_snippet)
    docs = query_mcp_operation(operation_id, info="docs")
    return {
        "signature": docs['signature'],
        "description": docs['description'],
        "confidence": f"{confidence:.0%}"
    }
```

### Runtime Integration

```python
# Runtime execution
def execute_call(call_node):
    # Use CharCNN to identify operation
    operation_id = call_node.operation_id  # From parser

    # Query MCP for implementation
    impl = query_mcp_operation(operation_id, target_lang="python")

    # Execute Python code
    result = eval(impl['code'].format(**args))
    return result
```

---

## Development Plan

### Week 1: LSP Server (6-8 hours)

**Day 1-2: LSP Foundation**
- Set up `tools/lsp/` directory
- Install pygls: `pip install pygls`
- Create basic LSP server (handle initialize, textDocument/didOpen)
- Test with simple echo server

**Day 2-3: Syntax Diagnostics**
- Integrate `dsl/pw_parser.py`
- Parse file on textDocument/didChange
- Return diagnostics for parse errors
- Test in VS Code

**Day 3-4: Hover + Completion**
- Implement textDocument/hover
- Query CharCNN for operation ID
- Query MCP for docs
- Implement textDocument/completion
- Test completion suggestions

**Day 4-5: Go-to-Definition + Polish**
- Implement textDocument/definition
- Add caching for CharCNN/MCP queries
- Performance testing (<100ms response)
- Documentation

### Week 2: Runtime Environment (6-8 hours)

**Day 1-2: Runtime Foundation**
- Create `dsl/runtime.py`
- Implement IR interpreter (basic nodes)
- Execute simple PW programs (hello world)

**Day 2-3: Operation Resolution**
- Integrate CharCNN + MCP in runtime
- Execute file.read, str.split, etc.
- Test with Phase 4.0 demo operations

**Day 3-4: CLI Command**
- Create `cli/pw_run.py`
- Argument parsing (--target, --debug)
- Error formatting (map to PW source)
- Create `bin/pw` shell script

**Day 4-5: Testing + Performance**
- Test all Phase 4.0 operations via runtime
- Performance testing (<100ms startup)
- Error handling edge cases
- Documentation

---

## Testing Plan

### LSP Tests

1. **Syntax Diagnostics**
   ```pw
   let x =  # Parse error (incomplete)
   ```
   - Expect: Red squiggle, error message

2. **Hover Information**
   ```pw
   let content = file.read(path)
              # Hover over 'file.read'
   ```
   - Expect: Signature, docs, confidence

3. **Code Completion**
   ```pw
   let content = file.
                    # Trigger completion
   ```
   - Expect: file.read, file.write, file.exists, ...

4. **Go-to-Definition**
   ```pw
   func foo() { return 42 }
   let x = foo()
        # Click on 'foo'
   ```
   - Expect: Jump to function definition

### Runtime Tests

1. **Hello World**
   ```pw
   print("Hello, world!")
   ```
   ```bash
   $ pw run hello.al
   Hello, world!
   ```

2. **File I/O**
   ```pw
   file.write("test.txt", "Hello")
   let content = file.read("test.txt")
   print(content)
   ```
   ```bash
   $ pw run file_io.al
   Hello
   ```

3. **All Phase 4.0 Operations**
   - Run `pw_compile_demo.py` operations via runtime
   - Expect: Same results as manual transpilation

4. **Error Handling**
   ```pw
   let x = unknown_operation()
   ```
   ```bash
   $ pw run error.al
   Error at line 1, column 9:
   Unknown operation: unknown_operation
   ```

---

## Success Metrics

### LSP Server
- ✅ Response time <100ms (90th percentile)
- ✅ 100% of parse errors caught
- ✅ CharCNN operations have hover docs
- ✅ Completion suggestions ranked by confidence
- ✅ Zero crashes on malformed code

### Runtime
- ✅ Startup time <100ms
- ✅ Operation execution <1ms
- ✅ All Phase 4.0 operations work (7/7)
- ✅ Error messages show PW source location
- ✅ 100% compatibility with CharCNN + MCP

### Developer Experience
- ✅ `pw run` feels instant (<100ms)
- ✅ VS Code feels responsive (<100ms)
- ✅ Error messages are clear and actionable
- ✅ Code completion is helpful and accurate

---

## Risks & Mitigations

### Risk 1: LSP Performance
**Risk**: LSP response time >100ms causes editor lag
**Mitigation**:
- Cache CharCNN predictions (same code → same operation)
- Cache MCP queries (same operation → same docs)
- Use async I/O for MCP queries
- Profile and optimize hot paths

### Risk 2: Runtime Complexity
**Risk**: Full IR interpreter is too complex for 6-8 hours
**Mitigation**:
- Start with transpile-then-execute (Phase 4.0 already works)
- Incrementally add direct execution for common patterns
- Defer complex features (async, classes) to Phase 4.3+

### Risk 3: MCP Server Startup
**Risk**: MCP server startup adds latency
**Mitigation**:
- Start MCP server once, keep alive
- Reuse MCP connection across requests
- Add health check to restart if needed

### Risk 4: CharCNN Confidence
**Risk**: CharCNN uncertain on valid code
**Mitigation**:
- Show confidence score in LSP hover
- Warn user if confidence <70%
- Fallback to signature matching if confidence low

---

## Deliverables

### LSP Server
- `tools/lsp/server.py` - LSP server (500 lines)
- `tools/lsp/__init__.py` - Protocol types (50 lines)
- `.vscode/extensions/pw-language/client/extension.ts` - VS Code client (200 lines)
- `tools/lsp/README.md` - Documentation

### Runtime
- `dsl/runtime.py` - Runtime engine (400 lines)
- `dsl/executor.py` - IR executor (300 lines)
- `cli/pw_run.py` - CLI command (200 lines)
- `bin/pw` - Shell wrapper (50 lines)
- `docs/runtime/USAGE.md` - User documentation

### Testing
- `tests/lsp/test_diagnostics.py` - LSP tests
- `tests/lsp/test_hover.py` - Hover tests
- `tests/lsp/test_completion.py` - Completion tests
- `tests/runtime/test_execution.py` - Runtime tests
- `tests/runtime/test_operations.py` - Operation tests

### Documentation
- `PHASE4_2_COMPLETE.md` - Completion report
- `docs/lsp/ARCHITECTURE.md` - LSP design
- `docs/runtime/ARCHITECTURE.md` - Runtime design
- `docs/getting-started.md` - User tutorial

---

## Post-Phase 4.2

### What's Next: Phase 4.3

Once Phase 4.2 is complete, we'll have:
- ✅ CharCNN (100% accuracy)
- ✅ MCP server (84 operations)
- ✅ LSP server (code intelligence)
- ✅ Runtime (`pw run` command)

Phase 4.3 will focus on:
1. **Standard Library Expansion** (TA1)
   - Add stdlib modules (List, Map, Set, Option, Result)
   - Implement generics support in parser
   - Expand to 200+ operations

2. **Formatter + Linter** (TA3)
   - `pw fmt` - Canonical formatting
   - `pw lint` - Style + best practices
   - Integration with LSP

3. **Testing Framework** (TA3)
   - `pw test` - Unit testing
   - `pw bench` - Benchmarking
   - Test discovery + fixtures

4. **Package Manager** (TA4)
   - `pw install` - Install packages
   - `pw publish` - Publish to registry
   - Dependency resolution

---

## Timeline

**Phase 4.2 Total**: 12-16 hours

- LSP Server: 6-8 hours
- Runtime: 6-8 hours

**Optimistic**: 2 work days (6-8 hours/day)
**Realistic**: 3-4 work days (4-5 hours/day)
**Pessimistic**: 5-7 work days (2-3 hours/day)

---

## How to Start

### Prerequisites Check

```bash
# 1. Verify Phase 4.1 complete
python3 validation/test_large_model.py
# Expect: 100% accuracy

# 2. Check MCP server
python3 -c "from pw_operations_mcp import OperationServer; print('OK')"
# Expect: OK

# 3. Check CharCNN
python3 -c "from ml.inference import lookup_operation; print('OK')"
# Expect: OK
```

### Start LSP Development

```bash
# 1. Create LSP directory
mkdir -p tools/lsp

# 2. Install dependencies
pip install pygls

# 3. Create basic server
# (See LSP development plan above)

# 4. Test in VS Code
code .vscode/extensions/pw-language
# Update package.json to point to LSP server
```

### Start Runtime Development

```bash
# 1. Create runtime module
touch dsl/runtime.py dsl/executor.py

# 2. Test with hello world
echo 'print("Hello")' > test.al
python3 -c "from dsl.runtime import execute; execute('test.pw')"

# 3. Add operation resolution
# (See runtime development plan above)

# 4. Create CLI command
# (See CLI development plan above)
```

---

## Questions Before Starting

1. **Scope**: Is Phase 4.2 scope reasonable (LSP + runtime)? Or should we split into 4.2 (LSP) and 4.3 (runtime)?

2. **Priorities**: Which is more important: LSP (developer experience) or runtime (execution)?

3. **Timeline**: Is 12-16 hours reasonable, or should we allocate more time?

4. **Dependencies**: Should we coordinate with TA2/TA3 agents, or handle this directly?

---

**Status**: Ready to start pending approval

**Blockers**: None - Phase 4.1 complete

**Risk Level**: Low - building on validated CharCNN + MCP architecture
