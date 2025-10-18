# AssertLang - Complete Alignment Plan
**Date:** October 18, 2025
**Goal:** Make EVERYTHING match across the board

---

## Current State Audit

### ❌ MISMATCHES FOUND

| Component | Current State | Issue |
|-----------|---------------|-------|
| **pyproject.toml** | `version = "0.0.1"` | ❌ Doesn't match PyPI |
| **PyPI Latest** | `0.0.4` | ❌ Pre-pivot version (old product?) |
| **GitHub Default Branch** | `feature/multi-agent-contracts-pivot` | ❌ Feature branch as default |
| **Main Branch** | Has contracts README | ❌ Might be behind feature branch |
| **Local Install** | `2.2.0a4` (editable) | ❌ Random alpha version |
| **Product Description** | "Executable contracts..." | ✅ Correct everywhere |
| **Syntax** | `.al` files with contracts | ✅ Works perfectly |
| **CLI Commands** | `asl build` | ✅ Works perfectly |

### ✅ WHAT WORKS

- The actual product (transpiler + contracts)
- Examples in `examples/agent_coordination/`
- Proof of determinism documented
- Tests passing (302/302)
- CLI functional

---

## The Problem

**Everything works, but nothing aligns:**

1. **Version Chaos**
   - Code says 0.0.1
   - PyPI says 0.0.4
   - No clear "current version"

