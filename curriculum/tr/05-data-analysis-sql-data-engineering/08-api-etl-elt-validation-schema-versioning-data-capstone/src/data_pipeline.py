"""End-to-end ETL/ELT capstone with validation, lineage, and versioned outputs."""

from __future__ import annotations

import csv
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
import json
from pathlib import Path
import sqlite3
from typing import Any

from api_client import canonical_json_bytes, sha256_hex, write_raw_snapshot
from data_contracts import (
    DataContract,
    FieldSpec,
    ValidationIssue,
    compatibility_issues,
    issues_as_json,
    validate_records,
)

CUSTOMER_CONTRACT = DataContract(
    name="customers",
    version="1.0.0",
    primary_key=("customer_id",),
    fields=(
        FieldSpec("customer_id", "string", pattern=r"c\d+"),
        FieldSpec("customer_name", "string", pattern=r".+"),
        FieldSpec("region", "string", allowed_values=("north", "south", "east", "west")),
        FieldSpec("updated_at", "datetime"),
    ),
)

ORDER_CONTRACT = DataContract(
    name="orders",
    version="1.0.0",
    primary_key=("order_id",),
    fields=(
        FieldSpec("order_id", "string", pattern=r"o\d+"),
        FieldSpec("customer_id", "string", pattern=r"c\d+"),
        FieldSpec("order_at", "datetime"),
        FieldSpec("status", "string", allowed_values=("paid", "cancelled", "refunded")),
        FieldSpec("amount", "number", minimum=0),
        FieldSpec("updated_at", "datetime"),
    ),
)

SCHEMA_SQL = """
PRAGMA foreign_keys = ON;
CREATE TABLE IF NOT EXISTS pipeline_runs (
    dataset_version TEXT PRIMARY KEY,
    run_at TEXT NOT NULL,
    pipeline_version TEXT NOT NULL,
    input_checksum TEXT NOT NULL,
    contract_fingerprint TEXT NOT NULL,
    status TEXT NOT NULL,
    manifest_path TEXT
);
CREATE TABLE IF NOT EXISTS customers (
    customer_id TEXT PRIMARY KEY,
    customer_name TEXT NOT NULL,
    region TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    dataset_version TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS orders (
    order_id TEXT PRIMARY KEY,
    customer_id TEXT NOT NULL REFERENCES customers(customer_id),
    order_at TEXT NOT NULL,
    status TEXT NOT NULL,
    amount REAL NOT NULL CHECK (amount >= 0),
    updated_at TEXT NOT NULL,
    dataset_version TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_orders_customer_status_date
ON orders(customer_id, status, order_at);
CREATE TABLE IF NOT EXISTS customer_features (
    customer_id TEXT PRIMARY KEY REFERENCES customers(customer_id),
    paid_order_count INTEGER NOT NULL,
    total_paid_amount REAL NOT NULL,
    average_paid_order_amount REAL NOT NULL,
    latest_paid_order_at TEXT,
    dataset_version TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS rejected_records (
    dataset_version TEXT NOT NULL,
    entity TEXT NOT NULL,
    record_index INTEGER NOT NULL,
    raw_json TEXT NOT NULL,
    issues_json TEXT NOT NULL,
    PRIMARY KEY (dataset_version, entity, record_index)
);
"""


@dataclass(frozen=True)
class PipelineConfig:
    workspace: Path
    pipeline_version: str = "1.0.0"
    warehouse_name: str = "warehouse.db"


@dataclass(frozen=True)
class PipelineResult:
    dataset_version: str
    manifest_path: Path
    warehouse_path: Path
    valid_customers: int
    valid_orders: int
    rejected_records: int
    reused: bool


def _utc(value: datetime) -> str:
    if value.tzinfo is None:
        raise ValueError("run_at must be timezone-aware")
    return value.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


def _contract_fingerprint() -> str:
    value = {
        "customers": CUSTOMER_CONTRACT.fingerprint(),
        "orders": ORDER_CONTRACT.fingerprint(),
    }
    return sha256_hex(canonical_json_bytes(value))


def _version(
    customers: list[dict[str, Any]],
    orders: list[dict[str, Any]],
    code: str,
) -> tuple[str, str]:
    inputs = {
        "customers": sha256_hex(canonical_json_bytes(customers)),
        "orders": sha256_hex(canonical_json_bytes(orders)),
    }
    input_checksum = sha256_hex(canonical_json_bytes(inputs))
    payload = {
        "input_checksum": input_checksum,
        "contract_fingerprint": _contract_fingerprint(),
        "pipeline_version": code,
    }
    return sha256_hex(canonical_json_bytes(payload))[:20], input_checksum


def _connect(path: Path) -> sqlite3.Connection:
    path.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(path)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    connection.executescript(SCHEMA_SQL)
    connection.commit()
    return connection


