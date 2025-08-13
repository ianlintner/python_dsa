from typing import List


def heap_sort(a: List[int]) -> List[int]:
    """
    In-place O(n log n) sort using binary heap. Not stable.

    Time: O(n log n) - always, regardless of input
    Space: O(1) - truly in-place (excluding output array copy)

    Advantages:
    - Guaranteed O(n log n) performance (no worst case like quicksort)
    - In-place sorting
    - Good for systems with memory constraints

    Disadvantages:
    - Not stable
    - Poor cache performance due to heap structure
    - Constant factors higher than quicksort

    Interview follow-ups:
    - How does heap structure work? (Complete binary tree in array)
    - Why not stable? (Long-distance swaps break relative order)
    - When to use over quicksort? (When guaranteed O(n log n) needed)
    """
    if len(a) <= 1:
        return a[:]

    arr = a[:]  # Keep original unchanged
    n = len(arr)

    # Build max heap (heapify)
    # Start from last non-leaf node and sift down
    for i in range(n // 2 - 1, -1, -1):
        _sift_down(arr, n, i)

    # Extract elements from heap one by one
    for end in range(n - 1, 0, -1):
        # Move current root (max) to end
        arr[0], arr[end] = arr[end], arr[0]

        # Restore heap property for reduced heap
        _sift_down(arr, end, 0)

    return arr


def _sift_down(a: List[int], heap_size: int, root: int):
    """
    Sift down element at root to maintain max heap property.

    Args:
        a: Array representing heap
        heap_size: Size of heap (may be less than array length)
        root: Index of element to sift down
    """
    while True:
        left = 2 * root + 1
        right = 2 * root + 2
        largest = root

        # Find largest among root and its children
        if left < heap_size and a[left] > a[largest]:
            largest = left

        if right < heap_size and a[right] > a[largest]:
            largest = right

        # If root is already largest, heap property satisfied
        if largest == root:
            break

        # Swap and continue sifting down
        a[root], a[largest] = a[largest], a[root]
        root = largest


def _sift_up(a: List[int], child: int):
    """
    Sift up element at child to maintain max heap property.
    Used when inserting new elements into heap.
    """
    while child > 0:
        parent = (child - 1) // 2

        if a[parent] >= a[child]:
            break

        a[parent], a[child] = a[child], a[parent]
        child = parent


def build_max_heap(a: List[int]) -> List[int]:
    """
    Build max heap from unsorted array.
    Time: O(n) - not O(n log n)!
    """
    arr = a[:]
    n = len(arr)

    # Start from last non-leaf and sift down
    for i in range(n // 2 - 1, -1, -1):
        _sift_down(arr, n, i)

    return arr


def heap_sort_min(a: List[int]) -> List[int]:
    """
    Heap sort using min heap (for descending order).
    """
    if len(a) <= 1:
        return a[:]

    arr = a[:]
    n = len(arr)

    # Build min heap
    for i in range(n // 2 - 1, -1, -1):
        _sift_down_min(arr, n, i)

    # Extract elements (will be in descending order)
    for end in range(n - 1, 0, -1):
        arr[0], arr[end] = arr[end], arr[0]
        _sift_down_min(arr, end, 0)

    return arr


def _sift_down_min(a: List[int], heap_size: int, root: int):
    """Sift down for min heap."""
    while True:
        left = 2 * root + 1
        right = 2 * root + 2
        smallest = root

        if left < heap_size and a[left] < a[smallest]:
            smallest = left

        if right < heap_size and a[right] < a[smallest]:
            smallest = right

        if smallest == root:
            break

        a[root], a[smallest] = a[smallest], a[root]
        root = smallest


def find_kth_largest(a: List[int], k: int) -> int:
    """
    Find kth largest element using heap.
    Alternative to quickselect.

    Time: O(n log k) using min heap of size k
    Space: O(k)
    """
    import heapq

    if k <= 0 or k > len(a):
        raise ValueError("k out of range")

    # Use min heap to keep k largest elements
    heap = []

    for num in a:
        if len(heap) < k:
            heapq.heappush(heap, num)
        elif num > heap[0]:
            heapq.heapreplace(heap, num)

    return heap[0]  # kth largest


def demo():
    """Demo function for heap sort."""
    print("Heap Sort Demo")
    print("=" * 40)

    test_cases = [
        [4, 10, 3, 5, 1],
        [1],
        [],
        [3, 3, 3, 3],
        [5, 4, 3, 2, 1],
        list(range(10)),
        [12, 11, 13, 5, 6, 7],
    ]

    for i, arr in enumerate(test_cases):
        print(f"Test {i+1}: {arr}")

        if arr:
            # Show heap building process
            heap = build_max_heap(arr)
            print(f"Max heap: {heap}")

        sorted_arr = heap_sort(arr)
        print(f"Sorted:   {sorted_arr}")

        # Test kth largest
        if arr and len(arr) >= 2:
            k = min(3, len(arr))
            kth = find_kth_largest(arr, k)
            print(f"{k}rd largest: {kth}")

        print()


if __name__ == "__main__":
    demo()
