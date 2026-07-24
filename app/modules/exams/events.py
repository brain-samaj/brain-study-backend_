from __future__ import annotations

"""
Exam Background Event Handlers.

Responsible for asynchronous workflows:

- Expired exam detection
- Auto submission
- OCR queue triggers
- AI grading queue triggers
- Review generation triggers

The API remains fast because heavy
operations happen asynchronously.
"""


from uuid import UUID


from app.modules.exams.models import (
    ExamStatus,
)

from app.modules.exams.repository import (
    ExamRepository,
)



class ExamEventService:
    """
    Handles exam lifecycle events.
    """


    def __init__(
        self,
        *,
        repository: ExamRepository,
    ) -> None:

        self._repository = repository



    async def handle_expired_exam(
        self,
        session_id: UUID,
    ) -> None:
        """
        Automatically expire unfinished exams.
        """

        session = await (
            self._repository
            .get_session(
                session_id,
            )
        )


        if session is None:

            return



        if session.status in {
            ExamStatus.GRADED,
            ExamStatus.SUBMITTED,
        }:

            return



        session.status = (
            ExamStatus.EXPIRED
        )


        await self._repository.update_session(
            session,
        )


        await self._repository.commit()



    async def queue_grading(
        self,
        session_id: UUID,
    ) -> dict:
        """
        Placeholder for Celery/RQ/
        background worker integration.
        """

        return {
            "task": "grading",
            "session_id": str(
                session_id
            ),
            "status": "queued",
        }



    async def queue_review_generation(
        self,
        session_id: UUID,
    ) -> dict:
        """
        Queue AI review creation.
        """

        return {
            "task": "review_generation",
            "session_id": str(
                session_id
            ),
            "status": "queued",
        }



    async def queue_ocr_processing(
        self,
        attachment_id: UUID,
    ) -> dict:
        """
        Queue handwritten OCR extraction.
        """

        return {
            "task": "ocr_processing",
            "attachment_id": str(
                attachment_id
            ),
            "status": "queued",
        }
