import os

import toml


def load_settings(file_settings: str) -> dict:
    if os.path.exists(file_settings):
        with open(file_settings, "r", encoding="utf-8") as file:
            print(f"Loaded settings from '{file_settings}'.")
            return toml.load(file)
    return {}
