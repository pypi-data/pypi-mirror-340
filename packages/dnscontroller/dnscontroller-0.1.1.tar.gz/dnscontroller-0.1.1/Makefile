.PHONY: help clean lint test test-ci test-packaging coverage docs release
.DEFAULT_GOAL := help

clean:
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -f {} +
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +
	rm -fr .tox/
	rm -f .coverage
	rm -fr htmlcov/

auto_lint_fix:
	uv run ruff check dnscontroller tests --fix
	uv run isort dnscontroller tests
	uv run black dnscontroller tests
	uv run ruff check dnscontroller tests --fix

lint:
	uv run ruff check dnscontroller tests
	uv run black dnscontroller tests --check
	uv run isort dnscontroller tests --check
	uv run codespell --check-filenames 'tests/**.py' dnscontroller tests pyproject.toml README.md Makefile docs --skip '**/_build'
	uv run mypy --ignore-missing-imports --show-error-codes dnscontroller tests

test:
	uv run pytest

test-ci: lint test

test-packaging:
	# test installing the package fresh on a new computer, using docker
	bash ./test_in_container.sh

coverage:
	uv run coverage run --source dnscontroller -m pytest
	uv run coverage report -m
	uv run coverage html
	$(BROWSER) htmlcov/index.html

docs: ## Generate Sphinx HTML documentation, including API docs
	rm -f docs/dnscontroller.rst
	rm -f docs/modules.rst
	uvx --from sphinx sphinx-apidoc -o docs/ dnscontroller
	uvx --from sphinx $(MAKE) -C docs clean
	uvx --from sphinx $(MAKE) -C docs html
	xdg-open docs/_build/html/index.html

servedocs: docs ## Autoreload docs
	uvx --with sphinx --from watchdog watchmedo shell-command -p '*.rst' -c '$(MAKE) -C docs html' -R -D .

release: clean ## Build and release to PyPI
	# Get primary branch name
	@if [ "$$(git rev-parse --abbrev-ref HEAD)" != "main" ] && [ "$$(git rev-parse --abbrev-ref HEAD)" != "master" ]; then \
		echo "Error: Must be on main/master branch to do release"; \
		exit 1; \
	fi
	@if git diff --exit-code --cached > /dev/null 2>&1 && git diff --exit-code > /dev/null 2>&1; then \
		echo "No changes to commit"; \
		exit 0; \
	else \
		echo "Error, cannot commit release commit with unresolved changes:"; \
		git status --short --untracked-files=no; \
		exit 1; \
	fi
	# Rerun tests
	$(MAKE) lint
	$(MAKE) test
	# Bump version
	rev_version
	# Build & Release to PyPI
	$(MAKE) clean
	uv build
	ls -l dist
	uv publish --token "$$(pcregrep -o1 'password: (pypi-.+)$$' ~/.pypirc)"
	# Push the release to github too.
	git push -u origin $$(git rev-parse --abbrev-ref HEAD)
