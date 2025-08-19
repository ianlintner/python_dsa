"""
LeetCode Top 100 Problem Collection

A curated collection of the most important coding interview problems,
organized by category with consistent structure, metadata, and demos.

This package provides:
- Canonical problem implementations with Solution classes
- Comprehensive test cases and demos
- Category-based organization
- Metadata registry for discovery and validation
"""

from ._registry import by_category, by_slug, get_all, validate_registry
from ._types import Category, Difficulty, ProblemMeta

__all__ = [
    "Difficulty",
    "Category",
    "ProblemMeta",
    "get_all",
    "by_category",
    "by_slug",
    "validate_registry",
]
