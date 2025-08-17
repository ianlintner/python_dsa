from __future__ import annotations

class FenwickTree:
    """
    Fenwick Tree (Binary Indexed Tree) for prefix sums with point updates.

    Supports:
    - add(i, delta): point update nums[i] += delta
    - prefix_sum(i): sum(nums[0..i])
    - range_sum(l, r): sum(nums[l..r])

    Time:
    - Update: O(log n)
    - Query:  O(log n)
    Space: O(n)

    Interview follow-ups:
    - How to build in O(n)? (Use internal tree and propagate)
    - How to do range updates / point queries? (BIT on diff array)
    - How to do range updates / range queries? (Use two BITs)
    - 2D Fenwick Tree? (Extend indexes to 2 dimensions)
    """

    def __init__(self, size_or_data: int | list[int]):
        if isinstance(size_or_data, int):
            n = size_or_data
            self.n = n
            self.bit = [0] * (n + 1)  # 1-indexed internal
        else:
            data = size_or_data
            self.n = len(data)
            self.bit = [0] * (self.n + 1)
            # O(n) build: add each value to its responsible ranges using internal bit parent relations
            for i, val in enumerate(data, start=1):
                self.bit[i] += val
                j = i + (i & -i)
                if j <= self.n:
                    self.bit[j] += self.bit[i]

    def add(self, index: int, delta: int) -> None:
        """Add delta to nums[index] (0-indexed external)."""
        i = index + 1
        while i <= self.n:
            self.bit[i] += delta
            i += i & -i

    def prefix_sum(self, index: int) -> int:
        """Return sum(nums[0..index]) inclusive. If index < 0, returns 0."""
        if index < 0:
            return 0
        i = min(index + 1, self.n)
        s = 0
        while i > 0:
            s += self.bit[i]
            i -= i & -i
        return s

    def range_sum(self, left: int, right: int) -> int:
        """Return sum(nums[left..right]) inclusive."""
        if right < left:
            return 0
        return self.prefix_sum(right) - self.prefix_sum(left - 1)

    def find_by_prefix(self, target_sum: int) -> int:
        """
        Find smallest index i such that prefix_sum(i) >= target_sum.
        Returns self.n if no such index exists.

        Requires all deltas (values) to be non-negative.
        """
        if target_sum <= 0:
            return 0
        # Largest power of two >= n
        idx = 0
        bit_mask = 1 << (self.n.bit_length())
        s = 0
        while bit_mask:
            next_idx = idx + bit_mask
            if next_idx <= self.n and s + self.bit[next_idx] < target_sum:
                s += self.bit[next_idx]
                idx = next_idx
            bit_mask >>= 1
        res = idx  # prefix sum < target_sum at idx
        if res + 1 > self.n:
            return self.n
        return res  # note: caller typically uses res for 1-indexed; adjust if needed

    def __len__(self) -> int:
        return self.n


class RangeFenwick:
    """
    Range update + range query Fenwick using two BITs.

    Supports:
    - range_add(l, r, delta): add delta to each element in [l, r]
    - prefix_sum(i)
    - range_sum(l, r)

    Idea:
      To support range add and prefix sum, maintain two BITs (B1, B2):
        prefix_sum(i) = sum(B1, i) * i - sum(B2, i)
      For range add [l, r] by delta:
        add(B1, l, delta), add(B1, r+1, -delta)
        add(B2, l, delta*(l-1)), add(B2, r+1, -delta*r)
    """

    def __init__(self, n: int):
        self.n = n
        self.b1 = FenwickTree(n)
        self.b2 = FenwickTree(n)

    def _add(self, bit: FenwickTree, idx: int, delta: int) -> None:
        if 0 <= idx < self.n:
            bit.add(idx, delta)

    def range_add(self, left: int, right: int, delta: int) -> None:
        if left > right:
            return
        # B1
        self._add(self.b1, left, delta)
        if right + 1 < self.n:
            self._add(self.b1, right + 1, -delta)
        # B2
        self._add(self.b2, left, delta * left)
        if right + 1 < self.n:
            self._add(self.b2, right + 1, -delta * (right + 1))

    def _prefix_sum(self, i: int) -> int:
        s1 = self.b1.prefix_sum(i)
        s2 = self.b2.prefix_sum(i)
        return s1 * (i + 1) - s2

    def prefix_sum(self, i: int) -> int:
        return self._prefix_sum(i)

    def range_sum(self, left: int, right: int) -> int:
        if right < left:
            return 0
        return self._prefix_sum(right) - self._prefix_sum(left - 1)


