from typing import List, TypeVar, Callable, Optional

T = TypeVar("T")


def insertion_sort(a: List[T], key: Optional[Callable[[T], object]] = None) -> List[T]:
    """
    Insertion Sort (stable).

    Idea:
      - Build the sorted array one element at a time by inserting current element
        into the correct position of the already-sorted prefix.
      - Good for small arrays and nearly-sorted inputs.

    Time:
      - Best: O(n) (already sorted)
      - Average/Worst: O(n^2)

    Space:
      - O(1) extra (sorting copy, algorithm is in-place on that copy)

    Stability:
      - Stable (equal elements keep original relative order)

    Pitfalls:
      - O(n^2) worst-case makes it unsuitable for large random arrays.
      - Useful as a base case for hybrid algorithms (e.g., quick/merge sort switch to
        insertion sort when subarray size is small).

    Parameters:
      - a: List of items to sort (will not be mutated)
      - key: Optional callable mapping item to a sortable key (like sorted(..., key=...))

    Returns:
      A new sorted list.

    Example:
      insertion_sort([3, 1, 2]) -> [1, 2, 3]
      insertion_sort([("a", 2), ("b", 1)], key=lambda x: x[1]) -> [("b",1), ("a",2)]
    """
    if len(a) <= 1:
        return a[:]

    arr = a[:]  # sort a copy (pure function interface)
    if key is None:
        # Compare items directly
        for i in range(1, len(arr)):
            cur = arr[i]
            j = i - 1
            # Shift larger elements to the right
            while j >= 0 and arr[j] > cur:
                arr[j + 1] = arr[j]
                j -= 1
            arr[j + 1] = cur
    else:
        # Compare by key
        for i in range(1, len(arr)):
            cur = arr[i]
            kcur = key(cur)
            j = i - 1
            while j >= 0 and key(arr[j]) > kcur:
                arr[j + 1] = arr[j]
                j -= 1
            arr[j + 1] = cur

    return arr


def insertion_sort_inplace(a: List[T], key: Optional[Callable[[T], object]] = None) -> None:
    """
    In-place insertion sort (mutates the input list).

    Same complexities and properties as insertion_sort.
    """
    if len(a) <= 1:
        return

    if key is None:
        for i in range(1, len(a)):
            cur = a[i]
            j = i - 1
            while j >= 0 and a[j] > cur:
                a[j + 1] = a[j]
                j -= 1
            a[j + 1] = cur
    else:
        for i in range(1, len(a)):
            cur = a[i]
            kcur = key(cur)
            j = i - 1
            while j >= 0 and key(a[j]) > kcur:
                a[j + 1] = a[j]
                j -= 1
            a[j + 1] = cur


def demo():
    print("Insertion Sort Demo")
    print("=" * 30)
    cases = [
        [],
        [1],
        [3, 1, 2, 4],
        [5, 4, 3, 2, 1],
        [2, 2, 1, 1, 3],
        ["banana", "apple", "cherry"],
        [("a", 2), ("b", 1), ("c", 2)],
    ]
    for i, arr in enumerate(cases, 1):
        print(f"Case {i}: {arr}")
        print("  sorted:", insertion_sort(arr))
    print()


if __name__ == "__main__":
    demo()
