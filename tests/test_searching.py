import pytest

from interview_workbook.algorithms.searching.advanced_search import (
    exponential_search,
    search_rotated,
    search_rotated_with_duplicates,
)
from interview_workbook.algorithms.searching.advanced_search import (
    lower_bound as adv_lower_bound,
)
from interview_workbook.algorithms.searching.advanced_search import (
    upper_bound as adv_upper_bound,
)
from interview_workbook.algorithms.searching.binary_search import (
    binary_search,
    binary_search_2d,
    binary_search_range,
)
from interview_workbook.algorithms.searching.binary_search import (
    lower_bound as bs_lower_bound,
)
from interview_workbook.algorithms.searching.binary_search import (
    upper_bound as bs_upper_bound,
)
from interview_workbook.algorithms.searching.quickselect import (
    find_median,
    quickselect,
)


class TestBinarySearchFamily:
    def test_binary_search_basic(self):
        arr = [1, 2, 3, 4, 5, 6, 7]
        assert binary_search(arr, 1) == 0
        assert binary_search(arr, 4) == 3
        assert binary_search(arr, 7) == 6
        assert binary_search(arr, 8) == -1

    def test_lower_upper_bound(self):
        arr = [1, 2, 2, 2, 3, 5]
        # binary_search module bounds
        assert bs_lower_bound(arr, 2) == 1
        assert bs_upper_bound(arr, 2) == 4
        # advanced_search module bounds
        assert adv_lower_bound(arr, 2) == 1
        assert adv_upper_bound(arr, 2) == 4

    def test_binary_search_range(self):
        arr = [1, 2, 2, 2, 3, 5]
        assert binary_search_range(arr, 2) == [1, 3]
        assert binary_search_range(arr, 4) == [-1, -1]

    def test_binary_search_2d(self):
        matrix = [
            [1, 4, 7],
            [10, 13, 14],
            [20, 21, 30],
        ]
        assert binary_search_2d(matrix, 1) is True
        assert binary_search_2d(matrix, 14) is True
        assert binary_search_2d(matrix, 2) is False


class TestQuickselectFamily:
    def test_quickselect_smallest_largest(self):
        arr = [7, 10, 4, 3, 20, 15]
        # k is 1-indexed in typical kth semantics; quickselect here expects index-based?
        # The quickselect implementation signature is (a, k, smallest=True) -> int, where k is rank (1-based) by convention in this repo.
        assert quickselect(arr[:], 1, smallest=True) == min(arr)
        assert quickselect(arr[:], 2, smallest=True) == sorted(arr)[1]
        assert quickselect(arr[:], 1, smallest=False) == max(arr)
        assert quickselect(arr[:], 2, smallest=False) == sorted(arr, reverse=True)[1]

    def test_find_median(self):
        assert find_median([1, 3, 2, 4, 5]) == 3.0
        assert find_median([1, 2, 3, 4]) == 2.5


class TestAdvancedSearches:
    def test_search_rotated(self):
        nums = [4, 5, 6, 7, 0, 1, 2]
        assert search_rotated(nums, 0) == 4
        assert search_rotated(nums, 3) == -1

    def test_search_rotated_with_duplicates(self):
        nums = [2, 5, 6, 0, 0, 1, 2]
        assert search_rotated_with_duplicates(nums, 0) != -1
        assert search_rotated_with_duplicates(nums, 3) == -1

    def test_exponential_search(self):
        arr = list(range(0, 100, 2))  # even numbers
        assert exponential_search(arr, 0) == 0
        assert exponential_search(arr, 18) == 9
        assert exponential_search(arr, 99) == -1


if __name__ == "__main__":
    pytest.main([__file__])
