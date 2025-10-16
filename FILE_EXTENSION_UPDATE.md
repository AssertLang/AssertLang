# File Extension Update: .pw → .al

**Date:** 2025-10-16
**Decision:** Use `.al` (AssertLang)
**Status:** ✅ COMPLETE

---

## Decision Rationale

### Why NOT `.pw`
- Users would ask "What does PW stand for?"
- Carries old "Promptware" brand
- No users yet, so no breaking changes

### Why NOT `.asl`
- Conflicts with American Sign Language ❌
- Could cause confusion in accessibility contexts

### Why YES `.al` ✅
- Clean abbreviation of AssertLang
- 2 characters (follows language conventions)
- Minor conflict with Assembly Language (uses `.asm` typically)
- Obvious meaning once brand is established

---

## Changes Made

### Files Updated: 787 total

**Extension changes:**
- `.pw` → `.al` in all documentation
- `.pw` → `.al` in all code examples
- `.pw` → `.al` in all CLI examples
- `.pw` → `.al` in all comments/docstrings

**Locations updated:**
- README.md - All examples
- docs/**/*.md - All documentation
- Python files - File extension checks
- JSON/TOML configs - File patterns

---

## Examples of Changes

### Before (`.pw`)
```bash
cat > hello_contract.pw << 'EOF'
asl build hello_contract.pw --lang python
```

### After (`.al`)
```bash
cat > hello_contract.al << 'EOF'
asl build hello_contract.al --lang python
```

---

## Verification

**Extension references updated:**
```bash
# Check for remaining .pw
grep -r "\.pw" . --include="*.md" --include="*.py" \
  | grep -v "BRANDING\|REBRAND\|SESSION\|RELEASE" \
  | wc -l
# Result: 0 ✅
```

**Files changed:** 787 files
**Backup files cleaned:** 1,089 .bak files removed

---

## CLI Impact

### Old Commands
```bash
promptware build contract.pw
promptware test contract.pw
```

### New Commands
```bash
asl build contract.al
asl test contract.al
```

---

## Migration Guide (for future users)

If you have existing `.pw` files:

```bash
# Rename all .pw files to .al
find . -name "*.pw" -exec rename 's/\.pw$/.al/' {} \;

# Or one by one
mv contract.pw contract.al
```

**Note:** Since there are no users yet, this migration is not needed.

---

## Brand Identity

**AssertLang Contract Files:**
- **Extension:** `.al`
- **MIME type:** `text/x-assertlang` (proposed)
- **Description:** "AssertLang contract file"
- **Icon:** (To be designed)

---

## File Extension Ecosystem

| Language | Extension | Notes |
|----------|-----------|-------|
| Python | `.py` | Standard |
| JavaScript | `.js` | Standard |
| TypeScript | `.ts` | Standard |
| Go | `.go` | Standard |
| Rust | `.rs` | Standard |
| Ruby | `.rb` | Standard |
| **AssertLang** | **`.al`** | **New** ✅ |

---

## Summary

✅ File extension successfully changed from `.pw` to `.al`
✅ 787 files updated across entire codebase
✅ All documentation updated
✅ All code examples updated
✅ Ready for commit and release

**Next steps:**
1. Commit changes
2. Update any external references (if they exist)
3. Publish documentation with new extension

---

**Last Updated:** 2025-10-16
**Status:** COMPLETE
**Decision by:** User (Hustler)
**Implemented by:** Automated script + manual verification
