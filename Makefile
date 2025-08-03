# PATH Framework - Makefile for UV Package Management

.PHONY: help install install-dev test lint format type-check security docs clean build publish

# Default target
help: ## Show this help message
	@echo "PATH Framework - UV Package Management"
	@echo "======================================"
	@echo ""
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'

help-maintenance: ## Show maintenance commands only
	@echo "PATH Framework - Maintenance Commands"
	@echo "===================================="
	@echo ""
	@echo "🧹 Cleaning & Cleanup:"
	@echo "  clean              - Clean up build artifacts and cache"
	@echo "  clean-projects     - Clean all generated projects only"
	@echo "  clean-all          - Deep clean: artifacts, cache, projects, and dependencies"
	@echo "  clean-nuclear      - Nuclear clean: everything including .venv (requires uv sync)"
	@echo ""
	@echo "💾 Backup & Restore:"
	@echo "  backup-projects    - Backup all projects to timestamped archive"
	@echo "  restore-projects   - Restore projects from backup archive"
	@echo ""
	@echo "🔧 System Health:"
	@echo "  health-check       - Comprehensive framework health check"
	@echo "  update-deps        - Update all dependencies to latest versions"
	@echo "  security-audit     - Run comprehensive security audit"
	@echo ""
	@echo "📊 Code Quality:"
	@echo "  code-quality       - Run comprehensive code quality checks"
	@echo "  format-code        - Auto-format all code"
	@echo "  performance-profile - Profile framework performance"
	@echo ""
	@echo "🚀 Release Management:"
	@echo "  release-check      - Pre-release validation checklist"
	@echo "  maintenance-report - Generate comprehensive maintenance report"
	@echo ""
	@echo "💡 Usage examples:"
	@echo "  make health-check        # Quick system check"
	@echo "  make backup-projects     # Backup before major changes"
	@echo "  make release-check       # Before creating a release"

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
	@echo "🧹 Cleaning build artifacts and cache..."
	@rm -rf build/
	@rm -rf dist/
	@rm -rf *.egg-info/
	@rm -rf .pytest_cache/
	@rm -rf .mypy_cache/
	@rm -rf htmlcov/
	@echo "Removing __pycache__ directories..."
	@find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	@find . -name "*.pyc" -delete 2>/dev/null || true
	@find . -name "*.pyo" -delete 2>/dev/null || true
	@echo "✅ Clean completed!"

