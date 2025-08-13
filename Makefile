SHELL := /bin/bash

.PHONY: help install precommit-install precommit-all format format-check lint lint-fix test check ci

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
	python -m pip install -U pip
	python -m pip install -e ".[dev]"

precommit-install:
	pre-commit install

precommit-all:
	pre-commit run --all-files --show-diff-on-failure --color=always

format:
	ruff format .

format-check:
	ruff format --check .

lint:
	ruff check .

lint-fix:
	ruff check --fix

test:
	python -m pytest -q

check: format-check lint

ci: install precommit-all test
