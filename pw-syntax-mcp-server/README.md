# PW Syntax MCP Server

**Universal Code Translation via MCP Tools**

Transform code between any programming language using atomic, composable MCP tools.

## 🚀 What is This?

The PW Syntax MCP Server exposes **76 atomic syntax tools** via the Model Context Protocol, enabling:
- **Agent-to-agent code sharing** - AI agents exchange executable code
- **Universal translation** - Any language → PW → Any language
- **Composable programs** - Build code as trees of MCP tool calls
- **Bidirectional** - Each tool parses AND generates code

## 🎯 Quick Start

```bash
# Install
pip install mcp

# Run server
python server.py

# Use from Claude Desktop or any MCP client
```

## 🛠️ Core Tools (30)

### Module & Imports
- `pw_module` - Define module/file
- `pw_import` - Import dependencies

### Functions
- `pw_function` - Define function
- `pw_parameter` - Function parameter
- `pw_return` - Return statement

### Control Flow
- `pw_if` - If statement
- `pw_for` - For loop
- `pw_while` - While loop
- `pw_assignment` - Variable assignment
- `pw_break` / `pw_continue` - Loop control

### Expressions
- `pw_call` - Function call
- `pw_binary_op` - Binary operations (+, -, *, /, ==, !=, <, >, etc.)
- `pw_literal` - Literal values (string, int, float, bool, null)
- `pw_identifier` - Variable reference
- `pw_array` - Array literal
- `pw_map` - Map/dict literal
- `pw_property_access` - Object.property
- `pw_index` - Array[index]

## 🌍 Translation Tools

### High-Level
- `translate_code(code, from_lang, to_lang)` - One-step translation
- `python_to_pw(code)` - Parse Python → PW tree
- `go_to_pw(code)` - Parse Go → PW tree
- `pw_to_python(tree)` - Generate Python from PW
- `pw_to_go(tree)` - Generate Go from PW

### Supported Languages (v0.1)
- ✅ Python
- ✅ Go
- 🚧 JavaScript/TypeScript (coming soon)
- 🚧 Rust (coming soon)
- 🚧 .NET (coming soon)

## 📖 Example Usage

### Agent A (Python) shares code with Agent B (Go)

```python
# Agent A: Parse Python to PW
python_code = """
def calculate(x, y):
    result = x + y
    return result * 2
"""

pw_tree = await mcp.call_tool("python_to_pw", {"code": python_code})

# Agent A sends pw_tree to Agent B (via any transport)

# Agent B: Generate Go from PW
go_code = await mcp.call_tool("pw_to_go", {"tree": pw_tree})

# Result:
# func Calculate(x int, y int) int {
#     result := x + y
#     return result * 2
# }
```

### Direct Translation

```python
result = await mcp.call_tool("translate_code", {
    "code": "def add(x, y): return x + y",
    "from_lang": "python",
    "to_lang": "go"
})

# Result: "func Add(x int, y int) int { return x + y }"
```

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│                  PW Syntax MCP Server                    │
│                                                          │
│  76 Atomic Syntax Tools:                                │
│    ├─ pw_module, pw_import                              │
│    ├─ pw_function, pw_parameter, pw_return              │
│    ├─ pw_if, pw_for, pw_while                           │
│    ├─ pw_assignment, pw_call                            │
│    ├─ pw_binary_op, pw_literal                          │
│    └─ ... (70 more)                                     │
│                                                          │
│  Translation Services:                                  │
│    ├─ python_to_pw()  → Parse Python → PW tree         │
│    ├─ go_to_pw()      → Parse Go → PW tree             │
│    ├─ pw_to_python()  → Generate Python from PW        │
│    ├─ pw_to_go()      → Generate Go from PW            │
│    └─ translate_code() → Direct language translation    │
└─────────────────────────────────────────────────────────┘
```

## 🎯 Why This is Novel

1. **Syntax-as-MCP-Tools** - First system to expose atomic syntax elements as MCP tools
2. **Agent-Native** - Designed specifically for AI agent code exchange
3. **Composable** - Programs = trees of MCP tool calls
4. **Bidirectional** - Each tool both parses and generates
5. **Universal Bridge** - N languages via 1 protocol (not N²)

## 📊 Comparison

| System | Granularity | MCP Native | Bidirectional | Agent-First |
|--------|-------------|------------|---------------|-------------|
| CrossTL | File-level | ❌ | ✅ | ❌ |
| LLVM IR | Compiler | ❌ | Partial | ❌ |
| Tree-sitter | AST only | ❌ | ❌ | ❌ |
| **PW Syntax** | **Syntax-level** | **✅** | **✅** | **✅** |

## 🔬 Research

Based on research in August-October 2025:
- **CrossTL** (Aug 2025) - Universal IR for GPU languages
- **MCP** (Nov 2024) - Adopted by Anthropic, OpenAI, Google
- **A2A Protocol** (Apr 2025) - Google's agent communication
- **Gap Found**: No one doing syntax-level MCP tools for code translation

See `../RESEARCH_ANALYSIS_SYNTAX_AS_MCP.md` for full analysis.

## 📈 Roadmap

### v0.1 (Current) - MVP
- [x] 30 core syntax tools
- [x] Python ⟷ PW translation
- [x] Go ⟷ PW translation
- [x] High-level `translate_code()` tool

### v0.2 - Language Expansion
- [ ] JavaScript/TypeScript support
- [ ] Rust support
- [ ] Advanced syntax tools (async, decorators, comprehensions)

### v0.3 - Production Ready
- [ ] .NET support
- [ ] Error handling & validation
- [ ] Performance optimization
- [ ] Complete 76-tool catalog

### v1.0 - Ecosystem
- [ ] MCP marketplace listing
- [ ] Claude Desktop integration
- [ ] Agent communication examples
- [ ] API hosting service

## 🤝 Contributing

This is a novel research project. Contributions welcome!

1. Fork the repo
2. Add new tools or languages
3. Submit PR with tests

## 📄 License

MIT

## 🙏 Acknowledgments

Built on the Promptware universal translation IR system.

Inspired by:
- CrossTL (universal IR)
- MCP (agent tooling protocol)
- LLVM (compiler IR design)
- A2A (agent communication)

---

**Ship code between agents, not just data!** 🚀
