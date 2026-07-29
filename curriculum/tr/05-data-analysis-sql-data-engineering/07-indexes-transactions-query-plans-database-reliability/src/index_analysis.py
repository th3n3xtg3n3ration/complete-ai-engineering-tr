"""Index creation, inspection, and EXPLAIN QUERY PLAN helpers."""

from __future__ import annotations

import sqlite3
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class QueryPlanStep:
    """One normalized SQLite query-plan row."""

    step_id: int
    parent_id: int
    detail: str


@dataclass(frozen=True)
class IndexInfo:
    """Compact index metadata."""

    name: str
    unique: bool
    columns: tuple[str, ...]
    partial: bool


INDEX_SQL = """
CREATE INDEX IF NOT EXISTS idx_transfers_source_created
ON transfers(source_account_id, created_at DESC);

CREATE INDEX IF NOT EXISTS idx_transfers_target_created
ON transfers(target_account_id, created_at DESC);

CREATE INDEX IF NOT EXISTS idx_accounts_owner
ON accounts(owner_name);
"""


def create_recommended_indexes(connection: sqlite3.Connection) -> None:
    """Create the lesson's workload-driven indexes."""

    connection.executescript(INDEX_SQL)
    connection.commit()


def explain_query_plan(
    connection: sqlite3.Connection,
    sql: str,
    parameters: Sequence[Any] | Mapping[str, Any] = (),
) -> list[QueryPlanStep]:
    """Return normalized EXPLAIN QUERY PLAN output."""

    if not sql.strip():
        raise ValueError("sql must not be empty")
    rows = connection.execute(f"EXPLAIN QUERY PLAN {sql}", parameters).fetchall()
    return [
        QueryPlanStep(step_id=int(row[0]), parent_id=int(row[1]), detail=str(row[3]))
        for row in rows
    ]


def plan_uses_index(plan: Sequence[QueryPlanStep], index_name: str | None = None) -> bool:
    """Return whether a query plan uses any index or a named index."""

    details = [step.detail.upper() for step in plan]
    if index_name is None:
        return any(
            "USING INDEX" in detail or "USING COVERING INDEX" in detail
            for detail in details
        )
    expected = index_name.upper()
    return any(expected in detail for detail in details)


def full_table_scan_detected(plan: Sequence[QueryPlanStep], table_name: str) -> bool:
    """Detect a full scan of a named table in a SQLite plan."""

    table = table_name.upper()
    for step in plan:
        detail = step.detail.upper()
        if f"SCAN {table}" in detail and "USING" not in detail:
            return True
    return False


def list_indexes(connection: sqlite3.Connection, table_name: str) -> list[IndexInfo]:
    """Return explicit and automatic indexes for one trusted table."""

    allowed = {"accounts", "transfers", "idempotency_keys"}
    if table_name not in allowed:
        raise ValueError(f"unsupported table: {table_name}")
    result: list[IndexInfo] = []
    for row in connection.execute(f"PRAGMA index_list({table_name})"):
        index_name = str(row[1])
        columns = tuple(
            str(column_row[2])
            for column_row in connection.execute(f"PRAGMA index_info('{index_name}')")
        )
        result.append(
            IndexInfo(
                name=index_name,
                unique=bool(row[2]),
                columns=columns,
                partial=bool(row[4]),
            )
        )
    return sorted(result, key=lambda item: item.name)


def index_supports_prefix(index: IndexInfo, filter_columns: Sequence[str]) -> bool:
    """Check whether filter columns match the left-most index prefix."""

    requested = tuple(filter_columns)
    if not requested:
        raise ValueError("filter_columns must not be empty")
    return index.columns[: len(requested)] == requested


def benchmark_query(
    connection: sqlite3.Connection,
    sql: str,
    parameters: Sequence[Any] | Mapping[str, Any] = (),
    *,
    repetitions: int = 50,
) -> float:
    """Return average query duration in seconds for a small teaching benchmark."""

    if repetitions <= 0:
        raise ValueError("repetitions must be positive")
    from time import perf_counter

    started = perf_counter()
    for _ in range(repetitions):
        connection.execute(sql, parameters).fetchall()
    return (perf_counter() - started) / repetitions


if __name__ == "__main__":
    from database_reliability import build_demo_database

    database = build_demo_database()
    create_recommended_indexes(database)
    for item in list_indexes(database, "transfers"):
        print(item)
