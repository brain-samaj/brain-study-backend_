from __future__ import annotations

from app.ai.analyzers.models import DocumentAnalysis
from app.ai.client import AIClient
from app.ai.prompts.objective_exam import build_objective_prompt
from app.ai.prompts.theory_exam import build_theory_exam_prompt
from app.modules.knowledge_engine.models import KnowledgeSource


class ExamGenerator:
    """
    Generates objective and theory examinations
    from processed knowledge sources.
    """

    def __init__(self):
        self.client = AIClient()

    async def generate(
        self,
        *,
        source: KnowledgeSource,
        objective_count: int = 10,
        theory_duration: int = 120,
        theory_answer_any: int = 5,
    ) -> dict:

        analysis = DocumentAnalysis(
            subject=source.subject,
            topic=source.title,
        )

        material = source.cleaned_text or ""

        objective_prompt = build_objective_prompt(
            analysis=analysis,
            material=material,
            total_questions=objective_count,
        )

        theory_prompt = build_theory_exam_prompt(
            analysis=analysis,
            material=material,
            duration=theory_duration,
            answer_any=theory_answer_any,
        )

        objective_questions = await self.client.generate_json(
            objective_prompt,
        )

        theory_questions = await self.client.generate_json(
            theory_prompt,
        )

        return {
            "objective": objective_questions,
            "theory": theory_questions,
        }
