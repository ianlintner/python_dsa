from __future__ import annotations

import importlib
import io
import sys
import traceback
from pathlib import Path

from flask import Flask, abort, jsonify, redirect, render_template, request, url_for

# Ensure we can import modules from src/
ROOT_DIR = Path(__file__).resolve().parents[1]
SRC_DIR = ROOT_DIR / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))


app = Flask(__name__, template_folder="templates", static_folder="static")


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
            mod = importlib.import_module(module_name)
        except Exception:
            # Skip modules that fail to import
            continue

        demo_fn = getattr(mod, "demo", None)
        if callable(demo_fn):
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


CATEGORIES = discover_demos()

# Map discovered sorting modules to visualization keys
SORTING_VIZ_MAP = {
    "algorithms.sorting.bubble_sort": "bubble",
    "algorithms.sorting.insertion_sort": "insertion",
    "algorithms.sorting.quick_sort": "quick",
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


@app.route("/")
def index():
    # Build categories with additional top-level visualization entries for the dashboard
    categories = {k: v[:] for k, v in CATEGORIES.items()}
    categories.setdefault("visualizations", [])
    categories["visualizations"].append(
        {
            "id": "viz.sorting",
            "title": "Sorting Visualizations",
            "category": "visualizations",
            "module": "viz.sorting",
            "path": "flask_app/visualizations/sorting_viz.py",
        }
    )
    categories["visualizations"].append(
        {
            "id": "viz.graph",
            "title": "Graph Traversal (BFS/DFS)",
            "category": "visualizations",
            "module": "viz.graph",
            "path": "flask_app/visualizations/graph_viz.py",
        }
    )
    categories["visualizations"].append(
        {
            "id": "viz.path",
            "title": "Pathfinding (A*/Dijkstra/BFS/GBFS)",
            "category": "visualizations",
            "module": "viz.path",
            "path": "flask_app/visualizations/path_viz.py",
        }
    )
    categories["visualizations"].append(
        {
            "id": "viz.arrays",
            "title": "Array Techniques (Binary Search / Two-Pointers / Sliding Window)",
            "category": "visualizations",
            "module": "viz.arrays",
            "path": "flask_app/visualizations/array_viz.py",
        }
    )
    categories["visualizations"].append(
        {
            "id": "viz.mst",
            "title": "Minimum Spanning Tree (Kruskal/Prim)",
            "category": "visualizations",
            "module": "viz.mst",
            "path": "flask_app/visualizations/mst_viz.py",
        }
    )
    categories["visualizations"].append(
        {
            "id": "viz.topo",
            "title": "Topological Sort (Kahn)",
            "category": "visualizations",
            "module": "viz.topo",
            "path": "flask_app/visualizations/topo_viz.py",
        }
    )
    categories["visualizations"].append(
        {
            "id": "viz.nn",
            "title": "Neural Network (MLP Binary Classifier)",
            "category": "visualizations",
            "module": "viz.nn",
            "path": "flask_app/visualizations/nn_viz.py",
        }
    )
    return render_template(
        "index.html",
        categories=categories,
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
    for demos in CATEGORIES.values():
        for d in demos:
            if d["id"] == module:
                meta = d
                break
        if meta:
            break

    if meta is None:
        abort(404, description=f"Demo not found for module {module}")

    return render_template("demo.html", meta=meta, output=None, error=None, code=None)


@app.post("/demo")
def demo_run():
    module = request.form.get("module")
    if not module:
        abort(400, description="Missing module")

    meta = None
    for demos in CATEGORIES.values():
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

    return render_template("demo.html", meta=meta, output=output, error=error, code=None)


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
    return render_template("demo.html", meta=meta, output=None, error=None, code=code)


@app.get("/viz/sorting")
def viz_sorting():
    # Render sorting visualization page
    algo = request.args.get("algo", "quick")
    try:
        from visualizations import sorting_viz as s_viz  # type: ignore

        algorithms = [{"key": k, "name": v["name"]} for k, v in s_viz.ALGORITHMS.items()]
    except Exception:
        algorithms = [
            {"key": "quick", "name": "Quick Sort"},
            {"key": "bubble", "name": "Bubble Sort"},
            {"key": "insertion", "name": "Insertion Sort"},
        ]
    return render_template("viz_sorting.html", algo=algo, algorithms=algorithms)


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
        from visualizations import sorting_viz as s_viz  # type: ignore

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
    return render_template("viz_graph.html", algo=algo, algorithms=algorithms)


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
        from visualizations import graph_viz as g_viz  # type: ignore

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
        from visualizations import path_viz as p_viz  # type: ignore

        algorithms = [{"key": k, "name": v["name"]} for k, v in p_viz.ALGORITHMS.items()]
    except Exception:
        algorithms = [
            {"key": "astar", "name": "A* (Manhattan)"},
            {"key": "dijkstra", "name": "Dijkstra"},
            {"key": "bfs", "name": "Breadth-First Search"},
            {"key": "gbfs", "name": "Greedy Best-First Search"},
        ]
    return render_template("viz_path.html", algo=algo, algorithms=algorithms)


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
        from visualizations import path_viz as p_viz  # type: ignore

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
        from visualizations import array_viz as a_viz  # type: ignore

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
    return render_template("viz_arrays.html", algo=algo, algorithms=algorithms)


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
        from visualizations import array_viz as a_viz  # type: ignore

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
        from visualizations import mst_viz as m_viz  # type: ignore

        algorithms = [{"key": k, "name": v["name"]} for k, v in m_viz.ALGORITHMS.items()]
    except Exception:
        algorithms = [
            {"key": "kruskal", "name": "Minimum Spanning Tree (Kruskal)"},
            {"key": "prim", "name": "Minimum Spanning Tree (Prim)"},
        ]
    return render_template("viz_mst.html", algo=algo, algorithms=algorithms)


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
        from visualizations import mst_viz as m_viz  # type: ignore

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
        from visualizations import topo_viz as t_viz  # type: ignore

        algorithms = [{"key": k, "name": v["name"]} for k, v in t_viz.ALGORITHMS.items()]
    except Exception:
        algorithms = [
            {"key": "kahn", "name": "Topological Sort (Kahn's Algorithm)"},
        ]
    return render_template("viz_topo.html", algo=algo, algorithms=algorithms)


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
        from visualizations import topo_viz as t_viz  # type: ignore

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
        from visualizations import nn_viz as nn  # type: ignore

        result = nn.visualize(
            dataset=dataset, n=n, hidden=hidden, lr=lr, epochs=epochs, seed=seed, grid=grid
        )
        return jsonify(result)
    except Exception as e:
        error = "".join(traceback.format_exception(type(e), e, e.__traceback__))
        return jsonify({"error": error}), 500


@app.get("/favicon.ico")
def favicon_ico():
    # Suppress 404 favicon requests in development
    from flask import Response as _Response

    return _Response(status=204)


if __name__ == "__main__":
    # For development
    app.run(host="127.0.0.1", port=5000, debug=True)
