"""
 Discovery

TODO: Add problem description
"""


import importlib
import pkgutil
import pathlib


def ensure_problems_loaded():
    """
    Import all modules in the leetcode package to trigger their problem registration.
    This ensures that `register_problem()` calls defined in each file are executed.
    """
    pkg_dir = pathlib.Path(__file__).parent
    pkg_name = __name__.rsplit(".", 1)[0]
    for _, module_name, _ in pkgutil.iter_modules([str(pkg_dir)]):
        if module_name.startswith("_"):
            continue
        full_name = f"{pkg_name}.{module_name}"
        try:
            importlib.import_module(full_name)
        except Exception:
            # Fail softly to avoid blocking test discovery
            continue
