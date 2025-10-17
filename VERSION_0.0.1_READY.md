# AssertLang v0.0.1 - First Release Ready

**Status:** 🟢 Ready for first release
**Date:** 2025-10-16
**Branch:** feature/multi-agent-contracts-pivot
**Version:** 0.0.1

---

## ✅ Version Set to 0.0.1

Updated all version references for first AssertLang release:

### Files Updated
- ✅ `pyproject.toml` - version = "0.0.1"
- ✅ `assertlang/__init__.py` - __version__ = "0.0.1"
- ✅ Package description updated (Promptware → AssertLang)

### VS Code Extension
- Version: 2.0.0 (independent versioning)
- Name: AL Language Support
- Status: Synced with AssertLang branding

---

## 📦 Current Status

### Repository
- **Package Name:** assertlang
- **Version:** 0.0.1
- **Python:** >=3.9
- **CLI Command:** `asl`

### Infrastructure
- ✅ GitHub repo: AssertLang/AssertLang
- ✅ Domains: assertlang.com, assertlang.dev
- ✅ CI/CD: 5 workflows deployed
- ✅ PyPI secret: PYPI_API_TOKEN configured
- ✅ Tests: 302/302 passing (100%)

### Recent Commits
1. `b26488e` - Set initial version to 0.0.1
2. `0ba0528` - Rebrand VS Code extension
3. Previous work on multi-agent contracts pivot

---

## 🚀 Release Workflow

### Option 1: First Release to Main (Recommended)

```bash
# 1. Push current branch
git push origin feature/multi-agent-contracts-pivot

# 2. Create PR to main
gh pr create --repo AssertLang/AssertLang \
  --base main \
  --head feature/multi-agent-contracts-pivot \
  --title "AssertLang v0.0.1: Initial Release" \
  --body "## Summary

First official release of AssertLang - executable contracts for multi-agent systems.

### Major Changes
- ✅ Complete rebrand: Promptware → AssertLang
- ✅ VS Code extension (AL language support)
- ✅ CI/CD infrastructure (5 workflows)
- ✅ Version set to 0.0.1
- ✅ 302/302 tests passing

### Infrastructure
- GitHub: AssertLang/AssertLang
- Domains: assertlang.com, assertlang.dev
- PyPI: Ready to publish (token configured)

### Breaking Changes
None - this is the first release.

### Test Results
- Unit tests: 302/302 passing ✅
- Python versions: 3.9-3.13 ✅
- Multi-OS: Ubuntu, macOS, Windows ✅

Ready to merge and release! 🚀"

# 3. Merge PR (after approval/review)
gh pr merge --squash

# 4. Checkout main and pull
git checkout main
git pull origin main

# 5. Create release tag
git tag -a v0.0.1 -m "AssertLang v0.0.1 - Initial Release

First official release of AssertLang.

🚀 Executable contracts for multi-agent systems
✅ Deterministic coordination across frameworks
🌐 Multi-language transpilation (Python, JS, Go, Rust, C#)

See README.md for details."

# 6. Push tag
git push origin v0.0.1

# 7. Create GitHub release
gh release create v0.0.1 \
  --repo AssertLang/AssertLang \
  --title "v0.0.1: Initial Release" \
  --generate-notes

# 8. Watch automated publish
# Visit: https://github.com/AssertLang/AssertLang/actions
# Workflow automatically:
# - Builds package
# - Publishes to PyPI
# - Verifies installation
# Result: https://pypi.org/project/assertlang/
```

### Option 2: Release from Feature Branch (Testing)

```bash
# Create pre-release tag on current branch
git tag v0.0.1-beta
git push origin v0.0.1-beta

gh release create v0.0.1-beta \
  --repo AssertLang/AssertLang \
  --title "v0.0.1-beta: Pre-release" \
  --prerelease \
  --generate-notes

# Test publish workflow
# Then delete tag if needed: git tag -d v0.0.1-beta
```

---

## 📋 Pre-Release Checklist

### Code Quality
- [x] Version set to 0.0.1 in all locations
- [x] Tests passing (302/302)
- [x] No uncommitted changes (except docs)
- [x] Rebrand complete (Promptware → AssertLang)

### Infrastructure
- [x] GitHub repo configured
- [x] Domains acquired
- [x] CI/CD workflows deployed
- [x] PYPI_API_TOKEN secret added
- [x] README.md updated with AssertLang branding

### Documentation
- [x] README.md describes AssertLang correctly
- [x] CICD_READY.md - Complete CI/CD guide
- [x] CICD_WORKFLOW_SUMMARY.md - Developer workflow
- [x] SESSION_STATUS.md - Current session state
- [x] VERSION_0.0.1_READY.md - This file

### Release Process
- [ ] Merge feature branch to main
- [ ] Create v0.0.1 tag
- [ ] Create GitHub release
- [ ] Verify PyPI publication
- [ ] Test installation: `pip install assertlang`

---

## 🎯 After Release

### Immediate (Post-Release)
1. ✅ Verify package on PyPI: https://pypi.org/project/assertlang/
2. ✅ Test installation: `pip install assertlang`
3. ✅ Verify CLI works: `asl --version`
4. ✅ Update Current_Work.md with release notes

### Next Steps
1. Announce on social media (if desired)
2. Update documentation site (assertlang.dev)
3. Create first GitHub Discussion
4. Plan v0.0.2 features

---

## 📊 Version History

**v0.0.1** (2025-10-16) - Initial Release
- First public release
- AssertLang branding complete
- Multi-agent contracts functionality
- CI/CD infrastructure
- VS Code extension

**Previous:** 2.2.0-alpha4 (Promptware era - deprecated)

---

## 🔗 Important Links

**Repository:** https://github.com/AssertLang/AssertLang
**Domains:**
- https://assertlang.com (acquired)
- https://assertlang.dev (acquired)

**PyPI:** https://pypi.org/project/assertlang/ (after first release)
**CI/CD:** https://github.com/AssertLang/AssertLang/actions
**Secrets:** https://github.com/AssertLang/AssertLang/settings/secrets/actions

---

## ✅ Summary

**AssertLang v0.0.1 is ready for first release!**

**What's Ready:**
- ✅ Version set to 0.0.1
- ✅ Rebranding complete
- ✅ Tests passing
- ✅ CI/CD configured
- ✅ PyPI credentials set

**Next Action:**
```bash
# Push and create PR to main
git push origin feature/multi-agent-contracts-pivot
gh pr create --repo AssertLang/AssertLang --fill
```

**Then after merge:**
```bash
git tag v0.0.1
git push origin v0.0.1
gh release create v0.0.1 --generate-notes
```

**Status: Ready to ship! 🚀**
