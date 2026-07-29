"""Tests for lesson 2 pandas utilities."""

from __future__ import annotations

import importlib.util
from pathlib import Path
import sys

import pandas as pd
import pytest

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


foundations = _load_module("pandas_foundations")
pipeline = _load_module("dataframe_pipeline")
analytics = _load_module("customer_analytics")


def test_require_columns_reports_missing_columns() -> None:
    with pytest.raises(ValueError, match="missing required columns"):
        foundations.require_columns(pd.DataFrame({"a": [1]}), ["a", "b"])


def test_normalize_column_names() -> None:
    assert foundations.normalize_column_names([" Customer ID ", "Order-Value"]) == [
        "customer_id",
        "order_value",
    ]


def test_normalize_column_names_rejects_collisions() -> None:
    with pytest.raises(ValueError, match="collide"):
        foundations.normalize_column_names(["Order ID", "order-id"])


def test_profile_frame_counts_quality_issues() -> None:
    frame = pd.DataFrame({"a": [1, 1, None], "b": ["x", "x", "z"]})
    profile = foundations.profile_frame(frame)
    assert profile.rows == 3
    assert profile.columns == 2
    assert profile.missing_cells == 1
    assert profile.duplicate_rows == 1
    assert profile.memory_bytes > 0


def test_filter_rows_uses_equals_and_minimums() -> None:
    frame = pd.DataFrame({"segment": ["A", "A", "B"], "value": [2, 7, 9]})
    result = foundations.filter_rows(
        frame, equals={"segment": "A"}, minimums={"value": 5}
    )
    assert result["value"].tolist() == [7]


def test_assign_revenue_does_not_mutate_input() -> None:
    frame = pd.DataFrame({"quantity": [2], "unit_price": [4.5]})
    result = foundations.assign_revenue(frame)
    assert "revenue" not in frame.columns
    assert result.loc[0, "revenue"] == pytest.approx(9.0)


def test_grouped_summary_keeps_missing_groups() -> None:
    frame = pd.DataFrame({"group": ["A", None, "A"], "value": [1.0, 2.0, 3.0]})
    result = foundations.grouped_summary(
        frame, group_columns=["group"], value_column="value"
    )
    assert result["count"].sum() == 3
    assert result.loc[result["group"].eq("A"), "sum"].iloc[0] == pytest.approx(4.0)


def test_grouped_summary_rejects_empty_keys() -> None:
    with pytest.raises(ValueError, match="must not be empty"):
        foundations.grouped_summary(
            pd.DataFrame({"value": [1]}), group_columns=[], value_column="value"
        )


def test_safe_merge_validates_cardinality() -> None:
    left = pd.DataFrame({"id": [1, 2]})
    right = pd.DataFrame({"id": [1, 1], "name": ["a", "b"]})
    with pytest.raises(pd.errors.MergeError):
        foundations.safe_merge(left, right, on="id", validate="one_to_one")


def test_top_n_per_group_is_stable() -> None:
    frame = pd.DataFrame(
        {"group": ["A", "A", "A", "B"], "value": [5, 5, 3, 8], "row": [1, 2, 3, 4]}
    )
    result = foundations.top_n_per_group(
        frame, group_column="group", value_column="value", n=2
    )
    assert result["row"].tolist() == [1, 2, 4]


def test_parse_datetime_column_rejects_invalid_values() -> None:
    frame = pd.DataFrame({"timestamp": ["2026-01-01", "not-a-date"]})
    with pytest.raises(ValueError, match="invalid datetime"):
        foundations.parse_datetime_column(frame, "timestamp")


def test_preprocessor_requires_fit() -> None:
    preprocessor = pipeline.TabularPreprocessor(("age",), ("city",))
    with pytest.raises(RuntimeError, match="fit"):
        preprocessor.transform(pd.DataFrame({"age": [1], "city": ["A"]}))


def test_preprocessor_uses_training_median() -> None:
    train = pd.DataFrame({"age": [10.0, 30.0, None], "city": ["A", "B", "A"]})
    test = pd.DataFrame({"age": [None], "city": ["A"]})
    preprocessor = pipeline.TabularPreprocessor(("age",), ("city",)).fit(train)
    result = preprocessor.transform(test)
    assert result.loc[0, "age"] == pytest.approx(20.0)


def test_preprocessor_maps_unseen_categories() -> None:
    train = pd.DataFrame({"age": [10.0], "city": ["A"]})
    test = pd.DataFrame({"age": [20.0], "city": ["B"]})
    preprocessor = pipeline.TabularPreprocessor(("age",), ("city",)).fit(train)
    result = preprocessor.transform(test)
    assert str(result.loc[0, "city"]) == "__unknown__"


def test_one_hot_encode_is_deterministic() -> None:
    frame = pd.DataFrame({"city": pd.Categorical(["B", "A"], categories=["A", "B"])})
    result = pipeline.one_hot_encode(frame, ["city"])
    assert result.columns.tolist() == ["city_A", "city_B"]
    assert result.dtypes.astype(str).tolist() == ["int8", "int8"]


def test_prepare_transactions_deduplicates_by_last_record() -> None:
    frame = pd.DataFrame(
        {
            "transaction_id": [1, 1],
            "customer_id": [10, 10],
            "timestamp": ["2026-01-01", "2026-01-02"],
            "quantity": [1, 2],
            "unit_price": [5.0, 5.0],
        }
    )
    result = analytics.prepare_transactions(frame)
    assert len(result) == 1
    assert result.loc[0, "revenue"] == pytest.approx(10.0)


def test_prepare_transactions_rejects_negative_values() -> None:
    frame = pd.DataFrame(
        {
            "transaction_id": [1],
            "customer_id": [10],
            "timestamp": ["2026-01-01"],
            "quantity": [-1],
            "unit_price": [5.0],
        }
    )
    with pytest.raises(ValueError, match="non-negative"):
        analytics.prepare_transactions(frame)


def test_customer_metrics_aggregates_orders_and_revenue() -> None:
    frame = pd.DataFrame(
        {
            "transaction_id": [1, 2, 3],
            "customer_id": [10, 10, 20],
            "timestamp": pd.to_datetime(
                ["2026-01-01", "2026-01-02", "2026-01-03"], utc=True
            ),
            "revenue": [5.0, 10.0, 7.0],
        }
    )
    result = analytics.customer_metrics(frame)
    row = result.loc[result["customer_id"].eq(10)].iloc[0]
    assert row["order_count"] == 2
    assert row["total_revenue"] == pytest.approx(15.0)


def test_build_customer_report_keeps_customers_without_orders() -> None:
    transactions = pd.DataFrame(
        {
            "transaction_id": [1],
            "customer_id": [10],
            "timestamp": ["2026-01-01"],
            "quantity": [1],
            "unit_price": [5.0],
        }
    )
    customers = pd.DataFrame({"customer_id": [10, 20]})
    report = analytics.build_customer_report(transactions, customers)
    row = report.loc[report["customer_id"].eq(20)].iloc[0]
    assert row["order_count"] == pytest.approx(0.0)
    assert row["total_revenue"] == pytest.approx(0.0)


def test_build_customer_report_rejects_duplicate_dimension_keys() -> None:
    transactions = pd.DataFrame(
        {
            "transaction_id": [1],
            "customer_id": [10],
            "timestamp": ["2026-01-01"],
            "quantity": [1],
            "unit_price": [5.0],
        }
    )
    customers = pd.DataFrame({"customer_id": [10, 10]})
    with pytest.raises(pd.errors.MergeError):
        analytics.build_customer_report(transactions, customers)
