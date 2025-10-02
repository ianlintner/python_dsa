class SegmentTree:
    """
    Segment Tree with lazy propagation for range add and range sum queries.

    Supports:
    - range_add(l, r, delta): add delta to every element in [l, r]
    - range_sum(l, r): sum of elements in [l, r]
    - point_set(i, val): set arr[i] = val
    - point_add(i, delta): arr[i] += delta

    Indexing: 0-indexed externally, inclusive ranges.

    Time:
    - Build: O(n)
    - Query: O(log n)
    - Update: O(log n)
    Space: O(n)

    Interview follow-ups:
    - How to support range assign (set all in [l,r] to x)? (Use separate lazy tag for assign overriding add)
    - How to support min/max queries? (Change combine func; lazy add works for min/max as well)
    - Iterative implementation vs recursive? (Iterative is cache-friendly but trickier with lazy)
    - Difference from Fenwick Tree? (Fenwick simpler; segment tree supports more general ops)
    """

    def __init__(self, data: list[int]):
        self.n = len(data)
        self.size = 1
        while self.size < self.n:
            self.size <<= 1
        self.tree = [0] * (2 * self.size)
        self.lazy = [0] * (2 * self.size)
        # Build leaves
        for i in range(self.n):
            self.tree[self.size + i] = data[i]
        # Build internal nodes
        for i in range(self.size - 1, 0, -1):
            self.tree[i] = self.tree[i << 1] + self.tree[i << 1 | 1]

    def _apply(self, idx: int, add: int, length: int) -> None:
        """Apply lazy addition to node idx representing 'length' elements."""
        self.tree[idx] += add * length
        if idx < self.size:  # has children
            self.lazy[idx] += add

    def _push(self, idx: int, left_len: int, right_len: int) -> None:
        """Push lazy value at idx to its children."""
        if self.lazy[idx] != 0:
            add = self.lazy[idx]
            self._apply(idx << 1, add, left_len)
            self._apply(idx << 1 | 1, add, right_len)
            self.lazy[idx] = 0

    def _range_add(
        self, idx: int, left: int, right: int, ql: int, qr: int, add: int
    ) -> None:
        if ql > right or qr < left:
            return
        if ql <= left and right <= qr:
            self._apply(idx, add, right - left + 1)
            return
        mid = (left + right) // 2
        left_len = mid - left + 1
        right_len = right - mid
        self._push(idx, left_len, right_len)
        self._range_add(idx << 1, left, mid, ql, qr, add)
        self._range_add(idx << 1 | 1, mid + 1, right, ql, qr, add)
        self.tree[idx] = self.tree[idx << 1] + self.tree[idx << 1 | 1]

    def range_add(self, ql: int, qr: int, add: int) -> None:
        """Add 'add' to all elements in [ql, qr]."""
        if self.n == 0 or ql > qr:
            return
        ql = max(0, ql)
        qr = min(self.n - 1, qr)
        self._range_add(1, 0, self.size - 1, ql, qr, add)

    def _range_sum(self, idx: int, left: int, right: int, ql: int, qr: int) -> int:
        if ql > right or qr < left:
            return 0
        if ql <= left and right <= qr:
            return self.tree[idx]
        mid = (left + right) // 2
        left_len = mid - left + 1
        right_len = right - mid
        self._push(idx, left_len, right_len)
        return self._range_sum(idx << 1, left, mid, ql, qr) + self._range_sum(
            idx << 1 | 1, mid + 1, right, ql, qr
        )

    def range_sum(self, ql: int, qr: int) -> int:
        """Return sum of elements in [ql, qr]."""
        if self.n == 0 or ql > qr:
            return 0
        ql = max(0, ql)
        qr = min(self.n - 1, qr)
        return self._range_sum(1, 0, self.size - 1, ql, qr)

    def _point_set(self, idx: int, left: int, right: int, pos: int, val: int) -> None:
        if left == right:
            self.tree[idx] = val
            self.lazy[idx] = 0
            return
        mid = (left + right) // 2
        left_len = mid - left + 1
        right_len = right - mid
        self._push(idx, left_len, right_len)
        if pos <= mid:
            self._point_set(idx << 1, left, mid, pos, val)
        else:
            self._point_set(idx << 1 | 1, mid + 1, right, pos, val)
        self.tree[idx] = self.tree[idx << 1] + self.tree[idx << 1 | 1]

    def point_set(self, pos: int, val: int) -> None:
        """Set arr[pos] = val."""
        if pos < 0 or pos >= self.n:
            return
        self._point_set(1, 0, self.size - 1, pos, val)

    def point_add(self, pos: int, delta: int) -> None:
        """Add delta to arr[pos]."""
        self.range_add(pos, pos, delta)


