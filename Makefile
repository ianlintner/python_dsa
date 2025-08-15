SHELL := /bin/bash

PYTHON ?= python3

.PHONY: help install precommit-install precommit-all format format-check lint lint-fix test check ci run-ui

help:
	@echo "Targets:"
	@echo "  install            Install project with dev extras (ruff, pre-commit, pytest)"
	@echo "  precommit-install  Install git hooks (pre-commit)"
	@echo "  precommit-all      Run all pre-commit hooks across the repo"
	@echo "  format             Format code with Ruff formatter"
	@echo "  format-check       Check formatting (no changes)"
	@echo "  lint               Lint with Ruff"
	@echo "  lint-fix           Lint with Ruff and autofix"
	@echo "  test               Run pytest"
	@echo "  check              Run format-check + lint"
	@echo "  ci                 Install deps, run hooks, run tests (local CI parity)"

install:
	$(PYTHON) -m pip install -U pip
	$(PYTHON) -m pip install -e ".[dev]"

precommit-install:
	pre-commit install

precommit-all:
	pre-commit run --all-files --show-diff-on-failure --color=always

format:
	$(PYTHON) -m ruff format .

format-check:
	$(PYTHON) -m ruff format --check .

lint:
	$(PYTHON) -m ruff check .

lint-fix:
	$(PYTHON) -m ruff check --fix

test:
	$(PYTHON) -m pytest -q

check: format-check lint

ci: install precommit-all test

# Run the Flask UI for demos
run-ui:
	python3 flask_app/app.py
