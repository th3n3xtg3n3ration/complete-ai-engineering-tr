"""Tests for lesson 3 Polars utilities and lazy pipeline."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import polars as pl
import pytest
from polars.testing import assert_frame_equal

SRC = Path(__file__).resolve().parents[1] / "src"
sys.path.insert(0, str(SRC))


def _load_module(name: str):
    spec = importlib.util.spec_from_file_location(name, SRC / f"{name}.py")
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load {name}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


foundations = _load_module("polars_foundations")
lazy = _load_module("lazy_pipeline")
performance = _load_module("performance_comparison")


def _orders() -> pl.DataFrame:
    return pl.DataFrame(
        {
            "Order ID": ["o1", "o2", "o3"],
            "Customer ID": ["c1", "c1", "c2"],
            "Order At": ["2026-01-01", "2026-01-02", "2026-01-03"],
            "Quantity": [2, 1, 4],
            "Unit Price": [10.0, 8.0, 3.0],
            "Status": [" Paid ", None, "SHIPPED"],
        }
    )


def test_normalize_column_names() -> None:
    assert foundations.normalize_column_names([" Customer ID ", "Order-Value"]) == [
        "customer_id",
        "order_value",
    ]


def test_normalize_column_names_rejects_collision() -> None:
    with pytest.raises(ValueError, match="collide"):
        foundations.normalize_column_names(["Order ID", "order-id"])


def test_normalize_column_names_prefixes_numeric_name() -> None:
    assert foundations.normalize_column_names(["2026 value"]) == ["column_2026_value"]


def test_require_columns_reports_missing_columns() -> None:
    with pytest.raises(ValueError, match="missing required columns"):
        foundations.require_columns(pl.DataFrame({"a": [1]}), ["a", "b"])


def test_require_columns_works_for_lazy_frame() -> None:
    foundations.require_columns(pl.LazyFrame({"a": [1]}), ["a"])


def test_profile_frame_counts_nulls_and_memory() -> None:
    profile = foundations.profile_frame(
        pl.DataFrame({"a": [1, None], "b": [None, "x"]})
    )
    assert profile.rows == 2
    assert profile.columns == 2
    assert profile.null_cells == 2
    assert profile.estimated_size_bytes > 0


def test_prepare_orders_normalizes_and_calculates_revenue() -> None:
    result = foundations.prepare_orders(_orders())
    assert result.columns == [
        "order_id",
        "customer_id",
        "order_at",
        "quantity",
        "unit_price",
        "status",
        "revenue",
    ]
    assert result["revenue"].to_list() == pytest.approx([20.0, 8.0, 12.0])


def test_prepare_orders_fills_missing_status() -> None:
    result = foundations.prepare_orders(_orders())
    assert result.filter(pl.col("order_id") == "o2")["status"].item() == "unknown"


def test_prepare_orders_filters_invalid_rows() -> None:
    frame = _orders().vstack(
        pl.DataFrame(
            {
                "Order ID": ["bad"],
                "Customer ID": ["c3"],
                "Order At": ["not-a-date"],
                "Quantity": [0],
                "Unit Price": [-1.0],
                "Status": ["paid"],
            }
        )
    )
    assert foundations.prepare_orders(frame).height == 3


def test_prepare_orders_deduplicates_by_order_id_keep_last() -> None:
    duplicate = _orders().row(0, named=True) | {"Unit Price": 99.0}
    frame = _orders().vstack(pl.DataFrame([duplicate]))
    result = foundations.prepare_orders(frame)
    assert result.height == 3
    assert result.filter(pl.col("order_id") == "o1")["unit_price"].item() == 99.0


def test_customer_summary() -> None:
    result = foundations.customer_summary(foundations.prepare_orders(_orders()))
    c1 = result.filter(pl.col("customer_id") == "c1")
    assert c1["order_count"].item() == 2
    assert c1["total_revenue"].item() == pytest.approx(28.0)


def test_safe_left_join_validates_cardinality() -> None:
    left = pl.DataFrame({"id": [1, 2]})
    right = pl.DataFrame({"id": [1, 1], "name": ["a", "b"]})
    with pytest.raises(pl.exceptions.ComputeError):
        foundations.safe_left_join(left, right, on="id", validate="m:1")


def test_safe_left_join_preserves_left_rows() -> None:
    left = pl.DataFrame({"id": [1, 2]})
    right = pl.DataFrame({"id": [1], "name": ["a"]})
    result = foundations.safe_left_join(left, right, on="id")
    assert result.height == 2
    assert result.filter(pl.col("id") == 2)["name"].item() is None


def test_top_n_per_group_is_deterministic() -> None:
    frame = pl.DataFrame(
        {"g": ["a", "a", "a", "b"], "v": [5, 5, 3, 8], "row": [1, 2, 3, 4]}
    )
    result = foundations.top_n_per_group(
        frame,
        group_column="g",
        value_column="v",
        n=2,
    )
    assert result["row"].to_list() == [1, 2, 4]


def test_top_n_per_group_rejects_non_positive_n() -> None:
    with pytest.raises(ValueError, match="positive"):
        foundations.top_n_per_group(
            pl.DataFrame({"g": ["a"], "v": [1]}),
            group_column="g",
            value_column="v",
            n=0,
        )


def test_lazy_query_matches_eager_result() -> None:
    eager = foundations.customer_summary(foundations.prepare_orders(_orders()))
    query = lazy.customer_metrics(lazy.build_order_query(_orders().lazy()))
    actual = lazy.collect_query(query)
    assert_frame_equal(eager, actual, check_row_order=True)


def test_lazy_query_can_join_customer_attributes() -> None:
    customers = pl.DataFrame(
        {"Customer ID": ["c1", "c2"], "Segment": ["A", "B"]}
    )
    result = lazy.collect_query(
        lazy.build_order_query(_orders().lazy(), customers.lazy())
    )
    assert "segment" in result.columns
    assert result.filter(pl.col("customer_id") == "c2")["segment"].item() == "B"


def test_optimized_plan_is_non_empty() -> None:
    plan = lazy.optimized_plan(lazy.build_order_query(_orders().lazy()))
    assert isinstance(plan, str)
    assert plan.strip()


def test_scan_csv_builds_lazy_frame(tmp_path: Path) -> None:
    path = tmp_path / "orders.csv"
    _orders().write_csv(path)
    frame = lazy.collect_query(lazy.scan_csv(path))
    assert frame.height == 3


def test_sink_parquet_round_trip(tmp_path: Path) -> None:
    path = tmp_path / "result.parquet"
    query = lazy.build_order_query(_orders().lazy())
    lazy.sink_parquet(query, path)
    assert pl.read_parquet(path).height == 3


def test_synthetic_orders_are_reproducible() -> None:
    first = performance.make_synthetic_orders(50, seed=7)
    second = performance.make_synthetic_orders(50, seed=7)
    assert_frame_equal(first, second)


def test_eager_and_lazy_performance_helpers_match() -> None:
    frame = performance.make_synthetic_orders(100, seed=9)
    assert_frame_equal(
        performance.eager_customer_metrics(frame),
        performance.lazy_customer_metrics(frame),
        check_row_order=True,
    )
