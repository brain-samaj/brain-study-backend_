from __future__ import annotations

from pathlib import Path

from app.ai.services.document_processor import DocumentProcessor
from app.ai.services.knowledge_builder import KnowledgeBuilder
from app.ai.services.knowledge_builder import KnowledgeDocument


class KnowledgeOrchestrator:
    """
    Central pipeline for every study material.

    Upload
        ↓
    Extraction
        ↓
    Cleaning
        ↓
    Analysis
        ↓
    Chunking
        ↓
    Knowledge Building
        ↓
    Ready for:

        • Study Guide
        • Smart Study
        • Flashcards
        • Practice Exam
    """

    def __init__(self) -> None:

        self.processor = DocumentProcessor()

        self.builder = KnowledgeBuilder()

    async def process_file(
        self,
        path: str | Path,
    ) -> KnowledgeDocument:

        processed = await self.processor.process_file(
            path,
        )

        return self.builder.build(
            processed,
        )

    async def process_topic(
        self,
        *,
        title: str,
        subject: str,
        topic: str,
    ) -> KnowledgeDocument:

        processed = await self.processor.process_topic(
            title=title,
            subject=subject,
            topic=topic,
        )

        return self.builder.build(
            processed,
        )
