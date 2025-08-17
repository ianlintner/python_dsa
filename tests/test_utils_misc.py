import time

from interview_workbook.utils.check_sorted import is_sorted, is_strictly_sorted
from interview_workbook.utils.timing import timeit


def test_check_sorted_variants():
    assert is_sorted([1, 1, 2, 3]) is True
    assert is_sorted([3, 2, 1], reverse=True) is True
    assert is_sorted([1, 3, 2]) is False

    assert is_strictly_sorted([1, 2, 3]) is True
    assert is_strictly_sorted([1, 1, 2]) is False
    assert is_strictly_sorted([3, 2, 1], reverse=True) is True


def test_timeit_decorator_executes_and_returns():
    calls = {"n": 0}

    @timeit  # should not raise, and should call the function
    def add(a: int, b: int) -> int:
        calls["n"] += 1
        return a + b

    before = time.time()
    out = add(2, 5)  # type: ignore[operator]  # wrapper returns original result
    after = time.time()

    assert out == 7
    assert calls["n"] == 1
    # ensure wrapper ran in a realistic time window
    assert after >= before
