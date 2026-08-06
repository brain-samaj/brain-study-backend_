from __future__ import annotations

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.exams.models import ExamAnswer
from app.modules.exams.models import ExamQuestion


class ExamReviewService:
    """
    Review service.

    Returns every question together with:

    - student's answer
    - correct answer
    - marks
    - obtained marks
    - explanation
    """

    def __init__(
        self,
        session: AsyncSession,
    ) -> None:
        self._session = session

    async def get_review(
        self,
        *,
        session_id: UUID,
    ) -> list[dict]:

        query = (
            select(
                ExamQuestion,
                ExamAnswer,
            )
            .outerjoin(
                ExamAnswer,
                (
                    (ExamAnswer.question_id == ExamQuestion.id)
                    &
                    (ExamAnswer.session_id == session_id)
                ),
            )
            .where(
                ExamQuestion.session_id == session_id
            )
            .order_by(
                ExamQuestion.question_number
            )
        )

        result = await self._session.execute(query)

        review: list[dict] = []

        for question, answer in result.all():

            if question.question_type.value == "objective":
                student_answer = (
                    answer.selected_option
                    if answer
                    else None
                )
            else:
                student_answer = (
                    answer.text_answer
                    if answer
                    else None
                )

            review.append(
                {
                    "question_id": str(question.id),
                    "question_number": question.question_number,
                    "question": question.question,
                    "question_type": question.question_type.value,
                    "student_answer": student_answer,
                    "correct_answer": question.correct_answer,
                    "marks": question.marks,
                    "obtained_marks": (
                        answer.awarded_marks
                        if answer
                        else 0
                    ),
                    "explanation": question.explanation,
                }
            )

        return review
