from __future__ import annotations

import importlib
import io
import sys
import traceback
from functools import lru_cache
from pathlib import Path

from flask import Flask, abort, jsonify, redirect, render_template, request, url_for

# Ensure we can import project packages (flask_app) and modules from src/
ROOT_DIR = Path(__file__).resolve().parents[1]
SRC_DIR = ROOT_DIR / "src"
# Add project root for absolute imports like "flask_app.*" when running this file directly
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))
# Add src for discovered demo modules under "src/"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))


app = Flask(__name__, template_folder="templates", static_folder="static")

# Central notes database for algorithm modules (keyed by full module name or basename)
MODULE_NOTES: dict[str, str] = {
    # Sorting
    "bubble_sort": """Summary: Repeatedly swap adjacent out-of-order pairs; pushes largest to the end each pass.
Time: Best O(n) (already sorted + early exit), Avg O(n^2), Worst O(n^2)
Space: O(1) in-place
Stability: Stable
When to use: Teaching, tiny inputs, nearly-sorted with early exit.
""",
    "selection_sort": """Summary: Repeatedly select min element and place it at the front.
Time: Best/Avg/Worst O(n^2)
Space: O(1) in-place
Stability: Not stable (simple implementations)
When to use: Tiny inputs, minimal swaps needed situations.
""",
    "insertion_sort": """Summary: Build sorted prefix by inserting each element into position.
Time: Best O(n), Avg/Worst O(n^2)
Space: O(1) in-place
Stability: Stable
When to use: Nearly sorted data, small arrays, as base-case for hybrid sorts.
""",
    "merge_sort": """Summary: Divide-and-conquer; recursively sort halves then merge.
Time: Best/Avg/Worst O(n log n)
Space: O(n) auxiliary (linked-list variant can be O(1))
Stability: Stable
When to use: Guaranteed O(n log n), external sorting, stable requirement.
""",
    "quick_sort": """Summary: Partition around a pivot; recursively sort partitions.
Time: Best/Avg O(n log n), Worst O(n^2) (poor pivots)
Space: O(log n) average stack, O(n) worst stack
Stability: Not stable (typical in-place)
Notes: Use randomized/median-of-three pivot; switch to insertion sort for small slices.
""",
    "heap_sort": """Summary: Build max-heap, repeatedly extract max to end.
Time: Best/Avg/Worst O(n log n)
Space: O(1) in-place (array heap)
Stability: Not stable
When to use: O(1) extra memory requirement with predictable O(n log n).
""",
    # Searching / selection
    "linear_search": """Summary: Scan sequentially until element found or end.
Time: Best O(1), Avg/Worst O(n)
Space: O(1)
When to use: Unsorted data, tiny inputs.
""",
    "binary_search": """Summary: Repeatedly halve search interval in sorted data.
Time: O(log n)
Space: O(1) iterative, O(log n) recursive
Requires: Monotonic/sorted sequence, random access preferred.
""",
    "quickselect": """Summary: Partition (QuickSort-style) to find k-th statistic.
Time: Avg O(n), Worst O(n^2)
Space: O(1) extra; recursion stack O(log n) avg
Tip: Randomized pivots reduce worst-case likelihood. Median-of-medians -> O(n) worst-case.
""",
    # Graphs
    "bfs_dfs": """Summary: BFS explores by levels; DFS dives deep along a branch.
BFS Time: O(V+E), Space: O(V) queue; shortest paths in unweighted graphs.
DFS Time: O(V+E), Space: O(V) stack; useful for cycles, topological order, components.
""",
    "dijkstra": """Summary: Single-source shortest paths on non-negative weights.
Time: O((V+E) log V) with binary heap; O(V^2) with adjacency matrix
Space: O(V)
Requires: Non-negative edge weights. For negatives, use Bellman-Ford.
""",
    "scc": """Summary: Strongly Connected Components (Kosaraju/Tarjan).
Time: O(V+E)
Space: O(V)
Use: Collapse SCCs to DAG, reasoning about cycles and components.
""",
    "a_star": """Summary: A* search using f(n)=g(n)+h(n) with admissible heuristic.
Time: Depends on heuristic; up to O(b^d) worst-case
Space: O(b^d) for open/closed sets
Notes: Admissible and consistent heuristics ensure optimality; common h: Manhattan/Euclidean.
""",
    "gbfs": """Summary: Greedy Best-First expands node with lowest heuristic h(n).
Time: Up to O(b^d)
Space: O(b^d)
Notes: Not optimal, can get stuck; fast with informative heuristics.
""",
    "kruskal": """Summary: Sort edges by weight; add if it doesn't form a cycle (Union-Find).
Time: O(E log E) ≈ O(E log V)
Space: O(V)
Use: Sparse graphs; simple with DSU for cycle detection.
""",
    "prim": """Summary: Grow MST from a start node using PQ of crossing edges.
Time: O(E log V) with binary heap; O(E + V log V) with Fibonacci heap
Space: O(V)
Use: Dense graphs or adjacency matrices; complements Kruskal.
""",
    "kahn": """Summary: Topological sort using indegrees and a queue.
Time: O(V+E)
Space: O(V)
Use: DAG scheduling, dependency resolution; detects cycles if output size < V.
""",
    # Strings
    "rabin_karp": """Summary: Rolling hash substring search.
Time: Avg O(n+m), Worst O(nm) with many collisions
Space: O(1) extra
Notes: Great for multiple pattern search with hashing; watch for modulus/hash collisions.
""",
    # Data structures
    "segment_tree": """Summary: Balanced tree over ranges for queries/updates.
Build: O(n), Query/Update: O(log n)
Space: O(n)
Use: Range sum/min/max, lazy propagation for range updates.
""",
    "fenwick_tree": """Summary: Binary Indexed Tree for prefix aggregates.
Build: O(n), Update/Prefix Query: O(log n)
Space: O(n)
Use: Compact alternative to segtree for prefix sums/diffs.
""",
    # DP / combinatorics
    "fibonacci": """Summary: DP/memoization yields O(n) time vs exponential recursion.
Time: O(n), Space: O(1) if iterative; O(n) with memo recursion stack.
""",
    "knapsack": """Summary: 0/1 knapsack DP over items and capacity.
Time: O(nW), Space: O(W) with rolling array
Notes: Pseudo-polynomial; NP-hard in general; consider value-based DP or meet-in-the-middle.
""",
    "lcs": """Summary: Longest Common Subsequence DP.
Time: O(nm), Space: O(min(n,m)) with Hirschberg
Use: Diff tools, sequence similarity.
""",
    "bitmask_tsp": """Summary: Held–Karp DP for TSP.
Time: O(n^2 2^n), Space: O(n 2^n)
Use: Small n exact TSP; else heuristics/approximation.
""",
    # Patterns
    "sliding_window": """Summary: Maintain a window with two pointers to satisfy constraints.
Typical Time: O(n), Space: O(1) or O(k) for counts.
Use: Subarrays with sum/unique/count constraints.
""",
    "two_pointers": """Summary: Pair pointers moving toward/along an array.
Typical Time: O(n), Space: O(1)
Use: Two-sum in sorted array, dedup, merging, partitioning.
""",
}


