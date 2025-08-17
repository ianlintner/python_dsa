from interview_workbook.algorithms.sorting import bubble_sort as bs
from interview_workbook.algorithms.sorting import insertion_sort as ins
from interview_workbook.algorithms.sorting import non_comparison_sorts as ncs
from interview_workbook.algorithms.sorting import selection_sort as sel


def test_bubble_sort_variants():
    arr = [3, 1, 2]
    assert bs.bubble_sort(arr) == [1, 2, 3]
    arr2 = [5, 4, 4, 1]
    bs.bubble_sort_inplace(arr2)
    assert arr2 == [1, 4, 4, 5]


def test_insertion_sort_variants():
    arr = [4, 2, 5, 1]
    assert ins.insertion_sort(arr) == [1, 2, 4, 5]
    arr2 = [3, 3, 2, 1]
    ins.insertion_sort_inplace(arr2)
    assert arr2 == [1, 2, 3, 3]


def test_selection_sort_variants():
    arr = [9, 7, 8, 6]
    out = sel.selection_sort(arr)
    assert out == [6, 7, 8, 9]
    arr2 = [5, 1, 4, 2]
    sel.selection_sort_inplace(arr2)
    assert arr2 == [1, 2, 4, 5]


def test_non_comparison_sorts_minimal():
    # counting_sort with non-negative integers
    arr = [3, 1, 2, 1, 0]
    assert ncs.counting_sort(arr, max_value=3) == [0, 1, 1, 2, 3]

    # counting_sort_by_key with tuples (value by key function)
    items = [("a", 2), ("b", 1), ("c", 2), ("d", 0)]
    out = ncs.counting_sort_by_key(items, key=lambda x: x[1], max_value=2)
    assert [k for k, _ in out] == ["d", "b", "a", "c"]

    # radix_sort_lsd_integers for non-negative integers
    arr2 = [170, 45, 75, 90, 802, 24, 2, 66]
    assert ncs.radix_sort_lsd_integers(arr2) == sorted(arr2)

    # radix_sort_lsd_fixed_strings
    strings = ["bca", "abc", "aaa", "zzz", "aba"]
    out2 = ncs.radix_sort_lsd_fixed_strings(strings, max_len=3)
    assert out2 == sorted(strings)
