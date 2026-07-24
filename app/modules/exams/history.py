from __future__ import annotations

from uuid import UUID

from sqlalchemy import desc
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.exams.models import ExamSession
from app.modules.exams.result_models import ExamResult


class ExamHistoryService:
    """
    Exam History Service.

    Responsibilities
    ----------------
    - Retrieve previous exams.
    - Provide student timeline.
    - Support pagination.
    - Prepare analytics data.

    History is read-only.
    """


    def __init__(
        self,
        session: AsyncSession,
    ) -> None:

        self._session = session



    async def get_history(
        self,
        *,
        owner_id: UUID,
        limit: int = 20,
        offset: int = 0,
    ) -> list[dict]:

        query = (
            select(
                ExamSession,
                ExamResult,
            )
            .join(
                ExamResult,
                ExamResult.session_id
                ==
                ExamSession.id,
                isouter=True,
            )
            .where(
                ExamSession.owner_id
                ==
                owner_id,
            )
            .order_by(
                desc(
                    ExamSession.created_at
                )
            )
            .limit(
                limit
            )
            .offset(
                offset
            )
        )


        result = await self._session.execute(
            query
        )


        records = []


        for session, exam_result in result.all():

            records.append(
                {
                    "session_id": session.id,

                    "material_id": (
                        session.material_id
                    ),

                    "exam_type": (
                        session.exam_type
                    ),

                    "difficulty": (
                        session.difficulty
                    ),

                    "status": (
                        session.status
                    ),

                    "score": (
                        exam_result.score
                        if exam_result
                        else 0
                    ),

                    "total_marks": (
                        exam_result.total_marks
                        if exam_result
                        else session.total_marks
                    ),

                    "percentage": (
                        exam_result.percentage
                        if exam_result
                        else 0
                    ),

                    "total_questions": (
                        session.total_questions
                    ),

                    "duration_minutes": (
                        session.duration_minutes
                    ),

                    "created_at": (
                        session.created_at
                    ),

                    "submitted_at": (
                        session.submitted_at
                    ),
                }
            )


        return records



    async def get_attempt_count(
        self,
        *,
        owner_id: UUID,
    ) -> int:

        result = await self._session.execute(
            select(
                ExamSession.id
            )
            .where(
                ExamSession.owner_id
                ==
                owner_id
            )
        )


        return len(
            result.scalars().all()
        )
