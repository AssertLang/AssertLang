#!/usr/bin/env bash
set -euo pipefail

# Integration branch pipeline.
# Usage: scripts/integration_run.sh

FEATURE_BRANCHES=(
  "feature/pw-standard-librarian"
  "feature/pw-runtime-core"
  "feature/pw-tooling-devex"
  "feature/pw-ecosystem-launch"
  "feature/pw-interop-parity"
  "feature/pw-safety-release"
)

INTEGRATION_BRANCH="integration/nightly"

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

echo "==> Ensuring clean working tree"
if [[ -n "$(git status --porcelain)" ]]; then
  echo "Working tree dirty. Aborting." >&2
  exit 1
fi

echo "==> Fetching remotes"
git fetch upstream
git fetch origin

echo "==> Resetting integration branch"
if git show-ref --verify --quiet "refs/heads/${INTEGRATION_BRANCH}"; then
  git branch -D "${INTEGRATION_BRANCH}"
fi
git checkout -b "${INTEGRATION_BRANCH}" upstream/main

echo "==> Merging feature branches"
for branch in "${FEATURE_BRANCHES[@]}"; do
  if git show-ref --verify --quiet "refs/remotes/origin/${branch}"; then
    echo "  -> Merging ${branch}"
    git merge --no-ff "origin/${branch}" -m "Merge ${branch} into ${INTEGRATION_BRANCH}" || {
      echo "Merge conflict detected with ${branch}. Resolve manually." >&2
      exit 1
    }
  else
    echo "  -> Skipping ${branch} (not found on origin)"
  }
done

echo "==> Running test suite"
if command -v pytest >/dev/null 2>&1; then
  pytest
else
  echo "pytest not available; skipping tests." >&2
fi

echo "==> Integration branch ready at ${INTEGRATION_BRANCH}"
echo "    Review tests, then push if desired:"
echo "      git push origin ${INTEGRATION_BRANCH}"
