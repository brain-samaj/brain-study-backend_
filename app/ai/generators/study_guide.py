from __future__ import annotations

from app.ai.client import AIClient
from app.ai.analyzers.models import DocumentAnalysis
from app.ai.prompts.study_guide import StudyGuidePromptBuilder


class StudyGuideGenerator:

    def __init__(self) -> None:
        self.client = AIClient()

    def generate(
        self,
        analysis: DocumentAnalysis,
        text: str,
    ) -> str:

        prompt = StudyGuidePromptBuilder.build(
            analysis,
            text,
        )

        return self.client.chat(
            prompt=prompt,
            model="llama-3.3-70b-versatile",
        )
