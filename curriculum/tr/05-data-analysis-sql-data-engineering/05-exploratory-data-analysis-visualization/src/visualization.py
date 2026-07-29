"""Matplotlib-based visualization helpers for reproducible EDA."""

from __future__ import annotations

from pathlib import Path
from typing import Sequence

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.figure import Figure


def _require_column(frame: pd.DataFrame, column: str) -> None:
    if column not in frame.columns:
        raise ValueError(f"missing required column: {column}")


def histogram_figure(
    frame: pd.DataFrame,
    column: str,
    *,
    bins: int = 20,
    title: str | None = None,
) -> Figure:
    """Create a numeric histogram and return its Figure."""

    if bins <= 0:
        raise ValueError("bins must be positive")
    _require_column(frame, column)
    values = pd.to_numeric(frame[column], errors="coerce")
    values = values.replace([np.inf, -np.inf], np.nan).dropna()
    if values.empty:
        raise ValueError(f"column has no finite numeric values: {column}")
    figure, axis = plt.subplots()
    axis.hist(values, bins=bins)
    axis.set_title(title or f"{column} distribution")
    axis.set_xlabel(column)
    axis.set_ylabel("Count")
    figure.tight_layout()
    return figure


def category_bar_figure(
    frame: pd.DataFrame,
    column: str,
    *,
    top_n: int = 10,
    include_missing: bool = True,
) -> Figure:
    """Create a top-category count bar chart."""

    if top_n <= 0:
        raise ValueError("top_n must be positive")
    _require_column(frame, column)
    values = frame[column].astype("string")
    if include_missing:
        values = values.fillna("<MISSING>")
    else:
        values = values.dropna()
    counts = values.value_counts().head(top_n).sort_values(ascending=True)
    if counts.empty:
        raise ValueError(f"column has no plottable values: {column}")
    figure, axis = plt.subplots()
    axis.barh(counts.index.astype(str), counts.to_numpy())
    axis.set_title(f"Top {column} categories")
    axis.set_xlabel("Count")
    axis.set_ylabel(column)
    figure.tight_layout()
    return figure


def scatter_figure(
    frame: pd.DataFrame,
    x: str,
    y: str,
    *,
    group: str | None = None,
) -> Figure:
    """Create a scatter chart, optionally separated by a categorical group."""

    required = [x, y] + ([group] if group else [])
    missing = [column for column in required if column not in frame.columns]
    if missing:
        raise ValueError(f"missing required columns: {missing}")
    data = frame[required].copy()
    data[x] = pd.to_numeric(data[x], errors="coerce")
    data[y] = pd.to_numeric(data[y], errors="coerce")
    data = data.dropna(subset=[x, y])
    if data.empty:
        raise ValueError("scatter data has no finite x/y rows")

    figure, axis = plt.subplots()
    if group is None:
        axis.scatter(data[x], data[y], alpha=0.7)
    else:
        for label, subset in data.groupby(group, dropna=False, observed=True):
            axis.scatter(subset[x], subset[y], alpha=0.7, label=str(label))
        axis.legend(title=group)
    axis.set_title(f"{y} vs {x}")
    axis.set_xlabel(x)
    axis.set_ylabel(y)
    figure.tight_layout()
    return figure


def correlation_heatmap_figure(
    frame: pd.DataFrame,
    columns: Sequence[str] | None = None,
) -> Figure:
    """Create a correlation heatmap without a seaborn dependency."""

    selected = (
        list(frame.select_dtypes(include="number").columns)
        if columns is None
        else list(columns)
    )
    missing = sorted(set(selected) - set(frame.columns))
    if missing:
        raise ValueError(f"missing required columns: {missing}")
    if len(selected) < 2:
        raise ValueError("at least two numeric columns are required")
    invalid = [
        column
        for column in selected
        if not pd.api.types.is_numeric_dtype(frame[column])
    ]
    if invalid:
        raise TypeError(f"columns must be numeric: {invalid}")

    correlation = frame[selected].corr()
    figure, axis = plt.subplots()
    image = axis.imshow(correlation.to_numpy(), vmin=-1.0, vmax=1.0)
    axis.set_xticks(range(len(selected)), selected, rotation=45, ha="right")
    axis.set_yticks(range(len(selected)), selected)
    axis.set_title("Correlation matrix")
    figure.colorbar(image, ax=axis, label="Correlation")
    figure.tight_layout()
    return figure


def missingness_figure(frame: pd.DataFrame) -> Figure:
    """Create a missing-value rate bar chart."""

    rates = frame.isna().mean().sort_values(ascending=True)
    figure, axis = plt.subplots()
    axis.barh(rates.index.astype(str), rates.to_numpy())
    axis.set_xlim(0.0, 1.0)
    axis.set_title("Missing-value rates")
    axis.set_xlabel("Missing rate")
    figure.tight_layout()
    return figure


def save_figure(
    figure: Figure,
    path: str | Path,
    *,
    dpi: int = 150,
    close: bool = True,
) -> Path:
    """Persist a figure and optionally release Matplotlib resources."""

    if dpi <= 0:
        raise ValueError("dpi must be positive")
    output = Path(path)
    output.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(output, dpi=dpi, bbox_inches="tight")
    if close:
        plt.close(figure)
    return output
