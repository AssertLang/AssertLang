# Manual Cleanup Required

**Date:** 2025-10-16
**Status:** ⚠️ Manual action needed before launch

---

## PyPI Cleanup (REQUIRED - 5 minutes)

### Problem

**12 versions of `promptware-dev` exist on PyPI:**
- 2.1.0b0 through 2.1.0b11

These need to be removed before launching AssertLang.

### Solution

**PyPI does not allow programmatic package deletion.** You must use the web interface.

#### Steps:

1. **Go to PyPI package management:**
   ```
   https://pypi.org/manage/project/promptware-dev/
   ```

2. **Log in with your PyPI account**

3. **Delete the project:**
   - Scroll to bottom of page
   - Look for "Delete project" section
   - Type `promptware-dev` to confirm
   - Click "Delete project"

4. **Verify deletion:**
   ```bash
   curl -s "https://pypi.org/pypi/promptware-dev/json" | head -1
   # Should return: 404 Not Found
   ```

**Time estimate:** 5 minutes

---

## Vercel Cleanup (DONE ✅)

**Status:** Already completed in Session 66

- ✅ `promptware-landing` project deleted via CLI
- ✅ No other Promptware projects found

---

## Why This Matters

**Before AssertLang launch, we need:**
- Clean PyPI namespace (no `promptware-dev` package)
- Clean GitHub namespace (migrated to AssertLang/AssertLang) ✅
- Clean Vercel namespace (no old sites) ✅

**This prevents:**
- User confusion (searching for promptware-dev)
- Name conflicts
- Split user base
- Negative SEO from old branding

---

## After Cleanup

Once `promptware-dev` is deleted from PyPI:

1. **Merge to main** (AssertLang/AssertLang)
2. **Add PYPI_API_TOKEN** to GitHub secrets
3. **Create v2.3.0 release**
4. **AssertLang auto-publishes to PyPI**

Then users can:
```bash
pip install assertlang  # Clean namespace!
```

---

## Troubleshooting

**Q: Can I keep old versions for backwards compatibility?**
A: No - complete rebrand means clean break. No users on promptware-dev (all beta versions).

**Q: What if I can't delete the package?**
A: Contact PyPI support: https://pypi.org/help/#admin-intervention

**Q: Will this affect the other "promptware" package (ExpressAI)?**
A: No - that's a different package owned by someone else. Don't touch it.

---

## Checklist

- [ ] Delete `promptware-dev` from PyPI (5 min)
- [ ] Verify deletion with curl command
- [ ] Proceed with AssertLang launch (see TODO_FOR_USER.md)

---

**Next:** See `TODO_FOR_USER.md` for launch steps after cleanup.
