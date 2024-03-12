import os
import sys
from typing import Dict, List

from .analyzers import analyze_flake8, analyze_pytest
from .utils import get_runnables, load_settings

FILE_REPORT = "judge_report.md"
FILE_SETTINGS = "judge_settings.toml"


def main():
    dir = (
        sys.argv[1] if len(sys.argv) > 1
        and not sys.argv[1].startswith("-") else os.getcwd()
    )
    settings: Dict = load_settings(FILE_SETTINGS)
    # Analyzers
    runnables: List = get_runnables(settings=settings)
    if "flake8" in runnables:
        analyze_flake8(
            path_base=dir,
            file_report=FILE_REPORT,
            settings=settings
        )
    if "pytest" in runnables:
        analyze_pytest(
            path_base=dir,
            file_report=FILE_REPORT,
            settings=settings
        )
