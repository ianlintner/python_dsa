from __future__ import annotations

import io
import importlib
import traceback
from pathlib import Path
import sys
from typing import Dict, List

from flask import Flask, render_template, request, redirect, url_for, abort


# Ensure we can import modules from src/
ROOT_DIR = Path(__file__).resolve().parents[1]
SRC_DIR = ROOT_DIR / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))


app = Flask(__name__, template_folder="templates", static_folder="static")


def discover_demos() -> Dict[str, List[dict]]:
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
    categories: Dict[str, List[dict]] = {}
    for d in demos:
        categories.setdefault(d["category"], []).append(d)
    return categories


CATEGORIES = discover_demos()


@app.route("/")
def index():
    return render_template("index.html", categories=CATEGORIES)


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


if __name__ == "__main__":
    # For development
    app.run(host="127.0.0.1", port=5000, debug=True)