def get_notes(module_name: str) -> str:
    """
    Returns a notes string for a given dotted module name.
    Falls back to using the basename (e.g. 'quick_sort') if full name not present).
    If not found, returns a generic Big-O helper note so the UI always shows guidance.
    """
    base = module_name.split(".")[-1]
    note = MODULE_NOTES.get(module_name) or MODULE_NOTES.get(base)
    if note:
        return note
    title = base.replace("_", " ").title()
    return f"""Summary: {title} — notes not yet curated.
Time: Estimate via loops/recurrences; common classes: O(1), O(log n), O(n), O(n log n), O(n^2)
Space: Count auxiliary structures and recursion depth.
Tip: See the Big-O Guide for how to derive bounds and compare trade-offs."""


def discover_demos() -> dict[str, list[dict]]:
    """
    Discover modules under src/ that expose a callable `demo()` function.
    Returns a mapping: category (e.g. 'algorithms/sorting') -> list of demo metadata.
    """
    demos = []
    for path in SRC_DIR.rglob("*.py"):
        if path.name == "__init__.py":
            continue

        rel = path.relative_to(SRC_DIR)
        module_name = ".".join(rel.with_suffix("").parts)

        try:
            src_text = path.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue
        import re

        if re.search(r"^\s*def\s+demo\s*\(", src_text, flags=re.M):
            category = "/".join(rel.parts[:-1]) or "."
            title = rel.stem.replace("_", " ").title()
            demos.append(
                {
                    "id": module_name,
                    "title": title,
                    "category": category,
                    "module": module_name,
                    "path": str(path),
                }
            )

    # Sort and group
    demos.sort(key=lambda d: (d["category"], d["title"]))
    categories: dict[str, list[dict]] = {}
    for d in demos:
        categories.setdefault(d["category"], []).append(d)
    return categories


