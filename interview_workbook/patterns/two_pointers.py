from typing import List, Tuple

def two_sum_sorted(nums: List[int], target: int) -> Tuple[int, int]:
    """
    Given a sorted array nums, return 0-based indices (i, j) such that nums[i] + nums[j] = target.
    If none exists, return (-1, -1).

    Time: O(n)  Space: O(1)
    """
    i, j = 0, len(nums) - 1
    while i < j:
        s = nums[i] + nums[j]
        if s == target:
            return i, j
        if s < target:
            i += 1
        else:
            j -= 1
    return -1, -1


def three_sum(nums: List[int]) -> List[List[int]]:
    """
    Return all unique triplets [a,b,c] such that a+b+c=0.
    Uses sorting + 2-pointer inner loop.

    Time: O(n^2)  Space: O(1) extra (excluding output)
    """
    nums.sort()
    n = len(nums)
    res: List[List[int]] = []
    for i in range(n):
        if i > 0 and nums[i] == nums[i - 1]:
            continue
        a = nums[i]
        l, r = i + 1, n - 1
        while l < r:
            s = a + nums[l] + nums[r]
            if s == 0:
                res.append([a, nums[l], nums[r]])
                l += 1
                while l < r and nums[l] == nums[l - 1]:
                    l += 1
                r -= 1
                while l < r and nums[r] == nums[r + 1]:
                    r -= 1
            elif s < 0:
                l += 1
            else:
                r -= 1
    return res


def container_with_most_water(height: List[int]) -> int:
    """
    LeetCode 11: Container With Most Water.
    Two pointers maximize area by moving the smaller pointer inward.

    Time: O(n)  Space: O(1)
    """
    i, j = 0, len(height) - 1
    best = 0
    while i < j:
        h = min(height[i], height[j])
        best = max(best, h * (j - i))
        if height[i] < height[j]:
            i += 1
        else:
            j -= 1
    return best


def remove_duplicates_sorted(nums: List[int]) -> int:
    """
    LeetCode 26: Remove Duplicates from Sorted Array (in-place).
    Returns new length k, with first k elements unique.

    Time: O(n)  Space: O(1)
    """
    if not nums:
        return 0
    k = 1
    for i in range(1, len(nums)):
        if nums[i] != nums[k - 1]:
            nums[k] = nums[i]
            k += 1
    return k


def merge_intervals(intervals: List[List[int]]) -> List[List[int]]:
    """
    Merge overlapping intervals.
    Sort by start, then iterate and merge if current start <= last end.

    Time: O(n log n) for sort, O(n) merge pass
    """
    if not intervals:
        return []
    intervals.sort(key=lambda x: x[0])
    merged: List[List[int]] = [intervals[0][:]]
    for s, e in intervals[1:]:
        last = merged[-1]
        if s <= last[1]:
            last[1] = max(last[1], e)
        else:
            merged.append([s, e])
    return merged


def demo():
    print("Two-Pointers Patterns Demo")
    print("=" * 40)

    # two_sum_sorted
    arr = [1, 2, 3, 4, 6, 8, 11]
    target = 10
    i, j = two_sum_sorted(arr, target)
    print(f"two_sum_sorted({arr}, {target}) -> indices=({i},{j}), values=({arr[i] if i!=-1 else None},{arr[j] if j!=-1 else None})")
    print()

    # three_sum
    arr2 = [-1, 0, 1, 2, -1, -4]
    triplets = three_sum(arr2)
    print(f"three_sum([-1,0,1,2,-1,-4]) -> {triplets}")
    print()

    # container with most water
    height = [1,8,6,2,5,4,8,3,7]
    print(f"container_with_most_water({height}) -> {container_with_most_water(height)}")
    print()

    # remove duplicates from sorted
    a = [0,0,1,1,1,2,2,3,3,4]
    k = remove_duplicates_sorted(a)
    print(f"remove_duplicates_sorted -> new length {k}, array[:k]={a[:k]}")
    print()

    # merge intervals
    intervals = [[1,3],[2,6],[8,10],[15,18]]
    print(f"merge_intervals({intervals}) -> {merge_intervals(intervals)}")
    print()

    print("Notes & Interview Tips:")
    print("  - Two pointers excel when the array is sorted or when shrinking/expanding ranges.")
    print("  - For unique triplets, skip duplicates after moving pointers.")
    print("  - For interval merging, always sort by start and track last merged interval.")


if __name__ == "__main__":
    demo()
