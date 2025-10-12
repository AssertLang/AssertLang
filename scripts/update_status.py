#!/usr/bin/env python3
"""
Auto-update CLAUDE.md and Current_Work.md from TA context files.
Usage: python scripts/update_status.py
"""

from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent
CLAUDE_MD = REPO_ROOT / "CLAUDE.md"
CURRENT_WORK_MD = REPO_ROOT / "Current_Work.md"

TA_CONFIGS = [
    {"num": 1, "name": "Standard Library & Syntax (Batch #11)", "branch": "feature/pw-standard-librarian"},
    {"num": 2, "name": "Runtime + CLI Core", "branch": "feature/pw-runtime-core"},
    {"num": 3, "name": "Tooling & DevEx (LSP, fmt, lint, test)", "branch": "feature/pw-tooling-devex"},
    {"num": 4, "name": "Ecosystem & Governance Launch", "branch": "feature/pw-ecosystem-launch"},
    {"num": 5, "name": "Interop Conformance & FFI", "branch": "feature/pw-interop-parity"},
    {"num": 6, "name": "Safety, CI, Release Automation", "branch": "feature/pw-safety-release"},
]


def read_context(ta_num: int) -> dict[str, Any]:
    """Read TA context.json file."""
    context_file = REPO_ROOT / f".claude/Task Agent {ta_num}/context.json"
    if not context_file.exists():
        return {"status": "unassigned", "completion_percent": 0}

    try:
        return json.loads(context_file.read_text())
    except json.JSONDecodeError:
        return {"status": "error", "completion_percent": 0}


def read_progress(ta_num: int) -> list[str]:
    """Read TA progress log (last 5 entries)."""
    progress_file = REPO_ROOT / f".claude/Task Agent {ta_num}/ta{ta_num}-current-progress.md"
    if not progress_file.exists():
        return []

    lines = progress_file.read_text().splitlines()
    # Extract last 5 log entries (lines starting with "- YYYY-MM-DD")
    entries = [l for l in lines if l.startswith("- 20")]
    return entries[-5:]


def format_status(context: dict[str, Any]) -> str:
    """Format TA status for CLAUDE.md roster."""
    status = context.get("status", "unassigned")
    completion = context.get("completion_percent", 0)
    focus = context.get("current_focus", "")
    blockers = context.get("blockers", [])

    if status == "unassigned":
        return "_unassigned_"
    elif status == "completed":
        return f"**COMPLETED** - {completion}%"
    elif blockers:
        blocker_text = blockers[0].get("description", "blocked") if isinstance(blockers[0], dict) else str(blockers[0])
        return f"**BLOCKED** - {blocker_text[:50]}..."
    elif status == "in_progress":
        return f"**IN PROGRESS** ({completion}%) - {focus[:60]}..."
    else:
        return f"{status} - {focus[:60]}..." if focus else status


def update_claude_md() -> None:
    """Update CLAUDE.md agent roster table."""
    if not CLAUDE_MD.exists():
        print(f"Error: {CLAUDE_MD} not found")
        return

    content = CLAUDE_MD.read_text()

    # Find the roster table
    table_pattern = r"(\| Agent \| Mission Focus.*?\n\|.*?\n)((?:\| TA\d.*?\n)+)"
    match = re.search(table_pattern, content, re.MULTILINE)

    if not match:
        print("Error: Could not find agent roster table in CLAUDE.md")
        return

    header = match.group(1)

    # Build new table rows
    new_rows = []
    for ta in TA_CONFIGS:
        context = read_context(ta["num"])
        status = format_status(context)

        row = (
            f"| TA{ta['num']} "
            f"| {ta['name']} "
            f"| `{ta['branch']}` "
            f"| `missions/TA{ta['num']}/mission.md` "
            f"| `.claude/Task Agent {ta['num']}/ta{ta['num']}-current-progress.md` "
            f"| {status} |"
        )
        new_rows.append(row)

    new_table = header + "\n".join(new_rows) + "\n"

    # Replace old table with new
    new_content = re.sub(table_pattern, new_table, content, flags=re.MULTILINE)

    CLAUDE_MD.write_text(new_content)
    print(f"✓ Updated {CLAUDE_MD}")


def update_current_work_md() -> None:
    """Update Current_Work.md with recent progress from all TAs."""
    if not CURRENT_WORK_MD.exists():
        print(f"Error: {CURRENT_WORK_MD} not found")
        return

    content = CURRENT_WORK_MD.read_text()

    # Collect recent progress from all TAs
    all_progress = []
    for ta in TA_CONFIGS:
        context = read_context(ta["num"])
        recent = context.get("recent_progress", [])
        for entry in recent[-3:]:  # Last 3 entries
            all_progress.append(f"**TA{ta['num']}**: {entry}")

    # Also get from progress logs
    for ta in TA_CONFIGS:
        progress_entries = read_progress(ta["num"])
        for entry in progress_entries[-2:]:  # Last 2 from logs
            all_progress.append(f"**TA{ta['num']}**: {entry}")

    # Sort by date (newest first)
    all_progress.sort(reverse=True)

    # Generate status summary section
    status_summary = f"""## 📊 Multi-Agent Status (Auto-Updated)

**Last Updated:** {datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")}

### Active Agents:
"""

    for ta in TA_CONFIGS:
        context = read_context(ta["num"])
        if context.get("status") not in ["unassigned", "completed"]:
            completion = context.get("completion_percent", 0)
            focus = context.get("current_focus", "In progress")
            status_summary += f"- **TA{ta['num']}**: {completion}% - {focus}\n"

    status_summary += "\n### Recent Progress:\n"
    for entry in all_progress[:10]:  # Top 10 most recent
        status_summary += f"- {entry}\n"

    # Insert or replace status section in Current_Work.md
    status_marker = "## 📊 Multi-Agent Status"
    if status_marker in content:
        # Replace existing section
        pattern = r"## 📊 Multi-Agent Status.*?(?=\n## |\Z)"
        new_content = re.sub(pattern, status_summary.rstrip(), content, flags=re.DOTALL)
    else:
        # Insert at top after title
        lines = content.splitlines()
        # Find first ## heading after title
        insert_idx = 0
        for i, line in enumerate(lines):
            if i > 0 and line.startswith("## "):
                insert_idx = i
                break

        lines.insert(insert_idx, "\n" + status_summary)
        new_content = "\n".join(lines)

    CURRENT_WORK_MD.write_text(new_content)
    print(f"✓ Updated {CURRENT_WORK_MD}")


def main() -> None:
    print("==> Syncing status from TA context files")
    update_claude_md()
    update_current_work_md()
    print("✓ Status sync complete")


if __name__ == "__main__":
    main()
