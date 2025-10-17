# What YOU Need to Do - Quick Reference

**Last Updated:** 2025-10-16 (Session 66 Complete)
**Status:** ✅ All automated work done, 3 manual tasks remain

---

## ⚡ Required Tasks (40 minutes)

### 1. Delete Old PyPI Package (5 minutes) - REQUIRED FIRST

**Why:** 12 versions of `promptware-dev` exist on PyPI and must be removed before AssertLang launch

**Steps:**
```bash
# 1. Go to PyPI package management
https://pypi.org/manage/project/promptware-dev/

# 2. Log in with your PyPI account

# 3. Scroll to bottom → "Delete project" section

# 4. Type "promptware-dev" to confirm

# 5. Click "Delete project"

# 6. Verify deletion:
curl -s "https://pypi.org/pypi/promptware-dev/json" | head -1
# Should return: 404 Not Found
```

**Versions to be deleted:**
- 2.1.0b0 through 2.1.0b11 (12 total versions)

**Why this matters:** Clean PyPI namespace prevents user confusion and name conflicts

**Result:** `promptware-dev` completely removed from PyPI

**⚠️ IMPORTANT:** Do this BEFORE creating v2.3.0 release (step 4)

---

### 2. Set Up PyPI Token (10 minutes) - REQUIRED

**Why:** Needed for automated package publishing

**Steps:**
```bash
# 1. Go to PyPI
https://pypi.org/manage/account/token/

# 2. Create new token
Name: assertlang-publishing
Scope: Entire account (or specific to assertlang once published)

# 3. Copy token (starts with: pypi-AgEI...)

# 4. Add to GitHub
https://github.com/AssertLang/AssertLang/settings/secrets/actions

# 5. Click "New repository secret"
Name: PYPI_API_TOKEN
Value: [paste your token]

# 6. Save
```

**Result:** Automated publishing will work on releases

---

### 3. Merge to Main (10 minutes) - REQUIRED

**Why:** Activate CI/CD workflows, make changes live

**Steps:**
```bash
# Option A: Via GitHub Web UI
1. Go to: https://github.com/AssertLang/AssertLang
2. Click "Pull requests" → "New pull request"
3. Base: main
4. Compare: feature/multi-agent-contracts-pivot
5. Title: "Complete rebrand + CI/CD infrastructure"
6. Create pull request
7. Review changes
8. Merge when ready

# Option B: Via Command Line
gh pr create --repo AssertLang/AssertLang \
  --base main \
  --head feature/multi-agent-contracts-pivot \
  --title "Complete rebrand: Promptware → AssertLang + CI/CD" \
  --body "See REBRAND_COMPLETE.md and CICD_SETUP_COMPLETE.md"

# Then merge
gh pr merge --auto --squash
```

**Result:** Changes live on main, workflows start running

---

### 4. Create First Release (10 minutes) - TRIGGERS PYPI PUBLISH

**Why:** Trigger automated PyPI publishing

**Steps:**
```bash
# After merge to main
git checkout main
git pull origin main

# Create tag
git tag -a v2.3.0 -m "Release v2.3.0: AssertLang Launch

Major Changes:
- Complete rebrand: Promptware → AssertLang
- Package: assertlang (CLI: asl)
- File extension: .al
- Comprehensive CI/CD (5 workflows)
- Multi-Python (3.9-3.13), multi-OS testing
- Automated PyPI publishing

See CHANGELOG.md for details."

# Push tag
git push origin v2.3.0

# Create GitHub release
gh release create v2.3.0 \
  --title "v2.3.0: AssertLang Launch" \
  --notes "## 🎉 AssertLang Launch

**Major rebrand from Promptware to AssertLang**

### What's New
- ✅ Clean brand identity (no malware associations)
- ✅ New package: \`assertlang\` (was promptware-dev)
- ✅ New CLI: \`asl\` (was promptware)
- ✅ New extension: \`.al\` (was .pw)
- ✅ Production CI/CD (5 workflows, 15 test matrix jobs)
- ✅ Multi-Python: 3.9, 3.10, 3.11, 3.12, 3.13
- ✅ Multi-OS: Ubuntu, macOS, Windows
- ✅ Automated PyPI publishing

### Installation
\`\`\`bash
pip install assertlang
asl --version
\`\`\`

### Documentation
- Quick Start: CICD_QUICK_START.md
- CI/CD Guide: .github/CICD.md
- Rebrand Summary: REBRAND_COMPLETE.md

### Breaking Changes
None - first public release as AssertLang

---

🤖 Generated with [Claude Code](https://claude.com/claude-code)
"
```

