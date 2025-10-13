# Phase 4: Compiler Integration - Implementation Plan

**Status**: Ready to Start
**Prerequisites**: ✅ All complete (MCP server, training data, trained CharCNN)
**Estimated Time**: 2-4 hours
**Expected Outcome**: End-to-end PW → Multi-language compilation with CharCNN operation lookup

---

## Objective

Integrate the trained CharCNN model into the Promptware compiler to enable:
```
PW source code → CharCNN operation lookup → MCP query → Target language code
```

---

## Phase 4 Tasks

### Task 1: Create Inference API (30 minutes)

**File**: `ml/inference.py`

**Purpose**: Provide simple API for looking up operations from PW code snippets.

**Implementation**:
```python
def lookup_operation(pw_code: str, top_k: int = 3) -> List[Tuple[str, float]]:
    """
    Predict operation from PW code snippet.

    Args:
        pw_code: PW code snippet (e.g., "file.read(path)")
        top_k: Number of predictions to return

    Returns:
        List of (operation_id, confidence) tuples
    """
    # Load model (cached)
    # Tokenize code
    # Run CharCNN
    # Return top-k predictions
    pass
```

**Test**:
- Test all 84 operations from validation set
- Verify <1ms inference time
- Check memory usage

---

### Task 2: Integrate into Parser (1 hour)

**File**: `dsl/pw_parser.py`

**Changes Needed**:

1. **Add CharCNN import**:
   ```python
   from ml.inference import lookup_operation
   ```

2. **Enhance operation parsing**:
   ```python
   def parse_operation_call(self, code_snippet: str):
       # Old: Manual pattern matching
       # New: CharCNN lookup
       predictions = lookup_operation(code_snippet, top_k=3)
       operation_id = predictions[0][0]  # Top prediction

       # Continue with existing IR generation
       return IRCall(operation=operation_id, ...)
   ```

3. **Add fallback**:
   ```python
   if confidence < 0.3:
       # Fall back to manual parsing
       operation_id = self._manual_parse_operation(code_snippet)
   ```

**Test**:
- Parse file with multiple operations
- Verify correct operation_id resolution
- Test fallback for unknown patterns

---

### Task 3: Connect to MCP Server (30 minutes)

**File**: `dsl/pw_compiler.py` (new or update existing)

**Implementation**:
```python
def compile_pw_to_target(pw_code: str, target_language: str) -> str:
    """
    End-to-end compilation with CharCNN + MCP.

    1. Parse PW code into IR
    2. For each operation call:
       - Use CharCNN to identify operation_id
       - Query MCP server for implementation
       - Substitute into IR
    3. Generate target language code
    """
    # Parse to IR
    ir = parse(pw_code)

    # Resolve operations via MCP
    for node in ir.walk():
        if isinstance(node, IRCall):
            # CharCNN lookup
            operation_id = lookup_operation(node.raw_code)[0][0]

            # MCP query
            impl = mcp_query(operation_id, target_language)

            # Substitute
            node.implementation = impl

    # Generate code
    return generate(ir, target_language)
```

**Test**:
- Compile simple PW program to Python
- Compile same program to JavaScript
- Verify generated code matches expected output

---

### Task 4: Build End-to-End Pipeline (1 hour)

**Create Test Programs**:

1. **Hello World** (`examples/hello.pw`):
   ```pw
   function main() {
       print("Hello, Promptware!")
   }
   ```

2. **File I/O** (`examples/file_io.pw`):
   ```pw
   function process_file(input_path: string, output_path: string) {
       let content = file.read(input_path)
       let upper = str.upper(content)
       file.write(output_path, upper)
   }
   ```

3. **HTTP API** (`examples/http_api.pw`):
   ```pw
   function fetch_users() {
       let data = http.get_json("https://api.example.com/users")
       for user in data {
           print(user.name)
       }
   }
   ```

4. **Data Processing** (`examples/csv_process.pw`):
   ```pw
   function process_csv(path: string) {
       let lines = file.read_lines(path)
       let results = []

       for line in lines {
           let parts = str.split(line, ",")
           if len(parts) >= 3 {
               results.push(parts[2])
           }
       }

       return str.join(results, "\n")
   }
   ```

**Test Each Program**:
- Compile to Python → Execute → Verify output
- Compile to JavaScript → Execute → Verify output
- Compile to Rust → Verify syntax (execution optional)

---

### Task 5: Performance Benchmarks (30 minutes)

