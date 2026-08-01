from __future__ import annotations

from app.ai.analyzers.models import DocumentAnalysis
from app.ai.client import AIClient
from app.ai.prompts.document_analysis import DocumentAnalysisPromptBuilder


class DocumentAnalyzer:
    """
    Performs one-time educational analysis of a study material.

    This analysis is stored permanently by the Knowledge Engine
    and reused by:

    • Study Guide
    • Smart Study
    • Flashcards
    • Practice Exams
    • AI Tutor
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
            temperature=0.10,
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

            teaching_style=data["teaching_style"],
            explanation_style=data["explanation_style"],
            example_density=data["example_density"],
            reasoning_depth=data["reasoning_depth"],

            needs_worked_examples=data["needs_worked_examples"],
            needs_real_life_examples=data["needs_real_life_examples"],
            needs_visual_explanations=data["needs_visual_explanations"],
            needs_step_by_step=data["needs_step_by_step"],
            needs_definitions_first=data["needs_definitions_first"],
            needs_classification=data["needs_classification"],
            needs_comparison_tables=data["needs_comparison_tables"],
            needs_timelines=data["needs_timelines"],
            needs_mnemonics=data["needs_mnemonics"],

            keywords=data["keywords"],
            learning_objectives=data["learning_objectives"],
            important_terms=data["important_terms"],
            prerequisites=data["prerequisites"],

            learning_style=data["learning_style"],
            confidence=data["confidence"],
        )
