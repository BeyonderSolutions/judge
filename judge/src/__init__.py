import os
import sys

from .analyzers import analyze_flake8, analyze_pytest
from .utils import load_settings

FILE_REPORT = "judge_report.md"
FILE_SETTINGS = "judge_settings.toml"


def main():
    dir = sys.argv[1] if len(sys.argv) > 1 else os.getcwd()
    settings: dict = load_settings(FILE_SETTINGS)
    # Analyzers
    analyze_flake8(path_base=dir, file_report=FILE_REPORT, settings=settings)
    analyze_pytest(path_base=dir, file_report=FILE_REPORT)