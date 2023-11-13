import io
import os
import sys

import flake8.main.application as f8
from dotenv import load_dotenv
from rich import print
from rich.table import Table


class FakeFile(io.StringIO):
    def __init__(self):
        super().__init__()
        self.buffer = self

    def write(self, s):
        if isinstance(s, bytes):
            # Decode bytes to a string and write
            s = s.decode('utf-8')
        super().write(s)

    def getvalue(self):
        return super().getvalue()


def flake8_to_dict(path_to_code):
    base_dir = os.path.commonpath([path_to_code])
    
    # Temporary redirect stdout to the custom FakeFile
    original_stdout = sys.stdout
    sys.stdout = FakeFile()

    # Initialize and run flake8
    app = f8.Application()
    app.initialize([
        '--exclude=venv,.venv,your_project/external_packages,*/site-packages/*',
        path_to_code
    ])
    app.run_checks()
    app.report()

    # Capture and restore stdout
    flake8_output = sys.stdout.getvalue()
    sys.stdout = original_stdout

    # Parse the flake8 output
    results = {}
    for line in flake8_output.strip().split('\n'):
        if line:  # Ensure the line is not empty
            file, line_no, col_no, msg = line.split(':', 3)
            # Remove base directory from file path
            relative_path = os.path.relpath(file, base_dir)
            error_code = msg.strip().split(' ')[0]
            results.setdefault(relative_path, []).append({
                'line': int(line_no),
                'column': int(col_no),
                'error_code': error_code,
                'message': msg.strip()[5:]
            })

    return results


def print_flake8_report(report):
    for file_path, issues in report.items():
        table = Table(title=file_path)

        # Define columns
        table.add_column("Line", justify="right")
        table.add_column("Col.", justify="right")
        table.add_column("Code")
        table.add_column("Message")

        # Add rows for each issue
        for issue in issues:
            table.add_row(str(issue["line"]), str(issue["column"]), issue["error_code"], issue["message"])

        # Print the table
        print(table)


load_dotenv()
report = flake8_to_dict(os.getenv("DIR"))
print_flake8_report(report)
