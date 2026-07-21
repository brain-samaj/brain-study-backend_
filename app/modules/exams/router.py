from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter
from fastapi import BackgroundTasks
from fastapi import Depends
from fastapi import File
from fastapi import Form
from fastapi import HTTPException
from fastapi import UploadFile
from fastapi import status

from sqlalchemy.orm import Session

from app.database.session import get_db

from app.modules.auth.dependencies import get_current_user
from app.modules.auth.models import User

from app.modules.exams.repository import ExamRepository
from app.modules.exams.service import ExamService

from app.modules.exams.schemas import (
    CreateExamRequest,
    ExamSessionResponse,
    SubmitObjectiveRequest,
    SubmitTheoryRequest,
    ExamResultResponse,
    ExamHistoryResponse,
)

from app.ai.services.theory_marker import TheoryMarker
from app.ai.services.exam_generator import ExamGenerator
from app.ai.services.ocr import OCRService


router = APIRouter(
    prefix="/exams",
    tags=["Exams"],
)


def get_exam_repository(
    db: Session = Depends(get_db),
) -> ExamRepository:
    return ExamRepository(db)


def get_exam_service(
    repository: ExamRepository = Depends(get_exam_repository),
) -> ExamService:

    return ExamService(
        repository=repository,
        ai_marker=TheoryMarker(),
    )


###############################################################
#
# CREATE EXAM
#
###############################################################


@router.post(
    "/create",
    response_model=ExamSessionResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_exam(
    payload: CreateExamRequest,
    current_user: User = Depends(get_current_user),
    repository: ExamRepository = Depends(
        get_exam_repository,
    ),
):

    generator = ExamGenerator()

    exam = await generator.generate_exam(
        user=current_user,
        payload=payload,
    )

    session = repository.create_session(
        exam.session,
    )

    repository.create_questions(
        exam.questions,
    )

    return session


###############################################################
#
# GET EXAM SESSION
#
###############################################################


@router.get(
    "/{session_id}",
    response_model=ExamSessionResponse,
)
async def get_exam_session(
    session_id: UUID,
    current_user: User = Depends(get_current_user),
    repository: ExamRepository = Depends(
        get_exam_repository,
    ),
):

    session = repository.get_session(
        session_id,
    )

    if session is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Exam session not found.",
        )

    if session.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied.",
        )

    return session


###############################################################
#
# GET EXAM QUESTIONS
#
###############################################################


@router.get(
    "/{session_id}/questions",
)
async def get_exam_questions(
    session_id: UUID,
    current_user: User = Depends(get_current_user),
    repository: ExamRepository = Depends(
        get_exam_repository,
    ),
):

    session = repository.get_session(
        session_id,
    )

    if session is None:
        raise HTTPException(
            status_code=404,
            detail="Exam not found.",
        )

    if session.user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Permission denied.",
        )

    return repository.get_questions(
        session_id,
    )


###############################################################
#
# AUTO SAVE OBJECTIVE ANSWER
#
###############################################################


@router.post(
    "/{session_id}/autosave/objective",
)
async def autosave_objective_answer(
    session_id: UUID,
    payload: SubmitObjectiveRequest,
    current_user: User = Depends(get_current_user),
    service: ExamService = Depends(
        get_exam_service,
    ),
):

    await service.autosave_objective(
        session_id=session_id,
        answers=payload.answers,
    )

    return {
        "message": "Answer saved.",
    }


###############################################################
#
# AUTO SAVE THEORY ANSWER
#
###############################################################


@router.post(
    "/{session_id}/autosave/theory",
)
async def autosave_theory_answer(
    session_id: UUID,
    payload: SubmitTheoryRequest,
    current_user: User = Depends(get_current_user),
    service: ExamService = Depends(
        get_exam_service,
    ),
):

    await service.autosave_theory(
        session_id=session_id,
        answers=payload.answers,
    )

    return {
        "message": "Answer saved.",
    }


###############################################################
#
# SAVE SINGLE THEORY ANSWER
#
###############################################################


@router.post(
    "/{session_id}/answer",
)
async def save_theory_answer(
    session_id: UUID,
    question_number: int = Form(...),
    answer: str = Form(...),
    current_user: User = Depends(get_current_user),
    service: ExamService = Depends(
        get_exam_service,
    ),
):

    await service.save_single_theory_answer(
        session_id=session_id,
        question_number=question_number,
        answer=answer,
    )

    return {
        "message": "Saved successfully.",
    }



###############################################################
#
# UPLOAD HANDWRITTEN THEORY ANSWER
#
###############################################################


