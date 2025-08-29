"""
 Registry

TODO: Add problem description
"""

from typing import Optional

from .top100_manifest import TOP_100_MANIFEST

# Exported constant for tests
# Augment each entry with a "module" key so metadata is consistent
PROBLEMS: list[dict] = []
for p in TOP_100_MANIFEST:
    category = p["category"].value if hasattr(p["category"], "value") else str(p["category"])
    module = f"interview_workbook.leetcode.{category}.{p['slug']}"
    PROBLEMS.append({**p, "module": module, "notes": p.get("notes", "")})


def register_problem(**kwargs) -> None:
    """Register an additional problem not in the TOP_100_MANIFEST (used by modules)."""
    category = (
        kwargs["category"].value
        if hasattr(kwargs["category"], "value")
        else str(kwargs["category"])
    )
    module = f"interview_workbook.leetcode.{category}.{kwargs['slug']}"
    new_entry = {**kwargs, "module": module, "notes": kwargs.get("notes", "")}
    # prevent duplicate slugs or ids
    slugs = [p["slug"] for p in PROBLEMS]
    ids = [p["id"] for p in PROBLEMS]
    if new_entry["slug"] in slugs or new_entry["id"] in ids:
        return
    PROBLEMS.append(new_entry)


def by_category(category) -> list[dict]:
    """Return problems filtered by the given category.
    Accepts either a Category enum or its string value."""
    cat_value = category.value if hasattr(category, "value") else str(category)
    return [p for p in PROBLEMS if p["category"].value == cat_value]


def by_slug(slug: str) -> Optional[dict]:
    """Return a problem by slug, or None if not found."""
    for p in PROBLEMS:
        if p["slug"] == slug:
            return p
    return None


def get_all() -> list[dict]:
    """Return a shallow copy of all problems in the manifest (with module metadata)."""
    return PROBLEMS.copy()


def validate_registry() -> bool:
    """Validate that all problems have unique slugs and are consistent."""
    slugs = [p["slug"] for p in PROBLEMS]
    return len(slugs) == len(set(slugs))


def get_stats() -> dict:
    """Return statistics about the problem manifest grouped by category and difficulty."""
    stats = {
        "total": len(PROBLEMS),
        "by_category": {},
        "by_difficulty": {},
    }
    for p in PROBLEMS:
        cat = p["category"].value
        diff = p["difficulty"].value
        stats["by_category"][cat] = stats["by_category"].get(cat, 0) + 1
        stats["by_difficulty"][diff] = stats["by_difficulty"].get(diff, 0) + 1
    return stats