class RangeMinSegmentTree:
    """
    Segment Tree for range minimum query (RMQ) with point updates.

    Supports:
    - range_min(l, r): min over [l, r]
    - point_set(i, val): set arr[i] = val

    Time:
    - Build: O(n)
    - Query/Update: O(log n)
    """

    def __init__(self, data: list[int]):
        self.n = len(data)
        self.size = 1
        while self.size < self.n:
            self.size <<= 1
        INF = 10**18
        self.INF = INF
        self.tree = [INF] * (2 * self.size)
        # Build leaves
        for i in range(self.n):
            self.tree[self.size + i] = data[i]
        # Build internal nodes
        for i in range(self.size - 1, 0, -1):
            self.tree[i] = min(self.tree[i << 1], self.tree[i << 1 | 1])

    def range_min(self, ql: int, qr: int) -> int:
        if self.n == 0 or ql > qr:
            return self.INF
        ql = max(0, ql) + self.size
        qr = min(self.n - 1, qr) + self.size
        res = self.INF
        while ql <= qr:
            if ql & 1:
                res = min(res, self.tree[ql])
                ql += 1
            if not (qr & 1):
                res = min(res, self.tree[qr])
                qr -= 1
            ql >>= 1
            qr >>= 1
        return res

    def point_set(self, pos: int, val: int) -> None:
        if pos < 0 or pos >= self.n:
            return
        idx = self.size + pos
        self.tree[idx] = val
        idx >>= 1
        while idx:
            self.tree[idx] = min(self.tree[idx << 1], self.tree[idx << 1 | 1])
            idx >>= 1


def demo():
    print("Segment Tree Demo")
    print("=" * 40)

    arr = [2, 1, 3, 4, 5, 2, 3, 1]
    print(f"Array: {arr}")

    # Range Sum with Lazy Add
    print("\nRange Sum with Lazy Propagation:")
    st = SegmentTree(arr)
    print(f"range_sum(0, 7): {st.range_sum(0, 7)}  (expected {sum(arr)})")
    print("range_add(2, 5, +3)")
    st.range_add(2, 5, 3)
    arr2 = arr[:]
    for i in range(2, 6):
        arr2[i] += 3
    print(f"range_sum(2, 5): {st.range_sum(2, 5)}  (expected {sum(arr2[2:6])})")
    print("point_set(0, 10)")
    st.point_set(0, 10)
    arr2[0] = 10
    print(f"range_sum(0, 3): {st.range_sum(0, 3)}  (expected {sum(arr2[0:4])})")

    # Range Min
    print("\nRange Minimum Query (RMQ):")
    rmq = RangeMinSegmentTree(arr)
    print(f"range_min(0, 7): {rmq.range_min(0, 7)} (expected {min(arr)})")
    print("point_set(3, 0)")
    rmq.point_set(3, 0)
    print(
        f"range_min(2, 4): {rmq.range_min(2, 4)} (expected {min([arr[2], 0, arr[4]])})"
    )

    print("\nComplexity:")
    print("  Build: O(n)")
    print("  Range Query: O(log n)")
    print("  Range Update (with lazy): O(log n)")

    print("\nInterview tips:")
    print("  - Segment Trees are more general than Fenwick Trees")
    print("  - Use lazy propagation for range updates")
    print(
        "  - For range assign + range sum, maintain both 'assign' and 'add' lazy tags with priority"
    )
    print(
        "  - Iterative segment trees are compact and fast, but recursion is easier to reason about"
    )


if __name__ == "__main__":
    demo()
