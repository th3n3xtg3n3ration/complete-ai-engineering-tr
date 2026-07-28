from __future__ import annotations

from collections.abc import Sequence
from typing import TypeVar

T = TypeVar("T")


def linear_search(items: Sequence[T], target: T) -> int:
    for index, item in enumerate(items):
        if item == target:
            return index
    return -1


def binary_search(items: Sequence[T], target: T) -> int:
    left = 0
    right = len(items) - 1

    while left <= right:
        middle = (left + right) // 2
        value = items[middle]
        if value == target:
            return middle
        if value < target:
            left = middle + 1
        else:
            right = middle - 1
    return -1


def bubble_sort(items: Sequence[T]) -> list[T]:
    result = list(items)
    for end in range(len(result) - 1, 0, -1):
        swapped = False
        for index in range(end):
            if result[index] > result[index + 1]:
                result[index], result[index + 1] = result[index + 1], result[index]
                swapped = True
        if not swapped:
            break
    return result


def selection_sort(items: Sequence[T]) -> list[T]:
    result = list(items)
    for start in range(len(result)):
        minimum = start
        for index in range(start + 1, len(result)):
            if result[index] < result[minimum]:
                minimum = index
        result[start], result[minimum] = result[minimum], result[start]
    return result


def insertion_sort(items: Sequence[T]) -> list[T]:
    result = list(items)
    for index in range(1, len(result)):
        current = result[index]
        position = index - 1
        while position >= 0 and result[position] > current:
            result[position + 1] = result[position]
            position -= 1
        result[position + 1] = current
    return result


def merge_sort(items: Sequence[T]) -> list[T]:
    if len(items) <= 1:
        return list(items)

    middle = len(items) // 2
    left = merge_sort(items[:middle])
    right = merge_sort(items[middle:])
    return _merge(left, right)


def _merge(left: Sequence[T], right: Sequence[T]) -> list[T]:
    merged: list[T] = []
    left_index = 0
    right_index = 0

    while left_index < len(left) and right_index < len(right):
        if left[left_index] <= right[right_index]:
            merged.append(left[left_index])
            left_index += 1
        else:
            merged.append(right[right_index])
            right_index += 1

    merged.extend(left[left_index:])
    merged.extend(right[right_index:])
    return merged


def quick_sort(items: Sequence[T]) -> list[T]:
    if len(items) <= 1:
        return list(items)

    pivot = items[len(items) // 2]
    lower = [item for item in items if item < pivot]
    equal = [item for item in items if item == pivot]
    higher = [item for item in items if item > pivot]
    return quick_sort(lower) + equal + quick_sort(higher)


def recursive_factorial(number: int) -> int:
    if number < 0:
        raise ValueError("number must be non-negative")
    if number <= 1:
        return 1
    return number * recursive_factorial(number - 1)
