from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.async_session import get_async_db
from app.modules.auth.dependencies import get_current_user
from app.modules.auth.models import User
from app.modules.study_materials.repository import StudyMaterialRepository


router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"],
)


@router.get("/")
async def get_dashboard(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    material_repository = StudyMaterialRepository(db)

    materials = await material_repository.list_for_owner(
        owner_id=current_user.id,
        skip=0,
        limit=5,
    )

    total_materials = await material_repository.count_for_owner(
        current_user.id,
    )

    return {
        "stats": {
            "materials": total_materials,
            "study_kits": 0,
            "flashcards": 0,
            "progress": 0,
        },
        "recent_materials": [
            {
                "id": str(material.id),
                "title": material.title,
                "created_at": material.created_at,
            }
            for material in materials
        ],
    }

