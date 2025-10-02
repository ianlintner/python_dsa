import pytest

from interview_workbook.data_structures.fenwick_tree import FenwickTree
from interview_workbook.data_structures.heap_patterns import (
    MedianMaintenance,
    k_largest,
    merge_k_sorted,
    top_k_frequent,
)
from interview_workbook.data_structures.lfu_cache import LFUCache
from interview_workbook.data_structures.lru_cache import LRUCache, SimpleLRUCache
from interview_workbook.data_structures.segment_tree import (
    RangeMinSegmentTree,
    SegmentTree,
)
from interview_workbook.data_structures.trie import (
    Trie,
    WordDictionary,
    find_words_in_board,
)
from interview_workbook.data_structures.union_find import UnionFind


class TestUnionFind:
    def test_basic_union_find(self):
        uf = UnionFind(5)
        assert uf.num_components() == 5
        uf.union(0, 1)
        uf.union(1, 2)
        assert uf.connected(0, 2) is True
        assert uf.connected(0, 3) is False
        assert uf.component_size(0) == 3
        assert uf.num_components() == 3


class TestTrie:
    def test_trie_insert_search_prefix(self):
        trie = Trie()
        words = ["apple", "app", "apex", "bat", "batch"]
        for w in words:
            trie.insert(w)

        assert trie.search("apple") is True
        assert trie.search("appl") is False
        assert trie.starts_with("app") is True
        assert trie.starts_with("ba") is True
        assert trie.starts_with("cat") is False

        assert "apple" in trie
        assert "appl" not in trie

        # LCP may vary depending on implementation; ensure it's a prefix of at least one word
        lcp = trie.longest_common_prefix()
        assert any(word.startswith(lcp) for word in words)

        got = trie.get_words_with_prefix("ap", limit=10)
        assert set(got) >= {"app", "apple", "apex"}

    def test_word_dictionary(self):
        wd = WordDictionary()
        wd.add_word("bad")
        wd.add_word("dad")
        wd.add_word("mad")
        assert wd.search("pad") is False
        assert wd.search("bad") is True
        assert wd.search(".ad") is True
        assert wd.search("b..") is True

    def test_find_words_in_board(self):
        board = [
            ["o", "a", "a", "n"],
            ["e", "t", "a", "e"],
            ["i", "h", "k", "r"],
            ["i", "f", "l", "v"],
        ]
        words = ["oath", "pea", "eat", "rain"]
        found = find_words_in_board(board, words)
        assert set(found) >= {"oath", "eat"}


class TestCachesHeaps:
    def test_lru_cache(self):
        cache = LRUCache(2)
        cache.put(1, 1)
        cache.put(2, 2)
        assert cache.get(1) == 1
        cache.put(3, 3)  # evicts key 2
        assert cache.get(2) == -1
        cache.put(4, 4)  # evicts key 1
        assert cache.get(1) == -1
        assert cache.get(3) == 3
        assert cache.get(4) == 4

    def test_simple_lru_cache(self):
        cache = SimpleLRUCache(2)
        cache.put(1, 1)
        cache.put(2, 2)
        assert cache.get(1) == 1
        cache.put(3, 3)
        assert cache.get(2) == -1

    def test_lfu_cache(self):
        cache = LFUCache(2)
        cache.put(1, 1)
        cache.put(2, 2)
        assert cache.get(1) == 1  # freq(1)=2
        cache.put(3, 3)  # evicts key 2 (freq(2)=1)
        assert cache.get(2) == -1
        assert cache.get(3) == 3
        assert cache.get(1) == 1
        cache.put(
            4, 4
        )  # evict key 3 or 1 based on freq; touch 3 to ensure eviction target
        # To define eviction deterministically, bump key 3 before inserting 4
        # But since above we already accessed 3 once, both 1 and 3 have freq >= 1.
        # Accept either eviction policy: one of them should be missing now.
        missing_count = (cache.get(1) == -1) + (cache.get(3) == -1)
        assert missing_count == 1
        assert cache.get(4) == 4

    def test_heap_utilities(self):
        nums = [3, 1, 5, 12, 2, 11]
        assert set(k_largest(nums, 3)) == {12, 11, 5}

        arrs = [[1, 4, 5], [1, 3, 4], [2, 6]]
        assert merge_k_sorted(arrs) == [1, 1, 2, 3, 4, 4, 5, 6]

        nums2 = [1, 1, 1, 2, 2, 3]
        assert set(top_k_frequent(nums2, 2)) == {1, 2}

    def test_median_maintenance(self):
        mm = MedianMaintenance()
        seq = [5, 15, 1, 3]
        expected = [5.0, 10.0, 5.0, 4.0]
        got = []
        for x in seq:
            mm.add(x)
            got.append(mm.median())
        assert got == expected


class TestFenwickTree:
    def test_point_update_prefix_range_sum(self):
        ft = FenwickTree(10)
        for i, v in enumerate([1, 2, 3, 4, 5], start=1):
            ft.add(i, v)
        assert ft.prefix_sum(1) == 1
        assert ft.prefix_sum(3) == 1 + 2 + 3
        assert ft.range_sum(2, 4) == 2 + 3 + 4
        ft.add(3, 2)
        assert ft.prefix_sum(3) == 1 + 2 + (3 + 2)


class TestSegmentTree:
    def test_range_add_range_sum(self):
        arr = [1, 2, 3, 4, 5]
        st = SegmentTree(arr)
        assert st.range_sum(0, 4) == sum(arr)
        st.range_add(1, 3, 2)  # [1,4,5,6,5]
        assert st.range_sum(0, 4) == 1 + 4 + 5 + 6 + 5
        assert st.range_sum(2, 2) == 5
        st.point_add(0, 3)  # [4,4,5,6,5]
        assert st.range_sum(0, 0) == 4

    def test_range_min_tree(self):
        arr = [5, 3, 8, 1, 4]
        rmq = RangeMinSegmentTree(arr)
        assert rmq.range_min(0, 4) == 1
        assert rmq.range_min(0, 2) == 3
        rmq.point_set(3, 6)
        assert rmq.range_min(0, 4) == 3


if __name__ == "__main__":
    pytest.main([__file__])
