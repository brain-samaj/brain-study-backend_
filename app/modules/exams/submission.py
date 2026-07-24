from __future__ import annotations

from datetime import UTC
from datetime import datetime
from uuid import UUID

from app.modules.exams.exceptions import (
    ExamAlreadySubmittedError,
    SubmissionError,
)
from app.modules.exams.models import ExamStatus
from app.modules.exams.repository import ExamRepository
from app.modules.exams.submission_models import (
    ExamSubmission,
    SubmissionStatus,
)


class ExamSubmissionService:
    """
    Exam Submission Workflow Engine.

    Responsibilities
    ----------------
    - Validate exam state.
    - Freeze student answers.
    - Create immutable submission record.
    - Prepare grading pipeline.

    Submission is the point where the exam
    becomes a permanent attempt.
    """


    def __init__(
        self,
        *,
        repository: ExamRepository,
    ) -> None:

        self._repository = repository



    async def submit(
        self,
        *,
        session_id: UUID,
    ) -> ExamSubmission:

        session = await (
            self._repository
            .get_session(
                session_id,
            )
        )


        if session is None:

            raise SubmissionError(
                "Exam session not found."
            )


        if session.status in {
            ExamStatus.SUBMITTED,
            ExamStatus.GRADING,
            ExamStatus.GRADED,
        }:

            raise ExamAlreadySubmittedError(
                "Exam already submitted."
            )



        answers_snapshot = []


        for answer in session.answers:

            answers_snapshot.append(
                {
                    "question_id": (
                        str(answer.question_id)
                    ),

                    "selected_option": (
                        answer.selected_option
                    ),

                    "text_answer": (
                        answer.text_answer
                    ),

                    "ocr_answer": (
                        answer.ocr_answer
                    ),

                    "final_answer": (
                        answer.final_answer
                    ),

                    "attachments": [
                        {
                            "id": str(
                                attachment.id
                            ),

                            "filename": (
                                attachment.original_filename
                            ),

                            "ocr_text": (
                                attachment.ocr_text
                            ),
                        }

                        for attachment
                        in answer.attachments
                    ],
                }
            )



        question_snapshot = []


        for question in session.questions:

            question_snapshot.append(
                {
                    "id": str(
                        question.id
                    ),

                    "question": (
                        question.question
                    ),

                    "type": (
                        question.question_type.value
                    ),

                    "marks": (
                        question.marks
                    ),

                    "topic": (
                        question.topic
                    ),
                }
            )



        submission = ExamSubmission(
            session_id=session.id,
            owner_id=session.owner_id,
            material_id=session.material_id,

            status=(
                SubmissionStatus.SUBMITTED
            ),

            submitted_answers=(
                answers_snapshot
            ),

            question_snapshot=(
                question_snapshot
            ),

            total_questions=(
                session.total_questions
            ),

            answered_questions=len(
                [
                    answer
                    for answer
                    in session.answers
                    if answer.final_answer
                    or answer.selected_option
                ]
            ),

            attachment_count=sum(
                len(answer.attachments)
                for answer
                in session.answers
            ),

            contains_handwritten_answers=any(
                answer.ocr_answer
                for answer
                in session.answers
            ),

            submitted_at=datetime.now(
                UTC,
            ),
        )



        session.status = (
            ExamStatus.SUBMITTED
        )

        session.submitted_at = (
            datetime.now(
                UTC,
            )
        )


        await self._repository.create_submission(
            submission,
        )


        await self._repository.update_session(
            session,
        )


        await self._repository.commit()


        return submission
