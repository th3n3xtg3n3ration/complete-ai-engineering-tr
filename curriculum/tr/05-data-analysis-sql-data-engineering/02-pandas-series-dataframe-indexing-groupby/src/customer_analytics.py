"""End-to-end pandas example for transaction and customer analytics."""

from __future__ import annotations

import pandas as pd

from pandas_foundations import (
    assign_revenue,
    parse_datetime_column,
    require_columns,
    safe_merge,
)


def prepare_transactions(frame: pd.DataFrame) -> pd.DataFrame:
    """Validate, type, deduplicate, and enrich transaction records."""

    required = ["transaction_id", "customer_id", "timestamp", "quantity", "unit_price"]
    require_columns(frame, required)
    result = frame.copy()
    if result["transaction_id"].isna().any():
        raise ValueError("transaction_id must not contain missing values")
    result = result.drop_duplicates(subset="transaction_id", keep="last")
    result = parse_datetime_column(result, "timestamp")
    result = assign_revenue(result)
    if (result["quantity"] < 0).any() or (result["unit_price"] < 0).any():
        raise ValueError("quantity and unit_price must be non-negative")
    return result.sort_values("timestamp", kind="stable").reset_index(drop=True)


def customer_metrics(transactions: pd.DataFrame) -> pd.DataFrame:
    """Create one row per customer with frequency, revenue, and recency metrics."""

    require_columns(transactions, ["customer_id", "transaction_id", "timestamp", "revenue"])
    metrics = (
        transactions.groupby("customer_id", dropna=False, observed=True)
        .agg(
            order_count=("transaction_id", "nunique"),
            total_revenue=("revenue", "sum"),
            average_order_value=("revenue", "mean"),
            first_order=("timestamp", "min"),
            last_order=("timestamp", "max"),
        )
        .reset_index()
    )
    return metrics


def build_customer_report(
    transactions: pd.DataFrame,
    customers: pd.DataFrame,
) -> pd.DataFrame:
    """Join transaction metrics to a one-row-per-customer dimension."""

    require_columns(customers, ["customer_id"])
    prepared = prepare_transactions(transactions)
    metrics = customer_metrics(prepared)
    report = safe_merge(customers, metrics, on="customer_id", how="left", validate="one_to_one")
    fill_zero = ["order_count", "total_revenue", "average_order_value"]
    report[fill_zero] = report[fill_zero].fillna(0.0)
    return report


if __name__ == "__main__":
    tx = pd.DataFrame(
        {
            "transaction_id": [1, 2, 3],
            "customer_id": [10, 10, 20],
            "timestamp": ["2026-01-01", "2026-01-02", "2026-01-03"],
            "quantity": [1, 2, 3],
            "unit_price": [10.0, 5.0, 4.0],
        }
    )
    customers = pd.DataFrame({"customer_id": [10, 20, 30], "segment": ["A", "B", "C"]})
    print(build_customer_report(tx, customers))
