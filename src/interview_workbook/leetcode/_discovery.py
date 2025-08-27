"""
LeetCode problem discovery and auto-import system.

This module automatically discovers existing problem modules and imports them
to trigger their register_problem() calls, populating the registry.
"""

import importlib
import os
from pathlib import Path
from typing import Set

from ._registry import get_all, PROBLEMS
from ._types import Category


def get_leetcode_base_dir() -> Path:
    """Get the base directory for LeetCode problems."""
    return Path(__file__).parent


def discover_problem_modules() -> Set[str]:
    """
    Discover all problem module paths by scanning the filesystem.
    
    Returns:
        Set of module paths like "interview_workbook.leetcode.arrays_hashing.two_sum"
    """
    base_dir = get_leetcode_base_dir()
    modules = set()
    
    for category in Category:
        category_dir = base_dir / category.value
        if not category_dir.exists() or not category_dir.is_dir():
            continue
            
        for py_file in category_dir.glob("*.py"):
            if py_file.name.startswith("_") or py_file.name == "__init__.py":
                continue
                
            module_name = py_file.stem
            module_path = f"interview_workbook.leetcode.{category.value}.{module_name}"
            modules.add(module_path)
    
    return modules


def import_problem_module(module_path: str) -> bool:
    """
    Import a problem module to trigger its register_problem() call.
    
    Args:
        module_path: Full dotted module path
        
    Returns:
        True if import succeeded, False otherwise
    """
    try:
        importlib.import_module(module_path)
        return True
    except ImportError as e:
        print(f"Failed to import {module_path}: {e}")
        return False
    except Exception as e:
        print(f"Error importing {module_path}: {e}")
        return False


def discover_and_import_all() -> dict[str, bool]:
    """
    Discover and import all problem modules.
    
    Returns:
        Dict mapping module_path -> import_success
    """
    modules = discover_problem_modules()
    results = {}
    
    for module_path in sorted(modules):
        success = import_problem_module(module_path)
        results[module_path] = success
    
    return results


def get_registered_slugs() -> Set[str]:
    """Get set of slugs for all registered problems."""
    return {p["slug"] for p in get_all()}


def clear_registry() -> None:
    """Clear the problem registry. Useful for testing."""
    PROBLEMS.clear()


def ensure_problems_loaded() -> None:
    """
    Ensure all discoverable problems are loaded into the registry.
    This is called by other modules to populate the registry on-demand.
    """
    if not get_all():  # Registry is empty, need to populate
        discover_and_import_all()


# Auto-discovery on module import
discover_and_import_all()
