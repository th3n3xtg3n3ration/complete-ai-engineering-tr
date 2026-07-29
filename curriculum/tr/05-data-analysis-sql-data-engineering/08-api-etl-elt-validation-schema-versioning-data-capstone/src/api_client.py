"""HTTP extraction, retry, pagination, and immutable raw snapshot helpers."""

from __future__ import annotations

from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
from time import sleep
from typing import Any
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

JsonValue = dict[str, Any] | list[Any] | str | int | float | bool | None


@dataclass(frozen=True)
class HttpResponse:
    """Minimal transport-independent HTTP response."""

    status_code: int
    headers: Mapping[str, str]
    body: bytes


@dataclass(frozen=True)
class RetryPolicy:
    """Retry configuration for transient API failures."""

    max_attempts: int = 3
    base_delay_seconds: float = 0.1
    retry_statuses: tuple[int, ...] = (429, 500, 502, 503, 504)

    def __post_init__(self) -> None:
        if self.max_attempts <= 0:
            raise ValueError("max_attempts must be positive")
        if self.base_delay_seconds < 0:
            raise ValueError("base_delay_seconds must be non-negative")


@dataclass(frozen=True)
class RawSnapshot:
    """Metadata for one immutable raw JSON snapshot."""

    path: Path
    checksum: str
    record_count: int
    schema_version: str


class ApiError(RuntimeError):
    """Raised when extraction cannot return a valid JSON response."""


Transport = Callable[[str, Mapping[str, str], float], HttpResponse]
SleepFunction = Callable[[float], None]


def canonical_json_bytes(value: JsonValue) -> bytes:
    """Serialize JSON deterministically for hashing and versioning."""

    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")


def sha256_hex(content: bytes) -> str:
    """Return a hexadecimal SHA-256 digest."""

    return hashlib.sha256(content).hexdigest()


def _with_query_parameter(url: str, key: str, value: str) -> str:
    parts = urlsplit(url)
    query = dict(parse_qsl(parts.query, keep_blank_values=True))
    query[key] = value
    return urlunsplit((parts.scheme, parts.netloc, parts.path, urlencode(query), parts.fragment))


def _retry_delay(response: HttpResponse, policy: RetryPolicy, attempt: int) -> float:
    retry_after = response.headers.get("Retry-After")
    if retry_after is not None:
        try:
            return max(0.0, float(retry_after))
        except ValueError:
            pass
    return policy.base_delay_seconds * (2 ** (attempt - 1))


class ApiClient:
    """Small dependency-injected JSON API client with retry and pagination."""

    def __init__(
        self,
        transport: Transport,
        *,
        retry_policy: RetryPolicy | None = None,
        timeout_seconds: float = 10.0,
        sleep_fn: SleepFunction = sleep,
    ) -> None:
        if timeout_seconds <= 0:
            raise ValueError("timeout_seconds must be positive")
        self._transport = transport
        self._retry_policy = retry_policy or RetryPolicy()
        self._timeout_seconds = timeout_seconds
        self._sleep_fn = sleep_fn

    def get_json(
        self,
        url: str,
        *,
        headers: Mapping[str, str] | None = None,
    ) -> JsonValue:
        """Fetch one JSON document, retrying only transient failures."""

        request_headers = {"Accept": "application/json", **dict(headers or {})}
        last_error: Exception | None = None
        for attempt in range(1, self._retry_policy.max_attempts + 1):
            try:
                response = self._transport(url, request_headers, self._timeout_seconds)
            except OSError as error:
                last_error = error
                if attempt == self._retry_policy.max_attempts:
                    break
                self._sleep_fn(self._retry_policy.base_delay_seconds * (2 ** (attempt - 1)))
                continue

            if 200 <= response.status_code < 300:
                try:
                    return json.loads(response.body.decode("utf-8"))
                except (UnicodeDecodeError, json.JSONDecodeError) as error:
                    raise ApiError("API response is not valid UTF-8 JSON") from error

            if response.status_code not in self._retry_policy.retry_statuses:
                raise ApiError(f"API request failed with status {response.status_code}")
            if attempt < self._retry_policy.max_attempts:
                self._sleep_fn(_retry_delay(response, self._retry_policy, attempt))

        message = "API request exhausted retry attempts"
        if last_error is not None:
            raise ApiError(message) from last_error
        raise ApiError(message)

    def paginate(
        self,
        url: str,
        *,
        items_key: str = "items",
        next_cursor_key: str = "next_cursor",
        cursor_parameter: str = "cursor",
        headers: Mapping[str, str] | None = None,
        max_pages: int = 100,
    ) -> list[dict[str, Any]]:
        """Collect cursor-paginated records and guard against cursor loops."""

        if max_pages <= 0:
            raise ValueError("max_pages must be positive")
        records: list[dict[str, Any]] = []
        cursor: str | None = None
        seen_cursors: set[str] = set()
        current_url = url

        for _ in range(max_pages):
            payload = self.get_json(current_url, headers=headers)
            if not isinstance(payload, dict):
                raise ApiError("paginated response must be a JSON object")
            items = payload.get(items_key)
            if not isinstance(items, list) or not all(isinstance(item, dict) for item in items):
                raise ApiError(f"{items_key!r} must be a list of objects")
            records.extend(items)

            next_cursor = payload.get(next_cursor_key)
            if next_cursor in (None, ""):
                return records
            cursor = str(next_cursor)
            if cursor in seen_cursors:
                raise ApiError("pagination cursor loop detected")
            seen_cursors.add(cursor)
            current_url = _with_query_parameter(url, cursor_parameter, cursor)

        raise ApiError(f"pagination exceeded max_pages={max_pages}")


def _record_count(payload: JsonValue) -> int:
    if isinstance(payload, list):
        return len(payload)
    if isinstance(payload, dict) and isinstance(payload.get("items"), list):
        return len(payload["items"])
    return 1


def write_raw_snapshot(
    root: str | Path,
    *,
    source: str,
    payload: JsonValue,
    fetched_at: datetime,
    schema_version: str,
) -> RawSnapshot:
    """Write a content-addressed immutable JSON envelope with atomic replacement."""

    if not source.strip():
        raise ValueError("source must not be empty")
    if not schema_version.strip():
        raise ValueError("schema_version must not be empty")
    if fetched_at.tzinfo is None:
        raise ValueError("fetched_at must be timezone-aware")

    timestamp = fetched_at.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")
    envelope: dict[str, Any] = {
        "metadata": {
            "source": source,
            "fetched_at": timestamp,
            "schema_version": schema_version,
        },
        "data": payload,
    }
    content = canonical_json_bytes(envelope)
    checksum = sha256_hex(content)
    safe_timestamp = timestamp.replace(":", "").replace("-", "")
    directory = Path(root) / source
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / f"{safe_timestamp}_{checksum[:16]}.json"
    if not path.exists():
        temporary = path.with_suffix(".tmp")
        temporary.write_bytes(content)
        temporary.replace(path)
    return RawSnapshot(
        path=path,
        checksum=checksum,
        record_count=_record_count(payload),
        schema_version=schema_version,
    )
