#!/usr/bin/env bash
set -euo pipefail

# Check cross-TA dependencies and identify blockers
# Usage: scripts/check_deps.sh

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

echo "==> Analyzing Cross-TA Dependencies"
echo ""

# Parse dependencies.yml from each TA
for N in 1 2 3 4 5 6; do
  DEPS_FILE=".claude/Task Agent $N/dependencies.yml"

  if [[ ! -f "$DEPS_FILE" ]]; then
    continue
  fi

  echo "TA$N Dependencies:"

  # Extract depends_on section
  if grep -q "^depends_on:" "$DEPS_FILE"; then
    echo "  Depends on:"
    sed -n '/^depends_on:/,/^[^ ]/p' "$DEPS_FILE" | \
      grep -E '^\s+TA[0-9]:' | \
      sed 's/^/    /'
  fi

  # Extract blocks section
  if grep -q "^blocks:" "$DEPS_FILE"; then
    echo "  Blocks:"
    sed -n '/^blocks:/,/^[^ ]/p' "$DEPS_FILE" | \
      grep -E '^\s+TA[0-9]:' | \
      sed 's/^/    /'
  fi

  echo ""
done

# Identify critical path (TAs that are blocking others)
echo "==> Critical Path Analysis"
echo ""

BLOCKING_TAS=()
for N in 1 2 3 4 5 6; do
  DEPS_FILE=".claude/Task Agent $N/dependencies.yml"

  if [[ ! -f "$DEPS_FILE" ]]; then
    continue
  fi

  if grep -q "^blocks:" "$DEPS_FILE"; then
    BLOCKING_COUNT=$(sed -n '/^blocks:/,/^[^ ]/p' "$DEPS_FILE" | grep -c "^  TA" || echo "0")
    if [[ "$BLOCKING_COUNT" -gt 0 ]]; then
      BLOCKING_TAS+=("TA$N (blocks $BLOCKING_COUNT others)")
    fi
  fi
done

if [[ ${#BLOCKING_TAS[@]} -gt 0 ]]; then
  echo "Critical TAs (blocking others):"
  for TA in "${BLOCKING_TAS[@]}"; do
    echo "  - $TA"
  done
else
  echo "No blocking dependencies found"
fi

echo ""
echo "==> Recommendation:"
echo "Prioritize TAs on the critical path to unblock dependent work"
