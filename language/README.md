# Language Generators and Parsers

Code generators and parsers for all supported target languages.

## Overview

This directory contains the bidirectional translation system that converts between the PW intermediate representation (IR) and 5 target languages: Python, Node.js, Go, Rust, and C#.

## Components

### Forward Generators (IR → Code)

Generate target language code from AL IR:

- **`python_generator_v2.py`** - Python 3.8+ code generation
- **`nodejs_generator_v2.py`** - Node.js/JavaScript code generation
- **`go_generator_v2.py`** - Go 1.18+ code generation
- **`rust_generator_v2.py`** - Rust 2021 edition code generation
- **`dotnet_generator_v2.py`** - C# / .NET 8+ code generation

### Reverse Parsers (Code → IR)

Parse target language code into PW IR:

- **`python_parser_v2.py`** - Python → IR parser
- **`nodejs_parser_v2.py`** - Node.js → IR parser
- **`go_parser_v2.py`** - Go → IR parser (with AST parser)
- **`rust_parser_v2.py`** - Rust → IR parser (with AST parser)
- **`dotnet_parser_v2.py`** - C# → IR parser

### Helper Modules

- **`go_helpers.py`** - Go-specific helper functions
- **`library_mapping.py`** - Cross-language library/function mapping
- **`go_ast_parser`** - Go AST parser binary (compiled from go_ast_parser.go)
- **`go_ast_parser.go`** - Go AST parser source
- **`rust_ast_parser.rs`** - Rust AST parser (using syn crate)
- **`csharp_ast_parser.cs`** - C# AST parser (using Roslyn)
- **`typescript_ast_parser.ts`** - TypeScript AST parser

## Architecture

```
┌──────────────────┐
│  Target Language │
│   Source Code    │
└────────┬─────────┘
         │
    Reverse Parser
         │
         ▼
   ┌──────────┐
   │    IR    │ ← Universal Intermediate Representation
   └──────────┘
         │
    Forward Generator
         │
         ▼
┌──────────────────┐
│  Target Language │
│   Source Code    │
└──────────────────┘
```

## Usage

### Python Generation

```python
from language.python_generator_v2 import PythonGeneratorV2
from dsl.al_parser import parse_al

pw_code = "function add(x: int, y: int) -> int { return x + y; }"
ir = parse_al(pw_code)

generator = PythonGeneratorV2()
python_code = generator.generate(ir)
# Output: def add(x: int, y: int) -> int:\n    return x + y
```

### Python Parsing

```python
from language.python_parser_v2 import PythonParserV2

python_code = "def add(x: int, y: int) -> int:\n    return x + y"

parser = PythonParserV2()
ir = parser.parse_source(python_code)
# Output: IRModule with IRFunction nodes
```

### Go Generation

```python
from language.go_generator_v2 import GoGeneratorV2

generator = GoGeneratorV2()
go_code = generator.generate(ir)
# Output: func add(x int, y int) int {\n    return x + y\n}
```

### Cross-Language Translation

```python
# Python → PW → Go translation
python_code = "def add(x, y): return x + y"

# Step 1: Parse Python
python_parser = PythonParserV2()
ir = python_parser.parse_source(python_code)

# Step 2: Generate Go
go_generator = GoGeneratorV2()
go_code = go_generator.generate(ir)
# Output: Go code equivalent
```

## Testing

```bash
# Test Python generator
python3 tests/test_python_generator_v2.py

# Test Go generator
python3 tests/test_go_generator_v2.py

# Test cross-language translation
python3 tests/integration/test_cross_language.py

# Run all language tests
python3 -m pytest tests/test_*_generator_v2.py -v
```

## Language Features

### Python
- Python 3.8+ syntax
- Type hints
- Async/await
- List comprehensions
- Decorators
- Context managers

### Node.js
- Modern JavaScript (ES6+)
- Async/await
- Arrow functions
- Destructuring
- Template literals

### Go
- Go 1.18+ (generics support)
- Goroutines
- Channels
- Interfaces
- Struct methods

### Rust
- Rust 2021 edition
- Ownership system
- Traits
- Pattern matching
- Result<T, E> for error handling

### C# / .NET
- C# 10+ (.NET 8+)
- Async/await
- LINQ
- Properties
- Extension methods

## Type Mappings

| PW Type | Python | Node.js | Go | Rust | C# |
|---------|--------|---------|-----|------|-----|
| string  | str    | string  | string | String | string |
| int     | int    | number  | int    | i32    | int |
| float   | float  | number  | float64 | f64   | double |
| bool    | bool   | boolean | bool   | bool   | bool |
| array   | List   | Array   | []     | Vec    | List |
| map     | Dict   | Object  | map    | HashMap | Dictionary |
| null    | None   | null    | nil    | None   | null |

## Documentation

- See [docs/ARCHITECTURE.md](../docs/ARCHITECTURE.md) for system design
- See [docs/TYPE_SYSTEM.md](../docs/TYPE_SYSTEM.md) for type mapping details
- See individual generator files for language-specific documentation

## Version

Current: v2.1.0-beta
Status: Production Ready (99% test coverage)
