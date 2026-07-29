"""A small fit/transform pipeline for tabular pandas data."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable

import pandas as pd

from pandas_foundations import require_columns


@dataclass
class TabularPreprocessor:
    """Learn imputation values and categorical levels from training data only."""

    numeric_columns: tuple[str, ...]
    categorical_columns: tuple[str, ...]
    missing_category: str = "__missing__"
    unknown_category: str = "__unknown__"
    numeric_medians_: dict[str, float] = field(default_factory=dict, init=False)
    categories_: dict[str, tuple[str, ...]] = field(default_factory=dict, init=False)
    fitted_: bool = field(default=False, init=False)

    def __post_init__(self) -> None:
        overlap = set(self.numeric_columns) & set(self.categorical_columns)
        if overlap:
            raise ValueError(f"columns cannot be both numeric and categorical: {sorted(overlap)}")

    @property
    def required_columns(self) -> tuple[str, ...]:
        return self.numeric_columns + self.categorical_columns

    def fit(self, frame: pd.DataFrame) -> "TabularPreprocessor":
        require_columns(frame, self.required_columns)
        medians: dict[str, float] = {}
        for column in self.numeric_columns:
            numeric = pd.to_numeric(frame[column], errors="coerce")
            median = numeric.median(skipna=True)
            if pd.isna(median):
                raise ValueError(f"numeric column contains no usable values: {column}")
            medians[column] = float(median)

        levels: dict[str, tuple[str, ...]] = {}
        for column in self.categorical_columns:
            cleaned = frame[column].astype("string").fillna(self.missing_category)
            unique = sorted(set(cleaned.astype(str)))
            if self.unknown_category not in unique:
                unique.append(self.unknown_category)
            levels[column] = tuple(unique)

        self.numeric_medians_ = medians
        self.categories_ = levels
        self.fitted_ = True
        return self

    def transform(self, frame: pd.DataFrame) -> pd.DataFrame:
        if not self.fitted_:
            raise RuntimeError("fit must be called before transform")
        require_columns(frame, self.required_columns)
        result = frame.loc[:, self.required_columns].copy()

        for column in self.numeric_columns:
            result[column] = pd.to_numeric(result[column], errors="coerce").fillna(
                self.numeric_medians_[column]
            )

        for column in self.categorical_columns:
            values = result[column].astype("string").fillna(self.missing_category).astype(str)
            known = set(self.categories_[column])
            values = values.where(values.isin(known), self.unknown_category)
            result[column] = pd.Categorical(values, categories=self.categories_[column])

        return result

    def fit_transform(self, frame: pd.DataFrame) -> pd.DataFrame:
        return self.fit(frame).transform(frame)


def one_hot_encode(
    frame: pd.DataFrame,
    columns: Iterable[str],
    *,
    dtype: str = "int8",
) -> pd.DataFrame:
    """Return deterministic one-hot encoded columns for categorical features."""

    columns = tuple(columns)
    require_columns(frame, columns)
    return pd.get_dummies(frame, columns=list(columns), dtype=dtype)


if __name__ == "__main__":
    train = pd.DataFrame(
        {
            "age": [20, None, 40],
            "city": ["Ankara", "Istanbul", None],
        }
    )
    pipeline = TabularPreprocessor(("age",), ("city",))
    print(one_hot_encode(pipeline.fit_transform(train), ["city"]))
