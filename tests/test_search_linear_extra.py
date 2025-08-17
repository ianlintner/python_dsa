from typing import NamedTuple

from interview_workbook.algorithms.searching.linear_search import find_all, linear_search


class Item(NamedTuple):
    key: int
    value: str


def test_linear_search_basic_and_key():
    arr = [5, 3, 7, 3, 9]
    assert linear_search(arr, 7) == 2
    assert linear_search(arr, 4) == -1

    items = [Item(1, "a"), Item(2, "b"), Item(1, "c")]
    # Search by key attribute using key function
    assert linear_search(items, 2, key=lambda it: it.key) == 1
    assert linear_search(items, 3, key=lambda it: it.key) == -1


def test_find_all_occurrences_with_and_without_key():
    arr = [1, 2, 1, 3, 1]
    assert find_all(arr, 1) == [0, 2, 4]
    assert find_all(arr, 4) == []

    items = [Item(1, "a"), Item(2, "b"), Item(1, "c"), Item(3, "d"), Item(1, "e")]
    assert find_all(items, 1, key=lambda it: it.key) == [0, 2, 4]
    assert find_all(items, 4, key=lambda it: it.key) == []
