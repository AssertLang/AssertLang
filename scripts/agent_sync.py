#!/usr/bin/env python3
"""
Agent workflow helper.

Usage examples:
    python scripts/agent_sync.py start --mission TA1
    python scripts/agent_sync.py log --mission TA1 --entry "Completed stdlib core scaffolding."
"""

from __future__ import annotations

import argparse
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path
from textwrap import dedent
from datetime import datetime

REPO_ROOT = Path(__file__).resolve().parent.parent
MISSIONS_DIR = REPO_ROOT / "missions"
PLANNING_BRANCH = "planning/master-plan"


@dataclass(frozen=True)
class Mission:
    code: str
    branch: str
    mission_path: Path
    progress_path: Path


MISSION_MAP: dict[str, Mission] = {
    "TA1": Mission(
        code="TA1",
        branch="feature/pw-standard-librarian",
        mission_path=Path(".claude/Task Agent 1/ta1-current-mission.md"),
        progress_path=Path(".claude/Task Agent 1/ta1-current-progress.md"),
    ),
    "TA2": Mission(
        code="TA2",
        branch="feature/pw-runtime-core",
        mission_path=Path(".claude/Task Agent 2/ta2-current-mission.md"),
        progress_path=Path(".claude/Task Agent 2/ta2-current-progress.md"),
    ),
    "TA3": Mission(
        code="TA3",
        branch="feature/pw-tooling-devex",
        mission_path=Path(".claude/Task Agent 3/ta3-current-mission.md"),
        progress_path=Path(".claude/Task Agent 3/ta3-current-progress.md"),
    ),
    "TA4": Mission(
        code="TA4",
        branch="feature/pw-ecosystem-launch",
        mission_path=Path(".claude/Task Agent 4/ta4-current-mission.md"),
        progress_path=Path(".claude/Task Agent 4/ta4-current-progress.md"),
    ),
    "TA5": Mission(
        code="TA5",
        branch="feature/pw-interop-parity",
        mission_path=Path(".claude/Task Agent 5/ta5-current-mission.md"),
        progress_path=Path(".claude/Task Agent 5/ta5-current-progress.md"),
    ),
    "TA6": Mission(
        code="TA6",
        branch="feature/pw-safety-release",
        mission_path=Path(".claude/Task Agent 6/ta6-current-mission.md"),
        progress_path=Path(".claude/Task Agent 6/ta6-current-progress.md"),
    ),
}


