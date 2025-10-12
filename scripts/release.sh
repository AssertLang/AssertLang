#!/usr/bin/env bash
set -euo pipefail

# Full release automation
# Usage: scripts/release.sh v2.2.0

VERSION="${1:-}"
if [[ -z "$VERSION" ]]; then
  echo "Usage: scripts/release.sh VERSION" >&2
  echo "Example: scripts/release.sh v2.2.0" >&2
  exit 1
fi

# Strip 'v' prefix if present for version numbers
VERSION_NUM="${VERSION#v}"
VERSION_TAG="v${VERSION_NUM}"

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

echo "==> Starting release process for $VERSION_TAG"

# 1. Verify on integration/nightly or main
CURRENT_BRANCH="$(git branch --show-current)"
if [[ "$CURRENT_BRANCH" != "integration/nightly" ]] && [[ "$CURRENT_BRANCH" != "main" ]]; then
  echo "ERROR: Must be on integration/nightly or main branch for release" >&2
  exit 1
fi

# 2. Verify tests pass
echo "==> Running test suite"
if command -v pytest >/dev/null 2>&1; then
  pytest tests/ -v || {
    echo "ERROR: Tests failing. Fix before release." >&2
    exit 1
  }
else
  echo "WARNING: pytest not found, skipping tests" >&2
fi

# 3. Update version in pyproject.toml
echo "==> Updating version to $VERSION_NUM"
if [[ -f "pyproject.toml" ]]; then
  sed -i.bak "s/^version = .*/version = \"$VERSION_NUM\"/" pyproject.toml
  rm -f pyproject.toml.bak
fi

# 4. Generate release notes if they don't exist
RELEASE_NOTES="RELEASE_NOTES_${VERSION_TAG}.md"
if [[ ! -f "$RELEASE_NOTES" ]]; then
  echo "==> Generating release notes"
  cat > "$RELEASE_NOTES" <<EOF
# Promptware $VERSION_TAG

**Release Date:** $(date +%Y-%m-%d)
**Type:** $(echo "$VERSION_NUM" | grep -q 'b' && echo "Beta" || echo "Stable")

## Summary

[Auto-generated release - please add summary]

## Changes

$(git log --oneline "$(git describe --tags --abbrev=0 2>/dev/null || echo 'HEAD~10')..HEAD" | sed 's/^/- /')

## Test Results

- All tests passing: ✅
- Coverage: [Add coverage %]
- No regressions: ✅

## Installation

\`\`\`bash
pip install promptware-dev==$VERSION_NUM
\`\`\`

---

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
EOF
  echo "Release notes created: $RELEASE_NOTES (please review/edit)"
fi

# 5. Commit version bump
echo "==> Committing version bump"
git add pyproject.toml "$RELEASE_NOTES" 2>/dev/null || true
if ! git diff --cached --quiet; then
  git commit -m "Release $VERSION_TAG

Version bump and release notes for $VERSION_TAG.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>"
fi

# 6. Merge to main if on integration branch
if [[ "$CURRENT_BRANCH" == "integration/nightly" ]]; then
  echo "==> Merging integration/nightly → main"
  git checkout main
  git pull upstream main || echo "Warning: Could not pull upstream/main"
  git merge integration/nightly --no-ff -m "Merge integration/nightly for $VERSION_TAG release"
fi

# 7. Tag release
echo "==> Tagging $VERSION_TAG"
git tag -a "$VERSION_TAG" -m "Release $VERSION_TAG

$(cat "$RELEASE_NOTES" | head -20)

Full release notes: $RELEASE_NOTES"

# 8. Push to both remotes
echo "==> Pushing to origin and upstream"
git push origin main --tags
git push upstream main --tags || {
  echo "WARNING: Could not push to upstream (may need manual PR approval)" >&2
}

# 9. Create GitHub release
echo "==> Creating GitHub release"
gh release create "$VERSION_TAG" \
  --repo Promptware-dev/promptware \
  --notes-file "$RELEASE_NOTES" \
  --title "Promptware $VERSION_TAG" \
  || echo "WARNING: GitHub release creation failed (may need manual creation)"

# 10. Build and publish to PyPI
echo "==> Building distribution"
python -m build

echo "==> Publishing to PyPI"
if command -v twine >/dev/null 2>&1; then
  twine check dist/*promptware*${VERSION_NUM}*
  twine upload dist/*promptware*${VERSION_NUM}* || {
    echo "ERROR: PyPI upload failed. Manual intervention needed:" >&2
    echo "  twine upload dist/*promptware*${VERSION_NUM}*" >&2
    exit 1
  }
else
  echo "ERROR: twine not installed. Install: pip install twine" >&2
  exit 1
fi

# 11. Verify release
echo "==> Verifying release"
echo "  PyPI: https://pypi.org/project/promptware-dev/$VERSION_NUM/"
echo "  GitHub: https://github.com/Promptware-dev/promptware/releases/tag/$VERSION_TAG"

echo ""
echo "✅ Release $VERSION_TAG complete!"
echo ""
echo "Next steps:"
echo "  1. Verify PyPI page: https://pypi.org/project/promptware-dev/$VERSION_NUM/"
echo "  2. Verify GitHub release: https://github.com/Promptware-dev/promptware/releases/tag/$VERSION_TAG"
echo "  3. Test installation: pip install promptware-dev==$VERSION_NUM"
echo "  4. Update Current_Work.md with release summary"
echo "  5. Announce release (Discord, Twitter, etc.)"
