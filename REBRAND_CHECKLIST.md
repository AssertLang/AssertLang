# Rebrand Checklist: Promptware → AssertLang

**Date:** October 16, 2025
**Status:** IN PROGRESS

---

## ✅ Completed

1. **Domains purchased**
   - assertlang.com
   - assertlang.dev

2. **GitHub repo made PRIVATE**
   - Repository: AssertLang/AssertLang (now private)

3. **NPM check**
   - No `promptware` package exists ✅

---

## 🔄 Manual Cleanup Required (DO THESE FIRST)

### 1. PyPI Package Removal

**Status:** User confirmed package exists as `promptware-dev`

**Steps to remove:**

**Option A: Delete via PyPI Website (Recommended)**
1. Login to PyPI at https://pypi.org
2. Go to https://pypi.org/manage/project/promptware-dev/settings/
3. Scroll to "Delete project" section
4. Enter project name to confirm: `promptware-dev`
5. Click "Delete project"

**Option B: Verify if package exists first**
1. Visit https://pypi.org/project/assertlang/ in browser
2. If 404 → nothing to remove ✅
3. If package page exists → use Option A

**Note:** `pip index versions promptware-dev` returns "no matching distribution" but user confirmed it exists. Website check is needed.

---

### 2. Vercel Website Takedown

**Status:** User confirmed Vercel site exists

**Steps to remove:**

**Option A: Delete via Dashboard (Recommended)**
1. Login to https://vercel.com
2. Find Promptware project in dashboard
3. Click project → Settings
4. Scroll to "Delete Project"
5. Confirm deletion

**Option B: Use Vercel CLI**
```bash
npm i -g vercel
vercel login
vercel ls  # List projects
vercel remove <project-name>
```

**Note:** No vercel.json found in repo, likely deployed separately

---

## 🤖 Automated Rebrand (DO AFTER MANUAL CLEANUP)

Once PyPI and Vercel are cleaned up, run automated rebrand script.

### Files to Update

**Package Configuration:**
- `pyproject.toml` - Package name, email, description
- `setup.py` (if exists) - Package metadata

**Code:**
- `promptware/` directory → `assertlang/`
- All Python imports: `from promptware` → `from assertlang`
- CLI commands: `asl build` → `asl build` (or `assertlang build`)

**Documentation:** (76 files found)
- `README.md` - Links, badges, examples
- `Current_Work.md` - Project name
- `CLAUDE.md` - Project name
- `docs/` - All markdown files
- `examples/` - All example files
- `tests/` - Test file headers

**Domain References:** (76 files found)
- Replace `assertlang.dev` → `assertlang.dev`
- Replace `assertlang.com` → `assertlang.com`
- Replace `promptware.io` → `assertlang.io` (if exists)

**GitHub References:**
- `github.com/AssertLang/AssertLang` → `github.com/AssertLang/AssertLang`
- PyPI links: `pypi.org/project/assertlang` → `pypi.org/project/assertlang`

---

## 📋 Rebrand Script

