"""Tests for lesson 6 SQLite schema, queries, and quality checks."""

from __future__ import annotations

import importlib.util
import sqlite3
import sys
from pathlib import Path

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


database = _load_module("database")
queries = _load_module("analytics_queries")
quality = _load_module("query_quality")


@pytest.fixture
def connection() -> sqlite3.Connection:
    connection = database.build_demo_database()
    yield connection
    connection.close()


def test_foreign_keys_are_enabled(connection: sqlite3.Connection) -> None:
    assert connection.execute("PRAGMA foreign_keys").fetchone()[0] == 1


def test_schema_tables_exist(connection: sqlite3.Connection) -> None:
    for table in ("customers", "products", "orders", "order_items"):
        assert database.table_exists(connection, table)


def test_seed_counts(connection: sqlite3.Connection) -> None:
    assert database.row_count(connection, "customers") == 4
    assert database.row_count(connection, "products") == 4
    assert database.row_count(connection, "orders") == 5
    assert database.row_count(connection, "order_items") == 7


def test_row_count_rejects_untrusted_table(connection: sqlite3.Connection) -> None:
    with pytest.raises(ValueError, match="unsupported"):
        database.row_count(connection, "customers; DROP TABLE customers")


def test_transaction_commits(connection: sqlite3.Connection) -> None:
    with database.transaction(connection):
        connection.execute(
            "INSERT INTO customers VALUES (?, ?, ?, ?)",
            ("c5", "Ece", "east", "2025-05-01"),
        )
    assert database.row_count(connection, "customers") == 5


def test_transaction_rolls_back(connection: sqlite3.Connection) -> None:
    with pytest.raises(RuntimeError, match="boom"):
        with database.transaction(connection):
            connection.execute(
                "INSERT INTO customers VALUES (?, ?, ?, ?)",
                ("c5", "Ece", "east", "2025-05-01"),
            )
            raise RuntimeError("boom")
    assert database.row_count(connection, "customers") == 4


def test_fetch_all_returns_dictionaries(connection: sqlite3.Connection) -> None:
    rows = database.fetch_all(
        connection,
        "SELECT customer_id, customer_name FROM customers ORDER BY customer_id LIMIT 1",
    )
    assert rows == [{"customer_id": "c1", "customer_name": "Ada"}]


def test_paid_orders_threshold_is_parameterized(connection: sqlite3.Connection) -> None:
    rows = queries.paid_orders(connection, minimum_revenue=600)
    assert [row["order_id"] for row in rows] == ["o1", "o5"]


def test_parameter_value_cannot_inject_sql(connection: sqlite3.Connection) -> None:
    rows = queries.paid_orders(connection, minimum_revenue="0 OR 1=1")
    assert rows == []
    assert database.table_exists(connection, "orders")


def test_customer_summary_keeps_customer_without_orders(
    connection: sqlite3.Connection,
) -> None:
    rows = queries.customer_revenue_summary(connection)
    deniz = next(row for row in rows if row["customer_id"] == "c4")
    assert deniz["paid_order_count"] == 0
    assert deniz["total_revenue"] == pytest.approx(0.0)


def test_customer_summary_values(connection: sqlite3.Connection) -> None:
    rows = queries.customer_revenue_summary(connection)
    ada = next(row for row in rows if row["customer_id"] == "c1")
    assert ada["paid_order_count"] == 2
    assert ada["total_revenue"] == pytest.approx(1106.0)
    assert ada["average_order_value"] == pytest.approx(553.0)


def test_order_line_join_has_expected_grain(connection: sqlite3.Connection) -> None:
    rows = queries.order_line_details(connection)
    assert len(rows) == 7
    quality.assert_unique_key(rows, ["order_id", "product_id"])


def test_monthly_revenue_cte(connection: sqlite3.Connection) -> None:
    rows = queries.monthly_paid_revenue(connection)
    assert rows == [
        {"revenue_month": "2026-01", "paid_order_count": 1, "total_revenue": 1040.0},
        {"revenue_month": "2026-02", "paid_order_count": 2, "total_revenue": 666.0},
        {"revenue_month": "2026-03", "paid_order_count": 1, "total_revenue": 560.0},
    ]


def test_dense_rank_orders_customers(connection: sqlite3.Connection) -> None:
    rows = queries.customer_revenue_rank(connection)
    assert [(row["customer_id"], row["revenue_rank"]) for row in rows] == [
        ("c1", 1),
        ("c3", 2),
        ("c2", 3),
        ("c4", 4),
    ]


def test_running_revenue_window(connection: sqlite3.Connection) -> None:
    rows = queries.running_customer_revenue(connection)
    c1 = [row for row in rows if row["customer_id"] == "c1"]
    assert [row["running_revenue"] for row in c1] == pytest.approx([1040.0, 1106.0])


def test_lag_calculates_order_gap(connection: sqlite3.Connection) -> None:
    rows = queries.order_gap_days(connection)
    o2 = next(row for row in rows if row["order_id"] == "o2")
    assert o2["previous_order_at"] == "2026-01-05"
    assert o2["days_since_previous"] == 36


def test_not_exists_returns_customer_without_orders(connection: sqlite3.Connection) -> None:
    assert queries.customers_without_orders(connection) == [
        {"customer_id": "c4", "customer_name": "Deniz"}
    ]


def test_top_product_per_category(connection: sqlite3.Connection) -> None:
    rows = queries.top_product_per_category(connection)
    assert [(row["category"], row["product_id"]) for row in rows] == [
        ("electronics", "p1"),
        ("furniture", "p4"),
    ]


def test_validate_read_only_accepts_select_and_cte() -> None:
    quality.validate_read_only_sql("SELECT 1")
    quality.validate_read_only_sql("WITH x AS (SELECT 1) SELECT * FROM x")


def test_validate_read_only_rejects_mutation() -> None:
    with pytest.raises(ValueError, match="read-only"):
        quality.validate_read_only_sql("DELETE FROM orders")


def test_validate_read_only_ignores_keywords_in_comments() -> None:
    quality.validate_read_only_sql("-- DELETE is discussed here\nSELECT 1")


def test_explain_query_plan_returns_steps(connection: sqlite3.Connection) -> None:
    plan = quality.explain_query_plan(
        connection,
        "SELECT * FROM orders WHERE customer_id = ?",
        ("c1",),
    )
    assert plan
    assert all(step.detail for step in plan)


def test_assert_expected_columns(connection: sqlite3.Connection) -> None:
    rows = queries.monthly_paid_revenue(connection)
    quality.assert_expected_columns(
        rows,
        ["revenue_month", "paid_order_count", "total_revenue"],
    )


def test_assert_expected_columns_rejects_wrong_schema(
    connection: sqlite3.Connection,
) -> None:
    with pytest.raises(ValueError, match="unexpected columns"):
        quality.assert_expected_columns(queries.monthly_paid_revenue(connection), ["month"])


def test_assert_unique_key_rejects_duplicates() -> None:
    with pytest.raises(ValueError, match="duplicate query grain"):
        quality.assert_unique_key([{"id": 1}, {"id": 1}], ["id"])


def test_assert_non_negative(connection: sqlite3.Connection) -> None:
    quality.assert_non_negative(
        queries.customer_revenue_summary(connection),
        ["paid_order_count", "total_revenue", "average_order_value"],
    )


def test_assert_non_negative_rejects_negative_value() -> None:
    with pytest.raises(ValueError, match="negative value"):
        quality.assert_non_negative([{"amount": -1}], ["amount"])
