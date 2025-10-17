# AssertLang CI/CD Workflow - Complete Guide

**Status:** ✅ Infrastructure deployed and ready
**Branch:** feature/multi-agent-contracts-pivot
**Version:** 2.2.0-alpha4

---

## 🎯 Your CI/CD Workflow

### 1️⃣ **Development Workflow**

```bash
# 1. Make changes on feature branch
git checkout -b feature/new-feature

# 2. Write code, tests, docs
# ... coding ...

# 3. Commit changes
git add .
git commit -m "Add new feature"

# 4. Push to origin
git push origin feature/new-feature

# 5. Create PR
gh pr create --repo AssertLang/AssertLang \
  --base main \
  --head feature/new-feature \
  --title "Add new feature" \
  --fill
```

**What happens automatically:**
- ✅ Tests run on Python 3.9-3.13 (Ubuntu, macOS, Windows)
- ✅ Linting (black, flake8, isort, mypy)
- ✅ Security scanning (safety, bandit)
- ✅ Build verification
- ✅ Coverage report to Codecov
- ✅ Status checks on PR

---

### 2️⃣ **Release Workflow**

#### Option A: Automated Release (Recommended)

```bash
# 1. Merge PR to main
gh pr merge 123 --squash

# 2. Pull latest main
git checkout main
git pull origin main

# 3. Update version in pyproject.toml
# Edit: version = "2.3.0"

# 4. Commit version bump
git add pyproject.toml
git commit -m "Bump version to 2.3.0"
git push origin main

# 5. Create tag
git tag -a v2.3.0 -m "Release v2.3.0: Feature XYZ"
git push origin v2.3.0

# 6. Create GitHub release
gh release create v2.3.0 \
  --repo AssertLang/AssertLang \
  --title "v2.3.0: Feature XYZ" \
  --notes "## What's New
- Feature A
- Feature B
- Bug fix C

See CHANGELOG.md for full details."
```

**What happens automatically:**
1. ✅ GitHub Actions detects release
2. ✅ Builds package (wheel + source)
3. ✅ Runs twine check
4. ✅ Publishes to PyPI using `PYPI_API_TOKEN`
5. ✅ Waits 60s for PyPI to update
6. ✅ Verifies installation from PyPI
7. ✅ Uploads artifacts to GitHub release

**Result:** Package live on PyPI in ~5 minutes!

#### Option B: Manual Trigger

```bash
# Go to GitHub Actions
# Click "Publish to PyPI" workflow
# Click "Run workflow"
# Select: branch (main), test_pypi (false)
```

#### Option C: Local Release (Fallback)

```bash
# Use the release script
./scripts/release.sh v2.3.0
```

---

### 3️⃣ **Testing Workflow**

#### Local Testing

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=assertlang --cov-report=html
open htmlcov/index.html

# Run specific test
pytest tests/test_dsl_parser.py::test_parse_function -v

# Run linters
black --check assertlang/ tests/
flake8 assertlang/ tests/
mypy assertlang/

# Run integration tests
./scripts/integration_run.sh
```

#### CI Testing

**Automatic on:**
- Push to main/develop
- Pull requests to main/develop
- Manual trigger via Actions tab

**What runs:**
- 15 test jobs (5 Python versions × 3 OS)
- ~302 tests total
- Coverage report
- Integration tests (contract compilation, multi-language generation)
- CLI verification

---

### 4️⃣ **Monitoring**

**GitHub Actions:**
https://github.com/AssertLang/AssertLang/actions

**Test Results:**
- Check "Tests" workflow badge in README
- View detailed logs in Actions tab

**Coverage:**
https://codecov.io/gh/AssertLang/AssertLang

**PyPI Stats:**
https://pypistats.org/packages/assertlang

**Dependabot:**
https://github.com/AssertLang/AssertLang/security/dependabot

---

## 📋 Workflow Triggers

### Automatic Triggers

| Workflow | Trigger | Purpose |
|----------|---------|---------|
| **Tests** | Push to main/develop, PRs | Run full test suite |
| **Lint** | Push to main/develop, PRs | Code quality checks |
| **Build** | Push to main/develop, PRs | Verify package builds |
| **Docs** | Push to main, manual | Build documentation |
| **Publish** | GitHub release created | Publish to PyPI |

### Manual Triggers

All workflows support `workflow_dispatch` - run from Actions tab anytime.

---

## 🔐 Required Secrets

### PYPI_API_TOKEN (REQUIRED)

```bash
# 1. Get token from PyPI
# Visit: https://pypi.org/manage/account/token/
# Create new token:
#   - Name: assertlang-publishing
#   - Scope: Entire account (or project: assertlang)

# 2. Add to GitHub
# Visit: https://github.com/AssertLang/AssertLang/settings/secrets/actions
# Click "New repository secret"
# Name: PYPI_API_TOKEN
# Value: pypi-AgEI... (your token)
```

**Without this:** Publish workflow fails ❌

### CODECOV_TOKEN (OPTIONAL)

```bash
# 1. Get token from Codecov
# Visit: https://codecov.io/
# Sign in with GitHub
# Add AssertLang/AssertLang repository
# Copy token

