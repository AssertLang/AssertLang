# Release Checklist - AssertLang

**IMPORTANT**: Use this checklist for every production release to ensure version sync.

---

## Pre-Release Checks

### 1. Version Numbers (ALL MUST MATCH)

Update version in **ALL** of these files:

- [ ] `pyproject.toml` - `version = "X.Y.Zb#"`
- [ ] `setup.py` - `version="X.Y.Zb#"`
- [ ] `promptware/__init__.py` - `__version__ = "X.Y.Zb#"`
- [ ] `Current_Work.md` - **Version**: X.Y.Zb#

**Version Format:**
- Production: `2.1.0`
- Beta: `2.1.0b1`, `2.1.0b2`, etc.
- Alpha: `2.1.0a1`, `2.1.0a2`, etc.

### 2. Documentation Updates

- [ ] `CHANGELOG.md` - Add new version section at top
- [ ] `README.md` - Verify current (no updates usually needed)
- [ ] `Current_Work.md` - Update session, version, release sync status

### 3. Code Quality

- [ ] All tests passing
- [ ] No uncommitted changes
- [ ] Clean working tree (`git status`)

---

## Release Process

### Step 1: Commit Version Bump

```bash
git add pyproject.toml setup.py promptware/__init__.py Current_Work.md
git commit -m "chore: Bump version to X.Y.Zb# for PyPI release"
git push upstream main
```

### Step 2: Build Package

```bash
rm -rf dist/ build/ *.egg-info
python -m build
```

**Verify files:**
```bash
ls -lh dist/
# Should see:
# - promptware_dev-X.Y.Zb#-py3-none-any.whl
# - promptware_dev-X.Y.Zb#.tar.gz
```

### Step 3: Upload to PyPI

```bash
twine upload dist/*
```

**Verify URL**: https://pypi.org/project/assertlang/X.Y.Zb#/

### Step 4: Create Git Tag

**IMPORTANT**: Tag version MUST match PyPI version exactly!

```bash
git tag -a vX.Y.Zb# -m "Release message here"
git push upstream vX.Y.Zb#
```

**Format Examples:**
- `v2.1.0b2` for PyPI version `2.1.0b2`
- `v2.1.0` for PyPI version `2.1.0`

### Step 5: Create GitHub Release

```bash
gh release create vX.Y.Zb# \
  --repo AssertLang/AssertLang \
  --title "vX.Y.Zb# - Release Title" \
  --notes "$(cat RELEASE_NOTES.md)" \
  --prerelease  # Only for beta/alpha
```

**Verify URL**: https://github.com/AssertLang/AssertLang/releases/tag/vX.Y.Zb#

---

## Post-Release Verification

### Version Sync Check

Verify ALL versions match:

```bash
# Check local files
grep 'version.*=' pyproject.toml
grep 'version=' setup.py
grep '__version__' promptware/__init__.py
git tag --list | tail -1

# Check remote
# - GitHub: https://github.com/AssertLang/AssertLang/releases
# - PyPI: https://pypi.org/project/assertlang/
```

**All should show**: `X.Y.Zb#`

### Update Current_Work.md

Add release sync status section:

```markdown
## 📦 Release Sync Status

**GitHub Release**: [vX.Y.Zb#](https://github.com/AssertLang/AssertLang/releases/tag/vX.Y.Zb#)
**PyPI Package**: [X.Y.Zb#](https://pypi.org/project/assertlang/X.Y.Zb#/)
**Installation**: `pip install assertlang==X.Y.Zb#`

✅ All versions in sync across:
- `pyproject.toml` - version = "X.Y.Zb#"
- `setup.py` - version = "X.Y.Zb#"
- `promptware/__init__.py` - __version__ = "X.Y.Zb#"
- Git tag - vX.Y.Zb#
- GitHub release - vX.Y.Zb#
- PyPI package - X.Y.Zb#
- CHANGELOG.md - ## [X.Y.Zb#]
```

### Test Installation

```bash
# Create clean venv
python -m venv /tmp/test-install
source /tmp/test-install/bin/activate

# Install from PyPI
pip install assertlang==X.Y.Zb#

# Verify version
python -c "import promptware; print(promptware.__version__)"
# Should output: X.Y.Zb#

# Verify CLI
promptware --version
# Should output: promptware X.Y.Zb#

deactivate
```

---

## Common Mistakes to Avoid

### ❌ Version Mismatch
- GitHub tag: `v2.1.0-beta.1`
- PyPI version: `2.1.0b2`
- **WRONG**: Versions don't match!

### ✅ Correct Versioning
- GitHub tag: `v2.1.0b2`
- PyPI version: `2.1.0b2`
- **CORRECT**: Perfect match!

### ❌ Forgetting Files
Missing version update in any of:
- `pyproject.toml`
- `setup.py`
- `promptware/__init__.py`

### ✅ Update All Files
Check every file in version update commit.

### ❌ Wrong Tag Format
- `v2.1.0-beta-2` (dashes)
- `v2.1.0_b2` (underscore)

### ✅ Correct Tag Format
- `v2.1.0b2` (matches PyPI exactly)

---

## Rollback Procedure

If release has critical issues:

### 1. Yank PyPI Release
```bash
# This removes from pip install but keeps version reserved
pip install twine
twine yank promptware-dev X.Y.Zb#
```

### 2. Delete GitHub Release
```bash
gh release delete vX.Y.Zb# --repo AssertLang/AssertLang --yes
```

### 3. Delete Git Tag
```bash
git tag -d vX.Y.Zb#
git push upstream :refs/tags/vX.Y.Zb#
```

### 4. Revert Version Bump
```bash
git revert <commit-hash>
git push upstream main
```

---

## Version Number Guidelines

Follow [Semantic Versioning](https://semver.org/):

- **MAJOR** (2.0.0): Breaking changes
- **MINOR** (2.1.0): New features, backward compatible
- **PATCH** (2.1.1): Bug fixes, backward compatible

Pre-release suffixes:
- **Alpha** (2.1.0a1): Early testing, unstable
- **Beta** (2.1.0b1): Feature complete, testing
- **RC** (2.1.0rc1): Release candidate

Increment:
- `2.1.0b1` → `2.1.0b2` (next beta)
- `2.1.0b2` → `2.1.0` (promote to stable)
- `2.1.0` → `2.1.1` (bug fix)
- `2.1.0` → `2.2.0` (new features)
- `2.1.0` → `3.0.0` (breaking changes)

---

**Last Updated**: 2025-10-08
**Maintained By**: Claude Code