@lru_cache(maxsize=1)
def get_categories() -> dict[str, list[dict]]:
    return discover_demos()


# Map discovered sorting modules to visualization keys
SORTING_VIZ_MAP = {
    "interview_workbook.algorithms.sorting.bubble_sort": "bubble",
    "interview_workbook.algorithms.sorting.insertion_sort": "insertion",
    "interview_workbook.algorithms.sorting.quick_sort": "quick",
    "interview_workbook.algorithms.sorting.merge_sort": "merge",
    "interview_workbook.algorithms.sorting.heap_sort": "heap",
}

# Graph visualizations (BFS/DFS) available for this module
GRAPH_VIZ_MODULES = {
    "graphs.bfs_dfs": True,
}

# Pathfinding visualizations available
PATH_VIZ_MODULES = {
    "graphs.a_star": True,
    "graphs.dijkstra": True,
}


# Template helper functions
@app.context_processor
def utility_processor():
    def get_card_type(category, demo):
        # Add a check for the existence of 'id' and its type
        demo_id = demo.get('id')
        if category == 'visualizations' or (isinstance(demo_id, str) and demo_id.startswith('viz.')):
            return 'visualization-card'
        if 'leetcode' in category:
            return 'leetcode-card'
        return 'algorithm-card'

    def get_demo_status(demo):
        # Placeholder logic for demo status
        if 'TODO' in demo.get('title', '').upper():
            return 'todo'
        if demo.get('id') and hash(demo['id']) % 5 == 0:
            return 'partial'
        return 'complete'

    def get_progress_percentage(demo):
        status = get_demo_status(demo)
        if status == 'complete':
            return 100
        if status == 'partial':
            return 50
        return 0

    def get_progress_text(demo):
        status = get_demo_status(demo)
        if status == 'complete':
            return "Completed"
        if status == 'partial':
            return "In Progress"
        return "Not Started"
        
    def get_category_progress(category, demos):
        completed = sum(1 for d in demos if get_demo_status(d) == 'complete')
        return int((completed / len(demos)) * 100) if demos else 0

    return dict(
        get_card_type=get_card_type,
        get_demo_status=get_demo_status,
        get_progress_percentage=get_progress_percentage,
        get_progress_text=get_progress_text,
        get_category_progress=get_category_progress,
    )


