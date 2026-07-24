from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status
from sqlalchemy.ext.asyncio import AsyncSession

from app.ai.client import AIClient
from app.database.async_session import get_async_db
from app.modules.auth.dependencies import get_current_user
from app.modules.knowledge_engine.repository import KnowledgeRepository
from app.modules.knowledge_engine.schemas import KnowledgeResponse
from app.modules.knowledge_engine.schemas import KnowledgeSummaryResponse
from app.modules.knowledge_engine.service import KnowledgeEngineService
from app.modules.study_materials.repository import StudyMaterialRepository

router = APIRouter(
    prefix="/knowledge",
    tags=["Knowledge Engine"],
)


def get_service(
    db: AsyncSession = Depends(get_async_db),
) -> KnowledgeEngineService:
    """
    Dependency factory for the Knowledge Engine service.
    """

    return KnowledgeEngineService(
        repository=KnowledgeRepository(db),
        study_material_repository=StudyMaterialRepository(db),
        ai_client=AIClient(),
    )


@router.post(
    "/materials/{material_id}/generate",
    response_model=KnowledgeResponse,
    status_code=status.HTTP_201_CREATED,
)
async def generate_knowledge(
    material_id: UUID,
    _: object = Depends(get_current_user),
    service: KnowledgeEngineService = Depends(get_service),
) -> KnowledgeResponse:
    """
    Generate structured knowledge for a study material.

    If knowledge already exists, the cached version is returned.
    """

    try:
        knowledge = await service.build_from_material(
            material_id=material_id,
        )
        return KnowledgeResponse.model_validate(knowledge)

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc


@router.get(
    "/materials/{material_id}",
    response_model=KnowledgeResponse,
)
async def get_knowledge(
    material_id: UUID,
    _: object = Depends(get_current_user),
    service: KnowledgeEngineService = Depends(get_service),
) -> KnowledgeResponse:
    """
    Retrieve processed knowledge for a study material.
    """

    knowledge = await service.get(
        material_id=material_id,
    )

    if knowledge is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Knowledge has not been generated for this material.",
        )

    return KnowledgeResponse.model_validate(knowledge)


@router.get(
    "/materials/{material_id}/summary",
    response_model=KnowledgeSummaryResponse,
)
async def get_knowledge_summary(
    material_id: UUID,
    _: object = Depends(get_current_user),
    service: KnowledgeEngineService = Depends(get_service),
) -> KnowledgeSummaryResponse:
    """
    Retrieve a lightweight summary of processed knowledge.
    """

    knowledge = await service.get(
        material_id=material_id,
    )

    if knowledge is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Knowledge has not been generated for this material.",
        )

    return KnowledgeSummaryResponse.model_validate(knowledge)


@router.post(
    "/materials/{material_id}/refresh",
    response_model=KnowledgeResponse,
)
async def refresh_knowledge(
    material_id: UUID,
    _: object = Depends(get_current_user),
    service: KnowledgeEngineService = Depends(get_service),
) -> KnowledgeResponse:
    """
    Regenerate knowledge from the latest version of the study material.
    """

    try:
        knowledge = await service.refresh(
            material_id=material_id,
        )
        return KnowledgeResponse.model_validate(knowledge)

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc
