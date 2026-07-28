from pathlib import Path
import importlib.util

import pytest

MODULE_PATH = Path(__file__).parents[1] / "src" / "data_pipeline.py"
SPEC = importlib.util.spec_from_file_location("data_pipeline", MODULE_PATH)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)

Record = MODULE.Record
InvalidRecordError = MODULE.InvalidRecordError
validate_record = MODULE.validate_record
iter_valid_records = MODULE.iter_valid_records
batch = MODULE.batch
summarize = MODULE.summarize


def test_validate_record_normalizes_values():
    assert validate_record({"name": " Ada ", "score": 90}) == Record("Ada", 90.0)


@pytest.mark.parametrize(
    "row",
    [
        {"name": "", "score": 50},
        {"name": "Ada", "score": "90"},
        {"name": "Ada", "score": -1},
        {"name": "Ada", "score": 101},
        {"name": "Ada", "score": True},
    ],
)
def test_validate_record_rejects_invalid_rows(row):
    with pytest.raises(InvalidRecordError):
        validate_record(row)


def test_iter_valid_records_skips_invalid_rows():
    rows = [
        {"name": "Ada", "score": 90},
        {"name": "", "score": 30},
        {"name": "Mert", "score": 70},
    ]
    assert list(iter_valid_records(rows)) == [Record("Ada", 90), Record("Mert", 70)]


def test_batch_groups_and_keeps_remainder():
    assert list(batch(range(5), 2)) == [[0, 1], [2, 3], [4]]


def test_batch_rejects_non_positive_size():
    with pytest.raises(ValueError):
        list(batch([1, 2], 0))


def test_summarize_records():
    result = summarize([Record("Ada", 90), Record("Mert", 70)])
    assert result == {"count": 2, "average": 80.0, "maximum": 90}


def test_summarize_empty_input():
    assert summarize([]) == {"count": 0, "average": 0.0, "maximum": 0.0}
