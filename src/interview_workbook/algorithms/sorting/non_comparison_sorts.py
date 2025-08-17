from __future__ import annotations

from collections.abc import Callable
from typing import Any


def counting_sort(
    nums: list[int],
    min_val: int | None = None,
    max_val: int | None = None,
    stable: bool = True,
) -> list[int]:
    """
    Counting Sort for integers (handles negatives via offset).

    Time: O(n + k) where k = max_val - min_val + 1
    Space: O(n + k)

    Notes:
    - Stable variant is generally preferred; unstable is slightly faster and uses less memory
    - Suitable when k is not much larger than n
    - For wide ranges (large k), prefer comparison sorts or radix sort

    Args:
        nums: list of integers
        min_val, max_val: optionally provide known range to avoid scanning

    Returns:
        New sorted list (does not modify input)
    """
    n = len(nums)
    if n <= 1:
        return nums[:]

    if min_val is None or max_val is None:
        min_val = min(nums)
        max_val = max(nums)

    k = max_val - min_val + 1
    if k <= 0:
        return nums[:]

    # Frequency array
    count = [0] * k
    for x in nums:
        count[x - min_val] += 1

    if not stable:
        # Compute positions via prefix accumulation into original array order
        idx = 0
        out = [0] * n
        for v, c in enumerate(count):
            if c:
                val = v + min_val
                out[idx : idx + c] = [val] * c
                idx += c
        return out

    # Stable: prefix sums, then place from right to left
    for i in range(1, k):
        count[i] += count[i - 1]

    out = [0] * n
    for i in range(n - 1, -1, -1):
        v = nums[i]
        count[v - min_val] -= 1
        out[count[v - min_val]] = v

    return out


def counting_sort_by_key(
    items: list[Any],
    key: Callable[[Any], int],
    key_min: int | None = None,
    key_max: int | None = None,
) -> list[Any]:
    """
    Stable counting sort by integer key in small range.

    Args:
        items: list of arbitrary items
        key: function mapping item -> int in [key_min, key_max]
        key_min, key_max: optionally provide known range

    Returns:
        New list stably sorted by key(item)
    """
    n = len(items)
    if n <= 1:
        return items[:]

    if key_min is None or key_max is None:
        vals = [key(x) for x in items]
        key_min = min(vals)
        key_max = max(vals)
    else:
        vals = [key(x) for x in items]

    k = key_max - key_min + 1
    count = [0] * k
    for v in vals:
        count[v - key_min] += 1

    for i in range(1, k):
        count[i] += count[i - 1]

    out = [None] * n  # type: ignore
    # place from right for stability
    for i in range(n - 1, -1, -1):
        v = vals[i]
        count[v - key_min] -= 1
        out[count[v - key_min]] = items[i]

    return out  # type: ignore


