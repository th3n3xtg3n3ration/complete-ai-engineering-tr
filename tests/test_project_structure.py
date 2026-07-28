from pathlib import Path

ROOT = Path(__file__).parents[1]


def test_required_project_files_exist() -> None:
    required = [
        "README.md",
        "README.tr.md",
        "README.en.md",
        "CURRICULUM.md",
        "ROADMAP.md",
        "CONTRIBUTING.md",
        "CODE_OF_CONDUCT.md",
        "SECURITY.md",
        "LICENSE-CODE",
        "LICENSE-CONTENT.md",
    ]
    missing = [path for path in required if not (ROOT / path).exists()]
    assert not missing, f"Eksik proje dosyaları: {missing}"


def test_first_lesson_has_required_artifacts() -> None:
    lesson = ROOT / "curriculum/tr/00-orientation/01-ai-ecosystem"
    required = [
        "README.md",
        "metadata.yml",
        "theory.md",
        "concept-map.md",
        "exercises/beginner.md",
        "quiz/pre-quiz.json",
        "quiz/post-quiz.json",
        "assignment/assignment.md",
        "assignment/rubric.md",
        "common-mistakes.md",
        "interview-questions.md",
    ]
    missing = [path for path in required if not (lesson / path).exists()]
    assert not missing, f"İlk derste eksik dosyalar: {missing}"


def test_all_modules_have_readme() -> None:
    module_root = ROOT / "curriculum/tr"
    modules = [path for path in module_root.iterdir() if path.is_dir()]
    assert len(modules) == 16
    assert all((module / "README.md").exists() for module in modules)
