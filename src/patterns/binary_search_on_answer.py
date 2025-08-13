from bisect import bisect_right
from typing import List


def ship_within_days(weights: List[int], days: int) -> int:
    """
    LeetCode 1011: Capacity To Ship Packages Within D Days.
    Binary search on capacity. Feasibility: greedy pack until overflow -> new day.

    Time: O(n log(sum(weights)))
    """
    lo = max(weights)  # capacity must be at least the max weight
    hi = sum(weights)  # and at most total weight

    def can_ship(cap: int) -> bool:
        d = 1
        cur = 0
        for w in weights:
            if cur + w <= cap:
                cur += w
            else:
                d += 1
                cur = w
                if d > days:
                    return False
        return True

    while lo < hi:
        mid = (lo + hi) // 2
        if can_ship(mid):
            hi = mid
        else:
            lo = mid + 1
    return lo


def min_eating_speed(piles: List[int], h: int) -> int:
    """
    LeetCode 875: Koko Eating Bananas.
    Binary search on speed k. Feasibility: sum(ceil(p/k)) <= h.

    Time: O(n log max(p))
    """
    import math

    lo, hi = 1, max(piles)

    def hours_needed(k: int) -> int:
        return sum((p + k - 1) // k for p in piles)  # integer ceil

    while lo < hi:
        mid = (lo + hi) // 2
        if hours_needed(mid) <= h:
            hi = mid
        else:
            lo = mid + 1
    return lo


def split_array_largest_sum(nums: List[int], m: int) -> int:
    """
    LeetCode 410: Split Array Largest Sum.
    Minimize the largest subarray sum by splitting into m parts. Binary search on answer.

    Time: O(n log sum(nums))
    """
    lo, hi = max(nums), sum(nums)

    def can_split(limit: int) -> bool:
        parts = 1
        cur = 0
        for x in nums:
            if cur + x <= limit:
                cur += x
            else:
                parts += 1
                cur = x
                if parts > m:
                    return False
        return True

    while lo < hi:
        mid = (lo + hi) // 2
        if can_split(mid):
            hi = mid
        else:
            lo = mid + 1
    return lo


def kth_smallest_in_sorted_matrix(matrix: List[List[int]], k: int) -> int:
    """
    LeetCode 378: Kth Smallest Element in a Sorted Matrix (rows and columns sorted).
    Binary search on value domain [min, max]. Counting <= mid per row via upper_bound.

    Time: O(n log(max-min)) with O(n log n) per check (or O(n) with two-pointer count)
    """
    n = len(matrix)
    if n == 0 or len(matrix[0]) == 0:
        raise ValueError("Empty matrix")
    lo, hi = matrix[0][0], matrix[-1][-1]

    def count_le(x: int) -> int:
        # Count elements <= x using per-row upper_bound
        cnt = 0
        for row in matrix:
            # bisect_right returns index of first > x, which equals count <= x
            cnt += bisect_right(row, x)
        return cnt

    while lo < hi:
        mid = (lo + hi) // 2
        if count_le(mid) >= k:
            hi = mid
        else:
            lo = mid + 1
    return lo


def demo():
    print("Binary Search on Answer Demo")
    print("=" * 40)

    # Ship within days
    weights = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    days = 5
    print(
        f"Ship within {days} days, weights={weights}: capacity = {ship_within_days(weights, days)}"
    )
    print()

    # Koko eating bananas
    piles = [3, 6, 7, 11]
    h = 8
    print(f"Koko min speed to finish in {h} hours, piles={piles}: {min_eating_speed(piles, h)}")
    print()

    # Split array largest sum
    nums = [7, 2, 5, 10, 8]
    m = 2
    print(
        f"Split array {nums} into {m} parts, min largest sum = {split_array_largest_sum(nums, m)}"
    )
    print()

    # Kth smallest in sorted matrix
    matrix = [[1, 5, 9], [10, 11, 13], [12, 13, 15]]
    k = 8
    print(f"{k}-th smallest in matrix: {kth_smallest_in_sorted_matrix(matrix, k)}")
    print()

    print("Notes & Interview Tips:")
    print(
        "  - When decision is monotonic (feasible/not), binary search the minimal feasible answer."
    )
    print("  - Feasibility checks are typically greedy or counting based.")
    print(
        "  - Common problems: capacity constraints, speed rates, subdivision limits, kth value in range."
    )


if __name__ == "__main__":
    demo()
