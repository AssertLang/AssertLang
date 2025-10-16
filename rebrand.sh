#!/bin/bash
# rebrand.sh - Automated Promptware → AssertLang rebrand
# Run this AFTER manual PyPI and Vercel cleanup

set -e

echo "🔄 Starting Promptware → AssertLang rebrand..."
echo ""
echo "⚠️  WARNING: This will modify 200+ files. Make sure you have:"
echo "   1. ✅ Removed promptware-dev from PyPI"
echo "   2. ✅ Taken down Vercel website"
echo "   3. ✅ Created backup: git branch backup-pre-rebrand"
echo ""
read -p "Continue? (y/n) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Aborted."
    exit 1
fi

# Create backup branch
echo "📦 Creating backup branch..."
git branch backup-pre-rebrand 2>/dev/null || echo "Backup branch already exists"

echo ""
echo "🚀 Starting rebrand..."
echo ""

# 1. Rename package directory
echo "📦 [1/10] Renaming package directory: promptware → assertlang..."
if [ -d "promptware" ]; then
  git mv promptware assertlang 2>/dev/null || mv promptware assertlang
  echo "   ✅ Package directory renamed"
else
  echo "   ⚠️  promptware/ directory not found, skipping"
fi

# 2. Update pyproject.toml
echo "📝 [2/10] Updating pyproject.toml..."
if [ -f "pyproject.toml" ]; then
  sed -i.bak 's/name = "promptware-dev"/name = "assertlang"/' pyproject.toml
  sed -i.bak 's/hello@promptware.dev/hello@assertlang.dev/' pyproject.toml
  sed -i.bak 's/Promptware Contributors/AssertLang Contributors/' pyproject.toml
  sed -i.bak 's/promptware = "promptware.cli:main"/asl = "assertlang.cli:main"/' pyproject.toml
  sed -i.bak 's/Executable contracts for multi-agent systems/Executable contracts for multi-agent systems/' pyproject.toml
  echo "   ✅ pyproject.toml updated"
else
  echo "   ⚠️  pyproject.toml not found"
fi

# 3. Update Python imports
echo "🐍 [3/10] Updating Python imports (this may take a minute)..."
PYTHON_FILES=$(find . -name "*.py" \
  -not -path "./.venv/*" \
  -not -path "./venv/*" \
  -not -path "./node_modules/*" \
  -not -path "./.git/*" \
  -not -path "./build/*" \
  -not -path "./dist/*" \
  -not -path "./.mcpd/*" | wc -l | tr -d ' ')
echo "   Found $PYTHON_FILES Python files to update..."

find . -name "*.py" \
  -not -path "./.venv/*" \
  -not -path "./venv/*" \
  -not -path "./node_modules/*" \
  -not -path "./.git/*" \
  -not -path "./build/*" \
  -not -path "./dist/*" \
  -not -path "./.mcpd/*" \
  -exec sed -i.bak 's/from promptware/from assertlang/g' {} +

find . -name "*.py" \
  -not -path "./.venv/*" \
  -not -path "./venv/*" \
  -not -path "./node_modules/*" \
  -not -path "./.git/*" \
  -not -path "./build/*" \
  -not -path "./dist/*" \
  -not -path "./.mcpd/*" \
  -exec sed -i.bak 's/import promptware/import assertlang/g' {} +

echo "   ✅ Python imports updated"

# 4. Update CLI command references in docs
echo "💻 [4/10] Updating CLI command references..."
find . \( -name "*.md" -o -name "*.py" \) \
  -not -path "./.venv/*" \
  -not -path "./node_modules/*" \
  -not -path "./.git/*" \
  -not -path "./.mcpd/*" \
  -exec sed -i.bak 's/promptware build/asl build/g' {} +

find . \( -name "*.md" -o -name "*.py" \) \
  -not -path "./.venv/*" \
  -not -path "./node_modules/*" \
  -not -path "./.git/*" \
  -not -path "./.mcpd/*" \
  -exec sed -i.bak 's/promptware test/asl test/g' {} +

find . \( -name "*.md" -o -name "*.py" \) \
  -not -path "./.venv/*" \
  -not -path "./node_modules/*" \
  -not -path "./.git/*" \
  -not -path "./.mcpd/*" \
  -exec sed -i.bak 's/promptware compile/asl compile/g' {} +

find . \( -name "*.md" -o -name "*.py" \) \
  -not -path "./.venv/*" \
  -not -path "./node_modules/*" \
  -not -path "./.git/*" \
  -not -path "./.mcpd/*" \
  -exec sed -i.bak 's/pip install promptware-dev/pip install assertlang/g' {} +

echo "   ✅ CLI commands updated"

# 5. Update domain references
echo "🌐 [5/10] Updating domain references..."
find . -type f \( -name "*.md" -o -name "*.py" -o -name "*.toml" -o -name "*.json" \) \
  -not -path "./.venv/*" \
  -not -path "./node_modules/*" \
  -not -path "./.git/*" \
  -not -path "./build/*" \
  -not -path "./dist/*" \
  -not -path "./.mcpd/*" \
  -exec sed -i.bak 's/promptware\.dev/assertlang.dev/g' {} +

