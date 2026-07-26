from __future__ import annotations

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.modules.exams.models import ExamAnswer
from app.modules.exams.models import ExamQuestion
from app.modules.exams.models import ExamSession
from app.modules.exams.result_models import ExamResult
from app.modules.exams.submission_models import ExamSubmission


class ExamRepository:
    """
    Async repository layer for Exam module.

    Responsibilities
    ----------------
    - Database access only.
    - No business logic.
    - No AI logic.
    - No validation logic.

    Service layer decides what should happen.
    Repository only communicates with PostgreSQL.
    """

    def __init__(
        self,
        session: AsyncSession,
    ) -> None:

        self.session = session


    # ========================================================
    # SESSION
    # ========================================================

    async def get_session(
        self,
        session_id: UUID,
    ) -> ExamSession | None:

        result = await self.session.execute(
            select(
                ExamSession
            )
            .options(
                selectinload(
                    ExamSession.questions
                ),
                selectinload(
                    ExamSession.answers
                ),
            )
            .where(
                ExamSession.id == session_id
            )
        )

        return result.scalar_one_or_none()



    async def create_session(
        self,
        exam_session: ExamSession,
    ) -> ExamSession:

        self.session.add(
            exam_session
        )

        await self.session.flush()

        return exam_session



    async def update_session(
        self,
        exam_session: ExamSession,
    ) -> ExamSession:

        self.session.add(
            exam_session
        )

        await self.session.flush()

        return exam_session



    # ========================================================
    # QUESTIONS
    # ========================================================


    async def create_question(
        self,
        question: ExamQuestion,
    ) -> ExamQuestion:

        self.session.add(
            question
        )

        await self.session.flush()

        return question



    async def get_question(
        self,
        question_id: UUID,
    ) -> ExamQuestion | None:

        result = await self.session.execute(
            select(
                ExamQuestion
            )
            .where(
                ExamQuestion.id == question_id
            )
        )

        return result.scalar_one_or_none()



    # ========================================================
    # ANSWERS
    # ========================================================


    async def get_answer(
        self,
        *,
        session_id: UUID,
        question_id: UUID,
    ) -> ExamAnswer | None:

        result = await self.session.execute(
            select(
                ExamAnswer
            )
            .options(
                selectinload(
                    ExamAnswer.attachments
                )
            )
            .where(
                ExamAnswer.session_id
                ==
                session_id
            )
            .where(
                ExamAnswer.question_id
                ==
                question_id
            )
        )

        return result.scalar_one_or_none()



    async def create_answer(
        self,
        *,
        session_id: UUID,
        question_id: UUID,
    ) -> ExamAnswer:

        answer = ExamAnswer(
            session_id=session_id,
            question_id=question_id,
        )

        self.session.add(
            answer
        )

        await self.session.flush()

        return answer



    async def update_answer(
        self,
        answer: ExamAnswer,
    ) -> ExamAnswer:

        self.session.add(
            answer
        )

        await self.session.flush()

        return answer



    # ========================================================
    # SUBMISSIONS
    # ========================================================


    async def create_submission(
        self,
        submission: ExamSubmission,
    ) -> ExamSubmission:

        self.session.add(
            submission
        )

        await self.session.flush()

        return submission



    async def get_submission(
        self,
        session_id: UUID,
    ) -> ExamSubmission | None:

        result = await self.session.execute(
            select(
                ExamSubmission
            )
            .where(
                ExamSubmission.session_id
                ==
                session_id
            )
        )

        return result.scalar_one_or_none()



    # ========================================================
    # RESULTS
    # ========================================================


    async def create_result(
        self,
        result: ExamResult,
    ) -> ExamResult:

        self.session.add(
            result
        )

        await self.session.flush()

        return result



    async def get_result(
        self,
        session_id: UUID,
    ) -> ExamResult | None:

        result = await self.session.execute(
            select(
                ExamResult
            )
            .where(
                ExamResult.session_id
                ==
                session_id
            )
        )

        return result.scalar_one_or_none()



    # ========================================================
    # TRANSACTION
    # ========================================================


    async def commit(
        self,
    ) -> None:

        await self.session.commit()



    async def rollback(
        self,
    ) -> None:

        await self.session.rollback()
