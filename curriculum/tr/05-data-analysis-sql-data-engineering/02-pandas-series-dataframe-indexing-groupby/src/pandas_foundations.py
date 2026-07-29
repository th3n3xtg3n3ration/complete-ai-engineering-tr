"""Reliable pandas helpers for indexing, aggregation, joins, and validation."""

from __future__ import annotations

from dataclasses import dataclass
import re
from typing import Iterable, Mapping, Sequence

import pandas as pd


@dataclass(frozen=True)
class DataFrameProfile:
    rows: int
    columns: int
    missing_cells: int
    duplicate_rows: int
    memory_bytes: int


def require_columns(frame: pd.DataFrame, required: Iterable[str]) -> None:
    """Raise ``ValueError`` when one or more required columns are absent."""

    missing = sorted(set(required) - set(frame.columns))
    if missing:
        raise ValueError(f"missing required columns: {missing}")


def normalize_column_names(columns: Iterable[object]) -> list[str]:
    """Convert arbitrary labels to deterministic snake_case names.

    The function rejects collisions after normalization instead of silently
    overwriting columns.
    """

    normalized: list[str] = []
    for raw in columns:
        name = str(raw).strip().lower()
        name = re.sub(r"[^a-z0-9]+", "_", name).strip("_")
        if not name:
            raise ValueError("column names must contain at least one alphanumeric character")
        normalized.append(name)
    if len(normalized) != len(set(normalized)):
        raise ValueError("column names collide after normalization")
    return normalized


def normalize_frame_columns(frame: pd.DataFrame) -> pd.DataFrame:
    """Return a copy whose columns are normalized to snake_case."""

    result = frame.copy()
    result.columns = normalize_column_names(result.columns)
    return result


def profile_frame(frame: pd.DataFrame) -> DataFrameProfile:
    """Return compact structural and quality metrics for a DataFrame."""

    return DataFrameProfile(
        rows=int(frame.shape[0]),
        columns=int(frame.shape[1]),
        missing_cells=int(frame.isna().sum().sum()),
        duplicate_rows=int(frame.duplicated().sum()),
        memory_bytes=int(frame.memory_usage(index=True, deep=True).sum()),
    )


def filter_rows(
    frame: pd.DataFrame,
    *,
    equals: Mapping[str, object] | None = None,
    minimums: Mapping[str, float] | None = None,
) -> pd.DataFrame:
    """Filter rows with explicit boolean masks and return a defensive copy."""

    equals = equals or {}
    minimums = minimums or {}
    require_columns(frame, set(equals) | set(minimums))
    mask = pd.Series(True, index=frame.index, dtype=bool)
    for column, value in equals.items():
        mask &= frame[column].eq(value)
    for column, value in minimums.items():
        mask &= frame[column].ge(value)
    return frame.loc[mask].copy()


def assign_revenue(
    frame: pd.DataFrame,
    *,
    quantity_column: str = "quantity",
    unit_price_column: str = "unit_price",
    output_column: str = "revenue",
) -> pd.DataFrame:
    """Add a revenue column without mutating the input frame."""

    require_columns(frame, [quantity_column, unit_price_column])
    result = frame.copy()
    result[output_column] = (
        pd.to_numeric(result[quantity_column], errors="raise")
        * pd.to_numeric(result[unit_price_column], errors="raise")
    )
    return result


def grouped_summary(
    frame: pd.DataFrame,
    *,
    group_columns: Sequence[str],
    value_column: str,
) -> pd.DataFrame:
    """Aggregate count, sum, mean, median, min, and max by one or more keys."""

    if not group_columns:
        raise ValueError("group_columns must not be empty")
    require_columns(frame, [*group_columns, value_column])
    result = (
        frame.groupby(list(group_columns), dropna=False, observed=True)[value_column]
        .agg(["count", "sum", "mean", "median", "min", "max"])
        .reset_index()
    )
    return result


def safe_merge(
    left: pd.DataFrame,
    right: pd.DataFrame,
    *,
    on: str | Sequence[str],
    how: str = "left",
    validate: str | None = None,
) -> pd.DataFrame:
    """Merge frames while surfacing cardinality and key errors."""

    keys = [on] if isinstance(on, str) else list(on)
    require_columns(left, keys)
    require_columns(right, keys)
    if how not in {"left", "right", "inner", "outer"}:
        raise ValueError(f"unsupported merge type: {how}")
    return left.merge(right, on=keys, how=how, validate=validate, sort=False)


def top_n_per_group(
    frame: pd.DataFrame,
    *,
    group_column: str,
    value_column: str,
    n: int = 3,
) -> pd.DataFrame:
    """Return the highest-valued ``n`` rows within each group."""

    if n <= 0:
        raise ValueError("n must be positive")
    require_columns(frame, [group_column, value_column])
    ordered = frame.sort_values(
        [group_column, value_column], ascending=[True, False], kind="stable"
    )
    return ordered.groupby(group_column, dropna=False, observed=True).head(n).copy()


def parse_datetime_column(
    frame: pd.DataFrame,
    column: str,
    *,
    utc: bool = True,
) -> pd.DataFrame:
    """Parse a datetime column and reject invalid values."""

    require_columns(frame, [column])
    result = frame.copy()
    parsed = pd.to_datetime(result[column], errors="coerce", utc=utc)
    invalid = parsed.isna() & result[column].notna()
    if invalid.any():
        bad_examples = result.loc[invalid, column].astype(str).head(3).tolist()
        raise ValueError(f"invalid datetime values in {column}: {bad_examples}")
    result[column] = parsed
    return result


if __name__ == "__main__":
    sample = pd.DataFrame(
        {
            "Customer ID": [1, 1, 2],
            "Quantity": [2, 1, 4],
            "Unit Price": [5.0, 10.0, 3.0],
        }
    )
    sample = normalize_frame_columns(sample)
    sample = assign_revenue(sample)
    print(grouped_summary(sample, group_columns=["customer_id"], value_column="revenue"))
