from typing import List, Tuple


def suffix_array(s: str) -> List[int]:
    """
    Build suffix array of string s using O(n log n) doubling algorithm.
    Returns SA: list of starting indices of suffixes in lexicographic order.

    Example:
      s = "banana"
      suffixes (sorted): ["a", "ana", "anana", "banana", "na", "nana"]
      SA = [5, 3, 1, 0, 4, 2]
    """
    n = len(s)
    if n == 0:
        return []
    # Initial ranking by characters (ord)
    sa = list(range(n))
    rank = [ord(c) for c in s]
    tmp = [0] * n

    k = 1
    while k < n:
        # Sort by (rank[i], rank[i+k]) pair
        sa.sort(key=lambda i: (rank[i], rank[i + k] if i + k < n else -1))
        # Recompute tmp ranks
        tmp[sa[0]] = 0
        for i in range(1, n):
            prev = sa[i - 1]
            cur = sa[i]
            prev_pair = (rank[prev], rank[prev + k] if prev + k < n else -1)
            cur_pair = (rank[cur], rank[cur + k] if cur + k < n else -1)
            tmp[cur] = tmp[prev] + (prev_pair != cur_pair)
        # Move tmp into rank
        rank[:] = tmp[:]
        if rank[sa[-1]] == n - 1:
            break
        k <<= 1
    return sa


def lcp_kasai(s: str, sa: List[int]) -> List[int]:
    """
    Kasai algorithm to build LCP array from string s and suffix array sa.
    LCP[i] = length of longest common prefix of suffixes sa[i] and sa[i-1].
    LCP[0] = 0 by convention.

    Time: O(n)
    """
    n = len(s)
    if n == 0:
        return []
    rank = [0] * n
    for i, p in enumerate(sa):
        rank[p] = i
    lcp = [0] * n
    k = 0
    for i in range(n):
        r = rank[i]
        if r == 0:
            k = 0
            continue
        j = sa[r - 1]
        while i + k < n and j + k < n and s[i + k] == s[j + k]:
            k += 1
        lcp[r] = k
        if k:
            k -= 1
    return lcp


def longest_repeated_substring_sa(s: str) -> Tuple[int, str, List[int]]:
    """
    Find longest repeated substring via SA + LCP.
    Returns (length, substring, starting_positions).
    If none found, returns (0, "", []).
    """
    n = len(s)
    if n == 0:
        return 0, "", []
    sa = suffix_array(s)
    lcp = lcp_kasai(s, sa)
    max_len = 0
    idx = -1
    for i in range(1, n):
        if lcp[i] > max_len:
            max_len = lcp[i]
            idx = i
    if max_len == 0:
        return 0, "", []
    sub = s[sa[idx] : sa[idx] + max_len]
    # Collect positions for this substring among neighbors with same LCP
    positions = set()
    # Check leftwards
    i = idx
    while i >= 1 and lcp[i] >= max_len:
        positions.add(sa[i])
        positions.add(sa[i - 1])
        i -= 1
    # Check rightwards
    i = idx + 1
    while i < n and lcp[i] >= max_len:
        positions.add(sa[i])
        positions.add(sa[i - 1])
        i += 1
    return max_len, sub, sorted(list(positions))


def sa_substring_search(s: str, sa: List[int], pattern: str) -> List[int]:
    """
    Search for all occurrences of 'pattern' in 's' using suffix array 'sa'.
    Returns starting indices. Time: O(m log n), m = len(pattern)
    """
    n = len(s)
    m = len(pattern)
    if m == 0 or n == 0 or m > n:
        return []

    # Lower bound for pattern
    lo, hi = 0, n
    while lo < hi:
        mid = (lo + hi) // 2
        start = sa[mid]
        if s[start : start + m] < pattern:
            lo = mid + 1
        else:
            hi = mid
    left = lo

    # Upper bound for pattern
    lo, hi = 0, n
    while lo < hi:
        mid = (lo + hi) // 2
        start = sa[mid]
        if s[start : start + m] <= pattern:
            lo = mid + 1
        else:
            hi = mid
    right = lo

    res = []
    for i in range(left, right):
        if s[sa[i] : sa[i] + m] == pattern:
            res.append(sa[i])
    return sorted(res)


def suffix_array_with_lcp(s: str) -> Tuple[List[int], List[int]]:
    """
    Convenience function returning (SA, LCP).
    """
    sa = suffix_array(s)
    lcp = lcp_kasai(s, sa)
    return sa, lcp


def demo():
    print("Suffix Array + LCP (Kasai) Demo")
    print("=" * 45)

    # Basic example
    s = "banana"
    sa = suffix_array(s)
    lcp = lcp_kasai(s, sa)
    print(f"String: {s}")
    print(f"SA:  {sa}")
    print(f"LCP: {lcp}")
    length, sub, pos = longest_repeated_substring_sa(s)
    print(f"Longest repeated substring: '{sub}' (len={length}) at {pos}")
    print()

    # Substring search
    text = "abracadabra abracadabra"
    pattern = "abra"
    sa_t = suffix_array(text)
    matches = sa_substring_search(text, sa_t, pattern)
    print(f"Text:    {text}")
    print(f"Pattern: {pattern}")
    print(f"Matches at indices: {matches}")
    print()

    # Random example with repeated patterns
    s2 = "mississippi"
    sa2, lcp2 = suffix_array_with_lcp(s2)
    print(f"String: {s2}")
    print(f"SA:  {sa2}")
    print(f"LCP: {lcp2}")
    length2, sub2, pos2 = longest_repeated_substring_sa(s2)
    print(f"Longest repeated substring: '{sub2}' (len={length2}) at {pos2}")
    print()

    print("Notes & Interview Tips:")
    print("  - SA in O(n log n) via doubling; LCP in O(n) via Kasai.")
    print("  - Useful for multi-pattern search, repeats, and suffix-based problems.")
    print(
        "  - Alternatives: Suffix Tree/Automaton for linear-time construction with more complexity."
    )


if __name__ == "__main__":
    demo()
