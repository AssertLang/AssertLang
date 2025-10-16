# AssertLang Architecture: Dual Mode - Runtime + Universal Translator

**Date:** 2025-10-12
**Critical Clarification:** Preserving AssertLang's core value proposition

---

## The Critical Question

> "Will this roadmap keep the key features of multi-language translation with PW as the translation and common language for bridging?"

**Answer:** **YES - and the native runtime actually ENHANCES translation capabilities.**

---

## AssertLang's Unique Value Proposition

**Core Vision:** AssertLang is a **universal translator** - a common language that bridges Python, Rust, Go, TypeScript, and C#.

**Key Capabilities:**
1. **Write once in PW, run anywhere** (transpile to any target language)
2. **Bridge between languages** (call Python from Rust via PW, etc.)
3. **Common IR** (unified representation for all languages)
4. **Multi-language projects** (one codebase, multiple targets)

**This must be preserved.**

---

## Current Architecture (What We Have)

```
PW Source Code
    ↓
Parser (dsl/pw_parser.py)
    ↓
IR (Intermediate Representation)
    ↓
    ├→ Python Generator    → Python code (.py)
    ├→ Rust Generator      → Rust code (.rs)
    ├→ Go Generator        → Go code (.go)
    ├→ TypeScript Generator → TS code (.ts)
    └→ C# Generator        → C# code (.cs)
```

**Status:** All 5 code generators exist and work. This is AssertLang's current strength.

---

## New Architecture (What Session 44 Added)

```
PW Source Code
    ↓
Parser (dsl/pw_parser.py)
    ↓
IR (Intermediate Representation)
    ↓
    ├→ PW Runtime (NEW)    → Direct execution ✅
    ├→ Python Generator    → Python code (.py) ✅
    ├→ Rust Generator      → Rust code (.rs) ✅
    ├→ Go Generator        → Go code (.go) ✅
    ├→ TypeScript Generator → TS code (.ts) ✅
    └→ C# Generator        → C# code (.cs) ✅
```

**Key Point:** The PW Runtime is an **ADDITIONAL** execution path, **NOT a replacement** for code generation.

---

## The Dual Mode: Why Both?

### Mode 1: Direct Execution (PW Runtime)

**Use Case:** Development, scripting, rapid prototyping

**Advantages:**
- ✅ Fast iteration (no compilation step)
- ✅ True language independence
- ✅ REPL for experimentation
- ✅ Debugging in PW itself
- ✅ Single source of truth

**Example:**
```bash
pwenv run script.al  # Executes directly in PW runtime
```

### Mode 2: Transpilation (Code Generators)

**Use Case:** Production deployment, performance-critical code, integration with existing projects

