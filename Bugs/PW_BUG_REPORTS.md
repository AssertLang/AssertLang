# PW Bug Reports - Systematic Testing

**Date:** 2025-10-08
**Reporter:** COORDINATOR Agent
**PW Version:** 2.1.0b1
**Purpose:** Detailed reproduction steps for PW agent to fix

---

## 🔴 BUG #1: Class Compilation Crash (CRITICAL)

### Priority: P0 - BLOCKER

### Description
ANY .pw file containing a `class` keyword fails to compile with internal error.

### Reproduction Steps

1. Create file `test_class.pw`:
```pw
class User {
    id: int;
    name: string;

    constructor(id: int, name: string) {
        self.id = id;
        self.name = name;
    }
}
```

2. Run: `promptware build test_class.pw --lang python`

3. **Result:**
```
Build failed: 'NoneType' object has no attribute 'prop_type'
```

### Expected Behavior
Should compile to Python class:
```python
class User:
    def __init__(self, id: int, name: string):
        self.id = id
        self.name = name
```

### Actual Behavior
Internal compiler error, no line number, no stack trace for user.

### Files That Fail
- ❌ test_class.pw (minimal 14-line example)
- ❌ simple_user_manager.pw (49 lines with methods)
- ❌ user_management_system.pw (470 lines complex)
- ❌ examples/todo_list_manager.pw (YOUR OFFICIAL EXAMPLE!)

### Files That Work
- ✅ examples/calculator.pw (functions only, no classes)
- ✅ working_example.pw (functions + for-in loops)

### Root Cause Hypothesis
Type inference fails when processing `self.field = value` assignments in constructor.
The code tries to access `.prop_type` attribute on a None object, suggesting:
- Class fields aren't being registered in type environment
- Or `self` type isn't being resolved correctly
- Or constructor parameter types aren't propagating to assignments

### Impact
**BLOCKS ALL OBJECT-ORIENTED PROGRAMMING**
- Cannot use classes
- Cannot build realistic applications
- Makes PW unsuitable for agent code generation

### What PW Agent Needs to Fix
1. Add null check before accessing `.prop_type`
2. Ensure class fields are registered in type environment during parsing
3. Ensure `self` type is resolved to the containing class type
4. Test that official examples compile before releasing
5. Add better error messages with line numbers and context

---

## 🟡 BUG #2: C-Style For Loops Not Implemented

### Priority: P1 - HIGH (Documentation Mismatch)

### Description
Documentation and user guidance say C-style for loops are supported, but parser rejects them.

### Reproduction Steps

1. Create file `test_for.pw`:
```pw
function count_to_ten() -> int {
    for (let i = 0; i < 10; i = i + 1) {
        // loop body
    }
    return 10;
}
```

2. Run: `promptware build test_for.pw --lang python`

3. **Result:**
```
Build failed: [Line 2:14] Expected IDENTIFIER, got KEYWORD
```

### Expected Behavior (per documentation)
Should support: `for (let i = 0; i < 10; i = i + 1) { }`

### Actual Behavior
Parser only supports: `for (item in collection) { }`

### Evidence
`dsl/pw_parser.py` lines 1067-1117 only implement for-in loops:
```python
def parse_for(self) -> IRFor:
    """
    Parse for loop (C-style syntax).
    Syntax:
        for (item in items) { body }
        for (i in range(0, 10)) { body }
    """
    self.expect(TokenType.KEYWORD)  # "for"
    self.expect(TokenType.LPAREN)
    iterator = self.expect(TokenType.IDENTIFIER).value  # Expects iterator, not 'let'
```

Comment says "C-style syntax" but implementation is for-in only!

### What PW Agent Needs to Fix
**Option A:** Implement C-style for loops
- Add parsing for `for (init; condition; increment)`
- Generate appropriate IR (IRFor with init/condition/increment fields)
- Update generators for Python/Go/Rust

**Option B:** Update documentation
- Remove claims about C-style for loop support
- Clearly state only for-in loops are supported
- Show workarounds (while loops, array indices)

**Recommendation:** Option A - implement C-style loops (common need)

---

## 🟡 BUG #3: Try/Catch Syntax Ambiguity

### Priority: P1 - HIGH (Prevents Error Handling)

### Description
Parser expects Python-style colon+indent, but C-style braces seem natural given rest of syntax.

### Reproduction Steps

1. Create file `test_try.pw`:
```pw
function safe_divide(a: int, b: int) -> int {
    try {
        if (b == 0) {
            throw "Division by zero";
        }
        return a / b;
    } catch (error) {
        return 0;
    }
}
```

2. Run: `promptware build test_try.pw --lang python`

