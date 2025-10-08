# Correct PW MCP Architecture

## The Misunderstanding

I built the system **backwards**. I included parsers when we shouldn't need them!

---

## What I Built (WRONG)

```
Agent A (Python) → Python code → [Parser] → PW MCP → [Generator] → Go code → Agent B
                     ↑                                                ↑
                 Shouldn't exist!                              Shouldn't exist!
```

**Problem**: Agents send **raw code** (Python/Go), then we parse it. This is the OLD way!

---

## What You Described (CORRECT)

```
Agent A → PW MCP tool calls → Server → Target code (if needed for execution)
          ↑
      Agents speak PW natively!
```

**Agents compose code by calling MCP tools**:

```javascript
// Agent composing a function
await mcp.call("pw_function", {
  name: "calculate",
  params: [
    {tool: "pw_parameter", params: {name: "x", type: "int"}},
    {tool: "pw_parameter", params: {name: "y", type: "int"}}
  ],
  body: [
    {tool: "pw_assignment", params: {
      target: "result",
      value: {tool: "pw_binary_op", params: {op: "+", left: ..., right: ...}}
    }},
    {tool: "pw_return", params: {value: ...}}
  ]
})
```

**No parsing needed** - the MCP call IS already in PW format!

---

## Correct System Architecture

### Layer 1: MCP Protocol (Input)

Agents send MCP tool calls (JSON):
```json
{
  "tool": "pw_if",
  "params": {
    "condition": {"tool": "pw_binary_op", ...},
    "then_body": [...],
    "target_lang": "python"
  }
}
```

### Layer 2: IR Conversion

```
MCP tree → IR node
```

Already implemented in `ir_converter.py`!

### Layer 3: Code Generation

```
IR node → Target language code
```

Use existing generators:
- `PythonGeneratorV2` for Python
- `GoGeneratorV2` for Go
- etc.

### Layer 4: Return to Agent

```json
{
  "result": "if (x > 0):\n    return True\nelse:\n    return False"
}
```

---

## What Agents Actually Do

### Scenario 1: Agent Composes Code

**Agent doesn't write Python** - it composes via MCP:

```python
# Agent makes MCP calls
function_tree = await mcp.call("pw_function", {
    "name": "greet",
    "params": [{"tool": "pw_parameter", ...}],
    "body": [...],
    "target_lang": "python"  # Generate Python when done
})
```

**Server returns**:
```python
def greet(name: str) -> str:
    return "Hello, " + name
```

### Scenario 2: Agent-to-Agent Communication

**Agent A** wants to share logic with **Agent B**:

```
Agent A: Composes PW MCP tree (via tool calls)
Agent A: Sends PW MCP tree to Agent B (JSON message)
Agent B: Receives PW MCP tree
Agent B: Generates code in ITS language (Go/Rust/whatever)
```

**No language conversion needed** - they share PW directly!

---

## What Should Be Removed

### ❌ Remove: Language Parsers

Delete these from the MCP server:
- `PythonParserV2` usage
- `GoParserV2` usage
- All AST parsing

**Why**: Agents don't send raw code - they send MCP calls!

### ❌ Remove: `python_to_pw()` and `go_to_pw()`

These functions assume agents send raw code and we parse it.

**Wrong model**: Agents already speak PW via MCP!

### ✅ Keep: Code Generators

Keep:
- `pw_to_python()`
- `pw_to_go()`
- Generators for all target languages

**Why**: Agents need to **execute** code, so we generate runnable code from PW.

---

## Correct Flow Examples

### Example 1: Single Agent, Multiple Languages

```
Agent: "Generate this PW function in Python AND Go"

Agent → MCP Server:
  pw_function(...) with params, body, etc.

Server → Agent:
  Python version: "def calculate(x): return x * 2"
  Go version: "func Calculate(x int) int { return x * 2 }"
```

### Example 2: Agent Collaboration

```
Agent A (Python specialist):
  - Composes business logic via PW MCP calls
  - Creates PW MCP tree: {"tool": "pw_module", "params": {...}}
  - Sends tree to Agent B

Agent B (Go specialist):
  - Receives PW MCP tree
  - Calls: pw_to_go(tree)
  - Gets Go code to run
```

### Example 3: Code as Data

```
Agent stores code in database:
  - Composes PW MCP tree
  - Stores as JSON
  - Later: Retrieves and generates Python/Go/Rust on demand
```

---

