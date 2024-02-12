import os
import re
import xml.etree.ElementTree as ET

import pytest


def analyze_pytest(
    path_base: str,
    file_report: str,
    report_xml_path="pytest_report.xml"
):
    # Run pytest and generate an XML report.
    pytest.main([
        path_base,
        '--no-header',
        '--no-summary',
        '-rA',
        f'--junitxml={report_xml_path}'
    ])
    # Parse the XML report and write to the markdown report.
    _parse_and_write_pytest_report(report_xml_path, file_report)


def _parse_and_write_pytest_report(report_xml_path, markdown_file_path):
    # Parse the XML file.
    tree = ET.parse(report_xml_path)
    root = tree.getroot()

    with open(markdown_file_path, 'a', encoding="utf-8") as md_file:
        md_file.write("\n## 🧪 pytest\n")
        md_file.write("Automated unit testing for Python.\n")
        testcases = root.findall(".//testcase")
        failures_present = False
        # Loop through test cases.
        for testcase in testcases:
            failures = testcase.findall("failure")
            if failures:
                failures_present = True
                test_name = f"`{testcase.attrib.get('classname')}`" \
                    f"::`{testcase.attrib.get('name')}`"
                md_file.write(f"### 📄 {test_name}\n")
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
    os.remove(report_xml_path)
