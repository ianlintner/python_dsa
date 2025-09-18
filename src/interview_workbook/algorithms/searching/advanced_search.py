from __future__ import annotations

from collections.abc import Callable


def lower_bound(arr: list[int], target: int) -> int:
    """
    Return the first index i such that arr[i] >= target.
    If all elements are smaller, returns len(arr).

    Time: O(log n)
    """
    lo, hi = 0, len(arr)
    while lo < hi:
        mid = (lo + hi) // 2
        if arr[mid] < target:
            lo = mid + 1
        else:
            hi = mid
    return lo


def upper_bound(arr: list[int], target: int) -> int:
    """
    Return the first index i such that arr[i] > target.
    If all elements are <= target, returns len(arr).

    Time: O(log n)
    """
    lo, hi = 0, len(arr)
    while lo < hi:
        mid = (lo + hi) // 2
        if arr[mid] <= target:
            lo = mid + 1
        else:
            hi = mid
    return lo


def search_rotated(nums: list[int], target: int) -> int:
    """
    Search in rotated sorted array without duplicates.
    Returns index or -1 if not found.

    Time: O(log n)
    LeetCode 33
    """
    lo, hi = 0, len(nums) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if nums[mid] == target:
            return mid
        # Left half sorted
        if nums[lo] <= nums[mid]:
            if nums[lo] <= target < nums[mid]:
                hi = mid - 1
            else:
                lo = mid + 1
        else:
            # Right half sorted
            if nums[mid] < target <= nums[hi]:
                lo = mid + 1
            else:
                hi = mid - 1
    return -1


def search_rotated_with_duplicates(nums: list[int], target: int) -> int:
    """
    Search in rotated sorted array with duplicates.
    Returns index of one occurrence or -1 if not found.

    Time: O(log n) average, O(n) worst-case due to duplicates
    LeetCode 81
    """
    lo, hi = 0, len(nums) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if nums[mid] == target:
            return mid
        # Skip duplicates that break ordering detection
        if nums[lo] == nums[mid] == nums[hi]:
            lo += 1
            hi -= 1
            continue
        # Left half sorted
        if nums[lo] <= nums[mid]:
            if nums[lo] <= target < nums[mid]:
                hi = mid - 1
            else:
                lo = mid + 1
        else:
            # Right half sorted
            if nums[mid] < target <= nums[hi]:
                lo = mid + 1
            else:
                hi = mid - 1
    return -1


def exponential_search(arr: list[int], target: int) -> int:
    """
    Exponential search for sorted arrays: find range where target may lie, then binary search.

    Time: O(log i) where i is index of target
    """
    n = len(arr)
    if n == 0:
        return -1
    if arr[0] == target:
        return 0
    bound = 1
    while bound < n and arr[bound] < target:
        bound *= 2
    lo = bound // 2
    hi = min(bound, n - 1)
    # Standard binary search in [lo, hi]
    while lo <= hi:
        mid = (lo + hi) // 2
        if arr[mid] == target:
            return mid
        if arr[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return -1


def search_unknown_size(get: Callable[[int], int | None], target: int) -> int:
    """
    Search in an infinite/unknown-size sorted array through an accessor:
      get(i) -> value at index i or None if out-of-bounds.

    Returns index or -1 if not found.

    Strategy:
      - Exponentially expand high bound until get(hi) is None or >= target
      - Binary search between (lo, hi)

    Time: O(log index_of_target)
    """
    # Handle empty or initial None
    first = get(0)
    if first is None:
        return -1
    if first == target:
        return 0

    # Exponentially grow hi
    lo, hi = 0, 1
    while True:
        val = get(hi)
        if val is None or val >= target:
            break
        lo = hi
        hi *= 2

    # Binary search with safe getter
    while lo <= hi:
        mid = (lo + hi) // 2
        val = get(mid)
        if val is None or val > target:
            hi = mid - 1
        elif val < target:
            lo = mid + 1
        else:
            return mid
    return -1


class UnknownSizeArray:
    """
    Helper wrapper to simulate unknown-size access pattern on a Python list.
    get(i) returns arr[i] if 0 <= i < len(arr), else None.
    """

    def __init__(self, arr: list[int]):
        self.arr = arr

    def get(self, i: int) -> int | None:
        if 0 <= i < len(self.arr):
            return self.arr[i]
        return None


def demo():
    print("Advanced Searching Demo")
    print("=" * 40)

    # lower/upper bound
    arr = [1, 2, 2, 2, 3, 5, 7]
    print("Array:", arr)
    t = 2
    lb = lower_bound(arr, t)
    ub = upper_bound(arr, t)
    print(f"lower_bound({t}) = {lb} -> arr[{lb}:{ub}] = {arr[lb:ub]}")
    print(f"upper_bound({t}) = {ub}")
    print()

    # search rotated
    rotated = [4, 5, 6, 7, 0, 1, 2]
    for target in [0, 3, 7, 6]:
        idx = search_rotated(rotated, target)
        print(f"search_rotated({target}) in {rotated} -> {idx}")
    print()

    # search rotated with duplicates
    rotated_dup = [2, 5, 6, 0, 0, 1, 2]
    for target in [0, 3]:
        idx = search_rotated_with_duplicates(rotated_dup, target)
        print(f"search_rotated_with_duplicates({target}) in {rotated_dup} -> {idx}")
    print()

    # exponential search
    big_sorted = list(range(0, 100, 3))  # 0,3,6,9,...
    for target in [0, 9, 51, 99, 100]:
        idx = exponential_search(big_sorted, target)
        print(f"exponential_search({target}) -> {idx}")
    print()

    # unknown size search
    unknown = UnknownSizeArray(list(range(0, 1000, 7)))  # multiples of 7
    for target in [0, 14, 999, 994, 7]:
        idx = search_unknown_size(unknown.get, target)
        print(f"search_unknown_size({target}) -> {idx}")
    print()

    print("Notes & Interview Tips:")
    print("  - lower_bound/upper_bound useful for frequency and insertion points.")
    print("  - Rotated array search chooses the sorted half each step.")
    print("  - With duplicates, worst case degrades to O(n).")
    print("  - Unknown size arrays: exponential range expansion, then binary search.")
    print("  - Exponential search is useful for unbounded or very large arrays.")


if __name__ == "__main__":
    demo()
