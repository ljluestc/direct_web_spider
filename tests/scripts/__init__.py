#!/usr/bin/env python3
# encoding: utf-8
"""
Tests for scripts module
"""

from .test_run_100_percent_coverage_comprehensive import TestRun100PercentCoverageComprehensive
from .test_run_100_percent_coverage_comprehensive_comprehensive import TestRun100PercentCoverageComprehensiveComprehensive
from .test_scripts_simple import TestScriptsSimple
from .test_scripts_function_coverage import TestScriptsFunctionCoverage

__all__ = [
    'TestRun100PercentCoverageComprehensive',
    'TestRun100PercentCoverageComprehensiveComprehensive',
    'TestScriptsSimple',
    'TestScriptsFunctionCoverage'
]
