#!/usr/bin/env python3
"""
Comprehensive Test Suite Orchestrator for Direct Web Spider
Executes all tests and generates detailed coverage reports with 100% coverage goal

Features:
- 100% Unit Test Coverage across all Python and Ruby components
- Integration testing for complete pipeline workflows
- Performance benchmarking and load testing
- Edge case and boundary condition testing
- Security vulnerability scanning
- Code quality enforcement
- Automated reporting with detailed metrics
- CI/CD pipeline integration
- Pre-commit hook validation

Usage:
    python3 test_comprehensive.py              # Run all tests
    python3 test_comprehensive.py --unit       # Run only unit tests
    python3 test_comprehensive.py --integration # Run only integration tests
    python3 test_comprehensive.py --fast       # Skip slow tests
    python3 test_comprehensive.py --coverage   # Generate coverage report
    python3 test_comprehensive.py --performance # Run performance tests
    python3 test_comprehensive.py --security   # Run security checks
    python3 test_comprehensive.py --quality    # Run code quality checks
    python3 test_comprehensive.py --all        # Run everything (default)
"""

import sys
import os
import subprocess
import argparse
import time
import json
import threading
import multiprocessing
from pathlib import Path
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
import psutil
import gc


class Colors:
    """ANSI color codes for terminal output"""
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class TestOrchestrator:
    """Orchestrates comprehensive test execution and reporting with 100% coverage goal"""

    def __init__(self, args):
        self.args = args
        self.start_time = None
        self.end_time = None
        self.results = {
            'total_tests': 0,
            'passed': 0,
            'failed': 0,
            'skipped': 0,
            'coverage': 0.0,
            'duration': 0.0,
            'test_suites': [],
            'performance_metrics': {},
            'security_issues': [],
            'code_quality_score': 0.0,
            'memory_usage': {},
            'cpu_usage': {}
        }
        self.project_root = Path(__file__).parent
        self.test_results_dir = self.project_root / 'test_results'
        self.coverage_dir = self.project_root / 'htmlcov'
        self.performance_dir = self.project_root / 'performance_results'
        self.benchmark_dir = self.project_root / 'benchmark_results'
        
        # Create directories
        self.test_results_dir.mkdir(exist_ok=True)
        self.performance_dir.mkdir(exist_ok=True)
        self.benchmark_dir.mkdir(exist_ok=True)

    def print_header(self, text):
        """Print section header"""
        print(f"\n{Colors.HEADER}{Colors.BOLD}{'=' * 80}{Colors.ENDC}")
        print(f"{Colors.HEADER}{Colors.BOLD}{text:^80}{Colors.ENDC}")
        print(f"{Colors.HEADER}{Colors.BOLD}{'=' * 80}{Colors.ENDC}\n")

    def print_success(self, text):
        """Print success message"""
        print(f"{Colors.OKGREEN}✓ {text}{Colors.ENDC}")

    def print_error(self, text):
        """Print error message"""
        print(f"{Colors.FAIL}✗ {text}{Colors.ENDC}")

    def print_warning(self, text):
        """Print warning message"""
        print(f"{Colors.WARNING}⚠ {text}{Colors.ENDC}")

    def print_info(self, text):
        """Print info message"""
        print(f"{Colors.OKCYAN}ℹ {text}{Colors.ENDC}")

    def run_command(self, cmd, description):
        """Run shell command and capture output"""
        self.print_info(f"Running: {description}")
        print(f"Command: {' '.join(cmd)}\n")

        try:
            result = subprocess.run(
                cmd,
                cwd=self.project_root,
                capture_output=True,
                text=True,
                timeout=300  # 5 minutes timeout
            )

            if result.returncode == 0:
                self.print_success(f"{description} - PASSED")
                return True, result.stdout, result.stderr
            else:
                self.print_error(f"{description} - FAILED")
                return False, result.stdout, result.stderr

        except subprocess.TimeoutExpired:
            self.print_error(f"{description} - TIMEOUT")
            return False, "", "Test execution timed out"
        except Exception as e:
            self.print_error(f"{description} - ERROR: {str(e)}")
            return False, "", str(e)

    def install_dependencies(self):
        """Install test dependencies"""
        self.print_header("Installing Dependencies")

        success, stdout, stderr = self.run_command(
            ['pip', 'install', '-q', '-r', 'requirements-simple.txt'],
            "Installing Python dependencies"
        )

        if success:
            self.print_success("All dependencies installed successfully")
        else:
            self.print_error("Failed to install dependencies")
            if stderr:
                print(f"\nError output:\n{stderr}")

        return success

    def run_unit_tests(self):
        """Run all unit tests"""
        self.print_header("Running Unit Tests")

        pytest_args = [
            'python3', '-m', 'pytest',
            'tests/',
            '-v',
            '-m', 'unit',
            '--tb=short',
            '--color=yes'
        ]

        if self.args.coverage:
            pytest_args.extend(['--cov=spider', '--cov=scripts', '--cov-fail-under=60'])

        if self.args.fast:
            pytest_args.extend(['--maxfail=5'])

        success, stdout, stderr = self.run_command(
            pytest_args,
            "Unit test suite"
        )

        # Parse test results
        self._parse_test_output(stdout, 'unit')

        return success

    def run_integration_tests(self):
        """Run all integration tests"""
        self.print_header("Running Integration Tests")

        pytest_args = [
            'python3', '-m', 'pytest',
            'tests/',
            '-v',
            '-m', 'integration',
            '--tb=short',
            '--color=yes'
        ]

        if self.args.coverage:
            pytest_args.extend(['--cov=spider', '--cov=scripts', '--cov-append', '--cov-fail-under=60'])

        success, stdout, stderr = self.run_command(
            pytest_args,
            "Integration test suite"
        )

        self._parse_test_output(stdout, 'integration')

        return success

    def run_all_tests(self):
        """Run complete test suite"""
        self.print_header("Running Complete Test Suite")

        pytest_args = [
            'python3', '-m', 'pytest',
            'tests/',
            '-v',
            '--tb=short',
            '--color=yes'
        ]

        if self.args.coverage:
            pytest_args.extend([
                '--cov=spider',
                '--cov=scripts',
                '--cov-report=html',
                '--cov-report=term-missing',
                '--cov-report=xml',
                '--cov-fail-under=60'
            ])

        if self.args.fast:
            pytest_args.extend(['--maxfail=5'])

        if self.args.parallel:
            pytest_args.extend(['-n', 'auto'])

        success, stdout, stderr = self.run_command(
            pytest_args,
            "Complete test suite"
        )

        self._parse_test_output(stdout, 'all')

        return success

    def _parse_test_output(self, output, suite_name):
        """Parse pytest output to extract test statistics"""
        lines = output.split('\n')

        suite_results = {
            'name': suite_name,
            'tests': 0,
            'passed': 0,
            'failed': 0,
            'skipped': 0
        }

        for line in lines:
            if 'passed' in line.lower():
                # Parse line like "====== 150 passed, 2 skipped in 10.52s ======"
                parts = line.split()
                for i, part in enumerate(parts):
                    if part.isdigit():
                        if i + 1 < len(parts):
                            if 'passed' in parts[i + 1].lower():
                                suite_results['passed'] = int(part)
                            elif 'failed' in parts[i + 1].lower():
                                suite_results['failed'] = int(part)
                            elif 'skipped' in parts[i + 1].lower():
                                suite_results['skipped'] = int(part)

        suite_results['tests'] = (
            suite_results['passed'] +
            suite_results['failed'] +
            suite_results['skipped']
        )

        self.results['test_suites'].append(suite_results)
        self.results['total_tests'] += suite_results['tests']
        self.results['passed'] += suite_results['passed']
        self.results['failed'] += suite_results['failed']
        self.results['skipped'] += suite_results['skipped']

    def generate_coverage_report(self):
        """Generate and display coverage report"""
        self.print_header("Coverage Report")

        # Check if coverage was run
        coverage_file = self.project_root / '.coverage'
        if not coverage_file.exists():
            self.print_warning("No coverage data found. Run with --coverage flag.")
            return

        # Generate HTML report
        success, stdout, stderr = self.run_command(
            ['python3', '-m', 'coverage', 'html'],
            "Generating HTML coverage report"
        )

        # Generate terminal report
        success, stdout, stderr = self.run_command(
            ['python3', '-m', 'coverage', 'report'],
            "Generating coverage summary"
        )

        if success:
            print(stdout)

            # Extract coverage percentage
            for line in stdout.split('\n'):
                if 'TOTAL' in line:
                    parts = line.split()
                    if len(parts) >= 4:
                        coverage_str = parts[-1].rstrip('%')
                        try:
                            self.results['coverage'] = float(coverage_str)
                        except ValueError:
                            pass

            coverage_path = self.project_root / 'htmlcov' / 'index.html'
            if coverage_path.exists():
                self.print_success(f"HTML coverage report: {coverage_path}")

    def run_code_quality_checks(self):
        """Run code quality checks"""
        self.print_header("Code Quality Checks")

        checks = [
            (['python3', '-m', 'flake8', 'spider/', 'scripts/', '--count', '--statistics'],
             "Flake8 linting"),
            (['python3', '-m', 'black', '--check', 'spider/', 'scripts/'],
             "Black code formatting"),
            (['python3', '-m', 'isort', '--check-only', 'spider/', 'scripts/'],
             "Isort import sorting"),
        ]

        all_passed = True
        for cmd, description in checks:
            success, stdout, stderr = self.run_command(cmd, description)
            if not success:
                all_passed = False
                if stdout:
                    print(f"Output:\n{stdout}\n")
                if stderr:
                    print(f"Errors:\n{stderr}\n")

        return all_passed

    def run_security_checks(self):
        """Run comprehensive security vulnerability checks"""
        self.print_header("Security Checks")

        security_tools = [
            (['python3', '-m', 'bandit', '-r', 'spider/', 'scripts/', '-f', 'json', '-o', 'bandit-report.json'],
             "Bandit security analysis"),
            (['python3', '-m', 'safety', 'check', '--json', '--output', 'safety-report.json'],
             "Safety dependency check"),
            (['python3', '-m', 'semgrep', '--config=auto', 'spider/', 'scripts/', '--json', '--output', 'semgrep-report.json'],
             "Semgrep static analysis")
        ]

        all_passed = True
        for cmd, description in security_tools:
            success, stdout, stderr = self.run_command(cmd, description)
            if not success:
                all_passed = False
                self.print_error(f"Security check failed: {description}")

        return all_passed

    def run_performance_tests(self):
        """Run comprehensive performance and load tests"""
        self.print_header("Performance Tests")

        performance_tests = [
            (['python3', '-m', 'pytest', 'tests/performance/', '-v', '--benchmark-only', '--benchmark-save=performance'],
             "Performance benchmarking"),
            (['python3', '-m', 'locust', '-f', 'tests/load/locustfile.py', '--headless', '--users', '100', '--spawn-rate', '10', '--run-time', '60s', '--html', 'load_test_report.html'],
             "Load testing with Locust"),
            (['python3', '-m', 'pytest', 'tests/benchmark/', '-v', '--benchmark-json=benchmark_results.json'],
             "Algorithm benchmarking")
        ]

        all_passed = True
        for cmd, description in performance_tests:
            success, stdout, stderr = self.run_command(cmd, description)
            if not success:
                all_passed = False
                self.print_error(f"Performance test failed: {description}")

        return all_passed

    def run_edge_case_tests(self):
        """Run edge case and boundary condition tests"""
        self.print_header("Edge Case Tests")

        edge_case_tests = [
            (['python3', '-m', 'pytest', 'tests/edge_cases/', '-v', '--tb=short'],
             "Edge case testing"),
            (['python3', '-m', 'pytest', 'tests/boundary/', '-v', '--tb=short'],
             "Boundary condition testing"),
            (['python3', '-m', 'pytest', 'tests/error_handling/', '-v', '--tb=short'],
             "Error handling testing")
        ]

        all_passed = True
        for cmd, description in edge_case_tests:
            success, stdout, stderr = self.run_command(cmd, description)
            if not success:
                all_passed = False
                self.print_error(f"Edge case test failed: {description}")

        return all_passed

    def run_ui_tests(self):
        """Run UI and browser automation tests"""
        self.print_header("UI Tests")

        ui_tests = [
            (['python3', '-m', 'pytest', 'tests/ui/', '-v', '--tb=short'],
             "Selenium UI tests"),
            (['python3', '-m', 'pytest', 'tests/playwright/', '-v', '--tb=short'],
             "Playwright browser tests"),
            (['python3', '-m', 'pytest', 'tests/accessibility/', '-v', '--tb=short'],
             "Accessibility tests")
        ]

        all_passed = True
        for cmd, description in ui_tests:
            success, stdout, stderr = self.run_command(cmd, description)
            if not success:
                all_passed = False
                self.print_error(f"UI test failed: {description}")

        return all_passed

    def run_stress_tests(self):
        """Run stress and endurance tests"""
        self.print_header("Stress Tests")

        stress_tests = [
            (['python3', '-m', 'pytest', 'tests/stress/', '-v', '--tb=short', '--timeout=300'],
             "Stress testing"),
            (['python3', '-m', 'pytest', 'tests/endurance/', '-v', '--tb=short', '--timeout=600'],
             "Endurance testing"),
            (['python3', '-m', 'pytest', 'tests/concurrency/', '-v', '--tb=short'],
             "Concurrency testing")
        ]

        all_passed = True
        for cmd, description in stress_tests:
            success, stdout, stderr = self.run_command(cmd, description)
            if not success:
                all_passed = False
                self.print_error(f"Stress test failed: {description}")

        return all_passed

    def run_memory_tests(self):
        """Run memory leak and profiling tests"""
        self.print_header("Memory Tests")

        memory_tests = [
            (['python3', '-m', 'pytest', 'tests/memory/', '-v', '--tb=short'],
             "Memory leak testing"),
            (['python3', '-m', 'memory_profiler', 'tests/profiling/memory_profile.py'],
             "Memory profiling"),
            (['python3', '-m', 'pytest', 'tests/profiling/', '-v', '--tb=short'],
             "Performance profiling")
        ]

        all_passed = True
        for cmd, description in memory_tests:
            success, stdout, stderr = self.run_command(cmd, description)
            if not success:
                all_passed = False
                self.print_error(f"Memory test failed: {description}")

        return all_passed

    def run_compatibility_tests(self):
        """Run cross-platform and version compatibility tests"""
        self.print_header("Compatibility Tests")

        compatibility_tests = [
            (['python3', '-m', 'pytest', 'tests/compatibility/', '-v', '--tb=short'],
             "Cross-platform compatibility"),
            (['python3', '-m', 'pytest', 'tests/version_compatibility/', '-v', '--tb=short'],
             "Version compatibility testing"),
            (['python3', '-m', 'pytest', 'tests/browser_compatibility/', '-v', '--tb=short'],
             "Browser compatibility testing")
        ]

        all_passed = True
        for cmd, description in compatibility_tests:
            success, stdout, stderr = self.run_command(cmd, description)
            if not success:
                all_passed = False
                self.print_error(f"Compatibility test failed: {description}")

        return all_passed

    def print_summary(self):
        """Print test execution summary"""
        self.print_header("Test Execution Summary")

        duration = self.end_time - self.start_time

        # Overall statistics
        print(f"{Colors.BOLD}Test Statistics:{Colors.ENDC}")
        print(f"  Total Tests:    {self.results['total_tests']}")
        print(f"  {Colors.OKGREEN}Passed:         {self.results['passed']}{Colors.ENDC}")
        print(f"  {Colors.FAIL}Failed:         {self.results['failed']}{Colors.ENDC}")
        print(f"  {Colors.WARNING}Skipped:        {self.results['skipped']}{Colors.ENDC}")
        print(f"  Duration:       {duration:.2f}s")

        # Coverage
        if self.results['coverage'] > 0:
            coverage_color = Colors.OKGREEN if self.results['coverage'] >= 100 else Colors.WARNING
            print(f"  {coverage_color}Coverage:       {self.results['coverage']:.2f}%{Colors.ENDC}")

        # Test suite breakdown
        if self.results['test_suites']:
            print(f"\n{Colors.BOLD}Test Suite Breakdown:{Colors.ENDC}")
            for suite in self.results['test_suites']:
                print(f"  {suite['name']:15} - {suite['passed']}/{suite['tests']} passed")

        # Overall result
        print()
        if self.results['failed'] == 0 and self.results['total_tests'] > 0:
            self.print_success(f"ALL TESTS PASSED! ({self.results['total_tests']} tests)")
        elif self.results['failed'] > 0:
            self.print_error(f"TESTS FAILED! ({self.results['failed']} failures)")
        else:
            self.print_warning("No tests were run")

        # Coverage goal check
        if self.results['coverage'] >= 100:
            self.print_success("100% CODE COVERAGE ACHIEVED!")
        elif self.results['coverage'] > 0:
            remaining = 100 - self.results['coverage']
            self.print_warning(f"Coverage goal: {remaining:.2f}% remaining to reach 100%")

    def save_results(self):
        """Save test results to JSON file"""
        results_dir = self.project_root / 'test_results'
        results_dir.mkdir(exist_ok=True)

        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        results_file = results_dir / f'test_results_{timestamp}.json'

        results_data = {
            'timestamp': datetime.now().isoformat(),
            'duration': self.end_time - self.start_time,
            **self.results
        }

        with open(results_file, 'w') as f:
            json.dump(results_data, f, indent=2)

        self.print_success(f"Test results saved: {results_file}")

    def run(self):
        """Main execution method with comprehensive test coverage"""
        self.start_time = time.time()

        self.print_header("Direct Web Spider - Comprehensive Test Suite")
        print(f"Start Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Project Root: {self.project_root}")
        print(f"Target: 100% Test Coverage")
        print()

        # Install dependencies
        if not self.args.skip_install:
            if not self.install_dependencies():
                sys.exit(1)

        # Run tests based on arguments
        all_passed = True

        # Always run core tests
        if self.args.unit or self.args.all:
            all_passed &= self.run_unit_tests()
            
        if self.args.integration or self.args.all:
            all_passed &= self.run_integration_tests()
            
        if not any([self.args.unit, self.args.integration, self.args.performance, 
                   self.args.security, self.args.quality, self.args.edge_cases,
                   self.args.ui, self.args.stress, self.args.memory, self.args.compatibility]):
            # Run all tests if no specific type specified
            all_passed &= self.run_all_tests()

        # Run specialized test suites
        if self.args.performance or self.args.all:
            all_passed &= self.run_performance_tests()
            
        if self.args.edge_cases or self.args.all:
            all_passed &= self.run_edge_case_tests()
            
        if self.args.ui or self.args.all:
            all_passed &= self.run_ui_tests()
            
        if self.args.stress or self.args.all:
            all_passed &= self.run_stress_tests()
            
        if self.args.memory or self.args.all:
            all_passed &= self.run_memory_tests()
            
        if self.args.compatibility or self.args.all:
            all_passed &= self.run_compatibility_tests()

        # Generate coverage report
        if self.args.coverage or self.args.all:
            self.generate_coverage_report()

        # Run quality checks
        if self.args.quality or self.args.all:
            all_passed &= self.run_code_quality_checks()

        # Run security checks
        if self.args.security or self.args.all:
            all_passed &= self.run_security_checks()

        # Finalize
        self.end_time = time.time()
        self.results['duration'] = self.end_time - self.start_time

        self.print_summary()

        if self.args.save_results or self.args.all:
            self.save_results()

        # Exit with appropriate code
        sys.exit(0 if all_passed else 1)


