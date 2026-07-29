"""Tests for lesson 5 exploratory data analysis utilities."""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

import matplotlib
import numpy as np
import pandas as pd
import pytest

matplotlib.use("Agg")

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


foundations = _load_module("eda_foundations")
visualization = _load_module("visualization")
reporting = _load_module("eda_report")


@pytest.fixture
def frame() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "age": [20.0, 30.0, 40.0, 100.0],
            "income": [100.0, 200.0, 300.0, 400.0],
            "segment": ["A", "A", "B", None],
            "date": pd.to_datetime(
                ["2026-01-01", "2026-01-15", "2026-02-01", "2026-02-10"],
                utc=True,
            ),
            "target": [0, 0, 1, 1],
        }
    )


def test_require_columns_reports_missing(frame: pd.DataFrame) -> None:
    with pytest.raises(ValueError, match="missing required columns"):
        foundations.require_columns(frame, ["age", "missing"])


def test_profile_frame(frame: pd.DataFrame) -> None:
    profile = foundations.profile_frame(frame)
    assert profile.rows == 4
    assert profile.columns == 5
    assert profile.missing_cells == 1
    assert "age" in profile.numeric_columns
    assert "segment" in profile.categorical_columns
    assert "date" in profile.datetime_columns
    assert profile.memory_bytes > 0


def test_numeric_summary_contains_expected_statistics(frame: pd.DataFrame) -> None:
    summary = foundations.numeric_summary(frame, ["age"])
    assert summary.loc[0, "mean"] == pytest.approx(47.5)
    assert summary.loc[0, "median"] == pytest.approx(35.0)
    assert summary.loc[0, "iqr"] == pytest.approx(27.5)


def test_numeric_summary_rejects_non_numeric_column(frame: pd.DataFrame) -> None:
    with pytest.raises(TypeError, match="numeric"):
        foundations.numeric_summary(frame, ["segment"])


def test_categorical_summary_keeps_missing(frame: pd.DataFrame) -> None:
    summary = foundations.categorical_summary(frame, ["segment"])
    missing = summary.loc[summary["category"] == "<MISSING>", "count"].item()
    assert missing == 1
    assert summary["count"].sum() == 4


def test_categorical_summary_validates_top_n(frame: pd.DataFrame) -> None:
    with pytest.raises(ValueError, match="positive"):
        foundations.categorical_summary(frame, ["segment"], top_n=0)


def test_correlation_pairs_are_unique_and_sorted(frame: pd.DataFrame) -> None:
    result = foundations.correlation_pairs(frame, ["age", "income", "target"])
    assert len(result) == 3
    assert result["absolute_correlation"].is_monotonic_decreasing
    assert not (result["feature_a"] == result["feature_b"]).any()


def test_correlation_pairs_validate_method(frame: pd.DataFrame) -> None:
    with pytest.raises(ValueError, match="method"):
        foundations.correlation_pairs(frame, method="invalid")


def test_outlier_summary_detects_extreme_value() -> None:
    frame = pd.DataFrame({"value": [1.0, 2.0, 3.0, 4.0, 100.0]})
    summary = foundations.outlier_summary_iqr(frame)
    assert summary.loc[0, "outlier_count"] == 1


def test_segment_summary(frame: pd.DataFrame) -> None:
    result = foundations.segment_summary(
        frame,
        segment_columns=["segment"],
        metric_columns=["income"],
    )
    group_a = result.loc[result["segment"] == "A"]
    assert group_a["income_count"].item() == 2
    assert group_a["income_sum"].item() == pytest.approx(300.0)


def test_segment_summary_rejects_empty_segments(frame: pd.DataFrame) -> None:
    with pytest.raises(ValueError, match="must not be empty"):
        foundations.segment_summary(
            frame,
            segment_columns=[],
            metric_columns=["income"],
        )


def test_temporal_summary(frame: pd.DataFrame) -> None:
    result = foundations.temporal_summary(
        frame,
        date_column="date",
        value_column="income",
        frequency="MS",
    )
    assert result["row_count"].tolist() == [2, 2]
    assert result["sum"].tolist() == pytest.approx([300.0, 700.0])


def test_histogram_returns_figure(frame: pd.DataFrame) -> None:
    figure = visualization.histogram_figure(frame, "age", bins=4)
    assert figure.axes[0].get_xlabel() == "age"


def test_histogram_rejects_non_numeric_values() -> None:
    with pytest.raises(ValueError, match="no finite"):
        visualization.histogram_figure(pd.DataFrame({"x": ["a", "b"]}), "x")


def test_category_bar_returns_figure(frame: pd.DataFrame) -> None:
    figure = visualization.category_bar_figure(frame, "segment")
    assert figure.axes[0].get_ylabel() == "segment"


def test_scatter_with_group_returns_legend(frame: pd.DataFrame) -> None:
    figure = visualization.scatter_figure(
        frame,
        "age",
        "income",
        group="segment",
    )
    assert figure.axes[0].get_legend() is not None


def test_correlation_heatmap_requires_two_columns(frame: pd.DataFrame) -> None:
    with pytest.raises(ValueError, match="at least two"):
        visualization.correlation_heatmap_figure(frame, ["age"])


def test_save_figure_creates_file(frame: pd.DataFrame, tmp_path: Path) -> None:
    path = visualization.save_figure(
        visualization.missingness_figure(frame),
        tmp_path / "missingness.png",
    )
    assert path.exists()
    assert path.stat().st_size > 0


def test_demo_data_is_reproducible() -> None:
    first = reporting.make_demo_data(50, seed=7)
    second = reporting.make_demo_data(50, seed=7)
    pd.testing.assert_frame_equal(first, second)


def test_demo_data_validates_row_count() -> None:
    with pytest.raises(ValueError, match="positive"):
        reporting.make_demo_data(0)


def test_markdown_summary_contains_profile(frame: pd.DataFrame) -> None:
    config = reporting.EDAConfig(
        numeric_columns=("age", "income"),
        categorical_columns=("segment",),
        target_column="target",
    )
    text = reporting.build_markdown_summary(frame, config)
    assert "# Exploratory Data Analysis Report" in text
    assert "Rows: 4" in text
    assert "Target column: `target`" in text


def test_report_generation_writes_expected_artifacts(
    frame: pd.DataFrame,
    tmp_path: Path,
) -> None:
    config = reporting.EDAConfig(
        numeric_columns=("age", "income"),
        categorical_columns=("segment",),
        segment_columns=("segment",),
        target_column="target",
    )
    artifacts = reporting.generate_eda_report(frame, tmp_path, config)
    expected = {
        "profile",
        "numeric_summary",
        "categorical_summary",
        "outlier_summary",
        "correlation_pairs",
        "segment_summary",
        "report",
        "missingness_figure",
        "correlation_heatmap",
        "histogram_age",
        "histogram_income",
        "category_segment",
    }
    assert expected <= set(artifacts)
    assert all(path.exists() and path.stat().st_size > 0 for path in artifacts.values())
    profile = json.loads((tmp_path / "profile.json").read_text(encoding="utf-8"))
    assert profile["rows"] == 4


def test_report_rejects_missing_configured_column(
    frame: pd.DataFrame,
    tmp_path: Path,
) -> None:
    config = reporting.EDAConfig(
        numeric_columns=("does_not_exist",),
        categorical_columns=(),
    )
    with pytest.raises(ValueError, match="missing configured columns"):
        reporting.generate_eda_report(frame, tmp_path, config)
