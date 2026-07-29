"""Tests for linear regression, regularization, and evaluation utilities."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import numpy as np
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


models = _load_module("linear_models")
diagnostics = _load_module("regression_diagnostics")
pipelines = _load_module("regression_pipeline")


@pytest.fixture
def linear_data():
    return models.make_linear_regression_data(
        row_count=300,
        feature_count=3,
        noise_standard_deviation=0.05,
        random_state=7,
    )


@pytest.fixture
def tabular_data():
    rng = np.random.default_rng(5)
    rows = 160
    frame = pd.DataFrame(
        {
            "size_m2": rng.normal(110, 25, rows),
            "room_count": rng.integers(1, 6, rows),
            "age_years": rng.integers(0, 40, rows).astype(float),
            "district": rng.choice(["north", "south", "central"], rows),
        }
    )
    frame.loc[0, "age_years"] = np.nan
    district_effect = frame["district"].map(
        {"north": 200_000.0, "south": -100_000.0, "central": 300_000.0}
    )
    target = (
        800_000
        + 22_000 * frame["size_m2"]
        + 80_000 * frame["room_count"]
        - 7_500 * frame["age_years"].fillna(frame["age_years"].median())
        + district_effect
        + rng.normal(0, 30_000, rows)
    )
    return frame, target


def test_make_data_is_reproducible() -> None:
    first = models.make_linear_regression_data(random_state=3)
    second = models.make_linear_regression_data(random_state=3)
    assert np.array_equal(first[0], second[0])
    assert np.array_equal(first[1], second[1])


def test_make_data_rejects_invalid_arguments() -> None:
    with pytest.raises(ValueError, match="row_count"):
        models.make_linear_regression_data(row_count=0)


def test_normal_equation_recovers_coefficients(linear_data) -> None:
    X, y, coefficients, intercept = linear_data
    model = models.NormalEquationRegressor().fit(X, y)
    assert model.coefficients_ == pytest.approx(coefficients, abs=0.02)
    assert model.intercept_ == pytest.approx(intercept, abs=0.02)


def test_normal_equation_predict_requires_fit() -> None:
    with pytest.raises(RuntimeError, match="fit"):
        models.NormalEquationRegressor().predict([[1.0]])


def test_normal_equation_supports_no_intercept() -> None:
    X = np.arange(1, 5, dtype=float).reshape(-1, 1)
    y = 2 * X[:, 0]
    model = models.NormalEquationRegressor(fit_intercept=False).fit(X, y)
    assert model.intercept_ == 0.0
    assert model.coefficients_ == pytest.approx([2.0])


def test_normal_equation_validates_row_count() -> None:
    with pytest.raises(ValueError, match="same number"):
        models.NormalEquationRegressor().fit([[1], [2]], [1])


def test_gradient_descent_converges(linear_data) -> None:
    X, y, coefficients, intercept = linear_data
    model = models.GradientDescentRegressor(
        learning_rate=0.05,
        max_iterations=10_000,
        tolerance=1e-12,
    ).fit(X, y)
    assert model.coefficients_ == pytest.approx(coefficients, abs=0.03)
    assert model.intercept_ == pytest.approx(intercept, abs=0.03)
    assert model.loss_history_[-1] < model.loss_history_[0]


def test_gradient_descent_rejects_bad_hyperparameters() -> None:
    with pytest.raises(ValueError, match="learning_rate"):
        models.GradientDescentRegressor(learning_rate=0)


def test_gradient_descent_l2_shrinks_coefficients(linear_data) -> None:
    X, y, _, _ = linear_data
    plain = models.GradientDescentRegressor(l2_penalty=0.0).fit(X, y)
    ridge = models.GradientDescentRegressor(l2_penalty=2.0).fit(X, y)
    assert np.linalg.norm(ridge.coefficients_) < np.linalg.norm(plain.coefficients_)


def test_regression_metrics_perfect_prediction() -> None:
    result = diagnostics.regression_metrics([1, 2, 3], [1, 2, 3], feature_count=1)
    assert result.mae == 0.0
    assert result.rmse == 0.0
    assert result.r2 == 1.0
    assert result.adjusted_r2 == 1.0


def test_regression_metrics_can_have_negative_r2() -> None:
    result = diagnostics.regression_metrics([1, 2, 3], [100, 100, 100])
    assert result.r2 < 0


def test_regression_metrics_validates_shapes() -> None:
    with pytest.raises(ValueError, match="identical shape"):
        diagnostics.regression_metrics([1, 2], [1])


def test_adjusted_r2_is_none_when_degrees_of_freedom_invalid() -> None:
    result = diagnostics.regression_metrics([1, 2], [1, 2], feature_count=2)
    assert result.adjusted_r2 is None


def test_residual_summary_reports_direction() -> None:
    summary = diagnostics.residual_summary([10, 10], [8, 12])
    assert summary.mean == 0.0
    assert summary.underprediction_rate == 0.5
    assert summary.overprediction_rate == 0.5
    assert summary.maximum_absolute_residual == 2.0


def test_heteroskedasticity_signal_detects_pattern() -> None:
    fitted = np.arange(1, 21, dtype=float)
    residuals = np.arange(1, 21, dtype=float)
    assert diagnostics.heteroskedasticity_signal(fitted, residuals) > 0.99


def test_heteroskedasticity_signal_handles_constant_values() -> None:
    assert diagnostics.heteroskedasticity_signal([1, 1], [2, -2]) == 0.0


def test_vif_detects_collinearity() -> None:
    frame = pd.DataFrame(
        {
            "a": np.arange(1, 21, dtype=float),
            "b": np.arange(1, 21, dtype=float) * 2,
            "c": np.arange(1, 21, dtype=float) ** 2,
        }
    )
    result = diagnostics.variance_inflation_factors(frame, ["a", "b", "c"])
    assert np.isinf(result.loc[result["feature"].isin(["a", "b"]), "vif"]).all()


def test_vif_requires_finite_values() -> None:
    frame = pd.DataFrame({"a": [1, np.nan], "b": [2, 3]})
    with pytest.raises(ValueError, match="finite"):
        diagnostics.variance_inflation_factors(frame, ["a", "b"])


def test_slice_metrics_orders_worst_slice_first() -> None:
    frame = pd.DataFrame(
        {
            "segment": ["a", "a", "b", "b"],
            "actual": [1.0, 2.0, 1.0, 2.0],
            "prediction": [1.0, 2.0, 4.0, 5.0],
        }
    )
    result = diagnostics.slice_regression_metrics(
        frame,
        actual_column="actual",
        prediction_column="prediction",
        slice_columns=["segment"],
    )
    assert result.loc[0, "segment"] == "b"


def test_slice_metrics_requires_slice_column() -> None:
    frame = pd.DataFrame({"actual": [1], "prediction": [1]})
    with pytest.raises(ValueError, match="slice_columns"):
        diagnostics.slice_regression_metrics(
            frame,
            actual_column="actual",
            prediction_column="prediction",
            slice_columns=[],
        )


def test_worst_residual_rows() -> None:
    frame = pd.DataFrame(
        {"actual": [1, 2, 3], "prediction": [1, 10, 2], "id": ["a", "b", "c"]}
    )
    result = diagnostics.worst_residual_rows(
        frame,
        actual_column="actual",
        prediction_column="prediction",
        top_n=1,
    )
    assert result.loc[0, "id"] == "b"


def test_preprocessor_requires_features() -> None:
    with pytest.raises(ValueError, match="at least one"):
        pipelines.build_preprocessor([], [])


def test_preprocessor_rejects_overlap() -> None:
    with pytest.raises(ValueError, match="overlap"):
        pipelines.build_preprocessor(["x"], ["x"])


def test_pipeline_handles_missing_and_unknown_category(tabular_data) -> None:
    frame, target = tabular_data
    train = frame.iloc[:120]
    evaluation = frame.iloc[120:].copy()
    evaluation.loc[evaluation.index[0], "district"] = "unknown"
    pipeline = pipelines.build_regression_pipeline(
        ["size_m2", "room_count", "age_years"],
        ["district"],
        model_name="ridge",
    )
    pipeline.fit(train, target.iloc[:120])
    predictions = pipeline.predict(evaluation)
    assert len(predictions) == len(evaluation)
    assert np.isfinite(predictions).all()


def test_build_pipeline_rejects_unknown_model() -> None:
    with pytest.raises(ValueError, match="unsupported"):
        pipelines.build_regression_pipeline(["x"], [], model_name="forest")


def test_build_pipeline_validates_elastic_net_ratio() -> None:
    with pytest.raises(ValueError, match="l1_ratio"):
        pipelines.build_regression_pipeline(
            ["x"],
            [],
            model_name="elastic_net",
            l1_ratio=2.0,
        )


def test_polynomial_pipeline_adds_features(tabular_data) -> None:
    frame, target = tabular_data
    pipeline = pipelines.build_regression_pipeline(
        ["size_m2", "room_count", "age_years"],
        [],
        model_name="ridge",
        polynomial_degree=2,
    )
    pipeline.fit(frame.drop(columns="district"), target)
    names = pipeline[:-1].get_feature_names_out()
    assert len(names) > 3


def test_evaluate_pipeline_returns_metrics(tabular_data) -> None:
    frame, target = tabular_data
    pipeline = pipelines.build_regression_pipeline(
        ["size_m2", "room_count", "age_years"],
        ["district"],
        model_name="ridge",
    )
    result = pipelines.evaluate_pipeline(
        pipeline,
        frame.iloc[:120],
        target.iloc[:120],
        frame.iloc[120:],
        target.iloc[120:],
        model_name="ridge",
    )
    assert result.rmse > 0
    assert result.r2 > 0.9


def test_compare_models_returns_sorted_table(tabular_data) -> None:
    frame, target = tabular_data
    configured = {
        name: pipelines.build_regression_pipeline(
            ["size_m2", "room_count", "age_years"],
            ["district"],
            model_name=name,
            alpha=0.1,
        )
        for name in ("linear", "ridge", "lasso", "elastic_net")
    }
    result = pipelines.compare_models(
        configured,
        frame.iloc[:120],
        target.iloc[:120],
        frame.iloc[120:],
        target.iloc[120:],
    )
    assert set(result["model_name"]) == set(configured)
    assert result["rmse"].is_monotonic_increasing


def test_cross_validation_report(tabular_data) -> None:
    frame, target = tabular_data
    pipeline = pipelines.build_regression_pipeline(
        ["size_m2", "room_count", "age_years"],
        ["district"],
        model_name="ridge",
    )
    report = pipelines.cross_validation_report(pipeline, frame, target, folds=4)
    assert report["rmse_mean"] > 0
    assert report["r2_mean"] > 0.9


def test_cross_validation_requires_two_folds(tabular_data) -> None:
    frame, target = tabular_data
    pipeline = pipelines.build_regression_pipeline(
        ["size_m2"],
        ["district"],
    )
    with pytest.raises(ValueError, match="at least two"):
        pipelines.cross_validation_report(pipeline, frame, target, folds=1)
