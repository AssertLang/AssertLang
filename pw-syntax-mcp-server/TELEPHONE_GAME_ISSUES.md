# Telephone Game Test - Issues Discovered

**Test Date**: 2025-10-06
**Test**: Multi-agent code translation round-trips
**Result**: 3/4 tests passed, critical issues found

---

## Test Overview

Simulated "blind agents" passing code through multiple translations:
- Python → PW MCP → Go → PW MCP → Python
- Extended chain: 5 translations across languages

---

## Critical Issues Found

### Issue 1: Module-Level Variable Assignments 🔴 CRITICAL

**Symptom**:
```python
# Generated Python (INVALID SYNTAX!)
IRIdentifier(name='total') = 0
IRIdentifier(name='message') = (("Hello, " + name))

def SumList(numbers):
    total: int = 0  # Duplicate!
```

**Root Cause**: Go parser extracting module-level variable declarations as separate statements, Python generator placing them outside functions.

**Impact**: Generated Python code is syntactically invalid, breaks the translation chain.

**Location**: `language/go_parser_v2.py` + `language/python_generator_v2.py`

---

### Issue 2: Import Statement Leakage 🟠 HIGH

**Symptom**:
```python
# Python code shouldn't have Go imports!
import errors
import fmt

def AddNumbers(x, y):
    ...
```

**Root Cause**: Go imports being preserved in PW MCP tree and re-emitted in Python.

**Impact**: Invalid Python imports, code won't run.

**Location**: `translators/go_bridge.py` or `language/go_parser_v2.py`

---

### Issue 3: Return Value Wrapping 🟠 HIGH

**Symptom**:
```python
# Original
return result

# After Go round-trip
return [result, None]  # Go's (value, error) pattern!
```

**Root Cause**: Go generator wraps returns as `(value, error)`, parser treats as tuple, Python generator emits list.

**Impact**: Semantic change - return type is different!

**Location**: `language/go_generator_v2.py` (error wrapping) + `language/python_generator_v2.py`

---

### Issue 4: Empty Else Bodies 🟡 MEDIUM

**Symptom**:
```python
if (n > 0):
    pass  # ← Should have body here!
return ["positive", None]
return ["negative", None]  # Unreachable!
```

**Root Cause**: If/else structure not preserved correctly through Go translation.

**Impact**: Logic errors, unreachable code.

**Location**: `language/go_parser_v2.py` (_parse_if) or `language/python_generator_v2.py`

---

### Issue 5: Multi-Round-Trip Degradation 🔴 CRITICAL

**Symptom**:
```
Round 1: Python → Go → Python ✅ Works (with issues)
Round 2: Python → Go → Python ❌ CRASHES
```

**Root Cause**: Issues 1-4 compound - invalid syntax from round 1 can't be parsed in round 2.

**Impact**: System not robust enough for real agent-to-agent communication.

**Location**: Systemic - all parsers/generators

---

## Test Results

### ✅ PASS: Simple Function (3/4 tests)
- Arithmetic operations preserved
- Function structure maintained
- **BUT**: Invalid module-level assignments present

### ✅ PASS: Conditional Logic
- If/else structure mostly preserved
- Comparison operators maintained
- **BUT**: Empty else bodies, return wrapping

### ✅ PASS: Loop with Accumulator
- For loop structure preserved
- Accumulator pattern maintained
- **BUT**: Module-level assignment bug, invalid syntax

### ❌ FAIL: Multi-Language Chain
- **Crashed on translation 3** (Python → Go)
- Invalid Python syntax from previous translation
- Cannot be parsed by Python AST

---

## Root Cause Analysis

### Design Flaw: Language-Specific Assumptions in IR

The IR is supposed to be **language-agnostic**, but:

1. **Go's error handling pattern** (`return value, error`) leaks into IR
2. **Module-level vs function-level scope** not properly distinguished
3. **Import statements** not filtered by target language

### Missing: Semantic Normalization Layer

Current flow:
```
Python → IR → PW MCP → IR → Go
                ↓
            (GOOD: Language-agnostic)

Go → IR → PW MCP → IR → Python
     ↓
  (BAD: Go idioms leak into IR!)
```

**Need**: Normalization step when converting from language-specific AST to IR.

---

## Recommended Fixes

### Fix 1: Module Variable Scope Tracking 🔴 Priority 1

**Problem**: Variables declared at module level in Go end up as orphaned assignments in Python.

**Solution**:
```python
# In go_parser_v2.py
# When parsing module-level var declarations:
# - Mark them as module_vars in IRModule
# - Don't emit as separate statements

# In python_generator_v2.py
# When generating module:
# - Only emit module_vars at module level
# - Function-local vars stay in functions
```

