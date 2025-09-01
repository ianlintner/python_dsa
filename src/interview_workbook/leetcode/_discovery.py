"""
 Discovery

TODO: Add problem description
"""

import importlib
import pathlib
import pkgutil


def ensure_problems_loaded():
    """
    Import all modules in the leetcode package to trigger their problem registration.
    This ensures that `register_problem()` calls defined in each file are executed.
    """
    pkg_dir = pathlib.Path(__file__).parent
    pkg_name = "src.interview_workbook.leetcode" # Use a fixed path
    
    for _, module_name, is_pkg in pkgutil.iter_modules([str(pkg_dir)]):
        if module_name.startswith("_"):
            continue
        
        if is_pkg:
            sub_pkg_dir = pkg_dir / module_name
            sub_pkg_name = f"{pkg_name}.{module_name}"
            for _, sub_module_name, _ in pkgutil.iter_modules([str(sub_pkg_dir)]):
                if sub_module_name.startswith("_"):
                    continue
                full_name = f"{sub_pkg_name}.{sub_module_name}"
                try:
                    importlib.import_module(full_name)
                except Exception:
                    continue
        else:
            full_name = f"{pkg_name}.{module_name}"
            try:
                importlib.import_module(full_name)
            except Exception:
                # Fail softly to avoid blocking test discovery
                continue
