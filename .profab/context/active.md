# Generated: 2026-01-26T21:15:00Z | Device: mac-mini-m4 | Monotonic: 1200000100021

# Active Context: AssertLang

## Current Focus
Production-ready executable contracts language for multi-agent AI coordination.

## The Problem Solved
Agents from different frameworks (CrewAI, LangGraph, AutoGen) can't reliably coordinate because they interpret the same task differently. AssertLang provides deterministic behavior through executable contracts.

## How It Works
1. Define behavior in `.al` files (simple, readable syntax)
2. Transpile to Python, JS, Go, Rust, C# (identical logic)
3. All agents execute the same validation/business logic
4. Deterministic coordination guaranteed

## Key Components
```
├── assertlang/     # Core Python module
├── language/       # Parser, lexer, transpiler
├── dsl/            # DSL definitions
├── examples/       # Usage examples
├── tests/          # 235+ test files
├── tools/          # CLI tools
├── translators/    # Language transpilers
├── stdlib/         # Standard library
└── schemas/        # JSON schemas
```

## Current Status
- **Version**: 0.1.6 (Production for Python)
- **Tests**: 67/67 passing
- **PyPI**: Published and available
- **Multi-language**: JS, TS, Go, Rust, C# transpilation working
- **MCP**: Full integration for agent coordination
