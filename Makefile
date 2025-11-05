SRC_FILES = sphinx_simplepdf/

.PHONY: list
list:
	@$(MAKE) -pRrq -f $(lastword $(MAKEFILE_LIST)) : 2>/dev/null | awk -v RS= -F: '/^# File/,/^# Finished Make data base/ {if ($$1 !~ "^[#.]") {print $$1}}' | sort | egrep -v -e '^[^[:alnum:]]' -e '^$@$$'

.PHONY: lint
lint:
	pre-commit run --all-files

#.PHONY: test
#test:
#	uv run pytest -n auto --tb=long tests/

.PHONY: test-matrix
test-matrix:
	uv run tox

.PHONY: docs-html
docs-html:
	uv run sphinx-build -a -E -j auto -b html docs/ docs/_build

.PHONY: docs-html-fast
docs-html-fast:
	uv run sphinx-build -j auto -b html docs/ docs/_build

.PHONY: docs-pdf
docs-pdf:
	uv run make --directory docs/ clean && uv run make --directory docs/ latexpdf

.PHONY: demo-pdf
demo-pdf:
	uv run sphinx-build -M simplepdf demo demo/_build

.PHONY: docs-linkcheck
docs-linkcheck:
	uv run make --directory docs/ linkcheck

.PHONY: format
format:
	uv run ruff format ${SRC_FILES}
	uv run ruff check --fix ${SRC_FILES}
