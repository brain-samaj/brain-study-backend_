from __future__ import annotations

import logging

from app.ai.services.knowledge_builder import KnowledgeBuilder
from app.ai.services.teacher import TeacherAI
from app.modules.knowledge_engine.repository import KnowledgeRepository

logger = logging.getLogger(__name__)


class AIOrchestrator:
    """
    Brain Study AI Orchestrator

    This class is the single entry point into the AI system.

    Responsibilities

    • Process uploaded materials
    • Build the Knowledge Engine
    • Teach the material
    • Generate Smart Study
    • Generate Flashcards
    • Generate Exams

    IMPORTANT

    The frontend must NEVER know AI exists.

    Every response should feel like it was written
    by an experienced teacher.
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
        """
        Process an uploaded document or topic
        into the Knowledge Engine.
        """

        source = self.repository.get(source_id)

        if source is None:
            raise ValueError(
                "Knowledge source not found."
            )

        builder = KnowledgeBuilder(
            self.repository,
        )

        try:

            await builder.build(source)

            logger.info(
                "Knowledge Engine built for %s",
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

    async def build_learning_pack(
        self,
        *,
        subject: str,
        title: str,
        material: str,
        education_level: str,
    ):
        """
        Build a Study Guide.

        This is NOT a summary.

        The AI behaves like a world-class teacher.

        It automatically decides HOW the topic
        should be taught.

        Examples

        Mathematics
            • Formula explanation
            • Step-by-step worked examples
            • Tricks
            • Practice

        Biology
            • Processes
            • Real-life examples
            • Analogies
            • Diagrams (descriptions)

        Programming
            • Code
            • Output
            • Explanation of every line

        History
            • Timeline
            • Events
            • Cause and effect

        English
            • Examples
            • Structure
            • Grammar
            • Writing samples

        etc...
        """

        teacher = TeacherAI()

        return await teacher.generate(
            subject=subject,
            title=title,
            material=material,
            education_level=education_level,
        )