def _atomic_bytes(path: Path, content: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_bytes(content)
    temporary.replace(path)


def _write_jsonl(path: Path, records: list[dict[str, Any]]) -> None:
    content = b"\n".join(canonical_json_bytes(record) for record in records)
    _atomic_bytes(path, content + (b"\n" if records else b""))


def _write_csv(path: Path, records: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(".tmp")
    with temporary.open("w", encoding="utf-8", newline="") as handle:
        fields = list(records[0]) if records else []
        writer = csv.DictWriter(handle, fieldnames=fields)
        if fields:
            writer.writeheader()
            writer.writerows(records)
    temporary.replace(path)


def _quarantine_validation(
    connection: sqlite3.Connection,
    version: str,
    entity: str,
    source: list[dict[str, Any]],
    result: Any,
) -> int:
    count = 0
    for index in result.rejected_indices:
        record_issues = [issue for issue in result.issues if issue.record_index == index]
        connection.execute(
            """INSERT OR REPLACE INTO rejected_records
               VALUES (?, ?, ?, ?, ?)""",
            (
                version,
                entity,
                index,
                canonical_json_bytes(source[index]).decode(),
                issues_as_json(record_issues),
            ),
        )
        count += 1
    return count


def _upsert_customers(
    connection: sqlite3.Connection,
    records: list[dict[str, Any]],
    version: str,
) -> None:
    connection.executemany(
        """
        INSERT INTO customers VALUES (
            :customer_id, :customer_name, :region, :updated_at, :dataset_version
        )
        ON CONFLICT(customer_id) DO UPDATE SET
            customer_name=excluded.customer_name,
            region=excluded.region,
            updated_at=excluded.updated_at,
            dataset_version=excluded.dataset_version
        WHERE excluded.updated_at >= customers.updated_at
        """,
        [record | {"dataset_version": version} for record in records],
    )


def _upsert_orders(
    connection: sqlite3.Connection,
    records: list[dict[str, Any]],
    version: str,
) -> None:
    connection.executemany(
        """
        INSERT INTO orders VALUES (
            :order_id, :customer_id, :order_at, :status,
            :amount, :updated_at, :dataset_version
        )
        ON CONFLICT(order_id) DO UPDATE SET
            customer_id=excluded.customer_id,
            order_at=excluded.order_at,
            status=excluded.status,
            amount=excluded.amount,
            updated_at=excluded.updated_at,
            dataset_version=excluded.dataset_version
        WHERE excluded.updated_at >= orders.updated_at
        """,
        [record | {"dataset_version": version} for record in records],
    )


def _features(connection: sqlite3.Connection, version: str) -> list[dict[str, Any]]:
    connection.execute("DELETE FROM customer_features")
    connection.execute(
        """
        INSERT INTO customer_features
        SELECT c.customer_id,
               COUNT(o.order_id),
               COALESCE(SUM(o.amount), 0.0),
               COALESCE(AVG(o.amount), 0.0),
               MAX(o.order_at),
               ?
        FROM customers AS c
        LEFT JOIN orders AS o
          ON o.customer_id=c.customer_id AND o.status='paid'
        GROUP BY c.customer_id
        """,
        (version,),
    )
    rows = connection.execute(
        "SELECT * FROM customer_features ORDER BY customer_id"
    ).fetchall()
    return [dict(row) for row in rows]


def _artifact(path: Path, root: Path) -> dict[str, Any]:
    return {
        "path": str(path.relative_to(root)),
        "sha256": sha256_hex(path.read_bytes()),
        "size_bytes": path.stat().st_size,
    }


def run_pipeline(
    *,
    customers: list[dict[str, Any]],
    orders: list[dict[str, Any]],
    config: PipelineConfig,
    run_at: datetime,
) -> PipelineResult:
    run_at_text = _utc(run_at)
    version, input_checksum = _version(customers, orders, config.pipeline_version)
    manifest_path = config.workspace / "manifests" / f"{version}.json"
    warehouse_path = config.workspace / config.warehouse_name
    if manifest_path.exists():
        counts = json.loads(manifest_path.read_text(encoding="utf-8"))["counts"]
        return PipelineResult(
            version,
            manifest_path,
            warehouse_path,
            counts["valid_customers"],
            counts["valid_orders"],
            counts["rejected_records"],
            True,
        )

    bronze = config.workspace / "bronze"
    customer_snapshot = write_raw_snapshot(
        bronze,
        source="customers",
        payload=customers,
        fetched_at=run_at,
        schema_version=CUSTOMER_CONTRACT.version,
    )
    order_snapshot = write_raw_snapshot(
        bronze,
        source="orders",
        payload=orders,
        fetched_at=run_at,
        schema_version=ORDER_CONTRACT.version,
    )
    customer_result = validate_records(customers, CUSTOMER_CONTRACT)
    order_result = validate_records(orders, ORDER_CONTRACT)
    valid_customers = list(customer_result.valid_records)
    candidate_orders = list(order_result.valid_records)
    silver_customers = config.workspace / "silver" / f"customers_{version}.jsonl"
    silver_orders = config.workspace / "silver" / f"orders_{version}.jsonl"
    gold = config.workspace / "gold" / f"customer_features_{version}.csv"

    connection = _connect(warehouse_path)
    rejected = 0
    try:
        connection.execute(
            """
            INSERT INTO pipeline_runs VALUES (?, ?, ?, ?, ?, 'running', NULL)
            ON CONFLICT(dataset_version) DO UPDATE SET status='running'
            """,
            (
                version,
                run_at_text,
                config.pipeline_version,
                input_checksum,
                _contract_fingerprint(),
            ),
        )
        connection.commit()
        connection.execute("BEGIN")
        connection.execute("DELETE FROM rejected_records WHERE dataset_version=?", (version,))
        rejected += _quarantine_validation(
            connection, version, "customers", customers, customer_result
        )
        rejected += _quarantine_validation(connection, version, "orders", orders, order_result)
        _upsert_customers(connection, valid_customers, version)

        known = {row[0] for row in connection.execute("SELECT customer_id FROM customers")}
        valid_orders: list[dict[str, Any]] = []
        for index, record in enumerate(candidate_orders):
            if record["customer_id"] in known:
                valid_orders.append(record)
                continue
            issue = ValidationIssue(
                index,
                "customer_id",
                "foreign_key",
                "customer_id does not exist in curated customers",
            )
            connection.execute(
                "INSERT OR REPLACE INTO rejected_records VALUES (?, 'orders', ?, ?, ?)",
                (
                    version,
                    1_000_000 + index,
                    canonical_json_bytes(record).decode(),
                    issues_as_json([issue]),
                ),
            )
            rejected += 1

        _upsert_orders(connection, valid_orders, version)
        feature_rows = _features(connection, version)
        connection.commit()

        _write_jsonl(silver_customers, valid_customers)
        _write_jsonl(silver_orders, valid_orders)
        _write_csv(gold, feature_rows)
        manifest = {
            "dataset_version": version,
            "run_at": run_at_text,
            "pipeline_version": config.pipeline_version,
            "input_checksum": input_checksum,
            "source_snapshot_checksums": {
                "customers": customer_snapshot.checksum,
                "orders": order_snapshot.checksum,
            },
            "contract_fingerprints": {
                "customers": CUSTOMER_CONTRACT.fingerprint(),
                "orders": ORDER_CONTRACT.fingerprint(),
            },
            "counts": {
                "input_customers": len(customers),
                "input_orders": len(orders),
                "valid_customers": len(valid_customers),
                "valid_orders": len(valid_orders),
                "rejected_records": rejected,
                "customer_features": len(feature_rows),
            },
            "lineage": {
                "bronze": [
                    str(customer_snapshot.path.relative_to(config.workspace)),
                    str(order_snapshot.path.relative_to(config.workspace)),
                ],
                "silver": [
                    str(silver_customers.relative_to(config.workspace)),
                    str(silver_orders.relative_to(config.workspace)),
                ],
                "gold": [str(gold.relative_to(config.workspace))],
            },
            "artifacts": {
                "customers_silver": _artifact(silver_customers, config.workspace),
                "orders_silver": _artifact(silver_orders, config.workspace),
                "customer_features": _artifact(gold, config.workspace),
            },
        }
        _atomic_bytes(
            manifest_path,
            json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True).encode(),
        )
        connection.execute(
            "UPDATE pipeline_runs SET status='succeeded', manifest_path=? WHERE dataset_version=?",
            (str(manifest_path), version),
        )
        connection.commit()
    except Exception:
        connection.rollback()
        connection.execute(
            "UPDATE pipeline_runs SET status='failed' WHERE dataset_version=?", (version,)
        )
        connection.commit()
        raise
    finally:
        connection.close()

    return PipelineResult(
        version,
        manifest_path,
        warehouse_path,
        len(valid_customers),
        len(valid_orders),
        rejected,
        False,
    )


def verify_manifest(workspace: str | Path, manifest_path: str | Path) -> list[str]:
    root = Path(workspace)
    manifest = json.loads(Path(manifest_path).read_text(encoding="utf-8"))
    errors: list[str] = []
    for name, metadata in manifest["artifacts"].items():
        path = root / metadata["path"]
        if not path.exists():
            errors.append(f"missing artifact: {name}")
        elif sha256_hex(path.read_bytes()) != metadata["sha256"]:
            errors.append(f"checksum mismatch: {name}")
    return errors


def contract_upgrade_report(old: DataContract, new: DataContract) -> dict[str, Any]:
    issues = compatibility_issues(old, new)
    return {
        "old_version": old.version,
        "new_version": new.version,
        "compatible": not issues,
        "issues": issues,
        "new_fingerprint": new.fingerprint(),
    }


if __name__ == "__main__":
    demo_customers = [
        {
            "customer_id": "c1",
            "customer_name": "Ada",
            "region": "north",
            "updated_at": "2026-07-29T10:00:00Z",
        }
    ]
    demo_orders = [
        {
            "order_id": "o1",
            "customer_id": "c1",
            "order_at": "2026-07-29T10:05:00Z",
            "status": "paid",
            "amount": 125.0,
            "updated_at": "2026-07-29T10:06:00Z",
        }
    ]
    result = run_pipeline(
        customers=demo_customers,
        orders=demo_orders,
        config=PipelineConfig(Path("data-capstone-output")),
        run_at=datetime.now(timezone.utc),
    )
    print(asdict(result))
