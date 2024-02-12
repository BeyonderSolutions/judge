import pytest
from io import StringIO
import sys

def analyze_pytest(path_base: str, file_report: str):
    # Redirect stdout to capture the pytest output
    original_stdout = sys.stdout
    sys.stdout = StringIO()

    # Run pytest programmatically
    pytest.main([path_base, '--no-header', '--no-summary'])

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
        if "failed" in pytest_output:
            md_file.write("\n> Some tests have failed. See below for details.\n\n")
        else:
            md_file.write("\n✅ All tests passed!\n")

        # Process and write the details of pytest results
        lines = pytest_output.split('\n')
        for line in lines:
            if line.startswith("FAILED") or line.startswith("ERROR"):
                # Simplify output, adjust as needed
                test_name = line.split(" ")[0]
                reason = line.split("[")[0]
                md_file.write(f"- **{test_name}**: {reason}\n")

    # Optionally, print a summary or the entire pytest output to console
    print(pytest_output)
