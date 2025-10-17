#!/bin/bash

# Rename Promptware → AssertLang
# This script handles folder rename + fixes hardcoded paths

set -e  # Exit on error

OLD_NAME="Promptware"
NEW_NAME="AssertLang"
BASE_DIR="/Users/hustlermain/HUSTLER_CONTENT/HSTLR/DEV"

echo "🔄 Renaming $OLD_NAME → $NEW_NAME"
echo ""

# Check we're in the right place
if [ ! -f "pyproject.toml" ]; then
    echo "❌ Error: Must run from project root (where pyproject.toml exists)"
    exit 1
fi

# Check if already renamed
CURRENT_DIR=$(basename "$PWD")
if [ "$CURRENT_DIR" = "$NEW_NAME" ]; then
    echo "✅ Already renamed to $NEW_NAME"
    exit 0
fi

# Step 1: Commit current work (safety checkpoint)
echo "📝 Step 1/5: Creating safety checkpoint..."
git add -A
git commit -m "Pre-rename checkpoint: $OLD_NAME → $NEW_NAME" || echo "Nothing to commit"

# Step 2: Go up and rename folder
echo "📁 Step 2/5: Renaming folder..."
cd "$BASE_DIR" || exit 1

if [ ! -d "$OLD_NAME" ]; then
    echo "❌ Error: $OLD_NAME folder not found in $BASE_DIR"
    exit 1
fi

mv "$OLD_NAME" "$NEW_NAME"
echo "   ✓ Renamed folder"

# Step 3: Enter new folder
cd "$NEW_NAME" || exit 1
echo "   ✓ Entered $NEW_NAME"

# Step 4: Fix MCP config if it exists
echo "🔧 Step 3/5: Fixing MCP configuration..."
if [ -f ".cursor/mcp.json" ]; then
    # Create backup
    cp .cursor/mcp.json .cursor/mcp.json.bak

    # Replace paths
    sed -i '' "s|/$OLD_NAME/|/$NEW_NAME/|g" .cursor/mcp.json

    # Count changes
    CHANGES=$(diff .cursor/mcp.json.bak .cursor/mcp.json | grep -c "^<" || echo "0")
    echo "   ✓ Updated $CHANGES paths in .cursor/mcp.json"

    # Keep backup for safety
    echo "   ✓ Backup saved: .cursor/mcp.json.bak"
else
    echo "   ⚠ No .cursor/mcp.json found (skipping)"
fi

# Step 5: Recreate virtual environment
echo "🐍 Step 4/5: Recreating virtual environment..."
if [ -d ".venv" ]; then
    rm -rf .venv
    echo "   ✓ Removed old .venv"
fi

python3 -m venv .venv
echo "   ✓ Created new .venv"

source .venv/bin/activate
echo "   ✓ Activated .venv"

pip install -q -e .
echo "   ✓ Installed package in editable mode"

# Step 6: Verification
echo "✅ Step 5/5: Verifying setup..."
echo ""

# Check git still works
if git status > /dev/null 2>&1; then
    echo "   ✓ Git repository: OK"
else
    echo "   ❌ Git repository: ERROR"
fi

# Check package imports
if python -c "import assertlang" 2>/dev/null; then
    echo "   ✓ Python import: OK"
else
    echo "   ❌ Python import: ERROR"
fi

# Check CLI
if command -v asl > /dev/null 2>&1; then
    echo "   ✓ CLI command (asl): OK"
else
    echo "   ⚠ CLI command (asl): Run 'source .venv/bin/activate' first"
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ SUCCESS: Renamed to AssertLang"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "📍 New location: $BASE_DIR/$NEW_NAME"
echo ""
echo "Next steps:"
echo "  1. cd $BASE_DIR/$NEW_NAME"
echo "  2. source .venv/bin/activate"
echo "  3. git status              # Verify git works"
echo "  4. asl --version           # Test CLI"
echo "  5. pytest tests/           # Run tests (optional)"
echo ""
echo "If anything broke:"
echo "  # Rollback with:"
echo "  cd $BASE_DIR && mv $NEW_NAME $OLD_NAME && cd $OLD_NAME"
echo "  git reset --hard HEAD~1    # Undo checkpoint commit"
echo ""
