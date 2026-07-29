"""SQLite reliability primitives: transactions, savepoints, integrity, and backup."""

from __future__ import annotations

import sqlite3
from collections.abc import Iterator
from contextlib import contextmanager
from pathlib import Path
from typing import Literal

TransactionMode = Literal["DEFERRED", "IMMEDIATE", "EXCLUSIVE"]

SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS accounts (
    account_id TEXT PRIMARY KEY,
    owner_name TEXT NOT NULL,
    balance_kurus INTEGER NOT NULL CHECK (balance_kurus >= 0),
    version INTEGER NOT NULL DEFAULT 0,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS transfers (
    transfer_id TEXT PRIMARY KEY,
    source_account_id TEXT NOT NULL,
    target_account_id TEXT NOT NULL,
    amount_kurus INTEGER NOT NULL CHECK (amount_kurus > 0),
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (source_account_id) REFERENCES accounts(account_id),
    FOREIGN KEY (target_account_id) REFERENCES accounts(account_id),
    CHECK (source_account_id <> target_account_id)
);

CREATE TABLE IF NOT EXISTS idempotency_keys (
    idempotency_key TEXT PRIMARY KEY,
    operation_name TEXT NOT NULL,
    result_reference TEXT NOT NULL,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);
"""

SEED_ACCOUNTS = (
    ("a1", "Ada", 250_000, 0),
    ("a2", "Bora", 125_000, 0),
    ("a3", "Ceren", 75_000, 0),
)


def connect(
    path: str | Path = ":memory:",
    *,
    timeout_seconds: float = 5.0,
    enable_wal: bool = True,
) -> sqlite3.Connection:
    """Create a configured SQLite connection suitable for lesson examples."""

    if timeout_seconds < 0:
        raise ValueError("timeout_seconds must be non-negative")
    connection = sqlite3.connect(str(path), timeout=timeout_seconds)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    connection.execute(f"PRAGMA busy_timeout = {int(timeout_seconds * 1000)}")
    if enable_wal and str(path) != ":memory:":
        connection.execute("PRAGMA journal_mode = WAL")
    return connection


def create_schema(connection: sqlite3.Connection) -> None:
    """Create the reliability lesson schema."""

    connection.executescript(SCHEMA_SQL)
    connection.commit()


def seed_accounts(connection: sqlite3.Connection) -> None:
    """Insert deterministic accounts into an empty schema."""

    connection.executemany(
        "INSERT INTO accounts(account_id, owner_name, balance_kurus, version) VALUES (?, ?, ?, ?)",
        SEED_ACCOUNTS,
    )
    connection.commit()


def build_demo_database(path: str | Path = ":memory:") -> sqlite3.Connection:
    """Create and seed the deterministic lesson database."""

    connection = connect(path)
    create_schema(connection)
    seed_accounts(connection)
    return connection


@contextmanager
def transaction(
    connection: sqlite3.Connection,
    *,
    mode: TransactionMode = "IMMEDIATE",
) -> Iterator[sqlite3.Connection]:
    """Commit a transaction on success and roll it back on failure."""

    if mode not in {"DEFERRED", "IMMEDIATE", "EXCLUSIVE"}:
        raise ValueError(f"unsupported transaction mode: {mode}")
    try:
        connection.execute(f"BEGIN {mode}")
        yield connection
    except Exception:
        connection.rollback()
        raise
    else:
        connection.commit()


@contextmanager
def savepoint(connection: sqlite3.Connection, name: str) -> Iterator[sqlite3.Connection]:
    """Create a nested rollback boundary inside an existing transaction."""

    if not name.replace("_", "").isalnum() or name[0].isdigit():
        raise ValueError("savepoint name must be a safe SQL identifier")
    connection.execute(f"SAVEPOINT {name}")
    try:
        yield connection
    except Exception:
        connection.execute(f"ROLLBACK TO SAVEPOINT {name}")
        connection.execute(f"RELEASE SAVEPOINT {name}")
        raise
    else:
        connection.execute(f"RELEASE SAVEPOINT {name}")


def account_balance(connection: sqlite3.Connection, account_id: str) -> int:
    """Return an account balance in kuruş."""

    row = connection.execute(
        "SELECT balance_kurus FROM accounts WHERE account_id = ?",
        (account_id,),
    ).fetchone()
    if row is None:
        raise KeyError(f"unknown account: {account_id}")
    return int(row[0])


def transfer_funds(
    connection: sqlite3.Connection,
    *,
    transfer_id: str,
    source_account_id: str,
    target_account_id: str,
    amount_kurus: int,
    idempotency_key: str,
) -> str:
    """Transfer money atomically and make retries idempotent."""

    if amount_kurus <= 0:
        raise ValueError("amount_kurus must be positive")
    if source_account_id == target_account_id:
        raise ValueError("source and target accounts must differ")
    if not idempotency_key.strip():
        raise ValueError("idempotency_key must not be empty")

    existing = connection.execute(
        "SELECT result_reference FROM idempotency_keys WHERE idempotency_key = ?",
        (idempotency_key,),
    ).fetchone()
    if existing is not None:
        return str(existing[0])

    with transaction(connection, mode="IMMEDIATE"):
        source = connection.execute(
            "SELECT balance_kurus FROM accounts WHERE account_id = ?",
            (source_account_id,),
        ).fetchone()
        target = connection.execute(
            "SELECT 1 FROM accounts WHERE account_id = ?",
            (target_account_id,),
        ).fetchone()
        if source is None or target is None:
            raise KeyError("source or target account does not exist")
        if int(source[0]) < amount_kurus:
            raise ValueError("insufficient funds")

        connection.execute(
            """
            UPDATE accounts
            SET balance_kurus = balance_kurus - ?,
                version = version + 1,
                updated_at = CURRENT_TIMESTAMP
            WHERE account_id = ?
            """,
            (amount_kurus, source_account_id),
        )
        connection.execute(
            """
            UPDATE accounts
            SET balance_kurus = balance_kurus + ?,
                version = version + 1,
                updated_at = CURRENT_TIMESTAMP
            WHERE account_id = ?
            """,
            (amount_kurus, target_account_id),
        )
        connection.execute(
            """
            INSERT INTO transfers(
                transfer_id, source_account_id, target_account_id, amount_kurus
            ) VALUES (?, ?, ?, ?)
            """,
            (transfer_id, source_account_id, target_account_id, amount_kurus),
        )
        connection.execute(
            """
            INSERT INTO idempotency_keys(idempotency_key, operation_name, result_reference)
            VALUES (?, 'transfer_funds', ?)
            """,
            (idempotency_key, transfer_id),
        )
    return transfer_id


def optimistic_update_balance(
    connection: sqlite3.Connection,
    *,
    account_id: str,
    expected_version: int,
    new_balance_kurus: int,
) -> int:
    """Update one account only when the expected version still matches."""

    if expected_version < 0:
        raise ValueError("expected_version must be non-negative")
    if new_balance_kurus < 0:
        raise ValueError("new_balance_kurus must be non-negative")
    cursor = connection.execute(
        """
        UPDATE accounts
        SET balance_kurus = ?, version = version + 1, updated_at = CURRENT_TIMESTAMP
        WHERE account_id = ? AND version = ?
        """,
        (new_balance_kurus, account_id, expected_version),
    )
    if cursor.rowcount != 1:
        connection.rollback()
        raise RuntimeError("optimistic locking conflict")
    connection.commit()
    row = connection.execute(
        "SELECT version FROM accounts WHERE account_id = ?",
        (account_id,),
    ).fetchone()
    return int(row[0])


def integrity_report(connection: sqlite3.Connection) -> dict[str, object]:
    """Return SQLite integrity and foreign-key diagnostics."""

    integrity_rows = [str(row[0]) for row in connection.execute("PRAGMA integrity_check")]
    foreign_key_rows = [tuple(row) for row in connection.execute("PRAGMA foreign_key_check")]
    return {
        "integrity_ok": integrity_rows == ["ok"],
        "integrity_messages": integrity_rows,
        "foreign_key_violations": foreign_key_rows,
    }


def backup_database(
    source: sqlite3.Connection,
    destination_path: str | Path,
) -> Path:
    """Create a consistent SQLite backup using the backup API."""

    destination = Path(destination_path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    target = connect(destination, enable_wal=False)
    try:
        source.backup(target)
    finally:
        target.close()
    return destination


if __name__ == "__main__":
    database = build_demo_database()
    print("Ada balance (TL):", account_balance(database, "a1") / 100)
