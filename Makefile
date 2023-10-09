SHELL:=/usr/bin/env bash
PKGDIR = quote_scraper

.PHONY: format
format:
	poetry run isort $(PKGDIR) tests
	poetry run black $(PKGDIR) tests

.PHONY: mypy
mypy:
	poetry run mypy $(PKGDIR) tests

.PHONY: flake
flake:
	poetry run flake8 $(PKGDIR) tests

.PHONY: lint
lint: format mypy flake
	# poetry run docr8 -q docs

.PHONY: sunit
sunit:
	poetry run pytest -s tests

.PHONY: unit
unit:
	poetry run pytest tests

.PHONY: package
package:
	poetry check
	poetry run pip check
	poetry run safety check --short-report

.PHONY: test
test: lint package unit

.PHONY: stest
stest: lint package sunit

.PHONY: clean
clean: clean-build clean-pyc clean-test ## remove all build, test, coverage and Python artifacts

.PHONY: clean-build
clean-build: ## remove build artifacts
	rm -fr build/
	rm -fr docs/_build
	rm -fr dist/
	rm -fr .eggs/
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -f {} +

.PHONY: clean-pyc
clean-pyc: ## remove Python file artifacts
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

.PHONY: clean-test
clean-test: ## remove test and coverage artifacts
	rm -fr .tox/
	rm -f .coverage
	rm -fr htmlcov/
	rm -fr .pytest_cache
	rm -fr .mypy_cache
