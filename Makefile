.PHONY: install run run-hold e2e test lint format clean

VENV=.venv

install:
	python3 -m venv $(VENV)
	. $(VENV)/bin/activate; pip install -U pip
	. $(VENV)/bin/activate; pip install -e .

run:
	. $(VENV)/bin/activate; mcp run "Create a web service that responds 'Hello, World!'"

run-hold:
	. $(VENV)/bin/activate; mcp run --hold "Create a web service that responds 'Hello, World!'"

e2e:
	. $(VENV)/bin/activate; pytest -q tests/test_mvp_e2e.py || true

test:
	. $(VENV)/bin/activate; pytest -q || true

lint:
	. $(VENV)/bin/activate; python -m pip install ruff || true
	. $(VENV)/bin/activate; ruff check . || true

format:
	. $(VENV)/bin/activate; python -m pip install black || true
	. $(VENV)/bin/activate; black daemon runners cli tests || true

clean:
	rm -rf $(VENV) .pytest_cache **/__pycache__ .mcpd/*

