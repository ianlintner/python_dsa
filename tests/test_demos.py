import importlib
import random

# Use the Flask app's discovery and runner to find and execute demo()s
from flask_app.app import discover_demos, run_demo  # type: ignore


def _seed_all():
    random.seed(0)
    try:
        import numpy as _np  # type: ignore  # noqa: F401

        _np.random.seed(0)
    except Exception:
        pass


def _flatten_categories(categories: dict[str, list[dict]]) -> list[dict]:
    out: list[dict] = []
    for demos in categories.values():
        out.extend(demos)
    return out


def test_discover_demos_nonempty():
    cats = discover_demos()
    all_demos = _flatten_categories(cats)
    # Ensure we discover at least some demo()s
    assert isinstance(cats, dict)
    assert len(all_demos) > 0


def test_run_all_demos_headless():
    """
    Run every discovered demo() in a headless manner with seeded randomness.
    The test passes as long as no exceptions are raised when running demo() and
    the captured output is a string (may be empty for some demos).
    """
    _seed_all()
    cats = discover_demos()
    all_demos = _flatten_categories(cats)
    # Sort deterministically by module id for consistent order
    all_demos.sort(key=lambda d: d["id"])

    for meta in all_demos:
        module_id = meta["id"]
        # Sanity: verify importable before running
        mod = importlib.import_module(module_id)
        assert hasattr(mod, "demo"), f"Module {module_id} missing demo()"
        out = run_demo(module_id)
        assert isinstance(out, str)
        # Ensure no progress tracking remnants in output (UI-related, not algorithm logs)
        assert "progress tracking" not in out.lower()