@app.route("/")
def index():
    # Build categories with additional top-level visualization entries for the dashboard
    categories = {k: v[:] for k, v in get_categories().items()}
    
    # Add LeetCode problems to categories
    from src.interview_workbook.leetcode._registry import get_all as get_all_leetcode
    from src.interview_workbook.leetcode._types import Category
    
    leetcode_problems = get_all_leetcode()
    for problem in leetcode_problems:
        category_key = f"leetcode/{problem['category'].value}"
        categories.setdefault(category_key, []).append(problem)

    # Add visualizations
    categories.setdefault("visualizations", [])
    visualizations = [
        {"id": "viz.sorting", "title": "Sorting Visualizations", "category": "visualizations", "module": "viz.sorting", "path": "flask_app/visualizations/sorting_viz.py"},
        {"id": "viz.graph", "title": "Graph Traversal (BFS/DFS)", "category": "visualizations", "module": "viz.graph", "path": "flask_app/visualizations/graph_viz.py"},
        {"id": "viz.path", "title": "Pathfinding (A*/Dijkstra/BFS/GBFS)", "category": "visualizations", "module": "viz.path", "path": "flask_app/visualizations/path_viz.py"},
        {"id": "viz.arrays", "title": "Array Techniques", "category": "visualizations", "module": "viz.arrays", "path": "flask_app/visualizations/array_viz.py"},
        {"id": "viz.mst", "title": "Minimum Spanning Tree (Kruskal/Prim)", "category": "visualizations", "module": "viz.mst", "path": "flask_app/visualizations/mst_viz.py"},
        {"id": "viz.topo", "title": "Topological Sort (Kahn)", "category": "visualizations", "module": "viz.topo", "path": "flask_app/visualizations/topo_viz.py"},
        {"id": "viz.nn", "title": "Neural Network (MLP Classifier)", "category": "visualizations", "module": "viz.nn", "path": "flask_app/visualizations/nn_viz.py"},
    ]
    categories["visualizations"].extend(visualizations)

    total_demos = sum(len(demos) for demos in categories.values())
    # Placeholder for completion stats
    completed_demos = int(total_demos * 0.87)
    remaining_todos = total_demos - completed_demos
    completion_percentage = int((completed_demos / total_demos) * 100) if total_demos > 0 else 0

    return render_template(
        "index.html",
        categories=categories,
        total_demos=total_demos,
        completed_demos=completed_demos,
        remaining_todos=remaining_todos,
        completion_percentage=completion_percentage,
        sorting_viz_map=SORTING_VIZ_MAP,
        graph_viz_modules=GRAPH_VIZ_MODULES,
        path_viz_modules=PATH_VIZ_MODULES,
    )


def run_demo(module_name: str) -> str:
    """Import the module and execute its demo() while capturing stdout."""
    mod = importlib.import_module(module_name)
    demo_fn = getattr(mod, "demo", None)
    if not callable(demo_fn):
        raise ValueError(f"Module {module_name} does not define a callable demo()")

    import contextlib

    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        demo_fn()
    return buf.getvalue()


@app.get("/demo")
def demo_page():
    module = request.args.get("module")
    if not module:
        return redirect(url_for("index"))

    meta = None
    for demos in get_categories().values():
        for d in demos:
            if d["id"] == module:
                meta = d
                break
        if meta:
            break

    if meta is None:
        abort(404, description=f"Demo not found for module {module}")

    return render_template(
        "demo.html", meta=meta, output=None, error=None, code=None, notes=get_notes(meta["id"])
    )


@app.post("/demo")
def demo_run():
    module = request.form.get("module")
    if not module:
        abort(400, description="Missing module")

    meta = None
    for demos in get_categories().values():
        for d in demos:
            if d["id"] == module:
                meta = d
                break
        if meta:
            break

    if meta is None:
        abort(404, description=f"Demo not found for module {module}")

    output, error = None, None
    try:
        output = run_demo(module)
    except Exception as e:
        error = "".join(traceback.format_exception(type(e), e, e.__traceback__))

    return render_template(
        "demo.html", meta=meta, output=output, error=error, code=None, notes=get_notes(meta["id"])
    )


@app.post("/api/demo")
def api_demo_run():
    module = request.form.get("module")
    if not module and request.is_json:
        data = request.get_json(silent=True) or {}
        module = data.get("module")
    if not module:
        return jsonify({"error": "Missing module"}), 400
    try:
        output = run_demo(module)
        return jsonify({"output": output, "error": None})
    except Exception as e:
        error = "".join(traceback.format_exception(type(e), e, e.__traceback__))
        return jsonify({"output": None, "error": error})


