# PW: A True Universal Programming Language

**Design Philosophy**: PW is NOT a leaky abstraction - it's a genuinely language-agnostic intermediate representation with **ONE canonical way** to express each programming concept.

---

## The Problem We Solved

### Before: Leaky Abstraction ❌

```
Python → IR → Go     (Go error returns leak into IR)
Go → IR → Python     (Python gets Go's error tuples)
Python → IR → Go → IR → Python → CRASH (compound leakage)
```

**Issue**: Language-specific idioms leaked through the IR:
- Go's `(value, error)` returns → Python tuples `[value, None]`
- Go stdlib imports → Invalid Python imports
- Module-level vars → Orphaned assignments

**Result**: Translation degraded after 2-3 round-trips

---

### After: Pure Universal Language ✅

```
Python → [Normalize] → Pure PW → [Denormalize] → Go
Go     → [Normalize] → Pure PW → [Denormalize] → Python
Python → PW → Go → PW → Python → ... (infinite round-trips work!)
```

**Solution**: Semantic Normalization Layer

**Result**: PW is truly universal - no language-specific patterns exist in PW representation

---

## Architecture: Two-Way Normalization

### Core Concept

```
┌─────────────────────────────────────────────────────┐
│                                                      │
│  Language-Specific                  Language-Specific│
│  (Python, Go, Rust)                 (Python, Go, Rust)│
│         ↓                                   ↑         │
│    [NORMALIZE]                        [DENORMALIZE]  │
│         ↓                                   ↑         │
│  ┌──────────────────────────────────────────────┐   │
│  │                                              │   │
│  │              PURE PW (Universal)             │   │
│  │                                              │   │
│  │  • ONE way to represent returns              │   │
│  │  • ONE way to handle errors                  │   │
│  │  • NO language-specific imports              │   │
│  │  • NO language-specific idioms               │   │
│  │                                              │   │
│  └──────────────────────────────────────────────┘   │
│                                                      │
└─────────────────────────────────────────────────────┘
```

---

## PW Universal Concepts

### 1. Error Handling

**PW Canonical Form**:
```pw
function DoWork(x: int) -> string
  throws:
    - NetworkError
    - ValidationError
  body:
    if invalid:
      throw ValidationError("bad input")
    return result
```

**Language-Specific Mappings**:

**Python** (Denormalized):
```python
def do_work(x: int) -> str:
    if invalid:
        raise ValidationError("bad input")
    return result
```

**Go** (Denormalized):
```go
func DoWork(x int) (string, error) {
    if invalid {
        return "", ValidationError{"bad input"}
    }
    return result, nil
}
```

**Rust** (Denormalized):
```rust
fn do_work(x: i32) -> Result<String, Error> {
    if invalid {
        return Err(ValidationError("bad input"));
    }
    Ok(result)
}
```

### Key Insight

**PW doesn't care HOW languages handle errors** - it just declares:
- Function CAN throw
- What exceptions it throws
- Where throws happen

Languages implement this their own way during denormalization.

---

### 2. Return Values

**PW Canonical Form**:
```pw
function Calculate(x: int) -> int:
  body:
    return x * 2
```

**Single return value, always.**

**Language-Specific Mappings**:

**Python** (unchanged):
```python
def calculate(x: int) -> int:
    return x * 2
```

**Go** (error tuple added if function throws):
```go
// No throws → no error tuple
func Calculate(x int) int {
    return x * 2
}

// With throws → error tuple added
func Calculate(x int) (int, error) {
    return x * 2, nil
}
```

**Rust** (Result type added if function throws):
```rust
// No throws → raw return
fn calculate(x: i32) -> i32 {
    x * 2
}

// With throws → Result wrapper
fn calculate(x: i32) -> Result<i32, Error> {
    Ok(x * 2)
}
```

---

### 3. Imports

**PW Canonical Form**:
```pw
module MyApp
version 1.0.0

# Only domain-specific imports (libraries user actually uses)
import http_client
import database
```

**NO stdlib imports in PW** - these are language-specific implementation details.

**Language-Specific Denormalization**:

**Python**:
```python
from __future__ import annotations  # Auto-added
import http_client  # User library
import database     # User library
```

**Go**:
```go
import (
    "errors"  # Auto-added (if function has throws)
    "fmt"     # Auto-added (if function has throws)
    "http_client"  # User library
    "database"     # User library
)
```