class FenwickTree2D:
    """
    2D Fenwick Tree for rectangle sum queries with point updates.

    Supports:
    - add(x, y, delta)
    - prefix_sum(x, y): sum over rectangle (0,0) to (x,y)
    - range_sum(x1, y1, x2, y2): sum over sub-rectangle

    Time:
    - Update: O(log n * log m)
    - Query:  O(log n * log m)
    Space: O(n * m)
    """

    def __init__(self, rows: int, cols: int):
        self.n = rows
        self.m = cols
        self.bit = [[0] * (cols + 1) for _ in range(rows + 1)]

    def add(self, x: int, y: int, delta: int) -> None:
        i = x + 1
        while i <= self.n:
            j = y + 1
            while j <= self.m:
                self.bit[i][j] += delta
                j += j & -j
            i += i & -i

    def prefix_sum(self, x: int, y: int) -> int:
        if x < 0 or y < 0:
            return 0
        i = min(x + 1, self.n)
        res = 0
        while i > 0:
            j = min(y + 1, self.m)
            while j > 0:
                res += self.bit[i][j]
                j -= j & -j
            i -= i & -i
        return res

    def range_sum(self, x1: int, y1: int, x2: int, y2: int) -> int:
        if x2 < x1 or y2 < y1:
            return 0
        return (
            self.prefix_sum(x2, y2)
            - self.prefix_sum(x1 - 1, y2)
            - self.prefix_sum(x2, y1 - 1)
            + self.prefix_sum(x1 - 1, y1 - 1)
        )


def demo():
    print("Fenwick Tree (Binary Indexed Tree) Demo")
    print("=" * 50)

    # 1D Fenwick Tree basic usage
    arr = [3, 2, -1, 6, 5, 4, -3, 3, 7, 2, 3]
    ft = FenwickTree(arr)
    print(f"Array: {arr}")
    print(f"prefix_sum(4) [sum of arr[0..4]]: {ft.prefix_sum(4)}")
    print(f"range_sum(3, 8): {ft.range_sum(3, 8)}")

    print("Update: add +2 at index 5")
    ft.add(5, 2)
    print(f"New prefix_sum(5): {ft.prefix_sum(5)}")
    print(f"New range_sum(3, 8): {ft.range_sum(3, 8)}")
    print()

    # Range add + range sum using two BITs
    print("RangeFenwick (range add + range sum) Demo")
    n = 10
    rft = RangeFenwick(n)
    print(f"Initial zero array of size {n}")
    print("range_add(2, 6, +5)")
    rft.range_add(2, 6, 5)
    print(f"range_sum(0, 9): {rft.range_sum(0, 9)} (should be 5 * 5 = 25)")
    print(f"range_sum(2, 6): {rft.range_sum(2, 6)} (should be 5 * 5 = 25)")
    print(f"prefix_sum(6): {rft.prefix_sum(6)} (should be 25)")
    print()

    # 2D Fenwick Tree demo
    print("FenwickTree2D Demo")
    rows, cols = 4, 5
    ft2d = FenwickTree2D(rows, cols)
    updates = [(0, 0, 1), (1, 2, 3), (3, 4, 5), (2, 1, 2)]
    for x, y, d in updates:
        ft2d.add(x, y, d)
        print(f"add({x}, {y}, {d})")
    print(f"prefix_sum(3, 4): {ft2d.prefix_sum(3, 4)}")
    print(f"range_sum(1, 1, 3, 4): {ft2d.range_sum(1, 1, 3, 4)}")
    print()

    print("Complexity:")
    print("  Update: O(log n), Query: O(log n) for 1D")
    print("  Update: O(log n log m), Query: O(log n log m) for 2D")
    print()
    print("Interview tips:")
    print("  - Great for dynamic prefix sums and inversion counts")
    print("  - Alternative to Segment Tree when only sums are needed")
    print("  - Easier to implement than Segment Tree")
    print("  - Can support 'find kth prefix' with non-negative values")


if __name__ == "__main__":
    demo()
