from __future__ import annotations

from pathlib import Path

from app.ai.extractors.factory import ExtractorFactory
from app.ai.retrieval.cleaner import TextCleaner
from app.modules.knowledge_engine.models import KnowledgeSource
from app.modules.knowledge_engine.repository import KnowledgeRepository


class DocumentProcessor:

    def __init__(
        self,
        repository: KnowledgeRepository,
    ):
        self.repository = repository

    async def process(
        self,
        source: KnowledgeSource,
    ) -> KnowledgeSource:

        if not source.file_path:
            raise ValueError("Document has no file path.")

        extractor = ExtractorFactory.create(
            Path(source.file_path),
        )

        raw_text = extractor.extract()

        cleaned_text = TextCleaner.clean(
            raw_text,
        )

        return self.repository.update_processing(
            source,
            status="completed",
            raw_text=raw_text,
            cleaned_text=cleaned_text,
        )

    async def fail(
        self,
        source: KnowledgeSource,
        error: Exception,
    ) -> KnowledgeSource:

        return self.repository.update_processing(
            source,
            status="failed",
            error_message=str(error),
        )
