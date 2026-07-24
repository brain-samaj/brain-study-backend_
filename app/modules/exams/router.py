from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status

from app.modules.auth.dependencies import get_current_user

from app.modules.exams.dependencies import (
    get_autosave_service,
    get_exam_service,
    get_grading_service,
)

from app.modules.exams.autosave import (
    ExamAutosaveService,
)

from app.modules.exams.grading import (
    ExamGradingService,
)

from app.modules.exams.schemas import (
    CreateExamRequest,
    ExamSessionResponse,
    ObjectiveAnswerRequest,
    TheoryAnswerRequest,
)

from app.modules.exams.service import (
    ExamService,
)


router = APIRouter(
    prefix="/exams",
    tags=[
        "Exams"
    ],
)


# ============================================================
# CREATE EXAM
# ============================================================


@router.post(
    "",
    response_model=ExamSessionResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_exam(
    material_id: UUID,
    request: CreateExamRequest,
    current_user=Depends(
        get_current_user,
    ),
    service: ExamService = Depends(
        get_exam_service,
    ),
):

    try:

        exam = await service.create_exam(
            owner_id=current_user.id,
            material_id=material_id,
            request=request,
        )

        return exam


    except Exception as exc:

        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc



# ============================================================
# GET EXAM
# ============================================================


@router.get(
    "/{session_id}",
    response_model=ExamSessionResponse,
)
async def get_exam(
    session_id: UUID,
    current_user=Depends(
        get_current_user,
    ),
    service: ExamService = Depends(
        get_exam_service,
    ),
):

    try:

        return await service.get_exam(
            session_id,
        )


    except Exception as exc:

        raise HTTPException(
            status_code=404,
            detail=str(exc),
        ) from exc


# ============================================================
# AUTOSAVE OBJECTIVE ANSWER
# ============================================================


@router.post(
    "/{session_id}/answers/{question_id}/objective",
)
async def save_objective_answer(
    session_id: UUID,
    question_id: UUID,
    payload: ObjectiveAnswerRequest,
    current_user=Depends(
        get_current_user,
    ),
    service: ExamAutosaveService = Depends(
        get_autosave_service,
    ),
):

    try:

        answer = await service.autosave_objective(
            session_id=session_id,
            question_id=question_id,
            selected_option=payload.selected_option,
        )


        return {
            "success": True,
            "answer_id": answer.id,
            "saved_at": answer.updated_at,
        }


    except Exception as exc:

        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc



# ============================================================
# AUTOSAVE THEORY ANSWER
# ============================================================


@router.post(
    "/{session_id}/answers/{question_id}/theory",
)
async def save_theory_answer(
    session_id: UUID,
    question_id: UUID,
    payload: TheoryAnswerRequest,
    current_user=Depends(
        get_current_user,
    ),
    service: ExamAutosaveService = Depends(
        get_autosave_service,
    ),
):

    try:

        answer = await service.autosave_theory(
            session_id=session_id,
            question_id=question_id,
            text_answer=payload.text_answer,
        )


        return {
            "success": True,
            "answer_id": answer.id,
            "saved_at": answer.updated_at,
        }


    except Exception as exc:

        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc



# ============================================================
# SUBMIT EXAM
# ============================================================


@router.post(
    "/{session_id}/submit",
)
async def submit_exam(
    session_id: UUID,
    current_user=Depends(
        get_current_user,
    ),
    grading_service: ExamGradingService = Depends(
        get_grading_service,
    ),
):

    try:

        result = await grading_service.grade_session(
            session_id=session_id,
        )


        return {
            "success": True,
            "session_id": result.session_id,
            "score": result.score,
            "percentage": result.percentage,
            "message": (
                "Exam submitted and graded successfully."
            ),
        }


    except Exception as exc:

        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc


# ============================================================
# GET EXAM TIMER
# ============================================================


@router.get(
    "/{session_id}/timer",
)
async def exam_timer(
    session_id: UUID,
    current_user=Depends(
        get_current_user,
    ),
):

    from app.modules.exams.timer import (
        ExamTimerService,
    )

    from app.modules.exams.dependencies import (
        get_exam_repository,
    )


    repository = await get_exam_repository()


    service = ExamTimerService(
        repository=repository,
    )


    try:

        return await service.get_remaining_time(
            session_id,
        )


    except Exception as exc:

        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc



# ============================================================
# GET EXAM RESULT
# ============================================================


@router.get(
    "/{session_id}/result",
)
async def get_exam_result(
    session_id: UUID,
    current_user=Depends(
        get_current_user,
    ),
):

    from app.modules.exams.dependencies import (
        get_exam_repository,
    )


    repository = await get_exam_repository()


    result = await repository.get_result(
        session_id,
    )


    if result is None:

        raise HTTPException(
            status_code=404,
            detail="Result not found.",
        )


    return {
        "id": result.id,
        "score": result.score,
        "total_marks": result.total_marks,
        "percentage": result.percentage,
        "objective_score": result.objective_score,
        "theory_score": result.theory_score,
        "strengths": result.strengths,
        "weaknesses": result.weaknesses,
        "recommendations": result.recommendations,
        "ai_summary": result.ai_summary,
    }



# ============================================================
# GET EXAM HISTORY
# ============================================================


@router.get(
    "/history",
)
async def exam_history(
    limit: int = 20,
    offset: int = 0,
    current_user=Depends(
        get_current_user,
    ),
):

    from app.modules.exams.history import (
        ExamHistoryService,
    )

    from app.database.async_session import (
        get_async_session,
    )

    async for session in get_async_session():

        service = ExamHistoryService(
            session,
        )

        return await service.get_history(
            owner_id=current_user.id,
            limit=limit,
            offset=offset,
        )



# ============================================================
# HEALTH CHECK
# ============================================================


@router.get(
    "/health",
)
async def exam_health():

    return {
        "module": "exams",
        "status": "healthy",
    }