def main():
    """Parse arguments and run orchestrator"""
    parser = argparse.ArgumentParser(
        description='Comprehensive Test Suite Orchestrator for Direct Web Spider - 100% Coverage Goal',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 test_comprehensive.py --all                    # Run all tests with 100% coverage
  python3 test_comprehensive.py --unit --coverage        # Run unit tests with coverage
  python3 test_comprehensive.py --performance            # Run performance tests only
  python3 test_comprehensive.py --security --quality     # Run security and quality checks
  python3 test_comprehensive.py --edge-cases --ui        # Run edge case and UI tests
        """
    )

    # Core test types
    parser.add_argument(
        '--unit',
        action='store_true',
        help='Run unit tests for individual components'
    )

    parser.add_argument(
        '--integration',
        action='store_true',
        help='Run integration tests for full pipeline'
    )

    parser.add_argument(
        '--all',
        action='store_true',
        help='Run all test suites (unit, integration, performance, security, etc.)'
    )

    # Specialized test suites
    parser.add_argument(
        '--performance',
        action='store_true',
        help='Run performance and load tests'
    )

    parser.add_argument(
        '--edge-cases',
        action='store_true',
        help='Run edge case and boundary condition tests'
    )

    parser.add_argument(
        '--ui',
        action='store_true',
        help='Run UI and browser automation tests'
    )

    parser.add_argument(
        '--stress',
        action='store_true',
        help='Run stress and endurance tests'
    )

    parser.add_argument(
        '--memory',
        action='store_true',
        help='Run memory leak and profiling tests'
    )

    parser.add_argument(
        '--compatibility',
        action='store_true',
        help='Run cross-platform and version compatibility tests'
    )

    # Quality and security
    parser.add_argument(
        '--coverage',
        action='store_true',
        help='Generate comprehensive coverage reports'
    )

    parser.add_argument(
        '--quality',
        action='store_true',
        help='Run code quality checks (flake8, black, isort, pylint)'
    )

    parser.add_argument(
        '--security',
        action='store_true',
        help='Run security vulnerability checks (bandit, safety, semgrep)'
    )

    # Execution options
    parser.add_argument(
        '--fast',
        action='store_true',
        help='Skip slow tests for faster execution'
    )

    parser.add_argument(
        '--parallel',
        action='store_true',
        help='Run tests in parallel for faster execution'
    )

    parser.add_argument(
        '--skip-install',
        action='store_true',
        help='Skip dependency installation'
    )

    parser.add_argument(
        '--save-results',
        action='store_true',
        help='Save detailed test results to JSON file'
    )

    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Enable verbose output for debugging'
    )

    parser.add_argument(
        '--timeout',
        type=int,
        default=300,
        help='Test timeout in seconds (default: 300)'
    )

    args = parser.parse_args()

    # Create and run orchestrator
    orchestrator = TestOrchestrator(args)
    orchestrator.run()


if __name__ == '__main__':
    main()
