# Lexer EOF Infinite Loop Bug Fix

## Summary
Fixed a critical infinite loop bug in the PW language lexer that occurred when tokenizing identifiers at end-of-file (EOF).

## Symptom
Lexer would hang indefinitely when parsing code without trailing newlines, such as:
```
import x
```

Debug trace showed:
```
Tokenizing: 'import x'
Advance called 100+ times, pos=8/8, char=''
INFINITE LOOP DETECTED at pos=8, line=1
Recent tokens: [Token(KEYWORD, 'import', 1:1)]
```

## Root Cause
**Location**: `/dsl/pw_parser.py`, line 356 in `Lexer.read_identifier()`

**Original code**:
```python
while self.peek().isalnum() or self.peek() in "_":
    ident += self.advance()
```

**The bug**: When `self.peek()` returns empty string `""` at EOF:
- `"".isalnum()` returns `False` (correct)
- `"" in "_"` returns `**True**` (surprising!)

In Python, the empty string is a substring of every string, so `"" in "_"` evaluates to `True`. This caused the while loop to continue executing, repeatedly calling `self.advance()` which returns `""` when at EOF, resulting in an infinite loop.

## The Fix
**Line 356** changed from:
```python
while self.peek().isalnum() or self.peek() in "_":
```

**To**:
```python
while self.peek() and (self.peek().isalnum() or self.peek() == "_"):
```

**Changes**:
1. Added explicit check `self.peek()` to exit loop when empty string is encountered
2. Changed `self.peek() in "_"` to `self.peek() == "_"` to avoid substring matching behavior

## Testing
### Test Cases Verified
✓ Simple import: `import x`
✓ Dotted import: `import stdlib.core`
✓ Python-style class: `class List<T>:\n    items: array<T>`
✓ Simple function: `function test() -> int { return 42 }`
✓ Generic function with params
✓ Multiple imports
✓ Complex generic classes

### Regression Tests
✓ All 16 generic parser tests passing
✓ All 22 enum comprehensive tests passing
✓ All lexer EOF scenarios handled correctly

## Impact
- **Files changed**: 1 (`dsl/pw_parser.py`)
- **Lines changed**: 1 (line 356)
- **Breaking changes**: None
- **Performance impact**: None (actually slightly faster due to short-circuit evaluation)

## Session Information
- **Session**: 46+ (Parser debugging specialist)
- **Date**: 2025-10-13
- **Branch**: `feature/pw-standard-librarian`
