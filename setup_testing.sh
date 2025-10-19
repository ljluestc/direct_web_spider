#!/bin/bash
###############################################################################
# Testing Environment Setup Script for Direct Web Spider
# This script sets up a complete testing environment with all dependencies
###############################################################################

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Functions
print_header() {
    echo -e "\n${BLUE}================================${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}================================${NC}\n"
}

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ $1${NC}"
}

# Check if running in virtualenv
check_virtualenv() {
    if [[ -z "${VIRTUAL_ENV}" ]]; then
        print_warning "Not running in a virtual environment"
        print_info "Recommended: Create and activate a virtual environment first"
        echo ""
        echo "  python3 -m venv venv"
        echo "  source venv/bin/activate  # On Linux/macOS"
        echo "  venv\\Scripts\\activate     # On Windows"
        echo ""
        read -p "Continue anyway? (y/N) " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            exit 1
        fi
    else
        print_success "Running in virtual environment: ${VIRTUAL_ENV}"
    fi
}

# Check Python version
check_python() {
    print_header "Checking Python Version"

    if ! command -v python3 &> /dev/null; then
        print_error "Python 3 is not installed"
        exit 1
    fi

    PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
    print_success "Python $PYTHON_VERSION found"

    # Check if version is 3.8+
    MAJOR=$(echo $PYTHON_VERSION | cut -d'.' -f1)
    MINOR=$(echo $PYTHON_VERSION | cut -d'.' -f2)

    if [ "$MAJOR" -lt 3 ] || ([ "$MAJOR" -eq 3 ] && [ "$MINOR" -lt 8 ]); then
        print_error "Python 3.8+ is required (found $PYTHON_VERSION)"
        exit 1
    fi
}

# Install system dependencies
install_system_deps() {
    print_header "Installing System Dependencies"

    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        print_info "Detected Linux system"
        if command -v apt-get &> /dev/null; then
            print_info "Installing with apt-get..."
            sudo apt-get update -qq
            sudo apt-get install -y tesseract-ocr
            print_success "System dependencies installed"
        else
            print_warning "apt-get not found, skipping system dependencies"
        fi
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        print_info "Detected macOS system"
        if command -v brew &> /dev/null; then
            print_info "Installing with Homebrew..."
            brew install tesseract
            print_success "System dependencies installed"
        else
            print_warning "Homebrew not found, skipping system dependencies"
        fi
    else
        print_warning "Unknown OS, skipping system dependencies"
    fi
}

# Install Python dependencies
install_python_deps() {
    print_header "Installing Python Dependencies"

    print_info "Upgrading pip..."
    python3 -m pip install --upgrade pip setuptools wheel -q

    print_info "Installing project dependencies..."
    pip3 install -r requirements.txt -q

    print_success "Python dependencies installed"
}

# Install development tools
install_dev_tools() {
    print_header "Installing Development Tools"

    print_info "Installing pre-commit..."
    pip3 install pre-commit -q

    print_info "Installing git hooks..."
    pre-commit install

    print_success "Development tools installed"
}

# Create necessary directories
create_directories() {
    print_header "Creating Directories"

    mkdir -p log
    mkdir -p test_results
    mkdir -p htmlcov

    print_success "Directories created"
}

# Verify installation
verify_installation() {
    print_header "Verifying Installation"

    # Check pytest
    if python3 -m pytest --version &> /dev/null; then
        PYTEST_VERSION=$(python3 -m pytest --version | head -n1)
        print_success "pytest: $PYTEST_VERSION"
    else
        print_error "pytest not installed correctly"
        exit 1
    fi

    # Check coverage
    if python3 -m coverage --version &> /dev/null; then
        COVERAGE_VERSION=$(python3 -m coverage --version | head -n1)
        print_success "coverage: $COVERAGE_VERSION"
    else
        print_error "coverage not installed correctly"
        exit 1
    fi

    # Check pre-commit
    if pre-commit --version &> /dev/null; then
        PRECOMMIT_VERSION=$(pre-commit --version)
        print_success "pre-commit: $PRECOMMIT_VERSION"
    else
        print_warning "pre-commit not installed"
    fi

    # Count test files
    TEST_COUNT=$(find tests -name 'test_*.py' | wc -l | tr -d ' ')
    print_success "Test files found: $TEST_COUNT"
}

# Run initial tests
run_initial_tests() {
    print_header "Running Initial Test Suite"

    print_info "Running smoke tests..."

    if python3 -m pytest tests/test_logger.py -v --tb=short; then
        print_success "Smoke tests passed"
    else
        print_warning "Some smoke tests failed (this is normal for initial setup)"
    fi
}

# Print next steps
print_next_steps() {
    print_header "Setup Complete!"

    echo -e "${GREEN}Testing environment is ready!${NC}\n"

    echo "Next steps:"
    echo ""
    echo "  1. Run tests:"
    echo "     ${BLUE}pytest${NC}                          # Run all tests"
    echo "     ${BLUE}pytest --cov=spider --cov=scripts${NC}  # With coverage"
    echo "     ${BLUE}make test${NC}                      # Using Makefile"
    echo ""
    echo "  2. Generate coverage report:"
    echo "     ${BLUE}pytest --cov=spider --cov=scripts --cov-report=html${NC}"
    echo "     ${BLUE}make coverage${NC}"
    echo ""
    echo "  3. Run comprehensive test suite:"
    echo "     ${BLUE}python3 test_comprehensive.py --coverage${NC}"
    echo "     ${BLUE}make comprehensive${NC}"
    echo ""
    echo "  4. View coverage report:"
    echo "     ${BLUE}open htmlcov/index.html${NC}  # macOS"
    echo "     ${BLUE}xdg-open htmlcov/index.html${NC}  # Linux"
    echo ""
    echo "  5. Run pre-commit hooks:"
    echo "     ${BLUE}pre-commit run --all-files${NC}"
    echo ""
    echo "See ${BLUE}TESTING.md${NC} for comprehensive testing documentation"
    echo ""
}

# Main execution
main() {
    clear
    print_header "Direct Web Spider - Testing Setup"

    check_virtualenv
    check_python
    install_system_deps
    install_python_deps
    install_dev_tools
    create_directories
    verify_installation
    run_initial_tests
    print_next_steps
}

# Run main function
main
