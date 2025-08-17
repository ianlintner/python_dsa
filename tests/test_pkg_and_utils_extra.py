import io
import sys

import pytest


def capture_stdout(fn, *args, **kwargs) -> str:
    buf = io.StringIO()
    old = sys.stdout
    try:
        sys.stdout = buf
        out = fn(*args, **kwargs)
        return buf.getvalue() or ""
    finally:
        sys.stdout = old


def test_src_algorithms_sorting_init_exposes_modules():
    # Import the lightweight top-level namespace to cover src/algorithms/sorting/__init__.py
    import src.algorithms.sorting as srt  # type: ignore

    # Validate that submodules are accessible via the namespace
    assert hasattr(srt, "bubble_sort")
    assert hasattr(srt, "insertion_sort")
    assert hasattr(srt, "selection_sort")
    assert hasattr(srt, "non_comparison_sorts")

    # Smoke call one function through the namespace
    res = srt.bubble_sort.bubble_sort([3, 1, 2])
    assert res == [1, 2, 3]


def test_timing_decorators_timeit_and_time_algorithms():
    from interview_workbook.utils.timing import time_algorithms, timeit

    # timeit should print timing and return original result
    @timeit
    def add(a: int, b: int) -> int:
        return a + b

    out = capture_stdout(add, 2, 3)
    assert "add took" in out
    assert add(2, 3) == 5

    # time_algorithms should run the test_fn once per algorithm and print timings
    def alg_a(x: int) -> int:
        return x + 1

    def alg_b(x: int) -> int:
        return x * 2

    @time_algorithms(alg_a, alg_b)
    def run_one(algo, x: int) -> int:
        return algo(x)

    out2 = capture_stdout(run_one, 7)
    # Should print a header and timings for each algorithm
    assert "Timing comparison" in out2
    assert "alg_a" in out2 and "alg_b" in out2
    # And the decorator returns a dict of results
    results = run_one(7)
    assert isinstance(results, dict)
    assert results["alg_a"][0] == 8
    assert results["alg_b"][0] == 14


def test_check_sorted_strict_and_reverse():
    from interview_workbook.utils.check_sorted import (
        is_sorted,
        is_strictly_sorted,
    )

    asc = [1, 2, 2, 3]
    desc = [5, 4, 3, 2, 1]
    desc_strict = [5, 4, 3, 2, 1]
    not_sorted = [1, 3, 2]

    # Ascending cases
    assert is_sorted(asc) is True
    assert is_strictly_sorted(asc) is False
    assert is_sorted(not_sorted) is False
    assert is_strictly_sorted([1, 2, 3, 4]) is True

    # Descending cases (reverse=True)
    assert is_sorted(desc, reverse=True) is True
    assert is_strictly_sorted(desc_strict, reverse=True) is True
    assert is_sorted([3, 4, 2], reverse=True) is False


@pytest.mark.timeout(10)
def test_main_list_and_demo_help_paths_smoke():
    """
    Exercise additional branches in src/main.py via list_demos() and invalid demo key.
    """
    from src.main import list_demos, run_demo

    out_list = capture_stdout(list_demos)
    assert "Available demos:" in out_list

    out_invalid = capture_stdout(run_demo, "invalid.demo.key")
    assert "Demo not found" in out_invalid
    assert "Available demos:" in out_invalid
