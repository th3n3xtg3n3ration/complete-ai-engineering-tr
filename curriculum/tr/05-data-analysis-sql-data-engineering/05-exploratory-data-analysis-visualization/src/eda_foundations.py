"""Reusable exploratory data analysis utilities built on pandas."""

from __future__ import annotations

from collections.abc import Iterable, Sequence
from dataclasses import asdict, dataclass
from typing import Any

import numpy as np
import pandas as pd


@dataclass(frozen=True)
class DataFrameProfile:
    """Compact structural and data-quality profile."""

    rows: int
    columns: int
    missing_cells: int
    duplicate_rows: int
    numeric_columns: tuple[str, ...]
    categorical_columns: tuple[str, ...]
    datetime_columns: tuple[str, ...]
    memory_bytes: int

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def require_columns(frame: pd.DataFrame, required: Iterable[str]) -> None:
    """Raise a clear error when required columns are absent."""

    missing = sorted(set(required) - set(frame.columns))
    if missing:
        raise ValueError(f"missing required columns: {missing}")


def profile_frame(frame: pd.DataFrame) -> DataFrameProfile:
    """Return structural, missingness, duplication, and dtype diagnostics."""

    numeric = tuple(frame.select_dtypes(include="number").columns)
    datetime_columns = tuple(
        column
        for column in frame.columns
        if pd.api.types.is_datetime64_any_dtype(frame[column])
    )
    categorical = tuple(
        column
        for column in frame.columns
        if column not in numeric and column not in datetime_columns
    )
    return DataFrameProfile(
        rows=len(frame),
        columns=len(frame.columns),
        missing_cells=int(frame.isna().sum().sum()),
        duplicate_rows=int(frame.duplicated().sum()),
        numeric_columns=numeric,
        categorical_columns=categorical,
        datetime_columns=datetime_columns,
        memory_bytes=int(frame.memory_usage(index=True, deep=True).sum()),
    )


def _resolve_numeric_columns(
    frame: pd.DataFrame,
    columns: Sequence[str] | None,
) -> list[str]:
    selected = (
        list(frame.select_dtypes(include="number").columns)
        if columns is None
        else list(columns)
    )
    require_columns(frame, selected)
    invalid = [
        column
        for column in selected
        if not pd.api.types.is_numeric_dtype(frame[column])
    ]
    if invalid:
        raise TypeError(f"columns must be numeric: {invalid}")
    return selected


def numeric_summary(
    frame: pd.DataFrame,
    columns: Sequence[str] | None = None,
) -> pd.DataFrame:
    """Return deterministic descriptive statistics for numeric columns."""

    selected = _resolve_numeric_columns(frame, columns)
    records: list[dict[str, float | int | str]] = []
    for column in selected:
        values = pd.to_numeric(frame[column], errors="coerce")
        finite = values.replace([np.inf, -np.inf], np.nan).dropna()
        if finite.empty:
            records.append(
                {
                    "column": column,
                    "count": 0,
                    "missing_count": int(values.isna().sum()),
                    "mean": np.nan,
                    "std": np.nan,
                    "min": np.nan,
                    "q1": np.nan,
                    "median": np.nan,
                    "q3": np.nan,
                    "max": np.nan,
                    "iqr": np.nan,
                    "skew": np.nan,
                }
            )
            continue
        q1 = float(finite.quantile(0.25))
        q3 = float(finite.quantile(0.75))
        records.append(
            {
                "column": column,
                "count": int(finite.count()),
                "missing_count": int(values.isna().sum()),
                "mean": float(finite.mean()),
                "std": float(finite.std(ddof=1)) if len(finite) > 1 else 0.0,
                "min": float(finite.min()),
                "q1": q1,
                "median": float(finite.median()),
                "q3": q3,
                "max": float(finite.max()),
                "iqr": q3 - q1,
                "skew": float(finite.skew()) if len(finite) > 2 else 0.0,
            }
        )
    return pd.DataFrame.from_records(records)


def categorical_summary(
    frame: pd.DataFrame,
    columns: Sequence[str] | None = None,
    *,
    top_n: int = 10,
    missing_label: str = "<MISSING>",
) -> pd.DataFrame:
    """Return top category counts and rates in long format."""

    if top_n <= 0:
        raise ValueError("top_n must be positive")
    selected = (
        list(frame.select_dtypes(exclude="number").columns)
        if columns is None
        else list(columns)
    )
    require_columns(frame, selected)
    records: list[dict[str, object]] = []
    row_count = len(frame)
    for column in selected:
        values = frame[column].astype("string").fillna(missing_label)
        counts = values.value_counts(dropna=False).head(top_n)
        for category, count in counts.items():
            records.append(
                {
                    "column": column,
                    "category": str(category),
                    "count": int(count),
                    "rate": float(count / row_count) if row_count else 0.0,
                }
            )
    return pd.DataFrame.from_records(
        records,
        columns=["column", "category", "count", "rate"],
    )


