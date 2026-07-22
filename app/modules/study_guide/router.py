from __future__ import annotations

from fastapi import APIRouter
from fastapi import Depends

from app.modules.auth.dependencies import get_current_user
from app.modules.knowledge_engine.dependencies import get_repository
from app.modules.study_guide.schemas import (
    GenerateStudyGuideRequest,
    StudyGuideResponse,
)
from app.modules.study_guide.service import StudyGuideService

router = APIRouter(
    prefix="/study-guide",
    tags=["Study Guide"],
)


@router.post(
    "/generate",
    response_model=StudyGuideResponse,
)
async def generate_study_guide(
    request: GenerateStudyGuideRequest,
    current_user=Depends(get_current_user),
    repository=Depends(get_repository),
):
    """
    Generate a complete AI-powered Study Guide from a Study Material.
    """

    service = StudyGuideService(
        repository=repository,
    )

    study_guide = await service.generate(
        study_material_id=request.study_material_id,
        education_level=current_user.education_level,
    )

    return StudyGuideResponse(
        study_guide=study_guide,
    )
