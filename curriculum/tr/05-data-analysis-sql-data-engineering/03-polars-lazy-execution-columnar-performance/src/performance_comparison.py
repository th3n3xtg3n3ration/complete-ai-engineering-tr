"""Small, reproducible eager-versus-lazy Polars benchmark."""

from __future__ import annotations

import random
from dataclasses import dataclass
from time import perf_counter

import polars as pl
from polars.testing import assert_frame_equal

from lazy_pipeline import build_order_query, collect_query, customer_metrics
from polars_foundations import customer_summary, prepare_orders


@dataclass(frozen=True)
class BenchmarkResult:
    rows: int
    eager_seconds: float
    lazy_seconds: float
    eager_bytes: int
    lazy_bytes: int


def make_synthetic_orders(row_count: int, *, seed: int = 42) -> pl.DataFrame:
    """Generate deterministic order data without third-party generators."""

    if row_count <= 0:
        raise ValueError("row_count must be positive")
    rng = random.Random(seed)
    return pl.DataFrame(
        {
            "order_id": [f"o{index}" for index in range(row_count)],
            "customer_id": [
                f"c{rng.randrange(max(2, row_count // 20))}"
                for _ in range(row_count)
            ],
            "order_at": [
                f"2026-01-{1 + (index % 28):02d}" for index in range(row_count)
            ],
            "quantity": [1 + rng.randrange(5) for _ in range(row_count)],
            "unit_price": [
                round(1.0 + rng.random() * 99.0, 2) for _ in range(row_count)
            ],
            "status": [
                rng.choice(("paid", "paid", "shipped", "refunded"))
                for _ in range(row_count)
            ],
        }
    )


def eager_customer_metrics(frame: pl.DataFrame) -> pl.DataFrame:
    return customer_summary(prepare_orders(frame))


def lazy_customer_metrics(
    frame: pl.DataFrame,
    *,
    streaming: bool = False,
) -> pl.DataFrame:
    query = customer_metrics(build_order_query(frame.lazy()))
    return collect_query(query, streaming=streaming)


def benchmark(row_count: int = 100_000, *, seed: int = 42) -> BenchmarkResult:
    """Benchmark equivalent eager and lazy workloads and verify equality."""

    frame = make_synthetic_orders(row_count, seed=seed)

    eager_start = perf_counter()
    eager_result = eager_customer_metrics(frame)
    eager_seconds = perf_counter() - eager_start

    lazy_start = perf_counter()
    lazy_result = lazy_customer_metrics(frame)
    lazy_seconds = perf_counter() - lazy_start

    assert_frame_equal(eager_result, lazy_result, check_row_order=True)
    return BenchmarkResult(
        rows=row_count,
        eager_seconds=eager_seconds,
        lazy_seconds=lazy_seconds,
        eager_bytes=int(eager_result.estimated_size()),
        lazy_bytes=int(lazy_result.estimated_size()),
    )


if __name__ == "__main__":
    print(benchmark(50_000))
