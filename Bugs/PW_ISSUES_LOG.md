# PW Language Issues Log

**Date:** 2025-10-08
**Reporter:** COORDINATOR Agent (Claude)
**PW Version:** 2.1.0b1

---

## Issue 1: C-Style For Loops Not Supported

**Description:**
Documentation and user guidance indicated C-style for loops are supported, but the parser only supports for-in loops.

**Expected Syntax (from user):**
```pw
for (let i = 0; i < 10; i = i + 1) {
    // body
}
```

**Actual Supported Syntax:**
```pw
for (item in collection) {
    // body
}
```

**Error Message:**
```
Build failed: [Line 169:14] Expected IDENTIFIER, got KEYWORD
```

**Impact:**
Cannot write index-based loops. Must use for-in loops for all iteration.

**Workaround:**
Replace all C-style for loops with for-in loops.

---

## Issue 2: Try/Catch Syntax Unclear

**Description:**
Try/catch blocks fail to parse with brace syntax.

**Attempted Syntax:**
```pw
try {
    if (condition) {
        throw "error";
    }
} catch (error) {
    return false;
}
```

**Error Message:**
```
Build failed: [Line 62:13] Expected :, got {
```

**Parser Evidence:**
The parser (pw_parser.py:1470-1511) expects Python-style colon+indentation:
```python
self.expect(TokenType.COLON)
self.expect(TokenType.NEWLINE)
self.expect(TokenType.INDENT)
```

**Expected Syntax (likely):**
```pw
try:
    // code
catch error:
    // handle
```

**Impact:**
Cannot determine correct try/catch syntax. Mixed brace/colon syntax is confusing.

**Workaround:**
Avoided using try/catch entirely in demonstration code.

---

## Issue 3: Null Type Incompatible with Map Return Type

**Description:**
Functions declared with `-> map` return type cannot return `null`.

**Code:**
```pw
function find_user() -> map {
    if (not_found) {
        return null;  // ERROR
    }
    return user_map;
}
```

**Error Message:**
```
Build failed: [Line 0:0] Return type mismatch: expected map, got null
Return type mismatch: expected map, got null
```

**Impact:**
Cannot use null as "not found" sentinel. Must return empty map `{}`.

**Workaround:**
Changed all `return null` to `return {}` for map-returning functions.

---

## Issue 4: Internal Compiler Error - Classes Completely Broken

**Description:**
Compiler crashes with NoneType attribute error for ANY file containing classes.

**Minimal Reproduction:**
```pw
class User {
    id: int;
    name: string;

    constructor(id: int, name: string) {
        self.id = id;
        self.name = name;
    }
}

function test() -> int {
    return 42;
}
```

**Error Message:**
```
Build failed: 'NoneType' object has no attribute 'prop_type'
```

**Testing Results:**
- ❌ user_management_system.pw (complex, 470 lines) - FAILS
- ❌ simple_user_manager.pw (simple, 49 lines) - FAILS
- ❌ test_class.pw (minimal, 14 lines) - FAILS
- ❌ examples/todo_list_manager.pw (official example!) - FAILS
- ✅ examples/calculator.pw (functions only, no classes) - WORKS

**Impact:**
**CRITICAL: Classes are completely non-functional**. Any PW file with a `class` keyword fails to compile.

**Root Cause:**
Type inference crashes when processing class field assignments in constructors. The code `self.id = id` causes the compiler to try to access `prop_type` on a None object.

**Status:**
This is a blocking issue that prevents writing any object-oriented code in PW.

**Need from PW Developer:**
1. **URGENT FIX**: Classes are advertised as a core feature but don't work
2. Fix type resolution for self.field assignments
3. Test all official examples in /examples directory
4. Add regression tests for classes before releasing

---

## Issue 5: Documentation Inconsistency

**Description:**
User stated PW supports "C-style for loops", but parser only implements for-in loops.

**User Quote:**
> "For loops: Both C-style and for-in loops (for (let i = 0; i < 10; i++) and for (item in items))"

**Parser Reality:**
Only for-in loops are implemented (pw_parser.py:1067-1117).

**Impact:**
Creates false expectations. Developers write invalid code based on documentation.

**Recommendation:**
- Update documentation to reflect only for-in loops are supported
- OR implement C-style for loops in parser
- Clarify roadmap for C-style loop support

---

## Issue 6: While Loops - Not Tested

**Description:**
Documentation mentions while loops, but haven't tested them yet.

**Status:**
Untested - avoided in demonstration code after other loop issues.

---

## Issue 7: Break Statement - Not Tested

**Description:**
Documentation mentions `break` for loop control, but haven't tested it.

**Status:**
Untested - avoided in demonstration code after C-style loop issues.

---

## Summary

**Blockers:**
1. Complex type inference crashes (Issue #4) - prevents compiling realistic programs
2. C-style for loop mismatch (Issue #1) - limits iteration patterns
3. Try/catch syntax ambiguity (Issue #2) - prevents error handling

**Recommendations:**
1. Fix type inference crash with better error messages
2. Clarify and document exact supported syntax for all control flow
3. Consider adding optional type hints to aid inference
4. Add more working examples of complex programs (classes, methods, loops, maps)

---

**Next Steps:**
Will attempt to create simpler, working examples to isolate the type inference crash.
