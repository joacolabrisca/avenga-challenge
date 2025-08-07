## Command-line utility for running API automation tests.

import argparse
import subprocess
import sys
from pathlib import Path


## Run a shell command and handle errors
def run_command(command: str, description: str) -> bool:
    print(f"\n{description}...")
    print(f"Executing: {command}")
    
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed with exit code {e.returncode}")
        if e.stdout:
            print("STDOUT:", e.stdout)
        if e.stderr:
            print("STDERR:", e.stderr)
        return False


## Install project dependencies
def install_dependencies():
    return run_command("pip install -r requirements.txt", "Installing dependencies")


## Clean generated test files and reports
def clean_generated_files():
    files_to_clean = [
        "reports/*.html",
        "reports/*.xml", 
        "reports/*.json",
        "reports/coverage/",
        "__pycache__/",
        "*.pyc"
    ]
    
    for pattern in files_to_clean:
        run_command(f"rm -rf {pattern}", f"Cleaning {pattern}")


## Build the pytest command based on arguments
def build_pytest_command(args) -> str:
    cmd_parts = ["pytest"]
    
    # Add markers if specified
    if args.markers:
        markers_str = " or ".join(args.markers)
        cmd_parts.append(f"-m '{markers_str}'")
    
    # Add verbose flag
    if args.verbose:
        cmd_parts.append("-v")
    
    # Add HTML report
    if args.html_report:
        cmd_parts.append("--html=reports/report.html --self-contained-html")
    
    # Add coverage report
    if args.coverage:
        cmd_parts.append("--cov=utils --cov-report=html:reports/coverage --cov-report=term-missing")
    
    # Add additional options
    cmd_parts.extend([
        "--tb=short",
        "--disable-warnings"
    ])
    
    return " ".join(cmd_parts)


## Main function to run the test automation
def main():
    parser = argparse.ArgumentParser(description='Run Books API automation tests')
    
    parser.add_argument(
        '--markers', 
        nargs='+', 
        help='PyTest markers to run (e.g., smoke, regression, api)'
    )
    parser.add_argument(
        '--html-report', 
        action='store_true', 
        help='Generate HTML test report'
    )
    parser.add_argument(
        '--coverage', 
        action='store_true', 
        help='Generate code coverage report'
    )
    parser.add_argument(
        '--verbose', '-v', 
        action='store_true', 
        help='Run in verbose mode'
    )
    parser.add_argument(
        '--install-deps', 
        action='store_true', 
        help='Install dependencies before running tests'
    )
    parser.add_argument(
        '--clean', 
        action='store_true', 
        help='Clean generated files before running tests'
    )
    
    args = parser.parse_args()
    
    print("🚀 Books API Automation Test Runner")
    print("=" * 50)
    
    # Install dependencies if requested
    if args.install_deps:
        if not install_dependencies():
            print("❌ Failed to install dependencies. Exiting.")
            sys.exit(1)
    
    # Clean generated files if requested
    if args.clean:
        clean_generated_files()
    
    # Create reports directory if it doesn't exist
    Path("reports").mkdir(exist_ok=True)
    
    # Build and execute pytest command
    pytest_cmd = build_pytest_command(args)
    
    print(f"\n🧪 Running tests with command:")
    print(f"   {pytest_cmd}")
    print("\n" + "=" * 50)
    
    # Run the tests
    success = run_command(pytest_cmd, "Running API tests")
    
    if success:
        print("\n✅ All tests completed successfully!")
        
        # Show report locations
        if args.html_report:
            print(f"📊 HTML Report: reports/report.html")
        if args.coverage:
            print(f"📈 Coverage Report: reports/coverage/index.html")
        
        print(f"📁 All reports: reports/")
    else:
        print("\n❌ Some tests failed. Check the output above for details.")
        sys.exit(1)


if __name__ == "__main__":
    main() 
