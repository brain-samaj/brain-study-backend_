from __future__ import annotations

from app.ai.client import AIClient
from app.ai.prompts.objective_exam import OBJECTIVE_EXAM_PROMPT
from app.ai.prompts.theory_exam import THEORY_EXAM_PROMPT
from app.modules.knowledge_engine.models import KnowledgeSource


class ExamGenerator:

    def __init__(self):
        self.client = AIClient()

    async def generate(
        self,
        *,
        source: KnowledgeSource,
    ) -> dict:

        objective_prompt = OBJECTIVE_EXAM_PROMPT.format(
            title=source.title,
            subject=source.subject,
            content=source.cleaned_text,
        )

        theory_prompt = THEORY_EXAM_PROMPT.format(
            title=source.title,
            subject=source.subject,
            content=source.cleaned_text,
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
