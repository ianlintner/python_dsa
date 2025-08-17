def z_array(s: str) -> list[int]:
    """
    Compute Z-array for string s.
    Z[i] = length of the longest substring starting at i which is also a prefix of s.

    Time: O(n)
    Space: O(n)

    Insight:
    - Maintain a window [L, R] which is the rightmost segment matched with prefix.
    - Reuse previous computations within [L, R] to avoid re-comparing.
    """
    n = len(s)
    if n == 0:
        return []
    Z = [0] * n
    L = R = 0
    for i in range(1, n):
        if i <= R:
            # i is within [L, R], mirror = i - L
            Z[i] = min(R - i + 1, Z[i - L])
        # Try to extend Z[i]
        while i + Z[i] < n and s[Z[i]] == s[i + Z[i]]:
            Z[i] += 1
        # Update [L, R] if extended past R
        if i + Z[i] - 1 > R:
            L, R = i, i + Z[i] - 1
    Z[0] = n
    return Z


def z_search(text: str, pattern: str, sep: str = "$") -> list[int]:
    """
    Pattern matching using Z-algorithm.
    Build string P + sep + T and compute Z on it.

    Returns: starting indices in text where pattern occurs.

    Time: O(n + m)
    """
    if not pattern or not text or len(pattern) > len(text):
        return []
    # Ensure separator not in either string (fallback to rare unicode if needed)
    if sep in text or sep in pattern:
        sep = "\u0001"  # Start of Heading control character (unlikely to be in inputs)
        if sep in text or sep in pattern:
            raise ValueError("Separator collision in z_search; provide a safe 'sep' explicitly.")

    s = pattern + sep + text
    Z = z_array(s)
    m = len(pattern)
    res = []
    for i in range(m + 1, len(s)):
        if Z[i] >= m:
            res.append(i - (m + 1))
    return res


def longest_substring_prefix_match(s: str) -> list[int]:
    """
    For each position i, return the length of the longest prefix of s that matches s[i:].
    This is exactly Z-array semantics, returned for convenience on original string.
    """
    return z_array(s)


def string_periods(s: str) -> list[int]:
    """
    Return all periods p of the string such that s[i] == s[i+p] for all valid i.
    Period p means the string is constructed by repeating a substring of length p.
    Uses Z-array properties: if n % p == 0 and Z[p] >= n - p then p is a period.

    Time: O(n)
    """
    n = len(s)
    if n == 0:
        return []
    Z = z_array(s)
    periods = []
    for p in range(1, n):
        if n % p == 0 and Z[p] >= n - p:
            periods.append(p)
    return periods


def longest_border(s: str) -> int:
    """
    Longest border = longest proper prefix which is also a suffix.
    Using Z-array: border length is max i such that i + Z[i] == n.

    Time: O(n)
    """
    n = len(s)
    if n == 0:
        return 0
    Z = z_array(s)
    best = 0
    for i in range(1, n):
        if i + Z[i] == n:
            best = max(best, Z[i])
    return best


def z_array_with_explanations(s: str) -> list[tuple[int, int]]:
    """
    Return list of tuples (index, Z[index]) for explanatory printing.
    """
    Z = z_array(s)
    return list(enumerate(Z))


def demo():
    print("Z-Algorithm Demo")
    print("=" * 40)

    # Basic Z-array
    s = "aabxaayaab"
    Z = z_array(s)
    print(f"String: {s}")
    print(f"Z-array: {Z}")
    print()

    # Pattern search via Z
    text = "abxabcabcabyabcab"
    pattern = "abcab"
    matches = z_search(text, pattern)
    print(f"Text:    {text}")
    print(f"Pattern: {pattern}")
    print(f"Matches at indices: {matches}")
    print()

    # String periods
    s2 = "abababab"
    per = string_periods(s2)
    print(f"String: {s2}")
    print(f"Periods: {per} (smallest period {per[0] if per else 'N/A'})")
    print()

    # Longest border
    s3 = "abcababcab"
    lb = longest_border(s3)
    print(f"String: {s3}")
    print(f"Longest border length: {lb} (border: '{s3[:lb]}')")
    print()

    # Explanations
    s4 = "aaaaa"
    exp = z_array_with_explanations(s4)
    print(f"String: {s4}")
    print("Index, Z[index]:")
    for i, z in exp:
        print(f"  {i}: {z}")
    print()

    print("Notes & Interview Tips:")
    print(
        "  - Z-array is symmetric to prefix function (KMP) but often simpler for pattern matching."
    )
    print("  - Common uses: pattern search, string periodicity, borders, runs.")
    print("  - Complexity: O(n). Maintain [L, R] window to reuse matches.")


if __name__ == "__main__":
    demo()
