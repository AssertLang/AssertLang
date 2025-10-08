# Normalizer Reality Check

## The Honest Truth

**Status**: The semantic normalizer is **conceptually correct** but **cannot fix broken parsers**.

---

## What Actually Happened

### Test Results

```
Python → Python: ✅ Works
Go → Python: ❌ BROKEN (invalid Python generated)
Python → Go → Python: ❌ BROKEN (crashes)
```

### Root Cause

The normalizer **assumes the IR is already correct**. But the **Go parser produces broken IR**:

```python
# What Go parser creates:
IRAssignment(
    target=IRIdentifier(name='message'),  # ❌ Should be string "message"
    value=IRBinaryOp(
        left=IRIdentifier(name='("Hello, "'),  # ❌ Mangled string!
        right=IRIdentifier(name='name)')       # ❌ Extra parenthesis!
    )
)
```

This is **fundamentally broken** - you can't normalize garbage.

---

## The Real Problems

### Problem #1: Go Parser is Broken 🔴 CRITICAL

The Go parser (`language/go_parser_v2.py`) has bugs:

1. **String literals get mangled** - `"Hello, "` becomes `IRIdentifier(name='("Hello, "')`
2. **Assignment targets are wrong type** - Creates `IRIdentifier` instead of string
3. **Function-local vars extracted as module vars** - Scope tracking broken

**This is NOT a normalization problem** - it's a parser bug.

---

### Problem #2: Normalizer Can't Fix Broken IR

**The normalizer assumes**:
- IR is semantically valid
- Types are correct (string targets, proper expressions)
- Structure is sound

**Reality**:
- IR from Go parser is malformed
- Can't "normalize" `IRIdentifier(name='("Hello, "')` - it's just broken

**Analogy**: You can't "normalize" a car with square wheels. You need to fix the wheels first.

---

## What the Normalizer CAN Do ✅

The normalizer **successfully handles**:

1. **Removing Go stdlib imports** ✅
   ```python
   # Before normalization
   imports = [errors, fmt, my_library]

   # After normalization
   imports = [my_library]  # Go stdlib stripped!
   ```

2. **Stripping error returns** ✅ (when IR is correct)
   ```python
   # Before
   return [value, nil]

   # After
   return value
   ```

3. **Adding language-specific imports** ✅
   ```python
   # Python denormalization adds
   from __future__ import annotations
   ```

**But**: These only work if the **input IR is already valid**.

---

## What the Normalizer CANNOT Do ❌

1. **Fix broken string parsing** - Can't repair `IRIdentifier(name='("Hello, "')`
2. **Fix wrong data types** - Can't convert `IRIdentifier` target to string
3. **Fix scope tracking** - Can't move module vars to function scope
4. **Fix mangled expressions** - Garbage in, garbage out

---

## The Telephone Game Truth

### Why Tests Still Fail

**Test 1 (Python → Python)**: ✅ **PASSES**
- Python parser is good
- Python generator is good
- Normalizer not needed (same language)

**Test 2 (Go → Python)**: ❌ **FAILS**
- Go parser produces broken IR
- Normalizer can't fix broken IR
- Python generator emits `IRIdentifier(name='message')` because that's what's in the IR

**Test 3 (Python → Go → Python)**: ❌ **CRASHES**
- Go parser breaks the IR from round 1
- Round 2 tries to parse invalid Python
- Crash

---

## What We Actually Need

### Option 1: Fix the Go Parser 🔴 Required

**File**: `language/go_parser_v2.py`

**Bugs to fix**:
1. String literal parsing - don't create `IRIdentifier` for string constants
2. Assignment target extraction - use string, not `IRIdentifier`
3. Module vs function scope - track properly

**Estimated effort**: 4-6 hours

---

### Option 2: Add IR Validation Layer 🟡 Recommended

**New file**: `dsl/ir_validator.py`

```python
def validate_ir(ir_module: IRModule) -> List[str]:
    """
    Validate IR is well-formed before normalization.

    Returns list of errors found.
    """
    errors = []

    for func in ir_module.functions:
        for stmt in func.body:
            if isinstance(stmt, IRAssignment):
                # Target must be string, not IRIdentifier!
                if not isinstance(stmt.target, str):
                    errors.append(
                        f"IRAssignment target must be string, got {type(stmt.target)}"
                    )

    return errors
```

This would **catch broken IR** before it propagates through the system.

---

### Option 3: Defensive Normalization 🟢 Band-Aid

Make normalizer **attempt to fix** common parser bugs:

```python
def _fix_broken_assignment(assign: IRAssignment) -> IRAssignment:
    """Attempt to repair broken assignment from buggy parser."""

    # Fix 1: Extract string from IRIdentifier target
    if isinstance(assign.target, IRIdentifier):
        target = assign.target.name
    else:
        target = assign.target

    # Fix 2: Unwrap mangled string literals
    value = _fix_broken_expression(assign.value)

    return IRAssignment(target=target, value=value, ...)
```

**Downside**: Fragile, treats symptoms not cause.

---

## Recommendation

### Short Term (Now)

1. **Document the issue** ✅ (this file)
2. **Add IR validation** - Catch bugs early
3. **Fix critical Go parser bugs** - String literals, assignment targets

### Medium Term (Next Session)

1. **Comprehensive Go parser rewrite** - Fix all scope/parsing issues
2. **Add parser unit tests** - Prevent regressions
3. **Re-run telephone game** - Should pass with fixed parser

### Long Term (V1.0)

1. **IR validation in CI** - Every commit validates IR correctness
2. **Parser fuzzing** - Auto-discover parser bugs
3. **Bidirectional test suite** - Every language pair tested

---

## Key Insight

**The normalizer IS working as designed**. It's not a silver bullet that can fix broken parsers.

Think of the system as a pipeline:

```
Parser → IR → Normalizer → MCP → Denormalizer → Generator
  ↑                ↑
  Bug here     Can't fix garbage
```

**Fix the parser, and the normalizer will shine.**

---

## Updated Status

**Normalizer**: ✅ Implemented, conceptually correct
**Go Parser**: ❌ Broken, produces invalid IR
**Python Parser**: ✅ Works correctly
**Python Generator**: ✅ Works correctly (given valid IR)
**Go Generator**: ❌ Also has issues (adds error returns when it shouldn't)

**Telephone Game**: **Blocked on Go parser bugs**

---

## Honest Assessment

You asked: **"is it though show me show me the game of telephone."**

**Answer**: No, it's not working yet. The normalizer is correct but the underlying parsers are broken. We need to:

1. Fix Go parser (critical)
2. Add IR validation
3. Then re-test

**The vision is right, the architecture is right, but the implementation has bugs that need fixing.**

---

**End of Reality Check**
