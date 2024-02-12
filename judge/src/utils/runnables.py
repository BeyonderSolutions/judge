import sys
from typing import Dict, List

ANALYZERS = {
    "flake8": ["--flake8", "-f8"],
    "pytest": ["--pytest", "-pt"]
}


def get_runnables(settings: Dict) -> List:
    def get_all():
        return list(ANALYZERS.keys())

    args = sys.argv[1:]
    # First, check if we're running all.
    if "--run-all" in args or "-a" in args:
        return get_all()
    # Second, check if we're running some in particular.
    runnables = []
    for key, flags in ANALYZERS.items():
        for flag in flags:
            if flag in args:
                runnables.append(key)
                break
    if runnables:
        return runnables
    # Finally, check for defaults.
    defaults = settings.get("judge", {}).get("defaults", [])
    if not defaults:
        return get_all()
    return defaults
