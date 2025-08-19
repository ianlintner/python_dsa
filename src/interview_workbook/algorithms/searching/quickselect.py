import random


def quickselect(a: list[int], k: int, smallest: bool = True) -> int:
    """
    Find kth order statistic using quickselect algorithm.

    Time: O(n) average, O(n^2) worst case
    Space: O(1) iterative, O(log n) recursive average

    Args:
        a: Input array (will be modified)
        k: 1-indexed rank (1 = smallest/largest element)
        smallest: If True, find kth smallest; if False, find kth largest

    Returns: kth order statistic

    Pitfalls:
    - Array gets modified (not pure function)
    - Worst case O(n^2) with bad pivot selection
    - Off-by-one errors with k indexing

    Interview follow-ups:
    - How to make it stable? (Use auxiliary array with indices)
    - How to find median? (k = n//2)
    - How to find multiple order statistics efficiently? (Use selection tree)
    """
    if not 1 <= k <= len(a):
        raise IndexError(f"k={k} out of range for array of length {len(a)}")

    # Convert 1-indexed rank to 0-indexed target position for kth smallest
    target_k = (k - 1) if smallest else (len(a) - k)

    lo, hi = 0, len(a) - 1

    while lo < hi:
        pivot_idx = _partition_random(a, lo, hi)

        if pivot_idx == target_k:
            return a[pivot_idx]
        elif pivot_idx < target_k:
            lo = pivot_idx + 1
        else:
            hi = pivot_idx - 1

    return a[lo]


def _partition_random(a: list[int], lo: int, hi: int) -> int:
    """Lomuto partition with random pivot selection."""
    # Randomize pivot to avoid worst case
    pivot_idx = random.randint(lo, hi)
    a[pivot_idx], a[hi] = a[hi], a[pivot_idx]

    pivot = a[hi]
    i = lo

    for j in range(lo, hi):
        if a[j] <= pivot:
            a[i], a[j] = a[j], a[i]
            i += 1

    a[i], a[hi] = a[hi], a[i]
    return i


def quickselect_recursive(a: list[int], k: int, lo: int = 0, hi: int = None) -> int:
    """Recursive implementation of quickselect."""
    if hi is None:
        hi = len(a) - 1

    if lo == hi:
        return a[lo]

    pivot_idx = _partition_random(a, lo, hi)

    if k == pivot_idx:
        return a[k]
    elif k < pivot_idx:
        return quickselect_recursive(a, k, lo, pivot_idx - 1)
    else:
        return quickselect_recursive(a, k, pivot_idx + 1, hi)


def find_median(a: list[int]) -> float:
    """
    Find median using quickselect.

    Time: O(n) average
    Returns: Median value (float for even-length arrays)
    """
    arr = a[:]  # Don't modify original
    n = len(arr)

    if n == 0:
        raise ValueError("Cannot find median of empty array")

    if n % 2 == 1:
        # Odd length: return middle element (rank = n//2 + 1)
        return float(quickselect(arr, n // 2 + 1))
    else:
        # Even length: average of two middle elements (ranks n//2 and n//2 + 1)
        mid1 = quickselect(arr, n // 2)
        # Need fresh copy since quickselect modifies array
        arr2 = a[:]
        mid2 = quickselect(arr2, n // 2 + 1)
        return (mid1 + mid2) / 2.0


def find_kth_largest_heap(a: list[int], k: int) -> int:
    """
    Alternative: Find kth largest using min heap.

    Time: O(n log k)
    Space: O(k)

    Better than quickselect when k << n.
    """
    import heapq

    if k <= 0 or k > len(a):
        raise ValueError("k out of range")

    # Maintain min heap of k largest elements
    heap = []

    for num in a:
        if len(heap) < k:
            heapq.heappush(heap, num)
        elif num > heap[0]:
            heapq.heapreplace(heap, num)

    return heap[0]


def find_kth_smallest_heap(a: list[int], k: int) -> int:
    """
    Find kth smallest using max heap.

    Time: O(n log k)
    Space: O(k)
    """
    import heapq

    if k <= 0 or k > len(a):
        raise ValueError("k out of range")

    # Maintain max heap of k smallest elements (negate values)
    heap = []

    for num in a:
        if len(heap) < k:
            heapq.heappush(heap, -num)
        elif num < -heap[0]:
            heapq.heapreplace(heap, -num)

    return -heap[0]


def median_of_medians(a: list[int], k: int) -> int:
    """
    Deterministic O(n) selection using median-of-medians pivot.

    Guarantees O(n) worst-case time by choosing good pivot.
    More complex but theoretically optimal.
    """

    def select(arr: list[int], left: int, right: int, k: int) -> int:
        if left == right:
            return arr[left]

        # Divide into groups of 5
        groups = []
        for i in range(left, right + 1, 5):
            group = arr[i : min(i + 5, right + 1)]
            group.sort()
            groups.append(group[len(group) // 2])  # Median of group

        # Find median of medians
        if len(groups) == 1:
            pivot = groups[0]
        else:
            pivot = select(groups, 0, len(groups) - 1, len(groups) // 2)

        # Partition around pivot
        pivot_idx = partition_around_value(arr, left, right, pivot)

        if k == pivot_idx:
            return arr[k]
        elif k < pivot_idx:
            return select(arr, left, pivot_idx - 1, k)
        else:
            return select(arr, pivot_idx + 1, right, k)

    def partition_around_value(arr: list[int], left: int, right: int, pivot_val: int) -> int:
        # Find pivot and move to end
        for i in range(left, right + 1):
            if arr[i] == pivot_val:
                arr[i], arr[right] = arr[right], arr[i]
                break

        # Standard partition
        i = left
        for j in range(left, right):
            if arr[j] <= pivot_val:
                arr[i], arr[j] = arr[j], arr[i]
                i += 1

        arr[i], arr[right] = arr[right], arr[i]
        return i

    arr = a[:]
    return select(arr, 0, len(arr) - 1, k)


def demo():
    """Demo function for quickselect variants."""
    print("Quickselect Demo")
    print("=" * 40)

    test_arrays = [
        [3, 2, 1, 5, 6, 4],
        [3, 2, 3, 1, 2, 4, 5, 5, 6],
        [1],
        [7, 10, 4, 3, 20, 15],
        list(range(10, 0, -1)),  # Reverse sorted
    ]

    for i, arr in enumerate(test_arrays):
        print(f"Test {i + 1}: {arr}")
        sorted_arr = sorted(arr)
        print(f"Sorted: {sorted_arr}")

        # Test various ranks (1-indexed)
        for rank in [1, len(arr) // 2 + 1, len(arr)]:
            # Test quickselect (modifies array)
            arr_copy = arr[:]
            kth_smallest = quickselect(arr_copy, rank, smallest=True)

            arr_copy = arr[:]
            kth_largest = quickselect(arr_copy, rank, smallest=False)

            # Test heap-based alternatives (also 1-indexed)
            kth_smallest_heap = find_kth_smallest_heap(arr, rank)
            kth_largest_heap = find_kth_largest_heap(arr, rank)

            print(f"  rank={rank}: {rank}th smallest = {kth_smallest} (heap: {kth_smallest_heap})")
            print(f"  rank={rank}: {rank}th largest = {kth_largest} (heap: {kth_largest_heap})")

        # Test median
        try:
            median = find_median(arr)
            print(f"  Median: {median}")
        except ValueError as e:
            print(f"  Median: {e}")

        print()


if __name__ == "__main__":
    demo()
