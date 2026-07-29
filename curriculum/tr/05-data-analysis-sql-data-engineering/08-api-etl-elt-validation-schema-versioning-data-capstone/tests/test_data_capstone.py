"""Tests for lesson 8 API extraction, contracts, ETL/ELT, and versioning."""

from __future__ import annotations

import importlib.util
import json
from datetime import datetime, timezone
from pathlib import Path
import sqlite3
import sys

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


api = _load_module("api_client")
contracts = _load_module("data_contracts")
pipeline = _load_module("data_pipeline")

RUN_AT = datetime(2026, 7, 29, 12, 0, tzinfo=timezone.utc)


def _customers() -> list[dict[str, object]]:
    return [
        {
            "customer_id": "c1",
            "customer_name": "Ada",
            "region": "north",
            "updated_at": "2026-07-29T10:00:00Z",
        },
        {
            "customer_id": "c2",
            "customer_name": "Bora",
            "region": "south",
            "updated_at": "2026-07-29T10:00:00Z",
        },
    ]


def _orders() -> list[dict[str, object]]:
    return [
        {
            "order_id": "o1",
            "customer_id": "c1",
            "order_at": "2026-07-29T10:05:00Z",
            "status": "paid",
            "amount": 100.0,
            "updated_at": "2026-07-29T10:06:00Z",
        },
        {
            "order_id": "o2",
            "customer_id": "c1",
            "order_at": "2026-07-29T11:05:00Z",
            "status": "cancelled",
            "amount": 50.0,
            "updated_at": "2026-07-29T11:06:00Z",
        },
    ]


def test_canonical_json_is_order_independent() -> None:
    assert api.canonical_json_bytes({"b": 2, "a": 1}) == api.canonical_json_bytes(
        {"a": 1, "b": 2}
    )


def test_retry_policy_validates_arguments() -> None:
    with pytest.raises(ValueError, match="positive"):
        api.RetryPolicy(max_attempts=0)


def test_api_client_returns_decoded_json() -> None:
    def transport(url, headers, timeout):
        assert url == "https://example.test/items"
        assert headers["Accept"] == "application/json"
        assert timeout == 3.0
        return api.HttpResponse(200, {}, b'{"items": [{"id": 1}]}')

    client = api.ApiClient(transport, timeout_seconds=3.0)
    assert client.get_json("https://example.test/items") == {"items": [{"id": 1}]}


def test_api_client_retries_transient_status() -> None:
    statuses = iter([503, 200])
    delays: list[float] = []

    def transport(url, headers, timeout):
        status = next(statuses)
        return api.HttpResponse(status, {}, b'{"ok": true}')

    client = api.ApiClient(
        transport,
        retry_policy=api.RetryPolicy(max_attempts=2, base_delay_seconds=0.25),
        sleep_fn=delays.append,
    )
    assert client.get_json("https://example.test") == {"ok": True}
    assert delays == [0.25]


def test_api_client_uses_retry_after() -> None:
    statuses = iter([429, 200])
    delays: list[float] = []

    def transport(url, headers, timeout):
        status = next(statuses)
        headers = {"Retry-After": "2"} if status == 429 else {}
        return api.HttpResponse(status, headers, b'{"ok": true}')

    client = api.ApiClient(transport, sleep_fn=delays.append)
    client.get_json("https://example.test")
    assert delays == [2.0]


def test_api_client_rejects_invalid_json() -> None:
    client = api.ApiClient(lambda *_: api.HttpResponse(200, {}, b"not-json"))
    with pytest.raises(api.ApiError, match="valid UTF-8 JSON"):
        client.get_json("https://example.test")


def test_pagination_collects_pages() -> None:
    def transport(url, headers, timeout):
        if "cursor=next" in url:
            return api.HttpResponse(200, {}, b'{"items": [{"id": 2}], "next_cursor": null}')
        return api.HttpResponse(200, {}, b'{"items": [{"id": 1}], "next_cursor": "next"}')

    client = api.ApiClient(transport)
    assert client.paginate("https://example.test/items") == [{"id": 1}, {"id": 2}]