@app.get("/source")
def source():
    module = request.args.get("module")
    if not module:
        abort(400, description="Missing module")

    rel = Path(module.replace(".", "/") + ".py")
    filepath = SRC_DIR / rel
    if not filepath.exists():
        abort(404, description=f"Source not found for module {module}")

    code = filepath.read_text(encoding="utf-8")
    meta = {
        "id": module,
        "title": rel.stem.replace("_", " ").title(),
        "category": "/".join(rel.parts[:-1]),
        "path": str(filepath),
    }
    return render_template(
        "demo.html", meta=meta, output=None, error=None, code=code, notes=get_notes(meta["id"])
    )


@app.get("/viz/sorting")
def viz_sorting():
    # Render sorting visualization page
    algo = request.args.get("algo", "quick")
    try:
        from flask_app.visualizations import sorting_viz as s_viz  # type: ignore

        algorithms = [{"key": k, "name": v["name"]} for k, v in s_viz.ALGORITHMS.items()]
    except Exception:
        algorithms = [
            {"key": "quick", "name": "Quick Sort"},
            {"key": "bubble", "name": "Bubble Sort"},
            {"key": "insertion", "name": "Insertion Sort"},
        ]
    return render_template(
        "viz_sorting.html",
        algo=algo,
        algorithms=algorithms,
        notes=get_notes(
            {
                "quick": "quick_sort",
                "bubble": "bubble_sort",
                "insertion": "insertion_sort",
                "merge": "merge_sort",
                "heap": "heap_sort",
            }.get(algo, algo)
        ),
    )


@app.post("/api/viz/sorting")
def api_viz_sorting():
    # Return JSON frames for a sorting visualization
    if request.is_json:
        data = request.get_json(silent=True) or {}
    else:
        data = request.form

    algo = data.get("algo", "quick")
    n = int(data.get("n", 30))
    seed = data.get("seed", None)
    seed = int(seed) if seed not in (None, "", "null") else None
    unique = data.get("unique", "true")
    if isinstance(unique, str):
        unique = unique.lower() != "false"

    try:
        from flask_app.visualizations import sorting_viz as s_viz  # type: ignore

        result = s_viz.visualize(algo, n=n, seed=seed, unique=unique)
        return jsonify(result)
    except Exception as e:
        error = "".join(traceback.format_exception(type(e), e, e.__traceback__))
        return jsonify({"error": error}), 500


@app.get("/viz/graph")
def viz_graph():
    # Render BFS/DFS visualization page
    algo = request.args.get("algo", "bfs")
    algorithms = [
        {"key": "bfs", "name": "Breadth-First Search"},
        {"key": "dfs", "name": "Depth-First Search"},
    ]
    return render_template(
        "viz_graph.html",
        algo=algo,
        algorithms=algorithms,
        notes=get_notes({"bfs": "bfs_dfs", "dfs": "bfs_dfs"}.get(algo, "bfs_dfs")),
    )


@app.post("/api/viz/graph")
def api_viz_graph():
    # Return JSON frames for BFS/DFS visualization
    if request.is_json:
        data = request.get_json(silent=True) or {}
    else:
        data = request.form

    algo = data.get("algo", "bfs")
    n = int(data.get("n", 12))
    p = float(data.get("p", 0.25))
    start = int(data.get("start", 0))
    seed = data.get("seed", None)
    seed = int(seed) if seed not in (None, "", "null") else None

    try:
        from flask_app.visualizations import graph_viz as g_viz  # type: ignore

        result = g_viz.visualize(algo, n=n, p=p, seed=seed, start=start)
        return jsonify(result)
    except Exception as e:
        error = "".join(traceback.format_exception(type(e), e, e.__traceback__))
        return jsonify({"error": error}), 500


