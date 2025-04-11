import argparse
import os
import pytest
import time
import shutil
import subprocess
from typing import List, Optional


class CLIRunner:
    def __init__(self):
        self.timestamp = time.strftime("%Y%m%d%H%M%S", time.localtime())
        self.current_path = os.getcwd()
        self.report_path = None
        self.result_path = None
        self.csv_path = None

    def setup_paths(self):
        self.report_path = os.path.join(self.current_path, "report", self.timestamp, "report")
        self.result_path = os.path.join(self.current_path, "report", self.timestamp, "results")
        self.csv_path = os.path.join(self.current_path, "report", self.timestamp, "csv")
        # Create directories
        os.makedirs(self.report_path, exist_ok=True)
        os.makedirs(self.result_path, exist_ok=True)
        os.makedirs(self.csv_path, exist_ok=True)
        
        # Create csv file
        self.csv_file_path = os.path.join(self.csv_path, "report.csv")

    def run_tests(self, test_path: Optional[str] = None, repeat: int = 1, markers: Optional[List[str]] = None):
        pytest_args = [
            "-v", "-s",
            "--capture=sys",
            "--alluredir", self.result_path,
            "--csv", self.csv_file_path
        ]

        # Add repeat option using pytest-repeat if repeat > 1
        if repeat > 1:
            pytest_args.extend(["--repeat", str(repeat)])

        # Add test path if specified
        if test_path:
            pytest_args.append(test_path)

        # Add markers if specified
        if markers:
            for marker in markers:
                pytest_args.extend(["-m", marker])

        pytest.main(pytest_args)

    def generate_report(self):
        """Generate Allure report if available."""
        try:
            # Try to run allure command
            result = subprocess.run(["allure", "--version"], capture_output=True, text=True)
            if result.returncode == 0:
                # Allure is available, generate report
                subprocess.run(["allure", "generate", self.result_path, "-o", self.report_path, "--clean"])
                print("Allure report has been generated")
                return True
        except FileNotFoundError:
            print("Allure command line tool is not installed. Skipping report generation.")
            print("To install Allure, follow these steps:")
            print("1. Download Allure from: https://github.com/allure-framework/allure2/releases")
            print("2. Extract the archive to a directory")
            print("3. Add the bin directory to your system PATH")
        except Exception as e:
            print(f"Error generating Allure report: {e}")
        return False

    def customize_report(self):
        """Customize the report if it was generated."""
        if not os.path.exists(self.report_path):
            return

        try:
            self._update_report_title()
            self._update_summary_json()
            self._replace_favicon()
        except Exception as e:
            print(f"Warning: Could not customize report: {e}")

    def _update_report_title(self):
        """Update the report title."""
        index_file_path = os.path.join(self.report_path, "index.html")
        if os.path.exists(index_file_path):
            self._replace_in_file(index_file_path, 
                                "<title>Allure Report</title>", 
                                "<title>PyECUTest测试报告</title>")

    def _update_summary_json(self):
        """Update the summary JSON file."""
        summary_json_path = os.path.join(self.report_path, "widgets", "summary.json")
        if os.path.exists(summary_json_path):
            self._replace_in_file(summary_json_path, 
                                '"reportName":"Allure Report"', 
                                '"reportName":"PyECUTest测试报告📖🌝"')

    def _replace_favicon(self):
        """Replace the favicon if custom one exists."""
        favicon_path = os.path.join(self.current_path, "resource", "report", "ico", "favicon.ico")
        report_favicon_path = os.path.join(self.report_path, "favicon.ico")
        if os.path.exists(favicon_path) and os.path.exists(os.path.dirname(report_favicon_path)):
            shutil.copy(favicon_path, report_favicon_path)
            print("favicon.ico has been replaced")

    @staticmethod
    def _replace_in_file(file_path: str, old_text: str, new_text: str):
        """Replace text in a file."""
        if not os.path.exists(file_path):
            return
            
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                content = file.read()
            content = content.replace(old_text, new_text)
            with open(file_path, "w", encoding="utf-8") as file:
                file.write(content)
        except Exception as e:
            print(f"Warning: Could not modify {file_path}: {e}")

    def open_report(self):
        """Open the generated report."""
        if not os.path.exists(self.report_path):
            print("No report to open. Generate a report first.")
            return

        try:
            subprocess.run(["allure", "open", self.report_path])
        except FileNotFoundError:
            print("Allure command line tool is not installed. Cannot open report.")
            print(f"You can manually open the report at: {self.report_path}")
        except Exception as e:
            print(f"Error opening report: {e}")

    def run(self, test_path: Optional[str] = None, repeat: int = 1, markers: Optional[List[str]] = None, 
            no_report: bool = False, open_report: bool = False):
        """Run the test suite."""
        self.setup_paths()
        self.run_tests(test_path, repeat, markers)
        
        if not no_report:
            if self.generate_report():
                self.customize_report()
                if open_report:
                    self.open_report()


def main():
    parser = argparse.ArgumentParser(description='PyECUTest - A testing framework for ECU testing based on pytest')
    parser.add_argument('test_path', nargs='?', help='Path to test file or directory')
    parser.add_argument('-m', '--markers', nargs='+', help='Run tests with specific markers')
    parser.add_argument('-r', '--repeat', type=int, default=1, help='Number of times to repeat each test')
    parser.add_argument('--no-report', action='store_true', help='Do not generate Allure report')
    parser.add_argument('--open-report', action='store_true', help='Open Allure report after generation')

    args = parser.parse_args()

    runner = CLIRunner()
    runner.run(
        test_path=args.test_path,
        repeat=args.repeat,
        markers=args.markers,
        no_report=args.no_report,
        open_report=args.open_report
    )


if __name__ == "__main__":
    main() 