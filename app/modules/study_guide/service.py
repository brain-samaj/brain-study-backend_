from __future__ import annotations

from fastapi import HTTPException
from fastapi import status

from app.ai.services.teacher import TeacherAI
from app.modules.knowledge_engine.repository import KnowledgeRepository


class StudyGuideService:
    """
    Generates a complete study guide from a Study Material.

    Frontend only sends:

        study_material_id

    Backend automatically:

        Study Material
            ↓
        Knowledge Engine
            ↓
        Teacher AI
            ↓
        Complete Study Guide
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

        source = self.repository.get_by_study_material(
            study_material_id,
        )

        if source is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Study material not found.",
            )

        if source.processing_status != "completed":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Study material is still processing.",
            )

        if not source.cleaned_text:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No knowledge could be extracted from this material.",
            )

        return await self.teacher.generate_study_guide(
            title=source.title,
            subject=source.subject,
            material=source.cleaned_text,
            education_level=education_level,
        )

