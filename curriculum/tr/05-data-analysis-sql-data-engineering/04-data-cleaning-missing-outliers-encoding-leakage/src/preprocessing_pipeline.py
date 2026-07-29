"""Leakage-safe fit/transform preprocessing for tabular data."""

from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np
import pandas as pd

from data_quality import iqr_bounds, require_columns


_MISSING = "__MISSING__"
_OTHER = "__OTHER__"


def _normalize_category(series: pd.Series) -> pd.Series:
    text = series.astype("string").str.strip().str.lower()
    return text.fillna(_MISSING)


@dataclass
class TabularCleaner:
    """Learn imputation, clipping, and category mappings from training data only."""

    numeric_columns: tuple[str, ...]
    categorical_columns: tuple[str, ...]
    outlier_multiplier: float = 1.5
    rare_category_min_count: int = 2
    medians_: dict[str, float] = field(default_factory=dict, init=False)
    bounds_: dict[str, tuple[float, float]] = field(default_factory=dict, init=False)
    categories_: dict[str, tuple[str, ...]] = field(default_factory=dict, init=False)
    feature_names_: tuple[str, ...] = field(default=(), init=False)
    is_fitted_: bool = field(default=False, init=False)

    def __post_init__(self) -> None:
        if set(self.numeric_columns) & set(self.categorical_columns):
            raise ValueError("numeric and categorical columns must be disjoint")
        if self.outlier_multiplier <= 0 or not np.isfinite(self.outlier_multiplier):
            raise ValueError("outlier_multiplier must be positive and finite")
        if self.rare_category_min_count <= 0:
            raise ValueError("rare_category_min_count must be positive")

    @property
    def required_columns(self) -> tuple[str, ...]:
        return self.numeric_columns + self.categorical_columns

    def fit(self, frame: pd.DataFrame) -> "TabularCleaner":
        """Fit all preprocessing statistics on training data."""

        require_columns(frame, self.required_columns)
        self.medians_.clear()
        self.bounds_.clear()
        self.categories_.clear()

        for column in self.numeric_columns:
            numeric = pd.to_numeric(frame[column], errors="coerce").replace(
                [np.inf, -np.inf], np.nan
            )
            finite = numeric.dropna()
            if finite.empty:
                raise ValueError(f"{column} has no finite training values")
            self.medians_[column] = float(finite.median())
            self.bounds_[column] = iqr_bounds(
                finite,
                multiplier=self.outlier_multiplier,
            )

        for column in self.categorical_columns:
            normalized = _normalize_category(frame[column])
            counts = normalized.value_counts(dropna=False)
            kept = sorted(
                str(value)
                for value, count in counts.items()
                if int(count) >= self.rare_category_min_count and value != _MISSING
            )
            categories = tuple([_MISSING, _OTHER, *kept])
            self.categories_[column] = categories

        names = list(self.numeric_columns)
        for column in self.categorical_columns:
            names.extend(f"{column}={value}" for value in self.categories_[column])
        self.feature_names_ = tuple(names)
        self.is_fitted_ = True
        return self

    def transform(self, frame: pd.DataFrame) -> pd.DataFrame:
        """Apply training statistics without learning from new data."""

        if not self.is_fitted_:
            raise RuntimeError("fit must be called before transform")
        require_columns(frame, self.required_columns)
        output = pd.DataFrame(index=frame.index)

        for column in self.numeric_columns:
            numeric = pd.to_numeric(frame[column], errors="coerce").replace(
                [np.inf, -np.inf], np.nan
            )
            lower, upper = self.bounds_[column]
            output[column] = (
                numeric.clip(lower, upper)
                .fillna(self.medians_[column])
                .astype(float)
            )

        for column in self.categorical_columns:
            normalized = _normalize_category(frame[column])
            allowed = set(self.categories_[column])
            mapped = normalized.where(normalized.isin(allowed), _OTHER)
            categorical = pd.Categorical(
                mapped,
                categories=list(self.categories_[column]),
            )
            encoded = pd.get_dummies(
                categorical,
                prefix=column,
                prefix_sep="=",
                dtype=float,
            )
            encoded.index = frame.index
            for category in self.categories_[column]:
                name = f"{column}={category}"
                output[name] = encoded.get(name, pd.Series(0.0, index=frame.index))

        return output.loc[:, self.feature_names_].copy()

    def fit_transform(self, frame: pd.DataFrame) -> pd.DataFrame:
        """Fit on training data and return transformed training features."""

        return self.fit(frame).transform(frame)
