import io
import os
import sys

import flake8.main.application as f8
from rich import print
from rich.panel import Panel
from rich.table import Table

LINK_CODES = "https://pycodestyle.pycqa.org/en/latest/intro.html#error-codes"
LINK_PEP8 = "https://peps.python.org/pep-0008/"


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


def main():
    dir = sys.argv[1] if len(sys.argv) > 1 else os.getcwd()
    report = flake8_to_dict(dir)
    markdown_file_path = 'judge_report.md'
    print_flake8_report(report, markdown_file_path)


def flake8_to_dict(path_to_code):
    base_dir = os.path.commonpath([path_to_code])
    # Temporary redirect stdout to the custom FakeFile
    original_stdout = sys.stdout
    sys.stdout = FakeFile()
    # Initialize and run flake8
    app = f8.Application()
    app.initialize([
        "--exclude=*env*,.*env*," +
        "your_project/external_packages," +
        "*/site-packages/*",
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
            file, line_no, col_no, msg = line.rsplit(':', 3)
            # Remove base directory from file path
            relative_path = os.path.relpath(file, base_dir)
            error_code = msg.strip().split(' ')[0]
            # Append the issue to the results dict
            results.setdefault(relative_path, []).append({
                'line': int(line_no),
                'column': int(col_no),
                'error_code': error_code,
                'message': msg.strip()[5:]
            })
    return results


def md_link(content, link):
    return f"[{content}]({link})"


def print_flake8_report(report, markdown_file_path):
    with open(markdown_file_path, 'w', encoding="utf-8") as md_file:
        md_file.write("# ⚖️ Judge Report\n")
        md_file.write("## ❄️ flake8\n")
        pep8_link = md_link("PEP8", LINK_PEP8)
        md_file.write(f"Python code review for {pep8_link} compliance.\n")
        # Sanity check. If there are no issues, report will be empty.
        if not report:
            message = "✅ No issues found!"
            md_file.write(f"\n>{message}\n")
            print(Panel(message, title="Success", expand=False, style="green"))
            return
        # Loop through each issue.
        for file_path, issues in report.items():
            table = Table(title=file_path, title_justify="left")
            # Define columns
            table.add_column("Line", justify="right")
            table.add_column("Col.", justify="right")
            table.add_column("Code")
            table.add_column("Message")
            # Markdown table header
            md_file.write(f"### 📄 `{file_path}`\n\n")
            md_file.write("| Line | Col. | Code | Message |\n")
            md_file.write("|-----:|-----:|------|---------|\n")
            # Add rows for each issue
            for issue in issues:
                line_str = str(issue["line"])
                col_str = str(issue["column"])
                code = issue["error_code"]
                message = issue["message"]
                table.add_row(line_str, col_str, code, message)
                # Add Markdown row
                code_link = md_link(code, LINK_CODES)
                md_file.write(
                    f"| {line_str} | {col_str} | {code_link} | {message} |\n"
                )
            # Print the table to console
            print(table)

if __name__ == "__main__":
    main()