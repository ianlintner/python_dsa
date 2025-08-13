from collections.abc import Callable
from typing import TypeVar

T = TypeVar("T")


def bubble_sort(a: list[T], key: Callable[[T], object] | None = None) -> list[T]:
    """
    Bubble Sort (stable).

    Idea:
      - Repeatedly swap adjacent out-of-order pairs, sinking the maximum to the end each pass.
      - Optimized by stopping early if no swaps in a pass.

    Time:
      - Best: O(n) when already sorted (with early exit)
      - Average/Worst: O(n^2)

    Space:
      - O(1) extra (sorting a copy, algorithm is in-place on that copy)

    Stability:
      - Stable (only swaps adjacent out-of-order elements)

    Parameters:
      - a: List of items to sort (will not be mutated)
      - key: Optional callable mapping item to a sortable key

    Returns:
      A new sorted list.
    """
    n = len(a)
    if n <= 1:
        return a[:]
    arr = a[:]
    if key is None:
        for end in range(n - 1, 0, -1):
            swapped = False
            for i in range(end):
                if arr[i] > arr[i + 1]:
                    arr[i], arr[i + 1] = arr[i + 1], arr[i]
                    swapped = True
            if not swapped:
                break
    else:
        for end in range(n - 1, 0, -1):
            swapped = False
            for i in range(end):
                if key(arr[i]) > key(arr[i + 1]):
                    arr[i], arr[i + 1] = arr[i + 1], arr[i]
                    swapped = True
            if not swapped:
                break
    return arr


def bubble_sort_inplace(a: list[T], key: Callable[[T], object] | None = None) -> None:
    """
    In-place bubble sort (mutates the input list).

    Same complexities and properties as bubble_sort.
    """
    n = len(a)
    if n <= 1:
        return
    if key is None:
        for end in range(n - 1, 0, -1):
            swapped = False
            for i in range(end):
                if a[i] > a[i + 1]:
                    a[i], a[i + 1] = a[i + 1], a[i]
                    swapped = True
            if not swapped:
                break
    else:
        for end in range(n - 1, 0, -1):
            swapped = False
            for i in range(end):
                if key(a[i]) > key(a[i + 1]):
                    a[i], a[i + 1] = a[i + 1], a[i]
                    swapped = True
            if not swapped:
                break


def demo():
    print("Bubble Sort Demo")
    print("=" * 30)
    cases = [
        [],
        [1],
        [3, 1, 2, 4],
        [5, 4, 3, 2, 1],
        [2, 2, 1, 1, 3],
        ["banana", "apple", "cherry"],
    ]
    for i, arr in enumerate(cases, 1):
        print(f"Case {i}: {arr}")
        print("  sorted:", bubble_sort(arr))
    print()


if __name__ == "__main__":
    demo()
