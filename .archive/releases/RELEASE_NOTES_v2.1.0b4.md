# Release Notes: v2.1.0b4

**Release Date**: 2025-10-08
**Previous Version**: v2.1.0b3
**Status**: Beta Release

---

## 🎯 Overview

Critical bug fix release addressing two P1 blockers discovered during agent training. Both bugs prevented proper agent training and blocked production use of security and algorithm code.

---

## 🔥 Critical Fixes

### Bug #7: Safe Map Key Access ✅ FIXED
**Priority**: P1 - Critical Blocker
**Impact**: Blocked SECURITY and DATABASE agents

**Problem**:
```pw
if (self.users[username] != null) {
    // Check if user exists
}
```

Generated unsafe Python code that threw `KeyError`:
```python
if (self.users[username] != None):  # ❌ KeyError!
```

**Solution**:
- Enhanced Python generator with property type tracking
- Fixed IR ↔ MCP converter to preserve class property types
- Map reads now generate safe `.get()` access
- Map writes still use direct `[]=` assignment

**After Fix**:
```python
if (self.users.get(username) != None):  # ✅ Safe!
```

**Files Changed**:
- `language/python_generator_v2.py` - Added property_types tracking
- `pw-syntax-mcp-server/translators/ir_converter.py` - Fixed pw_property handler

**Tests Added**: 10 comprehensive tests (all passing)

---

### Bug #9: Integer Division ✅ FIXED
**Priority**: P1 - Critical Blocker
**Impact**: Blocked CODER agent and all algorithms

**Problem**:
```pw
let mid = (left + right) / 2;
let val = arr[mid];  // TypeError!
```

Python 3 generated float division instead of integer division:
```python
mid = ((left + right) / 2)  # Returns 3.0, not 3
val = arr[mid]              # ❌ TypeError: list indices must be integers
```

**Solution**:
- Added type inference engine to Python generator
- Integer ÷ Integer now generates `//` (integer division)
- Float divisions still correctly use `/`

**After Fix**:
```python
mid = ((left + right) // 2)  # ✅ Returns 3 (int)
val = arr[mid]               # ✅ Works!
```

**Files Changed**:
- `language/python_generator_v2.py` - Added `_infer_expression_type()` method

**Tests Added**: 14 comprehensive tests (all passing)

---

## 📊 Test Results

### New Tests
- Bug #7 tests: 10/10 passing ✅
- Bug #9 tests: 14/14 passing ✅
- **Total new**: 24 tests (100%)

### Regression Testing
- All existing tests: 105/105 passing ✅
- **Total**: 129/129 tests passing (100%)
- **Regressions**: None detected

### Real-World Verification
Tested with exact failing examples from bug reports:
- ✅ `training/security_auth_system.pw` - Authentication now works
- ✅ `training/coder_algorithms.py` - Binary search now works

---

## 🚀 Agent Training Impact

### Before (v2.1.0b3)
- SECURITY agent: ❌ BLOCKED
- CODER agent: ❌ BLOCKED
- Progress: 1/11 agents (9%)

### After (v2.1.0b4)
- SECURITY agent: ✅ UNBLOCKED
- CODER agent: ✅ UNBLOCKED
- Progress: Ready to resume training

---

## 📝 Known Issues

### Minor: Duplicate Future Imports (Non-Blocking)
Generated Python files sometimes have duplicate `from __future__ import annotations`.

**Impact**: Low - Code runs correctly
**Workaround**: Python allows duplicates
**Priority**: P3 - Nice to have

---

## 🔧 Technical Details

### Type Inference System
New type inference engine tracks:
- Literal types (int, float, string, bool)
- Variable types from declarations
- Function return types
- Binary operation result types
- Special functions like `len()` → int

### Safe Map Access
Property type tracking system:
- Registers class property types during generation
- Distinguishes map reads (use `.get()`) from writes (use `[]=`)
- Preserves type info through IR ↔ MCP conversion
- Works in both direct and CLI code paths

---

## 📦 Installation

```bash
pip install assertlang==2.1.0b4
```

Or upgrade:
```bash
pip install --upgrade promptware-dev
```

---

## 🔄 Migration from v2.1.0b3

No breaking changes. Simply upgrade and rebuild:

```bash
pip install --upgrade promptware-dev
asl build your_file.pw --lang python -o output.py
```

All existing `.pw` files will compile with the new fixes automatically.

---

## 🎓 What's Next

### v2.1.0b5 (Planned)
- Fix duplicate future imports
- Additional cross-language improvements
- Performance optimizations

### v2.1.0 (Stable)
- Complete agent training (11/11 agents)
- Production hardening
- Full documentation update

---

## 📚 Resources

- [Quick Reference](docs/QUICK_REFERENCE.md)
- [Safe Patterns Guide](docs/SAFE_PATTERNS.md)
- [Bug Fix Summary](Bugs/V2.1.0b3/BUG_FIX_SUMMARY.md)
- [GitHub Release](https://github.com/AssertLang/AssertLang/releases/tag/v2.1.0b4)

---

## ✨ Contributors

Special thanks to the specialized sub-agents that tackled these complex bugs:
- Bug #7 Agent: Safe map access implementation
- Bug #9 Agent: Type inference and integer division
- CLI Path Agent: IR ↔ MCP property preservation

---

**Confidence Level**: HIGH
All fixes thoroughly tested with real-world examples and comprehensive test suites.
