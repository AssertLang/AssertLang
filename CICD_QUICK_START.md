# CI/CD Quick Start Guide

**Status:** ✅ Infrastructure deployed to GitHub
**Commit:** 259d37f
**Branch:** feature/multi-agent-contracts-pivot

---

## ⚡ What's Ready

✅ **5 GitHub Actions workflows** deployed and configured
✅ **Dependabot** configured for weekly updates
✅ **Status badges** added to README
✅ **Test configuration** added to pyproject.toml
✅ **Documentation** complete

---

## 🔑 Required: Set Up Secrets (5 minutes)

**Before workflows can run, add these secrets:**

### 1. PyPI Token (REQUIRED)

```bash
# Get token from: https://pypi.org/manage/account/token/
# Name: assertlang-publishing
# Scope: Entire account (or project: assertlang)

# Add to GitHub:
# Settings → Secrets and variables → Actions → New repository secret
# Name: PYPI_API_TOKEN
# Value: pypi-AgEI... (your token)
```

### 2. Codecov Token (OPTIONAL - for coverage reports)

```bash
# Get from: https://codecov.io/
# Sign in with GitHub
# Add AssertLang/AssertLang repository
# Copy token

# Add to GitHub:
# Name: CODECOV_TOKEN
# Value: (your token)
```

### 3. Test PyPI Token (OPTIONAL - for testing)

```bash
# Get from: https://test.pypi.org/manage/account/token/

# Add to GitHub:
# Name: TEST_PYPI_API_TOKEN
# Value: (your token)
```

---

## 🚀 Usage

### Running Tests (Automatic)

**Tests run automatically on:**
- Every push to `main` or `develop`
- Every pull request to `main` or `develop`

**What runs:**
- ✅ Tests on Python 3.9, 3.10, 3.11, 3.12, 3.13
- ✅ Tests on Ubuntu, macOS, Windows
- ✅ Code coverage uploaded to Codecov
- ✅ Linting (black, flake8, isort, mypy)
- ✅ Security scanning (safety, bandit)
- ✅ Package building & verification

### Publishing to PyPI (Automatic)

**Option 1: GitHub Release (Recommended)**

```bash
# Tag the release
git tag -a v2.2.0 -m "Release v2.2.0: Feature XYZ"
git push origin v2.2.0

# Create GitHub release
gh release create v2.2.0 \
  --title "v2.2.0: Feature XYZ" \
  --notes "## What's New
- Feature A
- Feature B
- Bug fix C"

# Workflow automatically:
# 1. Builds package
# 2. Publishes to PyPI
# 3. Verifies publication
# 4. Uploads artifacts to release
```

**Option 2: Manual Trigger**

```bash
# Go to: Actions → Publish to PyPI → Run workflow
# Select branch: main
# test_pypi: false (or true to test first)
```

### Testing Locally

```bash
# Run tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=assertlang --cov-report=html
open htmlcov/index.html

# Run linters
black --check assertlang/ tests/
flake8 assertlang/ tests/
mypy assertlang/

# Build package
python -m build
twine check dist/*
```

---

## 📊 Monitoring

**View Workflows:**
https://github.com/AssertLang/AssertLang/actions

**Check Coverage:**
https://codecov.io/gh/AssertLang/AssertLang

**PyPI Stats:**
https://pypistats.org/packages/assertlang

**Dependabot:**
https://github.com/AssertLang/AssertLang/security/dependabot

---

## 🎯 Next Steps

### 1. Add Secrets (Required)

```bash
# Go to: https://github.com/AssertLang/AssertLang/settings/secrets/actions
# Add: PYPI_API_TOKEN (required)
# Add: CODECOV_TOKEN (optional)
```

### 2. Merge to Main (Triggers First Run)

```bash
# Create PR
gh pr create --repo AssertLang/AssertLang \
  --base main \
  --head feature/multi-agent-contracts-pivot \
  --title "CI/CD Infrastructure + Rebrand" \
  --fill

# After merge, workflows run automatically
```

### 3. Watch First Run

```bash
# Go to Actions tab
# Watch test.yml, lint.yml, build.yml run
# Verify all pass ✅
```

### 4. First Release

```bash
# After merge to main
git checkout main
git pull origin main

# Create release
git tag -a v2.2.0 -m "Release v2.2.0"
git push origin v2.2.0

gh release create v2.2.0 \
  --title "v2.2.0: AssertLang Rebrand + CI/CD" \
  --notes "## Major Changes
- Complete rebrand: Promptware → AssertLang
- Comprehensive CI/CD infrastructure
- Multi-Python, multi-OS testing
- Automated PyPI publishing

See CHANGELOG.md for details."

# Watch publish.yml run
# Package automatically published to PyPI ✅
```

---

## 🐛 Troubleshooting

### Tests Failing?

```bash
# Check logs in GitHub Actions
# Run locally to debug:
pytest tests/test_name.py::test_function -v
```

### Lint Failures?

```bash
# Fix formatting:
black assertlang/ tests/
isort assertlang/ tests/

# Check:
black --check assertlang/
flake8 assertlang/
```

### Publish Failing?

```bash
# Check PYPI_API_TOKEN is set correctly
# Verify version doesn't already exist on PyPI
# Test with Test PyPI first:
gh workflow run publish.yml -f test_pypi=true
```

### Badges Not Updating?

```bash
# Badges update after first workflow run
# Wait for workflows to complete
# Hard refresh browser (Cmd+Shift+R)
```

---

## 📚 Full Documentation

- **Comprehensive guide:** `.github/CICD.md`
- **Setup summary:** `CICD_SETUP_COMPLETE.md`
- **This quick start:** `CICD_QUICK_START.md`

---

## ✅ Checklist

Before first release:

- [ ] Add PYPI_API_TOKEN to GitHub secrets
- [ ] (Optional) Add CODECOV_TOKEN
- [ ] Merge CI/CD branch to main
- [ ] Verify workflows pass
- [ ] Create first release tag
- [ ] Verify PyPI publication
- [ ] Check badges display correctly

---

**Questions?** See `.github/CICD.md` or open an issue.

**Status:** Ready to deploy! Just add secrets and merge.
