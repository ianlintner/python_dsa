"""
LeetCode Top 100 audit and documentation generator.

This module compares the Top 100 manifest with currently registered problems
and generates updated documentation that reflects the actual implementation status.
"""

from pathlib import Path
from typing import Dict, List, Set, Tuple

from ._discovery import discover_problem_modules, ensure_problems_loaded, get_registered_slugs
from ._registry import get_all, get_stats
from ._types import Category
from .top100_manifest import TOP_100_MANIFEST, get_category_stats, get_problems_by_category


def audit_implementation_status() -> Dict[str, any]:
    """
    Audit current implementation status against the Top 100 manifest.
    
    Returns:
        Dict with implementation status, missing problems, etc.
    """
    ensure_problems_loaded()
    
    # Get registered problems
    registered = get_registered_slugs()
    
    # Get manifest problems
    manifest_slugs = {p["slug"] for p in TOP_100_MANIFEST}
    
    # Calculate status
    implemented = registered & manifest_slugs
    missing = manifest_slugs - registered
    extra = registered - manifest_slugs  # Problems implemented but not in Top 100
    
    # Get detailed info
    manifest_by_slug = {p["slug"]: p for p in TOP_100_MANIFEST}
    registered_problems = {p["slug"]: p for p in get_all()}
    
    # Group by category
    implemented_by_category = {}
    missing_by_category = {}
    
    for category in Category:
        cat_name = category.value
        manifest_problems = get_problems_by_category(category)
        manifest_category_slugs = {p["slug"] for p in manifest_problems}
        
        impl_in_cat = implemented & manifest_category_slugs
        missing_in_cat = missing & manifest_category_slugs
        
        implemented_by_category[cat_name] = sorted(impl_in_cat)
        missing_by_category[cat_name] = sorted(missing_in_cat)
    
    return {
        "total_manifest": len(manifest_slugs),
        "total_implemented": len(implemented),
        "total_missing": len(missing),
        "total_extra": len(extra),
        "implemented_slugs": sorted(implemented),
        "missing_slugs": sorted(missing),
        "extra_slugs": sorted(extra),
        "implemented_by_category": implemented_by_category,
        "missing_by_category": missing_by_category,
        "manifest_by_slug": manifest_by_slug,
        "registered_by_slug": registered_problems,
        "category_stats": get_category_stats(),
        "discovered_modules": discover_problem_modules(),
    }


def generate_category_section(category: Category, audit_data: Dict) -> str:
    """Generate markdown section for a category."""
    cat_name = category.value
    problems = get_problems_by_category(category)
    implemented = set(audit_data["implemented_by_category"][cat_name])
    
    # Category header with count
    total_in_category = len(problems)
    impl_in_category = len(implemented)
    
    # Convert category name to display name
    display_name = cat_name.replace("_", " ").title()
    if display_name == "Arrays Hashing":
        display_name = "Arrays & Hashing"
    elif display_name == "Two Pointers":
        display_name = "Two Pointers"
    elif display_name == "Dp 1D":
        display_name = "1-D DP"
    elif display_name == "Dp 2D":
        display_name = "2-D DP"
    elif display_name == "Bit Manip":
        display_name = "Bit Manipulation"
    elif display_name == "Math Geometry":
        display_name = "Math & Geometry"
    
    lines = [
        f"### {display_name} ({impl_in_category}/{total_in_category} problems)",
    ]
    
    # Add category description based on category
    descriptions = {
        Category.ARRAYS_HASHING: "Focus on array manipulation and hash table usage patterns.",
        Category.TWO_POINTERS: "Problems solved using two-pointer technique with opposite or same direction pointers.",
        Category.SLIDING_WINDOW: "Problems using sliding window technique with fixed or variable window sizes.",
        Category.STACK: "Problems utilizing stack data structure for parsing, validation, and computation.",
        Category.BINARY_SEARCH: "Classic binary search and its variations on sorted arrays and search spaces.",
        Category.LINKED_LIST: "Fundamental linked list manipulation patterns and algorithms.",
        Category.TREES: "Binary tree traversal, validation, and manipulation algorithms.",
        Category.TRIES: "Prefix tree (trie) data structure implementation and applications.",
        Category.HEAP: "Priority queue and heap-based algorithms for optimization problems.",
        Category.BACKTRACKING: "Recursive backtracking for combinatorial search problems.",
        Category.GRAPHS: "Graph traversal, topological sorting, and connectivity algorithms.",
        Category.INTERVALS: "Interval merging, scheduling, and overlap detection problems.",
        Category.GREEDY: "Greedy algorithmic approaches for optimization problems.",
        Category.DP_1D: "One-dimensional dynamic programming patterns.",
        Category.DP_2D: "Two-dimensional dynamic programming for grid and string problems.",
        Category.BIT_MANIP: "Bitwise operations and bit manipulation techniques.",
        Category.MATH_GEOMETRY: "Mathematical algorithms and geometric problems.",
    }
    
    if category in descriptions:
        lines.append(descriptions[category])
        lines.append("")
    
    # Separate implemented and planned
    implemented_problems = [p for p in problems if p["slug"] in implemented]
    missing_problems = [p for p in problems if p["slug"] not in implemented]
    
    if implemented_problems:
        lines.append("**Implemented:**")
        for prob in implemented_problems:
            lines.append(f'- [x] `{prob["slug"]}` - {prob["title"]} ({prob["difficulty"].value})')
        lines.append("")
    
    if missing_problems:
        lines.append("**Planned:**")
        for prob in missing_problems:
            lines.append(f'- [ ] `{prob["slug"]}` - {prob["title"]} ({prob["difficulty"].value})')
        lines.append("")
    
    return "\n".join(lines)


