import io
import os
import re
import sys

import flake8.main.application as f8
import toml
from rich import print
from rich.panel import Panel
from rich.table import Table

FILE_REPORT = "judge_report.md"
FILE_SETTINGS = "judge_settings.toml"
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
    # Load the settings file.
    if os.path.exists(FILE_SETTINGS):
        with open(FILE_SETTINGS, "r", encoding="utf-8") as file:
            settings = toml.load(file)
            print(f"Loaded settings from '{FILE_SETTINGS}'.")
    else:
        settings = {}
    # Flake8
    report = flake8_to_dict(dir, settings=settings.get("flake8", {}))
    print_flake8_report(report, FILE_REPORT)


def flake8_to_dict(path_to_code: str, settings: dict = {}):
    # Arguments for flake8.
    ignore = f"--ignore={','.join(settings['ignore'])}" \
        if settings.get("ignore", []) else ""
    exclude = str(','.join(settings.get("exclude", [])))
    # Initialize the flake8 application.
    app = f8.Application()
    # Base directory for relative paths.
    base_dir = os.path.commonpath([path_to_code])
    # Temporary redirect stdout to the custom FakeFile
    original_stdout = sys.stdout
    sys.stdout = FakeFile()

    # Initialize and run flake8.
    app.initialize([
        ignore,
        "--exclude=*env*,.*env*,"
        "your_project/external_packages,"
        "*/site-packages/*," + exclude,
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
            # Parse everything.
            pattern = re.compile(r"(.*\.py):(\d+):(\d+): (\w+) (.*)")
            try:
                match = pattern.match(line)
                results.setdefault(relative_path, []).append({
                    "file": match.group(1),
                    "line": int(match.group(2)),
                    "column": int(match.group(3)),
                    "error_code": match.group(4),
                    "message": match.group(5)
                })
            except Exception as e:
                print(e)
                print("There was an error parsing the following flake8 line:")
                print(line)
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
            print(Panel(
                message,
                title="Success",
                title_align="left",
                expand=False,
                style="green"
            ))
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
                code_link = md_link(
                    code,
                    f"https://www.flake8rules.com/rules/{code}.html"
                )
                md_file.write(
                    f"| {line_str} | {col_str} | {code_link} | {message} |\n"
                )
            # Print the table to console
            print(table)


if __name__ == "__main__":
    main()
