from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter
from fastapi import Depends
from fastapi import File
from fastapi import Form
from fastapi import HTTPException
from fastapi import Query
from fastapi import UploadFile
from fastapi import status

from sqlalchemy.ext.asyncio import AsyncSession

from app.ai.client import AIClient

from app.database.async_session import get_async_db

from app.modules.auth.dependencies import get_current_user

from app.modules.auth.models import User

from app.modules.knowledge_engine.repository import (
    KnowledgeRepository,
)

from app.modules.knowledge_engine.service import (
    KnowledgeEngineService,
)

from app.modules.study_materials.repository import (
    StudyMaterialRepository,
)

from app.modules.study_materials.schemas import (
    DeleteStudyMaterialResponse,
    StudyMaterialListResponse,
    StudyMaterialResponse,
)

from app.modules.study_materials.service import (
    StudyMaterialService,
)

router = APIRouter(
    prefix="/study-materials",
    tags=["Study Materials"],
)


def get_service(
    db: AsyncSession = Depends(get_db),
) -> StudyMaterialService:

    material_repository = StudyMaterialRepository(db)

    knowledge_service = KnowledgeEngineService(
        repository=KnowledgeRepository(db),
        study_material_repository=material_repository,
        ai_client=AIClient(),
    )

    return StudyMaterialService(
        repository=material_repository,
        knowledge_service=knowledge_service,
        ai_client=AIClient(),
    )

@router.post(
    "/upload",
    response_model=StudyMaterialResponse,
    status_code=status.HTTP_201_CREATED,
)
async def upload_material(
    title: str = Form(...),
    description: str | None = Form(None),
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    service: StudyMaterialService = Depends(get_service),
) -> StudyMaterialResponse:
    """
    Upload a study material.

    Supported formats

    • PDF

    • DOCX

    • PPTX

    • TXT

    • Markdown

    • PNG

    • JPG

    • JPEG

    • BMP

    • GIF

    • WEBP
    """

    material = await service.upload(
        current_user=current_user,
        title=title,
        description=description,
        file=file,
    )

    return StudyMaterialResponse.model_validate(
        material,
    )


@router.post(
    "/topic",
    response_model=StudyMaterialResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_topic_material(
    title: str = Form(...),
    description: str = Form(...),
    current_user: User = Depends(get_current_user),
    service: StudyMaterialService = Depends(get_service),
) -> StudyMaterialResponse:
    """
    Create a study material without uploading a file.

    Useful for:

    • AI-generated notes

    • Typed lecture notes

    • Manual topics

    • Research ideas
    """

    material = await service.create_from_topic(
        current_user=current_user,
        title=title,
        description=description,
    )

    return StudyMaterialResponse.model_validate(
        material,
    )

@router.get(
    "/",
    response_model=StudyMaterialListResponse,
)
async def list_study_materials(
    skip: int = Query(
        0,
        ge=0,
    ),
    limit: int = Query(
        20,
        ge=1,
        le=100,
    ),
    current_user: User = Depends(get_current_user),
    service: StudyMaterialService = Depends(get_service),
) -> StudyMaterialListResponse:
    """
    List all study materials belonging to the current user.
    """

    items = await service.list(
        current_user=current_user,
        skip=skip,
        limit=limit,
    )

    return StudyMaterialListResponse(
        items=[
            StudyMaterialResponse.model_validate(item)
            for item in items
        ],
        total=len(items),
    )


@router.get(
    "/{material_id}",
    response_model=StudyMaterialResponse,
)
async def get_study_material(
    material_id: UUID,
    current_user: User = Depends(get_current_user),
    service: StudyMaterialService = Depends(get_service),
) -> StudyMaterialResponse:
    """
    Retrieve a single study material.
    """

    material = await service.get(
        material_id=material_id,
        current_user=current_user,
    )

    return StudyMaterialResponse.model_validate(
        material,
    )


from app.modules.study_materials.schemas import (
    StudyMaterialUpdate,
)


@router.patch(
    "/{material_id}",
    response_model=StudyMaterialResponse,
)
async def update_study_material(
    material_id: UUID,
    payload: StudyMaterialUpdate,
    current_user: User = Depends(get_current_user),
    service: StudyMaterialService = Depends(get_service),
) -> StudyMaterialResponse:
    """
    Update a study material.
    """

    material = await service.update(
        material_id=material_id,
        current_user=current_user,
        payload=payload,
    )

    return StudyMaterialResponse.model_validate(
        material,
    )


@router.post(
    "/{material_id}/archive",
    status_code=status.HTTP_200_OK,
)
async def archive_study_material(
    material_id: UUID,
    current_user: User = Depends(get_current_user),
    service: StudyMaterialService = Depends(get_service),
):
    """
    Archive a study material.
    """

    await service.archive(
        material_id=material_id,
        current_user=current_user,
    )

    return {
        "success": True,
        "message": "Study material archived successfully.",
    }


@router.post(
    "/{material_id}/reprocess",
    response_model=StudyMaterialResponse,
)
async def reprocess_study_material(
    material_id: UUID,
    current_user: User = Depends(get_current_user),
    service: StudyMaterialService = Depends(get_service),
) -> StudyMaterialResponse:
    """
    Rebuild AI knowledge from the study material.
    """

    material = await service.reprocess(
        material_id=material_id,
        current_user=current_user,
    )

    return StudyMaterialResponse.model_validate(
        material,
    )


@router.delete(
    "/{material_id}",
    response_model=DeleteStudyMaterialResponse,
)
async def delete_study_material(
    material_id: UUID,
    current_user: User = Depends(get_current_user),
    service: StudyMaterialService = Depends(get_service),
) -> DeleteStudyMaterialResponse:
    """
    Permanently delete a study material.
    """

    await service.delete(
        material_id=material_id,
        current_user=current_user,
    )

    return DeleteStudyMaterialResponse(
        success=True,
        message="Study material deleted successfully.",
    )

