#!/usr/bin/env python3
"""
Test runner script for the High School Management System API.

This script provides various test execution options including
basic test runs, coverage reports, and verbose output.
"""

import subprocess
import sys
import os


def run_command(cmd, description):
    """Run a command and handle the output."""
    print(f"\n{'='*60}")
    print(f"🧪 {description}")
    print(f"{'='*60}")
    
    try:
        result = subprocess.run(cmd, shell=True, check=True, cwd=os.getcwd())
        print(f"✅ {description} completed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed with exit code {e.returncode}")
        return False


def main():
    """Main test runner function."""
    if len(sys.argv) > 1:
        test_type = sys.argv[1]
    else:
        test_type = "basic"
    
    # Change to project root directory
    project_root = os.path.dirname(os.path.abspath(__file__))
    os.chdir(project_root)
    
    print("🚀 High School Management System - Test Runner")
    print(f"📁 Working directory: {project_root}")
    
    if test_type == "basic" or test_type == "all":
        # Run basic tests
        success = run_command(
            "python -m pytest tests/ -v", 
            "Running basic test suite"
        )
        if not success and test_type != "all":
            sys.exit(1)
    
    if test_type == "coverage" or test_type == "all":
        # Run tests with coverage
        success = run_command(
            "python -m pytest tests/ --cov=src --cov-report=term-missing --cov-report=html -v",
            "Running tests with coverage analysis"
        )
        if success:
            print("📊 Coverage report generated in htmlcov/index.html")
        if not success and test_type != "all":
            sys.exit(1)
    
    if test_type == "install":
        # Install dependencies
        success = run_command(
            "python -m pip install -r requirements.txt",
            "Installing test dependencies"
        )
        if not success:
            sys.exit(1)
    
    if test_type not in ["basic", "coverage", "install", "all"]:
        print(f"""
❓ Unknown test type: {test_type}

Available options:
  basic     - Run basic test suite (default)
  coverage  - Run tests with coverage analysis  
  install   - Install test dependencies
  all       - Run all tests and coverage

Usage examples:
  python run_tests.py
  python run_tests.py basic
  python run_tests.py coverage
  python run_tests.py install
  python run_tests.py all
        """)
        sys.exit(1)
    
    print(f"\n🎉 Test execution completed!")


if __name__ == "__main__":
    main()