def test_pagination_detects_cursor_loop() -> None:
    client = api.ApiClient(
        lambda *_: api.HttpResponse(200, {}, b'{"items": [], "next_cursor": "same"}')
    )
    with pytest.raises(api.ApiError, match="cursor loop"):
        client.paginate("https://example.test/items")


def test_raw_snapshot_is_content_addressed_and_idempotent(tmp_path: Path) -> None:
    first = api.write_raw_snapshot(
        tmp_path,
        source="orders",
        payload=[{"id": 1}],
        fetched_at=RUN_AT,
        schema_version="1.0.0",
    )
    second = api.write_raw_snapshot(
        tmp_path,
        source="orders",
        payload=[{"id": 1}],
        fetched_at=RUN_AT,
        schema_version="1.0.0",
    )
    assert first.path == second.path
    assert first.checksum == second.checksum
    assert first.record_count == 1


def test_raw_snapshot_requires_timezone(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="timezone-aware"):
        api.write_raw_snapshot(
            tmp_path,
            source="orders",
            payload=[],
            fetched_at=datetime(2026, 1, 1),
            schema_version="1.0.0",
        )


def test_contract_fingerprint_is_deterministic() -> None:
    assert pipeline.CUSTOMER_CONTRACT.fingerprint() == pipeline.CUSTOMER_CONTRACT.fingerprint()


def test_contract_coerces_number_and_datetime() -> None:
    result = contracts.validate_records(
        [
            {
                "order_id": "o1",
                "customer_id": "c1",
                "order_at": "2026-07-29T13:00:00+03:00",
                "status": "paid",
                "amount": "12.5",
                "updated_at": "2026-07-29T13:01:00+03:00",
            }
        ],
        pipeline.ORDER_CONTRACT,
    )
    assert result.valid_records[0]["amount"] == pytest.approx(12.5)
    assert result.valid_records[0]["order_at"] == "2026-07-29T10:00:00Z"


def test_contract_rejects_unknown_field() -> None:
    record = _customers()[0] | {"unexpected": 1}
    result = contracts.validate_records([record], pipeline.CUSTOMER_CONTRACT)
    assert result.rejected_indices == (0,)
    assert result.issues[0].code == "unknown_fields"


def test_contract_rejects_missing_required_field() -> None:
    record = _customers()[0].copy()
    del record["region"]
    result = contracts.validate_records([record], pipeline.CUSTOMER_CONTRACT)
    assert result.rejected_indices == (0,)
    assert any(issue.code == "required" for issue in result.issues)


def test_contract_rejects_duplicate_primary_key() -> None:
    result = contracts.validate_records(
        _customers() + [_customers()[0]],
        pipeline.CUSTOMER_CONTRACT,
    )
    assert result.rejected_indices == (2,)
    assert any(issue.code == "duplicate_key" for issue in result.issues)


def test_contract_rejects_invalid_enum() -> None:
    record = _orders()[0] | {"status": "pending"}
    result = contracts.validate_records([record], pipeline.ORDER_CONTRACT)
    assert result.rejected_indices == (0,)


def test_contract_rejects_negative_amount() -> None:
    record = _orders()[0] | {"amount": -1}
    result = contracts.validate_records([record], pipeline.ORDER_CONTRACT)
    assert result.rejected_indices == (0,)


def test_optional_addition_is_backward_compatible() -> None:
    old = pipeline.CUSTOMER_CONTRACT
    new = contracts.DataContract(
        name=old.name,
        version="1.1.0",
        fields=old.fields
        + (contracts.FieldSpec("email", "string", required=False, nullable=True),),
        primary_key=old.primary_key,
    )
    assert contracts.compatibility_issues(old, new) == []


