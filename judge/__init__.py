
import os
import sys

import toml
from rich import print

from .src.analyzers import analyze_flake8

FILE_REPORT = "judge_report.md"
FILE_SETTINGS = "judge_settings.toml"


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
    analyze_flake8(path_base=dir, file_report=FILE_REPORT, settings=settings)


if __name__ == "__main__":
    main()
