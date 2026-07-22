from __future__ import annotations

from app.ai.analyzers.models import DocumentAnalysis
from app.ai.client import AIClient
from app.ai.prompts.document_analysis import DocumentAnalysisPromptBuilder


class DocumentAnalyzer:
    """
    Performs a deep educational analysis of a document.

    The analysis produced here powers:

    • Study Guide
    • Smart Study
    • Flashcards
    • Practice Exam
    """

    def __init__(
        self,
        client: AIClient | None = None,
    ) -> None:

        self.client = client or AIClient()

    async def analyze(
        self,
        *,
        title: str,
        content: str,
    ) -> DocumentAnalysis:

        prompt = DocumentAnalysisPromptBuilder.build(
            title=title,
            content=content,
        )

        data = await self.client.generate_json(
            prompt=prompt,
            temperature=0.1,
        )

        return DocumentAnalysis(
            title=data["title"],
            subject=data["subject"],
            topic=data["topic"],
            difficulty=data["difficulty"],
            language=data["language"],
            education_level=data["education_level"],
            estimated_reading_minutes=data["estimated_reading_minutes"],
            word_count=data["word_count"],
            requires_calculations=data["requires_calculations"],
            requires_formulae=data["requires_formulae"],
            requires_tables=data["requires_tables"],
            requires_diagrams=data["requires_diagrams"],
            requires_code=data["requires_code"],
            requires_memorization=data["requires_memorization"],
            keywords=data["keywords"],
            learning_objectives=data["learning_objectives"],
            important_terms=data["important_terms"],
            prerequisites=data["prerequisites"],
            learning_style=data["learning_style"],
            confidence=data["confidence"],
        )
