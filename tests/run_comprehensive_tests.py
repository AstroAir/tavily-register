#!/usr/bin/env python3
"""
Comprehensive test runner for Tavily Register project.

This script runs all test suites with different configurations and generates
detailed coverage reports. It's designed to validate the enhanced test coverage
across all modules and scenarios.
"""
import os
import sys
import subprocess
import time
from pathlib import Path
from typing import List, Dict, Any


class ComprehensiveTestRunner:
    """Comprehensive test runner with coverage analysis."""

    def __init__(self, project_root: str = None):
        """Initialize test runner."""
        self.project_root = Path(project_root) if project_root else Path(__file__).parent.parent
        self.test_results: Dict[str, Any] = {}

    def run_unit_tests(self) -> Dict[str, Any]:
        """Run all unit tests with coverage."""
        print("🧪 Running Unit Tests...")
        print("=" * 50)

        cmd = [
            sys.executable, "-m", "pytest",
            "tests/unit/",
            "-v",
            "--cov=src",
            "--cov-report=term-missing",
            "--cov-report=html:htmlcov/unit",
            "--cov-report=json:coverage-unit.json"
        ]

        start_time = time.time()
        result = subprocess.run(cmd, cwd=self.project_root, capture_output=True, text=True)
        end_time = time.time()

        return {
            "name": "Unit Tests",
            "duration": end_time - start_time,
            "return_code": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "success": result.returncode == 0
        }

    def run_integration_tests(self) -> Dict[str, Any]:
        """Run all integration tests."""
        print("🔗 Running Integration Tests...")
        print("=" * 50)

        cmd = [
            sys.executable, "-m", "pytest",
            "tests/integration/",
            "-v",
            "--cov=src",
            "--cov-append",
            "--cov-report=html:htmlcov/integration"
        ]

        start_time = time.time()
        result = subprocess.run(cmd, cwd=self.project_root, capture_output=True, text=True)
        end_time = time.time()

        return {
            "name": "Integration Tests",
            "duration": end_time - start_time,
            "return_code": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "success": result.returncode == 0
        }
    
    def run_specific_module_tests(self, module_pattern: str) -> Dict[str, Any]:
        """Run tests for specific module pattern."""
        print(f"🎯 Running Tests for {module_pattern}...")
        print("=" * 50)
        
        cmd = [
            sys.executable, "-m", "pytest",
            f"tests/unit/test_{module_pattern}.py",
            "-v",
            "--cov=src",
            "--cov-report=term-missing"
        ]
        
        start_time = time.time()
        result = subprocess.run(cmd, cwd=self.project_root, capture_output=True, text=True)
        end_time = time.time()
        
        return {
            "name": f"{module_pattern.title()} Tests",
            "duration": end_time - start_time,
            "return_code": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "success": result.returncode == 0
        }
    
    def run_performance_tests(self) -> Dict[str, Any]:
        """Run performance-focused tests."""
        print("⚡ Running Performance Tests...")
        print("=" * 50)
        
        cmd = [
            sys.executable, "-m", "pytest",
            "tests/",
            "-v",
            "-k", "performance or timing or concurrent",
            "--durations=10"
        ]
        
        start_time = time.time()
        result = subprocess.run(cmd, cwd=self.project_root, capture_output=True, text=True)
        end_time = time.time()
        
        return {
            "name": "Performance Tests",
            "duration": end_time - start_time,
            "return_code": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "success": result.returncode == 0
        }
    
    def run_error_handling_tests(self) -> Dict[str, Any]:
        """Run error handling and edge case tests."""
        print("🚨 Running Error Handling Tests...")
        print("=" * 50)
        
        cmd = [
            sys.executable, "-m", "pytest",
            "tests/",
            "-v",
            "-k", "error or exception or edge or boundary",
            "--tb=short"
        ]
        
        start_time = time.time()
        result = subprocess.run(cmd, cwd=self.project_root, capture_output=True, text=True)
        end_time = time.time()
        
        return {
            "name": "Error Handling Tests",
            "duration": end_time - start_time,
            "return_code": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "success": result.returncode == 0
        }
    
    def generate_coverage_report(self) -> Dict[str, Any]:
        """Generate comprehensive coverage report."""
        print("📊 Generating Coverage Report...")
        print("=" * 50)
        
        cmd = [
            sys.executable, "-m", "pytest",
            "tests/",
            "--cov=src",
            "--cov-report=html:htmlcov/comprehensive",
            "--cov-report=term-missing",
            "--cov-report=json:coverage-comprehensive.json",
            "--cov-fail-under=80"  # Require at least 80% coverage
        ]
        
        start_time = time.time()
        result = subprocess.run(cmd, cwd=self.project_root, capture_output=True, text=True)
        end_time = time.time()
        
        return {
            "name": "Coverage Report",
            "duration": end_time - start_time,
            "return_code": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "success": result.returncode == 0
        }
    
    def run_all_tests(self) -> None:
        """Run all test suites and generate reports."""
        print("🚀 Starting Comprehensive Test Suite")
        print("=" * 60)
        
        # Test suites to run
        test_suites = [
            ("unit", self.run_unit_tests),
            ("integration", self.run_integration_tests),
            ("config", lambda: self.run_specific_module_tests("config")),
            ("utils", lambda: self.run_specific_module_tests("utils")),
            ("intelligent_automation", lambda: self.run_specific_module_tests("intelligent_automation")),
            ("traditional_automation", lambda: self.run_specific_module_tests("traditional_automation")),
            ("email_checker", lambda: self.run_specific_module_tests("email_checker")),
            ("email_login_helper", lambda: self.run_specific_module_tests("email_login_helper")),
            ("main_controller", lambda: self.run_specific_module_tests("main_controller")),
            ("performance", self.run_performance_tests),
            ("error_handling", self.run_error_handling_tests),
            ("coverage", self.generate_coverage_report)
        ]
        
        # Run each test suite
        for suite_name, suite_func in test_suites:
            try:
                result = suite_func()
                self.test_results[suite_name] = result
                
                if result["success"]:
                    print(f"✅ {result['name']} - PASSED ({result['duration']:.2f}s)")
                else:
                    print(f"❌ {result['name']} - FAILED ({result['duration']:.2f}s)")
                    print(f"   Error: {result['stderr'][:200]}...")
                
            except Exception as e:
                print(f"💥 {suite_name} - CRASHED: {e}")
                self.test_results[suite_name] = {
                    "name": suite_name,
                    "success": False,
                    "error": str(e)
                }
            
            print()
        
        # Generate summary
        self.print_summary()
    
    def print_summary(self) -> None:
        """Print test execution summary."""
        print("📋 Test Execution Summary")
        print("=" * 60)
        
        total_tests = len(self.test_results)
        passed_tests = sum(1 for result in self.test_results.values() if result.get("success", False))
        failed_tests = total_tests - passed_tests
        
        total_duration = sum(
            result.get("duration", 0) 
            for result in self.test_results.values()
        )
        
        print(f"Total Test Suites: {total_tests}")
        print(f"Passed: {passed_tests}")
        print(f"Failed: {failed_tests}")
        print(f"Total Duration: {total_duration:.2f}s")
        print()
        
        # Detailed results
        for suite_name, result in self.test_results.items():
            status = "✅ PASS" if result.get("success", False) else "❌ FAIL"
            duration = result.get("duration", 0)
            print(f"{status} {result.get('name', suite_name):30} ({duration:.2f}s)")
        
        print()
        
        if failed_tests == 0:
            print("🎉 All test suites passed successfully!")
        else:
            print(f"⚠️  {failed_tests} test suite(s) failed. Check the output above for details.")
        
        # Coverage information
        coverage_file = self.project_root / "coverage-comprehensive.json"
        if coverage_file.exists():
            try:
                import json
                with open(coverage_file) as f:
                    coverage_data = json.load(f)
                    total_coverage = coverage_data.get("totals", {}).get("percent_covered", 0)
                    print(f"📊 Overall Test Coverage: {total_coverage:.1f}%")
            except Exception:
                print("📊 Coverage data available in htmlcov/comprehensive/index.html")


