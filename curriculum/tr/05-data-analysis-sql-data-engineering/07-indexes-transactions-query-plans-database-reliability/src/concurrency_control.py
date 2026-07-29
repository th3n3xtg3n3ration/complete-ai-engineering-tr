"""Retry, lock, and concurrency-control helpers for SQLite workflows."""

from __future__ import annotations

import sqlite3
from collections.abc import Callable
from time import sleep
from typing import TypeVar

T = TypeVar("T")


def retry_locked_operation(
    operation: Callable[[], T],
    *,
    attempts: int = 3,
    initial_delay_seconds: float = 0.01,
    sleep_fn: Callable[[float], None] = sleep,
) -> T:
    """Retry transient SQLite lock errors with exponential backoff."""

    if attempts <= 0:
        raise ValueError("attempts must be positive")
    if initial_delay_seconds < 0:
        raise ValueError("initial_delay_seconds must be non-negative")

    delay = initial_delay_seconds
    for attempt in range(1, attempts + 1):
        try:
            return operation()
        except sqlite3.OperationalError as error:
            if "locked" not in str(error).lower() or attempt == attempts:
                raise
            sleep_fn(delay)
            delay *= 2
    raise AssertionError("unreachable")


def wal_mode_enabled(connection: sqlite3.Connection) -> bool:
    """Return whether the current database uses WAL journal mode."""

    return str(connection.execute("PRAGMA journal_mode").fetchone()[0]).lower() == "wal"


def busy_timeout_milliseconds(connection: sqlite3.Connection) -> int:
    """Read the configured SQLite busy timeout."""

    return int(connection.execute("PRAGMA busy_timeout").fetchone()[0])


def checkpoint_wal(
    connection: sqlite3.Connection,
    *,
    truncate: bool = False,
) -> tuple[int, int, int]:
    """Run a passive or truncating WAL checkpoint and return SQLite counters."""

    mode = "TRUNCATE" if truncate else "PASSIVE"
    row = connection.execute(f"PRAGMA wal_checkpoint({mode})").fetchone()
    return int(row[0]), int(row[1]), int(row[2])


def configure_read_connection(connection: sqlite3.Connection) -> None:
    """Apply read-oriented safety settings without weakening integrity checks."""

    connection.execute("PRAGMA foreign_keys = ON")
    connection.execute("PRAGMA query_only = ON")


def is_query_only(connection: sqlite3.Connection) -> bool:
    """Return whether writes are disabled on the connection."""

    return bool(connection.execute("PRAGMA query_only").fetchone()[0])


if __name__ == "__main__":
    print("Concurrency helpers are intended to be imported by the laboratory.")
