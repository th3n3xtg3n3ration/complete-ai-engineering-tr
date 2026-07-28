"""AI yaklaşımı seçimini öğretmek için basitleştirilmiş karar yardımcısı."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ProblemProfile:
    """Bir problemin öğretici amaçla kullanılan temel özellikleri."""

    rules_are_explicit: bool
    needs_prediction_from_data: bool
    needs_natural_language_generation: bool
    needs_private_or_current_knowledge: bool
    needs_multiple_tools_or_steps: bool


def recommend_approach(profile: ProblemProfile) -> list[str]:
    """Problem özelliklerine göre olası yaklaşımları basitten karmaşığa sıralar."""
    approaches: list[str] = []

    if profile.rules_are_explicit:
        approaches.append("classical-software")

    if profile.needs_prediction_from_data:
        approaches.append("machine-learning")

    if profile.needs_natural_language_generation:
        approaches.append("llm")

    if profile.needs_private_or_current_knowledge:
        approaches.append("rag")

    if profile.needs_multiple_tools_or_steps:
        approaches.append("agentic-workflow")

    if not approaches:
        approaches.append("clarify-problem")

    return approaches


def main() -> None:
    company_assistant = ProblemProfile(
        rules_are_explicit=True,
        needs_prediction_from_data=False,
        needs_natural_language_generation=True,
        needs_private_or_current_knowledge=True,
        needs_multiple_tools_or_steps=True,
    )

    print("Önerilen bileşenler:")
    for approach in recommend_approach(company_assistant):
        print(f"- {approach}")


if __name__ == "__main__":
    main()