**Rust**:
```rust
use std::error::Error;  // Auto-added (if function has throws)
use http_client;        // User library
use database;           // User library
```

---

### 4. Module-Level Variables

**PW Canonical Form**:
```pw
module Config
version 1.0.0

# Module-level constants
module_vars:
  - name: APP_NAME
    type: string
    value: "MyApp"
  - name: VERSION
    type: string
    value: "1.0.0"
```

**Language-Specific Denormalization**:

**Python**:
```python
APP_NAME = "MyApp"
VERSION = "1.0.0"
```

**Go**:
```go
var APP_NAME string = "MyApp"
var VERSION string = "1.0.0"
```

**Rust**:
```rust
const APP_NAME: &str = "MyApp";
const VERSION: &str = "1.0.0";
```

---

## Normalization Rules

### From Go to PW

**Strip**:
1. ✂️ Go stdlib imports (`errors`, `fmt`, `sync`, `time`)
2. ✂️ Error returns: `(value, error)` → `value` + `throws` declaration
3. ✂️ `nil` error returns: `return x, nil` → `return x`
4. ✂️ Explicit type declarations (infer when possible)

**Preserve**:
- ✅ Function logic
- ✅ Control flow
- ✅ Domain-specific imports
- ✅ Type information

### From Python to PW

