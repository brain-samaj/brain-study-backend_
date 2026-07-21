from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.dependencies.auth import get_current_user
from app.modules.materials.repository import MaterialRepository
from app.modules.smart_study.service import SmartStudyService

router = APIRouter(
    prefix="/smart-study",
    tags=["Smart Study"],
)

@router.post(
    "/{study_material_id}/start",
)
async def start_session(
    study_material_id: UUID,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):

    material = MaterialRepository(db).get_by_id(
        study_material_id,
    )

    if material is None:
        raise HTTPException(
            status_code=404,
            detail="Study material not found.",
        )

    service = SmartStudyService(db)

    return await service.next_question(
        user=current_user,
        study_material=material,
        analysis=material.analysis,
    )

from pydantic import BaseModel


class SubmitAnswerRequest(BaseModel):

    session_id: UUID

    question_id: UUID

    answer: str

@router.post("/submit")
async def submit_answer(
    payload: SubmitAnswerRequest,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):

    service = SmartStudyService(db)

    return await service.submit_answer(
        session_id=payload.session_id,
        question_id=payload.question_id,
        student_answer=payload.answer,
        user=current_user,
    )

@router.get(
    "/dashboard/{study_material_id}",
)
def dashboard(
    study_material_id: UUID,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):

    service = SmartStudyService(db)

    return service.dashboard(
        user_id=current_user.id,
        study_material_id=study_material_id,
    )
