"""Tests for lesson 7 indexes, transactions, and database reliability."""

from __future__ import annotations

import importlib.util
import sqlite3
import sys
from pathlib import Path

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


reliability = _load_module("database_reliability")
indexes = _load_module("index_analysis")
concurrency = _load_module("concurrency_control")


@pytest.fixture
def connection() -> sqlite3.Connection:
    database = reliability.build_demo_database()
    yield database
    database.close()


def test_connection_enables_foreign_keys(connection: sqlite3.Connection) -> None:
    assert connection.execute("PRAGMA foreign_keys").fetchone()[0] == 1


def test_busy_timeout_is_configured(tmp_path: Path) -> None:
    database = reliability.connect(tmp_path / "timeout.db", timeout_seconds=0.25)
    try:
        assert concurrency.busy_timeout_milliseconds(database) == 250
    finally:
        database.close()


def test_file_database_uses_wal(tmp_path: Path) -> None:
    database = reliability.connect(tmp_path / "wal.db")
    try:
        assert concurrency.wal_mode_enabled(database)
    finally:
        database.close()


def test_seed_balances(connection: sqlite3.Connection) -> None:
    assert reliability.account_balance(connection, "a1") == 250_000
    assert reliability.account_balance(connection, "a2") == 125_000


def test_unknown_account_raises(connection: sqlite3.Connection) -> None:
    with pytest.raises(KeyError, match="unknown account"):
        reliability.account_balance(connection, "missing")


def test_transaction_commits(connection: sqlite3.Connection) -> None:
    with reliability.transaction(connection):
        connection.execute(
            "INSERT INTO accounts(account_id, owner_name, balance_kurus) VALUES (?, ?, ?)",
            ("a4", "Deniz", 50_000),
        )
    assert reliability.account_balance(connection, "a4") == 50_000


def test_transaction_rolls_back(connection: sqlite3.Connection) -> None:
    with pytest.raises(RuntimeError, match="boom"):
        with reliability.transaction(connection):
            connection.execute(
                "INSERT INTO accounts(account_id, owner_name, balance_kurus) VALUES (?, ?, ?)",
                ("a4", "Deniz", 50_000),
            )
            raise RuntimeError("boom")
    with pytest.raises(KeyError):
        reliability.account_balance(connection, "a4")


def test_invalid_transaction_mode_rejected(connection: sqlite3.Connection) -> None:
    with pytest.raises(ValueError, match="unsupported"):
        with reliability.transaction(connection, mode="FAST"):
            pass


def test_savepoint_rolls_back_inner_work_only(connection: sqlite3.Connection) -> None:
    with reliability.transaction(connection):
        connection.execute(
            "INSERT INTO accounts(account_id, owner_name, balance_kurus) "
            "VALUES ('a4', 'Deniz', 1000)"
        )
        with pytest.raises(RuntimeError):
            with reliability.savepoint(connection, "inner_work"):
                connection.execute(
                    "INSERT INTO accounts(account_id, owner_name, balance_kurus) "
                    "VALUES ('a5', 'Ece', 1000)"
                )
                raise RuntimeError("rollback savepoint")
    assert reliability.account_balance(connection, "a4") == 1000
    with pytest.raises(KeyError):
        reliability.account_balance(connection, "a5")


def test_unsafe_savepoint_name_rejected(connection: sqlite3.Connection) -> None:
    with pytest.raises(ValueError, match="safe SQL identifier"):
        with reliability.savepoint(connection, "bad-name"):
            pass


def test_transfer_is_atomic(connection: sqlite3.Connection) -> None:
    result = reliability.transfer_funds(
        connection,
        transfer_id="t1",
        source_account_id="a1",
        target_account_id="a2",
        amount_kurus=25_000,
        idempotency_key="request-1",
    )
    assert result == "t1"
    assert reliability.account_balance(connection, "a1") == 225_000
    assert reliability.account_balance(connection, "a2") == 150_000


def test_transfer_is_idempotent(connection: sqlite3.Connection) -> None:
    arguments = {
        "transfer_id": "t1",
        "source_account_id": "a1",
        "target_account_id": "a2",
        "amount_kurus": 25_000,
        "idempotency_key": "request-1",
    }
    assert reliability.transfer_funds(connection, **arguments) == "t1"
    assert reliability.transfer_funds(connection, **arguments) == "t1"
    assert reliability.account_balance(connection, "a1") == 225_000
    assert connection.execute("SELECT COUNT(*) FROM transfers").fetchone()[0] == 1


def test_insufficient_funds_rolls_back(connection: sqlite3.Connection) -> None:
    with pytest.raises(ValueError, match="insufficient"):
        reliability.transfer_funds(
            connection,
            transfer_id="t1",
            source_account_id="a3",
            target_account_id="a2",
            amount_kurus=100_000,
            idempotency_key="request-1",
        )
    assert reliability.account_balance(connection, "a3") == 75_000
    assert reliability.account_balance(connection, "a2") == 125_000
    assert connection.execute("SELECT COUNT(*) FROM transfers").fetchone()[0] == 0