```bash
#!/bin/bash
# rebrand.sh - Automated Promptware → AssertLang rebrand

set -e

echo "🔄 Starting Promptware → AssertLang rebrand..."

# 1. Rename package directory
echo "📦 Renaming package directory..."
if [ -d "promptware" ]; then
  git mv promptware assertlang
fi

# 2. Update pyproject.toml
echo "📝 Updating pyproject.toml..."
sed -i.bak 's/name = "promptware-dev"/name = "assertlang"/' pyproject.toml
sed -i.bak 's/hello@assertlang.dev/hello@assertlang.dev/' pyproject.toml
sed -i.bak 's/Promptware Contributors/AssertLang Contributors/' pyproject.toml
sed -i.bak 's/promptware = "promptware.cli:main"/asl = "assertlang.cli:main"/' pyproject.toml

# 3. Update Python imports
echo "🐍 Updating Python imports..."
find . -name "*.py" -not -path "./.venv/*" -not -path "./node_modules/*" | \
  xargs sed -i.bak 's/from promptware/from assertlang/g'
find . -name "*.py" -not -path "./.venv/*" -not -path "./node_modules/*" | \
  xargs sed -i.bak 's/import promptware/import assertlang/g'

# 4. Update CLI references
echo "💻 Updating CLI references..."
find . -name "*.md" -o -name "*.py" | \
  xargs sed -i.bak 's/asl build/asl build/g'
find . -name "*.md" -o -name "*.py" | \
  xargs sed -i.bak 's/asl test/asl test/g'
find . -name "*.md" -o -name "*.py" | \
  xargs sed -i.bak 's/asl compile/asl compile/g'

# 5. Update domain references
echo "🌐 Updating domain references..."
find . -type f \( -name "*.md" -o -name "*.py" -o -name "*.toml" \) | \
  xargs sed -i.bak 's/promptware\.dev/assertlang.dev/g'
find . -type f \( -name "*.md" -o -name "*.py" -o -name "*.toml" \) | \
  xargs sed -i.bak 's/promptware\.com/assertlang.com/g'

# 6. Update GitHub references
echo "🐙 Updating GitHub references..."
find . -name "*.md" | \
  xargs sed -i.bak 's|github\.com/AssertLang/AssertLang|github.com/AssertLang/AssertLang|g'

# 7. Update PyPI references
echo "📦 Updating PyPI references..."
find . -name "*.md" | \
  xargs sed -i.bak 's|pypi\.org/project/promptware-dev|pypi.org/project/assertlang|g'

# 8. Update all "Promptware" text references
echo "📝 Updating Promptware → AssertLang in docs..."
find . -name "*.md" | \
  xargs sed -i.bak 's/Promptware/AssertLang/g'

# 9. Clean up backup files
echo "🧹 Cleaning up backup files..."
find . -name "*.bak" -delete

echo "✅ Rebrand complete!"
echo ""
echo "Next steps:"
echo "1. Review changes: git diff"
echo "2. Run tests: pytest"
echo "3. Verify package builds: python -m build"
echo "4. Commit changes: git add . && git commit -m 'Rebrand to AssertLang'"
```

---

## 🧪 Post-Rebrand Verification

1. **Test suite passes:**
   ```bash
   pytest
   # Should see: 248 tests passing
   ```

2. **Package builds successfully:**
   ```bash
   python -m build
   ls dist/  # Should see assertlang-*.tar.gz and assertlang-*.whl
   ```

3. **CLI works:**
   ```bash
   pip install -e .
   asl --version  # Or: assertlang --version
   ```

4. **Documentation is updated:**
   ```bash
   grep -r "Promptware" docs/  # Should find minimal results
   grep -r "promptware" README.md  # Should find minimal results
   ```

---

## 📊 Impact Summary

**Files to update:**
- 76+ markdown files (docs, README, guides)
- 200+ Python files (code, tests)
- 1 package config (pyproject.toml)
- 1 CLI entrypoint

**Search/Replace patterns:**
- `Promptware` → `AssertLang`
- `promptware` → `assertlang`
- `assertlang.dev` → `assertlang.dev`
- `AssertLang/AssertLang` → `AssertLang/AssertLang`
- `promptware-dev` (PyPI) → `assertlang` (PyPI)

**Estimated time:** 30-60 minutes (mostly automated)

---

## 🚨 Warnings

1. **DO NOT run rebrand script until:**
   - PyPI package is removed/verified
   - Vercel site is taken down
   - No other public references exist

2. **Backup before rebrand:**
   ```bash
   git branch backup-pre-rebrand
   ```

3. **Test thoroughly:**
   - All tests must pass
   - CLI must work
   - Package must build

---

## 🔗 New Infrastructure (After Rebrand)

1. **GitHub org:** github.com/AssertLang (user created)
2. **PyPI package:** pypi.org/project/assertlang (to be published)
3. **NPM package:** @assertlang/core (to be published)
4. **Website:** assertlang.dev (to be created)
5. **Documentation:** docs.assertlang.dev (to be created)

---

**Last Updated:** 2025-10-16
**Status:** Awaiting manual PyPI + Vercel cleanup