3. **Result:**
```
Build failed: [Line 2:9] Expected :, got {
```

### Expected Behavior (Unknown!)
No working examples of try/catch in codebase to reference.

### Parser Evidence
`dsl/pw_parser.py` lines 1470-1511 expects:
```python
self.expect(TokenType.COLON)     # Expects ':'
self.expect(TokenType.NEWLINE)
self.expect(TokenType.INDENT)
```

This suggests Python-style syntax:
```pw
try:
    // code
catch error:
    // handle
```

But rest of PW uses C-style braces!

### What PW Agent Needs to Fix
1. **Choose a syntax:** Brace or colon style?
2. **If brace style:** Update parser to accept `try { } catch (e) { }`
3. **If colon style:** Document clearly and provide examples
4. **Add working example** in examples/ directory
5. **Test compilation** to all target languages

**Recommendation:** Brace style for consistency with rest of language

---

## 🟡 BUG #4: Null Type Incompatible with Typed Returns

### Priority: P2 - MEDIUM (Workaround Exists)

### Description
Functions with typed return (like `-> map`) cannot return `null` to indicate "not found".

### Reproduction Steps

1. Create file `test_null.pw`:
```pw
function find_user(id: int) -> map {
    if (id < 0) {
        return null;  // Common "not found" pattern
    }
    return {id: id, name: "test"};
}
```

2. Run: `promptware build test_null.pw --lang python`

3. **Result:**
```
Build failed: [Line 0:0] Return type mismatch: expected map, got null
```

### Expected Behavior
Should allow null as valid return value (Option types: `map | null` or `map?`)

### Actual Behavior
Type checker rejects null returns even though they're common pattern.

### Workaround
Return empty map: `return {};`

### Impact
- Cannot use null sentinel values
- Empty map `{}` is ambiguous (empty result vs error?)
- Makes error handling less clear

### What PW Agent Needs to Fix
**Option A:** Add optional types
- Allow `-> map?` or `-> map | null` syntax
- Type checker accepts null for optional types
- Generators handle null checks in target languages

**Option B:** Document workaround
- Clearly state null not allowed in typed returns
- Show empty map pattern as official approach
- Consider adding Result<T, E> type for error handling

**Recommendation:** Option A - proper optional types

---

## 🟢 BUG #5: While Loops - Status Unknown

### Priority: P3 - LOW (Not Tested Yet)

### Description
Documentation mentions while loops but haven't tested them due to other issues.

### Test Needed
```pw
function count() -> int {
    let i = 0;
    while (i < 10) {
        i = i + 1;
    }
    return i;
}
```

### Status
**Awaiting test after Bug #1 (classes) is fixed.**

If while loops work, mark as ✅ WORKING
If they fail, document reproduction steps

---

## 🟢 BUG #6: Break/Continue - Status Unknown

### Priority: P3 - LOW (Not Tested Yet)

### Description
Documentation mentions break/continue for loop control but untested.

### Test Needed
```pw
function find_first_even(numbers: array) -> int {
    for (num in numbers) {
        if (num % 2 == 0) {
            return num;  // Early return works?
        }
    }
    return -1;
}

function count_until_five(numbers: array) -> int {
    let count = 0;
    for (num in numbers) {
        if (num == 5) {
            break;  // Does break work?
        }
        if (num < 0) {
            continue;  // Does continue work?
        }
        count = count + 1;
    }
    return count;
}
```

### Status
**Awaiting test after Bug #1 (classes) is fixed.**

---

## Summary for PW Agent

### Critical Path (Fix in Order)

1. **🔴 BUG #1: Fix class compilation crash** - Blocks everything
2. **🟡 BUG #2: C-style for loops** - Common need, doc mismatch
3. **🟡 BUG #3: Try/catch syntax** - Need error handling
4. **🟡 BUG #4: Optional types for null** - Ergonomics
5. **🟢 BUG #5-6: Test while/break/continue** - Verify they work

### Testing Checklist for PW Agent

After each fix:
- [ ] Test minimal reproduction case
- [ ] Test official examples compile (calculator.pw, todo_list_manager.pw)
- [ ] Test cross-compilation (Python, Go, Rust)
- [ ] Add regression test to prevent reoccurrence
- [ ] Update documentation if behavior changed

### Success Criteria

When complete:
- ✅ test_class.pw compiles successfully
- ✅ examples/todo_list_manager.pw compiles successfully
- ✅ user_management_system.pw compiles successfully
- ✅ All language features have working examples in examples/
- ✅ Error messages include line numbers and helpful context

---

**Next:** Awaiting PW agent fixes for Bug #1 (classes), then will test remaining features.
