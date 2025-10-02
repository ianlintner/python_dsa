from __future__ import annotations

from collections.abc import Callable
from typing import Optional


def selection_sort(a: list, key: Optional[Callable[[object], object]] = None) -> list:
    """
    Selection Sort (not stable).

    Idea:
      - Repeatedly select the minimum from the unsorted suffix and swap it
        into the next position of the sorted prefix.

    Time:
      - Best/Average/Worst: O(n^2)

    Space:
      - O(1) extra (sorting a copy, algorithm is in-place on that copy)

    Stability:
      - Not stable (swaps can reorder equal elements)

    When to use:
      - Educational purposes
      - Very small n

    Parameters:
      - a: List of items to sort (will not be mutated)
      - key: Optional callable mapping item to a sortable key

    Returns:
      A new sorted list.

    Example:
      selection_sort([3, 1, 2]) -> [1, 2, 3]
    """
    n = len(a)
    if n <= 1:
        return a[:]

    arr = a[:]
    if key is None:
        for i in range(n):
            min_idx = i
            for j in range(i + 1, n):
                if arr[j] < arr[min_idx]:
                    min_idx = j
            if min_idx != i:
                arr[i], arr[min_idx] = arr[min_idx], arr[i]
    else:
        for i in range(n):
            min_idx = i
            kmin = key(arr[min_idx])
            for j in range(i + 1, n):
                kj = key(arr[j])
                if kj < kmin:
                    min_idx = j
                    kmin = kj
            if min_idx != i:
                arr[i], arr[min_idx] = arr[min_idx], arr[i]
    return arr


def selection_sort_inplace(
    a: list, key: Optional[Callable[[object], object]] = None
) -> None:
    """
    In-place selection sort (mutates the input list).
    """
    n = len(a)
    if n <= 1:
        return

    if key is None:
        for i in range(n):
            min_idx = i
            for j in range(i + 1, n):
                if a[j] < a[min_idx]:
                    min_idx = j
            if min_idx != i:
                a[i], a[min_idx] = a[min_idx], a[i]
    else:
        for i in range(n):
            min_idx = i
            kmin = key(a[min_idx])
            for j in range(i + 1, n):
                kj = key(a[j])
                if kj < kmin:
                    min_idx = j
                    kmin = kj
            if min_idx != i:
                a[i], a[min_idx] = a[min_idx], a[i]


def demo():
    print("Selection Sort Demo")
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
        print("  sorted:", selection_sort(arr))
    print()


if __name__ == "__main__":
    demo()
