#!/usr/bin/env python3
"""
Comprehensive Automated Reporting System
Generates HTML, JSON, and console reports for test coverage and metrics
"""

import os
import sys
import json
import subprocess
import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional
import argparse
import logging

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

class AutomatedReporter:
    """Comprehensive automated reporting system"""
    
    def __init__(self, project_root: str = None):
        self.project_root = Path(project_root) if project_root else Path(__file__).parent.parent
        self.reports_dir = self.project_root / "reports"
        self.reports_dir.mkdir(exist_ok=True)
        
        # Setup logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(self.reports_dir / "reporting.log"),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
        
        # Report data
        self.report_data = {
            "timestamp": datetime.datetime.now().isoformat(),
            "project": "Direct Web Spider",
            "components": {}
        }
    
    def run_python_tests(self) -> Dict[str, Any]:
        """Run Python tests and collect coverage data"""
        self.logger.info("Running Python tests...")
        
        try:
            # Run tests with coverage
            cmd = [
                "python3", "-m", "pytest",
                "tests/",
                "-v",
                "--cov=spider",
                "--cov=scripts", 
                "--cov-report=json:reports/python_coverage.json",
                "--cov-report=html:reports/html/python",
                "--cov-report=term-missing",
                "--tb=short",
                "-p", "no:postgresql"
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, cwd=self.project_root)
            
            # Parse test results
            test_results = self._parse_pytest_output(result.stdout, result.stderr)
            
            # Load coverage data
            coverage_file = self.reports_dir / "python_coverage.json"
            coverage_data = {}
            if coverage_file.exists():
                with open(coverage_file, 'r') as f:
                    coverage_data = json.load(f)
            
            return {
                "status": "success" if result.returncode == 0 else "failed",
                "return_code": result.returncode,
                "test_results": test_results,
                "coverage": coverage_data,
                "stdout": result.stdout,
                "stderr": result.stderr
            }
            
        except Exception as e:
            self.logger.error(f"Error running Python tests: {e}")
            return {
                "status": "error",
                "error": str(e),
                "test_results": {},
                "coverage": {}
            }
    
    def run_go_tests(self) -> Dict[str, Any]:
        """Run Go tests and collect coverage data"""
        self.logger.info("Running Go tests...")
        
        try:
            # Check if Go is available
            go_check = subprocess.run(["go", "version"], capture_output=True, text=True)
            if go_check.returncode != 0:
                return {
                    "status": "skipped",
                    "reason": "Go not available",
                    "test_results": {},
                    "coverage": {}
                }
            
            # Run Go tests with coverage
            cmd = [
                "go", "test",
                "-v",
                "-coverprofile=reports/go_coverage.out",
                "-covermode=atomic",
                "./..."
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, cwd=self.project_root)
            
            # Parse test results
            test_results = self._parse_go_test_output(result.stdout, result.stderr)
            
            # Generate coverage report
            coverage_data = self._generate_go_coverage_report()
            
            return {
                "status": "success" if result.returncode == 0 else "failed",
                "return_code": result.returncode,
                "test_results": test_results,
                "coverage": coverage_data,
                "stdout": result.stdout,
                "stderr": result.stderr
            }
            
        except Exception as e:
            self.logger.error(f"Error running Go tests: {e}")
            return {
                "status": "error",
                "error": str(e),
                "test_results": {},
                "coverage": {}
            }
    
    def run_react_tests(self) -> Dict[str, Any]:
        """Run React tests and collect coverage data"""
        self.logger.info("Running React tests...")
        
        try:
            # Check if frontend directory exists
            frontend_dir = self.project_root / "frontend"
            if not frontend_dir.exists():
                return {
                    "status": "skipped",
                    "reason": "Frontend directory not found",
                    "test_results": {},
                    "coverage": {}
                }
            
            # Check if package.json exists
            package_json = frontend_dir / "package.json"
            if not package_json.exists():
                return {
                    "status": "skipped",
                    "reason": "package.json not found",
                    "test_results": {},
                    "coverage": {}
                }
            
            # Run npm test with coverage
            cmd = [
                "npm", "test",
                "--",
                "--coverage",
                "--watchAll=false",
                "--coverageReporters=json",
                "--coverageReporters=html",
                "--coverageReporters=text"
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, cwd=frontend_dir)
            
            # Parse test results
            test_results = self._parse_jest_output(result.stdout, result.stderr)
            
            # Load coverage data
            coverage_file = frontend_dir / "coverage" / "coverage-final.json"
            coverage_data = {}
            if coverage_file.exists():
                with open(coverage_file, 'r') as f:
                    coverage_data = json.load(f)
            
            return {
                "status": "success" if result.returncode == 0 else "failed",
                "return_code": result.returncode,
                "test_results": test_results,
                "coverage": coverage_data,
                "stdout": result.stdout,
                "stderr": result.stderr
            }
            
        except Exception as e:
            self.logger.error(f"Error running React tests: {e}")
            return {
                "status": "error",
                "error": str(e),
                "test_results": {},
                "coverage": {}
            }
    
    def _parse_pytest_output(self, stdout: str, stderr: str) -> Dict[str, Any]:
        """Parse pytest output to extract test statistics"""
        lines = stdout.split('\n')
        
        # Find summary line
        summary_line = None
        for line in reversed(lines):
            if "failed" in line and "passed" in line and "warnings" in line:
                summary_line = line
                break
        
        if not summary_line:
            return {"total": 0, "passed": 0, "failed": 0, "skipped": 0, "warnings": 0}
        
        # Extract numbers using regex-like parsing
        import re
        numbers = re.findall(r'(\d+)', summary_line)
        
        if len(numbers) >= 4:
            return {
                "total": int(numbers[0]) + int(numbers[1]) + int(numbers[2]),
                "passed": int(numbers[0]),
                "failed": int(numbers[1]),
                "skipped": int(numbers[2]),
                "warnings": int(numbers[3]) if len(numbers) > 3 else 0
            }
        
        return {"total": 0, "passed": 0, "failed": 0, "skipped": 0, "warnings": 0}
    
    def _parse_go_test_output(self, stdout: str, stderr: str) -> Dict[str, Any]:
        """Parse Go test output to extract test statistics"""
        lines = stdout.split('\n')
        
        # Find summary line
        summary_line = None
        for line in reversed(lines):
            if "PASS" in line or "FAIL" in line:
                summary_line = line
                break
        
        if not summary_line:
            return {"total": 0, "passed": 0, "failed": 0}
        
        # Simple parsing for Go test output
        passed = stdout.count("PASS")
        failed = stdout.count("FAIL")
        
        return {
            "total": passed + failed,
            "passed": passed,
            "failed": failed,
            "skipped": 0,
            "warnings": 0
        }
    
    def _parse_jest_output(self, stdout: str, stderr: str) -> Dict[str, Any]:
        """Parse Jest output to extract test statistics"""
        lines = stdout.split('\n')
        
        # Find summary line
        summary_line = None
        for line in reversed(lines):
            if "Tests:" in line and "passed" in line:
                summary_line = line
                break
        
        if not summary_line:
            return {"total": 0, "passed": 0, "failed": 0, "skipped": 0, "warnings": 0}
        
        # Extract numbers
        import re
        numbers = re.findall(r'(\d+)', summary_line)
        
        if len(numbers) >= 3:
            return {
                "total": int(numbers[0]),
                "passed": int(numbers[1]),
                "failed": int(numbers[2]),
                "skipped": int(numbers[3]) if len(numbers) > 3 else 0,
                "warnings": 0
            }
        
        return {"total": 0, "passed": 0, "failed": 0, "skipped": 0, "warnings": 0}
    
    def _generate_go_coverage_report(self) -> Dict[str, Any]:
        """Generate Go coverage report"""
        coverage_file = self.reports_dir / "go_coverage.out"
        if not coverage_file.exists():
            return {}
        
        try:
            # Run go tool cover to get coverage percentage
            cmd = ["go", "tool", "cover", "-func=reports/go_coverage.out"]
            result = subprocess.run(cmd, capture_output=True, text=True, cwd=self.project_root)
            
            if result.returncode == 0:
                lines = result.stdout.split('\n')
                total_line = [line for line in lines if "total:" in line]
                if total_line:
                    # Extract coverage percentage
                    import re
                    match = re.search(r'(\d+\.\d+)%', total_line[0])
                    if match:
                        return {
                            "total_coverage": float(match.group(1)),
                            "raw_output": result.stdout
                        }
            
            return {"raw_output": result.stdout}
            
        except Exception as e:
            self.logger.error(f"Error generating Go coverage report: {e}")
            return {}
    
    def generate_html_report(self) -> str:
        """Generate comprehensive HTML report"""
        html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Test Coverage Report - {self.report_data['project']}</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #f5f5f5;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            overflow: hidden;
        }}
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }}
        .header h1 {{
            margin: 0;
            font-size: 2.5em;
        }}
        .header p {{
            margin: 10px 0 0 0;
            opacity: 0.9;
        }}
        .summary {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            padding: 30px;
        }}
        .summary-card {{
            background: #f8f9fa;
            border-radius: 8px;
            padding: 20px;
            text-align: center;
            border-left: 4px solid #007bff;
        }}
        .summary-card h3 {{
            margin: 0 0 10px 0;
            color: #333;
        }}
        .summary-card .number {{
            font-size: 2em;
            font-weight: bold;
            color: #007bff;
        }}
        .component {{
            margin: 30px;
            border: 1px solid #e0e0e0;
            border-radius: 8px;
            overflow: hidden;
        }}
        .component-header {{
            background: #f8f9fa;
            padding: 20px;
            border-bottom: 1px solid #e0e0e0;
        }}
        .component-header h2 {{
            margin: 0;
            color: #333;
        }}
        .component-content {{
            padding: 20px;
        }}
        .status {{
            display: inline-block;
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 0.9em;
            font-weight: bold;
        }}
        .status.success {{
            background: #d4edda;
            color: #155724;
        }}
        .status.failed {{
            background: #f8d7da;
            color: #721c24;
        }}
        .status.error {{
            background: #f5c6cb;
            color: #721c24;
        }}
        .status.skipped {{
            background: #fff3cd;
            color: #856404;
        }}
        .coverage-bar {{
            width: 100%;
            height: 20px;
            background: #e0e0e0;
            border-radius: 10px;
            overflow: hidden;
            margin: 10px 0;
        }}
        .coverage-fill {{
            height: 100%;
            background: linear-gradient(90deg, #28a745, #20c997);
            transition: width 0.3s ease;
        }}
        .coverage-fill.low {{
            background: linear-gradient(90deg, #dc3545, #fd7e14);
        }}
        .coverage-fill.medium {{
            background: linear-gradient(90deg, #ffc107, #fd7e14);
        }}
        .test-results {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 15px;
            margin: 20px 0;
        }}
        .test-stat {{
            text-align: center;
            padding: 15px;
            background: #f8f9fa;
            border-radius: 6px;
        }}
        .test-stat .number {{
            font-size: 1.5em;
            font-weight: bold;
            color: #333;
        }}
        .test-stat .label {{
            color: #666;
            font-size: 0.9em;
        }}
        .footer {{
            background: #f8f9fa;
            padding: 20px;
            text-align: center;
            color: #666;
            border-top: 1px solid #e0e0e0;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Test Coverage Report</h1>
            <p>{self.report_data['project']} - Generated on {self.report_data['timestamp']}</p>
        </div>
        
        <div class="summary">
            <div class="summary-card">
                <h3>Python Backend</h3>
                <div class="number">{self._get_python_coverage()}%</div>
                <div class="coverage-bar">
                    <div class="coverage-fill {self._get_coverage_class('python')}" 
                         style="width: {self._get_python_coverage()}%"></div>
                </div>
            </div>
            <div class="summary-card">
                <h3>Go Backend</h3>
                <div class="number">{self._get_go_coverage()}%</div>
                <div class="coverage-bar">
                    <div class="coverage-fill {self._get_coverage_class('go')}" 
                         style="width: {self._get_go_coverage()}%"></div>
                </div>
            </div>
            <div class="summary-card">
                <h3>React Frontend</h3>
                <div class="number">{self._get_react_coverage()}%</div>
                <div class="coverage-bar">
                    <div class="coverage-fill {self._get_coverage_class('react')}" 
                         style="width: {self._get_react_coverage()}%"></div>
                </div>
            </div>
        </div>
        
        {self._generate_component_sections()}
        
        <div class="footer">
            <p>Generated by Automated Reporting System</p>
        </div>
    </div>
</body>
</html>
        """
        
        # Save HTML report
        html_file = self.reports_dir / "index.html"
        with open(html_file, 'w') as f:
            f.write(html_content)
        
        return str(html_file)
    
    def _get_python_coverage(self) -> float:
        """Get Python coverage percentage"""
        python_data = self.report_data.get("components", {}).get("python", {})
        coverage = python_data.get("coverage", {})
        return coverage.get("totals", {}).get("percent_covered", 0.0)
    
    def _get_go_coverage(self) -> float:
        """Get Go coverage percentage"""
        go_data = self.report_data.get("components", {}).get("go", {})
        coverage = go_data.get("coverage", {})
        return coverage.get("total_coverage", 0.0)
    
    def _get_react_coverage(self) -> float:
        """Get React coverage percentage"""
        react_data = self.report_data.get("components", {}).get("react", {})
        coverage = react_data.get("coverage", {})
        # Jest coverage format
        if "total" in coverage:
            return coverage["total"].get("lines", {}).get("pct", 0.0)
        return 0.0
    
    def _get_coverage_class(self, component: str) -> str:
        """Get CSS class for coverage bar"""
        coverage = 0.0
        if component == "python":
            coverage = self._get_python_coverage()
        elif component == "go":
            coverage = self._get_go_coverage()
        elif component == "react":
            coverage = self._get_react_coverage()
        
        if coverage >= 80:
            return ""
        elif coverage >= 60:
            return "medium"
        else:
            return "low"
    
    def _generate_component_sections(self) -> str:
        """Generate HTML sections for each component"""
        sections = []
        
        for component, data in self.report_data.get("components", {}).items():
            status_class = data.get("status", "unknown")
            test_results = data.get("test_results", {})
            
            sections.append(f"""
            <div class="component">
                <div class="component-header">
                    <h2>{component.title()} Backend</h2>
                    <span class="status {status_class}">{status_class.upper()}</span>
                </div>
                <div class="component-content">
                    <div class="test-results">
                        <div class="test-stat">
                            <div class="number">{test_results.get('total', 0)}</div>
                            <div class="label">Total Tests</div>
                        </div>
                        <div class="test-stat">
                            <div class="number">{test_results.get('passed', 0)}</div>
                            <div class="label">Passed</div>
                        </div>
                        <div class="test-stat">
                            <div class="number">{test_results.get('failed', 0)}</div>
                            <div class="label">Failed</div>
                        </div>
                        <div class="test-stat">
                            <div class="number">{test_results.get('skipped', 0)}</div>
                            <div class="label">Skipped</div>
                        </div>
                    </div>
                </div>
            </div>
            """)
        
        return "".join(sections)
    
    def generate_json_report(self) -> str:
        """Generate JSON report"""
        json_file = self.reports_dir / "report.json"
        with open(json_file, 'w') as f:
            json.dump(self.report_data, f, indent=2)
        return str(json_file)
    
    def generate_console_report(self) -> None:
        """Generate console report"""
        print("\n" + "="*80)
        print(f"TEST COVERAGE REPORT - {self.report_data['project'].upper()}")
        print("="*80)
        print(f"Generated: {self.report_data['timestamp']}")
        print()
        
        for component, data in self.report_data.get("components", {}).items():
            status = data.get("status", "unknown")
            test_results = data.get("test_results", {})
            coverage = data.get("coverage", {})
            
            print(f"{component.upper()} BACKEND:")
            print(f"  Status: {status.upper()}")
            print(f"  Tests: {test_results.get('total', 0)} total, {test_results.get('passed', 0)} passed, {test_results.get('failed', 0)} failed")
            
            if component == "python":
                coverage_pct = coverage.get("totals", {}).get("percent_covered", 0.0)
                print(f"  Coverage: {coverage_pct:.1f}%")
            elif component == "go":
                coverage_pct = coverage.get("total_coverage", 0.0)
                print(f"  Coverage: {coverage_pct:.1f}%")
            elif component == "react":
                coverage_pct = coverage.get("total", {}).get("lines", {}).get("pct", 0.0)
                print(f"  Coverage: {coverage_pct:.1f}%")
            
            print()
        
        print("="*80)
    
    def run_all_tests(self) -> None:
        """Run all tests and generate reports"""
        self.logger.info("Starting comprehensive test run...")
        
        # Run Python tests
        self.logger.info("Running Python tests...")
        self.report_data["components"]["python"] = self.run_python_tests()
        
        # Run Go tests
        self.logger.info("Running Go tests...")
        self.report_data["components"]["go"] = self.run_go_tests()
        
        # Run React tests
        self.logger.info("Running React tests...")
        self.report_data["components"]["react"] = self.run_react_tests()
        
        # Generate reports
        self.logger.info("Generating reports...")
        
        # JSON report
        json_file = self.generate_json_report()
        self.logger.info(f"JSON report generated: {json_file}")
        
        # HTML report
        html_file = self.generate_html_report()
        self.logger.info(f"HTML report generated: {html_file}")
        
        # Console report
        self.generate_console_report()
        
        self.logger.info("Automated reporting completed!")

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description="Automated Test Reporting System")
    parser.add_argument("--project-root", help="Project root directory")
    parser.add_argument("--python-only", action="store_true", help="Run only Python tests")
    parser.add_argument("--go-only", action="store_true", help="Run only Go tests")
    parser.add_argument("--react-only", action="store_true", help="Run only React tests")
    
    args = parser.parse_args()
    
    reporter = AutomatedReporter(args.project_root)
    
    if args.python_only:
        reporter.report_data["components"]["python"] = reporter.run_python_tests()
    elif args.go_only:
        reporter.report_data["components"]["go"] = reporter.run_go_tests()
    elif args.react_only:
        reporter.report_data["components"]["react"] = reporter.run_react_tests()
    else:
        reporter.run_all_tests()

if __name__ == "__main__":
    main()