@router.post(
    "/{session_id}/upload-answer",
)
async def upload_handwritten_answer(
    session_id: UUID,
    background_tasks: BackgroundTasks,
    question_number: int = Form(...),
    image: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    service: ExamService = Depends(
        get_exam_service,
    ),
):

    if image.content_type is None:
        raise HTTPException(
            status_code=400,
            detail="Invalid image.",
        )

    if not image.content_type.startswith("image/"):
        raise HTTPException(
            status_code=400,
            detail="Only image uploads are allowed.",
        )

    ocr = OCRService()

    extracted_text = await ocr.extract_text(
        image=image,
    )

    await service.save_single_theory_answer(
        session_id=session_id,
        question_number=question_number,
        answer=extracted_text,
    )

    background_tasks.add_task(
        service.process_theory_answer,
        session_id=session_id,
        question_number=question_number,
    )

    return {
        "message": "Image uploaded successfully.",
        "ocr_text": extracted_text,
    }


###############################################################
#
# SUBMIT OBJECTIVE EXAM
#
###############################################################


@router.post(
    "/{session_id}/submit-objective",
    response_model=ExamResultResponse,
)
async def submit_objective_exam(
    session_id: UUID,
    payload: SubmitObjectiveRequest,
    current_user: User = Depends(get_current_user),
    service: ExamService = Depends(
        get_exam_service,
    ),
):

    return await service.submit_objective_exam(
        session_id=session_id,
        student_answers=payload.answers,
    )


###############################################################
#
# SUBMIT THEORY EXAM
#
###############################################################


@router.post(
    "/{session_id}/submit-theory",
    response_model=ExamResultResponse,
)
async def submit_theory_exam(
    session_id: UUID,
    payload: SubmitTheoryRequest,
    current_user: User = Depends(get_current_user),
    service: ExamService = Depends(
        get_exam_service,
    ),
):

    return await service.submit_theory_exam(
        session_id=session_id,
        submitted_answers=payload.answers,
    )


###############################################################
#
# SUBMIT COMPLETE EXAM
#
###############################################################


@router.post(
    "/{session_id}/submit",
    response_model=ExamResultResponse,
)
async def submit_complete_exam(
    session_id: UUID,
    current_user: User = Depends(get_current_user),
    service: ExamService = Depends(
        get_exam_service,
    ),
):

    return await service.submit_complete_exam(
        session_id=session_id,
    )



###############################################################
#
# GET EXAM RESULT
#
###############################################################


@router.get(
    "/{session_id}/result",
    response_model=ExamResultResponse,
)
async def get_exam_result(
    session_id: UUID,
    current_user: User = Depends(get_current_user),
    repository: ExamRepository = Depends(
        get_exam_repository,
    ),
):

    session = repository.get_session(session_id)

    if session is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Exam session not found.",
        )

    if session.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied.",
        )

    result = repository.get_result(session_id)

    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Exam result not available.",
        )

    return result


###############################################################
#
# EXAM HISTORY
#
###############################################################


@router.get(
    "/history",
    response_model=list[ExamHistoryResponse],
)
async def exam_history(
    current_user: User = Depends(get_current_user),
    repository: ExamRepository = Depends(
        get_exam_repository,
    ),
):

    return repository.get_user_exam_history(
        current_user.id,
    )


###############################################################
#
# REVIEW PREVIOUS EXAM
#
###############################################################


@router.get(
    "/{session_id}/review",
)
async def review_exam(
    session_id: UUID,
    current_user: User = Depends(get_current_user),
    repository: ExamRepository = Depends(
        get_exam_repository,
    ),
):

    session = repository.get_session(session_id)

    if session is None:
        raise HTTPException(
            status_code=404,
            detail="Exam session not found.",
        )

    if session.user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Access denied.",
        )

    result = repository.get_result(
        session_id,
    )

    submissions = repository.get_session_submissions(
        session_id,
    )

    questions = repository.get_questions(
        session_id,
    )

    return {
        "session": session,
        "result": result,
        "questions": questions,
        "submissions": submissions,
    }


###############################################################
#
# REGENERATE EXAM
#
###############################################################


@router.post(
    "/{session_id}/regenerate",
)
async def regenerate_exam(
    session_id: UUID,
    current_user: User = Depends(get_current_user),
    service: ExamService = Depends(
        get_exam_service,
    ),
):

    return await service.regenerate_exam(
        session_id=session_id,
    )


###############################################################
#
# DELETE EXAM SESSION
#
###############################################################


@router.delete(
    "/{session_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_exam(
    session_id: UUID,
    current_user: User = Depends(get_current_user),
    repository: ExamRepository = Depends(
        get_exam_repository,
    ),
):

    session = repository.get_session(
        session_id,
    )

    if session is None:
        raise HTTPException(
            status_code=404,
            detail="Exam session not found.",
        )

    if session.user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Access denied.",
        )

    repository.delete_session(
        session,
    )

    return None


###############################################################
#
# HEALTH CHECK
#
###############################################################


@router.get(
    "/health",
)
async def health():

    return {
        "status": "healthy",
        "module": "exam-engine",
    }
