from __future__ import annotations

from fastapi import APIRouter
from fastapi import Depends
from fastapi import File
from fastapi import UploadFile
from fastapi import status

from app.modules.auth.dependencies import get_current_user
from app.modules.knowledge_engine.dependencies import get_repository
from app.modules.knowledge_engine.schemas import (
    CreateTopicRequest,
    KnowledgeSourceResponse,
)
from app.modules.knowledge_engine.service import KnowledgeEngineService

router = APIRouter(
    prefix="/knowledge",
    tags=["Knowledge Engine"],
)


@router.post(
    "/topic",
    response_model=KnowledgeSourceResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_topic(
    request: CreateTopicRequest,
    user=Depends(get_current_user),
    repository=Depends(get_repository),
):

    service = KnowledgeEngineService(repository)

    return await service.create_topic(
        user_id=user.id,
        title=request.title,
        subject=request.subject,
        topic_description=request.topic_description,
    )


@router.post(
    "/upload",
    response_model=KnowledgeSourceResponse,
    status_code=status.HTTP_201_CREATED,
)
async def upload_document(
    file: UploadFile = File(...),
    user=Depends(get_current_user),
    repository=Depends(get_repository),
):

    service = KnowledgeEngineService(repository)

    return await service.upload_document(
        user_id=user.id,
        file=file,
    )
