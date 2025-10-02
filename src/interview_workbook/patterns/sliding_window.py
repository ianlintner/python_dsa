from collections import Counter, deque


def max_sliding_window(nums: list[int], k: int) -> list[int]:
    """
    Sliding Window Maximum using a monotonic deque.

    Time: O(n)
    Space: O(k)

    Returns max of each window of size k.
    """
    n = len(nums)
    if k <= 0 or k > n:
        return []
    dq = deque()  # stores indices, values in decreasing order
    out = []
    for i, x in enumerate(nums):
        # Remove indices out of window
        while dq and dq[0] <= i - k:
            dq.popleft()
        # Maintain decreasing deque
        while dq and nums[dq[-1]] <= x:
            dq.pop()
        dq.append(i)
        if i >= k - 1:
            out.append(nums[dq[0]])
    return out


def min_sliding_window(nums: list[int], k: int) -> list[int]:
    """
    Sliding Window Minimum using a monotonic deque.

    Time: O(n)
    Space: O(k)
    """
    n = len(nums)
    if k <= 0 or k > n:
        return []
    dq = deque()  # increasing deque
    out = []
    for i, x in enumerate(nums):
        while dq and dq[0] <= i - k:
            dq.popleft()
        while dq and nums[dq[-1]] >= x:
            dq.pop()
        dq.append(i)
        if i >= k - 1:
            out.append(nums[dq[0]])
    return out


def length_of_longest_substring_without_repeating(s: str) -> int:
    """
    Classic sliding window with hash map.

    Time: O(n)
    Space: O(min(n, alphabet))

    LeetCode 3
    """
    last_index: dict[str, int] = {}
    start = 0
    best = 0
    for i, ch in enumerate(s):
        if ch in last_index and last_index[ch] >= start:
            start = last_index[ch] + 1
        last_index[ch] = i
        best = max(best, i - start + 1)
    return best


def min_window_substring(s: str, t: str) -> str:
    """
    Minimum window substring containing all chars of t (with multiplicity).

    Time: O(n)
    Space: O(1) if alphabet size is bounded (e.g., ASCII)

    LeetCode 76
    """
    if not s or not t or len(t) > len(s):
        return ""
    need = Counter(t)
    missing = len(t)
    left = 0
    best_len = float("inf")
    best = (0, 0)
    for right, ch in enumerate(s):
        if need[ch] > 0:
            missing -= 1
        need[ch] -= 1
        # shrink when valid
        while missing == 0:
            if right - left + 1 < best_len:
                best_len = right - left + 1
                best = (left, right)
            # pop left
            left_ch = s[left]
            need[left_ch] += 1
            if need[left_ch] > 0:
                missing += 1
            left += 1
    if best_len == float("inf"):
        return ""
    left_idx, right_idx = best
    return s[left_idx : right_idx + 1]


def count_subarrays_sum_k(nums: list[int], k: int) -> int:
    """
    Count subarrays with sum exactly k using prefix sums + hash map.

    Time: O(n)
    Space: O(n)

    LeetCode 560
    """
    from collections import defaultdict

    count = defaultdict(int)
    count[0] = 1
    prefix = 0
    ans = 0
    for x in nums:
        prefix += x
        ans += count[prefix - k]
        count[prefix] += 1
    return ans


def longest_ones_with_k_zero_flips(nums: list[int], k: int) -> int:
    """
    Given binary array nums, return longest subarray with at most k zeros (flip at most k zeros).

    Time: O(n)
    Space: O(1)

    LeetCode 1004 variant
    """
    left = 0
    zeros = 0
    best = 0
    for right, x in enumerate(nums):
        if x == 0:
            zeros += 1
        while zeros > k:
            if nums[left] == 0:
                zeros -= 1
            left += 1
        best = max(best, right - left + 1)
    return best


def subarray_max_sum_at_most_k(nums: list[int], k: int) -> int:
    """
    Largest subarray length where sum <= k for non-negative nums using sliding window.

    Time: O(n)
    Space: O(1)

    If nums can be negative, need prefix sums + monotonic queue (more complex).
    """
    left = 0
    cur_sum = 0
    best = 0
    for right, x in enumerate(nums):
        cur_sum += x
        while cur_sum > k and left <= right:
            cur_sum -= nums[left]
            left += 1
        best = max(best, right - left + 1)
    return best


def demo():
    print("Sliding Window and Monotonic Queue Demo")
    print("=" * 45)

    nums = [1, 3, -1, -3, 5, 3, 6, 7]
    k = 3
    print(f"Array: {nums}, k={k}")
    print(f"Max sliding window: {max_sliding_window(nums, k)}")
    print(f"Min sliding window: {min_sliding_window(nums, k)}")
    print()

    s = "abcabcbb"
    print(
        f"Longest substring without repeating in '{s}': {length_of_longest_substring_without_repeating(s)}"
    )
    s2 = "ADOBECODEBANC"
    t2 = "ABC"
    print(
        f"Min window substring of '{s2}' containing '{t2}': '{min_window_substring(s2, t2)}'"
    )
    print()

    arr = [1, 1, 1]
    target = 2
    print(
        f"Count subarrays sum={target} in {arr}: {count_subarrays_sum_k(arr, target)}"
    )
    print()

    bin_arr = [1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0]
    flips = 2
    print(
        f"Longest ones with at most {flips} zero flips in {bin_arr}: {longest_ones_with_k_zero_flips(bin_arr, flips)}"
    )
    print()

    nonneg = [1, 2, 1, 0, 1, 1, 0]
    at_most = 4
    print(
        f"Max length subarray with sum <= {at_most} in {nonneg}: {subarray_max_sum_at_most_k(nonneg, at_most)}"
    )
    print()

    print("Notes & Interview Tips:")
    print("  - Use hash maps for variable-sized windows keyed on counts/needs.")
    print("  - Use deque for O(1) amortized push/pop extremes to get window min/max.")
    print(
        "  - For sums with negative numbers, sliding window breaks; use prefix sums and other techniques."
    )


if __name__ == "__main__":
    demo()