def main():
    """Main entry point for comprehensive test runner."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Run comprehensive tests for Tavily Register")
    parser.add_argument("--suite", choices=[
        "unit", "integration", "performance", "error", "coverage", "all"
    ], default="all", help="Test suite to run")
    parser.add_argument("--module", help="Specific module to test (e.g., config, utils)")
    
    args = parser.parse_args()
    
    runner = ComprehensiveTestRunner()
    
    if args.module:
        result = runner.run_specific_module_tests(args.module)
        print(f"✅ {result['name']} completed" if result["success"] else f"❌ {result['name']} failed")
    elif args.suite == "unit":
        result = runner.run_unit_tests()
        print(f"✅ Unit tests completed" if result["success"] else f"❌ Unit tests failed")
    elif args.suite == "integration":
        result = runner.run_integration_tests()
        print(f"✅ Integration tests completed" if result["success"] else f"❌ Integration tests failed")
    elif args.suite == "performance":
        result = runner.run_performance_tests()
        print(f"✅ Performance tests completed" if result["success"] else f"❌ Performance tests failed")
    elif args.suite == "error":
        result = runner.run_error_handling_tests()
        print(f"✅ Error handling tests completed" if result["success"] else f"❌ Error handling tests failed")
    elif args.suite == "coverage":
        result = runner.generate_coverage_report()
        print(f"✅ Coverage report generated" if result["success"] else f"❌ Coverage report failed")
    else:
        runner.run_all_tests()


if __name__ == "__main__":
    main()
