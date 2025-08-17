from bisect import bisect_left


def subset_sum_mitm(nums: list[int], target: int) -> bool:
    """
    Meet-in-the-middle subset sum existence.
    Splits nums into two halves, enumerates all subset sums for each half,
    and checks if any pair sums to target.

    Time: O(2^(n/2) log 2^(n/2)) ~ O(2^(n/2) * n)
    Space: O(2^(n/2))
    """
    n = len(nums)
    mid = n // 2
    left = nums[:mid]
    right = nums[mid:]

    left_sums = []
    for mask in range(1 << len(left)):
        s = 0
        for i in range(len(left)):
            if mask & (1 << i):
                s += left[i]
        left_sums.append(s)

    right_sums = []
    for mask in range(1 << len(right)):
        s = 0
        for i in range(len(right)):
            if mask & (1 << i):
                s += right[i]
        right_sums.append(s)

    right_sums.sort()
    for s in left_sums:
        need = target - s
        j = bisect_left(right_sums, need)
        if j < len(right_sums) and right_sums[j] == need:
            return True
    return False


def subset_sum_mitm_count(nums: list[int], target: int) -> int:
    """
    Count the number of subsets whose sum equals target using meet-in-the-middle.
    """
    n = len(nums)
    mid = n // 2
    left = nums[:mid]
    right = nums[mid:]

    left_sums = []
    for mask in range(1 << len(left)):
        s = 0
        for i in range(len(left)):
            if mask & (1 << i):
                s += left[i]
        left_sums.append(s)

    from collections import Counter

    right_sums = []
    for mask in range(1 << len(right)):
        s = 0
        for i in range(len(right)):
            if mask & (1 << i):
                s += right[i]
        right_sums.append(s)

    right_count = Counter(right_sums)
    total = 0
    for s in left_sums:
        total += right_count[target - s]
    return total


def subset_sum_mitm_closest(nums: list[int]) -> tuple[int, int]:
    """
    Partition nums into two groups with sum as close as possible.
    Returns (sumA, sumB) with |sumA - sumB| minimized.
    Uses meet-in-the-middle to find closest to total//2.

    Useful variant: min difference partition.
    """
    total = sum(nums)
    target = total // 2

    n = len(nums)
    mid = n // 2
    left = nums[:mid]
    right = nums[mid:]

    left_sums = []
    for mask in range(1 << len(left)):
        s = 0
        for i in range(len(left)):
            if mask & (1 << i):
                s += left[i]
        left_sums.append(s)

    right_sums = []
    for mask in range(1 << len(right)):
        s = 0
        for i in range(len(right)):
            if mask & (1 << i):
                s += right[i]
        right_sums.append(s)

    right_sums.sort()
    best_sumA = 0

    from bisect import bisect_right

    for s in left_sums:
        # choose t in right_sums such that s + t is as close as possible to target
        rem = target - s
        j = bisect_right(right_sums, rem)
        candidates = []
        if j < len(right_sums):
            candidates.append(right_sums[j])
        if j - 1 >= 0:
            candidates.append(right_sums[j - 1])
        for t in candidates:
            cur = s + t
            if abs(cur - target) < abs(best_sumA - target):
                best_sumA = cur

    sumA = best_sumA
    sumB = total - sumA
    return sumA, sumB


def demo():
    print("Meet-in-the-Middle Patterns Demo")
    print("=" * 40)

    nums = [3, 34, 4, 12, 5, 2]
    target = 9
    print(f"Subset sum existence: nums={nums}, target={target}")
    print("  Exists? ->", subset_sum_mitm(nums, target))
    print()

    nums2 = [1, 2, 3, 4, 5]
    target2 = 7
    cnt = subset_sum_mitm_count(nums2, target2)
    print(f"Count subsets equal to {target2} in {nums2}: {cnt}")
    print()

    nums3 = [3, 1, 4, 2, 2, 1]
    a, b = subset_sum_mitm_closest(nums3)
    print(f"Min-diff partition of {nums3}: sums = ({a}, {b}), diff = {abs(a - b)}")
    print()

    print("Notes & Interview Tips:")
    print("  - Meet-in-the-middle splits n into n/2 + n/2 to reduce O(2^n) to ~O(2^(n/2)).")
    print("  - Useful when n ~ 30-40 where pure backtracking is too slow.")
    print("  - Combine with sorting + binary search or hash maps for counts.")


if __name__ == "__main__":
    demo()
