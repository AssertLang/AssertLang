# AssertLang CI/CD Documentation

**Last Updated:** 2025-10-16
**Status:** ✅ Complete

---

## Overview

AssertLang uses GitHub Actions for comprehensive CI/CD automation covering testing, linting, building, and publishing.

## Workflows

### 1. **test.yml** - Comprehensive Testing

**Triggers:**
- Push to `main` or `develop`
- Pull requests to `main` or `develop`
- Manual dispatch

**What it does:**
- Tests across Python 3.9, 3.10, 3.11, 3.12, 3.13
- Tests on Ubuntu, macOS, Windows
- Runs full test suite with coverage
- Uploads coverage to Codecov
- Verifies CLI commands work
- Runs integration tests for contract compilation

**Status Badge:**
```markdown
[![Tests](https://github.com/AssertLang/AssertLang/actions/workflows/test.yml/badge.svg)](https://github.com/AssertLang/AssertLang/actions/workflows/test.yml)
```

### 2. **lint.yml** - Code Quality

**Triggers:**
- Push to `main` or `develop`
- Pull requests to `main` or `develop`

**What it does:**
- Black formatting check
- isort import sorting check
- flake8 linting
- mypy type checking
- Security scanning (safety, bandit)

**Status Badge:**
```markdown
[![Code Quality](https://github.com/AssertLang/AssertLang/actions/workflows/lint.yml/badge.svg)](https://github.com/AssertLang/AssertLang/actions/workflows/lint.yml)
```

### 3. **build.yml** - Package Building

**Triggers:**
- Push to `main` or `develop`
- Pull requests to `main` or `develop`
- Manual dispatch

**What it does:**
- Builds Python wheel and source distribution
- Validates package with twine
- Checks wheel contents
- Tests installation on Ubuntu, macOS, Windows
- Uploads build artifacts

**Status Badge:**
```markdown
[![Build](https://github.com/AssertLang/AssertLang/actions/workflows/build.yml/badge.svg)](https://github.com/AssertLang/AssertLang/actions/workflows/build.yml)
```

### 4. **publish.yml** - PyPI Publishing

**Triggers:**
- GitHub release published
- Manual dispatch (with Test PyPI option)

**What it does:**
- Builds package
- Publishes to PyPI (or Test PyPI)
- Verifies publication
- Uploads artifacts to GitHub release

**Required Secrets:**
- `PYPI_API_TOKEN` - PyPI API token for publishing
- `TEST_PYPI_API_TOKEN` - Test PyPI token (optional)

**Status Badge:**
```markdown
[![Publish](https://github.com/AssertLang/AssertLang/actions/workflows/publish.yml/badge.svg)](https://github.com/AssertLang/AssertLang/actions/workflows/publish.yml)
```

### 5. **docs.yml** - Documentation

**Triggers:**
- Push to `main` affecting docs
- Manual dispatch

**What it does:**
- Validates markdown links
- Checks example code
- Builds documentation site
- (Optional) Deploys to GitHub Pages

### 6. **dependabot.yml** - Dependency Updates

**Schedule:** Weekly (Mondays)

**What it does:**
- Checks Python dependencies for updates
- Checks GitHub Actions for updates
- Creates PRs for updates
- Auto-labels PRs

---

## Setting Up Secrets

### Required Secrets

1. **PYPI_API_TOKEN**
   ```bash
   # Generate at: https://pypi.org/manage/account/token/
   # Add to: GitHub repo → Settings → Secrets → Actions
   ```

2. **CODECOV_TOKEN** (optional, for coverage reports)
   ```bash
   # Get from: https://codecov.io/gh/AssertLang/AssertLang
   # Add to: GitHub repo → Settings → Secrets → Actions
   ```

3. **TEST_PYPI_API_TOKEN** (optional, for testing)
   ```bash
   # Generate at: https://test.pypi.org/manage/account/token/
   # Add to: GitHub repo → Settings → Secrets → Actions
   ```

---

## Release Process

### Automated Release Workflow

1. **Create a release tag:**
   ```bash
   git tag -a v2.2.0 -m "Release v2.2.0: Feature XYZ"
   git push origin v2.2.0
   ```

