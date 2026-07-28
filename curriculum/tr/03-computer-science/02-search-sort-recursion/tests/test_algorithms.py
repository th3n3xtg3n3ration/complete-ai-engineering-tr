from pathlib import Path
import sys

SOURCE_DIRECTORY = Path(__file__).resolve().parents[1] / "src"
sys.path.insert(0, str(SOURCE_DIRECTORY))

from algorithms import (  # noqa: E402
    binary_search,
    bubble_sort,
    insertion_sort,
    linear_search,
    merge_sort,
    quick_sort,
    recursive_factorial,
    selection_sort,
)


def test_search_algorithms_find_existing_values() -> None:
    items = [1, 3, 5, 7, 9]
    assert linear_search(items, 7) == 3
    assert binary_search(items, 7) == 3


def test_search_algorithms_return_minus_one() -> None:
    items = [1, 3, 5, 7, 9]
    assert linear_search(items, 4) == -1
    assert binary_search(items, 4) == -1


def test_sorting_algorithms() -> None:
    items = [5, 1, 4, 2, 8, 2]
    expected = sorted(items)
    algorithms = (
        bubble_sort,
        selection_sort,
        insertion_sort,
        merge_sort,
        quick_sort,
    )
    for algorithm in algorithms:
        assert algorithm(items) == expected
        assert items == [5, 1, 4, 2, 8, 2]


def test_sorting_empty_and_single_item_sequences() -> None:
    for algorithm in (bubble_sort, selection_sort, insertion_sort, merge_sort, quick_sort):
        assert algorithm([]) == []
        assert algorithm([42]) == [42]


def test_recursive_factorial() -> None:
    assert recursive_factorial(0) == 1
    assert recursive_factorial(5) == 120


def test_recursive_factorial_rejects_negative_input() -> None:
    try:
        recursive_factorial(-1)
    except ValueError as error:
        assert str(error) == "number must be non-negative"
    else:
        raise AssertionError("Expected ValueError")
