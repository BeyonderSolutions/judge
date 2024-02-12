import sys
from io import StringIO

import pytest


def analyze_pytest(path_base: str, file_report: str):
    # Redirect stdout to capture the pytest output
    original_stdout = sys.stdout
    sys.stdout = StringIO()

    # Run pytest programmatically with options for detailed output
    pytest.main([path_base, '-vv', '--no-header', '--no-summary', '-rA'])

    # Capture the pytest output
    pytest_output = sys.stdout.getvalue()

    # Restore stdout
    sys.stdout = original_stdout

    # Parse and print the pytest report
    _print_pytest_report(pytest_output, file_report)

def _print_pytest_report(pytest_output, markdown_file_path):
    with open(markdown_file_path, 'a', encoding="utf-8") as md_file:  # Append mode
        md_file.write("\n## 🧪 pytest\n")
        md_file.write("Python pytest results.\n")
        # Search for test failure indications
        failures = [line for line in pytest_output.split('\n') if 'FAILED' in line]
        if failures:
            md_file.write("\n> Some tests have failed. See below for details.\n\n")
            for failure in failures:
                # Extract test name and failure reason (simplified)
                test_name = failure.split("::")[-1].split(" ")[0]
                reason = "Failure details not shown here. Check the test output for more information."
                md_file.write(f"- **{test_name}**: {reason}\n")
        else:
            md_file.write("\n✅ All tests passed!\n")

    # Optionally, print a summary or the entire pytest output to console
    print(pytest_output)
