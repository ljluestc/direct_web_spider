# Testing Guide for Direct Web Spider

Comprehensive testing documentation for the Direct Web Spider project.

---

## Table of Contents

- [Overview](#overview)
- [Quick Start](#quick-start)
- [Test Structure](#test-structure)
- [Running Tests](#running-tests)
- [Coverage Requirements](#coverage-requirements)
- [Writing Tests](#writing-tests)
- [CI/CD Integration](#cicd-integration)
- [Troubleshooting](#troubleshooting)

---

## Overview

The Direct Web Spider project has a comprehensive test suite designed to achieve **100% code coverage** across all modules. The testing infrastructure includes:

- **Unit Tests**: Test individual components in isolation
- **Integration Tests**: Test complete workflows and pipelines
- **Coverage Tracking**: Monitor and enforce 100% test coverage
- **CI/CD Pipeline**: Automated testing on every commit
- **Pre-commit Hooks**: Run tests before commits

### Test Statistics

- **Total Test Files**: 50+
- **Coverage Goal**: 100%
- **Test Frameworks**: pytest, pytest-cov, pytest-asyncio
- **Test Categories**: Unit, Integration, Performance

---

## Quick Start

### 1. Install Dependencies

```bash
# Install test dependencies
pip install -r requirements.txt

# Or use make
make install
```

### 2. Run Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=spider --cov=scripts

# Or use make
make test
make coverage
```

### 3. View Coverage Report

```bash
# Generate HTML coverage report
pytest --cov=spider --cov=scripts --cov-report=html

# Open in browser
open htmlcov/index.html  # macOS
xdg-open htmlcov/index.html  # Linux
```

---

## Test Structure

```
tests/
├── __init__.py                 # Test package init
├── conftest.py                 # Shared fixtures and configuration
├── test_logger.py              # Logger module tests
├── test_encoding.py            # Encoding module tests
├── test_utils.py               # Utils module tests
├── test_optparse.py            # Command-line parsing tests
├── models/                     # Model tests (11 files)
│   ├── test_category.py
│   ├── test_page.py
│   ├── test_product.py
│   └── ...
├── base/                       # Base class tests (5 files)
│   ├── test_fetcher.py
│   ├── test_parser.py
│   └── ...
├── downloaders/                # Downloader tests (3 files)
│   ├── test_normal_downloader.py
│   ├── test_ty_downloader.py
│   └── test_em_downloader.py
├── fetchers/                   # Fetcher tests (6 files)
├── parsers/                    # Parser tests (6 files)
├── diggers/                    # Digger tests (6 files)
├── paginaters/                 # Paginater tests (6 files)
└── integration/                # Integration tests
    ├── test_pipeline.py
    └── test_scripts.py
```

---

## Running Tests

### Basic Commands

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run specific test file
pytest tests/test_logger.py

# Run specific test class
pytest tests/test_logger.py::TestLoggerMixin

# Run specific test method
pytest tests/test_logger.py::TestLoggerMixin::test_logger_mixin_initialization
```

### Test Categories

```bash
# Run only unit tests
pytest -m unit

# Run only integration tests
pytest -m integration

# Run only model tests
pytest -m model

# Run only downloader tests
pytest -m downloader
```

### Site-Specific Tests

```bash
# Test Dangdang site
pytest -m dangdang

# Test JingDong site
pytest -m jingdong

# Test all sites
pytest tests/fetchers/ tests/parsers/ tests/diggers/ tests/paginaters/
```

### Coverage Commands

```bash
# Run with coverage
pytest --cov=spider --cov=scripts

# Coverage with HTML report
pytest --cov=spider --cov=scripts --cov-report=html

# Coverage with missing lines
pytest --cov=spider --cov=scripts --cov-report=term-missing

# Enforce 100% coverage
pytest --cov=spider --cov=scripts --cov-fail-under=100
```

### Performance Testing

```bash
# Run tests in parallel (faster)
pytest -n auto

# Skip slow tests
pytest -m "not slow"

# Run benchmarks
pytest --benchmark-only
```

### Using Make Commands

```bash
# Run all tests
make test

# Run unit tests
make test-unit

# Run integration tests
make test-integration

# Run with coverage
make coverage

# Enforce 100% coverage
make coverage-100

# Run comprehensive test suite
make comprehensive

# Run fast tests (skip slow)
make test-fast

# Run tests in parallel
make test-parallel
```

### Using Test Orchestrator

```bash
# Run comprehensive test suite with full reports
python3 test_comprehensive.py --coverage

# Run with quality checks
python3 test_comprehensive.py --coverage --quality

# Run with security checks
python3 test_comprehensive.py --coverage --quality --security

# Save results to JSON
python3 test_comprehensive.py --coverage --save-results

# Run only unit tests
python3 test_comprehensive.py --unit

# Run only integration tests
python3 test_comprehensive.py --integration

# Skip slow tests
python3 test_comprehensive.py --fast

# Run tests in parallel
python3 test_comprehensive.py --parallel
```

---

## Coverage Requirements

### Goal: 100% Code Coverage

The project aims for **100% test coverage** across all modules:

- `spider/` - All spider modules
- `scripts/` - All script files

### Current Coverage

To check current coverage:

```bash
# Generate coverage report
pytest --cov=spider --cov=scripts --cov-report=term-missing

# View HTML report
open htmlcov/index.html
```

### Coverage Reports

Coverage reports are generated in multiple formats:

1. **Terminal**: Shows coverage summary with missing lines
2. **HTML**: Interactive HTML report in `htmlcov/`
3. **XML**: Machine-readable report for CI/CD

### Enforcing Coverage

```bash
# Fail if coverage is below 100%
pytest --cov=spider --cov=scripts --cov-fail-under=100
```

---

## Writing Tests

### Test File Naming

- Test files must start with `test_`
- Example: `test_logger.py`, `test_encoding.py`

### Test Class Naming

```python
@pytest.mark.unit
class TestLogger:
    """Test cases for Logger class"""
    pass
```

### Test Method Naming

```python
def test_logger_initialization(self):
    """Test that logger initializes correctly"""
    pass
```

### Using Fixtures

```python
def test_with_mock_category(self, mock_category):
    """Test using a mock category fixture"""
    assert mock_category.kind == "dangdang"
```

### Test Markers

```python
@pytest.mark.unit          # Unit test
@pytest.mark.integration   # Integration test
@pytest.mark.slow          # Slow test
@pytest.mark.dangdang      # Dangdang-specific test
```

### Example Unit Test

```python
"""
Unit tests for spider.logger module
"""
import pytest
from spider.logger import LoggerMixin, get_logger


@pytest.mark.unit
class TestLoggerMixin:
    """Test cases for LoggerMixin"""

    def test_logger_mixin_initialization(self):
        """Test LoggerMixin can be mixed into a class"""
        class TestClass(LoggerMixin):
            pass

        obj = TestClass()
        assert hasattr(obj, 'logger')

    def test_logger_file_generation(self, tmp_path):
        """Test logger file path generation"""
        # Test implementation
        pass
```

### Example Integration Test

```python
@pytest.mark.integration
class TestPipeline:
    """Integration tests for complete pipeline"""

    def test_full_pipeline_dangdang(self):
        """Test complete Dangdang pipeline"""
        # 1. Fetch categories
        # 2. Generate pagination
        # 3. Extract product URLs
        # 4. Parse products
        pass
```

---

## CI/CD Integration

### GitHub Actions

The project uses GitHub Actions for continuous integration:

- **Triggers**: Push to master/main/develop, Pull requests
- **Matrix Testing**: Python 3.8, 3.9, 3.10, 3.11 on Ubuntu and macOS
- **Checks**: Tests, Coverage, Linting, Security

### CI Pipeline Jobs

1. **Test Suite**: Run all tests with coverage
2. **Code Quality**: Linting, formatting, type checking
3. **Build**: Package building and validation
4. **Performance**: Benchmark tests
5. **Documentation**: Documentation generation

### Pre-commit Hooks

Install pre-commit hooks to run tests before commits:

```bash
# Install pre-commit
pip install pre-commit

# Install hooks
pre-commit install

# Run manually
pre-commit run --all-files
```

### Hooks Include

- Code formatting (black, isort)
- Linting (flake8)
- Type checking (mypy)
- Security scanning (bandit)
- Test execution (pytest)

---

## Troubleshooting

### Common Issues

#### 1. MongoDB Connection Errors

**Problem**: Tests fail with MongoDB connection errors

**Solution**:
```bash
# Use mongomock for testing (no real MongoDB needed)
# It's automatically configured in conftest.py
```

#### 2. Import Errors

**Problem**: `ModuleNotFoundError: No module named 'spider'`

**Solution**:
```bash
# Run tests from project root
cd /path/to/direct_web_spider
pytest

# Or add project to PYTHONPATH
export PYTHONPATH=/path/to/direct_web_spider:$PYTHONPATH
```

#### 3. Coverage Not 100%

**Problem**: Coverage report shows less than 100%

**Solution**:
```bash
# Check which lines are missing
pytest --cov=spider --cov=scripts --cov-report=term-missing

# View HTML report for details
open htmlcov/index.html

# Write tests for uncovered code
```

#### 4. Slow Tests

**Problem**: Tests take too long to run

**Solution**:
```bash
# Run tests in parallel
pytest -n auto

# Skip slow tests during development
pytest -m "not slow"

# Run only specific test category
pytest tests/test_logger.py
```

#### 5. Pre-commit Hook Failures

**Problem**: Pre-commit hooks fail

**Solution**:
```bash
# Update hooks
pre-commit autoupdate

# Run hooks manually to see errors
pre-commit run --all-files

# Skip hooks if needed (not recommended)
git commit --no-verify
```

### Getting Help

- Check test output for detailed error messages
- Review test logs in `log/` directory
- Check GitHub Actions logs for CI failures
- Review `conftest.py` for fixture definitions

### Best Practices

1. **Run tests frequently**: Test early and often during development
2. **Write tests first**: Follow TDD (Test-Driven Development) when possible
3. **Keep tests isolated**: Each test should be independent
4. **Use fixtures**: Share common setup code using pytest fixtures
5. **Mock external dependencies**: Use mocks for HTTP requests, databases, etc.
6. **Test edge cases**: Cover boundary conditions and error cases
7. **Maintain coverage**: Keep coverage at 100%
8. **Review coverage reports**: Regularly check HTML coverage reports

---

## Additional Resources

- **pytest Documentation**: https://docs.pytest.org/
- **pytest-cov Documentation**: https://pytest-cov.readthedocs.io/
- **Pre-commit Documentation**: https://pre-commit.com/
- **GitHub Actions Documentation**: https://docs.github.com/en/actions

---

**Happy Testing!** 🧪
