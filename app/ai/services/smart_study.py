from __future__ import annotations

from app.ai.client import AIClient
from app.ai.prompts.smart_study import SmartStudyPromptBuilder
from app.ai.analyzers.models import DocumentAnalysis


class SmartStudyAIService:

    def __init__(self) -> None:
        self.client = AIClient()

    async def generate_question(
        self,
        *,
        analysis: DocumentAnalysis,
        content: str,
        previous_questions: list[str],
        weak_topics: list[str],
        difficulty: str,
    ) -> dict:

        prompt = SmartStudyPromptBuilder.build(
            analysis=analysis,
            content=content,
            previous_questions=previous_questions,
            weak_topics=weak_topics,
            difficulty=difficulty,
        )

        response = await self.client.generate_json(prompt)

        return response


# Backward compatibility alias
# Existing application services use SmartStudyEngine.
SmartStudyEngine = SmartStudyAIService
