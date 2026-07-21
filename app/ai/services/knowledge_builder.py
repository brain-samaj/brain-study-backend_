from __future__ import annotations

from app.ai.services.document_processor import DocumentProcessor
from app.ai.services.study_guide_generator import StudyGuideGenerator
from app.ai.services.flashcard_generator import FlashcardGenerator
from app.ai.services.exam_generator import ExamGenerator
from app.modules.knowledge_engine.models import KnowledgeSource
from app.modules.knowledge_engine.repository import KnowledgeRepository


class KnowledgeBuilder:
    """
    Complete AI pipeline.

    Upload
        ↓
    Extract Text
        ↓
    Clean Text
        ↓
    Study Guide
        ↓
    Flashcards
        ↓
    Exams
    """

    def __init__(
        self,
        repository: KnowledgeRepository,
    ):
        self.repository = repository

        self.processor = DocumentProcessor(
            repository,
        )

        self.study_guide = StudyGuideGenerator()

        self.flashcards = FlashcardGenerator()

        self.exam = ExamGenerator()

    async def build(
        self,
        source: KnowledgeSource,
    ) -> None:

        source = await self.processor.process(
            source,
        )

        if not source.cleaned_text:
            raise ValueError(
                "No extracted text."
            )

        await self.study_guide.generate(
            source=source,
        )

        await self.flashcards.generate(
            source=source,
        )

        await self.exam.generate(
            source=source,
        )
