from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any


@dataclass(frozen=True, slots=True)
class Record:
    """Dosyada saklanacak doğrulanmış bir kayıt."""

    record_id: str
    category: str
    value: float

    def __post_init__(self) -> None:
        if not self.record_id.strip():
            raise ValueError("record_id boş olamaz")
        if not self.category.strip():
            raise ValueError("category boş olamaz")
        if self.value < 0:
            raise ValueError("value negatif olamaz")

    def to_dict(self) -> dict[str, str | float]:
        return asdict(self)

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "Record":
        required = {"record_id", "category", "value"}
        missing = required - payload.keys()
        if missing:
            raise ValueError(f"Eksik alanlar: {', '.join(sorted(missing))}")

        record_id = payload["record_id"]
        category = payload["category"]
        value = payload["value"]

        if not isinstance(record_id, str) or not isinstance(category, str):
            raise TypeError("record_id ve category metin olmalıdır")
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise TypeError("value sayısal olmalıdır")

        return cls(record_id=record_id, category=category, value=float(value))