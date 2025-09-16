import argparse
import re
from importlib import import_module
from pathlib import Path

# Demo registry - add entries as modules are implemented
DEMOS = {
    # Sorting algorithms
    "sorting.merge_sort": ("interview_workbook.algorithms.sorting.merge_sort", "demo"),
    "sorting.quick_sort": ("interview_workbook.algorithms.sorting.quick_sort", "demo"),
    "sorting.heap_sort": ("interview_workbook.algorithms.sorting.heap_sort", "demo"),
    "sorting.non_comparison_sorts": (
        "interview_workbook.algorithms.sorting.non_comparison_sorts",
        "demo",
    ),
    "sorting.insertion_sort": ("interview_workbook.algorithms.sorting.insertion_sort", "demo"),
    "sorting.selection_sort": ("interview_workbook.algorithms.sorting.selection_sort", "demo"),
    "sorting.bubble_sort": ("interview_workbook.algorithms.sorting.bubble_sort", "demo"),
    # Searching algorithms
    "searching.binary_search": ("interview_workbook.algorithms.searching.binary_search", "demo"),
    "searching.linear_search": ("interview_workbook.algorithms.searching.linear_search", "demo"),
    "searching.quickselect": ("interview_workbook.algorithms.searching.quickselect", "demo"),
    "searching.advanced_search": (
        "interview_workbook.algorithms.searching.advanced_search",
        "demo",
    ),
    # Graph algorithms
    "graphs.dijkstra": ("interview_workbook.graphs.dijkstra", "demo"),
    "graphs.bfs_dfs": ("interview_workbook.graphs.bfs_dfs", "demo"),
    "graphs.topological_sort": ("interview_workbook.graphs.topological_sort", "demo"),
    "graphs.bellman_ford": ("interview_workbook.graphs.bellman_ford", "demo"),
    "graphs.floyd_warshall": ("interview_workbook.graphs.floyd_warshall", "demo"),
    "graphs.mst": ("interview_workbook.graphs.mst", "demo"),
    "graphs.a_star": ("interview_workbook.graphs.a_star", "demo"),
    "graphs.scc": ("interview_workbook.graphs.scc", "demo"),
    # Dynamic Programming
    "dp.fibonacci": ("interview_workbook.dp.fibonacci", "demo"),
    "dp.coin_change": ("interview_workbook.dp.coin_change", "demo"),
    "dp.longest_increasing_subsequence": (
        "interview_workbook.dp.longest_increasing_subsequence",
        "demo",
    ),
    "dp.knapsack": ("interview_workbook.dp.knapsack", "demo"),
    "dp.edit_distance": ("interview_workbook.dp.edit_distance", "demo"),
    "dp.bitmask_tsp": ("interview_workbook.dp.bitmask_tsp", "demo"),
    "dp.state_compression_grid": ("interview_workbook.dp.state_compression_grid", "demo"),
    "dp.lcs": ("interview_workbook.dp.lcs", "demo"),
    # String algorithms
    "strings.kmp": ("interview_workbook.strings.kmp", "demo"),
    "strings.rabin_karp": ("interview_workbook.strings.rabin_karp", "demo"),
    "strings.z_algorithm": ("interview_workbook.strings.z_algorithm", "demo"),
    "strings.manacher": ("interview_workbook.strings.manacher", "demo"),
    "strings.suffix_array": ("interview_workbook.strings.suffix_array", "demo"),
    # Patterns
    "patterns.sliding_window": ("interview_workbook.patterns.sliding_window", "demo"),
    "patterns.monotonic_stack": ("interview_workbook.patterns.monotonic_stack", "demo"),
    "patterns.backtracking": ("interview_workbook.patterns.backtracking", "demo"),
    "patterns.meet_in_the_middle": ("interview_workbook.patterns.meet_in_the_middle", "demo"),
    "patterns.binary_search_on_answer": (
        "interview_workbook.patterns.binary_search_on_answer",
        "demo",
    ),
    "patterns.two_pointers": ("interview_workbook.patterns.two_pointers", "demo"),
    # Data structures
    "data_structures.union_find": ("interview_workbook.data_structures.union_find", "demo"),
    "data_structures.trie": ("interview_workbook.data_structures.trie", "demo"),
    "data_structures.lru_cache": ("interview_workbook.data_structures.lru_cache", "demo"),
    "data_structures.lfu_cache": ("interview_workbook.data_structures.lfu_cache", "demo"),
    "data_structures.fenwick_tree": ("interview_workbook.data_structures.fenwick_tree", "demo"),
    "data_structures.segment_tree": ("interview_workbook.data_structures.segment_tree", "demo"),
    "data_structures.heap_patterns": ("interview_workbook.data_structures.heap_patterns", "demo"),
    # Systems / Streaming
    "systems.reservoir_sampling": ("interview_workbook.systems.reservoir_sampling", "demo"),
    "systems.rate_limiter": ("interview_workbook.systems.rate_limiter", "demo"),
    "systems.sharded_bfs": ("interview_workbook.systems.sharded_bfs", "demo"),
    "systems.consensus_basics": ("interview_workbook.systems.consensus_basics", "demo"),
    # Concurrency
    "concurrency.intro": ("interview_workbook.concurrency.intro", "demo"),
    # Math / Number Theory
    "math.number_theory": ("interview_workbook.math_utils.number_theory", "demo"),
}


