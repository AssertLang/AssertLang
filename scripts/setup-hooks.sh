#!/bin/bash
# Setup git hooks for repository cleanliness validation

HOOK_DIR=".git/hooks"
HOOK_FILE="$HOOK_DIR/pre-commit"

echo "🔧 Setting up git hooks..."

# Create pre-commit hook
cat > "$HOOK_FILE" << 'EOF'
#!/bin/bash
# Pre-commit hook to validate repository cleanliness

echo "🔍 Running repository cleanliness check..."

if [ -f scripts/validate_clean_repo.sh ]; then
    ./scripts/validate_clean_repo.sh
    if [ $? -ne 0 ]; then
        echo ""
        echo "❌ Commit blocked due to repository cleanliness violations."
        echo "   Please fix the issues above before committing."
        echo ""
        echo "   To bypass this check (NOT RECOMMENDED for production):"
        echo "   git commit --no-verify"
        exit 1
    fi
else
    echo "⚠️  Warning: validate_clean_repo.sh not found. Skipping validation."
fi

echo "✅ Repository cleanliness check passed!"
EOF

chmod +x "$HOOK_FILE"

echo "✅ Pre-commit hook installed successfully!"
echo ""
echo "This hook will now run on every commit to prevent non-production files"
echo "from being accidentally committed."
echo ""
echo "To bypass the hook (NOT recommended):"
echo "  git commit --no-verify"