2. **Create GitHub Release:**
   ```bash
   gh release create v2.2.0 \
     --title "v2.2.0: Feature XYZ" \
     --notes "Release notes here"
   ```

3. **Automation kicks in:**
   - `publish.yml` triggers
   - Builds package
   - Publishes to PyPI
   - Verifies publication
   - Uploads artifacts to release

### Manual Release (Emergency)

```bash
# Build locally
python -m build

# Publish to Test PyPI first
twine upload --repository testpypi dist/*

# Verify on Test PyPI
pip install --index-url https://test.pypi.org/simple/ assertlang

# Publish to PyPI
twine upload dist/*
```

---

## Branch Protection

**Recommended settings for `main` branch:**

- ✅ Require pull request reviews (1 approver)
- ✅ Require status checks to pass:
  - `test` (all Python versions)
  - `lint`
  - `build`
- ✅ Require branches to be up to date
- ✅ Require linear history
- ⚠️ Do not allow force pushes
- ⚠️ Do not allow deletions

---

## Local Development

### Running Tests Locally

```bash
# Install dev dependencies
pip install -e ".[dev]"

# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=assertlang --cov-report=html

# Run specific test file
pytest tests/test_cli.py -v
```

### Running Linters Locally

```bash
# Format code
black assertlang/ tests/
isort assertlang/ tests/

# Check formatting
black --check assertlang/ tests/

# Lint
flake8 assertlang/ tests/

# Type check
mypy assertlang/
```

### Building Locally

```bash
# Clean old builds
rm -rf dist/ build/ *.egg-info

# Build package
python -m build

# Check package
twine check dist/*

# Install locally
pip install dist/*.whl
```

---

## Debugging CI Failures

### Test Failures

1. Check the test workflow logs
2. Look for specific test failures
3. Run failing tests locally:
   ```bash
   pytest tests/test_name.py::test_function_name -v
   ```

### Lint Failures

1. Run linters locally to see full output
2. Fix formatting:
   ```bash
   black assertlang/ tests/
   isort assertlang/ tests/
   ```

### Build Failures

1. Check build logs for import errors
2. Verify package structure:
   ```bash
   pip install check-wheel-contents
   check-wheel-contents dist/*.whl
   ```

### Publish Failures

1. Check that secrets are configured correctly
2. Verify PyPI token hasn't expired
3. Check if version already exists on PyPI
4. Test with Test PyPI first

---

## Monitoring

### GitHub Actions

- View all workflows: https://github.com/AssertLang/AssertLang/actions
- View specific workflow runs: Click on workflow → specific run
- Download artifacts from completed runs

### PyPI

- Package page: https://pypi.org/project/assertlang/
- Download stats: https://pypistats.org/packages/assertlang

### Codecov

- Coverage dashboard: https://codecov.io/gh/AssertLang/AssertLang
- View coverage trends over time

---

## Maintenance

### Weekly Tasks

- ✅ Review Dependabot PRs
- ✅ Check for failing builds
- ✅ Monitor test coverage

### Monthly Tasks

- ✅ Review and update CI/CD workflows
- ✅ Check for outdated GitHub Actions
- ✅ Review security reports

### Before Major Releases

- ✅ Run full test suite locally
- ✅ Test on all supported Python versions
- ✅ Build and test package installation
- ✅ Review changelog
- ✅ Update version numbers

---

## Troubleshooting

### "Secret not found" error

**Problem:** Workflow can't find PYPI_API_TOKEN
**Solution:** Add token to repo secrets (Settings → Secrets → Actions)

### Tests fail on Windows but pass on Linux

**Problem:** Path separator issues
**Solution:** Use `pathlib.Path` instead of string concatenation

### Coverage not uploading

**Problem:** CODECOV_TOKEN missing or invalid
**Solution:** Get new token from codecov.io and update secret

### Package not publishing

**Problem:** Version already exists on PyPI
**Solution:** Bump version number in `pyproject.toml` and `setup.py`

---

## Contact

**Questions about CI/CD?**
- Open an issue: https://github.com/AssertLang/AssertLang/issues
- Label with `ci/cd`

**Security issues?**
- Report privately: https://github.com/AssertLang/AssertLang/security/advisories
