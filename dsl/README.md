# PW DSL Core

Core implementation of the PW programming language.

## Overview

This directory contains the foundational components of the AssertLang Domain-Specific Language (PW DSL), including the parser, intermediate representation, type system, and validation.

## Components

### Core Files

- **`ir.py`** - Intermediate Representation (IR) data structures
  - IRModule, IRFunction, IRClass, IRExpression, IRStatement
  - Universal representation used by all generators

- **`pw_parser.py`** - PW → IR Parser
  - Lexer: Tokenizes PW source code
  - Parser: Builds AST from tokens
  - Type Checker: Two-pass type validation
  - Converts PW code to IR

- **`pw_generator.py`** - IR → PW Generator
  - Converts IR back to PW DSL
  - Used for round-trip translation validation

- **`type_system.py`** - Universal Type System
  - Cross-language type mapping
  - Type inference engine
  - Type compatibility rules

- **`validator.py`** - IR Semantic Validator
  - Validates IR structure correctness
  - Ensures semantic consistency

- **`idiom_translator.py`** - Language Idiom Translator
  - Translates language-specific patterns
  - Maps decorators ↔ middleware, etc.

- **`context_analyzer.py`** - Context Analysis
  - Analyzes code context for better translation
  - Infers types from usage patterns

- **`type_inference.py`** - Advanced Type Inference
  - Infers types from default values
  - Propagates types through expressions
  - Array/map element type inference

## Architecture

```
PW Source Code
      ↓
   Lexer (pw_parser.py)
      ↓
   Tokens
      ↓
   Parser (pw_parser.py)
      ↓
   AST
      ↓
Type Checker (pw_parser.py)
      ↓
   IR (ir.py)
      ↓
Validator (validator.py)
      ↓
Code Generators (../language/)
      ↓
Target Language Code
```

## Usage

### Parsing PW Code

```python
from dsl.al_parser import parse_al

pw_code = """
function add(x: int, y: int) -> int {
    return x + y;
}
"""

ir = parse_al(pw_code)
# Returns IRModule with functions, classes, etc.
```

### Generating PW Code

```python
from dsl.al_generator import PWGenerator

generator = PWGenerator()
pw_code = generator.generate(ir)
# Returns PW source code string
```

### Type System

```python
from dsl.type_system import TypeSystem

ts = TypeSystem()
python_type = ts.map_type("string", "python")  # Returns "str"
go_type = ts.map_type("string", "go")          # Returns "string"
```

## Testing

```bash
# Run parser tests
python3 tests/test_pw_parser.py

# Run type system tests
python3 tests/test_type_system.py

# Run IR tests
python3 tests/test_ir.py
```

## Documentation

- See [docs/ARCHITECTURE.md](../docs/ARCHITECTURE.md) for system architecture
- See [docs/PW_DSL_2.0_SPEC.md](../docs/PW_DSL_2.0_SPEC.md) for language specification
- See [docs/TYPE_SYSTEM.md](../docs/TYPE_SYSTEM.md) for type system details

## Version

Current: v2.1.0-beta
