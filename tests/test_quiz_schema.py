import json
from pathlib import Path

ROOT = Path(__file__).parents[1]


def test_quiz_files_have_valid_answers() -> None:
    quiz_files = list((ROOT / "curriculum").rglob("quiz/*.json"))
    assert quiz_files

    for path in quiz_files:
        data = json.loads(path.read_text(encoding="utf-8"))
        assert data["type"] in {"pre", "post"}
        assert isinstance(data["questions"], list)
        for question in data["questions"]:
            assert len(question["options"]) >= 2
            assert 0 <= question["answer_index"] < len(question["options"])
            assert question["explanation"].strip()
