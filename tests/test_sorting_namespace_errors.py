import pytest


def test_sorting_namespace_raises_on_unknown_attr():
    import src.algorithms.sorting as srt  # type: ignore

    with pytest.raises(AttributeError):
        _ = srt.this_attribute_does_not_exist  # noqa: F841
