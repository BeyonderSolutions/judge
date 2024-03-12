import os
import re
import xml.etree.ElementTree as ET
from typing import Dict, List

import pytest

PATH_XML = "pytest_report.xml"


def analyze_pytest(
    path_base: str,
    file_report: str,
    settings: Dict = {}
) -> None:
    # Retrieve the settings for pytest.
    settings = settings.get("pytest", {})
    paths: List = settings.get("paths", [])
    if not paths:
        paths.append(path_base)
    # Run pytest and generate an XML report.
    first = True
    for path in paths:
        pytest.main([
            path,
            '--no-header',
            '--no-summary',
            '-rA',
            f'--junitxml={PATH_XML}'
        ])
        # Parse the XML report and write to the markdown report.
        _parse_and_write_pytest_report(file_report, path=path, first=first)
        first = False


def _parse_and_write_pytest_report(
    markdown_file_path: str,
    path: str,
    first: bool
) -> None:
    # Parse the XML file.
    tree = ET.parse(PATH_XML)
    root = tree.getroot()

    with open(markdown_file_path, 'a', encoding="utf-8") as md_file:
        if first:
            md_file.write("\n## 🧪 pytest\n")
            md_file.write("Automated unit testing for Python.\n")
        md_file.write(f"\n### 📁 `{path}`\n")
        testcases = root.findall(".//testcase")
        failures_present = False
        # Loop through test cases.
        for testcase in testcases:
            failures = testcase.findall("failure")
            if failures:
                failures_present = True
                test_name = f"`{testcase.attrib.get('classname')}`" \
                    f"::`{testcase.attrib.get('name')}`"
                md_file.write(f"#### 📄 `{test_name}`\n")
                for failure in failures:
                    sections = failure.text.strip().split("\n_")
                    for index, section in enumerate(sections):
                        # Exclude lines that consist solely of underscores or
                        # spaces and underscores.
                        lines = section.strip().split('\n')
                        filtered_lines = [
                            line for line
                            in lines if not re.match(r'^[_\s]*$', line)
                        ]
                        if filtered_lines:
                            md_file.write("```\n")
                            md_file.write("\n".join(filtered_lines))
                            md_file.write("\n```\n\n")
        if not failures_present:
            md_file.write("\n>✅ All tests passed!\n")
    # Delete the pytest_report.xml file
    os.remove(PATH_XML)
