from typing import List


def merge_sort(a: List[int]) -> List[int]:
    """
    Stable O(n log n) sort via divide-and-conquer.

    Time: O(n log n) - always, regardless of input
    Space: O(n) - due to merging buffer and recursion stack

    Pitfalls:
    - Avoid excessive list slicing in tight loops for large n
    - Consider iterative bottom-up approach for lower recursion overhead
    - Not in-place, requires O(n) extra space

    Interview follow-ups:
    - How to make it in-place? (Complex, involves rotations)
    - How does it compare to quicksort? (Stable, guaranteed O(n log n), but uses more space)
    - When would you choose merge sort? (When stability is required, external sorting)
    """
    n = len(a)
    if n <= 1:
        return a[:]

    mid = n // 2
    left = merge_sort(a[:mid])
    right = merge_sort(a[mid:])
    return _merge(left, right)


def _merge(left: List[int], right: List[int]) -> List[int]:
    """Merge two sorted arrays into one sorted array."""
    i = j = 0
    result = []

    # Merge while both arrays have elements
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:  # <= ensures stability
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    # Add remaining elements
    result.extend(left[i:])
    result.extend(right[j:])
    return result


def merge_sort_inplace(a: List[int]) -> None:
    """
    In-place merge sort (modifies input array).
    Still requires O(n) auxiliary space for merging.
    """

    def merge_sort_helper(arr: List[int], temp: List[int], left: int, right: int):
        if left >= right:
            return

        mid = (left + right) // 2
        merge_sort_helper(arr, temp, left, mid)
        merge_sort_helper(arr, temp, mid + 1, right)
        merge_inplace(arr, temp, left, mid, right)

    def merge_inplace(arr: List[int], temp: List[int], left: int, mid: int, right: int):
        # Copy to temp array
        for i in range(left, right + 1):
            temp[i] = arr[i]

        i, j, k = left, mid + 1, left

        while i <= mid and j <= right:
            if temp[i] <= temp[j]:
                arr[k] = temp[i]
                i += 1
            else:
                arr[k] = temp[j]
                j += 1
            k += 1

        # Copy remaining elements
        while i <= mid:
            arr[k] = temp[i]
            i += 1
            k += 1
        while j <= right:
            arr[k] = temp[j]
            j += 1
            k += 1

    if len(a) <= 1:
        return

    temp = [0] * len(a)
    merge_sort_helper(a, temp, 0, len(a) - 1)


def demo():
    """Demo function for merge sort."""
    print("Merge Sort Demo")
    print("=" * 40)

    test_cases = [[5, 1, 4, 2, 8, 0, 2], [1], [], [3, 3, 3, 3], [5, 4, 3, 2, 1], list(range(10))]

    for i, arr in enumerate(test_cases):
        print(f"Test {i+1}: {arr}")
        sorted_arr = merge_sort(arr)
        print(f"Sorted:  {sorted_arr}")

        # Test in-place version
        arr_copy = arr[:]
        merge_sort_inplace(arr_copy)
        print(f"In-place: {arr_copy}")
        print()


if __name__ == "__main__":
    demo()
