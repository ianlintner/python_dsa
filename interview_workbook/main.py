import argparse
from importlib import import_module

# Demo registry - add entries as modules are implemented
DEMOS = {
    # Sorting algorithms
    "sorting.merge_sort": ("algorithms.sorting.merge_sort", "demo"),
    "sorting.quick_sort": ("algorithms.sorting.quick_sort", "demo"),
    "sorting.heap_sort": ("algorithms.sorting.heap_sort", "demo"),
    "sorting.non_comparison_sorts": ("algorithms.sorting.non_comparison_sorts", "demo"),

    # Searching algorithms
    "searching.binary_search": ("algorithms.searching.binary_search", "demo"),
    "searching.quickselect": ("algorithms.searching.quickselect", "demo"),
    "searching.advanced_search": ("algorithms.searching.advanced_search", "demo"),

    # Graph algorithms
    "graphs.dijkstra": ("graphs.dijkstra", "demo"),
    "graphs.bfs_dfs": ("graphs.bfs_dfs", "demo"),
    "graphs.topological_sort": ("graphs.topological_sort", "demo"),
    "graphs.bellman_ford": ("graphs.bellman_ford", "demo"),
    "graphs.floyd_warshall": ("graphs.floyd_warshall", "demo"),
    "graphs.mst": ("graphs.mst", "demo"),
    "graphs.a_star": ("graphs.a_star", "demo"),

    # Dynamic Programming
    "dp.fibonacci": ("dp.fibonacci", "demo"),
    "dp.coin_change": ("dp.coin_change", "demo"),
    "dp.longest_increasing_subsequence": ("dp.longest_increasing_subsequence", "demo"),
    "dp.knapsack": ("dp.knapsack", "demo"),
    "dp.edit_distance": ("dp.edit_distance", "demo"),
    "dp.bitmask_tsp": ("dp.bitmask_tsp", "demo"),

    # String algorithms
    "strings.kmp": ("strings.kmp", "demo"),
    "strings.rabin_karp": ("strings.rabin_karp", "demo"),
    "strings.z_algorithm": ("strings.z_algorithm", "demo"),
    "strings.manacher": ("strings.manacher", "demo"),
    "strings.suffix_array": ("strings.suffix_array", "demo"),

    # Patterns
    "patterns.sliding_window": ("patterns.sliding_window", "demo"),
    "patterns.monotonic_stack": ("patterns.monotonic_stack", "demo"),
    "patterns.backtracking": ("patterns.backtracking", "demo"),
    "patterns.meet_in_the_middle": ("patterns.meet_in_the_middle", "demo"),

    # Data structures
    "data_structures.union_find": ("data_structures.union_find", "demo"),
    "data_structures.trie": ("data_structures.trie", "demo"),
    "data_structures.lru_cache": ("data_structures.lru_cache", "demo"),
    "data_structures.lfu_cache": ("data_structures.lfu_cache", "demo"),
    "data_structures.fenwick_tree": ("data_structures.fenwick_tree", "demo"),
    "data_structures.segment_tree": ("data_structures.segment_tree", "demo"),

    # Systems / Streaming
    "systems.reservoir_sampling": ("systems.reservoir_sampling", "demo"),
    "systems.rate_limiter": ("systems.rate_limiter", "demo"),

    # Concurrency
    "concurrency.intro": ("concurrency.intro", "demo"),

    # Math / Number Theory
    "math.number_theory": ("math.number_theory", "demo"),
}

def list_demos():
    """List all available demos."""
    print("Available demos:")
    for k in sorted(DEMOS):
        print(f"  {k}")

def run_demo(key: str):
    """Run a specific demo by key."""
    if key not in DEMOS:
        print(f"Demo not found: {key}")
        print("Available demos:")
        list_demos()
        return
    mod_name, fn_name = DEMOS[key]
    # Try absolute import first (when executed from repo root),
    # then fallback to package-relative import (when executed inside the package dir).
    try:
        mod = import_module(f"interview_workbook.{mod_name}")
    except ImportError:
        try:
            mod = import_module(mod_name)
        except ImportError as e:
            print(f"Error importing module '{mod_name}': {e}")
            print("Tip: Run from the repository root, e.g., `python3 interview_workbook/main.py --demo ...`")
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
  python interview_workbook/main.py --list
  python interview_workbook/main.py --demo sorting.merge_sort
  python interview_workbook/main.py --demo graphs.dijkstra
        """
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
