from collections import defaultdict

MOD_DEFAULT = 1_000_000_007
BASE_DEFAULT = 256  # typical for byte/char rolling hash


def rabin_karp_search(
    text: str, pattern: str, base: int = BASE_DEFAULT, mod: int = MOD_DEFAULT
) -> list[int]:
    """
    Rabin-Karp substring search using rolling hash.

    Time: O(n + m) average, O(n*m) worst-case if many collisions without verification
    Space: O(1) extra (besides output)

    Returns:
        List of starting indices in 'text' where 'pattern' occurs.

    Notes:
    - Uses polynomial rolling hash base^k modulo a large prime.
    - Performs verification on hash matches to avoid false positives.
    - For multiple pattern search, consider Aho-Corasick or using multiple hashes.
    """
    n, m = len(text), len(pattern)
    if m == 0 or n == 0 or m > n:
        return []
    if base <= 1 or mod <= 1:
        raise ValueError("base and mod must be > 1")

    # Precompute base^(m-1) % mod used for removing the leftmost char
    high_base = pow(base, m - 1, mod)

    # Compute initial hashes
    h_pat = 0
    h_txt = 0
    for i in range(m):
        h_pat = (h_pat * base + ord(pattern[i])) % mod
        h_txt = (h_txt * base + ord(text[i])) % mod

    res: list[int] = []
    # Slide the window
    for i in range(n - m + 1):
        # If hash matches, verify substring to avoid collisions
        if h_txt == h_pat and text[i : i + m] == pattern:
            res.append(i)
        if i < n - m:
            # Remove leftmost char, add next char
            left = ord(text[i])
            right = ord(text[i + m])
            h_txt = (h_txt - left * high_base) % mod
            h_txt = (h_txt * base + right) % mod
    return res


def rolling_hashes_all_substrings(
    s: str, k: int, base: int = BASE_DEFAULT, mod: int = MOD_DEFAULT
) -> list[int]:
    """
    Compute rolling hashes for all substrings of length k in s.
    Returns a list of hashes aligned with starting indices.

    Useful for duplicate detection, string periodicity checks, etc.
    """
    n = len(s)
    if k <= 0 or k > n:
        return []
    high_base = pow(base, k - 1, mod)
    h = 0
    for i in range(k):
        h = (h * base + ord(s[i])) % mod
    hashes = [h]
    for i in range(1, n - k + 1):
        left = ord(s[i - 1])
        right = ord(s[i + k - 1])
        h = (h - left * high_base) % mod
        h = (h * base + right) % mod
        hashes.append(h)
    return hashes


def find_repeated_substring_length_k(
    s: str, k: int, base: int = BASE_DEFAULT, mod: int = MOD_DEFAULT
) -> list[tuple[str, list[int]]]:
    """
    Find all repeated substrings of length k and their starting positions using rolling hash + verification.
    Returns list of (substring, [positions]).
    """
    n = len(s)
    if k <= 0 or k > n:
        return []
    hashes = rolling_hashes_all_substrings(s, k, base, mod)
    buckets: dict[int, list[int]] = defaultdict(list)
    for i, h in enumerate(hashes):
        buckets[h].append(i)
    results: list[tuple[str, list[int]]] = []
    seen_substrings: dict[str, bool] = {}
    for idxs in buckets.values():
        if len(idxs) > 1:
            groups: dict[str, list[int]] = {}
            for i in idxs:
                sub = s[i : i + k]
                groups.setdefault(sub, []).append(i)
            for sub, positions in groups.items():
                if len(positions) > 1 and sub not in seen_substrings:
                    results.append((sub, positions))
                    seen_substrings[sub] = True
    return results


def longest_repeated_substring(s: str) -> tuple[str, list[int]]:
    """
    Find one longest repeated substring using binary search on length + rolling hash.
    Returns (substring, positions). If none, returns ("", []).

    Time: O(n log n) average with hashing (verification included)
    """
    n = len(s)
    if n <= 1:
        return "", []

    def exists_len(k: int) -> tuple[str, list[int]]:
        if k == 0:
            return "", []
        hashes = rolling_hashes_all_substrings(s, k)
        buckets: dict[int, list[int]] = defaultdict(list)
        for i, h in enumerate(hashes):
            buckets[h].append(i)
        for idxs in buckets.values():
            if len(idxs) > 1:
                # verify duplicates
                seen_pos: dict[str, int] = {}
                for i in idxs:
                    sub = s[i : i + k]
                    if sub in seen_pos:
                        # Return first found; sufficient for binary search decision
                        return sub, [seen_pos[sub], i]
                    seen_pos[sub] = i
        return "", []

    lo, hi = 1, n - 1
    best_sub = ""
    while lo <= hi:
        mid = (lo + hi) // 2
        sub, positions = exists_len(mid)
        if sub:
            best_sub, _ = sub, positions
            lo = mid + 1
        else:
            hi = mid - 1
    if not best_sub:
        return "", []
    # Collect all positions for best_sub
    positions: list[int] = []
    k = len(best_sub)
    for i in range(n - k + 1):
        if s[i : i + k] == best_sub:
            positions.append(i)
    return best_sub, positions


def demo():
    print("Rabin-Karp and Rolling Hash Demo")
    print("=" * 40)

    # Rabin-Karp search
    text = "abracadabra abracadabra"
    pattern = "abra"
    print(f"Text:    {text}")
    print(f"Pattern: {pattern}")
    matches = rabin_karp_search(text, pattern)
    print(f"Matches at indices: {matches}")
    print()

    # Repeated substrings of fixed length
    s = "banana"
    k = 2
    repeats = find_repeated_substring_length_k(s, k)
    print(f"Repeated substrings of length {k} in '{s}':")
    for sub, pos in repeats:
        print(f"  '{sub}' at {pos}")
    print()

    # Longest repeated substring
    s2 = "ATCGATCGA$ATCGA"
    lrs, pos = longest_repeated_substring(s2)
    print(f"Longest repeated substring in '{s2}': '{lrs}' at {pos}")
    print()

    print("Notes & Interview Tips:")
    print("  - Use rolling hash for substring search and duplicate detection.")
    print("  - Always verify on hash match to avoid false positives.")
    print("  - Double hashing can reduce collision probability.")
    print("  - For many patterns, prefer Aho-Corasick (trie + automaton).")


if __name__ == "__main__":
    demo()
