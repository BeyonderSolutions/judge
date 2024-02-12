import sys
from io import StringIO

import pytest

import xml.etree.ElementTree as ET

def analyze_pytest(path_base: str, file_report: str, report_xml_path="pytest_report.xml"):
    # Run pytest and generate an XML report
    pytest.main([path_base, '--no-header', '--no-summary', '-rA', f'--junitxml={report_xml_path}'])

    # Parse the XML report and write to the markdown report
    _parse_and_write_pytest_report(report_xml_path, file_report)

def _parse_and_write_pytest_report(report_xml_path, markdown_file_path):
    # Parse the XML file
    tree = ET.parse(report_xml_path)
    root = tree.getroot()

    with open(markdown_file_path, 'a', encoding="utf-8") as md_file:
        md_file.write("\n## 🧪 pytest\n")
        md_file.write("Python pytest results.\n")

        testcases = root.findall(".//testcase")
        failures_present = False

        for testcase in testcases:
            failures = testcase.findall("failure")
            if failures:
                failures_present = True
                # Assuming 'classname' and 'name' attributes hold the test suite and test name respectively
                test_name = f"{testcase.attrib.get('classname')}::{testcase.attrib.get('name')}"
                md_file.write(f"- **{test_name}**: \n")
                md_file.write("```\n")  # Markdown code block for readability
                for failure in failures:
                    md_file.write(failure.text.strip())  # Include the failure details
                    md_file.write("\n")
                md_file.write("```\n")

        if not failures_present:
            md_file.write("\n✅ All tests passed!\n")