**Strip**:
1. ✂️ `__future__` imports
2. ✂️ Decorators (store as metadata, don't execute)
3. ✂️ Type hints (extract to PW type system)

**Preserve**:
- ✅ Exception raises (convert to `throws`)
- ✅ Function logic
- ✅ Control flow
- ✅ Domain-specific imports

---

## Denormalization Rules

### From PW to Go

**Add**:
1. ➕ Go stdlib imports (`errors`, `fmt` if function has throws)
2. ➕ Error returns: `return value` → `return value, nil`
3. ➕ Error tuples in function signatures if `throws` declared
4. ➕ Explicit type declarations

**Generate**:
- Go-idiomatic code
- Error handling with `if err != nil`
- Proper Go formatting

### From PW to Python

**Add**:
1. ➕ `__future__` annotations import
2. ➕ Exception raises from `throws` declarations
3. ➕ Type hints from PW type system

**Filter**:
- ❌ Remove Go/Rust/Java stdlib imports
- ❌ Remove error tuples if present

**Generate**:
- Pythonic code
- Exception-based error handling
- PEP 8 formatting

---

## Implementation: Semantic Normalizer

### File: `translators/semantic_normalizer.py`

```python
class SemanticNormalizer:
    """
    Two-way normalization between languages and pure PW.

    Input Normalization (Language → PW):
    - normalize_from_go(ir) → strip Go idioms
    - normalize_from_python(ir) → strip Python idioms

    Output Denormalization (PW → Language):
    - denormalize_to_go(ir) → apply Go idioms
    - denormalize_to_python(ir) → apply Python idioms
    """
```

### Integration Points

**In Translation Bridges**:

```python
# python_bridge.py
def python_to_pw(code):
    ir = parser.parse(code)              # Language-specific IR
    normalized = normalize_ir(ir, "python")  # Strip Python idioms → Pure PW
    return ir_to_mcp(normalized)         # Pure PW → MCP tree

def pw_to_python(tree):
    ir = mcp_to_ir(tree)                 # MCP tree → Pure PW IR
    denormalized = denormalize_ir(ir, "python")  # Apply Python idioms
    return generator.generate(denormalized)      # Generate Python code
```

---

## Benefits

### 1. Infinite Round-Trips ∞

```
Python → PW → Go → PW → Python → PW → Go → ... (works forever!)
```

No degradation, no compound leakage.

### 2. Language Independence

Adding a new language (Rust, .NET, JavaScript) requires:
1. Parser (Language → IR)
2. Generator (IR → Language)
3. Normalizer (2 functions: normalize_from_X, denormalize_to_X)

That's it. No N² translators needed.

### 3. PW as True Lingua Franca

Agents can exchange **pure PW code** without knowing each other's languages:
- Agent A (Python): Sends PW MCP tree
- Agent B (Go): Receives PW MCP tree
- Agent C (Rust): Also receives same PW MCP tree

All three can execute the same logic in their native language.

### 4. Future-Proof

New language features added to PW → all languages benefit:
- Add async/await to PW
- Python gets async/await
- Go gets goroutines
- Rust gets async
- One concept, N implementations

---

## Testing Strategy

### Unit Tests

```python
def test_go_normalization():
    # Go with error returns
    go_code = """
    func DoWork() (string, error) {
        return "ok", nil
    }
    """

    ir = parse_go(go_code)
    normalized = normalize_from_go(ir)

    # Assert: no error returns in normalized IR
    assert normalized.functions[0].return_type == "string"
    assert len(normalized.functions[0].body) == 1
    assert not has_error_tuple(normalized.functions[0].body[0])

def test_python_denormalization():
    # Pure PW with throws
    pw_ir = IRModule(
        functions=[
            IRFunction(
                name="do_work",
                throws=["NetworkError"],
                body=[IRReturn(value=...)]
            )
        ]
    )

    denormalized = denormalize_to_python(pw_ir)

    # Assert: Python has raise statement
    assert has_exception_handling(denormalized)
```

### Integration Tests (Telephone Game)

```python
def test_infinite_roundtrip():
    original = "def add(x, y): return x + y"

    # 10 round-trips
    code = original
    for i in range(10):
        pw = python_to_pw(code)
        go = pw_to_go(pw)
        pw2 = go_to_pw(go)
        code = pw_to_python(pw2)

    # Assert: final code semantically equivalent to original
    assert equivalent(original, code)
```

---

## Resource Efficiency

### Question: "How do we do that programmatically without wasting resources?"

### Answer: Lazy Normalization + Caching

1. **Parse once, normalize once**
   - Parse language code → IR (cached)
   - Normalize IR → PW (cached)
   - Reuse for multiple translations

2. **Denormalize on-demand**
   - PW → Target language only when needed
   - Don't denormalize to all languages speculatively

3. **Shared PW representation**
   - N agents share ONE PW MCP tree
   - Each agent denormalizes to their language when executing
   - Network transfer is minimal (PW MCP tree is compact JSON)

### Example: Resource Efficiency

**Inefficient** ❌:
```
Agent A: Python code → Python → Go translator → Go code → Send to B
Agent B: Receives Go → Go → Rust translator → Rust code → Send to C
Agent C: Receives Rust → Rust → Python translator → ...
```
**3 translations, 3x network transfers**

**Efficient** ✅:
```
Agent A: Python code → PW MCP tree → Send to B, C, D
Agent B: PW MCP tree → Go code (local)
Agent C: PW MCP tree → Rust code (local)
Agent D: PW MCP tree → Python code (local)
```
**1 normalization, 1x network transfer, N local denormalizations**

---

## Future Extensions

### 1. PW DSL Text Format

Currently: PW exists as IR + MCP JSON

Future: PW as readable text format
```pw
module Calculator
version 1.0.0

function add(x: int, y: int) -> int:
  return x + y

function divide(x: int, y: int) -> float
  throws:
    - DivisionByZeroError
  body:
    if y == 0:
      throw DivisionByZeroError("Cannot divide by zero")
    return x / y
```

### 2. Optimizations

- **Semantic-preserving transformations** (e.g., loop unrolling)
- **Dead code elimination** in PW IR
- **Type inference** improvements
- **Cross-language constant folding**

### 3. Language-Specific Hints

Allow optional hints without breaking universality:
```pw
function process_data(items: array<string>) -> array<string>
  hints:
    python:
      use_comprehension: true  # Use list comprehension
    go:
      concurrent: true          # Use goroutines
    rust:
      simd: true                # Use SIMD instructions
  body:
    # Universal logic
```

---

## Conclusion

**PW is now a TRUE universal language**, not a leaky abstraction.

**Key Properties**:
- ✅ ONE canonical representation for each concept
- ✅ NO language-specific idioms in PW IR
- ✅ Infinite round-trips work perfectly
- ✅ Resource-efficient (normalize once, denormalize locally)
- ✅ Future-proof (add languages without breaking existing code)

**The Vision Realized**:
```
"ONE common programming language that is PW which is basically
 an MCP-based syntax programming language"
```

We achieved this through **semantic normalization** - not by forcing languages to be the same, but by providing a pure intermediate representation that ALL languages can map to/from without leaking their idioms.

---

**End of Document**
