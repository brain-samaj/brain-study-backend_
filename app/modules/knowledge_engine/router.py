from __future__ import annotations

from fastapi import APIRouter
from fastapi import Depends
from fastapi import File
from fastapi import UploadFile

from app.modules.auth.dependencies import get_current_user
from app.modules.auth.models import User
from app.modules.knowledge_engine.dependencies import get_repository
from app.modules.knowledge_engine.repository import KnowledgeRepository
from app.modules.knowledge_engine.schemas import (
    CreateTopicRequest,
    KnowledgeSourceResponse,
    UploadResponse,
)
from app.modules.knowledge_engine.service import (
    KnowledgeEngineService,
)

router = APIRouter(
    prefix="/knowledge",
    tags=["Knowledge Engine"],
)


def get_service(
    repository: KnowledgeRepository = Depends(get_repository),
) -> KnowledgeEngineService:
    return KnowledgeEngineService(repository)


@router.post(
    "/topic",
    response_model=KnowledgeSourceResponse,
)
async def create_topic(
    request: CreateTopicRequest,
    current_user: User = Depends(get_current_user),
    service: KnowledgeEngineService = Depends(get_service),
):
    return await service.create_topic(
        user_id=current_user.id,
        title=request.title,
        subject=request.subject,
        topic_description=request.topic_description,
    )


@router.post(
    "/upload",
    response_model=UploadResponse,
)
async def upload_document(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    service: KnowledgeEngineService = Depends(get_service),
):
    return await service.upload_document(
        user_id=current_user.id,
        file=file,
    )


@router.get(
    "/sources",
    response_model=list[KnowledgeSourceResponse],
)
async def list_sources(
    current_user: User = Depends(get_current_user),
    repository: KnowledgeRepository = Depends(get_repository),
):
    return repository.list_by_user(
        current_user.id,
    )
