#!/usr/bin/env bash
set -euo pipefail

# Git sync automation - push current branch to origin
# Usage: scripts/git_sync.sh [--force]

FORCE_FLAG=""
if [[ "${1:-}" == "--force" ]]; then
  FORCE_FLAG="--force-with-lease"
fi

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

CURRENT_BRANCH="$(git branch --show-current)"

echo "==> Syncing branch: $CURRENT_BRANCH"

# Verify we're not on main/master (safety check)
if [[ "$CURRENT_BRANCH" == "main" ]] || [[ "$CURRENT_BRANCH" == "master" ]]; then
  echo "ERROR: Cannot auto-sync main/master branch. Use release.sh instead." >&2
  exit 1
fi

# Verify we're not pushing to upstream accidentally
REMOTE_URL="$(git remote get-url origin 2>/dev/null || echo '')"
if [[ "$REMOTE_URL" == *"AssertLang-dev/assertlang"* ]]; then
  echo "ERROR: origin points to upstream. Fix remote configuration:" >&2
  echo "  git remote set-url origin git@github.com:3CH0xyz/assertlang.git" >&2
  exit 1
fi

# Check for uncommitted changes
if [[ -n "$(git status --porcelain)" ]]; then
  echo "WARNING: You have uncommitted changes. Commit first or use --force to push anyway." >&2
  git status --short
  exit 1
fi

# Push to origin (user's fork)
echo "==> Pushing to origin/$CURRENT_BRANCH"
git push origin "$CURRENT_BRANCH" $FORCE_FLAG

echo "✓ Synced $CURRENT_BRANCH → origin"