**Files to modify**:
- `language/go_parser_v2.py` (parse module vars correctly)
- `language/python_generator_v2.py` (emit module vars at top level)
- `dsl/ir.py` (ensure IRModule.module_vars is properly used)

---

### Fix 2: Language-Specific Import Filtering 🟠 Priority 2

**Problem**: Go imports (`errors`, `fmt`) appearing in Python code.

**Solution**:
```python
# In python_generator_v2.py
# Filter out language-specific imports:
IGNORE_IMPORTS = {"errors", "fmt", "sync", "time"}  # Go stdlib

def _generate_imports(self, imports):
    return [
        imp for imp in imports
        if imp.module not in IGNORE_IMPORTS
    ]
```

**Alternative**: Map Go stdlib to Python stdlib
- `errors` → remove (Python uses exceptions)
- `fmt` → remove (Python uses print)
- `sync` → `threading`
- `time` → `time`

**Files to modify**:
- `language/python_generator_v2.py` (import filtering)
- `language/go_generator_v2.py` (semantic import mapping)

---

### Fix 3: Return Value Normalization 🟠 Priority 2

**Problem**: Go's `(value, error)` pattern creates tuples in Python.

**Solution**:

**Option A**: Strip error returns when converting Go → Python
```python
# In go_parser_v2.py
def _parse_return(self, stmt):
    # If return has 2 values and last is nil/None:
    if len(values) == 2 and is_error_nil(values[1]):
        return IRReturn(value=values[0])  # Just return first value
```

**Option B**: Add metadata to IR
```python
# In dsl/ir.py
@dataclass
class IRReturn:
    value: IRExpression
    error_handling: bool = False  # Mark Go-style error returns
```

**Files to modify**:
- `language/go_parser_v2.py` (detect error pattern)
- `language/python_generator_v2.py` (unwrap error returns)

---

### Fix 4: Control Flow Body Preservation 🟡 Priority 3

**Problem**: If/else bodies becoming empty `pass` statements.

**Solution**:
```python
# In go_parser_v2.py
# Ensure if/else bodies are fully parsed
def _parse_if(self, node):
    then_body = [self._parse_stmt(s) for s in node.body]
    else_body = [self._parse_stmt(s) for s in node.orelse] if node.orelse else []

    # Validation
    assert len(then_body) > 0, "If body cannot be empty"

    return IRIf(condition=..., then_body=then_body, else_body=else_body)
```

**Files to modify**:
- `language/go_parser_v2.py` (_parse_if method)
- Add validation/assertions

---

## Testing Strategy

### Phase 1: Fix Critical Issues (1-2)
1. Fix module variable scope
2. Fix import filtering
3. Run telephone test again → should get 4/4

### Phase 2: Fix Semantic Issues (3-4)
1. Normalize return values
2. Fix control flow bodies
3. Run extended chain test → should survive 5+ translations

### Phase 3: Stress Testing
1. Complex code with classes
2. Nested control flow
3. 10-translation chains
4. Multiple languages (add Rust, .NET, JS)

---

## Success Metrics

### Current State
- ✅ Simple functions work (with syntax errors)
- ✅ Basic control flow preserved (with issues)
- ❌ Multi-round-trip fails at translation 3
- ❌ Generated code not runnable (syntax errors)

### Target State
- ✅ All 4 telephone tests pass
- ✅ 5+ translation chains work
- ✅ Generated code is syntactically valid
- ✅ Generated code is semantically equivalent
- ✅ Code is runnable (passes basic execution tests)

---

## Next Steps

1. **Immediate**: Fix module variable scope (Issue #1)
2. **Priority**: Fix import filtering (Issue #2)
3. **Important**: Normalize returns (Issue #3)
4. **Polish**: Fix control flow (Issue #4)
5. **Validate**: Re-run all telephone tests
6. **Extend**: Test with real code examples

---

## Lessons Learned

### What Worked ✅
- PW MCP tree format successfully transfers between agents
- IR structure is generally language-agnostic
- Type information is preserved
- Basic syntax patterns translate correctly

### What Didn't Work ❌
- Language-specific idioms leak through IR
- No normalization layer for language-specific patterns
- Module vs function scope not properly tracked
- Generated code not validated before emission

### Key Insight 💡
**The IR is language-agnostic, but the parsers and generators are not.**

We need a **semantic normalization layer** that:
1. Detects language-specific patterns (Go error returns, Python comprehensions)
2. Converts them to universal IR patterns
3. Re-emits them in target language idioms

---

**End of Report**
