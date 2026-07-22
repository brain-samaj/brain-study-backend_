from __future__ import annotations

from fastapi import APIRouter
from fastapi import Depends

from app.modules.auth.dependencies import get_current_user
from app.modules.knowledge_engine.dependencies import get_repository
from app.modules.study_guide.schemas import GenerateStudyGuideRequest
from app.modules.study_guide.service import StudyGuideService

router = APIRouter(
    prefix="/study-guide",
    tags=["Study Guide"],
)


@router.post("/generate")
async def generate_study_guide(
    request: GenerateStudyGuideRequest,
    current_user=Depends(get_current_user),
    repository=Depends(get_repository),
):
    """
    Generate a complete Study Guide.

    The frontend never tells the AI how to teach.

    It only supplies the knowledge source.

    Brain Study automatically teaches the topic
    in the best possible way for the student's
    education level.
    """

    service = StudyGuideService(
        repository=repository,
    )

    return await service.generate(
        knowledge_source_id=request.knowledge_source_id,
        education_level=current_user.education_level,
    )

