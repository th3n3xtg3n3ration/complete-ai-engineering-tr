import json

import pytest

from data_toolkit import Record, load_records, save_records, summarize


def test_record_rejects_negative_value():
    with pytest.raises(ValueError):
        Record("r-1", "model", -1)


def test_save_and_load_round_trip(tmp_path):
    path = tmp_path / "nested" / "records.json"
    expected = [Record("r-1", "model", 10.5), Record("r-2", "veri", 4)]

    save_records(path, expected)

    assert path.exists()
    assert load_records(path) == expected
    assert "veri" in path.read_text(encoding="utf-8")


def test_load_rejects_non_list_root(tmp_path):
    path = tmp_path / "records.json"
    path.write_text(json.dumps({"record_id": "r-1"}), encoding="utf-8")

    with pytest.raises(TypeError, match="liste"):
        load_records(path)


def test_load_rejects_invalid_record(tmp_path):
    path = tmp_path / "records.json"
    path.write_text('[{"record_id": "r-1", "category": "x"}]', encoding="utf-8")

    with pytest.raises(ValueError, match="Eksik"):
        load_records(path)


def test_summarize_groups_categories():
    records = [
        Record("1", "training", 8),
        Record("2", "training", 2.5),
        Record("3", "inference", 3),
    ]

    assert summarize(records) == {"training": 10.5, "inference": 3.0}