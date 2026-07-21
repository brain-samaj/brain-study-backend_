from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter
from fastapi import Depends
from fastapi import File
from fastapi import Form
from fastapi import UploadFile
from fastapi import status
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.modules.auth.dependencies import get_current_user
from app.modules.auth.models import User
from app.modules.study_materials.repository import StudyMaterialRepository
from app.modules.study_materials.schemas import (
    DeleteStudyMaterialResponse,
    StudyMaterialCreate,
    StudyMaterialListResponse,
    StudyMaterialResponse,
    StudyMaterialUpdate,
)
from app.modules.study_materials.service import StudyMaterialService

router = APIRouter(
    prefix="/study-materials",
    tags=["Study Materials"],
)


def get_service(
    db: Session = Depends(get_db),
) -> StudyMaterialService:
    return StudyMaterialService(
        StudyMaterialRepository(db),
    )


@router.post(
    "/upload",
    response_model=StudyMaterialResponse,
    status_code=status.HTTP_201_CREATED,
)
async def upload_study_material(
    title: str = Form(...),
    description: str | None = Form(None),
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    service: StudyMaterialService = Depends(get_service),
):
    payload = StudyMaterialCreate(
        title=title,
        description=description,
    )

    return service.upload(
        current_user=current_user,
        metadata=payload,
        file=file,
    )


@router.get(
    "",
    response_model=StudyMaterialListResponse,
)
def list_study_materials(
    skip: int = 0,
    limit: int = 20,
    current_user: User = Depends(get_current_user),
    service: StudyMaterialService = Depends(get_service),
):
    items = service.list(
        current_user=current_user,
        skip=skip,
        limit=limit,
    )

    return {
        "total": len(items),
        "items": items,
    }


@router.get(
    "/{material_id}",
    response_model=StudyMaterialResponse,
)
def get_study_material(
    material_id: UUID,
    current_user: User = Depends(get_current_user),
    service: StudyMaterialService = Depends(get_service),
):
    return service.get(
        material_id=material_id,
        current_user=current_user,
    )


@router.patch(
    "/{material_id}",
    response_model=StudyMaterialResponse,
)
def update_study_material(
    material_id: UUID,
    payload: StudyMaterialUpdate,
    current_user: User = Depends(get_current_user),
    service: StudyMaterialService = Depends(get_service),
):
    return service.update(
        material_id=material_id,
        payload=payload,
        current_user=current_user,
    )


@router.delete(
    "/{material_id}",
    response_model=DeleteStudyMaterialResponse,
)
def delete_study_material(
    material_id: UUID,
    current_user: User = Depends(get_current_user),
    service: StudyMaterialService = Depends(get_service),
):
    service.delete(
        material_id=material_id,
        current_user=current_user,
    )

    return {
        "success": True,
        "message": "Study material deleted successfully.",
    }