clean-projects: ## Clean all generated projects only
	@echo "🗂️  Cleaning generated projects..."
	@if [ -d "projects" ]; then \
		echo "Removing all projects in projects/ directory..."; \
		rm -rf projects/*/; \
		echo "✅ Projects cleaned successfully!"; \
	else \
		echo "📁 No projects directory found"; \
	fi

clean-all: ## Deep clean: artifacts, cache, projects, and dependencies
	@echo "🧹 Performing deep clean..."
	@make clean
	@echo "Removing all generated projects..."
	@rm -rf projects/
	@echo "Cleaning UV cache..."
	@uv cache clean
	@echo "✅ Deep clean completed!"

clean-nuclear: ## Nuclear clean: everything including .venv (requires uv sync afterward)
	@echo "☢️  Performing nuclear clean - removing EVERYTHING..."
	@echo "This will remove .venv and require 'uv sync' to rebuild"
	@read -p "Are you sure? [y/N]: " confirm; \
	if [ "$$confirm" = "y" ] || [ "$$confirm" = "Y" ]; then \
		echo "🧹 Cleaning build artifacts..."; \
		rm -rf build/ dist/ *.egg-info/ .pytest_cache/ .mypy_cache/ htmlcov/; \
		echo "💥 Removing ALL __pycache__ directories (including .venv)..."; \
		find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true; \
		find . -name "*.pyc" -delete 2>/dev/null || true; \
		find . -name "*.pyo" -delete 2>/dev/null || true; \
		echo "🗂️  Removing projects directory..."; \
		rm -rf projects/; \
		echo "💀 Removing virtual environment..."; \
		rm -rf .venv/; \
		echo "🧹 Cleaning UV cache..."; \
		uv cache clean; \
		echo "☢️  Nuclear clean completed!"; \
		echo "🔄 Run 'uv sync' to rebuild your environment"; \
	else \
		echo "❌ Nuclear clean cancelled"; \
	fi

backup-projects: ## Backup all projects to timestamped archive
	@echo "💾 Creating projects backup..."
	@if [ -d "projects" ]; then \
		timestamp=$$(date +"%Y%m%d_%H%M%S"); \
		backup_name="projects_backup_$$timestamp.tar.gz"; \
		tar -czf "$$backup_name" projects/; \
		echo "✅ Projects backed up to: $$backup_name"; \
		ls -lh "$$backup_name"; \
	else \
		echo "⚠️  No projects directory found"; \
	fi

restore-projects: ## Restore projects from backup archive
	@echo "📂 Restoring projects from backup..."
	@echo "Available backups:"
	@ls -1 projects_backup_*.tar.gz 2>/dev/null || echo "No backup files found"
	@read -p "Enter backup filename: " backup_file; \
	if [ -f "$$backup_file" ]; then \
		echo "Extracting $$backup_file..."; \
		tar -xzf "$$backup_file"; \
		echo "✅ Projects restored from $$backup_file"; \
	else \
		echo "❌ Backup file not found: $$backup_file"; \
	fi

health-check: ## Comprehensive framework health check
	@echo "🏥 PATH Framework Health Check"
	@echo "=============================="
	@echo ""
	@echo "1️⃣  Environment Check:"
	@make uv-check
	@echo ""
	@echo "2️⃣  Dependencies Check:"
	@uv sync --dry-run
	@echo ""
	@echo "3️⃣  Framework Structure:"
	@echo "Core modules:"
	@ls -la path_framework/core/ 2>/dev/null || echo "❌ Core missing"
	@echo "Architecture phase:"
	@ls -la path_framework/phases/arch/ 2>/dev/null || echo "❌ Arch phase missing"
	@echo ""
	@echo "4️⃣  Test Suite:"
	@make test-unit
	@echo ""
	@echo "5️⃣  Project Status:"
	@make arch-status

update-deps: ## Update all dependencies to latest compatible versions
	@echo "🔄 Updating dependencies..."
	@uv sync --upgrade
	@echo "📋 Generating dependency report..."
	@uv tree > dependency-report.txt
	@echo "✅ Dependencies updated! Report saved to dependency-report.txt"

security-audit: ## Run comprehensive security audit
	@echo "🔒 Running security audit..."
	@echo "1. Checking for known vulnerabilities..."
	@uv run safety check --json > security-report.json 2>/dev/null || echo "Safety check completed"
	@echo "2. Running bandit security scan..."
	@uv run bandit -r path_framework -f json -o bandit-report.json || echo "Bandit scan completed"
	@echo "3. Checking for outdated packages..."
	@uv tree --outdated > outdated-packages.txt 2>/dev/null || echo "Package check completed"
	@echo "✅ Security audit completed! Reports saved to:"
	@echo "   - security-report.json"
	@echo "   - bandit-report.json" 
	@echo "   - outdated-packages.txt"

performance-profile: ## Profile framework performance
	@echo "⚡ Running performance profiling..."
	@uv run python -m cProfile -o profile-stats.prof -m path_framework.cli --help
	@echo "Generating profile report..."
	@uv run python -c "import pstats; p=pstats.Stats('profile-stats.prof'); p.sort_stats('cumulative').print_stats(20)" > profile-report.txt
	@echo "✅ Performance profile saved to profile-report.txt"

code-quality: ## Run comprehensive code quality checks
	@echo "📊 Running code quality analysis..."
	@echo "1. Code formatting (black)..."
	@uv run black --check --diff path_framework/ || echo "Formatting issues found"
	@echo "2. Import sorting (isort)..."
	@uv run isort --check-only --diff path_framework/ || echo "Import sorting issues found"
	@echo "3. Type checking (mypy)..."
	@uv run mypy path_framework/ || echo "Type checking completed"
	@echo "4. Linting (flake8)..."
	@uv run flake8 path_framework/ || echo "Linting completed"
	@echo "5. Complexity analysis..."
	@uv run radon cc path_framework/ -a || echo "Complexity analysis completed"
	@echo "✅ Code quality analysis completed!"

format-code: ## Auto-format all code
	@echo "🎨 Formatting code..."
	@uv run black path_framework/
	@uv run isort path_framework/
	@echo "✅ Code formatted!"

release-check: ## Pre-release validation checklist
	@echo "🚀 Release Readiness Check"
	@echo "=========================="
	@echo ""
	@echo "✅ Running comprehensive checks..."
	@make health-check
	@echo ""
	@make security-audit
	@echo ""
	@make code-quality
	@echo ""
	@echo "📋 Release Checklist:"
	@echo "  [ ] All tests passing"
	@echo "  [ ] Documentation updated"
	@echo "  [ ] Security audit clean"
	@echo "  [ ] Performance acceptable"
	@echo "  [ ] Version bumped in pyproject.toml"
	@echo "  [ ] CHANGELOG.md updated"
	@echo "  [ ] Git tag created"

maintenance-report: ## Generate comprehensive maintenance report
	@echo "📊 Generating maintenance report..."
	@timestamp=$$(date +"%Y-%m-%d_%H-%M-%S"); \
	report_file="maintenance-report-$$timestamp.md"; \
	echo "# PATH Framework Maintenance Report" > $$report_file; \
	echo "Generated: $$(date)" >> $$report_file; \
	echo "" >> $$report_file; \
	echo "## Environment" >> $$report_file; \
	uv --version >> $$report_file 2>&1; \
	echo "" >> $$report_file; \
	echo "## Dependencies" >> $$report_file; \
	uv tree >> $$report_file 2>&1; \
	echo "" >> $$report_file; \
	echo "## Project Structure" >> $$report_file; \
	find path_framework -name "*.py" | wc -l | xargs echo "Python files:" >> $$report_file; \
	find . -name "*.md" | wc -l | xargs echo "Documentation files:" >> $$report_file; \
	echo "" >> $$report_file; \
	echo "## Test Coverage" >> $$report_file; \
	make test-coverage >> $$report_file 2>&1; \
	echo "✅ Maintenance report saved to: $$report_file"
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

# Arch Phase Operations - Architecture & Software Engineering
arch-init: ## Initialize new project for Architecture phase
	@echo "🚀 Initializing new PATH Framework project..."
	@read -p "Enter project name: " project_name; \
	uv run python -m path_framework.cli init "$$project_name" --template default
	@echo "✅ Project initialized in projects/ directory"

arch-run: ## Run Architecture phase generation
	@echo "🏗️  Running Architecture & Software Engineering phase..."
	@read -p "Enter project name: " project_name; \
	uv run python -m path_framework.cli arch "$$project_name" --path "./projects/$$project_name" --interactive

arch-demo: ## Run Architecture phase demonstration with sample project
	@echo "🎯 Running Architecture phase demo with sample e-commerce project..."
	uv run python demo_proper_projects.py
	@echo "📁 Check results in: projects/demo-ecommerce-platform/path_artifacts/arch/"

arch-llm-demo: ## Demonstrate real LLM integration
	@echo "🤖 Testing PATH Framework with real LLM integration..."
	@echo "💡 Set OPENAI_API_KEY or ANTHROPIC_API_KEY for real LLM calls"
	uv run python demo_llm_standalone.py

arch-validate: ## Validate Architecture phase implementation and run tests
	@echo "✅ Validating Architecture phase implementation..."
	uv run pytest framework_tests/ -v -k "arch" --tb=short
	@echo "📊 Checking test coverage for Architecture phase..."
	uv run pytest framework_tests/ --cov=path_framework.phases.arch --cov-report=term

arch-full: ## Complete Architecture workflow: init + architecture + validation
	@echo "🎯 Running complete Architecture phase workflow..."
	@read -p "Enter project name: " project_name; \
	echo "1️⃣  Initializing project: $$project_name"; \
	uv run python -m path_framework.cli init "$$project_name" --template default; \
	echo "2️⃣  Running architecture phase..."; \
	uv run python -m path_framework.cli arch "$$project_name" --path "./projects/$$project_name" --non-interactive; \
	echo "3️⃣  Validating results..."; \
	if [ -d "./projects/$$project_name/path_artifacts/arch" ]; then \
		echo "✅ Architecture phase artifacts generated successfully!"; \
		ls -la "./projects/$$project_name/path_artifacts/arch/"; \
	else \
		echo "❌ Phase 1 artifacts not found"; \
	fi

arch-clean: ## Clean all generated artifacts for a project
	@echo "🧹 Cleaning project artifacts..."
	@read -p "Enter project name: " project_name; 
	if [ -d "./projects/$$project_name" ]; then 
		echo "Removing artifacts for project: $$project_name"; 
		rm -rf "./projects/$$project_name/path_artifacts/"; 
		echo "✅ Artifacts cleaned successfully!"; 
	else 
		echo "❌ Project $$project_name not found in ./projects/"; 
	fi

arch-status: ## Show Architecture phase implementation status
	@echo "📊 PATH Framework Architecture Phase Status"
	@echo "==========================================="
	@echo ""
	@echo "🏗️  Implementation Status:"
	@if [ -f "path_framework/phases/arch/simple_orchestrator.py" ]; then \
		echo "  ✅ Simple Orchestrator: Ready"; \
	else \
		echo "  ❌ Simple Orchestrator: Missing"; \
	fi
	@if [ -f "path_framework/phases/arch/ai/domain_analyst.py" ]; then \
		echo "  ✅ AI Domain Analyst: Ready"; \
	else \
		echo "  ❌ AI Domain Analyst: Missing"; \
	fi
	@if [ -f "path_framework/core/llm_client.py" ]; then \
		echo "  ✅ LLM Integration: Ready"; \
	else \
		echo "  ❌ LLM Integration: Missing"; \
	fi
	@echo ""
	@echo "📁 Projects Directory:"
	@if [ -d "projects" ]; then \
		echo "  ✅ Projects folder exists"; \
		echo "  📊 Projects: $$(ls projects/ 2>/dev/null | wc -l) found"; \
		if [ $$(ls projects/ 2>/dev/null | wc -l) -gt 0 ]; then \
			echo "  📂 Active projects:"; \
			ls -1 projects/ | sed 's/^/    - /'; \
		fi; \
	else \
		echo "  📁 No projects directory (will be created on first use)"; \
	fi
	@echo ""
	@echo "🤖 LLM Integration:"
	@if [ -n "$$OPENAI_API_KEY" ]; then \
		echo "  ✅ OpenAI API key configured"; \
	elif [ -n "$$ANTHROPIC_API_KEY" ]; then \
		echo "  ✅ Anthropic API key configured"; \
	else \
		echo "  ⚠️  No LLM API keys configured (will use mock mode)"; \
	fi
	@echo ""
	@echo "📚 Available Commands:"
	@echo "  make arch-init     - Initialize new project"
	@echo "  make arch-run      - Run architecture generation"
	@echo "  make arch-demo     - Run sample demonstration"
	@echo "  make arch-full     - Complete Architecture workflow"

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
	@echo "3. Check Architecture phase status:"
	@echo "   make arch-status"
	@echo ""
	@echo "4. Try Architecture demo:"
	@echo "   make arch-demo"
	@echo ""
	@echo "5. Create your project:"
	@echo "   make arch-init"
	@echo ""
	@echo "6. Run architecture phase:"
	@echo "   make arch-run"
	@echo ""
	@echo "7. View documentation:"
	@echo "   make docs && make docs-serve"
	@echo ""
	@echo "💡 For real LLM integration:"
	@echo "   export OPENAI_API_KEY='your-key'"
	@echo "   make arch-llm-demo"
