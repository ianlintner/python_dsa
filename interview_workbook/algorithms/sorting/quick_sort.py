from typing import List
import random

def quick_sort(a: List[int]) -> List[int]:
    """
    Average O(n log n), worst-case O(n^2). Not stable. Can be in-place.
    
    Time: O(n log n) average, O(n^2) worst case
    Space: O(log n) average (recursion stack), O(n) worst case
    
    Pitfalls:
    - Worst case O(n^2) when pivot is always min/max (sorted input)
    - Not stable - equal elements may be reordered
    - Stack overflow on deeply nested recursion for worst case
    
    Mitigations:
    - Randomized pivot selection
    - Median-of-three pivot selection
    - Hybrid approach (switch to insertion sort for small subarrays)
    - Iterative implementation to avoid stack overflow
    
    Interview follow-ups:
    - How to handle duplicates efficiently? (3-way partitioning)
    - When does quicksort perform poorly? (Already sorted, many duplicates)
    - How to make it stable? (Use auxiliary array, but loses in-place benefit)
    """
    if len(a) <= 1:
        return a[:]
    
    arr = a[:]  # Keep original unchanged
    _quicksort_recursive(arr, 0, len(arr) - 1)
    return arr

def _quicksort_recursive(a: List[int], lo: int, hi: int):
    """Recursive quicksort helper."""
    if lo >= hi:
        return
    
    # Use randomized pivot to avoid worst case
    pivot_idx = _partition_hoare_random(a, lo, hi)
    _quicksort_recursive(a, lo, pivot_idx)
    _quicksort_recursive(a, pivot_idx + 1, hi)

def _partition_hoare_random(a: List[int], lo: int, hi: int) -> int:
    """
    Hoare partition scheme with randomized pivot.
    Returns partition index where left side <= pivot, right side >= pivot.
    """
    # Randomize pivot to avoid worst case
    pivot_idx = random.randint(lo, hi)
    a[lo], a[pivot_idx] = a[pivot_idx], a[lo]
    
    pivot = a[lo]
    i, j = lo - 1, hi + 1
    
    while True:
        # Move i right until we find element >= pivot
        i += 1
        while a[i] < pivot:
            i += 1
        
        # Move j left until we find element <= pivot
        j -= 1
        while a[j] > pivot:
            j -= 1
        
        # If pointers crossed, we're done
        if i >= j:
            return j
        
        # Swap elements
        a[i], a[j] = a[j], a[i]

def _partition_lomuto(a: List[int], lo: int, hi: int) -> int:
    """
    Lomuto partition scheme (simpler but does more swaps).
    Returns partition index where left side <= pivot, right side > pivot.
    """
    # Choose last element as pivot
    pivot = a[hi]
    i = lo  # Index of smaller element
    
    for j in range(lo, hi):
        if a[j] <= pivot:
            a[i], a[j] = a[j], a[i]
            i += 1
    
    a[i], a[hi] = a[hi], a[i]
    return i

def quick_sort_3way(a: List[int]) -> List[int]:
    """
    3-way quicksort for handling many duplicate keys efficiently.
    Partitions into: < pivot, = pivot, > pivot
    
    Time: O(n log n) average, O(n) when all elements equal
    """
    if len(a) <= 1:
        return a[:]
    
    arr = a[:]
    _quicksort_3way_recursive(arr, 0, len(arr) - 1)
    return arr

def _quicksort_3way_recursive(a: List[int], lo: int, hi: int):
    """3-way quicksort recursive helper."""
    if lo >= hi:
        return
    
    lt, gt = _partition_3way(a, lo, hi)
    _quicksort_3way_recursive(a, lo, lt - 1)
    _quicksort_3way_recursive(a, gt + 1, hi)

def _partition_3way(a: List[int], lo: int, hi: int) -> tuple[int, int]:
    """
    3-way partition: a[lo..lt-1] < pivot, a[lt..gt] = pivot, a[gt+1..hi] > pivot
    Returns (lt, gt) indices.
    """
    pivot = a[lo]
    i, lt, gt = lo, lo, hi
    
    while i <= gt:
        if a[i] < pivot:
            a[lt], a[i] = a[i], a[lt]
            lt += 1
            i += 1
        elif a[i] > pivot:
            a[i], a[gt] = a[gt], a[i]
            gt -= 1
            # Don't increment i, need to check swapped element
        else:
            i += 1
    
    return lt, gt

def quick_sort_iterative(a: List[int]) -> List[int]:
    """
    Iterative quicksort to avoid recursion stack overflow.
    Uses explicit stack to simulate recursion.
    """
    if len(a) <= 1:
        return a[:]
    
    arr = a[:]
    stack = [(0, len(arr) - 1)]
    
    while stack:
        lo, hi = stack.pop()
        if lo >= hi:
            continue
        
        pivot_idx = _partition_hoare_random(arr, lo, hi)
        stack.append((lo, pivot_idx))
        stack.append((pivot_idx + 1, hi))
    
    return arr

def demo():
    """Demo function for quick sort variants."""
    print("Quick Sort Demo")
    print("=" * 40)
    
    test_cases = [
        [3, 6, 8, 10, 1, 2, 1],
        [5, 4, 3, 2, 1],  # Worst case for naive pivot
        [1, 1, 1, 1, 1],  # Many duplicates
        [1],
        [],
        list(range(10)),
        [5, 2, 8, 2, 9, 1, 2, 2]  # Many duplicates mixed
    ]
    
    for i, arr in enumerate(test_cases):
        print(f"Test {i+1}: {arr}")
        
        # Test different variants
        result1 = quick_sort(arr)
        result2 = quick_sort_3way(arr)
        result3 = quick_sort_iterative(arr)
        
        print(f"Standard:   {result1}")
        print(f"3-way:      {result2}")
        print(f"Iterative:  {result3}")
        print()

if __name__ == "__main__":
    demo()
