import io
import sys

import src  # cover src/__init__


def test_src_pkg_metadata():
    # Basic package metadata smoke
    assert isinstance(src.__version__, str)
    assert isinstance(src.__author__, str)
    assert len(src.__version__) > 0
    assert len(src.__author__) > 0


def capture_stdout(fn, *args, **kwargs) -> str:
    buf = io.StringIO()
    old = sys.stdout
    try:
        sys.stdout = buf
        fn(*args, **kwargs)
        return buf.getvalue()
    finally:
        sys.stdout = old


def test_main_list_and_run_demo_smoke():
    # Import inside test to avoid side-effects on import
    from src.main import list_demos, run_demo

    # list_demos prints the available demos
    out = capture_stdout(list_demos)
    assert "Available demos:" in out
    assert "dp.lcs" in out or "dp.lcs".replace(".", " ") in out

    # Run a lightweight demo that should be deterministic and quick
    # Choose dp.lcs (prints small cases) and math.number_theory (small operations)
    capture_stdout(run_demo, "dp.lcs")
    capture_stdout(run_demo, "math.number_theory")

    # Invalid key path falls back to listing demos
    out2 = capture_stdout(run_demo, "does.not.exist")
    assert "Demo not found" in out2
