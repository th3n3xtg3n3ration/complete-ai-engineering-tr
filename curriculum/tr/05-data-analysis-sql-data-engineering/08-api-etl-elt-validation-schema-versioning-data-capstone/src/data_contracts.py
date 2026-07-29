"""Versioned data contracts and record-level validation utilities."""

from __future__ import annotations

import json
import re
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from typing import Any, Literal

from api_client import canonical_json_bytes, sha256_hex

TypeName = Literal["string", "integer", "number", "boolean", "datetime"]


@dataclass(frozen=True)
class FieldSpec:
    """Schema and validation rules for one field."""

    name: str
    type_name: TypeName
    required: bool = True
    nullable: bool = False
    minimum: float | None = None
    maximum: float | None = None
    allowed_values: tuple[Any, ...] = ()
    pattern: str | None = None


@dataclass(frozen=True)
class DataContract:
    """Versioned record contract with an optional primary key."""

    name: str
    version: str
    fields: tuple[FieldSpec, ...]
    primary_key: tuple[str, ...] = ()
    reject_unknown_fields: bool = True

    def fingerprint(self) -> str:
        payload = {
            "name": self.name,
            "version": self.version,
            "fields": [asdict(field) for field in self.fields],
            "primary_key": self.primary_key,
            "reject_unknown_fields": self.reject_unknown_fields,
        }
        return sha256_hex(canonical_json_bytes(payload))


@dataclass(frozen=True)
class ValidationIssue:
    """One validation problem attached to a record and field."""

    record_index: int
    field: str
    code: str
    message: str


@dataclass(frozen=True)
class ValidationResult:
    """Validated records and rejected-record diagnostics."""

    valid_records: tuple[dict[str, Any], ...]
    issues: tuple[ValidationIssue, ...]
    rejected_indices: tuple[int, ...]


def _coerce_datetime(value: Any) -> str:
    if not isinstance(value, str):
        raise ValueError("expected ISO-8601 datetime string")
    normalized = value[:-1] + "+00:00" if value.endswith("Z") else value
    parsed = datetime.fromisoformat(normalized)
    if parsed.tzinfo is None:
        raise ValueError("datetime must include a timezone")
    return parsed.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


def _coerce_value(value: Any, type_name: TypeName) -> Any:
    if type_name == "string":
        if not isinstance(value, str):
            raise ValueError("expected string")
        return value.strip()
    if type_name == "integer":
        if isinstance(value, bool):
            raise ValueError("expected integer")
        if isinstance(value, int):
            return value
        if isinstance(value, str) and re.fullmatch(r"[+-]?\d+", value.strip()):
            return int(value)
        raise ValueError("expected integer")
    if type_name == "number":
        if isinstance(value, bool):
            raise ValueError("expected number")
        try:
            number = float(value)
        except (TypeError, ValueError) as error:
            raise ValueError("expected number") from error
        if number != number or number in (float("inf"), float("-inf")):
            raise ValueError("number must be finite")
        return number
    if type_name == "boolean":
        if isinstance(value, bool):
            return value
        if value in (0, "0", "false", "False"):
            return False
        if value in (1, "1", "true", "True"):
            return True
        raise ValueError("expected boolean")
    if type_name == "datetime":
        return _coerce_datetime(value)
    raise ValueError(f"unsupported type: {type_name}")


def _validate_field(field: FieldSpec, value: Any) -> Any:
    if value is None:
        if field.nullable:
            return None
        raise ValueError("null is not allowed")
    coerced = _coerce_value(value, field.type_name)
    if field.minimum is not None and float(coerced) < field.minimum:
        raise ValueError(f"value must be >= {field.minimum}")
    if field.maximum is not None and float(coerced) > field.maximum:
        raise ValueError(f"value must be <= {field.maximum}")
    if field.allowed_values and coerced not in field.allowed_values:
        raise ValueError(f"value must be one of {field.allowed_values}")
    if field.pattern is not None and not re.fullmatch(field.pattern, str(coerced)):
        raise ValueError(f"value does not match pattern {field.pattern!r}")
    return coerced


def validate_records(
    records: list[dict[str, Any]],
    contract: DataContract,
) -> ValidationResult:
    """Validate and coerce records while preserving detailed rejection reasons."""

    fields = {field.name: field for field in contract.fields}
    valid: list[dict[str, Any]] = []
    issues: list[ValidationIssue] = []
    rejected: set[int] = set()
    seen_keys: set[tuple[Any, ...]] = set()

    for index, record in enumerate(records):
        if not isinstance(record, dict):
            issues.append(ValidationIssue(index, "<record>", "type", "record must be an object"))
            rejected.add(index)
            continue

        unknown = sorted(set(record) - set(fields))
        if unknown and contract.reject_unknown_fields:
            issues.append(
                ValidationIssue(index, "<record>", "unknown_fields", f"unknown fields: {unknown}")
            )
            rejected.add(index)

        normalized: dict[str, Any] = {}
        for field in contract.fields:
            if field.name not in record:
                if field.required:
                    issues.append(
                        ValidationIssue(index, field.name, "required", "required field is missing")
                    )
                    rejected.add(index)
                continue
            try:
                normalized[field.name] = _validate_field(field, record[field.name])
            except ValueError as error:
                issues.append(ValidationIssue(index, field.name, "invalid", str(error)))
                rejected.add(index)

        if index in rejected:
            continue
        if contract.primary_key:
            key = tuple(normalized.get(column) for column in contract.primary_key)
            if any(value is None for value in key):
                issues.append(
                    ValidationIssue(
                        index,
                        "<primary_key>",
                        "null_key",
                        "primary key cannot be null",
                    )
                )
                rejected.add(index)
                continue
            if key in seen_keys:
                issues.append(
                    ValidationIssue(
                        index,
                        "<primary_key>",
                        "duplicate_key",
                        f"duplicate key: {key}",
                    )
                )
                rejected.add(index)
                continue
            seen_keys.add(key)
        valid.append(normalized)

    return ValidationResult(tuple(valid), tuple(issues), tuple(sorted(rejected)))


def compatibility_issues(old: DataContract, new: DataContract) -> list[str]:
    """Return backward-compatibility problems for consumers of the old contract."""

    old_fields = {field.name: field for field in old.fields}
    new_fields = {field.name: field for field in new.fields}
    issues: list[str] = []

    for name, old_field in old_fields.items():
        new_field = new_fields.get(name)
        if new_field is None:
            issues.append(f"field removed: {name}")
            continue
        if old_field.type_name != new_field.type_name:
            issues.append(f"field type changed: {name}")
        if old_field.nullable and not new_field.nullable:
            issues.append(f"nullable field became non-nullable: {name}")
        if set(old_field.allowed_values) - set(new_field.allowed_values):
            issues.append(f"allowed values removed: {name}")

    for name, new_field in new_fields.items():
        if name not in old_fields and new_field.required and not new_field.nullable:
            issues.append(f"new required field added: {name}")

    if old.primary_key != new.primary_key:
        issues.append("primary key changed")
    return issues


def issues_as_json(issues: list[ValidationIssue] | tuple[ValidationIssue, ...]) -> str:
    """Serialize issues deterministically for quarantine storage."""

    return json.dumps([asdict(issue) for issue in issues], ensure_ascii=False, sort_keys=True)
