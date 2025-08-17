import io
import sys


def capture_stdout(fn, *args, **kwargs) -> str:
    buf = io.StringIO()
    old = sys.stdout
    try:
        sys.stdout = buf
        fn(*args, **kwargs)
        return buf.getvalue()
    finally:
        sys.stdout = old


def test_main_run_demo_import_error_branch(monkeypatch):
    # Exercise the ImportError fallback branch in src/main.run_demo
    import src.main as main

    # Inject a fake demo that points to a non-existent module
    fake_key = "fake.module"
    main.DEMOS[fake_key] = ("totally_nonexistent.module.path", "demo")
    out = capture_stdout(main.run_demo, fake_key)
    # Should print an error importing module tip
    assert "Error importing module" in out or "Tip:" in out
    # Clean up
    main.DEMOS.pop(fake_key, None)


def test_check_sorted_len_guards_and_reverse():
    from interview_workbook.utils.check_sorted import is_sorted, is_strictly_sorted

    # len <= 1 guards
    assert is_sorted([]) is True
    assert is_sorted([7]) is True
    assert is_sorted([7], reverse=True) is True
    assert is_strictly_sorted([]) is True
    assert is_strictly_sorted([7]) is True
    assert is_strictly_sorted([7], reverse=True) is True

    # Mixed sanity
    assert is_sorted([3, 2, 1], reverse=True) is True
    assert is_strictly_sorted([3, 2, 2], reverse=True) is False


def test_linear_search_empty_and_singleton():
    from interview_workbook.algorithms.searching.linear_search import find_all, linear_search

    assert linear_search([], 1) == -1
    assert linear_search([42], 42) == 0
    assert find_all([], 5) == []
    assert find_all([9], 9) == [0]


def test_lazy_sorting_namespace_multiple_attrs():
    # Ensure lazy __getattr__ exposes multiple submodules without circular import
    import src.algorithms.sorting as srt  # type: ignore

    # Access multiple submodules to hit lazy path
    res1 = srt.insertion_sort.insertion_sort([3, 1, 2])
    res2 = srt.selection_sort.selection_sort([3, 1, 2])
    assert res1 == [1, 2, 3]
    assert res2 == [1, 2, 3]

    # Access non_comparison_sorts namespace too
    assert hasattr(srt.non_comparison_sorts, "counting_sort")