@app.get("/viz/path")
def viz_path():
    # Render pathfinding visualization page (A*, Dijkstra, BFS, Greedy Best-First)
    algo = request.args.get("algo", "astar")
    try:
        from flask_app.visualizations import path_viz as p_viz  # type: ignore

        algorithms = [{"key": k, "name": v["name"]} for k, v in p_viz.ALGORITHMS.items()]
    except Exception:
        algorithms = [
            {"key": "astar", "name": "A* (Manhattan)"},
            {"key": "dijkstra", "name": "Dijkstra"},
            {"key": "bfs", "name": "Breadth-First Search"},
            {"key": "gbfs", "name": "Greedy Best-First Search"},
        ]
    return render_template(
        "viz_path.html",
        algo=algo,
        algorithms=algorithms,
        notes=get_notes(
            {"astar": "a_star", "dijkstra": "dijkstra", "bfs": "bfs_dfs", "gbfs": "gbfs"}.get(
                algo, algo
            )
        ),
    )


@app.post("/api/viz/path")
def api_viz_path():
    if request.is_json:
        data = request.get_json(silent=True) or {}
    else:
        data = request.form

    algo = data.get("algo", "astar")
    rows = int(data.get("rows", 20))
    cols = int(data.get("cols", 30))
    density = float(data.get("density", 0.25))
    seed = data.get("seed", None)
    seed = int(seed) if seed not in (None, "", "null") else None

    try:
        from flask_app.visualizations import path_viz as p_viz  # type: ignore

        result = p_viz.visualize(algo, rows=rows, cols=cols, density=density, seed=seed)
        return jsonify(result)
    except Exception as e:
        error = "".join(traceback.format_exception(type(e), e, e.__traceback__))
        return jsonify({"error": error}), 500


@app.get("/viz/arrays")
def viz_arrays():
    # Render array techniques visualization page (Binary Search / Two-Pointers / Sliding Window)
    algo = request.args.get("algo", "binary_search")
    try:
        from flask_app.visualizations import array_viz as a_viz  # type: ignore

        algorithms = [{"key": k, "name": v["name"]} for k, v in a_viz.ALGORITHMS.items()]
    except Exception:
        algorithms = [
            {"key": "binary_search", "name": "Binary Search"},
            {"key": "two_pointers_sum", "name": "Two Pointers (Two-Sum in Sorted Array)"},
            {
                "key": "sliding_window_min_len_geq",
                "name": "Sliding Window (Min Len with Sum ≥ target)",
            },
        ]
    return render_template(
        "viz_arrays.html",
        algo=algo,
        algorithms=algorithms,
        notes=get_notes(
            {
                "binary_search": "binary_search",
                "two_pointers_sum": "two_pointers",
                "sliding_window_min_len_geq": "sliding_window",
            }.get(algo, algo)
        ),
    )


@app.post("/api/viz/arrays")
def api_viz_arrays():
    # Return JSON frames for array techniques visualization
    if request.is_json:
        data = request.get_json(silent=True) or {}
    else:
        data = request.form

    algo = data.get("algo", "binary_search")
    n = int(data.get("n", 30))
    seed = data.get("seed", None)
    seed = int(seed) if seed not in (None, "", "null") else None
    target = data.get("target", None)
    target = int(target) if target not in (None, "", "null") else None

    try:
        from flask_app.visualizations import array_viz as a_viz  # type: ignore

        result = a_viz.visualize(algo, n=n, seed=seed, target=target)
        return jsonify(result)
    except Exception as e:
        error = "".join(traceback.format_exception(type(e), e, e.__traceback__))
        return jsonify({"error": error}), 500


@app.get("/viz/mst")
def viz_mst():
    # Render MST visualization page (Kruskal/Prim)
    algo = request.args.get("algo", "kruskal")
    try:
        from flask_app.visualizations import mst_viz as m_viz  # type: ignore

        algorithms = [{"key": k, "name": v["name"]} for k, v in m_viz.ALGORITHMS.items()]
    except Exception:
        algorithms = [
            {"key": "kruskal", "name": "Minimum Spanning Tree (Kruskal)"},
            {"key": "prim", "name": "Minimum Spanning Tree (Prim)"},
        ]
    return render_template(
        "viz_mst.html",
        algo=algo,
        algorithms=algorithms,
        notes=get_notes({"kruskal": "kruskal", "prim": "prim"}.get(algo, algo)),
    )


