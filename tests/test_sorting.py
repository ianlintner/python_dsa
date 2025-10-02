import random

import pytest

from interview_workbook.algorithms.sorting.heap_sort import heap_sort
from interview_workbook.algorithms.sorting.merge_sort import (
    merge_sort,
    merge_sort_inplace,
)
from interview_workbook.algorithms.sorting.quick_sort import quick_sort, quick_sort_3way
from interview_workbook.utils.check_sorted import is_sorted


class TestSorting:
    """Test cases for sorting algorithms."""

    def test_empty_array(self):
        """Test sorting empty arrays."""
        empty = []
        assert merge_sort(empty) == []
        assert quick_sort(empty) == []
        assert heap_sort(empty) == []

    def test_single_element(self):
        """Test sorting single element arrays."""
        single = [42]
        assert merge_sort(single) == [42]
        assert quick_sort(single) == [42]
        assert heap_sort(single) == [42]

    def test_already_sorted(self):
        """Test sorting already sorted arrays."""
        sorted_arr = [1, 2, 3, 4, 5]
        assert merge_sort(sorted_arr) == sorted_arr
        assert quick_sort(sorted_arr) == sorted_arr
        assert heap_sort(sorted_arr) == sorted_arr

    def test_reverse_sorted(self):
        """Test sorting reverse sorted arrays."""
        reverse = [5, 4, 3, 2, 1]
        expected = [1, 2, 3, 4, 5]
        assert merge_sort(reverse) == expected
        assert quick_sort(reverse) == expected
        assert heap_sort(reverse) == expected

    def test_duplicates(self):
        """Test sorting arrays with duplicates."""
        duplicates = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3]
        expected = sorted(duplicates)

        assert merge_sort(duplicates) == expected
        assert quick_sort(duplicates) == expected
        assert quick_sort_3way(duplicates) == expected
        assert heap_sort(duplicates) == expected

    def test_all_same(self):
        """Test sorting arrays with all same elements."""
        same = [7, 7, 7, 7, 7]
        assert merge_sort(same) == same
        assert quick_sort(same) == same
        assert heap_sort(same) == same

    def test_random_arrays(self):
        """Test sorting random arrays."""
        for _ in range(10):
            arr = [random.randint(1, 100) for _ in range(20)]
            expected = sorted(arr)

            assert merge_sort(arr) == expected
            assert quick_sort(arr) == expected
            assert heap_sort(arr) == expected

    def test_merge_sort_inplace(self):
        """Test in-place merge sort."""
        test_cases = [[], [1], [3, 1, 4, 1, 5], [5, 4, 3, 2, 1], [1, 2, 3, 4, 5]]

        for arr in test_cases:
            original = arr[:]
            expected = sorted(original)
            merge_sort_inplace(arr)
            assert arr == expected

    def test_stability_merge_sort(self):
        """Test that merge sort is stable."""
        # Use tuples where second element is original position
        arr = [(3, 0), (1, 1), (3, 2), (2, 3)]
        result = merge_sort(arr)

        # Check that relative order of equal elements is preserved
        threes = [item for item in result if item[0] == 3]
        assert threes == [(3, 0), (3, 2)]  # Original order preserved

    def test_large_array(self):
        """Test sorting larger arrays."""
        large_arr = list(range(1000, 0, -1))  # 1000 elements in reverse
        expected = list(range(1, 1001))

        assert merge_sort(large_arr) == expected
        assert is_sorted(quick_sort(large_arr))
        assert is_sorted(heap_sort(large_arr))


if __name__ == "__main__":
    pytest.main([__file__])
