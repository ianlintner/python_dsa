import random

from interview_workbook.algorithms.sorting.bubble_sort import (
    bubble_sort,
    bubble_sort_inplace,
)
from interview_workbook.algorithms.sorting.insertion_sort import (
    insertion_sort,
    insertion_sort_inplace,
)
from interview_workbook.algorithms.sorting.selection_sort import (
    selection_sort,
    selection_sort_inplace,
)


class TestBasicSorts:
    def test_empty(self):
        assert insertion_sort([]) == []
        assert selection_sort([]) == []
        assert bubble_sort([]) == []

    def test_single(self):
        assert insertion_sort([1]) == [1]
        assert selection_sort([1]) == [1]
        assert bubble_sort([1]) == [1]

    def test_already_sorted(self):
        arr = [1, 2, 3, 4, 5]
        assert insertion_sort(arr) == arr
        assert selection_sort(arr) == arr
        assert bubble_sort(arr) == arr

    def test_reverse_sorted(self):
        arr = [5, 4, 3, 2, 1]
        expected = [1, 2, 3, 4, 5]
        assert insertion_sort(arr) == expected
        assert selection_sort(arr) == expected
        assert bubble_sort(arr) == expected

    def test_duplicates(self):
        arr = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3]
        expected = sorted(arr)
        assert insertion_sort(arr) == expected
        assert selection_sort(arr) == expected
        assert bubble_sort(arr) == expected

    def test_random_small(self):
        for _ in range(10):
            arr = [random.randint(-50, 50) for _ in range(20)]
            expected = sorted(arr)
            assert insertion_sort(arr) == expected
            assert selection_sort(arr) == expected
            assert bubble_sort(arr) == expected

    def test_inplace_variants(self):
        cases = [
            [],
            [1],
            [3, 1, 2, 4],
            [5, 4, 3, 2, 1],
            [2, 2, 1, 1, 3],
        ]
        for arr in cases:
            exp = sorted(arr)
            a1 = arr[:]
            insertion_sort_inplace(a1)
            assert a1 == exp

            a2 = arr[:]
            selection_sort_inplace(a2)
            assert a2 == exp

            a3 = arr[:]
            bubble_sort_inplace(a3)
            assert a3 == exp

    def test_stability_insertion_bubble(self):
        # Use tuples (key, original_index) to test relative order stability
        arr = [(3, 0), (1, 1), (3, 2), (2, 3), (3, 4)]
        ins = insertion_sort(arr)
        bub = bubble_sort(arr)
        # All 1s then 2s then 3s; within key groups, original order preserved
        assert [x[0] for x in ins] == [1, 2, 3, 3, 3]
        assert [x[0] for x in bub] == [1, 2, 3, 3, 3]
        threes_ins = [x for x in ins if x[0] == 3]
        threes_bub = [x for x in bub if x[0] == 3]
        assert threes_ins == [(3, 0), (3, 2), (3, 4)]
        assert threes_bub == [(3, 0), (3, 2), (3, 4)]

    def test_selection_not_stable_correctness_only(self):
        # Selection sort isn't stable; assert correctness but not stability
        arr = [(2, "a"), (1, "x"), (2, "b")]
        result = selection_sort(arr, key=lambda x: x[0])
        assert [x[0] for x in result] == [1, 2, 2]
