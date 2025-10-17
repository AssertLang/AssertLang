#!/bin/bash
# update_extension.sh - Update file extension from .pw to .al

set -e

echo "🔄 Updating file extension: .pw → .al"
echo ""

# Update all .pw references in markdown files
echo "📝 [1/3] Updating .pw → .al in documentation..."
find . -name "*.md" \
  -not -path "./.git/*" \
  -not -path "./.venv/*" \
  -not -path "./node_modules/*" \
  -not -path "./.mcpd/*" \
  -not -name "*BRANDING*" \
  -not -name "*REBRAND*" \
  -not -name "*SESSION_*" \
  -not -name "*RELEASE_NOTES*" \
  -not -path "./.archive/*" \
  -not -path "./docs/archive/*" \
  -exec sed -i.bak 's/\.pw\b/.al/g' {} +

echo "   ✅ Documentation updated"

# Update .pw references in Python files
echo "🐍 [2/3] Updating .pw → .al in Python code..."
find . -name "*.py" \
  -not -path "./.git/*" \
  -not -path "./.venv/*" \
  -not -path "./node_modules/*" \
  -not -path "./.mcpd/*" \
  -not -path "./build/*" \
  -not -path "./dist/*" \
  -exec sed -i.bak 's/\.pw"/.al"/g' {} +

find . -name "*.py" \
  -not -path "./.git/*" \
  -not -path "./.venv/*" \
  -not -path "./node_modules/*" \
  -not -path "./.mcpd/*" \
  -not -path "./build/*" \
  -not -path "./dist/*" \
  -exec sed -i.bak "s/\.pw'/.al'/g" {} +

echo "   ✅ Python code updated"

# Update .pw references in config/other files
echo "⚙️  [3/3] Updating .pw → .al in config files..."
find . -type f \( -name "*.json" -o -name "*.toml" -o -name "*.yaml" -o -name "*.yml" \) \
  -not -path "./.git/*" \
  -not -path "./.venv/*" \
  -not -path "./node_modules/*" \
  -not -path "./.mcpd/*" \
  -exec sed -i.bak 's/\.pw"/.al"/g' {} +

echo "   ✅ Config files updated"

# Clean up backup files
echo "🧹 Cleaning up backup files..."
find . -name "*.bak" \
  -not -path "./.git/*" \
  -not -path "./.venv/*" \
  -not -path "./node_modules/*" \
  -not -path "./.mcpd/*" \
  -delete

echo ""
echo "✅ File extension update complete!"
echo ""
echo "📊 Summary:"
echo "   • .pw → .al in all documentation"
echo "   • .pw → .al in all Python code"
echo "   • .pw → .al in all config files"
echo ""
echo "🔍 Verify changes:"
echo "   git diff | grep -E '\\.pw|\\.al' | head -20"
echo ""
echo "✅ Done!"