## What the Server ACTUALLY Provides

### High-Level Tools (Keep These)

1. **`pw_to_python(tree)`** - Generate Python from PW
2. **`pw_to_go(tree)`** - Generate Go from PW
3. **`pw_to_rust(tree)`** - Generate Rust from PW (future)

**Input**: PW MCP tree (JSON)
**Output**: Runnable code in target language

### Atomic Syntax Tools (These are the CORE)

These let agents **compose** PW:

1. **`pw_if`** - Create IF statement
2. **`pw_for`** - Create FOR loop
3. **`pw_function`** - Create function
4. **`pw_assignment`** - Create variable assignment
5. ... (30+ tools)

**Input**: Syntax element parameters
**Output**: IR node OR generated code in target language

---

## Revised `server.py` Design

### Current (Wrong)

```python
@app.call_tool()
async def handle_call_tool(name, args):
    if name == "translate_code":
        # Uses parsers! ❌ Wrong!
        pw_tree = python_to_pw(args["code"])
        ...
```

### Correct Design

```python
@app.call_tool()
async def handle_call_tool(name, args):

    # High-level: Generate code from PW tree
    if name == "pw_to_python":
        pw_tree = args["tree"]  # Already in PW format!
        python_code = generate_python(pw_tree)
        return python_code

    # Atomic: Create PW element, optionally generate code
    elif name == "pw_if":
        condition = args["condition"]
        then_body = args["then_body"]
        else_body = args.get("else_body")
        target_lang = args.get("target_lang")

        # Create IR node
        ir_if = IRIf(condition=..., then_body=..., else_body=...)

        # If target_lang specified, generate code
        if target_lang:
            if target_lang == "python":
                return generate_python_if(ir_if)
            elif target_lang == "go":
                return generate_go_if(ir_if)

        # Otherwise return PW MCP representation
        return ir_to_mcp(ir_if)
```

---

## Why This is Better

### 1. No Parser Bugs

Parsers are complex and buggy (we saw this!). **Don't parse - just accept MCP calls!**

### 2. Language-Agnostic from Start

Agents never write language-specific code. They compose **pure PW** via MCP.

### 3. Smaller Surface Area

- No AST parsing
- No language detection
- No syntax error handling
- Just: MCP → IR → Code generation

### 4. True Universal Language

**PW is the primary language.** Python/Go/Rust are just "execution formats" for PW.

```
PW (primary) → Python (for execution)
PW (primary) → Go (for execution)
PW (primary) → Rust (for execution)
```

---

## Migration Plan

### Phase 1: Remove Parsers

1. Delete `python_to_pw()` from `python_bridge.py`
2. Delete `go_to_pw()` from `go_bridge.py`
3. Remove `translate_code` tool (uses parsers)

### Phase 2: Update Documentation

1. Update README: "Agents compose PW via MCP, don't send raw code"
2. Update examples to show MCP tool composition
3. Remove any "parse Python" examples

### Phase 3: Add Composition Examples

Show agents how to **compose** PW:

```python
# Example: Agent composes a function
function_mcp = {
    "tool": "pw_function",
    "params": {
        "name": "calculate",
        "params": [
            {"tool": "pw_parameter", "params": {"name": "x", "type": "int"}}
        ],
        "body": [
            {"tool": "pw_return", "params": {
                "value": {"tool": "pw_binary_op", "params": {
                    "op": "*",
                    "left": {"tool": "pw_identifier", "params": {"name": "x"}},
                    "right": {"tool": "pw_literal", "params": {"value": 2, "type": "int"}}
                }}
            }}
        ]
    }
}

# Generate Python
python_code = await mcp.call("pw_to_python", {"tree": function_mcp})
```

---

## The Correct Vision

**PW is not a translation layer between languages.**

**PW IS the language.** Agents think in PW, compose in PW, share PW.

Languages like Python/Go are just **execution backends** - ways to run PW code on specific platforms.

```
Agent's Mental Model:
  "I'm writing PW. I can run it as Python or Go, but I'm THINKING in PW."

NOT:
  "I'm writing Python, then translating to Go."
```

---

## Your Original Vision (Validated)

You said: **"PW is a programming language. The bridge is the gap between all these different other languages"**

**You were right.** I built it backwards by including parsers.

**Correct model**:
- Agents compose PW (via MCP)
- Server generates Python/Go/Rust (for execution)
- No parsing, no translation, just generation

---

**End of Correct Architecture**