@app.post("/api/viz/mst")
def api_viz_mst():
    # Return JSON frames for MST visualization
    if request.is_json:
        data = request.get_json(silent=True) or {}
    else:
        data = request.form

    algo = data.get("algo", "kruskal")
    n = int(data.get("n", 12))
    k = int(data.get("k", 3))
    start = int(data.get("start", 0))
    seed = data.get("seed", None)
    seed = int(seed) if seed not in (None, "", "null") else None

    try:
        from flask_app.visualizations import mst_viz as m_viz  # type: ignore

        result = m_viz.visualize(algo, n=n, k=k, seed=seed, start=start)
        return jsonify(result)
    except Exception as e:
        error = "".join(traceback.format_exception(type(e), e, e.__traceback__))
        return jsonify({"error": error}), 500


@app.get("/viz/topo")
def viz_topo():
    # Render topological sort visualization page (Kahn's algorithm)
    algo = request.args.get("algo", "kahn")
    try:
        from flask_app.visualizations import topo_viz as t_viz  # type: ignore

        algorithms = [{"key": k, "name": v["name"]} for k, v in t_viz.ALGORITHMS.items()]
    except Exception:
        algorithms = [
            {"key": "kahn", "name": "Topological Sort (Kahn's Algorithm)"},
        ]
    return render_template(
        "viz_topo.html",
        algo=algo,
        algorithms=algorithms,
        notes=get_notes({"kahn": "kahn"}.get(algo, algo)),
    )


@app.post("/api/viz/topo")
def api_viz_topo():
    # Return JSON frames for topological sort visualization
    if request.is_json:
        data = request.get_json(silent=True) or {}
    else:
        data = request.form

    algo = data.get("algo", "kahn")
    n = int(data.get("n", 12))
    layers = int(data.get("layers", 3))
    p = float(data.get("p", 0.35))
    seed = data.get("seed", None)
    seed = int(seed) if seed not in (None, "", "null") else None

    try:
        from flask_app.visualizations import topo_viz as t_viz  # type: ignore

        result = t_viz.visualize(algo, n=n, layers=layers, p=p, seed=seed)
        return jsonify(result)
    except Exception as e:
        error = "".join(traceback.format_exception(type(e), e, e.__traceback__))
        return jsonify({"error": error}), 500


@app.get("/viz/nn")
def viz_nn():
    # Render neural network (MLP) visualization page
    dataset = request.args.get("dataset", "blobs")
    return render_template("viz_nn.html", dataset=dataset)


@app.post("/api/viz/nn")
def api_viz_nn():
    # Return JSON frames for NN training visualization
    if request.is_json:
        data = request.get_json(silent=True) or {}
    else:
        data = request.form

    dataset = data.get("dataset", "blobs")
    n = int(data.get("n", 200))
    hidden = int(data.get("hidden", 8))
    lr = float(data.get("lr", 0.5))
    epochs = int(data.get("epochs", 50))
    grid = int(data.get("grid", 32))
    seed = data.get("seed", None)
    seed = int(seed) if seed not in (None, "", "null") else None

    try:
        from flask_app.visualizations import nn_viz as nn  # type: ignore

        result = nn.visualize(
            dataset=dataset, n=n, hidden=hidden, lr=lr, epochs=epochs, seed=seed, grid=grid
        )
        return jsonify(result)
    except Exception as e:
        error = "".join(traceback.format_exception(type(e), e, e.__traceback__))
        return jsonify({"error": error}), 500


@app.get("/big-o")
def big_o_guide():
    # Render Big-O/time-space complexity guide page
    return render_template("big_o.html")


@app.get("/favicon.ico")
def favicon_ico():
    # Suppress 404 favicon requests in development
    from flask import Response as _Response

    return _Response(status=204)


if __name__ == "__main__":
    # For development
    app.run(host="127.0.0.1", port=5000, debug=True)
