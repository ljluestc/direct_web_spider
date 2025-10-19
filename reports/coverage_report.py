#!/usr/bin/env python3
"""
Automated Coverage Reporting System
Generates comprehensive coverage reports for all systems
"""

import os
import sys
import json
import subprocess
import datetime
from pathlib import Path
from typing import Dict, List, Any
import argparse


class CoverageReporter:
    """Comprehensive coverage reporting system"""
    
    def __init__(self, project_root: str = "."):
        self.project_root = Path(project_root)
        self.reports_dir = self.project_root / "reports"
        self.reports_dir.mkdir(exist_ok=True)
        self.timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        
    def generate_python_coverage_report(self) -> Dict[str, Any]:
        """Generate Python backend coverage report"""
        print("🔍 Generating Python Backend Coverage Report...")
        
        try:
            # Run pytest with coverage
            result = subprocess.run([
                "python3", "-m", "pytest", 
                "tests/", 
                "--cov=spider", 
                "--cov=scripts",
                "--cov-report=json:reports/python_coverage.json",
                "--cov-report=html:reports/python_html",
                "--cov-report=term-missing",
                "--tb=no", "-q"
            ], capture_output=True, text=True, cwd=self.project_root)
            
            # Parse coverage data
            coverage_file = self.reports_dir / "python_coverage.json"
            if coverage_file.exists():
                with open(coverage_file) as f:
                    coverage_data = json.load(f)
                
                total_coverage = coverage_data.get('totals', {}).get('percent_covered', 0)
                
                return {
                    "system": "Python Backend",
                    "coverage_percentage": round(total_coverage, 2),
                    "status": "✅ PASS" if total_coverage >= 80 else "❌ FAIL",
                    "files_covered": len(coverage_data.get('files', {})),
                    "lines_covered": coverage_data.get('totals', {}).get('covered_lines', 0),
                    "lines_total": coverage_data.get('totals', {}).get('num_statements', 0),
                    "timestamp": self.timestamp
                }
            else:
                return {
                    "system": "Python Backend",
                    "coverage_percentage": 0,
                    "status": "❌ NO DATA",
                    "error": "Coverage file not found"
                }
                
        except Exception as e:
            return {
                "system": "Python Backend",
                "coverage_percentage": 0,
                "status": "❌ ERROR",
                "error": str(e)
            }
    
    def generate_go_coverage_report(self) -> Dict[str, Any]:
        """Generate Go backend coverage report"""
        print("🔍 Generating Go Backend Coverage Report...")
        
        try:
            # Check if Go files exist
            go_files = list(self.project_root.glob("**/*.go"))
            if not go_files:
                return {
                    "system": "Go Backend",
                    "coverage_percentage": 0,
                    "status": "⚠️ NO GO FILES",
                    "message": "No Go source files found"
                }
            
            # Run Go tests with coverage
            result = subprocess.run([
                "go", "test", "-coverprofile=reports/go_coverage.out", 
                "-covermode=count", "./..."
            ], capture_output=True, text=True, cwd=self.project_root)
            
            if result.returncode == 0:
                # Parse coverage output
                coverage_result = subprocess.run([
                    "go", "tool", "cover", "-func=reports/go_coverage.out"
                ], capture_output=True, text=True, cwd=self.project_root)
                
                # Extract total coverage percentage
                lines = coverage_result.stdout.split('\n')
                total_line = [line for line in lines if 'total:' in line]
                
                if total_line:
                    coverage_pct = float(total_line[0].split()[-1].replace('%', ''))
                    return {
                        "system": "Go Backend",
                        "coverage_percentage": round(coverage_pct, 2),
                        "status": "✅ PASS" if coverage_pct >= 80 else "❌ FAIL",
                        "timestamp": self.timestamp
                    }
            
            return {
                "system": "Go Backend",
                "coverage_percentage": 0,
                "status": "❌ NO TESTS",
                "message": "No Go tests found or tests failed"
            }
            
        except Exception as e:
            return {
                "system": "Go Backend",
                "coverage_percentage": 0,
                "status": "❌ ERROR",
                "error": str(e)
            }
    
    def generate_react_coverage_report(self) -> Dict[str, Any]:
        """Generate React frontend coverage report"""
        print("🔍 Generating React Frontend Coverage Report...")
        
        try:
            # Check if React project exists
            package_json = self.project_root / "package.json"
            if not package_json.exists():
                return {
                    "system": "React Frontend",
                    "coverage_percentage": 0,
                    "status": "⚠️ NO REACT PROJECT",
                    "message": "No package.json found"
                }
            
            # Check if Jest is configured
            with open(package_json) as f:
                package_data = json.load(f)
            
            if "jest" not in package_data and "scripts" not in package_data:
                return {
                    "system": "React Frontend",
                    "coverage_percentage": 0,
                    "status": "⚠️ NO JEST CONFIG",
                    "message": "Jest not configured"
                }
            
            # Run Jest with coverage
            result = subprocess.run([
                "npm", "test", "--", "--coverage", "--watchAll=false"
            ], capture_output=True, text=True, cwd=self.project_root)
            
            # Parse Jest coverage output
            if "All files" in result.stdout:
                lines = result.stdout.split('\n')
                coverage_line = [line for line in lines if 'All files' in line]
                if coverage_line:
                    parts = coverage_line[0].split()
                    coverage_pct = float(parts[-1].replace('%', ''))
                    return {
                        "system": "React Frontend",
                        "coverage_percentage": round(coverage_pct, 2),
                        "status": "✅ PASS" if coverage_pct >= 80 else "❌ FAIL",
                        "timestamp": self.timestamp
                    }
            
            return {
                "system": "React Frontend",
                "coverage_percentage": 0,
                "status": "❌ NO COVERAGE DATA",
                "message": "Could not parse coverage data"
            }
            
        except Exception as e:
            return {
                "system": "React Frontend",
                "coverage_percentage": 0,
                "status": "❌ ERROR",
                "error": str(e)
            }
    
    def generate_comprehensive_report(self) -> Dict[str, Any]:
        """Generate comprehensive coverage report for all systems"""
        print("🚀 Generating Comprehensive Coverage Report...")
        
        reports = {
            "python": self.generate_python_coverage_report(),
            "go": self.generate_go_coverage_report(),
            "react": self.generate_react_coverage_report()
        }
        
        # Calculate overall metrics
        total_coverage = sum(r.get('coverage_percentage', 0) for r in reports.values())
        avg_coverage = total_coverage / len(reports) if reports else 0
        
        systems_passing = sum(1 for r in reports.values() if r.get('status', '').startswith('✅'))
        
        comprehensive_report = {
            "timestamp": self.timestamp,
            "overall_coverage": round(avg_coverage, 2),
            "systems_passing": systems_passing,
            "total_systems": len(reports),
            "status": "✅ ALL SYSTEMS PASS" if systems_passing == len(reports) else "⚠️ SOME SYSTEMS FAIL",
            "systems": reports,
            "summary": {
                "python_backend": reports['python'].get('coverage_percentage', 0),
                "go_backend": reports['go'].get('coverage_percentage', 0),
                "react_frontend": reports['react'].get('coverage_percentage', 0)
            }
        }
        
        return comprehensive_report
    
    def save_report(self, report: Dict[str, Any], filename: str = None):
        """Save report to JSON file"""
        if filename is None:
            filename = f"coverage_report_{self.timestamp}.json"
        
        report_path = self.reports_dir / filename
        with open(report_path, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"📊 Report saved to: {report_path}")
        return report_path
    
    def generate_html_report(self, report: Dict[str, Any]):
        """Generate HTML coverage report"""
        html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Coverage Report - {self.timestamp}</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        .header {{ background: #2c3e50; color: white; padding: 20px; border-radius: 5px; }}
        .summary {{ background: #ecf0f1; padding: 15px; margin: 10px 0; border-radius: 5px; }}
        .system {{ margin: 10px 0; padding: 15px; border: 1px solid #bdc3c7; border-radius: 5px; }}
        .pass {{ background: #d5f4e6; border-color: #27ae60; }}
        .fail {{ background: #fadbd8; border-color: #e74c3c; }}
        .warning {{ background: #fef9e7; border-color: #f39c12; }}
        .coverage-bar {{ background: #ecf0f1; height: 20px; border-radius: 10px; overflow: hidden; }}
        .coverage-fill {{ height: 100%; background: linear-gradient(90deg, #e74c3c 0%, #f39c12 50%, #27ae60 100%); }}
        .metric {{ display: inline-block; margin: 5px 10px; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>🚀 Comprehensive Coverage Report</h1>
        <p>Generated: {report['timestamp']}</p>
    </div>
    
    <div class="summary">
        <h2>📊 Overall Summary</h2>
        <div class="metric"><strong>Overall Coverage:</strong> {report['overall_coverage']}%</div>
        <div class="metric"><strong>Systems Passing:</strong> {report['systems_passing']}/{report['total_systems']}</div>
        <div class="metric"><strong>Status:</strong> {report['status']}</div>
        
        <div class="coverage-bar">
            <div class="coverage-fill" style="width: {report['overall_coverage']}%"></div>
        </div>
    </div>
    
    <h2>🔍 System Details</h2>
"""
        
        for system_name, system_report in report['systems'].items():
            status_class = "pass" if system_report.get('status', '').startswith('✅') else "fail" if system_report.get('status', '').startswith('❌') else "warning"
            
            html_content += f"""
    <div class="system {status_class}">
        <h3>{system_report.get('system', system_name.title())}</h3>
        <div class="metric"><strong>Coverage:</strong> {system_report.get('coverage_percentage', 0)}%</div>
        <div class="metric"><strong>Status:</strong> {system_report.get('status', 'Unknown')}</div>
"""
            
            if 'files_covered' in system_report:
                html_content += f'        <div class="metric"><strong>Files Covered:</strong> {system_report["files_covered"]}</div>'
            if 'lines_covered' in system_report:
                html_content += f'        <div class="metric"><strong>Lines Covered:</strong> {system_report["lines_covered"]}/{system_report.get("lines_total", 0)}</div>'
            if 'error' in system_report:
                html_content += f'        <div class="metric"><strong>Error:</strong> {system_report["error"]}</div>'
            if 'message' in system_report:
                html_content += f'        <div class="metric"><strong>Message:</strong> {system_report["message"]}</div>'
            
            html_content += "    </div>"
        
        html_content += """
</body>
</html>
"""
        
        html_path = self.reports_dir / f"coverage_report_{self.timestamp}.html"
        with open(html_path, 'w') as f:
            f.write(html_content)
        
        print(f"🌐 HTML report saved to: {html_path}")
        return html_path


def main():
    parser = argparse.ArgumentParser(description="Generate comprehensive coverage reports")
    parser.add_argument("--project-root", default=".", help="Project root directory")
    parser.add_argument("--output", help="Output filename for JSON report")
    parser.add_argument("--html", action="store_true", help="Generate HTML report")
    
    args = parser.parse_args()
    
    reporter = CoverageReporter(args.project_root)
    
    print("🚀 Starting Comprehensive Coverage Report Generation...")
    print("=" * 60)
    
    # Generate comprehensive report
    report = reporter.generate_comprehensive_report()
    
    # Save JSON report
    json_path = reporter.save_report(report, args.output)
    
    # Generate HTML report if requested
    if args.html:
        html_path = reporter.generate_html_report(report)
    
    # Print summary
    print("\n" + "=" * 60)
    print("📊 COVERAGE REPORT SUMMARY")
    print("=" * 60)
    print(f"Overall Coverage: {report['overall_coverage']}%")
    print(f"Systems Passing: {report['systems_passing']}/{report['total_systems']}")
    print(f"Status: {report['status']}")
    print("\nSystem Details:")
    for system_name, system_report in report['systems'].items():
        print(f"  {system_report.get('system', system_name.title())}: {system_report.get('coverage_percentage', 0)}% - {system_report.get('status', 'Unknown')}")
    
    print(f"\n📁 Reports saved to: {reporter.reports_dir}")
    if args.html:
        print(f"🌐 View HTML report: {html_path}")
    
    return 0 if report['systems_passing'] == report['total_systems'] else 1


if __name__ == "__main__":
    sys.exit(main())
