import io
import sys
from importlib import reload

import pytest


def capture_stdout(fn, *args, **kwargs) -> str:
    buf = io.StringIO()
    old = sys.stdout
    try:
        sys.stdout = buf
        fn(*args, **kwargs)
        return buf.getvalue() or ""
    finally:
        sys.stdout = old


def test_main_cli_paths_cover_list_and_demo_and_help(monkeypatch):
    import src.main as main

    # --list path
    monkeypatch.setenv("PYTHONUNBUFFERED", "1")
    monkeypatch.setattr(sys, "argv", ["prog", "--list"])
    out_list = capture_stdout(main.main)
    assert "Available demos:" in out_list

    # --demo path (use a quick/cheap demo)
    monkeypatch.setattr(sys, "argv", ["prog", "--demo", "dp.lcs"])
    out_demo = capture_stdout(main.main)
    # Should include the running banner for the selected demo
    assert "Running dp.lcs demo" in out_demo

    # No args -> prints help
    monkeypatch.setattr(sys, "argv", ["prog"])
    out_help = capture_stdout(main.main)
    assert "usage:" in out_help or "Python Interview Algorithms Workbook" in out_help

    # reload main to ensure no side effects linger
    reload(main)


def test_linear_search_and_find_all_on_iterables():
    from interview_workbook.algorithms.searching.linear_search import (
        find_all,
        linear_search,
    )

    # Use a non-Sequence iterable (generator) to cover iterable branch in find_all
    def gen():
        for x in [1, 2, 1, 3, 1]:
            yield x

    # key=None path with generator
    assert find_all(gen(), 1) == [0, 2, 4]

    # key supplied: compare key(v) == target (target is raw value)
    class Item:
        def __init__(self, key):
            self.key = key

    def gen_items():
        for k in [1, 2, 1, 3, 1]:
            yield Item(k)

    assert find_all(gen_items(), 1, key=lambda it: it.key) == [0, 2, 4]

    # linear_search works on lists (already covered), add a quick key-path smoke
    items = [Item(1), Item(2), Item(3)]
    assert linear_search(items, 2, key=lambda it: it.key) == 1


def test_non_comparison_sorts_additional_branches():
    from interview_workbook.algorithms.sorting import non_comparison_sorts as ncs

    # counting_sort unstable branch
    arr = [3, 1, 2, 1, 0]
    assert ncs.counting_sort(arr, min_value=0, max_value=3, stable=False) == [
        0,
        1,
        1,
        2,
        3,
    ]

    # counting_sort_by_key with provided min/max aliases
    items = [("a", 3), ("b", 1), ("c", 2)]
    sorted_items = ncs.counting_sort_by_key(
        items, key=lambda x: x[1], min_value=1, max_value=3
    )
    assert [x[1] for x in sorted_items] == [1, 2, 3]

    # radix_sort_lsd_fixed_strings with explicit max_len (exercise padding path)
    strings = ["ab", "a", "abc"]
    out = ncs.radix_sort_lsd_fixed_strings(strings, max_len=3)
    assert out == ["a", "ab", "abc"]


@pytest.mark.timeout(5)
def test_utils_timing_more_paths():
    # Cover time_algorithms with more than one run and ensure it returns dict and prints header
    from interview_workbook.utils.timing import time_algorithms, timeit

    calls = {"a": 0, "b": 0}

    def alg_a(x: int) -> int:
        calls["a"] += 1
        return x + 10

    def alg_b(x: int) -> int:
        calls["b"] += 1
        return x * 10

    @time_algorithms(alg_a, alg_b)
    def run_for_both(algo, x: int) -> int:
        return algo(x)

    out = capture_stdout(run_for_both, 5)
    assert "Timing comparison" in out
    res = run_for_both(5)
    assert res["alg_a"][0] == 15 and res["alg_b"][0] == 50
    assert calls["a"] >= 2 and calls["b"] >= 2

    # Cover timeit printing path on a simple function that raises and still prints timing
    @timeit
    def may_raise(flag: bool) -> int:
        if flag:
            raise ValueError("boom")
        return 42

    # No raise
    out_ok = capture_stdout(may_raise, False)
    assert "may_raise took" in out_ok
    # With raise (still prints)
    with pytest.raises(ValueError):
        capture_stdout(may_raise, True)
