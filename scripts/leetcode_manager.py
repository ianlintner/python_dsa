#!/usr/bin/env python3
"""
LeetCode Top 100 Management CLI

This script provides utilities for managing the LeetCode Top 100 implementation:
- Audit current status
- Update documentation
- Scaffold new problems
- Fix slug mismatches
"""

import argparse
import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from interview_workbook.leetcode._audit import (
    run_audit,
    print_audit_summary,
    update_docs_file,
    generate_docs,
)
from interview_workbook.leetcode.top100_manifest import (
    TOP_100_MANIFEST,
    get_problem_by_slug,
    get_problems_by_category,
)
from interview_workbook.leetcode._discovery import (
    discover_problem_modules,
    get_registered_slugs,
    ensure_problems_loaded,
)
from interview_workbook.leetcode._types import Category, Difficulty


def cmd_audit(args):
    """Run audit and print summary."""
    print_audit_summary()


def cmd_update_docs(args):
    """Update the documentation file."""
    success = update_docs_file()
    if success:
        print("✅ Documentation updated successfully!")
    else:
        print("❌ Failed to update documentation!")
        sys.exit(1)


def cmd_scaffold(args):
    """Scaffold a new problem."""
    slug = args.slug

    # Find problem in manifest
    problem = get_problem_by_slug(slug)
    if not problem:
        print(f"❌ Problem '{slug}' not found in Top 100 manifest")
        sys.exit(1)

    category = problem["category"]
    difficulty = problem["difficulty"]
    title = problem["title"]
    url = problem["url"]
    tags = problem["tags"]

    # Generate the problem module
    module_content = generate_problem_template(
        slug=slug,
        title=title,
        category=category,
        difficulty=difficulty,
        url=url,
        tags=tags,
        problem_id=problem.get("id"),
    )

    # Create the file
    category_dir = Path("src/interview_workbook/leetcode") / category.value
    category_dir.mkdir(parents=True, exist_ok=True)

    problem_file = category_dir / f"{slug}.py"
    if problem_file.exists() and not args.force:
        print(f"❌ File {problem_file} already exists! Use --force to overwrite.")
        sys.exit(1)

    problem_file.write_text(module_content)
    print(f"✅ Created {problem_file}")

    # Generate test file
    test_content = generate_test_template(slug, title, category)
    test_file = Path("tests") / f"test_leetcode_{slug}.py"

    if not test_file.exists() or args.force:
        test_file.write_text(test_content)
        print(f"✅ Created {test_file}")


def cmd_list_missing(args):
    """List missing problems by category."""
    audit_data = run_audit()

    if args.category:
        try:
            cat = Category(args.category)
            missing = audit_data["missing_by_category"][cat.value]
            if missing:
                print(f"Missing problems in {cat.value}:")
                for slug in missing:
                    prob = audit_data["manifest_by_slug"][slug]
                    print(f"  - {slug} ({prob['difficulty'].value}) - {prob['title']}")
            else:
                print(f"✅ All problems implemented in {cat.value}")
        except ValueError:
            print(f"❌ Invalid category: {args.category}")
            print(f"Available categories: {[c.value for c in Category]}")
    else:
        print("Missing problems by category:")
        for category in Category:
            cat_name = category.value
            missing = audit_data["missing_by_category"][cat_name]
            if missing:
                print(f"\n{cat_name} ({len(missing)} missing):")
                for slug in missing[:5]:  # Show first 5
                    prob = audit_data["manifest_by_slug"][slug]
                    print(f"  - {slug} ({prob['difficulty'].value})")
                if len(missing) > 5:
                    print(f"  ... and {len(missing) - 5} more")


def cmd_fix_slugs(args):
    """Fix slug mismatches between registered and manifest."""
    audit_data = run_audit()

    # Find problems that might have slug mismatches
    registered = set(audit_data["registered_by_slug"].keys())
    manifest_slugs = set(p["slug"] for p in TOP_100_MANIFEST)

    # Look for potential matches (convert hyphens to underscores)
    potential_fixes = {}
    for reg_slug in registered:
        if reg_slug not in manifest_slugs:
            # Try converting hyphens to underscores
            fixed_slug = reg_slug.replace("-", "_")
            if fixed_slug in manifest_slugs:
                potential_fixes[reg_slug] = fixed_slug

    if not potential_fixes:
        print("✅ No obvious slug mismatches found!")
        return

    print("Found potential slug mismatches:")
    for old_slug, new_slug in potential_fixes.items():
        print(f"  {old_slug} -> {new_slug}")

    if not args.dry_run:
        print("\n⚠️  This would require manual file renaming and slug updates.")
        print("Use --dry-run to see what would be changed without making changes.")


