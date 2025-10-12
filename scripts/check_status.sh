#!/usr/bin/env bash
set -euo pipefail

# Check status of all Task Agents
# Usage: scripts/check_status.sh

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

echo "==> Task Agent Status Summary"
echo ""

for N in 1 2 3 4 5 6; do
  CONTEXT_FILE=".claude/Task Agent $N/context.json"

  if [[ ! -f "$CONTEXT_FILE" ]]; then
    echo "TA$N: Not initialized"
    continue
  fi

  STATUS=$(jq -r '.status // "unknown"' "$CONTEXT_FILE")
  COMPLETION=$(jq -r '.completion_percent // 0' "$CONTEXT_FILE")
  FOCUS=$(jq -r '.current_focus // "N/A"' "$CONTEXT_FILE")
  BLOCKERS=$(jq -r '.blockers | length' "$CONTEXT_FILE")

  echo "TA$N: $STATUS ($COMPLETION%)"
  echo "  Focus: $FOCUS"
  if [[ "$BLOCKERS" -gt 0 ]]; then
    echo "  ⚠️  Blockers: $BLOCKERS"
    jq -r '.blockers[] | "    - \(.description // .id)"' "$CONTEXT_FILE"
  fi
  echo ""
done

echo "==> Run 'python scripts/update_status.py' to sync CLAUDE.md and Current_Work.md"
