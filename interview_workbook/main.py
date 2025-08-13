import argparse
from importlib import import_module

# Demo registry - add entries as modules are implemented
DEMOS = {
    "sorting.merge_sort": ("algorithms.sorting.merge_sort", "demo"),
    "sorting.quick_sort": ("algorithms.sorting.quick_sort", "demo"),
    "sorting.heap_sort": ("algorithms.sorting.heap_sort", "demo"),
    "searching.binary_search": ("algorithms.searching.binary_search", "demo"),
    "searching.quickselect": ("algorithms.searching.quickselect", "demo"),
    "graphs.dijkstra": ("graphs.dijkstra", "demo"),
    "graphs.bfs_dfs": ("graphs.bfs_dfs", "demo"),
    "graphs.topological_sort": ("graphs.topological_sort", "demo"),
    "dp.fibonacci": ("dp.fibonacci", "demo"),
    "dp.coin_change": ("dp.coin_change", "demo"),
    "dp.longest_increasing_subsequence": ("dp.longest_increasing_subsequence", "demo"),
    "dp.knapsack": ("dp.knapsack", "demo"),
    "dp.edit_distance": ("dp.edit_distance", "demo"),
    "strings.kmp": ("strings.kmp", "demo"),
    "data_structures.union_find": ("data_structures.union_find", "demo"),
    "data_structures.trie": ("data_structures.trie", "demo"),
    "data_structures.lru_cache": ("data_structures.lru_cache", "demo"),
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
    
    try:
        mod_name, fn_name = DEMOS[key]
        mod = import_module(f"interview_workbook.{mod_name}")
        demo_fn = getattr(mod, fn_name)
        print(f"\n=== Running {key} demo ===")
        demo_fn()
    except (ImportError, AttributeError) as e:
        print(f"Error running demo {key}: {e}")
        print("This module may not be implemented yet.")

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