def discover_demos() -> dict[str, tuple[str, str]]:
    """
    Discover modules under src/ that expose a callable `demo()` function.
    Returns a mapping: demo_key -> (module_name, function_name).
    """
    discovered = {}
    src_dir = Path(__file__).parent  # Should be src/

    for path in src_dir.rglob("*.py"):
        if path.name == "__init__.py":
            continue

        # Get relative path from src/
        try:
            rel = path.relative_to(src_dir)
        except ValueError:
            continue  # Skip files outside src/

        # Convert path to module name
        module_name = ".".join(rel.with_suffix("").parts)

        # Read file and check for demo() function
        try:
            src_text = path.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue

        # Look for def demo( pattern
        if re.search(r"^\s*def\s+demo\s*\(", src_text, flags=re.M):
            # Create demo key based on module path
            # Convert interview_workbook.leetcode.arrays_hashing.two_sum -> leetcode.arrays_hashing.two_sum
            if module_name.startswith("interview_workbook."):
                demo_key = module_name[len("interview_workbook.") :]
            else:
                demo_key = module_name

            discovered[demo_key] = (module_name, "demo")

    return discovered


def get_all_demos() -> dict[str, tuple[str, str]]:
    """Get combined static and dynamically discovered demos."""
    return discover_demos()


def list_demos():
    """List all available demos."""
    all_demos = get_all_demos()
    print("Available demos:")

    # Group demos by category for better organization
    categories = {}
    for key in all_demos:
        if "." in key:
            category = key.split(".")[0]
        else:
            category = "misc"
        categories.setdefault(category, []).append(key)

    for category in sorted(categories):
        print(f"\n  {category}:")
        for demo_key in sorted(categories[category]):
            print(f"    {demo_key}")


def run_demo(key: str):
    """Run a specific demo by key."""
    all_demos = get_all_demos()
    if key not in all_demos:
        print(f"Demo not found: {key}")
        print("Available demos:")
        list_demos()
        return
    mod_name, fn_name = all_demos[key]
    # Try absolute import first (when executed from repo root),
    # then fallback to package-relative import (when executed inside the package dir).
    try:
        # Prefer plain imports with src/ layout
        mod = import_module(mod_name)
    except ImportError:
        try:
            # Fallback for legacy package layout
            mod = import_module(f"interview_workbook.{mod_name}")
        except ImportError as e:
            print(f"Error importing module '{mod_name}': {e}")
            print(
                "Tip: Run from the repository root, e.g., `python3 src/main.py --demo ...` or ensure PYTHONPATH includes ./src"
            )
            return
    try:
        demo_fn = getattr(mod, fn_name)
    except AttributeError:
        print(f"Module '{mod_name}' has no function '{fn_name}'")
        return
    print(f"\n=== Running {key} demo ===")
    demo_fn()


def main():
    parser = argparse.ArgumentParser(
        description="Python Interview Algorithms Workbook",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python src/main.py --list
  python src/main.py --demo sorting.merge_sort
  python src/main.py --demo graphs.dijkstra
        """,
    )
    parser.add_argument("--list", action="store_true", help="List available demos")
    parser.add_argument("--demo", type=str, help="Run a specific demo")

    args = parser.parse_args()

    if args.list:
        list_demos()
        return

    if args.demo:
        run_demo(args.demo)
        return

    parser.print_help()


if __name__ == "__main__":
    main()