def generate_problem_template(slug, title, category, difficulty, url, tags, problem_id=None):
    """Generate a problem module template."""

    # Create the problem description template
    tags_str = ", ".join(tags)
    id_comment = f"LeetCode {problem_id}: " if problem_id else ""

    template = f'''"""
{id_comment}{title}

[Problem description would go here - copy from LeetCode]

URL: {url}
Difficulty: {difficulty.value}
Category: {category.value.replace("_", " ").title()}

Patterns:
- [Pattern 1]
- [Pattern 2]

Complexity:
- Time: O(?)
- Space: O(?)

Pitfalls:
- [Pitfall 1]
- [Pitfall 2]

Follow-ups:
- [Follow-up question 1]
- [Follow-up question 2]
"""

from interview_workbook.leetcode._registry import register_problem
from interview_workbook.leetcode._runner import TestCase, create_demo_output, run_test_cases
from interview_workbook.leetcode._types import Category, Difficulty


class Solution:
    def placeholder_method(self, param: int) -> int:
        """
        [Method description]
        
        Args:
            param: [Parameter description]
            
        Returns:
            [Return value description]
        """
        # TODO: Implement solution
        pass


# Test cases
test_cases = [
    TestCase((0,), 0, "Example case 1"),
    TestCase((1,), 1, "Example case 2"),
    # TODO: Add more test cases
]


def demo() -> str:
    """Run {title} demo with test cases."""
    solution = Solution()

    test_results = run_test_cases(solution.placeholder_method, test_cases, "{id_comment}{title}")

    return create_demo_output(
        "{title}",
        test_results,
        time_complexity="O(?)",
        space_complexity="O(?)",
        approach_notes="""
Key insights:
1. [Insight 1]
2. [Insight 2]
3. [Insight 3]
        """.strip(),
    )


# Register the problem
register_problem(
    id={problem_id if problem_id else "None"},
    slug="{slug}",
    title="{title}",
    category=Category.{category.name},
    difficulty=Difficulty.{difficulty.name},
    tags={tags},
    url="{url}",
    notes="TODO: Add implementation notes",
)
'''

    return template


def generate_test_template(slug, title, category):
    """Generate a test file template."""

    module_path = f"interview_workbook.leetcode.{category.value}.{slug}"

    template = f'''"""
Tests for {title}
"""

import pytest
from src.{module_path.replace(".", "/")} import Solution


class TestSolution:
    def test_example_cases(self):
        """Test with provided examples."""
        solution = Solution()
        
        # TODO: Add test cases
        # Example:
        # assert solution.method_name(input) == expected_output
        pass
    
    def test_edge_cases(self):
        """Test edge cases."""
        solution = Solution()
        
        # TODO: Add edge case tests
        pass
    
    def test_large_input(self):
        """Test with larger inputs."""
        solution = Solution()
        
        # TODO: Add performance tests if needed
        pass
'''

    return template


def main():
    parser = argparse.ArgumentParser(description="LeetCode Top 100 Management CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Audit command
    audit_parser = subparsers.add_parser("audit", help="Run audit and show status")
    audit_parser.set_defaults(func=cmd_audit)

    # Update docs command
    docs_parser = subparsers.add_parser("update-docs", help="Update documentation")
    docs_parser.set_defaults(func=cmd_update_docs)

    # Scaffold command
    scaffold_parser = subparsers.add_parser("scaffold", help="Create new problem scaffold")
    scaffold_parser.add_argument("slug", help="Problem slug (e.g. 'two_sum')")
    scaffold_parser.add_argument("--force", action="store_true", help="Overwrite existing files")
    scaffold_parser.set_defaults(func=cmd_scaffold)

    # List missing command
    missing_parser = subparsers.add_parser("list-missing", help="List missing problems")
    missing_parser.add_argument("--category", help="Filter by category")
    missing_parser.set_defaults(func=cmd_list_missing)

    # Fix slugs command
    fix_parser = subparsers.add_parser("fix-slugs", help="Fix slug mismatches")
    fix_parser.add_argument("--dry-run", action="store_true", help="Show what would be changed")
    fix_parser.set_defaults(func=cmd_fix_slugs)

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    args.func(args)


if __name__ == "__main__":
    main()
