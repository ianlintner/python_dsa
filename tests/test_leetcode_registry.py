"""
Tests for LeetCode problem registry validation.
"""

import pytest

from interview_workbook.leetcode._registry import (
    PROBLEMS,
    by_category,
    by_slug,
    get_all,
    get_stats,
    validate_registry,
)
from interview_workbook.leetcode._types import Category, Difficulty


def test_registry_not_empty():
    """Registry should have at least some problems after importing modules."""
    # Import modules to trigger registration
    import interview_workbook.leetcode.arrays_hashing.two_sum  # noqa: F401
    import interview_workbook.leetcode.sliding_window.best_time_to_buy_sell_stock  # noqa: F401
    import interview_workbook.leetcode.two_pointers.valid_palindrome  # noqa: F401

    assert len(PROBLEMS) >= 3, "Registry should contain at least 3 problems"


def test_validate_registry():
    """Registry validation should pass for properly registered problems."""
    # Import modules to populate registry
    import interview_workbook.leetcode.arrays_hashing.two_sum  # noqa: F401
    import interview_workbook.leetcode.sliding_window.best_time_to_buy_sell_stock  # noqa: F401
    import interview_workbook.leetcode.two_pointers.valid_palindrome  # noqa: F401

    # Should not raise any exceptions
    validate_registry()


def test_by_slug():
    """by_slug should find problems correctly."""
    # Import modules to populate registry
    import interview_workbook.leetcode.arrays_hashing.two_sum  # noqa: F401

    problem = by_slug("two_sum")
    assert problem is not None
    assert problem["slug"] == "two_sum"
    assert problem["title"] == "Two Sum"
    assert problem["category"] == Category.ARRAYS_HASHING

    # Non-existent problem
    assert by_slug("nonexistent_problem") is None


def test_by_category():
    """by_category should filter problems correctly."""
    # Import modules to populate registry
    import interview_workbook.leetcode.arrays_hashing.two_sum  # noqa: F401
    import interview_workbook.leetcode.two_pointers.valid_palindrome  # noqa: F401

    arrays_problems = by_category(Category.ARRAYS_HASHING)
    assert len(arrays_problems) >= 1
    assert all(p["category"] == Category.ARRAYS_HASHING for p in arrays_problems)

    pointers_problems = by_category(Category.TWO_POINTERS)
    assert len(pointers_problems) >= 1
    assert all(p["category"] == Category.TWO_POINTERS for p in pointers_problems)


def test_get_all():
    """get_all should return copy of all problems."""
    # Import modules to populate registry
    import interview_workbook.leetcode.arrays_hashing.two_sum  # noqa: F401
    import interview_workbook.leetcode.two_pointers.valid_palindrome  # noqa: F401

    all_problems = get_all()
    assert len(all_problems) >= 2

    # Should be a copy, not the original
    all_problems.append({"fake": "problem"})
    assert len(get_all()) < len(all_problems)


def test_get_stats():
    """get_stats should return correct statistics."""
    # Import modules to populate registry
    import interview_workbook.leetcode.arrays_hashing.two_sum  # noqa: F401
    import interview_workbook.leetcode.sliding_window.best_time_to_buy_sell_stock  # noqa: F401
    import interview_workbook.leetcode.two_pointers.valid_palindrome  # noqa: F401

    stats = get_stats()

    assert "total" in stats
    assert "by_category" in stats
    assert "by_difficulty" in stats

    assert stats["total"] >= 3
    assert stats["by_category"]["arrays_hashing"] >= 1
    assert stats["by_category"]["two_pointers"] >= 1
    assert stats["by_category"]["sliding_window"] >= 1
    assert stats["by_difficulty"]["Easy"] >= 3


def test_problem_metadata_format():
    """Each problem should have properly formatted metadata."""
    # Import modules to populate registry
    import interview_workbook.leetcode.arrays_hashing.two_sum  # noqa: F401
    import interview_workbook.leetcode.sliding_window.best_time_to_buy_sell_stock  # noqa: F401
    import interview_workbook.leetcode.two_pointers.valid_palindrome  # noqa: F401

    for problem in PROBLEMS:
        # Required fields
        assert "id" in problem
        assert "slug" in problem
        assert "title" in problem
        assert "category" in problem
        assert "difficulty" in problem
        assert "tags" in problem
        assert "module" in problem
        assert "url" in problem
        assert "notes" in problem

        # Type checks
        assert isinstance(problem["slug"], str)
        assert isinstance(problem["title"], str)
        assert isinstance(problem["category"], Category)
        assert isinstance(problem["difficulty"], Difficulty)
        assert isinstance(problem["tags"], list)
        assert isinstance(problem["module"], str)
        assert problem["url"] is None or isinstance(problem["url"], str)
        assert problem["notes"] is None or isinstance(problem["notes"], str)

        # Format checks
        assert problem["slug"]  # Non-empty
        assert problem["title"]  # Non-empty
        assert problem["module"].startswith("interview_workbook.leetcode.")


def test_unique_constraints():
    """Problems should have unique slugs and IDs."""
    # Import modules to populate registry
    import interview_workbook.leetcode.arrays_hashing.two_sum  # noqa: F401
    import interview_workbook.leetcode.sliding_window.best_time_to_buy_sell_stock  # noqa: F401
    import interview_workbook.leetcode.two_pointers.valid_palindrome  # noqa: F401

    slugs = [p["slug"] for p in PROBLEMS]
    assert len(slugs) == len(set(slugs)), "All slugs should be unique"

    # IDs should be unique (excluding None values)
    ids = [p["id"] for p in PROBLEMS if p["id"] is not None]
    assert len(ids) == len(set(ids)), "All non-None IDs should be unique"


def test_module_path_consistency():
    """Module paths should match expected patterns."""
    # Import modules to populate registry
    import interview_workbook.leetcode.arrays_hashing.two_sum  # noqa: F401
    import interview_workbook.leetcode.sliding_window.best_time_to_buy_sell_stock  # noqa: F401
    import interview_workbook.leetcode.two_pointers.valid_palindrome  # noqa: F401

    for problem in PROBLEMS:
        expected_module = (
            f"interview_workbook.leetcode.{problem['category'].value}.{problem['slug']}"
        )
        assert problem["module"] == expected_module, f"Module path mismatch for {problem['slug']}"


@pytest.mark.parametrize(
    "slug,expected_category",
    [
        ("two_sum", Category.ARRAYS_HASHING),
        ("valid_palindrome", Category.TWO_POINTERS),
        ("best_time_to_buy_sell_stock", Category.SLIDING_WINDOW),
    ],
)
def test_specific_problems(slug, expected_category):
    """Test specific seed problems are registered correctly."""
    # Import modules to populate registry
    import interview_workbook.leetcode.arrays_hashing.two_sum  # noqa: F401
    import interview_workbook.leetcode.sliding_window.best_time_to_buy_sell_stock  # noqa: F401
    import interview_workbook.leetcode.two_pointers.valid_palindrome  # noqa: F401

    problem = by_slug(slug)
    assert problem is not None, f"Problem {slug} should be registered"
    assert problem["category"] == expected_category
    assert problem["difficulty"] == Difficulty.EASY  # All seed problems are Easy
