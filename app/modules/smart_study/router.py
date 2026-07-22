from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status

from sqlalchemy.orm import Session

from app.database.session import get_db
from app.modules.auth.dependencies import get_current_user
from app.modules.auth.models import User

from app.modules.knowledge_engine.repository import (
    KnowledgeRepository,
)

from app.modules.smart_study.repository import (
    SmartStudyRepository,
)

from app.modules.smart_study.service import (
    SmartStudyService,
)

from app.modules.smart_study.schemas import (
    StartSmartStudyRequest,
    SubmitAnswerRequest,
)

router = APIRouter(
    prefix="/smart-study",
    tags=["Smart Study"],
)


def get_service(
    db: Session = Depends(get_db),
) -> SmartStudyService:

    repository = SmartStudyRepository(db)

    knowledge_repository = KnowledgeRepository(db)

    return SmartStudyService(
        repository=repository,
        knowledge_repository=knowledge_repository,
    )


@router.post(
    "/session",
    status_code=status.HTTP_201_CREATED,
)
def start_session(
    request: StartSmartStudyRequest,
    current_user: User = Depends(get_current_user),
    service: SmartStudyService = Depends(get_service),
):

    try:

        return service.start_session(
            user_id=current_user.id,
            source_id=request.source_id,
        )

    except ValueError as exc:

        raise HTTPException(
            status_code=400,
            detail=str(exc),
        )


@router.get(
    "/{session_id}/next",
)
async def next_question(
    session_id: UUID,
    current_user: User = Depends(get_current_user),
    service: SmartStudyService = Depends(get_service),
):

    try:

        return await service.next_question(
            session_id=session_id,
        )

    except ValueError as exc:

        raise HTTPException(
            status_code=404,
            detail=str(exc),
        )


@router.post(
    "/{session_id}/answer",
)
def submit_answer(
    session_id: UUID,
    request: SubmitAnswerRequest,
    current_user: User = Depends(get_current_user),
    service: SmartStudyService = Depends(get_service),
):

    try:

        return service.submit_answer(
            session_id=session_id,
            question=request.question,
            selected_answer=request.selected_answer,
        )

    except ValueError as exc:

        raise HTTPException(
            status_code=400,
            detail=str(exc),
        )


@router.get(
    "/{session_id}/progress",
)
def progress(
    session_id: UUID,
    current_user: User = Depends(get_current_user),
    service: SmartStudyService = Depends(get_service),
):

    session = service.repository.get_session(
        session_id,
    )

    if session is None:

        raise HTTPException(
            status_code=404,
            detail="Study session not found.",
        )

    return {
        "session_id": session.id,
        "total_questions": session.total_questions,
        "correct_answers": session.correct_answers,
        "wrong_answers": session.wrong_answers,
        "mastery_score": session.mastery_score,
        "difficulty": session.difficulty_level,
        "current_streak": session.current_streak,
        "longest_streak": session.longest_streak,
        "completed": session.is_completed,
    }

