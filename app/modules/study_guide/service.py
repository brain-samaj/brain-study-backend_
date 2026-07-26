from __future__ import annotations

from fastapi import HTTPException, status

from app.ai.services.teacher import TeacherAI
from app.modules.knowledge_engine.repository import KnowledgeRepository


class StudyGuideService:
    """
    Generates a complete study guide from KnowledgeSource.
    """

    def __init__(
        self,
        repository: KnowledgeRepository,
    ) -> None:
        self.repository = repository
        self.teacher = TeacherAI()

    async def generate(
        self,
        *,
        study_material_id,
        education_level: str,
    ):
        source = await self.repository.get_by_material(
            material_id=study_material_id
        )

        if source is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Knowledge source not found.",
            )

        source_status = (
            source.status.value
            if hasattr(source.status, "value")
            else source.status
        )

        if source_status != "READY":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Knowledge source is not ready yet. Current status: {source_status}",
            )

        if not source.knowledge:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No extracted knowledge available.",
            )

        return await self.teacher.generate_study_guide(
            title=source.title,
            subject=source.title,
            material=source.knowledge,
            education_level=education_level,
        )