**Create**: `benchmarks/phase4_performance.py`

**Measure**:
1. **Operation Lookup Speed**:
   - Single operation: <1ms
   - Batch of 100 operations: <50ms

2. **Full Compilation Speed**:
   - 10-line program: <10ms
   - 100-line program: <100ms
   - 1000-line program: <1s

3. **Memory Usage**:
   - Model loading: <10MB
   - Inference: <5MB additional
   - Total: <15MB

4. **Accuracy**:
   - All 84 operations: 100% correct
   - Complex code: >95% correct

**Output**: Performance report with metrics vs. targets

---

## Success Criteria

### ✅ Functional Requirements
- [ ] CharCNN correctly identifies operations from PW code
- [ ] MCP server returns valid implementations
- [ ] Generated code compiles and runs
- [ ] All 4 test programs work in Python
- [ ] All 4 test programs work in JavaScript

### ✅ Performance Requirements
- [ ] Operation lookup: <1ms per operation
- [ ] Full compilation: <100ms for 100-line program
- [ ] Memory usage: <15MB total
- [ ] 100% accuracy on training set operations

### ✅ Code Quality
- [ ] Inference API has docstrings and type hints
- [ ] Parser integration is clean (no spaghetti code)
- [ ] MCP connection handles errors gracefully
- [ ] Test coverage: >90% for new code

### ✅ Documentation
- [ ] PHASE4_COMPLETE.md with results
- [ ] Updated Current_Work.md
- [ ] API documentation for inference.py
- [ ] Example programs with comments

---

## Potential Challenges & Solutions

### Challenge 1: Parser Integration Complexity
**Problem**: Existing parser may not easily support CharCNN lookup.
**Solution**: Create thin wrapper layer that intercepts operation calls before IR generation.

### Challenge 2: MCP Server Communication
**Problem**: Network latency for MCP queries.
**Solution**: Use local MCP server (no network), cache responses.

### Challenge 3: Operation Disambiguation
**Problem**: CharCNN might predict wrong operation for ambiguous code.
**Solution**: Use top-3 predictions + context to resolve ambiguity.

### Challenge 4: Generated Code Quality
**Problem**: MCP-generated code might not match existing generator quality.
**Solution**: Compare output with existing generators, adjust MCP templates.

---

## Timeline

| Task | Time | Dependencies |
|------|------|--------------|
| 1. Inference API | 30 min | Trained model |
| 2. Parser Integration | 1 hour | Inference API |
| 3. MCP Connection | 30 min | Parser integration |
| 4. End-to-End Pipeline | 1 hour | MCP connection |
| 5. Performance Benchmarks | 30 min | Pipeline complete |
| **Total** | **3.5 hours** | - |

Add 1 hour buffer for debugging → **4.5 hours total**

---

## Next Session Plan

**When user is ready to proceed:**

1. I'll create `ml/inference.py` with the lookup API
2. Test inference on all 84 operations
3. Integrate into parser (modify `dsl/pw_parser.py`)
4. Connect to MCP server
5. Build test programs
6. Run benchmarks
7. Document results in PHASE4_COMPLETE.md

**Deliverables**:
- Fully integrated compiler with CharCNN + MCP
- 4 working example programs
- Performance benchmark results
- Complete documentation

**Expected Result**:
```bash
$ pwenv compile examples/hello.pw --target python
$ python examples/hello.py
Hello, Promptware!
```

---

## Architecture Diagram

```
┌─────────────────┐
│   PW Source     │
│   Code (.pw)    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   PW Parser     │
│ (dsl/pw_parser) │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   CharCNN       │  ← NEW: Operation lookup
│  (ml/inference) │
└────────┬────────┘
         │ operation_id
         ▼
┌─────────────────┐
│   MCP Server    │  ← Existing: Get implementation
│ (pw_operations) │
└────────┬────────┘
         │ Python/JS/Rust code
         ▼
┌─────────────────┐
│  Code Generator │
│   (language/)   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Target Code    │
│ (.py/.js/.rs)   │
└─────────────────┘
```

---

## Bottom Line

**Phase 4 is the final integration step.**

After Phase 4, Promptware will have:
- ✅ Universal operation syntax (PW)
- ✅ Semantic operation lookup (CharCNN)
- ✅ Multi-language implementations (MCP)
- ✅ End-to-end compilation pipeline

**This is the revolutionary architecture you envisioned.**

Ready to proceed when you are.
