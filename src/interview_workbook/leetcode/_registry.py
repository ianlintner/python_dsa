"""
 Registry

TODO: Add problem description
"""


from .top100_manifest import TOP_100_MANIFEST


# Exported constant for tests
# Augment each entry with a "module" key so metadata is consistent
PROBLEMS: list[dict] = [
    {**p, "module": f"interview_workbook.leetcode.{p['slug']}", "notes": p.get("notes", "")}
    for p in TOP_100_MANIFEST
]

def register_problem(**kwargs) -> None:
    """Register an additional problem not in the TOP_100_MANIFEST (used by modules)."""
    PROBLEMS.append(kwargs)


def by_category(category: str) -> list[dict]:
    """Return problems filtered by the given category."""
    return [p for p in PROBLEMS if p["category"].value == category]


from typing import Optional

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
