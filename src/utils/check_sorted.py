from collections.abc import Sequence
from typing import Any


def is_sorted(a: Sequence[Any], reverse: bool = False) -> bool:
    """Check if sequence is sorted in ascending (or descending if reverse=True) order."""
    if len(a) <= 1:
        return True

    if reverse:
        return all(a[i] >= a[i + 1] for i in range(len(a) - 1))
    else:
        return all(a[i] <= a[i + 1] for i in range(len(a) - 1))


def is_strictly_sorted(a: Sequence[Any], reverse: bool = False) -> bool:
    """Check if sequence is strictly sorted (no duplicates)."""
    if len(a) <= 1:
        return True

    if reverse:
        return all(a[i] > a[i + 1] for i in range(len(a) - 1))
    else:
        return all(a[i] < a[i + 1] for i in range(len(a) - 1))
