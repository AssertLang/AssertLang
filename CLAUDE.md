# Claude Agent Release Playbook

Follow these steps whenever Hustler asks to build, review, or release Promptware changes.

## Current Agent Assignments

| Agent | Mission Focus | Branch | Mission Brief | Progress Log | Status |
|-------|---------------|--------|---------------|--------------|--------|
| TA1 | Standard Library & Syntax (Batch #11) | `feature/pw-standard-librarian` | `missions/TA1/mission.md` | `.claude/Task Agent 1/ta1-current-progress.md` | **IN PROGRESS** - Lead agent coordinating Bug Batch #11 fixes + stdlib foundation |
| TA2 | Runtime + CLI Core | `feature/pw-runtime-core` | `missions/TA2/mission.md` | `.claude/Task Agent 2/ta2-current-progress.md` | _unassigned_ |
| TA3 | Tooling & DevEx (LSP, fmt, lint, test) | `feature/pw-tooling-devex` | `missions/TA3/mission.md` | `.claude/Task Agent 3/ta3-current-progress.md` | _unassigned_ |
| TA4 | Ecosystem & Governance Launch | `feature/pw-ecosystem-launch` | `missions/TA4/mission.md` | `.claude/Task Agent 4/ta4-current-progress.md` | _unassigned_ |
| TA5 | Interop Conformance & FFI | `feature/pw-interop-parity` | `missions/TA5/mission.md` | `.claude/Task Agent 5/ta5-current-progress.md` | _unassigned_ |
| TA6 | Safety, CI, Release Automation | `feature/pw-safety-release` | `missions/TA6/mission.md` | `.claude/Task Agent 6/ta6-current-progress.md` | _unassigned_ |

> Update the `Status` column whenever a task agent is assigned, paused, or completed. Replace the `_unassigned_` text with a short note like “in progress via Claude task #42” or “complete – awaiting merge”. When reassigning an agent, overwrite the row instead of adding new ones to keep the roster compact.

## Branching & Iteration

_First-time setup_: ensure `planning/master-plan` exists on origin with the mission files.

1. Start mission workspace with helper script:
   ```bash
   python scripts/agent_sync.py start --mission TA<n>
   ```
   This checks out `feature/<mission>`, rebases on origin, and drops the mission brief under `missions/`.
2. Build & test within that branch. Keep `.claude/` out of commits.
3. Push updates to your fork only:
   ```bash
   git push origin feature/<mission>
   ```

## Preparing a Pull Request

1. Run tests:
   ```bash
   pytest
   python -m build
   ```
2. Ensure docs/changelogs are updated.
3. Log mission progress on planning branch:
   ```bash
   python scripts/agent_sync.py log --mission TA<n> --entry "Summary of work"
   ```
4. Push latest commits to origin:
   ```bash
   git push origin feature/<mission>
   ```
5. Open PR targeting `Promptware-dev/promptware` (`upstream/main`). Include summary + test results.

## Shipping a Release

1. Ready branch merged into `upstream/main`.
2. Update version files (`pyproject.toml`, `Current_Work.md`, `RELEASE_NOTES_<version>.md`).
3. Commit and tag:
   ```bash
   git checkout main
   git reset --hard upstream/main
   git tag <version>
   git push origin main --tags
   git push upstream main --tags
   ```
4. Publish artifacts:
   ```bash
   gh release create <version> --notes-file RELEASE_NOTES_<version>.md --repo Promptware-dev/promptware
   python -m build
   twine upload dist/*
   ```
   *(Replace PyPI step with GitHub Action once automation is live.)*

5. Optionally run integration pipeline before tagging:
   ```bash
   scripts/integration_run.sh
   ```

## Post-Release Checklist

- Update `Current_Work.md` “Next Work”.
- Verify GitHub release + PyPI page show the new version.
- Notify Hustler with a short summary (what shipped, test status, links).

## Guardrails

- Use GitHub noreply identity (`3CH0xyz@users.noreply.github.com`).
- No force pushes to `upstream/main`.
- Keep mission edits on `planning/master-plan` (script handles progress logging).
- When editing mission files manually, stage with `git add --force .claude/...` so the planning branch captures changes.
- Document any manual steps in `Current_Work.md` until CI/CD automation exists.
