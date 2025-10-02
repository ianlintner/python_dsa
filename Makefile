
# Makefile for Documentation (Bastage-style with plugins)

.PHONY: docs clean-docs serve-docs lint format fix

# Directory for built docs
DOCS_BUILD_DIR=site
# Linting and formatting
lint:
	@echo "Running flake8 lint checks..."
	flake8 src flask_app tests

format:
	@echo "Running black code formatter..."
	black --verbose --diff --color src flask_app tests || true

fix:
	@echo "Running pre-commit hooks (ruff, ruff-format, etc.)..."
	pre-commit run --all-files || true
	@echo "Auto-formatting and linting complete (errors ignored)."

# Default target: build docs
docs:
	@echo "Building documentation with Docker image..."
	docker run --rm -v $(PWD):/docs squidfunk/mkdocs-material build --clean

# Serve docs locally
serve-docs:
	@echo "Serving documentation at http://127.0.0.1:8000"
	mkdocs serve

# Clean built docs
clean-docs:
	@echo "Cleaning built documentation..."
	rm -rf $(DOCS_BUILD_DIR)