2. **Branch Confusion**
   - Default branch is a "feature" branch
   - Implies this is experimental (it's not!)
   - Main branch exists but unclear status

3. **PyPI Mismatch**
   - PyPI v0.0.4 might be OLD product (pre-pivot)
   - Website describes NEW product (contracts)
   - Users installing from PyPI get wrong thing?

4. **No Clear Story**
   - What version should users install?
   - What branch should they clone?
   - What's "stable" vs "experimental"?

---

## What SHOULD Match

### Single Source of Truth for Each:

| Item | Should Match | Everywhere |
|------|--------------|------------|
| **Product Name** | AssertLang | ✅ |
| **Product Description** | "Executable contracts for multi-agent systems" | ✅ |
| **Current Version** | `0.1.0` (NEW after pivot) | ❌ Needs update |
| **Stable Branch** | `main` | ❌ Not default |
| **Default Branch** | `main` | ❌ Currently feature branch |
| **File Extension** | `.al` | ✅ |
| **CLI Command** | `asl` | ✅ |
| **PyPI Package** | `assertlang==0.1.0` (contracts) | ❌ Currently 0.0.4 |
| **Install Command** | `pip install assertlang` | ⚠️  Installs old version |

---

## Complete Alignment Plan

### Phase 1: Local Cleanup ✅ (Already Done)
- ✅ Remove all "Promptware" references
- ✅ Remove all "PW" references
- ✅ Change all `.pw` → `.al`
- ✅ Update all examples

### Phase 2: Version & Branch Alignment (DO THIS NOW)

#### Step 1: Decide on Version Number
**Recommendation:** `0.1.0`
- Why: Major pivot from old product → new product
- Semantic versioning: `0.1.0` = first minor release
- Clear signal: "This is the contracts product"

Alternative: `1.0.0` (if you consider this production-ready)

#### Step 2: Update Version Everywhere
```bash
# Update pyproject.toml
version = "0.1.0"

# Update CURRENT_WORK.md
**Version:** 0.1.0

# Update README if version mentioned
```

#### Step 3: Clean Up Branches
**Option A: Merge Feature → Main**
```bash
git checkout main
git merge feature/multi-agent-contracts-pivot
git push origin main
gh repo edit AssertLang/AssertLang --default-branch main
```

**Option B: Delete Old Main, Rename Feature**
```bash
git branch -D main
git branch -m feature/multi-agent-contracts-pivot main
git push origin main --force
gh repo edit AssertLang/AssertLang --default-branch main
```

**Recommendation:** Option A (safer, preserves history)

### Phase 3: PyPI Publication

#### Step 1: Build Package
```bash
# Clean old builds
rm -rf dist/ build/ *.egg-info

# Build new package
python -m build
```

#### Step 2: Test Package Locally
```bash
# Install in test environment
pip install dist/assertlang-0.1.0-py3-none-any.whl

# Test CLI
asl --version  # Should show 0.1.0
asl build examples/agent_coordination/user_service_contract.al --lang python
```

#### Step 3: Publish to PyPI
```bash
# Upload to PyPI
twine upload dist/assertlang-0.1.0*

# Verify
pip install assertlang==0.1.0  # Should work
```

### Phase 4: GitHub Release

```bash
# Create release tag
git tag -a v0.1.0 -m "v0.1.0 - Multi-Agent Contracts Release"
git push origin v0.1.0

# Create GitHub release
gh release create v0.1.0 \
  --title "v0.1.0 - Executable Contracts for Multi-Agent Systems" \
  --notes-file RELEASE_NOTES_v0.1.0.md \
  --repo AssertLang/AssertLang
```

### Phase 5: Website/Documentation Alignment

#### Update Website
- ✅ Product description (already correct)
- ✅ Syntax examples (already correct)
- ❌ Install command: Update to `pip install assertlang==0.1.0`
- ❌ Version badges: Update to show v0.1.0
- ❌ Examples: Already correct

#### Update README Badges
```markdown
[![PyPI](https://img.shields.io/pypi/v/assertlang?style=flat-square)]
# This will auto-update after PyPI publish
```

---

## After Alignment - Everything Should Match

### Version: `0.1.0` Everywhere
- ✅ `pyproject.toml`
- ✅ PyPI package
- ✅ GitHub release tag
- ✅ Website install instructions
- ✅ Documentation

### Default Branch: `main` Everywhere
- ✅ GitHub default branch
- ✅ Clone instructions
- ✅ CI/CD pipelines
- ✅ Badges pointing to main

### Product: "Executable Contracts" Everywhere
- ✅ README
- ✅ PyPI description
- ✅ Website
- ✅ Documentation
- ✅ Examples

### Installation: Same Result Everywhere
```bash
# From PyPI
pip install assertlang  # → Gets 0.1.0 with contracts

# From GitHub
git clone https://github.com/AssertLang/AssertLang
# → Gets main branch with contracts

# Both produce: same product, same version
```

---

## Execution Order

### 1. Local Changes (5 minutes)
- [ ] Update `pyproject.toml` version to `0.1.0`
- [ ] Update `CURRENT_WORK.md` version
- [ ] Create `RELEASE_NOTES_v0.1.0.md`
- [ ] Commit changes

### 2. Branch Alignment (10 minutes)
- [ ] Checkout main branch
- [ ] Merge feature branch into main
- [ ] Push to origin/main
- [ ] Set main as default on GitHub
- [ ] Delete feature branch (optional)

### 3. Build & Test (5 minutes)
- [ ] Clean old builds
- [ ] Run `python -m build`
- [ ] Test package locally
- [ ] Run test suite

### 4. Publish (10 minutes)
- [ ] Publish to PyPI with `twine upload`
- [ ] Create GitHub release v0.1.0
- [ ] Verify PyPI shows 0.1.0
- [ ] Test `pip install assertlang`

### 5. Verify Alignment (5 minutes)
- [ ] Check PyPI version
- [ ] Check GitHub default branch
- [ ] Check website matches
- [ ] Test install from scratch

**Total Time:** ~35 minutes

---

## Success Criteria

After alignment, these should ALL be true:

✅ **Version**
- `pyproject.toml` says `0.1.0`
- PyPI latest is `0.1.0`
- GitHub release tag is `v0.1.0`
- `asl --version` shows `0.1.0`

✅ **Branch**
- GitHub default branch is `main`
- `main` has all contracts code
- Feature branch merged or deleted
- CI/CD runs on `main`

✅ **Product**
- PyPI description matches website
- README matches website
- Examples work
- Tests pass (302/302)

✅ **User Experience**
- `pip install assertlang` → contracts version
- `git clone` → contracts code
- Website → correct install instructions
- All examples run successfully

---

## Risk Assessment

### Low Risk
- ✅ Code works (tested)
- ✅ Tests pass
- ✅ Examples functional

### Medium Risk
- ⚠️  PyPI v0.0.4 users might get breaking changes
  - **Mitigation:** Clear release notes, version bump signals change
- ⚠️  Branch changes might break CI
  - **Mitigation:** Test CI after merge

### Zero Risk
- ✅ Not deleting old versions
- ✅ Not breaking existing functionality
- ✅ Just aligning what already works

---

## Post-Alignment Checklist

After everything is aligned:

- [ ] User runs: `pip install assertlang`
  - Gets: v0.1.0 with contracts ✅
- [ ] User runs: `asl --version`
  - Shows: `0.1.0` ✅
- [ ] User runs: `asl build contract.al --lang python`
  - Works: Transpiles correctly ✅
- [ ] User visits: GitHub repo
  - Sees: main branch with contracts ✅
- [ ] User visits: Website
  - Sees: Install instructions for 0.1.0 ✅
- [ ] User follows: Quickstart tutorial
  - Works: Everything runs ✅

---

## Next Action

**You decide:**

1. **Quick Alignment (Recommended)**
   - Update version to 0.1.0
   - Merge to main
   - Publish to PyPI
   - Done in 30 minutes

2. **Thorough Review First**
   - Review all changes
   - Test everything manually
   - Then align
   - Takes 1-2 hours

3. **Staged Rollout**
   - Align version locally first
   - Merge branches second
   - Publish PyPI last
   - Takes 1 day (with testing between)

**Recommendation:** Quick Alignment - everything already works, just needs publishing.

---

**Ready to execute?** Say the word and I'll start with Step 1 (update pyproject.toml).