def test_required_addition_is_breaking() -> None:
    old = pipeline.CUSTOMER_CONTRACT
    new = contracts.DataContract(
        name=old.name,
        version="2.0.0",
        fields=old.fields + (contracts.FieldSpec("email", "string"),),
        primary_key=old.primary_key,
    )
    assert "new required field added: email" in contracts.compatibility_issues(old, new)


def test_pipeline_publishes_layers_and_manifest(tmp_path: Path) -> None:
    result = pipeline.run_pipeline(
        customers=_customers(),
        orders=_orders(),
        config=pipeline.PipelineConfig(tmp_path),
        run_at=RUN_AT,
    )
    assert result.valid_customers == 2
    assert result.valid_orders == 2
    assert result.rejected_records == 0
    manifest = json.loads(result.manifest_path.read_text(encoding="utf-8"))
    assert manifest["counts"]["customer_features"] == 2
    assert (tmp_path / manifest["lineage"]["silver"][0]).exists()
    assert (tmp_path / manifest["lineage"]["gold"][0]).exists()


def test_pipeline_is_idempotent_for_same_inputs(tmp_path: Path) -> None:
    config = pipeline.PipelineConfig(tmp_path)
    first = pipeline.run_pipeline(
        customers=_customers(),
        orders=_orders(),
        config=config,
        run_at=RUN_AT,
    )
    second = pipeline.run_pipeline(
        customers=_customers(),
        orders=_orders(),
        config=config,
        run_at=datetime(2026, 7, 30, 12, 0, tzinfo=timezone.utc),
    )
    assert first.dataset_version == second.dataset_version
    assert second.reused is True


def test_pipeline_version_changes_dataset_version(tmp_path: Path) -> None:
    first = pipeline.run_pipeline(
        customers=_customers(),
        orders=_orders(),
        config=pipeline.PipelineConfig(tmp_path / "one", pipeline_version="1.0.0"),
        run_at=RUN_AT,
    )
    second = pipeline.run_pipeline(
        customers=_customers(),
        orders=_orders(),
        config=pipeline.PipelineConfig(tmp_path / "two", pipeline_version="1.1.0"),
        run_at=RUN_AT,
    )
    assert first.dataset_version != second.dataset_version


def test_pipeline_quarantines_invalid_records(tmp_path: Path) -> None:
    bad_customer = _customers()[0] | {"region": "moon"}
    result = pipeline.run_pipeline(
        customers=[bad_customer, _customers()[1]],
        orders=[],
        config=pipeline.PipelineConfig(tmp_path),
        run_at=RUN_AT,
    )
    assert result.valid_customers == 1
    assert result.rejected_records == 1
    connection = sqlite3.connect(result.warehouse_path)
    try:
        assert connection.execute("SELECT COUNT(*) FROM rejected_records").fetchone()[0] == 1
    finally:
        connection.close()


def test_pipeline_quarantines_orphan_order(tmp_path: Path) -> None:
    orphan = _orders()[0] | {"customer_id": "c999"}
    result = pipeline.run_pipeline(
        customers=_customers(),
        orders=[orphan],
        config=pipeline.PipelineConfig(tmp_path),
        run_at=RUN_AT,
    )
    assert result.valid_orders == 0
    assert result.rejected_records == 1


def test_pipeline_builds_paid_customer_features(tmp_path: Path) -> None:
    result = pipeline.run_pipeline(
        customers=_customers(),
        orders=_orders(),
        config=pipeline.PipelineConfig(tmp_path),
        run_at=RUN_AT,
    )
    connection = sqlite3.connect(result.warehouse_path)
    connection.row_factory = sqlite3.Row
    try:
        c1 = connection.execute(
            "SELECT * FROM customer_features WHERE customer_id = 'c1'"
        ).fetchone()
        c2 = connection.execute(
            "SELECT * FROM customer_features WHERE customer_id = 'c2'"
        ).fetchone()
    finally:
        connection.close()
    assert c1["paid_order_count"] == 1
    assert c1["total_paid_amount"] == pytest.approx(100.0)
    assert c2["paid_order_count"] == 0


