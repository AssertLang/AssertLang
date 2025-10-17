# Root Directory Cleanup Plan

**Date:** 2025-10-17
**Goal:** Make repository 1000% professional for enterprise review

**Current State:** 208 files in root directory ❌
**Target State:** ~15 essential files in root directory ✅

---

## KEEP in Root (Professional Essentials)

### Documentation (Required)
- README.md ✅
- LICENSE ✅
- CONTRIBUTING.md ✅
- CODE_OF_CONDUCT.md ✅
- SECURITY.md ✅
- CHANGELOG.md ✅

### Configuration (Required)
- pyproject.toml ✅
- .gitignore ✅
- .gitattributes (if exists) ✅

### Project Info (Optional but Good)
- CURRENT_STATUS.md ✅ (Recent project status)
- CLAUDE.md ✅ (Development instructions)

### Directories (Keep)
- assertlang/ ✅ (Main package)
- tests/ ✅ (Test suite)
- docs/ ✅ (Documentation)
- examples/ ✅ (Examples)
- scripts/ ✅ (Utility scripts)
- .github/ ✅ (GitHub configs)
- .vscode/ ✅ (VS Code configs)

---

## ARCHIVE to .archive/ (Development History)

### Session/Phase Files (26+ files)
- PHASE_*.md
- SESSION_*.md
- TASK_*.md
- *_COMPLETE.md
- *_SUMMARY.md
- *_REPORT.md
- *_ASSESSMENT.md

### Release Documentation
- RELEASE_*.md
- VERSION_*.md
- ANNOUNCEMENT_*.md

### Architecture Documents (Keep recent, archive old)
- ARCHITECTURE_*.md
- DESIGN_*.md
- IMPLEMENTATION_*.md

### Research/Planning
- BRANDING_RESEARCH_REPORT.md
- RESEARCH_*.md
- PLANNING_*.md

---

## DELETE (Temporary/Test Files)

### Debug Files
- debug_*.py
- test_*.py (in root, keep in tests/)
- audit_*.py

### Demo Files
- demo_*.pw
- demo_*.py
- example_*.pw (in root, keep in examples/)
- simple_*.pw (in root)

### Temporary Files
- __pycache__/
- *.egg-info/
- dist/
- build/
- .pytest_cache/

### Config Fragments
- *.json (except package.json)
- *.txt (except requirements.txt)

---

## Cleanup Actions

### Step 1: Create Archive Directory
```bash
mkdir -p .archive/sessions
mkdir -p .archive/releases
mkdir -p .archive/architecture
mkdir -p .archive/research
```

### Step 2: Move Session Files
```bash
mv PHASE_*.md SESSION_*.md TASK_*.md .archive/sessions/ 2>/dev/null || true
mv *_COMPLETE.md *_SUMMARY.md .archive/sessions/ 2>/dev/null || true
```

### Step 3: Move Release Files
```bash
mv RELEASE_*.md VERSION_*.md ANNOUNCEMENT_*.md .archive/releases/ 2>/dev/null || true
```

### Step 4: Move Architecture Files (old ones)
```bash
# Keep recent, archive old
mv ARCHITECTURE_*.md DESIGN_*.md .archive/architecture/ 2>/dev/null || true
```

### Step 5: Move Research Files
```bash
mv BRANDING_*.md RESEARCH_*.md .archive/research/ 2>/dev/null || true
```

### Step 6: Delete Temporary Files
```bash
rm -rf __pycache__ *.egg-info dist build .pytest_cache
rm -f debug_*.py test_*.py audit_*.py
rm -f demo_*.pw demo_*.py
rm -f *_test.py
```

### Step 7: Clean Up Test .pw Files
```bash
# Move to tests/ or delete
rm -f simple_*.pw data_processor.pw example_*.pw
```

---

## Expected Result

### Root Directory (After Cleanup)
```
AssertLang/
├── .github/               # GitHub configs
├── .vscode/               # VS Code configs
├── assertlang/            # Main package
├── docs/                  # Documentation
├── examples/              # Examples
├── scripts/               # Utility scripts
├── tests/                 # Test suite
├── .gitignore
├── CHANGELOG.md
├── CLAUDE.md
├── CODE_OF_CONDUCT.md
├── CONTRIBUTING.md
├── CURRENT_STATUS.md
├── LICENSE
├── pyproject.toml
├── README.md
├── SECURITY.md
└── logo2.svg
```

**Total Files in Root:** ~15 (vs 208 currently)

---

## .gitignore Updates

Add to .gitignore:
```
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
*.egg-info/
dist/
build/

# Testing
.pytest_cache/
.coverage
htmlcov/

# IDE
.vscode/*
!.vscode/extensions/
.idea/

# Archives (keep in repo)
# .archive/ is intentionally tracked

# Temporary
*.tmp
*.log
```

---

## Professional Checklist

After cleanup, verify:
- [ ] Root has <20 files
- [ ] No debug/test files in root
- [ ] No session/phase files in root
- [ ] All essential docs present
- [ ] .archive/ directory contains history
- [ ] .gitignore updated
- [ ] README.md is first file shown
- [ ] Directory structure clear

---

**Status:** READY TO EXECUTE
**Impact:** High (major improvement to professional appearance)
**Risk:** Low (archiving, not deleting)
