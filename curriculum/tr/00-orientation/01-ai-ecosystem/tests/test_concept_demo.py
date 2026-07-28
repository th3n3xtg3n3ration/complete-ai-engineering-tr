from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
import sys

MODULE_PATH = Path(__file__).parents[1] / "src" / "concept_demo.py"
SPEC = spec_from_file_location("concept_demo", MODULE_PATH)
assert SPEC is not None and SPEC.loader is not None
MODULE = module_from_spec(SPEC)
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)

ProblemProfile = MODULE.ProblemProfile
recommend_approach = MODULE.recommend_approach


def test_explicit_rules_only_recommend_classical_software() -> None:
    profile = ProblemProfile(True, False, False, False, False)
    assert recommend_approach(profile) == ["classical-software"]


def test_company_assistant_combines_multiple_components() -> None:
    profile = ProblemProfile(True, False, True, True, True)
    assert recommend_approach(profile) == [
        "classical-software",
        "llm",
        "rag",
        "agentic-workflow",
    ]


def test_undefined_problem_requests_clarification() -> None:
    profile = ProblemProfile(False, False, False, False, False)
    assert recommend_approach(profile) == ["clarify-problem"]