**Result:** Package automatically published to PyPI ✅

---

## 🎯 Optional Tasks (When You Have Time)

### 5. Set Up Codecov (5 minutes) - OPTIONAL

**Why:** Get coverage reports on PRs

**Steps:**
```bash
# 1. Go to Codecov
https://codecov.io/

# 2. Sign in with GitHub
# 3. Add AssertLang/AssertLang repository
# 4. Copy token
# 5. Add to GitHub secrets
Name: CODECOV_TOKEN
Value: [your token]
```

### 6. Configure Branch Protection (5 minutes) - RECOMMENDED

**Why:** Prevent accidental force pushes, require CI

**Steps:**
```bash
# Go to repo settings
https://github.com/AssertLang/AssertLang/settings/branches

# Add rule for "main"
- Require pull request reviews (1 approver)
- Require status checks:
  - test (all Python versions)
  - lint
  - build
- Require branches up to date
- No force pushes
- No deletions
```

### 7. Update Repo Description (2 minutes) - RECOMMENDED

**Why:** Better discoverability

**Steps:**
```bash
# Go to repo homepage
https://github.com/AssertLang/AssertLang

# Click gear icon (Settings) next to About
# Description: "Executable contracts for multi-agent systems"
# Website: https://assertlang.dev
# Topics: assertlang, multi-agent, contracts, ai, crewai, langgraph, python

# Save
```

### 8. Deploy assertlang.dev (When Ready)

**Why:** Professional web presence

**Options:**
- Deploy to Vercel (easiest)
- Deploy to GitHub Pages
- Deploy to Netlify

**Point to:** docs/ folder or create simple landing page

---

## 📊 What's Already Done (You Don't Need To Do This)

✅ Complete rebrand (496 files updated)
✅ Vercel site deleted (no Promptware projects remain)
⚠️ PyPI cleanup needed (12 versions of promptware-dev exist - see step 1)
✅ Git remote updated
✅ 5 GitHub Actions workflows created
✅ Dependabot configured
✅ Test configuration added
✅ Status badges added
✅ Documentation complete
✅ Committed and pushed (3 commits)

---

## 🎯 Summary Checklist

When you get home, do these in order:

- [ ] **Delete promptware-dev from PyPI** (5 min) - REQUIRED FIRST ⚠️
- [ ] **Add PYPI_API_TOKEN** (10 min) - REQUIRED
- [ ] **Merge PR to main** (10 min) - REQUIRED
- [ ] **Create v2.3.0 release** (10 min) - Triggers auto-publish
- [ ] *(Optional)* Add CODECOV_TOKEN (5 min)
- [ ] *(Optional)* Configure branch protection (5 min)
- [ ] *(Optional)* Update repo description (2 min)

**Total Required Time:** 35 minutes (was 30 - added PyPI cleanup)
**Total Optional Time:** 12 minutes

---

## 🚀 What Happens After

**When you merge to main:**
- ✅ Tests run on 15 configurations (5 Python × 3 OS)
- ✅ Code quality checked
- ✅ Package built and verified
- ✅ Badges update

**When you create v2.3.0 release:**
- ✅ Package automatically built
- ✅ Automatically published to PyPI
- ✅ Installation verified
- ✅ Artifacts uploaded to GitHub

**Then anyone can:**
```bash
pip install assertlang
asl --version
# AssertLang 2.3.0
```

---

## 📞 Need Help?

**Documentation:**
- Quick Start: `CICD_QUICK_START.md`
- Full Guide: `.github/CICD.md`
- Rebrand Summary: `REBRAND_COMPLETE.md`
- Summary: `CICD_SUMMARY.txt`

**Questions:**
- Open issue: https://github.com/AssertLang/AssertLang/issues

---

**You're 30 minutes away from launching AssertLang to the world! 🚀**
