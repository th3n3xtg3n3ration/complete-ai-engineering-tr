"""Tests for lesson 4 data-cleaning and leakage-safe preprocessing."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

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


quality = _load_module("data_quality")
pipeline = _load_module("preprocessing_pipeline")
leakage = _load_module("leakage_audit")


def test_require_columns_reports_missing() -> None:
    with pytest.raises(ValueError, match="missing required columns"):
        quality.require_columns(pd.DataFrame({"a": [1]}), ["a", "b"])


def test_profile_frame_counts_quality_issues() -> None:
    frame = pd.DataFrame({"a": [1, 1, None], "b": ["x", "x", "z"]})
    profile = quality.profile_frame(frame)
    assert profile.rows == 3
    assert profile.columns == 2
    assert profile.missing_cells == 1
    assert profile.duplicate_rows == 1
    assert profile.memory_bytes > 0


def test_missingness_report_is_sorted() -> None:
    frame = pd.DataFrame({"b": [1, None], "a": [None, None], "c": [1, 2]})
    report = quality.missingness_report(frame)
    assert report["column"].tolist() == ["a", "b", "c"]
    assert report["missing_rate"].tolist() == pytest.approx([1.0, 0.5, 0.0])


def test_duplicate_key_report() -> None:
    frame = pd.DataFrame({"id": [1, 1, 2], "value": [3, 4, 5]})
    report = quality.duplicate_key_report(frame, ["id"])
    assert report.to_dict("records") == [{"id": 1, "row_count": 2}]


def test_iqr_bounds_rejects_empty_numeric_data() -> None:
    with pytest.raises(ValueError, match="finite"):
        quality.iqr_bounds(pd.Series(["x", None]))


def test_cap_outliers_does_not_mutate_input() -> None:
    frame = pd.DataFrame({"value": [1.0, 2.0, 3.0, 100.0]})
    result, bounds = quality.cap_outliers_iqr(frame, ["value"])
    assert frame.loc[3, "value"] == 100.0
    assert result.loc[3, "value"] == pytest.approx(bounds["value"][1])


def test_robust_z_scores_handles_constant_series() -> None:
    result = quality.robust_z_scores(pd.Series([2.0, 2.0, 2.0]))
    assert result.tolist() == pytest.approx([0.0, 0.0, 0.0])


def test_coerce_numeric_columns_uses_nullable_float() -> None:
    frame = pd.DataFrame({"value": ["1", "bad", None]})
    result = quality.coerce_numeric_columns(frame, ["value"])
    assert str(result["value"].dtype) == "Float64"
    assert result["value"].isna().sum() == 2


def test_validate_numeric_range_rejects_invalid_value() -> None:
    with pytest.raises(ValueError, match="below"):
        quality.validate_numeric_range(
            pd.DataFrame({"age": [20, -1]}),
            "age",
            minimum=0,
        )


def _training_frame() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "age": [10.0, 30.0, None, 50.0, 70.0],
            "income": [100.0, 200.0, 300.0, 400.0, 500.0],
            "city": ["Ankara", "Ankara", "Izmir", None, "Rare"],
        }
    )


def _cleaner() -> pipeline.TabularCleaner:
    return pipeline.TabularCleaner(
        numeric_columns=("age", "income"),
        categorical_columns=("city",),
        rare_category_min_count=2,
    )


def test_cleaner_requires_fit() -> None:
    with pytest.raises(RuntimeError, match="fit"):
        _cleaner().transform(_training_frame())


def test_cleaner_uses_training_median() -> None:
    cleaner = _cleaner().fit(_training_frame())
    test = pd.DataFrame({"age": [None], "income": [250.0], "city": ["Ankara"]})
    result = cleaner.transform(test)
    assert result.loc[0, "age"] == pytest.approx(40.0)


def test_cleaner_maps_unknown_category_to_other() -> None:
    cleaner = _cleaner().fit(_training_frame())
    test = pd.DataFrame({"age": [40.0], "income": [250.0], "city": ["Bursa"]})
    result = cleaner.transform(test)
    assert result.loc[0, "city=__OTHER__"] == pytest.approx(1.0)


def test_cleaner_keeps_missing_category_separate() -> None:
    cleaner = _cleaner().fit(_training_frame())
    test = pd.DataFrame({"age": [40.0], "income": [250.0], "city": [None]})
    result = cleaner.transform(test)
    assert result.loc[0, "city=__MISSING__"] == pytest.approx(1.0)


def test_cleaner_columns_are_deterministic() -> None:
    cleaner = _cleaner().fit(_training_frame())
    first = cleaner.transform(_training_frame())
    second = cleaner.transform(_training_frame().iloc[::-1])
    assert first.columns.tolist() == second.columns.tolist() == list(cleaner.feature_names_)


def test_cleaner_does_not_mutate_input() -> None:
    frame = _training_frame()
    original = frame.copy(deep=True)
    _cleaner().fit_transform(frame)
    pd.testing.assert_frame_equal(frame, original)


def test_cleaner_clips_with_training_bounds() -> None:
    cleaner = _cleaner().fit(_training_frame())
    test = pd.DataFrame({"age": [10_000.0], "income": [250.0], "city": ["Ankara"]})
    result = cleaner.transform(test)
    assert result.loc[0, "age"] == pytest.approx(cleaner.bounds_["age"][1])


def test_feature_target_audit_flags_exact_proxy() -> None:
    frame = pd.DataFrame({"feature": [0, 1, 0], "target": [0, 1, 0]})
    findings = leakage.audit_feature_target_leakage(
        frame,
        target_column="target",
    )
    assert any(item.severity == "critical" for item in findings)


def test_feature_target_audit_flags_suspicious_name() -> None:
    frame = pd.DataFrame({"post_outcome_score": [1, 2, 3], "target": [0, 1, 0]})
    findings = leakage.audit_feature_target_leakage(
        frame,
        target_column="target",
    )
    assert any(item.column == "post_outcome_score" for item in findings)


def test_feature_target_audit_flags_near_perfect_numeric_proxy() -> None:
    frame = pd.DataFrame({"proxy": [0.0, 2.0, 4.0, 6.0], "target": [0, 1, 2, 3]})
    findings = leakage.audit_feature_target_leakage(
        frame,
        target_column="target",
    )
    assert any(item.column == "proxy" and item.severity == "critical" for item in findings)


def test_temporal_split_uses_strict_cutoff() -> None:
    frame = pd.DataFrame(
        {
            "event_at": ["2026-01-01", "2026-01-02", "2026-01-03"],
            "value": [1, 2, 3],
        }
    )
    train, evaluation = leakage.temporal_split(
        frame,
        time_column="event_at",
        cutoff="2026-01-03",
    )
    assert train["value"].tolist() == [1, 2]
    assert evaluation["value"].tolist() == [3]


def test_temporal_split_rejects_invalid_timestamp() -> None:
    frame = pd.DataFrame({"event_at": ["bad", "2026-01-02"]})
    with pytest.raises(ValueError, match="invalid timestamps"):
        leakage.temporal_split(
            frame,
            time_column="event_at",
            cutoff="2026-01-02",
        )


def test_overlapping_keys_returns_shared_entities() -> None:
    train = pd.DataFrame({"customer_id": [1, 2]})
    evaluation = pd.DataFrame({"customer_id": [2, 3]})
    overlap = leakage.overlapping_keys(
        train,
        evaluation,
        key_columns=["customer_id"],
    )
    assert overlap["customer_id"].tolist() == [2]


def test_assert_no_row_overlap_raises() -> None:
    train = pd.DataFrame({"row_id": [1, 2]})
    evaluation = pd.DataFrame({"row_id": [2, 3]})
    with pytest.raises(ValueError, match="overlap"):
        leakage.assert_no_row_overlap(
            train,
            evaluation,
            row_id_column="row_id",
        )
