"""
Registry for LeetCode problems with metadata and access helpers.
"""

from typing import Any

from ._types import Category, Difficulty, ProblemMeta

# Global registry of all problems - will be populated as problems are added
PROBLEMS: list[ProblemMeta] = []


def register_problem(
    id: int | str | None = None,
    slug: str | None = None,
    title: str = "",
    category: Category | str | None = None,
    difficulty: Difficulty | str = "Medium",
    tags: list[str] | None = None,
    url: str | None = None,
    notes: str | None = None,
    # Support legacy parameter names
    module_path: str | None = None,
    has_solution: bool | None = None,
    **kwargs,
) -> ProblemMeta:
    """Register a new problem in the registry."""
    # Handle legacy/inconsistent parameter formats
    if slug is None:
        # Extract slug from title or module_path if not provided
        if title:
            slug = title.lower().replace(" ", "_").replace("-", "_")
            slug = "".join(c for c in slug if c.isalnum() or c == "_")
        elif module_path:
            slug = module_path.split(".")[-1]
        else:
            raise ValueError("Must provide either slug, title, or module_path")

    # Convert string category to enum
    if isinstance(category, str):
        # Handle different string formats
        category_map = {
            "Binary Search": Category.BINARY_SEARCH,
            "binary_search": Category.BINARY_SEARCH,
            "Trees": Category.TREES,
            "trees": Category.TREES,
            "Linked List": Category.LINKED_LIST,
            "linked_list": Category.LINKED_LIST,
            "Stack": Category.STACK,
            "stack": Category.STACK,
            "Arrays & Hashing": Category.ARRAYS_HASHING,
            "arrays_hashing": Category.ARRAYS_HASHING,
            "Two Pointers": Category.TWO_POINTERS,
            "two_pointers": Category.TWO_POINTERS,
            "Sliding Window": Category.SLIDING_WINDOW,
            "sliding_window": Category.SLIDING_WINDOW,
        }
        category = category_map.get(category, Category.ARRAYS_HASHING)

    # Convert string difficulty to enum
    if isinstance(difficulty, str):
        difficulty_map = {
            "Easy": Difficulty.EASY,
            "Medium": Difficulty.MEDIUM,
            "Hard": Difficulty.HARD,
        }
        difficulty = difficulty_map.get(difficulty, Difficulty.MEDIUM)

    # Convert string id to int
    if isinstance(id, str):
        try:
            id = int(id)
        except ValueError:
            id = None

    # Default tags if not provided
    if tags is None:
        tags = []

    # Generate module path if not provided
    if category:
        auto_module_path = f"interview_workbook.leetcode.{category.value}.{slug}"
    else:
        auto_module_path = module_path or f"interview_workbook.leetcode.unknown.{slug}"

    problem: ProblemMeta = {
        "id": id,
        "slug": slug,
        "title": title,
        "category": category or Category.ARRAYS_HASHING,
        "difficulty": difficulty,
        "tags": tags,
        "module": auto_module_path,
        "url": url,
        "notes": notes,
    }

    PROBLEMS.append(problem)
    return problem


def get_all() -> list[ProblemMeta]:
    """Get all registered problems."""
    return PROBLEMS.copy()


def by_category(category: Category) -> list[ProblemMeta]:
    """Get all problems in a specific category."""
    return [p for p in PROBLEMS if p["category"] == category]


def by_slug(slug: str) -> ProblemMeta | None:
    """Get a problem by its slug identifier."""
    for problem in PROBLEMS:
        if problem["slug"] == slug:
            return problem
    return None


def by_difficulty(difficulty: Difficulty) -> list[ProblemMeta]:
    """Get all problems of a specific difficulty."""
    return [p for p in PROBLEMS if p["difficulty"] == difficulty]


def by_tag(tag: str) -> list[ProblemMeta]:
    """Get all problems containing a specific tag."""
    return [p for p in PROBLEMS if tag in p["tags"]]


def validate_registry() -> None:
    """
    Validate the problem registry for consistency.

    Checks:
    - All problems have unique slugs
    - Module paths match expected pattern
    - Category matches directory structure
    - Required fields are present

    Raises:
        ValueError: If validation fails
    """
    if not PROBLEMS:
        return  # Empty registry is valid during initial setup

    seen_slugs = set()
    seen_ids = set()

    for problem in PROBLEMS:
        # Check unique slugs
        if problem["slug"] in seen_slugs:
            raise ValueError(f"Duplicate slug: {problem['slug']}")
        seen_slugs.add(problem["slug"])

        # Check unique IDs (when present)
        if problem["id"] is not None:
            if problem["id"] in seen_ids:
                raise ValueError(f"Duplicate problem ID: {problem['id']}")
            seen_ids.add(problem["id"])

        # Check module path format
        expected_module = (
            f"interview_workbook.leetcode.{problem['category'].value}.{problem['slug']}"
        )
        if problem["module"] != expected_module:
            raise ValueError(
                f"Module path mismatch for {problem['slug']}: "
                f"expected {expected_module}, got {problem['module']}"
            )

        # Check required fields
        if not problem["slug"]:
            raise ValueError("Empty slug not allowed")
        if not problem["title"]:
            raise ValueError(f"Empty title for slug {problem['slug']}")

        # Check slug format (filesystem safe)
        if not problem["slug"].replace("_", "").replace("-", "").isalnum():
            raise ValueError(f"Invalid slug format: {problem['slug']}")


def get_categories() -> list[Category]:
    """Get all categories that have registered problems."""
    categories = {p["category"] for p in PROBLEMS}
    return sorted(categories, key=lambda c: c.value)


def get_stats() -> dict[str, Any]:
    """Get registry statistics."""
    if not PROBLEMS:
        return {"total": 0, "by_category": {}, "by_difficulty": {}}

    by_category = {}
    by_difficulty = {}

    for problem in PROBLEMS:
        # Count by category
        cat_name = problem["category"].value
        by_category[cat_name] = by_category.get(cat_name, 0) + 1

        # Count by difficulty
        diff_name = problem["difficulty"].value
        by_difficulty[diff_name] = by_difficulty.get(diff_name, 0) + 1

    return {
        "total": len(PROBLEMS),
        "by_category": by_category,
        "by_difficulty": by_difficulty,
    }
