# PW Bug Report - Batch 2 (Agent Training Issues)

**Date:** 2025-10-08
**Reporter:** COORDINATOR Agent
**PW Version:** 2.1.0b2
**Context:** Training specialist agents in PW

---

## 🟡 BUG #7: Map Key Existence Check Pattern Unclear

### Priority: P2 - Medium

### Description
No clear pattern for checking if a map key exists. Common patterns from other languages don't work as expected.

### Attempted Code
```pw
class AuthManager {
    users: map;

    constructor() {
        self.users = {};
    }

    function register(username: string, password: string) -> bool {
        // Need to check if key exists
        if (self.users[username] != null) {  // Does this work?
            return false;
        }
        self.users[username] = "value";
        return true;
    }
}
```

### Questions
1. Does `map[key] != null` work for checking key existence?
2. Or should we use a different pattern?
3. What does map indexing return for non-existent keys?
4. Do we need a `.has_key()` method or similar?

### Compilation Result
Code compiles to Python:
```python
if (self.users[username] != None):
    return False
```

But this will throw KeyError in Python if key doesn't exist!

### Expected Behavior
Need a safe way to check if map key exists before accessing. Suggestions:
- `map.has_key(key) -> bool`
- `map[key]` returns null for missing keys (not error)
- `.get(key, default)` method

### Impact
Cannot safely check map membership, making dictionary-based logic error-prone.

### Workaround
Unknown - need guidance from PW developer.

---

---

## 🟡 BUG #8: Array .length Property Not Translated to Python

### Priority: P1 - High

### Description
PW allows `.length` property on arrays, but Python generator doesn't translate this to `len()`.

### Reproduction Code
```pw
function find_max(arr: array) -> int {
    if (arr.length == 0) {
        return 0;
    }
    let max_val = arr[0];
    return max_val;
}
```

### Python Output (BROKEN)
```python
def find_max(arr: List) -> int:
    if (arr.length == 0):  # ❌ Should be len(arr)
        return 0
    max_val = arr[0]
    return max_val
```

### Expected Python Output
```python
def find_max(arr: List) -> int:
    if (len(arr) == 0):  # ✅ Correct
        return 0
    max_val = arr[0]
    return max_val
```

### Impact
Generated Python code has runtime errors. Arrays don't have `.length` attribute in Python.

### What PW Agent Needs to Fix
In Python generator (`dsl/python_generator.py`), translate:
- `arr.length` → `len(arr)`
- `string.length` → `len(string)`

### Workaround
None - this must be fixed in generator.

---

## Status: AWAITING PW AGENT FIX

**Issues found:**
1. Bug #7: Map key existence check pattern unclear
2. Bug #8: Array .length not translated to len() in Python

**Training continuing with simple examples until fixes applied.**
