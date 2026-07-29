"""Problem framing, validation, and leakage-aware dataset splitting utilities."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

import pandas as pd
from sklearn.model_selection import GroupShuffleSplit, train_test_split

TaskType = Literal[
    "regression",
    "binary_classification",
    "multiclass_classification",
]
SplitStrategy = Literal["random", "temporal", "entity"]


@dataclass(frozen=True)
class ValidationReport:
    """Compact diagnostics for a machine-learning problem table."""

    rows: int
    feature_count: int
    target_missing_count: int
    duplicate_entity_rows: int
    target_classes: tuple[object, ...]


@dataclass(frozen=True)
class DataSplit:
    """Train and evaluation partitions with their original row indices."""

    train: pd.DataFrame
    evaluation: pd.DataFrame
    strategy: SplitStrategy


@dataclass(frozen=True)
class ProblemDefinition:
    """Explicit contract for one supervised machine-learning problem."""

    name: str
    task_type: TaskType
    target_column: str
    feature_columns: tuple[str, ...]
    id_columns: tuple[str, ...] = ()
    timestamp_column: str | None = None
    positive_label: object | None = None
    excluded_columns: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not self.name.strip():
            raise ValueError("name must not be empty")
        if self.task_type not in {
            "regression",
            "binary_classification",
            "multiclass_classification",
        }:
            raise ValueError(f"unsupported task_type: {self.task_type}")
        if not self.target_column.strip():
            raise ValueError("target_column must not be empty")
        if not self.feature_columns:
            raise ValueError("feature_columns must not be empty")
        if len(set(self.feature_columns)) != len(self.feature_columns):
            raise ValueError("feature_columns must be unique")
        if self.target_column in self.feature_columns:
            raise ValueError("target_column must not be included in feature_columns")
        if set(self.excluded_columns) & set(self.feature_columns):
            raise ValueError("excluded_columns cannot also be feature_columns")
        if self.task_type == "binary_classification" and self.positive_label is None:
            raise ValueError("binary_classification requires positive_label")

    @property
    def required_columns(self) -> tuple[str, ...]:
        """Return all columns required to validate and split the dataset."""

        columns = [*self.feature_columns, self.target_column, *self.id_columns]
        if self.timestamp_column is not None:
            columns.append(self.timestamp_column)
        return tuple(dict.fromkeys(columns))

    def validate_frame(self, frame: pd.DataFrame) -> ValidationReport:
        """Validate schema, target semantics, and entity uniqueness diagnostics."""

        missing = sorted(set(self.required_columns) - set(frame.columns))
        if missing:
            raise ValueError(f"missing required columns: {missing}")
        if frame.empty:
            raise ValueError("frame must not be empty")

        target = frame[self.target_column]
        non_missing_target = target.dropna()
        if non_missing_target.empty:
            raise ValueError("target column has no observed values")

        classes: tuple[object, ...] = ()
        if self.task_type != "regression":
            classes = tuple(sorted(non_missing_target.unique().tolist(), key=str))
            if self.task_type == "binary_classification" and len(classes) != 2:
                raise ValueError(
                    "binary_classification requires exactly two observed classes"
                )
            if self.task_type == "multiclass_classification" and len(classes) < 3:
                raise ValueError(
                    "multiclass_classification requires at least three observed classes"
                )
            if (
                self.task_type == "binary_classification"
                and self.positive_label not in classes
            ):
                raise ValueError("positive_label is not present in observed target classes")

        duplicate_entity_rows = 0
        if self.id_columns:
            duplicate_entity_rows = int(
                frame.duplicated(subset=list(self.id_columns), keep=False).sum()
            )

        if self.timestamp_column is not None:
            parsed = pd.to_datetime(
                frame[self.timestamp_column],
                errors="coerce",
                format="mixed",
                utc=True,
            )
            invalid_count = int(parsed.isna().sum())
            if invalid_count:
                raise ValueError(
                    f"timestamp column contains {invalid_count} invalid values"
                )

        return ValidationReport(
            rows=len(frame),
            feature_count=len(self.feature_columns),
            target_missing_count=int(target.isna().sum()),
            duplicate_entity_rows=duplicate_entity_rows,
            target_classes=classes,
        )

    def model_frame(self, frame: pd.DataFrame) -> pd.DataFrame:
        """Return only declared features and target, preserving row order."""

        self.validate_frame(frame)
        return frame[[*self.feature_columns, self.target_column]].copy()

    def split(
        self,
        frame: pd.DataFrame,
        *,
        strategy: SplitStrategy = "random",
        test_size: float = 0.2,
        random_state: int = 42,
    ) -> DataSplit:
        """Create a deterministic random, temporal, or entity-level split."""

        self.validate_frame(frame)
        if not 0.0 < test_size < 1.0:
            raise ValueError("test_size must be between 0 and 1")
        if strategy not in {"random", "temporal", "entity"}:
            raise ValueError(f"unsupported split strategy: {strategy}")

        if strategy == "temporal":
            if self.timestamp_column is None:
                raise ValueError("temporal split requires timestamp_column")
            timestamps = pd.to_datetime(
                frame[self.timestamp_column],
                errors="raise",
                format="mixed",
                utc=True,
            )
            ordered = frame.assign(__split_timestamp=timestamps).sort_values(
                "__split_timestamp",
                kind="stable",
            )
            evaluation_rows = max(1, int(round(len(ordered) * test_size)))
            train = ordered.iloc[:-evaluation_rows].drop(columns="__split_timestamp")
            evaluation = ordered.iloc[-evaluation_rows:].drop(
                columns="__split_timestamp"
            )
            if train.empty:
                raise ValueError("temporal split produced an empty training set")
            return DataSplit(
                train=train.copy(),
                evaluation=evaluation.copy(),
                strategy=strategy,
            )

        if strategy == "entity":
            if not self.id_columns:
                raise ValueError("entity split requires id_columns")
            groups = frame[list(self.id_columns)].astype("string").agg(
                "||".join,
                axis=1,
            )
            if groups.nunique() < 2:
                raise ValueError("entity split requires at least two distinct entities")
            splitter = GroupShuffleSplit(
                n_splits=1,
                test_size=test_size,
                random_state=random_state,
            )
            train_indices, evaluation_indices = next(
                splitter.split(frame, groups=groups)
            )
            return DataSplit(
                train=frame.iloc[train_indices].copy(),
                evaluation=frame.iloc[evaluation_indices].copy(),
                strategy=strategy,
            )

        stratify = None
        if self.task_type != "regression":
            target = frame[self.target_column]
            counts = target.value_counts(dropna=False)
            if not target.isna().any() and len(counts) > 1 and counts.min() >= 2:
                stratify = target

        train, evaluation = train_test_split(
            frame,
            test_size=test_size,
            random_state=random_state,
            shuffle=True,
            stratify=stratify,
        )
        return DataSplit(
            train=train.copy(),
            evaluation=evaluation.copy(),
            strategy=strategy,
        )


def assert_no_entity_overlap(
    split: DataSplit,
    id_columns: tuple[str, ...],
) -> None:
    """Raise when an entity appears in both train and evaluation partitions."""

    if not id_columns:
        raise ValueError("id_columns must not be empty")
    for column in id_columns:
        if column not in split.train.columns or column not in split.evaluation.columns:
            raise ValueError(f"missing id column in split: {column}")

    train_keys = set(
        split.train[list(id_columns)].astype("string").agg("||".join, axis=1)
    )
    evaluation_keys = set(
        split.evaluation[list(id_columns)].astype("string").agg(
            "||".join,
            axis=1,
        )
    )
    overlap = sorted(train_keys & evaluation_keys)
    if overlap:
        raise ValueError(f"entity overlap detected: {overlap[:5]}")
