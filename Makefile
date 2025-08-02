# PATH Framework - Makefile for UV Package Management

.PHONY: help install install-dev test lint format type-check security docs clean build publish

# Default target
help: ## Show this help message
	@echo "PATH Framework - UV Package Management"
	@echo "======================================"
	@echo ""
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'

# Installation commands
install: ## Install production dependencies
	uv sync --no-dev

install-dev: ## Install all dependencies including development tools
	uv sync

install-all: ## Install with all optional dependencies
	uv sync --extra all

# Development commands
test: ## Run all tests
	uv run pytest

test-unit: ## Run unit tests only
	uv run pytest tests/unit -m "not integration and not e2e"

test-integration: ## Run integration tests
	uv run pytest tests/integration -m integration

test-e2e: ## Run end-to-end tests
	uv run pytest tests/e2e -m e2e

test-coverage: ## Run tests with coverage report
	uv run pytest --cov=path_framework --cov-report=html --cov-report=term

# Code quality commands
lint: ## Run linting checks
	uv run flake8 path_framework tests
	uv run isort --check-only path_framework tests

format: ## Format code with black and isort
	uv run black path_framework tests
	uv run isort path_framework tests

type-check: ## Run type checking with mypy
	uv run mypy path_framework

security: ## Run security checks
	uv run bandit -r path_framework
	uv run safety check

# Documentation commands
docs: ## Build documentation
	uv run sphinx-build -b html docs docs/_build/html

docs-serve: ## Serve documentation locally
	uv run python -m http.server 8000 --directory docs/_build/html

# Maintenance commands
clean: ## Clean up build artifacts and cache
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf .pytest_cache/
	rm -rf .mypy_cache/
	rm -rf htmlcov/
	find . -type d -name __pycache__ -delete
	find . -type f -name "*.pyc" -delete

# Build and publish commands
build: ## Build distribution packages
	uv build

publish-test: ## Publish to Test PyPI
	uv publish --repository testpypi

publish: ## Publish to PyPI
	uv publish

# Agent-specific commands
agents-list: ## List all available agents
	uv run path agents list

agents-status: ## Show agent status
	uv run path agents status

# Example project commands
example-init: ## Initialize example project
	uv run path init task-management-example --template api

example-run: ## Run complete example
	cd examples/task_management_api && uv run python run_full_cycle.py

# Environment management
env-info: ## Show environment information
	uv python list
	uv tree

env-update: ## Update all dependencies
	uv sync --upgrade

env-lock: ## Generate lock file
	uv lock

uv-install: ## Install UV package manager (if not installed)
	curl -LsSf https://astral.sh/uv/install.sh | sh

uv-update: ## Update UV to latest version
	uv self update

uv-check: ## Check UV installation and show project info
	@echo "UV Version:"
	@uv --version
	@echo ""
	@echo "Python Versions Available:"
	@uv python list
	@echo ""
	@echo "Project Dependencies:"
	@uv tree --depth 2

uv-add: ## Add a new dependency (usage: make uv-add PACKAGE=package-name)
	uv add $(PACKAGE)

uv-add-dev: ## Add a new development dependency (usage: make uv-add-dev PACKAGE=package-name)
	uv add --dev $(PACKAGE)

uv-remove: ## Remove a dependency (usage: make uv-remove PACKAGE=package-name)
	uv remove $(PACKAGE)

uv-outdated: ## Check for outdated dependencies
	uv pip list --outdated

# CI/CD commands
ci-setup: ## Set up CI environment
	uv sync --frozen

ci-test: ## Run CI test suite
	uv run pytest --junitxml=test-results.xml --cov=path_framework --cov-report=xml

ci-lint: ## Run CI linting checks
	uv run flake8 --format=junit-xml --output-file=lint-results.xml path_framework tests || true
	uv run mypy --junit-xml=type-check-results.xml path_framework || true

# Docker commands
docker-build: ## Build Docker image
	docker build -t path-framework:latest .

docker-run: ## Run Docker container
	docker run -it --rm path-framework:latest

docker-compose-up: ## Start development environment with docker-compose
	docker-compose up -d

docker-compose-down: ## Stop development environment
	docker-compose down

# Deployment commands
deploy-staging: ## Deploy to staging environment
	uv run path deploy --environment staging

deploy-prod: ## Deploy to production environment
	uv run path deploy --environment production --confirm

# Performance and profiling
benchmark: ## Run performance benchmarks
	uv run pytest tests/benchmarks -m benchmark

profile: ## Run profiling
	uv run python -m cProfile -o profile.stats -m path_framework.cli --help
	uv run python -c "import pstats; pstats.Stats('profile.stats').sort_stats('cumulative').print_stats(20)"

# Database commands (for examples)
db-setup: ## Set up example database
	docker run -d --name path-postgres -e POSTGRES_PASSWORD=pathpass -p 5432:5432 postgres:14

db-migrate: ## Run database migrations
	uv run alembic upgrade head

db-reset: ## Reset example database
	docker stop path-postgres || true
	docker rm path-postgres || true
	$(MAKE) db-setup

# Utility commands
validate-config: ## Validate PATH configuration
	uv run path validate-config

generate-report: ## Generate project report
	uv run path report --format html --output reports/latest.html

# Development workflow shortcuts
dev-setup: install-dev docs ## Complete development setup

pre-commit: format lint type-check test-unit ## Run pre-commit checks

full-check: format lint type-check security test test-coverage ## Run all checks

release-check: full-check build ## Prepare for release

# Version management
version-patch: ## Bump patch version
	uv run bump2version patch

version-minor: ## Bump minor version
	uv run bump2version minor

version-major: ## Bump major version
	uv run bump2version major

# Special targets for different environments
local: install-dev ## Set up for local development
	@echo "Local development environment ready!"
	@echo "Run 'make example-init' to create a sample project"

production: install ## Set up for production
	@echo "Production environment ready!"

ci: ci-setup ci-lint ci-test ## Complete CI pipeline

# Quick start for new users
quickstart: ## Quick start guide for new users
	@echo "PATH Framework Quick Start"
	@echo "=========================="
	@echo ""
	@echo "1. Install dependencies:"
	@echo "   make install-dev"
	@echo ""
	@echo "2. Run tests:"
	@echo "   make test"
	@echo ""
	@echo "3. Create example project:"
	@echo "   make example-init"
	@echo ""
	@echo "4. Run example:"
	@echo "   make example-run"
	@echo ""
	@echo "5. View documentation:"
	@echo "   make docs && make docs-serve"