def generate_neetcode_docs(audit_data: Dict) -> str:
    """Generate the complete NEETCODE_TOP100.md content."""
    
    total = audit_data["total_manifest"]
    implemented = audit_data["total_implemented"]
    
    content = f"""# NeetCode Top 100 LeetCode Problems

This document provides an index of the curated NeetCode Top 100 problems implemented in this repository.

## Overview

The LeetCode problem collection is organized into 17 categories based on algorithmic patterns. Each problem includes:

- **Solution class** with canonical method signatures
- **Comprehensive test cases** with edge cases
- **Demo function** for CLI and Flask integration
- **Educational content** including complexity analysis, pitfalls, and follow-ups
- **Problem metadata** with difficulty, tags, and LeetCode links

## Access Methods

### CLI
```bash
python3 src/main.py --list                    # List all available demos
python3 src/main.py --demo leetcode.arrays_hashing.two_sum
```

### Flask Web Interface
```bash
python3 -m flask --app flask_app.app run
```
Then navigate to http://localhost:5000 to explore problems interactively.

### Python API
```python
from interview_workbook.leetcode import get_all, by_category
from interview_workbook.leetcode._types import Category

# Get all problems
problems = get_all()

# Get problems by category
arrays_problems = by_category(Category.ARRAYS_HASHING)
```

## Problem Categories

"""

    # Generate each category section
    for category in Category:
        content += generate_category_section(category, audit_data)
        content += "\n"
    
    # Implementation status
    content += f"""## Implementation Status

**Progress:** {implemented}/{total} problems implemented ({implemented/total*100:.1f}%)

"""
    
    # Category breakdown
    content += "**By Category:**\n"
    for category in Category:
        cat_name = category.value
        cat_total = len(get_problems_by_category(category))
        cat_impl = len(audit_data["implemented_by_category"][cat_name])
        cat_pct = (cat_impl / cat_total * 100) if cat_total > 0 else 0
        
        display_name = cat_name.replace("_", " ").title()
        if display_name == "Arrays Hashing":
            display_name = "Arrays & Hashing"
        elif display_name == "Dp 1D":
            display_name = "1-D DP"
        elif display_name == "Dp 2D":
            display_name = "2-D DP"
        elif display_name == "Bit Manip":
            display_name = "Bit Manipulation"
        elif display_name == "Math Geometry":
            display_name = "Math & Geometry"
            
        content += f"- {display_name}: {cat_impl}/{cat_total} ({cat_pct:.0f}%)\n"
    
    content += f"""

## Technical Architecture

### Registry System
All problems are registered in a central registry with metadata including:
- Problem ID and LeetCode URL
- Category and difficulty classification
- Tags for algorithmic patterns
- Module path for dynamic import

### Testing Framework
Each problem includes:
- Unit tests for Solution class methods
- Test cases covering edge cases and examples
- Integration tests for demo functions
- Registry validation tests

### Discovery System
Both CLI and Flask automatically discover new problems through:
- File system scanning for `demo()` functions
- Dynamic module import and execution
- Category-based organization and filtering

## Contributing

To add a new problem:

1. Create the problem module in the appropriate category directory
2. Implement the `Solution` class with canonical method signatures
3. Add comprehensive test cases and a `demo()` function
4. Register the problem using `register_problem()`
5. The problem will automatically appear in CLI and Flask interfaces

See existing implementations for examples and patterns to follow.

---
*This document is auto-generated from the manifest and current implementations.*
*Last updated: {audit_data["total_implemented"]}/{audit_data["total_manifest"]} problems implemented*
"""
    
    return content


def run_audit() -> Dict:
    """Run audit and return results."""
    return audit_implementation_status()


def generate_docs() -> str:
    """Generate documentation based on current audit."""
    audit_data = run_audit()
    return generate_neetcode_docs(audit_data)


def update_docs_file() -> bool:
    """Update the docs/NEETCODE_TOP100.md file."""
    try:
        docs_path = Path("docs/NEETCODE_TOP100.md")
        new_content = generate_docs()
        
        # Write new content
        docs_path.write_text(new_content, encoding="utf-8")
        return True
    except Exception as e:
        print(f"Failed to update docs: {e}")
        return False


def print_audit_summary(audit_data: Dict = None) -> None:
    """Print a summary of the audit results."""
    if audit_data is None:
        audit_data = run_audit()
    
    total = audit_data["total_manifest"]
    impl = audit_data["total_implemented"]
    missing = audit_data["total_missing"]
    
    print(f"🎯 NeetCode Top 100 Implementation Status")
    print(f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print(f"📊 Progress: {impl}/{total} ({impl/total*100:.1f}%)")
    print(f"✅ Implemented: {impl}")
    print(f"❌ Missing: {missing}")
    
    if audit_data["extra_slugs"]:
        print(f"➕ Extra: {len(audit_data['extra_slugs'])}")
    
    print(f"\n📁 Discovered modules: {len(audit_data['discovered_modules'])}")
    
    if missing > 0:
        print(f"\n🔍 Next to implement:")
        for i, slug in enumerate(sorted(audit_data["missing_slugs"])[:5]):
            prob = audit_data["manifest_by_slug"][slug]
            print(f"   {i+1}. {slug} ({prob['difficulty'].value})")
        if missing > 5:
            print(f"   ... and {missing-5} more")


if __name__ == "__main__":
    # Run audit when called directly
    audit_data = run_audit()
    print_audit_summary(audit_data)
