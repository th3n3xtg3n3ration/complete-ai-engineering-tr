"""Reusable Polars utilities for columnar analytics workflows."""

from __future__ import annotations

from collections.abc import Iterable, Sequence
from dataclasses import dataclass
import re

import polars as pl


@dataclass(frozen=True)
class FrameProfile:
    """Compact data-quality and memory profile for an eager Polars frame."""

    rows: int
    columns: int
    null_cells: int
    estimated_size_bytes: int
    dtypes: tuple[str, ...]


def _column_names(frame: pl.DataFrame | pl.LazyFrame) -> list[str]:
    if isinstance(frame, pl.LazyFrame):
        return frame.collect_schema().names()
    return frame.columns


def require_columns(
    frame: pl.DataFrame | pl.LazyFrame,
    required: Iterable[str],
) -> None:
    """Raise a clear error when required columns are absent."""

    required_names = list(required)
    missing = sorted(set(required_names) - set(_column_names(frame)))
    if missing:
        raise ValueError(f"missing required columns: {missing}")


def normalize_column_names(names: Sequence[str]) -> list[str]:
    """Normalize names to deterministic snake_case and reject collisions."""

    normalized: list[str] = []
    for name in names:
        value = re.sub(r"[^0-9A-Za-z]+", "_", str(name).strip()).strip("_").lower()
        if not value:
            raise ValueError("column names must contain at least one alphanumeric character")
        if value[0].isdigit():
            value = f"column_{value}"
        normalized.append(value)
    if len(set(normalized)) != len(normalized):
        raise ValueError("normalized column names collide")
    return normalized


def normalize_frame_columns(
    frame: pl.DataFrame | pl.LazyFrame,
) -> pl.DataFrame | pl.LazyFrame:
    """Return a frame with normalized column names."""

    original = _column_names(frame)
    normalized = normalize_column_names(original)
    return frame.rename(dict(zip(original, normalized, strict=True)))


def profile_frame(frame: pl.DataFrame) -> FrameProfile:
    """Return row, null, dtype, and estimated-memory diagnostics."""

    null_cells = sum(frame.null_count().row(0)) if frame.width else 0
    return FrameProfile(
        rows=frame.height,
        columns=frame.width,
        null_cells=int(null_cells),
        estimated_size_bytes=int(frame.estimated_size()),
        dtypes=tuple(str(dtype) for dtype in frame.dtypes),
    )


def prepare_orders(frame: pl.DataFrame) -> pl.DataFrame:
    """Validate and clean an order table with native Polars expressions."""

    clean = normalize_frame_columns(frame)
    require_columns(
        clean,
        ("order_id", "customer_id", "order_at", "quantity", "unit_price"),
    )
    status_expr = (
        pl.col("status").cast(pl.String, strict=False).str.strip_chars().str.to_lowercase()
        if "status" in clean.columns
        else pl.lit("unknown")
    )
    result = (
        clean.with_columns(
            pl.col("order_id").cast(pl.String, strict=False),
            pl.col("customer_id").cast(pl.String, strict=False),
            pl.col("order_at")
            .cast(pl.String, strict=False)
            .str.to_datetime(strict=False)
            .alias("order_at"),
            pl.col("quantity").cast(pl.Int64, strict=False),
            pl.col("unit_price").cast(pl.Float64, strict=False),
            status_expr.fill_null("unknown").alias("status"),
        )
        .with_columns(
            (pl.col("quantity") * pl.col("unit_price")).alias("revenue")
        )
        .filter(
            pl.col("order_id").is_not_null()
            & pl.col("customer_id").is_not_null()
            & pl.col("order_at").is_not_null()
            & pl.col("quantity").is_not_null()
            & pl.col("unit_price").is_not_null()
            & (pl.col("quantity") > 0)
            & (pl.col("unit_price") >= 0)
        )
        .unique(subset=["order_id"], keep="last", maintain_order=True)
    )
    return result


def customer_summary(orders: pl.DataFrame) -> pl.DataFrame:
    """Build one deterministic analytical row per customer."""

    require_columns(orders, ("customer_id", "order_id", "order_at", "revenue"))
    return (
        orders.group_by("customer_id")
        .agg(
            pl.col("order_id").n_unique().alias("order_count"),
            pl.col("revenue").sum().alias("total_revenue"),
            pl.col("revenue").mean().alias("average_order_value"),
            pl.col("order_at").max().alias("latest_order_at"),
        )
        .sort("customer_id")
    )


def safe_left_join(
    left: pl.DataFrame,
    right: pl.DataFrame,
    *,
    on: str | list[str],
    validate: str = "m:1",
) -> pl.DataFrame:
    """Perform a left join while enforcing the expected key cardinality."""

    keys = [on] if isinstance(on, str) else on
    require_columns(left, keys)
    require_columns(right, keys)
    return left.join(right, on=on, how="left", validate=validate)


def top_n_per_group(
    frame: pl.DataFrame,
    *,
    group_column: str,
    value_column: str,
    n: int,
) -> pl.DataFrame:
    """Return deterministic top-N rows per group."""

    if n <= 0:
        raise ValueError("n must be positive")
    require_columns(frame, (group_column, value_column))
    row_index = "__source_row_index"
    if row_index in frame.columns:
        raise ValueError(f"reserved column already exists: {row_index}")
    return (
        frame.with_row_index(row_index)
        .sort(
            [group_column, value_column, row_index],
            descending=[False, True, False],
            nulls_last=True,
        )
        .group_by(group_column, maintain_order=True)
        .head(n)
        .drop(row_index)
    )


if __name__ == "__main__":
    sample = pl.DataFrame(
        {
            "Order ID": ["o1", "o2", "o2", "o3"],
            "Customer ID": ["c1", "c1", "c1", "c2"],
            "Order At": ["2026-01-01", "2026-01-02", "2026-01-02", "bad"],
            "Quantity": [2, 1, 1, 3],
            "Unit Price": [10.0, 5.0, 5.0, 7.5],
            "Status": ["Paid", " paid ", "PAID", None],
        }
    )
    prepared = prepare_orders(sample)
    print(prepared)
    print(customer_summary(prepared))