def run(cmd: list[str], *, cwd: Path | None = None, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(cmd, cwd=cwd, check=check, text=True, capture_output=False)


def run_capture(cmd: list[str], *, cwd: Path | None = None) -> str:
    completed = subprocess.run(cmd, cwd=cwd, check=True, text=True, capture_output=True)
    return completed.stdout


def ensure_clean_worktree() -> None:
    status = run_capture(["git", "status", "--porcelain"]).strip()
    if status:
        print("Error: Working tree is not clean. Please commit/stash changes before running.", file=sys.stderr)
        print(status, file=sys.stderr)
        sys.exit(1)


def fetch_branch(ref: str, *, required: bool = True) -> None:
    try:
        run(["git", "fetch", "origin", ref])
    except subprocess.CalledProcessError:
        if required:
            raise
        print(f"Warning: origin/{ref} not found. You may need to create it.", file=sys.stderr)


def checkout_and_update(branch: str) -> None:
    run(["git", "checkout", branch])
    run(["git", "pull", "--rebase", "origin", branch])


def write_mission_brief(mission: Mission) -> None:
    MISSIONS_DIR.mkdir(parents=True, exist_ok=True)
    target_dir = MISSIONS_DIR / mission.code
    target_dir.mkdir(parents=True, exist_ok=True)

    try:
        mission_text = run_capture(
            ["git", "show", f"origin/{PLANNING_BRANCH}:{mission.mission_path.as_posix()}"]
        )
    except subprocess.CalledProcessError:
        mission_text = mission.mission_path.read_text() if mission.mission_path.exists() else "# Mission\n"
        print(
            f"Warning: mission brief not found on origin/{PLANNING_BRANCH}; using working tree copy.",
            file=sys.stderr,
        )
    (target_dir / "mission.md").write_text(mission_text)

    try:
        progress_text = run_capture(
            ["git", "show", f"origin/{PLANNING_BRANCH}:{mission.progress_path.as_posix()}"]
        )
    except subprocess.CalledProcessError:
        progress_text = "# Progress Log\n"
    (target_dir / "progress.md").write_text(progress_text)

    print(
        dedent(
            f"""
            ✓ Mission brief ready for {mission.code}
              - Branch: {mission.branch}
              - Brief:   {target_dir / 'mission.md'}
              - Progress snapshot: {target_dir / 'progress.md'}
            
            Reminder:
              1. Develop on branch `{mission.branch}` only.
              2. Log updates with `python scripts/agent_sync.py log --mission {mission.code} --entry "…"`
              3. Before pushing, run `git pull --rebase origin {mission.branch}`.
            """
        ).strip()
    )


def append_progress(mission: Mission, entry: str) -> None:
    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
    formatted = f"- {timestamp}: {entry.strip()}\n"

    with tempfile.TemporaryDirectory() as tmp_dir_str:
        tmp_dir = Path(tmp_dir_str)
        try:
            run(["git", "fetch", "origin", PLANNING_BRANCH])
        except subprocess.CalledProcessError:
            print(
                f"Planning branch '{PLANNING_BRANCH}' not found. "
                "Create it on origin before logging progress:\n"
                "  git checkout -b planning/master-plan\n"
                "  git push origin HEAD:planning/master-plan",
                file=sys.stderr,
            )
            sys.exit(1)
        run(["git", "worktree", "add", tmp_dir_str, f"origin/{PLANNING_BRANCH}"])
        progress_file = tmp_dir / mission.progress_path
        progress_file.parent.mkdir(parents=True, exist_ok=True)
        if progress_file.exists():
            with progress_file.open("a", encoding="utf-8") as fh:
                fh.write(formatted)
        else:
            progress_file.write_text("# Progress Log\n" + formatted, encoding="utf-8")
        run(
            ["git", "add", "--force", mission.progress_path.as_posix()],
            cwd=tmp_dir,
        )
        run(
            [
                "git",
                "commit",
                "-m",
                f"TA{mission.code[-1]} progress update",
            ],
            cwd=tmp_dir,
        )
        run(
            ["git", "push", "origin", "HEAD:" + PLANNING_BRANCH],
            cwd=tmp_dir,
        )
        run(["git", "worktree", "remove", tmp_dir_str, "--force"])

    print(f"✓ Logged progress for {mission.code}: {entry.strip()}")


def start_mission(mission_code: str) -> None:
    mission = MISSION_MAP[mission_code]
    ensure_clean_worktree()
    fetch_branch(mission.branch)
    fetch_branch(PLANNING_BRANCH, required=False)
    checkout_and_update(mission.branch)
    write_mission_brief(mission)


def log_progress(mission_code: str, entry: str) -> None:
    mission = MISSION_MAP[mission_code]
    append_progress(mission, entry)


def main() -> None:
    parser = argparse.ArgumentParser(description="Agent branch helper.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    start_parser = subparsers.add_parser("start", help="Prepare workspace for a mission.")
    start_parser.add_argument("--mission", choices=MISSION_MAP.keys(), required=True)

    log_parser = subparsers.add_parser("log", help="Append a progress log entry on planning branch.")
    log_parser.add_argument("--mission", choices=MISSION_MAP.keys(), required=True)
    log_parser.add_argument("--entry", required=True)

    args = parser.parse_args()

    if args.command == "start":
        start_mission(args.mission)
    elif args.command == "log":
        log_progress(args.mission, args.entry)
    else:
        parser.error("Unknown command.")


if __name__ == "__main__":
    main()