# 2. Add to GitHub
# Name: CODECOV_TOKEN
# Value: (your token)
```

**Without this:** Coverage reports won't upload (tests still pass ✅)

### TEST_PYPI_API_TOKEN (OPTIONAL)

```bash
# For testing releases on Test PyPI
# Get from: https://test.pypi.org/manage/account/token/
# Add to GitHub as: TEST_PYPI_API_TOKEN
```

---

## 🚀 Quick Commands

### Development

```bash
# Create feature branch
git checkout -b feature/my-feature

# Make changes, commit
git add .
git commit -m "Add my feature"

# Push and create PR
git push origin feature/my-feature
gh pr create --fill

# View CI status
gh pr checks
```

### Release

```bash
# Simple release
git checkout main
git pull
# Update version in pyproject.toml
git add pyproject.toml
git commit -m "Bump version to 2.3.0"
git push
git tag v2.3.0
git push --tags
gh release create v2.3.0 --generate-notes
```

### Testing

```bash
# Local quick test
pytest tests/ -x  # Stop on first failure

# Full local test (like CI)
pytest tests/ --cov=assertlang --cov-report=term -v

# Lint like CI
black --check assertlang/ tests/
flake8 assertlang/ tests/
```

---

## 🎨 Badges

All badges configured in README:

```markdown
[![Tests](https://github.com/AssertLang/AssertLang/actions/workflows/test.yml/badge.svg)](https://github.com/AssertLang/AssertLang/actions/workflows/test.yml)
[![Code Quality](https://github.com/AssertLang/AssertLang/actions/workflows/lint.yml/badge.svg)](https://github.com/AssertLang/AssertLang/actions/workflows/lint.yml)
[![Build](https://github.com/AssertLang/AssertLang/actions/workflows/build.yml/badge.svg)](https://github.com/AssertLang/AssertLang/actions/workflows/build.yml)
[![codecov](https://codecov.io/gh/AssertLang/AssertLang/branch/main/graph/badge.svg)](https://codecov.io/gh/AssertLang/AssertLang)
```

Badges update automatically after workflow runs.

---

## ⚠️ Before First Release

**Checklist:**

- [ ] Add `PYPI_API_TOKEN` to GitHub secrets ⚠️ **REQUIRED**
- [ ] (Optional) Add `CODECOV_TOKEN`
- [ ] Merge `feature/multi-agent-contracts-pivot` to `main`
- [ ] Wait for workflows to pass
- [ ] Verify badges show green ✅
- [ ] Create first release tag
- [ ] Watch publish workflow
- [ ] Verify on PyPI: https://pypi.org/project/assertlang/

---

## 🐛 Troubleshooting

### Tests Failing in CI

```bash
# Run exact CI command locally
pytest tests/ --cov=assertlang --cov-report=xml --tb=short -v

# Check specific Python version
pyenv install 3.9.18
pyenv shell 3.9.18
pytest tests/
```

### Lint Failures

```bash
# Auto-fix formatting
black assertlang/ tests/
isort assertlang/ tests/

# Verify
black --check assertlang/ tests/
flake8 assertlang/ tests/
```

### Publish Failing

**Common issues:**
1. **No PYPI_API_TOKEN** → Add secret
2. **Version already exists** → Bump version
3. **Invalid package** → Run `twine check dist/*`

**Test first:**
```bash
# Publish to Test PyPI
gh workflow run publish.yml -f test_pypi=true
```

### Badge Not Updating

- Wait for workflow to complete
- Hard refresh browser (Cmd+Shift+R)
- Check workflow ran on main branch

---

## 📊 Workflow Status

**Current State:**

| Component | Status | Notes |
|-----------|--------|-------|
| GitHub Actions | ✅ Deployed | 5 workflows configured |
| Test Workflow | ✅ Ready | Python 3.9-3.13, Ubuntu/macOS/Windows |
| Lint Workflow | ✅ Ready | black, flake8, isort, mypy, safety, bandit |
| Build Workflow | ✅ Ready | Package build verification |
| Publish Workflow | ⚠️ Needs secret | Add PYPI_API_TOKEN |
| Docs Workflow | ✅ Ready | Manual trigger |
| Dependabot | ✅ Enabled | Weekly dependency updates |
| Codecov | ⚠️ Optional | Add CODECOV_TOKEN for coverage |

**Next Action:**
→ Add `PYPI_API_TOKEN` secret before first release

---

## 📚 Documentation

- **Quick Start:** `CICD_QUICK_START.md`
- **Full Setup:** `CICD_SETUP_COMPLETE.md`
- **Deployment:** `docs/how-to/deployment/ci-cd.md`
- **This Guide:** `CICD_WORKFLOW_SUMMARY.md`

---

## ✅ Summary

**Your workflow:**

1. **Develop** on feature branches
2. **Create PR** → CI runs automatically
3. **Merge to main** → All checks pass
4. **Create release** → Package publishes to PyPI
5. **Monitor** via Actions tab and badges

**Zero manual steps for:**
- Testing (15 environments)
- Linting
- Building
- Publishing to PyPI
- Uploading release artifacts

**Just add PYPI_API_TOKEN and you're ready to ship! 🚀**
