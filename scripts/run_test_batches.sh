#!/usr/bin/env bash
set -euo pipefail

# Run the core suites sequentially to avoid environment timeouts.
pytest tests/test_mvp_e2e.py
pytest tests/test_runners_io.py
pytest tests/test_verbs_contracts.py -vv
pytest tests/tools -q