def test_same_account_transfer_rejected(connection: sqlite3.Connection) -> None:
    with pytest.raises(ValueError, match="must differ"):
        reliability.transfer_funds(
            connection,
            transfer_id="t1",
            source_account_id="a1",
            target_account_id="a1",
            amount_kurus=100,
            idempotency_key="request-1",
        )


def test_optimistic_update_increments_version(connection: sqlite3.Connection) -> None:
    assert reliability.optimistic_update_balance(
        connection,
        account_id="a1",
        expected_version=0,
        new_balance_kurus=249_000,
    ) == 1


def test_optimistic_update_detects_conflict(connection: sqlite3.Connection) -> None:
    reliability.optimistic_update_balance(
        connection,
        account_id="a1",
        expected_version=0,
        new_balance_kurus=249_000,
    )
    with pytest.raises(RuntimeError, match="conflict"):
        reliability.optimistic_update_balance(
            connection,
            account_id="a1",
            expected_version=0,
            new_balance_kurus=248_000,
        )


def test_integrity_report_is_clean(connection: sqlite3.Connection) -> None:
    report = reliability.integrity_report(connection)
    assert report["integrity_ok"] is True
    assert report["foreign_key_violations"] == []


def test_backup_round_trip(connection: sqlite3.Connection, tmp_path: Path) -> None:
    destination = reliability.backup_database(connection, tmp_path / "backup.db")
    backup = reliability.connect(destination, enable_wal=False)
    try:
        assert reliability.account_balance(backup, "a1") == 250_000
    finally:
        backup.close()


def test_create_and_list_indexes(connection: sqlite3.Connection) -> None:
    indexes.create_recommended_indexes(connection)
    names = {item.name for item in indexes.list_indexes(connection, "transfers")}
    assert "idx_transfers_source_created" in names
    assert "idx_transfers_target_created" in names


def test_list_indexes_rejects_untrusted_table(connection: sqlite3.Connection) -> None:
    with pytest.raises(ValueError, match="unsupported"):
        indexes.list_indexes(connection, "transfers; DROP TABLE accounts")


def test_index_prefix_rules() -> None:
    info = indexes.IndexInfo(
        name="idx_example",
        unique=False,
        columns=("customer_id", "created_at"),
        partial=False,
    )
    assert indexes.index_supports_prefix(info, ["customer_id"])
    assert indexes.index_supports_prefix(info, ["customer_id", "created_at"])
    assert not indexes.index_supports_prefix(info, ["created_at"])


def test_query_plan_uses_named_index(connection: sqlite3.Connection) -> None:
    indexes.create_recommended_indexes(connection)
    plan = indexes.explain_query_plan(
        connection,
        "SELECT * FROM transfers WHERE source_account_id = ? ORDER BY created_at DESC",
        ("a1",),
    )
    assert indexes.plan_uses_index(plan, "idx_transfers_source_created")


def test_full_scan_detection(connection: sqlite3.Connection) -> None:
    plan = indexes.explain_query_plan(
        connection,
        "SELECT * FROM accounts WHERE balance_kurus > ?",
        (1000,),
    )
    assert indexes.full_table_scan_detected(plan, "accounts")


def test_benchmark_rejects_non_positive_repetitions(connection: sqlite3.Connection) -> None:
    with pytest.raises(ValueError, match="positive"):
        indexes.benchmark_query(connection, "SELECT 1", repetitions=0)


def test_retry_locked_operation_retries_then_succeeds() -> None:
    attempts = 0
    delays: list[float] = []

    def operation() -> str:
        nonlocal attempts
        attempts += 1
        if attempts < 3:
            raise sqlite3.OperationalError("database is locked")
        return "ok"

    result = concurrency.retry_locked_operation(
        operation,
        attempts=3,
        initial_delay_seconds=0.1,
        sleep_fn=delays.append,
    )
    assert result == "ok"
    assert delays == pytest.approx([0.1, 0.2])


def test_retry_locked_operation_does_not_retry_other_errors() -> None:
    calls = 0

    def operation() -> None:
        nonlocal calls
        calls += 1
        raise sqlite3.OperationalError("no such table")

    with pytest.raises(sqlite3.OperationalError, match="no such table"):
        concurrency.retry_locked_operation(operation, attempts=5, sleep_fn=lambda _: None)
    assert calls == 1


def test_query_only_connection_rejects_writes(connection: sqlite3.Connection) -> None:
    concurrency.configure_read_connection(connection)
    assert concurrency.is_query_only(connection)
    with pytest.raises(sqlite3.OperationalError, match="readonly"):
        connection.execute("DELETE FROM accounts")


def test_wal_checkpoint_returns_three_counters(tmp_path: Path) -> None:
    database = reliability.connect(tmp_path / "checkpoint.db")
    reliability.create_schema(database)
    try:
        result = concurrency.checkpoint_wal(database)
        assert len(result) == 3
        assert all(isinstance(value, int) for value in result)
    finally:
        database.close()