def correlation_pairs(
    frame: pd.DataFrame,
    columns: Sequence[str] | None = None,
    *,
    method: str = "pearson",
    minimum_absolute: float = 0.0,
) -> pd.DataFrame:
    """Return unique correlation pairs sorted by absolute strength."""

    if method not in {"pearson", "spearman", "kendall"}:
        raise ValueError("method must be pearson, spearman, or kendall")
    if not 0.0 <= minimum_absolute <= 1.0:
        raise ValueError("minimum_absolute must be between 0 and 1")
    selected = _resolve_numeric_columns(frame, columns)
    correlation = frame[selected].corr(method=method)
    records: list[dict[str, object]] = []
    for left_index, left in enumerate(selected):
        for right in selected[left_index + 1 :]:
            value = correlation.loc[left, right]
            if pd.isna(value) or abs(float(value)) < minimum_absolute:
                continue
            records.append(
                {
                    "feature_a": left,
                    "feature_b": right,
                    "correlation": float(value),
                    "absolute_correlation": abs(float(value)),
                }
            )
    result = pd.DataFrame.from_records(
        records,
        columns=[
            "feature_a",
            "feature_b",
            "correlation",
            "absolute_correlation",
        ],
    )
    if result.empty:
        return result
    return result.sort_values(
        ["absolute_correlation", "feature_a", "feature_b"],
        ascending=[False, True, True],
        kind="stable",
    ).reset_index(drop=True)


def outlier_summary_iqr(
    frame: pd.DataFrame,
    columns: Sequence[str] | None = None,
    *,
    multiplier: float = 1.5,
) -> pd.DataFrame:
    """Summarize IQR outlier counts without mutating the source frame."""

    if multiplier <= 0:
        raise ValueError("multiplier must be positive")
    selected = _resolve_numeric_columns(frame, columns)
    records: list[dict[str, object]] = []
    for column in selected:
        values = pd.to_numeric(frame[column], errors="coerce").dropna()
        if values.empty:
            lower = upper = np.nan
            count = 0
        else:
            q1 = float(values.quantile(0.25))
            q3 = float(values.quantile(0.75))
            iqr = q3 - q1
            lower = q1 - multiplier * iqr
            upper = q3 + multiplier * iqr
            count = int(((values < lower) | (values > upper)).sum())
        records.append(
            {
                "column": column,
                "lower_bound": lower,
                "upper_bound": upper,
                "outlier_count": count,
                "outlier_rate": float(count / len(values)) if len(values) else 0.0,
            }
        )
    return pd.DataFrame.from_records(records)


def segment_summary(
    frame: pd.DataFrame,
    *,
    segment_columns: Sequence[str],
    metric_columns: Sequence[str],
) -> pd.DataFrame:
    """Aggregate count, mean, median, and sum for analytical segments."""

    if not segment_columns:
        raise ValueError("segment_columns must not be empty")
    if not metric_columns:
        raise ValueError("metric_columns must not be empty")
    require_columns(frame, [*segment_columns, *metric_columns])
    _resolve_numeric_columns(frame, metric_columns)
    grouped = (
        frame.groupby(list(segment_columns), dropna=False, observed=True)[
            list(metric_columns)
        ]
        .agg(["count", "mean", "median", "sum"])
        .reset_index()
    )
    grouped.columns = [
        "_".join(str(part) for part in column if str(part))
        if isinstance(column, tuple)
        else str(column)
        for column in grouped.columns
    ]
    return grouped


def temporal_summary(
    frame: pd.DataFrame,
    *,
    date_column: str,
    value_column: str,
    frequency: str = "MS",
) -> pd.DataFrame:
    """Aggregate a numeric value across deterministic time buckets."""

    require_columns(frame, (date_column, value_column))
    values = frame[[date_column, value_column]].copy()
    values[date_column] = pd.to_datetime(values[date_column], errors="coerce", utc=True)
    values[value_column] = pd.to_numeric(values[value_column], errors="coerce")
    values = values.dropna(subset=[date_column, value_column])
    if values.empty:
        return pd.DataFrame(
            columns=["period", "row_count", "sum", "mean", "median"]
        )
    result = (
        values.set_index(date_column)[value_column]
        .resample(frequency)
        .agg(["count", "sum", "mean", "median"])
        .rename(columns={"count": "row_count"})
        .reset_index()
        .rename(columns={date_column: "period"})
    )
    return result
