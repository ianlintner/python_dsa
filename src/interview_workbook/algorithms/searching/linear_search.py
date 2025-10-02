from __future__ import annotations

from collections.abc import Callable, Iterable, Sequence
from typing import TypeVar

T = TypeVar("T")


def linear_search(
    a: Sequence[T], target: T, key: Callable[[T], object] | None = None
) -> int:
    """
    Linear search over a sequence.

    When to use:
      - Small inputs
      - Unsorted data
      - Streaming/iterators (O(1) extra space), though this function expects a Sequence to return an index

    Time: O(n)
    Space: O(1)

    Parameters:
      - a: Sequence to search
      - target: Value to find
      - key: Optional key extractor to compare derived values

    Returns:
      - Index of the first matching element, or -1 if not found.

    Examples:
      linear_search([3, 1, 4], 4) -> 2
      linear_search([("a", 2), ("b", 1)], ("?", 1), key=lambda x: x[1]) -> 1
    """
    if key is None:
        for i, v in enumerate(a):
            if v == target:
                return i
        return -1
    else:
        # Compare derived key from elements to the raw target value
        for i, v in enumerate(a):
            if key(v) == target:
                return i
        return -1


def find_all(
    a: Iterable[T], target: T, key: Callable[[T], object] | None = None
) -> list[int]:
    """
    Return all indices where target occurs (if input is a Sequence), else consume iterable and return indices in order.

    Time: O(n)
    Space: O(k) where k = number of matches (plus O(1) otherwise)
    """
    res: list[int] = []
    if isinstance(a, Sequence):
        if key is None:
            for i, v in enumerate(a):
                if v == target:
                    res.append(i)
        else:
            for i, v in enumerate(a):
                if key(v) == target:
                    res.append(i)
    else:
        # Fallback for generic Iterables without random access (indices are based on enumeration order)
        if key is None:
            for i, v in enumerate(a):
                if v == target:
                    res.append(i)
        else:
            for i, v in enumerate(a):
                if key(v) == target:
                    res.append(i)
    return res


def demo():
    print("Linear Search Demo")
    print("=" * 30)
    arr = [3, 1, 4, 1, 5, 9, 2]
    print("Array:", arr)
    for t in [3, 9, 8]:
        print(f"  search {t}: index ->", linear_search(arr, t))
    pairs = [("a", 2), ("b", 1), ("c", 2)]
    print("Pairs:", pairs)
    print("  search key=val 2:", linear_search(pairs, ("?", 2), key=lambda x: x[1]))
    print("  find_all of 1:", find_all(arr, 1))

    print()
    # Test with strings
    words = ["apple", "banana", "cherry", "date"]
    print("Words:", words)
    for t in ["banana", "date", "fig"]:
        print(f"  search {t}: index ->", linear_search(words, t))

    print()

    # Test with key function on objects
    class Item:
        def __init__(self, name: str, value: int):
            self.name = name
            self.value = value

        def __repr__(self):
            return f"Item({self.name}, {self.value})"

    items = [Item("x", 10), Item("y", 20), Item("z", 10)]
    print("Items:", items)
    print("  find_all value=10:", find_all(items, 10, key=lambda x: x.value))


if __name__ == "__main__":
    demo()
