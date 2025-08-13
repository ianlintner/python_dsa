from typing import Sequence, Optional

def binary_search(a: Sequence[int], target: int) -> int:
    """
    Standard binary search in sorted array.
    
    Time: O(log n)
    Space: O(1)
    
    Returns: Index of target if found, -1 otherwise
    
    Pitfalls:
    - Array must be sorted
    - Integer overflow in (lo + hi) // 2 for very large arrays
    - Off-by-one errors in loop conditions
    
    Interview follow-ups:
    - How to handle duplicates? (Use lower_bound/upper_bound)
    - What if array is rotated? (Modified binary search)
    - How to search in infinite array? (Exponential search + binary search)
    """
    lo, hi = 0, len(a) - 1
    
    while lo <= hi:
        mid = lo + (hi - lo) // 2  # Avoid overflow
        
        if a[mid] == target:
            return mid
        elif a[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1
    
    return -1

def binary_search_recursive(a: Sequence[int], target: int, lo: int = 0, hi: Optional[int] = None) -> int:
    """Recursive implementation of binary search."""
    if hi is None:
        hi = len(a) - 1
    
    if lo > hi:
        return -1
    
    mid = lo + (hi - lo) // 2
    
    if a[mid] == target:
        return mid
    elif a[mid] < target:
        return binary_search_recursive(a, target, mid + 1, hi)
    else:
        return binary_search_recursive(a, target, lo, mid - 1)

def lower_bound(a: Sequence[int], target: int) -> int:
    """
    Find first position where target could be inserted to keep array sorted.
    Returns first index i where a[i] >= target, or len(a) if no such index.
    
    Also known as "leftmost insertion point" or "first occurrence".
    """
    lo, hi = 0, len(a)
    
    while lo < hi:
        mid = lo + (hi - lo) // 2
        
        if a[mid] < target:
            lo = mid + 1
        else:
            hi = mid
    
    return lo

def upper_bound(a: Sequence[int], target: int) -> int:
    """
    Find first position after target where element could be inserted.
    Returns first index i where a[i] > target, or len(a) if no such index.
    
    Also known as "rightmost insertion point" or "after last occurrence".
    """
    lo, hi = 0, len(a)
    
    while lo < hi:
        mid = lo + (hi - lo) // 2
        
        if a[mid] <= target:
            lo = mid + 1
        else:
            hi = mid
    
    return lo

def find_first_occurrence(a: Sequence[int], target: int) -> int:
    """Find first occurrence of target in sorted array with duplicates."""
    idx = lower_bound(a, target)
    return idx if idx < len(a) and a[idx] == target else -1

def find_last_occurrence(a: Sequence[int], target: int) -> int:
    """Find last occurrence of target in sorted array with duplicates."""
    idx = upper_bound(a, target) - 1
    return idx if idx >= 0 and a[idx] == target else -1

def count_occurrences(a: Sequence[int], target: int) -> int:
    """Count occurrences of target in sorted array."""
    left = lower_bound(a, target)
    right = upper_bound(a, target)
    return right - left

def binary_search_range(a: Sequence[int], target: int) -> tuple[int, int]:
    """
    Find range [start, end] of target in sorted array.
    Returns [-1, -1] if target not found.
    
    LeetCode 34: Find First and Last Position of Element in Sorted Array
    """
    left = find_first_occurrence(a, target)
    if left == -1:
        return [-1, -1]
    
    right = find_last_occurrence(a, target)
    return [left, right]

def binary_search_2d(matrix: list[list[int]], target: int) -> bool:
    """
    Search in 2D matrix where:
    - Each row is sorted left to right
    - First element of each row > last element of previous row
    
    Time: O(log(m*n)) where m=rows, n=cols
    """
    if not matrix or not matrix[0]:
        return False
    
    m, n = len(matrix), len(matrix[0])
    lo, hi = 0, m * n - 1
    
    while lo <= hi:
        mid = lo + (hi - lo) // 2
        row, col = divmod(mid, n)
        val = matrix[row][col]
        
        if val == target:
            return True
        elif val < target:
            lo = mid + 1
        else:
            hi = mid - 1
    
    return False

def search_insert_position(a: Sequence[int], target: int) -> int:
    """
    Find position where target should be inserted in sorted array.
    Same as lower_bound.
    
    LeetCode 35: Search Insert Position
    """
    return lower_bound(a, target)

def demo():
    """Demo function for binary search variants."""
    print("Binary Search Demo")
    print("=" * 40)
    
    # Test basic binary search
    arr = [1, 2, 2, 3, 5, 7, 8, 9]
    print(f"Array: {arr}")
    
    for target in [2, 5, 6, 0, 10]:
        idx = binary_search(arr, target)
        print(f"Search {target}: index {idx}")
    
    print()
    
    # Test bounds with duplicates
    arr_dup = [1, 2, 2, 2, 3, 3, 5, 7]
    print(f"Array with duplicates: {arr_dup}")
    
    target = 2
    lb = lower_bound(arr_dup, target)
    ub = upper_bound(arr_dup, target)
    first = find_first_occurrence(arr_dup, target)
    last = find_last_occurrence(arr_dup, target)
    count = count_occurrences(arr_dup, target)
    
    print(f"Target {target}:")
    print(f"  Lower bound: {lb}")
    print(f"  Upper bound: {ub}")
    print(f"  First occurrence: {first}")
    print(f"  Last occurrence: {last}")
    print(f"  Count: {count}")
    print(f"  Range: {binary_search_range(arr_dup, target)}")
    
    print()
    
    # Test 2D search
    matrix = [
        [1,  4,  7,  11],
        [2,  5,  8,  12],
        [3,  6,  9,  16],
        [10, 13, 14, 17]
    ]
    print("2D Matrix search:")
    for target in [5, 11, 13, 20]:
        found = binary_search_2d(matrix, target)
        print(f"  Search {target}: {found}")

if __name__ == "__main__":
    demo()