def radix_sort_lsd_integers(nums: list[int], base: int = 10) -> list[int]:
    """
    Radix Sort (LSD) for integers, stable per digit using counting sort.

    Handles negatives by sorting absolute values and then merging:
      - Sort non-negatives as usual
      - Sort absolute values of negatives, then place them reversed (more negative first)

    Time: O(d * (n + base)) where d = number of digits
    Space: O(n + base)

    Constraints:
      - Works best when numbers have bounded number of digits
      - base typically 10 or 2^8 (256) for byte-wise
    """
    if not nums:
        return []

    non_neg = [x for x in nums if x >= 0]
    neg = [-x for x in nums if x < 0]  # store absolute values

    def _lsd_non_negative(arr: list[int]) -> list[int]:
        if not arr:
            return []
        max_val = max(arr)
        exp = 1
        out = arr[:]
        while max_val // exp > 0:
            # Stable counting sort by current digit
            count = [0] * base
            for v in out:
                digit = (v // exp) % base
                count[digit] += 1
            for i in range(1, base):
                count[i] += count[i - 1]
            tmp = [0] * len(out)
            for i in range(len(out) - 1, -1, -1):
                v = out[i]
                digit = (v // exp) % base
                count[digit] -= 1
                tmp[count[digit]] = v
            out = tmp
            exp *= base
        return out

    sorted_non_neg = _lsd_non_negative(non_neg)
    sorted_abs_neg = _lsd_non_negative(neg)
    # Convert back: negatives should appear in decreasing absolute value (i.e., more negative first)
    sorted_negatives = [-v for v in reversed(sorted_abs_neg)]
    return sorted_negatives + sorted_non_neg


def radix_sort_lsd_fixed_strings(strings: list[str], max_len: int | None = None) -> list[str]:
    """
    Radix Sort (LSD) for fixed-length ASCII strings. If variable length, left-pad with '\0'.

    Time: O(L * (n + 256)) where L = max_len
    Space: O(n + 256)

    Notes:
    - Uses byte-wise counting sort (alphabet size 256)
    - '\0' sorts before all printable characters
    - For Unicode beyond BMP or different collation rules, adapt bucket size accordingly
    """
    if not strings:
        return []

    if max_len is None:
        max_len = max(len(s) for s in strings)

    # Left-pad each string to same length with '\0' so that shorter strings come first lexicographically
    PAD = "\0"
    arr = [s.rjust(max_len, PAD) for s in strings]
    R = 256  # extended ASCII
    n = len(arr)

    for pos in range(max_len - 1, -1, -1):
        count = [0] * R
        for s in arr:
            count[ord(s[pos])] += 1
        for i in range(1, R):
            count[i] += count[i - 1]
        tmp = [""] * n
        for i in range(n - 1, -1, -1):
            ch = ord(arr[i][pos])
            count[ch] -= 1
            tmp[count[ch]] = arr[i]
        arr = tmp

    # Strip padding
    return [s.lstrip(PAD) for s in arr]


def demo():
    print("Non-Comparison Sorts Demo (Counting Sort, Radix Sort)")
    print("=" * 60)

    # Counting sort basic
    print("Counting Sort (integers, including negatives):")
    nums = [3, -2, 5, 0, -2, 3, 1, 0]
    print(f"Input:  {nums}")
    print(f"Sorted: {counting_sort(nums)}")
    print()

    # Counting sort by key (stable)
    print("Counting Sort By Key (stable):")
    items = [("apple", 3), ("pear", 1), ("plum", 3), ("fig", 2)]
    sorted_items = counting_sort_by_key(items, key=lambda x: x[1])
    print(f"Input:  {items}")
    print(f"Sorted by 2nd field: {sorted_items}")
    print()

    # Radix sort integers (LSD)
    print("Radix Sort (integers):")
    nums2 = [170, 45, 75, -90, 802, 24, 2, 66, -5]
    print(f"Input:  {nums2}")
    print(f"Sorted: {radix_sort_lsd_integers(nums2, base=10)}")
    print()

    # Radix sort fixed strings
    print("Radix Sort (fixed-length strings via padding):")
    strs = ["bcd", "abc", "ab", "abcd", "a", "xyz", "xy"]
    print(f"Input:  {strs}")
    print(f"Sorted: {radix_sort_lsd_fixed_strings(strs)}")
    print()

    print("Complexity Summary:")
    print("  Counting Sort: O(n + k), k = range of keys; stable variant preferred")
    print("  Radix Sort (integers): O(d * (n + base)), base often 10 or 256")
    print("  Radix Sort (strings): O(L * (n + Sigma)), Sigma=alphabet size (256)")
    print()
    print("When to use:")
    print("  - Counting sort: small integer ranges (IDs, grades, buckets)")
    print(
        "  - Radix sort: large n with bounded digits/lengths; when comparison sort overhead is high"
    )
    print()
    print("Interview follow-ups:")
    print("  - How to handle negatives in radix sort? (split and merge with reversed negatives)")
    print("  - How to ensure stability? (right-to-left placement in counting phase)")
    print("  - Memory trade-offs vs comparison sorts")


if __name__ == "__main__":
    demo()