find . -type f \( -name "*.md" -o -name "*.py" -o -name "*.toml" -o -name "*.json" \) \
  -not -path "./.venv/*" \
  -not -path "./node_modules/*" \
  -not -path "./.git/*" \
  -not -path "./build/*" \
  -not -path "./dist/*" \
  -not -path "./.mcpd/*" \
  -exec sed -i.bak 's/promptware\.com/assertlang.com/g' {} +

echo "   ✅ Domain references updated"

# 6. Update GitHub org references
echo "🐙 [6/10] Updating GitHub references..."
find . -name "*.md" \
  -not -path "./.venv/*" \
  -not -path "./node_modules/*" \
  -not -path "./.git/*" \
  -not -path "./.mcpd/*" \
  -exec sed -i.bak 's|github\.com/Promptware-dev/promptware|github.com/AssertLang/AssertLang|g' {} +

find . -name "*.md" \
  -not -path "./.venv/*" \
  -not -path "./node_modules/*" \
  -not -path "./.git/*" \
  -not -path "./.mcpd/*" \
  -exec sed -i.bak 's|Promptware-dev/promptware|AssertLang/AssertLang|g' {} +

echo "   ✅ GitHub references updated"

# 7. Update PyPI references
echo "📦 [7/10] Updating PyPI package references..."
find . -name "*.md" \
  -not -path "./.venv/*" \
  -not -path "./node_modules/*" \
  -not -path "./.git/*" \
  -not -path "./.mcpd/*" \
  -exec sed -i.bak 's|pypi\.org/project/promptware-dev|pypi.org/project/assertlang|g' {} +

echo "   ✅ PyPI references updated"

# 8. Update project name in text
echo "📝 [8/10] Updating 'Promptware' → 'AssertLang' in documentation..."
find . \( -name "*.md" -o -name "*.txt" \) \
  -not -path "./.venv/*" \
  -not -path "./node_modules/*" \
  -not -path "./.git/*" \
  -not -path "./BRANDING_RESEARCH_REPORT.md" \
  -not -path "./REBRAND_DECISION.md" \
  -not -path "./REBRAND_CHECKLIST.md" \
  -not -path "./.mcpd/*" \
  -exec sed -i.bak 's/Promptware/AssertLang/g' {} +

# Special handling for specific files
if [ -f "README.md" ]; then
  sed -i.bak 's|https://img.shields.io/pypi/v/promptware-dev|https://img.shields.io/pypi/v/assertlang|' README.md
  sed -i.bak 's|https://github.com/Promptware-dev/promptware|https://github.com/AssertLang/AssertLang|' README.md
fi

echo "   ✅ Documentation updated"

# 9. Update Python package references in code
echo "🐍 [9/10] Updating package name in Python files..."
find . -name "*.py" \
  -not -path "./.venv/*" \
  -not -path "./venv/*" \
  -not -path "./node_modules/*" \
  -not -path "./.git/*" \
  -not -path "./build/*" \
  -not -path "./dist/*" \
  -not -path "./.mcpd/*" \
  -exec sed -i.bak 's/"promptware"/"assertlang"/g' {} +

echo "   ✅ Package references updated"

# 10. Clean up backup files
echo "🧹 [10/10] Cleaning up backup files..."
BACKUP_COUNT=$(find . -name "*.bak" \
  -not -path "./.venv/*" \
  -not -path "./node_modules/*" \
  -not -path "./.git/*" \
  -not -path "./.mcpd/*" | wc -l | tr -d ' ')
echo "   Found $BACKUP_COUNT backup files to remove..."

find . -name "*.bak" \
  -not -path "./.venv/*" \
  -not -path "./node_modules/*" \
  -not -path "./.git/*" \
  -not -path "./.mcpd/*" \
  -delete

echo "   ✅ Backup files removed"

echo ""
echo "✅ Rebrand complete!"
echo ""
echo "📊 Summary:"
echo "   • Package directory: promptware → assertlang"
echo "   • PyPI package: promptware-dev → assertlang"
echo "   • GitHub: Promptware-dev/promptware → AssertLang/AssertLang"
echo "   • Domain: promptware.dev → assertlang.dev"
echo "   • CLI command: promptware → asl"
echo ""
echo "🧪 Next steps:"
echo "   1. Review changes:"
echo "      git status"
echo "      git diff"
echo ""
echo "   2. Run test suite:"
echo "      pytest"
echo "      # Should see: 248 tests passing"
echo ""
echo "   3. Test CLI:"
echo "      pip install -e ."
echo "      asl --version"
echo ""
echo "   4. Build package:"
echo "      python -m build"
echo "      ls dist/  # Should see assertlang-*.tar.gz"
echo ""
echo "   5. Check for remaining references:"
echo "      grep -r 'promptware' . --exclude-dir=.git --exclude-dir=node_modules --exclude-dir=.venv | grep -v BRANDING_RESEARCH | grep -v REBRAND"
echo ""
echo "   6. Commit changes:"
echo "      git add ."
echo "      git commit -m 'Rebrand: Promptware → AssertLang'"
echo ""
echo "✅ Done!"
