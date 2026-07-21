from __future__ import annotations

import logging

from app.ai.services.knowledge_builder import KnowledgeBuilder
from app.modules.knowledge_engine.repository import KnowledgeRepository

logger = logging.getLogger(__name__)


class AIOrchestrator:
    """
    Coordinates the complete AI pipeline.

    Upload
      ↓
    OCR / Text Extraction
      ↓
    Cleaning
      ↓
    Embeddings
      ↓
    Knowledge Base
      ↓
    Study Guide
      ↓
    Flashcards
      ↓
    Smart Study
      ↓
    Objective Exam
      ↓
    Theory Exam
    """

    def __init__(
        self,
        repository: KnowledgeRepository,
    ):
        self.repository = repository

    async def process_source(
        self,
        source_id,
    ):

        source = self.repository.get(
            source_id,
        )

        if source is None:
            raise ValueError(
                "Knowledge source not found."
            )

        builder = KnowledgeBuilder(
            self.repository,
        )

        try:

            await builder.build(
                source,
            )

            logger.info(
                "Knowledge pipeline completed for %s",
                source.id,
            )

            return source

        except Exception as exc:

            logger.exception(exc)

            self.repository.update_processing(
                source,
                status="failed",
                error_message=str(exc),
            )

            raise
