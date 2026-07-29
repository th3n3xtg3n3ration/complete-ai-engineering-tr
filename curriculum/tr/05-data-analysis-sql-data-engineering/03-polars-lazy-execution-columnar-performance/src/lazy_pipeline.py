"""Lazy Polars pipeline examples with pushdown-friendly expressions."""

from __future__ import annotations

from pathlib import Path

import polars as pl

from polars_foundations import normalize_frame_columns, require_columns


def scan_csv(path: str | Path) -> pl.LazyFrame:
    """Create a lazy CSV scan without materializing the file."""

    return pl.scan_csv(
        path,
        null_values=["", "NA", "N/A", "null"],
        infer_schema_length=1_000,
        try_parse_dates=True,
    )


def build_order_query(
    orders: pl.LazyFrame,
    customers: pl.LazyFrame | None = None,
    *,
    minimum_revenue: float = 0.0,
) -> pl.LazyFrame:
    """Build a lazy analytical query using native expressions only."""

    if minimum_revenue < 0:
        raise ValueError("minimum_revenue must be non-negative")
    clean_orders = normalize_frame_columns(orders)
    require_columns(
        clean_orders,
        ("order_id", "customer_id", "order_at", "quantity", "unit_price"),
    )
    status_expr = (
        pl.col("status").cast(pl.String, strict=False).str.strip_chars().str.to_lowercase()
        if "status" in clean_orders.collect_schema().names()
        else pl.lit("unknown")
    )
    query = (
        clean_orders.with_columns(
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
        .filter(
            pl.col("customer_id").is_not_null()
            & pl.col("order_at").is_not_null()
            & pl.col("quantity").is_not_null()
            & pl.col("unit_price").is_not_null()
            & (pl.col("quantity") > 0)
            & (pl.col("unit_price") >= 0)
        )
        .with_columns(
            (pl.col("quantity") * pl.col("unit_price")).alias("revenue")
        )
        .filter(pl.col("revenue") >= minimum_revenue)
    )
    if customers is not None:
        clean_customers = normalize_frame_columns(customers)
        require_columns(clean_customers, ("customer_id",))
        query = query.join(
            clean_customers,
            on="customer_id",
            how="left",
            validate="m:1",
        )
    return query


def customer_metrics(query: pl.LazyFrame) -> pl.LazyFrame:
    """Aggregate a lazy order query into customer-level metrics."""

    require_columns(query, ("customer_id", "order_id", "order_at", "revenue"))
    return (
        query.group_by("customer_id")
        .agg(
            pl.col("order_id").n_unique().alias("order_count"),
            pl.col("revenue").sum().alias("total_revenue"),
            pl.col("revenue").mean().alias("average_order_value"),
            pl.col("order_at").max().alias("latest_order_at"),
        )
        .sort("customer_id")
    )


def collect_query(query: pl.LazyFrame, *, streaming: bool = False) -> pl.DataFrame:
    """Materialize a query with the automatic or streaming engine."""

    engine = "streaming" if streaming else "auto"
    return query.collect(engine=engine)


def optimized_plan(query: pl.LazyFrame) -> str:
    """Return the optimized logical plan for diagnostics and teaching."""

    return query.explain(optimized=True)


def sink_parquet(query: pl.LazyFrame, path: str | Path) -> None:
    """Execute a lazy query and write the result directly to Parquet."""

    query.sink_parquet(path)


if __name__ == "__main__":
    orders = pl.DataFrame(
        {
            "order_id": ["o1", "o2", "o3"],
            "customer_id": ["c1", "c1", "c2"],
            "order_at": ["2026-01-01", "2026-01-02", "2026-01-03"],
            "quantity": [2, 1, 4],
            "unit_price": [10.0, 8.0, 3.0],
            "status": ["paid", "paid", "refunded"],
        }
    )
    query = customer_metrics(build_order_query(orders.lazy()))
    print(optimized_plan(query))
    print(collect_query(query))
