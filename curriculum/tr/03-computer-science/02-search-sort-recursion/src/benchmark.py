from __future__ import annotations

import random
import time
from collections.abc import Callable, Sequence

from algorithms import insertion_sort, merge_sort, quick_sort

SortFunction = Callable[[Sequence[int]], list[int]]


def measure(function: SortFunction, data: Sequence[int], repeats: int = 3) -> float:
    durations: list[float] = []
    expected = sorted(data)

    for _ in range(repeats):
        started = time.perf_counter()
        result = function(data)
        durations.append(time.perf_counter() - started)
        if result != expected:
            raise AssertionError(f"{function.__name__} produced an incorrect result")

    return min(durations)


def run_benchmark(sizes: Sequence[int] = (100, 1_000, 5_000)) -> None:
    algorithms: tuple[SortFunction, ...] = (insertion_sort, merge_sort, quick_sort)
    random_generator = random.Random(42)

    print(f"{'size':>8} {'algorithm':>18} {'seconds':>12}")
    print("-" * 42)

    for size in sizes:
        data = [random_generator.randint(0, size * 10) for _ in range(size)]
        for algorithm in algorithms:
            seconds = measure(algorithm, data)
            print(f"{size:>8} {algorithm.__name__:>18} {seconds:>12.6f}")


if __name__ == "__main__":
    run_benchmark()
