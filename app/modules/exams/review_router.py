from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from app.modules.auth.dependencies import (
    get_current_user,
)

from app.modules.exams.review import (
    ExamReviewService,
)

from app.modules.exams.dependencies import (
    get_review_service,
)

from app.modules.exams.repository import (
    ExamRepository,
)

from app.modules.exams.dependencies import (
    get_exam_repository,
)


router = APIRouter(
    prefix="/exams",
    tags=[
        "Exam Review",
    ],
)



# ============================================================
# GENERATE AI REVIEW
# ============================================================


@router.post(
    "/{session_id}/review",
)
async def generate_review(
    session_id: UUID,
    current_user=Depends(
        get_current_user,
    ),
    repository: ExamRepository = Depends(
        get_exam_repository,
    ),
    service: ExamReviewService = Depends(
        get_review_service,
    ),
):

    try:

        session = await repository.get_session(
            session_id,
        )


        if session is None:

            raise HTTPException(
                status_code=404,
                detail=(
                    "Exam session not found."
                ),
            )



        review = await service.generate_review(
            session,
        )


        return {

            "success": True,

            "review": {

                "overall_feedback": (
                    review.overall_feedback
                ),

                "strengths": (
                    review.strengths
                ),

                "weaknesses": (
                    review.weaknesses
                ),

                "recommendations": (
                    review.recommendations
                ),

                "study_plan": (
                    review.study_plan
                ),

                "topic_analysis": (
                    review.topic_analysis
                ),

                "confidence_score": (
                    review.confidence_score
                ),
            },
        }


    except HTTPException:

        raise


    except Exception as exc:

        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc
