.DEFAULT_GOAL := list

# Detect OS for platform-specific settings
UNAME := $(shell uname -s)

# macOS: Set library path for WeasyPrint native dependencies (Homebrew)
ifeq ($(UNAME),Darwin)
    BREW_PREFIX := $(shell brew --prefix 2>/dev/null)
    ifneq ($(BREW_PREFIX),)
        WEASYPRINT_ENV := DYLD_LIBRARY_PATH="$(BREW_PREFIX)/lib:$$DYLD_LIBRARY_PATH"
    endif
endif

.PHONY: list
list:
	@echo "Available targets:"
	@echo "  make lint          - Run pre-commit on all files"
	@echo "  make format        - Run pre-commit on all files (alias for lint)"
	@echo "  make test          - Run pytest"
	@echo "  make test-matrix   - Run nox for testing matrix"
	@echo "  make coverage      - Generate coverage reports"
	@echo "  make docs-html     - Build HTML documentation"
	@echo "  make docs-pdf      - Build PDF documentation"
	@echo "  make docs-linkcheck - Check documentation links"
	@echo "  make install       - Install package in development mode"
	@echo "  make install-dev   - Install package with dev dependencies"
	@echo "  make clean         - Clean build artifacts"

.PHONY: lint format
lint format:
	uv run pre-commit run --all-files

.PHONY: test
test:
	uv sync --group dev && uv run pytest

.PHONY: test-matrix
test-matrix:
	uv sync --group dev && uv run tox

.PHONY: coverage
coverage:
	uv run pytest --cov=sphinx_simplepdf --cov-report=html --cov-report=term || test $$? -eq 5

.PHONY: docs-demo
docs-demo:
	uv sync --group demo && uv run sphinx-build -M simplepdf demo demo/_build

.PHONY: docs-demo-deploy
docs-demo-deploy: docs-demo
	mkdir -p docs/_build
	cp demo/_build/simplepdf/Sphinx-SimplePDF-DEMO.pdf docs/_static

.PHONY: docs-html
docs-html: docs-demo-deploy
	uv sync --group docs && uv run sphinx-build -M html docs docs/_build

.PHONY: docs-pdf
docs-pdf: docs-demo-deploy
	uv sync --group docs && $(WEASYPRINT_ENV) uv run sphinx-build -M simplepdf docs docs/_build

.PHONY: docs-linkcheck
docs-linkcheck: docs-demo-deploy
	uv sync --group docs && uv run sphinx-build -M linkcheck docs docs/_build

.PHONY: install
install:
	uv sync

.PHONY: install-dev
install-dev:
	uv sync --group dev

.PHONY: clean
clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf .pytest_cache/
	rm -rf .ruff_cache/
	rm -rf .mypy_cache/
	rm -rf htmlcov/
	rm -rf docs/_build/
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.py[co]" -delete 2>/dev/null || true
