# Makefile for Direct Web Spider
# Provides convenient commands for development, testing, and deployment

.PHONY: help install test coverage lint format clean docs pre-commit ci all

# Default target
.DEFAULT_GOAL := help

# Colors for output
BLUE := \033[0;34m
GREEN := \033[0;32m
YELLOW := \033[0;33m
RED := \033[0;31m
NC := \033[0m  # No Color

help: ## Show this help message
	@echo "$(BLUE)Direct Web Spider - Development Commands$(NC)"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "$(GREEN)%-20s$(NC) %s\n", $$1, $$2}'

install: ## Install dependencies
	@echo "$(BLUE)Installing dependencies...$(NC)"
	python3 -m pip install --upgrade pip
	pip3 install -r requirements.txt
	@echo "$(GREEN)✓ Dependencies installed$(NC)"

install-dev: install ## Install development dependencies
	@echo "$(BLUE)Installing development dependencies...$(NC)"
	pip3 install pre-commit black flake8 pylint mypy isort bandit
	pre-commit install
	@echo "$(GREEN)✓ Development environment ready$(NC)"

test: ## Run all tests
	@echo "$(BLUE)Running test suite...$(NC)"
	pytest tests/ -v

test-unit: ## Run unit tests only
	@echo "$(BLUE)Running unit tests...$(NC)"
	pytest tests/ -v -m unit

test-integration: ## Run integration tests only
	@echo "$(BLUE)Running integration tests...$(NC)"
	pytest tests/ -v -m integration

test-fast: ## Run tests (skip slow tests)
	@echo "$(BLUE)Running fast tests...$(NC)"
	pytest tests/ -v -m "not slow"

test-parallel: ## Run tests in parallel
	@echo "$(BLUE)Running tests in parallel...$(NC)"
	pytest tests/ -v -n auto

coverage: ## Run tests with coverage report
	@echo "$(BLUE)Running tests with coverage...$(NC)"
	pytest tests/ -v --cov=spider --cov=scripts --cov-report=html --cov-report=term-missing
	@echo "$(GREEN)✓ Coverage report: htmlcov/index.html$(NC)"

coverage-100: ## Enforce 100% coverage
	@echo "$(BLUE)Running tests with 100% coverage requirement...$(NC)"
	pytest tests/ -v --cov=spider --cov=scripts --cov-report=html --cov-report=term-missing --cov-fail-under=100

comprehensive: ## Run comprehensive test suite
	@echo "$(BLUE)Running comprehensive test suite...$(NC)"
	python3 test_comprehensive.py --coverage --quality --security --save-results
	@echo "$(GREEN)✓ Comprehensive tests complete$(NC)"

lint: ## Run linting checks
	@echo "$(BLUE)Running linters...$(NC)"
	flake8 spider/ scripts/ --count --statistics
	@echo "$(GREEN)✓ Linting complete$(NC)"

format: ## Format code with black and isort
	@echo "$(BLUE)Formatting code...$(NC)"
	black spider/ scripts/ tests/
	isort spider/ scripts/ tests/
	@echo "$(GREEN)✓ Code formatted$(NC)"

format-check: ## Check code formatting
	@echo "$(BLUE)Checking code format...$(NC)"
	black --check spider/ scripts/ tests/
	isort --check-only spider/ scripts/ tests/

type-check: ## Run type checking with mypy
	@echo "$(BLUE)Running type checks...$(NC)"
	mypy spider/ scripts/ --ignore-missing-imports

security: ## Run security checks
	@echo "$(BLUE)Running security analysis...$(NC)"
	bandit -r spider/ scripts/ -f screen

quality: lint format-check type-check security ## Run all quality checks

clean: ## Clean build artifacts and caches
	@echo "$(BLUE)Cleaning build artifacts...$(NC)"
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null || true
	rm -rf dist/ build/ htmlcov/ .coverage coverage.xml
	@echo "$(GREEN)✓ Cleaned$(NC)"

pre-commit: ## Run pre-commit hooks
	@echo "$(BLUE)Running pre-commit hooks...$(NC)"
	pre-commit run --all-files

pre-commit-update: ## Update pre-commit hooks
	@echo "$(BLUE)Updating pre-commit hooks...$(NC)"
	pre-commit autoupdate

docs: ## Generate documentation
	@echo "$(BLUE)Generating documentation...$(NC)"
	@echo "$(YELLOW)Documentation generation not yet implemented$(NC)"

setup: install-dev ## Complete development setup
	@echo "$(BLUE)Setting up development environment...$(NC)"
	mkdir -p log test_results htmlcov
	@echo "$(GREEN)✓ Development environment ready$(NC)"
	@echo ""
	@echo "$(BLUE)Next steps:$(NC)"
	@echo "  1. Run 'make test' to run tests"
	@echo "  2. Run 'make coverage' to generate coverage report"
	@echo "  3. Run 'make comprehensive' for full test suite"

ci: clean quality coverage ## Run CI pipeline locally
	@echo "$(GREEN)✓ CI pipeline complete$(NC)"

all: clean install quality coverage ## Run everything
	@echo "$(GREEN)✓ All tasks complete$(NC)"

# Individual test categories
test-logger: ## Test logger module
	pytest tests/test_logger.py -v

test-encoding: ## Test encoding module
	pytest tests/test_encoding.py -v

test-utils: ## Test utils module
	pytest tests/test_utils.py -v

test-models: ## Test all models
	pytest tests/models/ -v

test-downloaders: ## Test all downloaders
	pytest tests/downloaders/ -v

test-fetchers: ## Test all fetchers
	pytest tests/fetchers/ -v

test-parsers: ## Test all parsers
	pytest tests/parsers/ -v

# Site-specific tests
test-dangdang: ## Test Dangdang site
	pytest tests/ -v -m dangdang

test-jingdong: ## Test JingDong site
	pytest tests/ -v -m jingdong

test-tmall: ## Test Tmall site
	pytest tests/ -v -m tmall

# Benchmarking
benchmark: ## Run performance benchmarks
	@echo "$(BLUE)Running benchmarks...$(NC)"
	pytest tests/ --benchmark-only

# Coverage badges and reports
coverage-badge: coverage ## Generate coverage badge
	@echo "$(BLUE)Generating coverage badge...$(NC)"
	coverage-badge -o coverage.svg -f
	@echo "$(GREEN)✓ Coverage badge: coverage.svg$(NC)"

# Watch mode for development
watch: ## Watch for changes and run tests
	@echo "$(BLUE)Watching for changes...$(NC)"
	pytest-watch tests/ -- -v

# Database operations
mongo-start: ## Start MongoDB (local)
	@echo "$(BLUE)Starting MongoDB...$(NC)"
	sudo systemctl start mongodb || brew services start mongodb-community

mongo-stop: ## Stop MongoDB
	@echo "$(BLUE)Stopping MongoDB...$(NC)"
	sudo systemctl stop mongodb || brew services stop mongodb-community

mongo-status: ## Check MongoDB status
	@echo "$(BLUE)MongoDB status:$(NC)"
	sudo systemctl status mongodb || brew services list | grep mongodb

# Requirements management
requirements-update: ## Update requirements.txt
	@echo "$(BLUE)Updating requirements...$(NC)"
	pip freeze > requirements.txt
	@echo "$(GREEN)✓ Requirements updated$(NC)"

requirements-check: ## Check for outdated packages
	@echo "$(BLUE)Checking for outdated packages...$(NC)"
	pip list --outdated

# Git operations
git-hooks: ## Install git hooks
	@echo "$(BLUE)Installing git hooks...$(NC)"
	pre-commit install --install-hooks
	@echo "$(GREEN)✓ Git hooks installed$(NC)"

# Information
info: ## Show project information
	@echo "$(BLUE)Project Information$(NC)"
	@echo "Python version: $$(python3 --version)"
	@echo "Pip version: $$(pip3 --version | head -n1)"
	@echo "Pytest version: $$(pytest --version 2>/dev/null || echo 'Not installed')"
	@echo "Pre-commit version: $$(pre-commit --version 2>/dev/null || echo 'Not installed')"
	@echo ""
	@echo "$(BLUE)Test Statistics$(NC)"
	@find tests -name 'test_*.py' | wc -l | awk '{print "Test files: " $$1}'
	@echo ""
	@echo "$(BLUE)Project Structure$(NC)"
	@tree -L 2 -I '__pycache__|*.pyc|.pytest_cache' spider/ 2>/dev/null || ls -R spider/

# Stats
stats: ## Show code statistics
	@echo "$(BLUE)Code Statistics$(NC)"
	@echo "Lines of code:"
	@find spider -name '*.py' -exec wc -l {} + | tail -n1
	@echo ""
	@echo "Test lines:"
	@find tests -name '*.py' -exec wc -l {} + | tail -n1
	@echo ""
	@echo "Test coverage:"
	@coverage report --skip-empty 2>/dev/null || echo "Run 'make coverage' first"
