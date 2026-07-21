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
    user=Depends(get_current_user),
    repository=Depends(get_repository),
):

    service = StudyGuideService(repository)

    return await service.generate(
        knowledge_source_id=request.knowledge_source_id,
        education_level=user.education_level,
    )
