from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
import sys
import tempfile

MODULE_PATH = Path(__file__).parents[1] / "tools" / "create_lesson.py"
SPEC = spec_from_file_location("create_lesson_tool", MODULE_PATH)
assert SPEC is not None and SPEC.loader is not None
MODULE = module_from_spec(SPEC)
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)

create_lesson = MODULE.create_lesson


def test_create_lesson_copies_and_customizes_template() -> None:
    with tempfile.TemporaryDirectory() as temporary_directory:
        module = Path(temporary_directory) / "01-python"
        lesson = create_lesson(
            module=module,
            lesson="01-variables-and-data-types",
            title="Değişkenler ve Veri Tipleri",
            level="L0",
        )

        assert lesson.exists()
        readme = (lesson / "README.md").read_text(encoding="utf-8")
        metadata = (lesson / "metadata.yml").read_text(encoding="utf-8")
        assert "Değişkenler ve Veri Tipleri" in readme
        assert "level: L0" in metadata