**Advantages:**
- ✅ Native performance (runs as Python/Rust/Go/TS/C#)
- ✅ No PW runtime dependency
- ✅ Integrate with existing codebases
- ✅ Deploy to any environment
- ✅ Platform-specific optimizations

**Example:**
```bash
pwenv build app.al --lang rust -o app.rs  # Generates Rust code
cargo build --release  # Compiles to native binary
```

---

## The Enhanced Vision: Universal Translator 2.0

### What AssertLang Becomes

**Not just a transpiler** (old vision):
```
PW → Python
PW → Rust
PW → Go
PW → TypeScript
PW → C#
```

**A universal bridge with native capabilities** (new vision):
```
                    PW (Common Language)
                    /  |  |  |  \  \
                   /   |  |  |   \  \
                  ↓    ↓  ↓  ↓    ↓  ↓
            Runtime Python Rust Go TS C#
                |      |    |   |  |  |
                └──────┴────┴───┴──┴──┘
                    Interoperability
```

### Key Enhancement: FFI Layer (Phase 5)

**The Big Idea:** AssertLang as a **runtime bridge** between languages.

**Example Scenario:**
```pw
// app.al - Single PW codebase

// Call Python library
@ffi(lang="python", module="requests")
function http_get(url: string) -> Result<string, string>

// Call Rust library
@ffi(lang="rust", crate="serde_json")
function parse_json<T>(json: string) -> Result<T, string>

// PW code that bridges them
function fetch_and_parse(url: string) -> Result<User, string> {
    let response = http_get(url)?;  // Python's requests
    let user = parse_json(response)?;  // Rust's serde_json
    return Ok(user);
}
```

**Result:** Use the best library from any language, all from PW code.

---

## How the Roadmap Supports Universal Translation

### Phase 1: Core Runtime (Months 0-8)

**Bytecode VM enables:**
- ✅ Fast development workflow (no waiting for compilation)
- ✅ Cross-language debugging (debug in PW, not target language)
- ✅ Consistent semantics (no language-specific quirks)

**Code generators remain:**
- ✅ All 5 generators stay operational
- ✅ Improved by better IR validation (VM finds bugs faster)
- ✅ Can test semantics in VM before generating code

### Phase 2: Standard Library (Months 8-14)

**Dual implementation:**
- ✅ Native PW stdlib (for runtime)
- ✅ Generated stdlib (for transpilation)

**Example:**
```pw
// stdlib/http.al
function get(url: string) -> Result<string, string> {
    // Implementation for PW runtime
    @native
    function http_get_native(url: string) -> Result<string, string>;
    return http_get_native(url);
}
```

**Transpilation:**
```python
# Generated Python
import requests

def get(url: str) -> Result[str, str]:
    try:
        response = requests.get(url)
        return Ok(response.text)
    except Exception as e:
        return Err(str(e))
```

```rust
// Generated Rust
use reqwest;

pub fn get(url: &str) -> Result<String, String> {
    reqwest::blocking::get(url)
        .and_then(|r| r.text())
        .map_err(|e| e.to_string())
}
```

### Phase 3: Development Tools (Months 14-20)

**Package Manager supports BOTH modes:**

```toml
# pw.toml
[package]
name = "my-app"
version = "0.1.0"

[dependencies]
# PW packages (for runtime)
stdlib = "1.0.0"

[dependencies.python]
# Python packages (for FFI or transpilation)
requests = "2.31.0"
pandas = "2.0.0"

[dependencies.rust]
# Rust crates (for FFI or transpilation)
serde = { version = "1.0", features = ["derive"] }

[target]
# Generate code for multiple targets
languages = ["python", "rust", "typescript"]
```

**Commands:**
```bash
# Mode 1: Direct execution
pwenv run app.al

# Mode 2: Transpilation
pwenv build app.al --lang python -o output.py
pwenv build app.al --lang rust -o output.rs

# Mode 3: Multi-target
pwenv build app.al --all-targets
# Generates: output.py, output.rs, output.go, output.ts, output.cs
```

### Phase 4: Performance & Polish (Months 20-24)

**Code generator improvements:**
- ✅ Optimized Python output (type hints, idiomatic code)
- ✅ Optimized Rust output (zero-cost abstractions)
- ✅ Optimized Go output (goroutines, channels)
- ✅ Optimized TypeScript output (async/await)
- ✅ Optimized C# output (LINQ, async)

**All validated against VM semantics.**

### Phase 5: FFI & Ecosystem (Months 24-30)

**The Universal Bridge:**

```pw
// bridge.al - The killer feature

// Define FFI interface
@ffi(lang="python", module="tensorflow")
class TensorFlowModel {
    function predict(input: array<float>) -> array<float>;
}

@ffi(lang="rust", crate="image")
function load_image(path: string) -> Result<Image, string>;

// PW code that bridges Python AI with Rust image processing
function classify_image(path: string) -> Result<string, string> {
    let img = load_image(path)?;  // Rust
    let pixels = img.to_array();

    let model = TensorFlowModel();
    let predictions = model.predict(pixels);  // Python

    let label = argmax(predictions);
    return Ok(label);
}
```

**Execution modes:**

1. **Runtime Mode:** PW VM calls Python + Rust via FFI
   - Fast development
   - No compilation
   - Mixed language execution

2. **Transpilation Mode:** Generate Python wrapper
   ```python
   # Generated output.py
   import tensorflow as tf
   # (calls Rust via PyO3 bindings)
   ```

3. **Transpilation Mode:** Generate Rust wrapper
   ```rust
   // Generated output.rs
   use pyo3::prelude::*;
   // (calls Python via PyO3)
   ```

---

## AssertLang's Unique Position

### What Makes This Special

**Other languages:**
- Python: Runs Python only
- Rust: Compiles to native only
- TypeScript: Transpiles to JavaScript only

**AssertLang:**
- ✅ Runs directly (PW runtime)
- ✅ Transpiles to 5 languages (Python, Rust, Go, TS, C#)
- ✅ Calls libraries from any language (FFI)
- ✅ Bridges between languages
- ✅ Single codebase, multiple deployment targets

### The Value Proposition

**For Developers:**
- Write once in PW
- Run anywhere (runtime or transpiled)
- Use best libraries from any language
- No language lock-in

**For Teams:**
- Common language for polyglot projects
- Bridge Python data science with Rust performance
- Unified codebase across microservices (each in different language)

**For Projects:**
- Prototype in PW runtime (fast iteration)
- Transpile to target language (production deployment)
- Mix and match (some services runtime, some transpiled)

---

## Revised Roadmap: Emphasizing Translation

### Phase 1: Core Runtime (Months 0-8)

**Add to deliverables:**
- ✅ All existing code generators remain operational
- ✅ Code generator test suite expanded (100+ tests per language)
- ✅ VM validates code generator semantics
- ✅ Roundtrip testing (PW → Target → PW)

### Phase 2: Standard Library (Months 8-14)

**Add to deliverables:**
- ✅ Stdlib implemented for BOTH runtime and code generation
- ✅ Target-specific optimizations
  - Python: Uses native list, dict
  - Rust: Uses Vec, HashMap
  - Go: Uses slices, maps
  - TypeScript: Uses Array, Map
  - C#: Uses List, Dictionary
- ✅ 500+ stdlib tests run in ALL modes (runtime + 5 transpiled)

### Phase 3: Development Tools (Months 14-20)

**Add to deliverables:**
- ✅ Package manager supports mixed dependencies (PW + Python + Rust + npm + NuGet)
- ✅ `pwenv build --all-targets` generates all 5 languages
- ✅ Multi-target validation (ensure semantic equivalence)

### Phase 4: Performance & Polish (Months 20-24)

**Add to deliverables:**
- ✅ Code generator optimizations
  - Python: Type hints, idiomatic patterns
  - Rust: Zero-cost abstractions, lifetime elision
  - Go: Goroutine patterns, defer usage
  - TypeScript: Async/await, promise chains
  - C#: LINQ, async patterns
- ✅ Benchmarks for ALL targets (not just runtime)
- ✅ Cross-language performance comparison

### Phase 5: FFI & Ecosystem (Months 24-30)

**NEW EMPHASIS: Universal Bridge**

**FFI Implementation (Months 24-26):**
- [ ] **Python FFI** (via ctypes/cffi)
  - Call Python libraries from PW runtime
  - Call PW from Python scripts
  - Bidirectional bridge

- [ ] **Rust FFI** (via C ABI)
  - Call Rust libraries from PW runtime
  - Compile PW runtime with Rust extensions
  - Zero-cost integration

- [ ] **Go FFI** (via cgo)
  - Call Go libraries from PW runtime
  - Goroutine integration

- [ ] **Node.js FFI** (via N-API)
  - Call npm packages from PW runtime
  - JavaScript async/await bridge

- [ ] **C# FFI** (via P/Invoke)
  - Call .NET libraries from PW runtime
  - CLR integration

**Bridge Patterns (Months 26-28):**
- [ ] Python ML + Rust performance
- [ ] Go microservices + TypeScript frontend
- [ ] C# business logic + Python data science
- [ ] Multi-language data pipelines

**Example Projects (Months 28-30):**
- [ ] AI application (Python TensorFlow + Rust image processing)
- [ ] Web service (Go backend + TypeScript API client)
- [ ] Desktop app (C# UI + Python computation)
- [ ] Data pipeline (PW orchestration, multi-language workers)

---

## The Complete Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                     AssertLang (PW)                          │
│                  Universal Translation Layer                 │
└─────────────────────────────────────────────────────────────┘
                              │
                    ┌─────────┴─────────┐
                    ↓                   ↓
            ┌───────────────┐   ┌───────────────┐
            │  PW Runtime   │   │ Code Generator│
            │   (Native)    │   │  (Transpiler) │
            └───────────────┘   └───────────────┘
                    │                   │
                    │                   ├→ Python Generator
                    │                   ├→ Rust Generator
                    │                   ├→ Go Generator
                    │                   ├→ TypeScript Generator
                    │                   └→ C# Generator
                    │
            ┌───────┴────────┐
            ↓                ↓
    ┌──────────────┐  ┌──────────────┐
    │  Direct Exec │  │  FFI Bridge  │
    │  (Fast Dev)  │  │(Multi-Lang)  │
    └──────────────┘  └──────────────┘
            │                │
            │                ├→ Python libs (requests, pandas, tensorflow)
            │                ├→ Rust crates (serde, tokio, image)
            │                ├→ Go packages (goroutines, net/http)
            │                ├→ npm packages (express, react, axios)
            │                └→ NuGet packages (Entity Framework, ML.NET)
            │
            └────────────────┐
                             ↓
                    ┌────────────────┐
                    │  Unified API   │
                    │ (Single Source)│
                    └────────────────┘
```

---

## Key Guarantees

### 1. All Code Generators Remain

**Promise:** The 5 existing code generators (Python, Rust, Go, TypeScript, C#) will:
- ✅ Continue to work
- ✅ Receive improvements and optimizations
- ✅ Be tested alongside the runtime
- ✅ Support all new language features

### 2. Transpilation is First-Class

**Promise:** Transpilation is NOT deprecated, it's enhanced:
- ✅ Multi-target builds (`pwenv build --all-targets`)
- ✅ Target-specific optimizations
- ✅ Semantic equivalence guarantees
- ✅ Cross-language validation

### 3. Universal Bridge is the Goal

**Promise:** The end state is:
- ✅ Write once in PW
- ✅ Run anywhere (runtime or transpiled)
- ✅ Call any library (Python, Rust, Go, TypeScript, C#)
- ✅ Bridge between languages seamlessly

---

## Comparison: Before vs. After

### Before Session 44

```
PW Source
    ↓
Parser → IR
    ↓
    ├→ Python Generator (slow development cycle)
    ├→ Rust Generator   (long compilation)
    ├→ Go Generator     (moderate compilation)
    ├→ TypeScript Generator (transpile + Node.js)
    └→ C# Generator     (compilation required)
```

**Pain points:**
- ❌ No fast iteration (always need to generate + compile)
- ❌ No debugging in PW (debug in target language)
- ❌ No REPL (can't experiment quickly)
- ❌ No semantic validation (bugs found late)

### After Complete Roadmap

```
PW Source
    ↓
Parser → IR
    ↓
    ├→ PW Runtime       (instant execution, REPL, debugging)
    │   └→ FFI Bridge → Call Python/Rust/Go/TS/C# libraries
    │
    ├→ Python Generator (optimized, validated, multi-lib)
    ├→ Rust Generator   (zero-cost, idiomatic, fast)
    ├→ Go Generator     (concurrent, goroutines, fast)
    ├→ TypeScript Generator (async, promises, types)
    └→ C# Generator     (LINQ, async, .NET integration)
```

**Benefits:**
- ✅ Fast iteration (runtime mode)
- ✅ PW-native debugging
- ✅ REPL for experimentation
- ✅ Early semantic validation
- ✅ Production deployment (transpilation)
- ✅ Multi-language libraries (FFI)
- ✅ Best of all worlds

---

## Summary: The Answer is YES

### Your Question
> "Will this keep the key features of multi-language translation with PW as the translation and common language for bridging?"

### The Answer
**YES - and it makes it BETTER.**

**What stays:**
- ✅ All 5 code generators (Python, Rust, Go, TypeScript, C#)
- ✅ Transpilation to native code
- ✅ Multi-language projects
- ✅ Universal translator vision

**What improves:**
- ✅ Fast development (runtime mode)
- ✅ Better debugging (PW-native)
- ✅ Cross-language validation
- ✅ FFI bridge (call any library)
- ✅ Semantic guarantees (VM tests all semantics)

**What's new:**
- ✅ Direct execution (no transpilation needed for dev)
- ✅ REPL (interactive experimentation)
- ✅ Multi-language bridging (FFI layer)
- ✅ Unified package manager (PW + Python + Rust + npm + NuGet)

### The Vision Enhanced

**AssertLang is not becoming "just another language."**

**AssertLang is becoming:**
- A universal translator (original vision) ✅
- A runtime bridge (new capability) ✅
- A development platform (enhanced productivity) ✅
- A polyglot ecosystem (FFI integration) ✅

**The runtime doesn't replace translation - it enables better translation.**

---

**Prepared by:** Lead Agent
**Date:** 2025-10-12
**Status:** Architecture clarified, dual-mode preserved
