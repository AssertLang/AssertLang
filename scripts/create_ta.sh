#!/usr/bin/env bash
set -euo pipefail

# Bootstrap a new Task Agent with full infrastructure
# Usage: scripts/create_ta.sh TA_NUM "Mission Name" "feature-branch-name"

TA_NUM="${1:-}"
MISSION_NAME="${2:-}"
BRANCH_NAME="${3:-}"

if [[ -z "$TA_NUM" ]] || [[ -z "$MISSION_NAME" ]] || [[ -z "$BRANCH_NAME" ]]; then
  echo "Usage: scripts/create_ta.sh TA_NUM 'Mission Name' 'feature-branch-name'" >&2
  echo "Example: scripts/create_ta.sh 7 'Web Dashboard' 'feature/pw-web-dashboard'" >&2
  exit 1
fi

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

TA_DIR=".claude/Task Agent $TA_NUM"

echo "==> Creating TA$TA_NUM infrastructure"

# Create directory
mkdir -p "$TA_DIR"

# Generate mission file
cat > "$TA_DIR/ta${TA_NUM}-current-mission.md" <<EOF
## Mission: $MISSION_NAME

**Assigned branch:** \`$BRANCH_NAME\` (tracked off \`upstream/main\`)
**Primary objective:** [Add objective here]

### Context & Constraints
- [Add context]

### Exit Criteria
- [ ] [Add exit criteria]

### Deliverables
- [Add deliverables]
EOF

# Generate progress file
cat > "$TA_DIR/ta${TA_NUM}-current-progress.md" <<EOF
# Progress Log

Initial setup: $(date +%Y-%m-%d)
EOF

# Generate context.json
cat > "$TA_DIR/context.json" <<EOF
{
  "mission": "TA$TA_NUM: $MISSION_NAME",
  "branch": "$BRANCH_NAME",
  "last_updated": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "assigned_agent": "unassigned",
  "status": "unassigned",
  "completion_percent": 0,
  "current_focus": "Not started",
  "blockers": [],
  "next_actions": [],
  "dependencies_status": {},
  "quality_metrics": {
    "tests_passing": 0,
    "tests_total": 0,
    "coverage_percent": 0,
    "regressions": 0
  },
  "recent_progress": []
}
EOF

# Copy template files from TA1
for FILE in dependencies.yml tests.yml decisions.md ta1-completion-criteria.md release-checklist.md; do
  SRC=".claude/Task Agent 1/$FILE"
  if [[ -f "$SRC" ]]; then
    DEST="$TA_DIR/$(echo "$FILE" | sed "s/ta1/ta$TA_NUM/g")"
    sed "s/TA1/TA$TA_NUM/g; s/ta1/ta$TA_NUM/g" "$SRC" > "$DEST"
    echo "  Created: $DEST"
  fi
done

# Update scripts/integration_run.sh to include new branch
if ! grep -q "$BRANCH_NAME" scripts/integration_run.sh; then
  sed -i.bak "/^FEATURE_BRANCHES=/a\\
  \"$BRANCH_NAME\"" scripts/integration_run.sh
  rm -f scripts/integration_run.sh.bak
  echo "  Updated: scripts/integration_run.sh"
fi

# Update scripts/agent_sync.py to include new TA
if ! grep -q "TA$TA_NUM" scripts/agent_sync.py; then
  # This is complex, just notify user to update manually
  echo "  ⚠️  TODO: Add TA$TA_NUM to scripts/agent_sync.py MISSION_MAP"
fi

# Update scripts/update_status.py TA_CONFIGS
if ! grep -q "\"num\": $TA_NUM" scripts/update_status.py; then
  echo "  ⚠️  TODO: Add TA$TA_NUM to scripts/update_status.py TA_CONFIGS"
fi

# Create feature branch
echo "==> Creating feature branch: $BRANCH_NAME"
git checkout -b "$BRANCH_NAME" upstream/main 2>/dev/null || \
  git checkout "$BRANCH_NAME" || \
  echo "  Branch may already exist"

# Create missions directory
mkdir -p "missions/TA$TA_NUM"

echo ""
echo "✓ TA$TA_NUM infrastructure created!"
echo ""
echo "Next steps:"
echo "  1. Edit $TA_DIR/ta${TA_NUM}-current-mission.md (add objectives)"
echo "  2. Edit $TA_DIR/dependencies.yml (define cross-TA deps)"
echo "  3. Add TA$TA_NUM to scripts/agent_sync.py MISSION_MAP"
echo "  4. Add TA$TA_NUM to scripts/update_status.py TA_CONFIGS"
echo "  5. Update CLAUDE.md roster table with TA$TA_NUM row"
echo "  6. Run: python scripts/update_status.py"
