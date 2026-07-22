from __future__ import annotations

from app.ai.services.orchestrator import AIOrchestrator
from app.modules.knowledge_engine.repository import KnowledgeRepository


class StudyGuideService:
    """
    Service layer responsible for generating study guides.

    Flow:
        Router
          ↓
        StudyGuideService
          ↓
        KnowledgeRepository
          ↓
        AIOrchestrator
          ↓
        Generated Learning Pack
    """

    def __init__(
        self,
        repository: KnowledgeRepository,
    ) -> None:
        self.repository = repository
        self.ai = AIOrchestrator(repository)

    async def generate(
        self,
        knowledge_source_id,
        education_level,
    ):
        """
        Generate a study guide from a knowledge source.
        """

        source = self.repository.get(
            knowledge_source_id,
        )

        if source is None:
            raise ValueError(
                "Knowledge source not found."
            )

        return await self.ai.build_learning_pack(
            subject=source.subject,
            title=source.title,
            material=source.cleaned_text,
            education_level=education_level,
        )
