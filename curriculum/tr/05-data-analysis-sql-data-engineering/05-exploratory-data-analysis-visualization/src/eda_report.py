"""Generate a repeatable EDA report with tables and Matplotlib figures."""

from __future__ import annotations

import json
from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd

from eda_foundations import (
    categorical_summary,
    correlation_pairs,
    numeric_summary,
    outlier_summary_iqr,
    profile_frame,
    segment_summary,
)
from visualization import (
    category_bar_figure,
    correlation_heatmap_figure,
    histogram_figure,
    missingness_figure,
    save_figure,
)


@dataclass(frozen=True)
class EDAConfig:
    """Explicit column roles used to produce a deterministic report."""

    numeric_columns: tuple[str, ...]
    categorical_columns: tuple[str, ...]
    segment_columns: tuple[str, ...] = ()
    target_column: str | None = None


def _ensure_columns(frame: pd.DataFrame, columns: Sequence[str]) -> None:
    missing = sorted(set(columns) - set(frame.columns))
    if missing:
        raise ValueError(f"missing configured columns: {missing}")


def build_markdown_summary(
    frame: pd.DataFrame,
    config: EDAConfig,
) -> str:
    """Build a concise Markdown narrative from computed EDA tables."""

    configured = [
        *config.numeric_columns,
        *config.categorical_columns,
        *config.segment_columns,
    ]
    if config.target_column:
        configured.append(config.target_column)
    _ensure_columns(frame, configured)

    profile = profile_frame(frame)
    numeric = numeric_summary(frame, config.numeric_columns)
    outliers = outlier_summary_iqr(frame, config.numeric_columns)
    correlations = correlation_pairs(frame, config.numeric_columns)

    lines = [
        "# Exploratory Data Analysis Report",
        "",
        "## Dataset profile",
        "",
        f"- Rows: {profile.rows}",
        f"- Columns: {profile.columns}",
        f"- Missing cells: {profile.missing_cells}",
        f"- Duplicate rows: {profile.duplicate_rows}",
        f"- Memory bytes: {profile.memory_bytes}",
        "",
        "## Numeric highlights",
        "",
    ]
    for record in numeric.to_dict("records"):
        lines.append(
            "- {column}: mean={mean:.4g}, median={median:.4g}, "
            "missing={missing_count}".format(**record)
        )

    lines.extend(["", "## Outlier highlights", ""])
    for record in outliers.to_dict("records"):
        lines.append(
            f"- {record['column']}: {record['outlier_count']} IQR outliers "
            f"({record['outlier_rate']:.1%})"
        )

    lines.extend(["", "## Strongest numeric relationships", ""])
    if correlations.empty:
        lines.append("- No valid numeric correlation pair was available.")
    else:
        for record in correlations.head(5).to_dict("records"):
            lines.append(
                f"- {record['feature_a']} ↔ {record['feature_b']}: "
                f"{record['correlation']:.3f}"
            )

    if config.target_column:
        lines.extend(
            [
                "",
                "## Target review",
                "",
                f"- Target column: `{config.target_column}`",
                f"- Missing target values: {int(frame[config.target_column].isna().sum())}",
                f"- Unique target values: {int(frame[config.target_column].nunique(dropna=True))}",
            ]
        )
    return "\n".join(lines) + "\n"


def generate_eda_report(
    frame: pd.DataFrame,
    output_dir: str | Path,
    config: EDAConfig,
) -> dict[str, Path]:
    """Write EDA tables, figures, and Markdown summary to one directory."""

    configured = [
        *config.numeric_columns,
        *config.categorical_columns,
        *config.segment_columns,
    ]
    if config.target_column:
        configured.append(config.target_column)
    _ensure_columns(frame, configured)

    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)
    artifacts: dict[str, Path] = {}

    profile_path = output / "profile.json"
    profile_path.write_text(
        json.dumps(profile_frame(frame).to_dict(), ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    artifacts["profile"] = profile_path

    tables = {
        "numeric_summary": numeric_summary(frame, config.numeric_columns),
        "categorical_summary": categorical_summary(
            frame, config.categorical_columns, top_n=20
        ),
        "outlier_summary": outlier_summary_iqr(frame, config.numeric_columns),
        "correlation_pairs": correlation_pairs(frame, config.numeric_columns),
    }
    if config.segment_columns and config.numeric_columns:
        tables["segment_summary"] = segment_summary(
            frame,
            segment_columns=config.segment_columns,
            metric_columns=config.numeric_columns,
        )
    for name, table in tables.items():
        path = output / f"{name}.csv"
        table.to_csv(path, index=False)
        artifacts[name] = path

    markdown_path = output / "report.md"
    markdown_path.write_text(build_markdown_summary(frame, config), encoding="utf-8")
    artifacts["report"] = markdown_path

    figure_path = output / "missingness.png"
    save_figure(missingness_figure(frame), figure_path)
    artifacts["missingness_figure"] = figure_path

    if len(config.numeric_columns) >= 2:
        path = output / "correlation_heatmap.png"
        save_figure(
            correlation_heatmap_figure(frame, config.numeric_columns),
            path,
        )
        artifacts["correlation_heatmap"] = path

    for column in config.numeric_columns:
        path = output / f"histogram_{column}.png"
        save_figure(histogram_figure(frame, column), path)
        artifacts[f"histogram_{column}"] = path

    for column in config.categorical_columns:
        path = output / f"category_{column}.png"
        save_figure(category_bar_figure(frame, column), path)
        artifacts[f"category_{column}"] = path

    return artifacts


def make_demo_data(row_count: int = 200, *, seed: int = 42) -> pd.DataFrame:
    """Generate deterministic customer data for the laboratory."""

    if row_count <= 0:
        raise ValueError("row_count must be positive")
    rng = np.random.default_rng(seed)
    age = rng.normal(39, 11, row_count).round(0)
    income = rng.lognormal(mean=10.5, sigma=0.45, size=row_count)
    tenure = rng.integers(1, 73, row_count)
    segment = rng.choice(["consumer", "business", "enterprise"], row_count)
    churn_probability = 1 / (
        1 + np.exp(-(-1.2 - 0.018 * tenure + 0.000005 * income))
    )
    churned = rng.binomial(1, churn_probability)

    frame = pd.DataFrame(
        {
            "age": age,
            "annual_income": income.round(2),
            "tenure_months": tenure,
            "segment": segment,
            "region": rng.choice(["north", "south", "east", "west"], row_count),
            "churned": churned,
        }
    )
    missing_indices = rng.choice(row_count, size=max(1, row_count // 20), replace=False)
    frame.loc[missing_indices, "annual_income"] = np.nan
    return frame


if __name__ == "__main__":
    demo = make_demo_data()
    config = EDAConfig(
        numeric_columns=("age", "annual_income", "tenure_months"),
        categorical_columns=("segment", "region"),
        segment_columns=("segment",),
        target_column="churned",
    )
    paths = generate_eda_report(demo, "eda-output", config)
    for name, path in paths.items():
        print(f"{name}: {path}")
