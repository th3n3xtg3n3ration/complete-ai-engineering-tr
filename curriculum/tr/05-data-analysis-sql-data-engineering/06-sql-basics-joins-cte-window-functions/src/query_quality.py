"""Quality checks and query-plan diagnostics for analytical SQL."""

from __future__ import annotations

import re
import sqlite3
from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class QueryPlanStep:
    """One normalized SQLite query-plan row."""

    step_id: int
    parent_id: int
    detail: str


_WRITE_KEYWORDS = re.compile(
    r"\b(INSERT|UPDATE|DELETE|DROP|ALTER|CREATE|REPLACE|VACUUM|ATTACH|DETACH)\b",
    flags=re.IGNORECASE,
)


def validate_read_only_sql(sql: str) -> None:
    """Reject empty or mutating SQL before analytical execution."""

    stripped = sql.strip()
    if not stripped:
        raise ValueError("SQL must not be empty")
    without_comments = re.sub(
        r"--.*?$|/\*.*?\*/",
        " ",
        stripped,
        flags=re.MULTILINE | re.DOTALL,
    )
    if _WRITE_KEYWORDS.search(without_comments):
        raise ValueError("only read-only analytical SQL is allowed")
    first_token = without_comments.lstrip().split(maxsplit=1)[0].upper()
    if first_token not in {"SELECT", "WITH", "EXPLAIN"}:
        raise ValueError("query must start with SELECT, WITH, or EXPLAIN")


def explain_query_plan(
    connection: sqlite3.Connection,
    sql: str,
    parameters: Sequence[Any] | Mapping[str, Any] = (),
) -> list[QueryPlanStep]:
    """Return normalized EXPLAIN QUERY PLAN output."""

    validate_read_only_sql(sql)
    rows = connection.execute(f"EXPLAIN QUERY PLAN {sql}", parameters).fetchall()
    return [
        QueryPlanStep(
            step_id=int(row[0]),
            parent_id=int(row[1]),
            detail=str(row[3]),
        )
        for row in rows
    ]


def assert_expected_columns(
    rows: Sequence[Mapping[str, Any]],
    expected: Iterable[str],
) -> None:
    """Validate the exact output schema for non-empty query results."""

    expected_columns = list(expected)
    if not rows:
        raise ValueError("query result must not be empty")
    actual_columns = list(rows[0].keys())
    if actual_columns != expected_columns:
        raise ValueError(
            f"unexpected columns: expected {expected_columns}, got {actual_columns}"
        )


def assert_unique_key(
    rows: Sequence[Mapping[str, Any]],
    key_columns: Iterable[str],
) -> None:
    """Raise when a query result violates its expected grain."""

    keys = list(key_columns)
    if not keys:
        raise ValueError("key_columns must not be empty")
    seen: set[tuple[Any, ...]] = set()
    for row in rows:
        key = tuple(row[column] for column in keys)
        if key in seen:
            raise ValueError(f"duplicate query grain: {key}")
        seen.add(key)


def assert_non_negative(
    rows: Sequence[Mapping[str, Any]],
    columns: Iterable[str],
) -> None:
    """Validate non-negative analytical measures."""

    selected = list(columns)
    for row_index, row in enumerate(rows):
        for column in selected:
            value = row[column]
            if value is not None and float(value) < 0:
                raise ValueError(
                    f"negative value at row {row_index}, column {column}: {value}"
                )