def test_newer_updates_replace_older_rows(tmp_path: Path) -> None:
    config = pipeline.PipelineConfig(tmp_path)
    first = pipeline.run_pipeline(
        customers=_customers(),
        orders=_orders(),
        config=config,
        run_at=RUN_AT,
    )
    updated_customers = _customers()
    updated_customers[0] = updated_customers[0] | {
        "customer_name": "Ada Lovelace",
        "updated_at": "2026-07-30T10:00:00Z",
    }
    pipeline.run_pipeline(
        customers=updated_customers,
        orders=_orders(),
        config=config,
        run_at=datetime(2026, 7, 30, 12, 0, tzinfo=timezone.utc),
    )
    connection = sqlite3.connect(first.warehouse_path)
    try:
        name = connection.execute(
            "SELECT customer_name FROM customers WHERE customer_id = 'c1'"
        ).fetchone()[0]
    finally:
        connection.close()
    assert name == "Ada Lovelace"


def test_older_updates_do_not_overwrite_newer_rows(tmp_path: Path) -> None:
    config = pipeline.PipelineConfig(tmp_path)
    newer = _customers()
    newer[0] = newer[0] | {
        "customer_name": "New Name",
        "updated_at": "2026-07-30T10:00:00Z",
    }
    pipeline.run_pipeline(
        customers=newer,
        orders=[],
        config=config,
        run_at=RUN_AT,
    )
    older = _customers()
    older[0] = older[0] | {
        "customer_name": "Old Name",
        "updated_at": "2026-07-28T10:00:00Z",
    }
    result = pipeline.run_pipeline(
        customers=older,
        orders=[],
        config=config,
        run_at=datetime(2026, 7, 30, 12, 0, tzinfo=timezone.utc),
    )
    connection = sqlite3.connect(result.warehouse_path)
    try:
        name = connection.execute(
            "SELECT customer_name FROM customers WHERE customer_id = 'c1'"
        ).fetchone()[0]
    finally:
        connection.close()
    assert name == "New Name"


def test_manifest_verification_passes(tmp_path: Path) -> None:
    result = pipeline.run_pipeline(
        customers=_customers(),
        orders=_orders(),
        config=pipeline.PipelineConfig(tmp_path),
        run_at=RUN_AT,
    )
    assert pipeline.verify_manifest(tmp_path, result.manifest_path) == []


def test_manifest_verification_detects_tampering(tmp_path: Path) -> None:
    result = pipeline.run_pipeline(
        customers=_customers(),
        orders=_orders(),
        config=pipeline.PipelineConfig(tmp_path),
        run_at=RUN_AT,
    )
    manifest = json.loads(result.manifest_path.read_text(encoding="utf-8"))
    artifact = tmp_path / manifest["artifacts"]["customer_features"]["path"]
    artifact.write_text("tampered", encoding="utf-8")
    assert pipeline.verify_manifest(tmp_path, result.manifest_path) == [
        "checksum mismatch: customer_features"
    ]


def test_pipeline_run_is_recorded_as_succeeded(tmp_path: Path) -> None:
    result = pipeline.run_pipeline(
        customers=_customers(),
        orders=_orders(),
        config=pipeline.PipelineConfig(tmp_path),
        run_at=RUN_AT,
    )
    connection = sqlite3.connect(result.warehouse_path)
    try:
        status = connection.execute(
            "SELECT status FROM pipeline_runs WHERE dataset_version = ?",
            (result.dataset_version,),
        ).fetchone()[0]
    finally:
        connection.close()
    assert status == "succeeded"


def test_contract_upgrade_report_exposes_fingerprint() -> None:
    report = pipeline.contract_upgrade_report(
        pipeline.CUSTOMER_CONTRACT,
        pipeline.CUSTOMER_CONTRACT,
    )
    assert report["compatible"] is True
    assert len(report["new_fingerprint"]) == 64
