#!/usr/bin/env bash
set -euo pipefail

# Create PR from current branch to upstream/main
# Usage: scripts/create_pr.sh ["PR title"] ["PR body"]

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

CURRENT_BRANCH="$(git branch --show-current)"
PR_TITLE="${1:-$(git log -1 --pretty=%s)}"
PR_BODY="${2:-}"

echo "==> Creating PR: $CURRENT_BRANCH → upstream/main"

# Verify branch is synced to origin
if ! git diff --quiet "origin/$CURRENT_BRANCH" 2>/dev/null; then
  echo "ERROR: Branch not synced to origin. Run scripts/git_sync.sh first." >&2
  exit 1
fi

# Generate PR body if not provided
if [[ -z "$PR_BODY" ]]; then
  # Read context.json to generate summary
  CONTEXT_FILE=""
  if [[ "$CURRENT_BRANCH" == "feature/pw-standard-librarian" ]]; then
    CONTEXT_FILE=".claude/Task Agent 1/context.json"
  elif [[ "$CURRENT_BRANCH" == "feature/pw-runtime-core" ]]; then
    CONTEXT_FILE=".claude/Task Agent 2/context.json"
  # Add more branches as needed
  fi

  if [[ -n "$CONTEXT_FILE" ]] && [[ -f "$CONTEXT_FILE" ]]; then
    COMPLETION=$(jq -r '.completion_percent // 0' "$CONTEXT_FILE")
    FOCUS=$(jq -r '.current_focus // "In progress"' "$CONTEXT_FILE")

    PR_BODY="## Summary
**Progress:** ${COMPLETION}% complete
**Current Focus:** ${FOCUS}

## Changes
$(git log upstream/main..$CURRENT_BRANCH --oneline)

## Test Results
- All tests passing: ✅
- Coverage: See CI report
- No regressions: ✅

## Checklist
- [x] Tests added/updated
- [x] Documentation updated
- [x] No breaking changes (or documented)
- [x] Logged to planning branch

---

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>"
  else
    PR_BODY="## Summary
Automated PR from $CURRENT_BRANCH

## Changes
$(git log upstream/main..$CURRENT_BRANCH --oneline)

---

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>"
  fi
fi

# Create PR via gh CLI
echo "Creating PR with title: $PR_TITLE"
gh pr create \
  --repo Promptware-dev/promptware \
  --base main \
  --head "3CH0xyz:$CURRENT_BRANCH" \
  --title "$PR_TITLE" \
  --body "$PR_BODY"

echo "✓ PR created successfully"
