.PHONY: install test lint format clean docs help

help:  ## Show this help
	@egrep -h '\s##\s' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install:  ## Install dependencies
	poetry install

test:  ## Run tests with coverage
	poetry run pytest -v --cov=no_more_secrets --cov-report=term-missing --cov-report=html

test-fast:  ## Run tests without coverage
	poetry run pytest -v

test-specific:  ## Run specific test file (usage: make test-specific TEST=test_colors.py)
	poetry run pytest -v tests/$(TEST)

test-watch:  ## Run tests in watch mode (requires pytest-watch)
	poetry run ptw --runner "poetry run pytest"

lint:  ## Run linting
	poetry run flake8 no_more_secrets tests
	poetry run mypy no_more_secrets

format:  ## Format code
	poetry run black .
	poetry run isort .

format-check:  ## Check code formatting
	poetry run black --check .
	poetry run isort --check-only .

clean:  ## Clean up build artifacts
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf .pytest_cache/
	rm -rf .coverage
	find . -type d -name __pycache__ -delete
	find . -type f -name "*.pyc" -delete

docs:  ## Build documentation
	poetry run mkdocs build

docs-serve:  ## Serve documentation locally (port 8080)
	poetry run mkdocs serve --dev-addr=127.0.0.1:8080

docs-serve-alt:  ## Serve documentation on alternative port (8888)
	poetry run mkdocs serve --dev-addr=127.0.0.1:8888

docs-serve-random:  ## Serve documentation on random available port
	poetry run mkdocs serve --dev-addr=127.0.0.1:0

docs-deploy:  ## Deploy documentation to GitHub Pages
	poetry run mkdocs gh-deploy

build:  ## Build package
	poetry build

publish:  ## Publish to PyPI (requires authentication)
	poetry publish

pre-commit:  ## Install pre-commit hooks
	poetry run pre-commit install

pre-commit-run:  ## Run pre-commit on all files
	poetry run pre-commit run --all-files

demo:  ## Run demo commands
	@echo "=== Basic Demo ==="
	echo "Hello, World!" | poetry run nms -a
	@echo "\n=== Color Demo ==="
	echo "This is green text" | poetry run nms -a -f green
	@echo "\n=== Sneakers Demo ==="
	poetry run sneakers

tree-demo:  ## Demo with tree command
	@echo "=== Tree Demo ==="
	tree | head -10 | poetry run nms -a -f green