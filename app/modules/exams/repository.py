from __future__ import annotations

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.modules.exams.models import ExamQuestion
from app.modules.exams.models import ExamSession
from app.modules.exams.result_models import ExamResult
from app.modules.exams.submission_models import ExamSubmission


class ExamRepository:

    def __init__(
        self,
        db: Session,
    ):
        self.db = db

    ####################################################
    # SESSION
    ####################################################

    def create_session(
        self,
        session: ExamSession,
    ) -> ExamSession:

        self.db.add(session)
        self.db.commit()
        self.db.refresh(session)

        return session

    def get_session(
        self,
        session_id: UUID,
    ) -> ExamSession | None:

        return self.db.get(
            ExamSession,
            session_id,
        )

    def update_session(
        self,
        session: ExamSession,
    ) -> ExamSession:

        self.db.add(session)
        self.db.commit()
        self.db.refresh(session)

        return session

    ####################################################
    # QUESTIONS
    ####################################################

    def create_questions(
        self,
        questions: list[ExamQuestion],
    ) -> None:

        self.db.add_all(questions)
        self.db.commit()

    def get_questions(
        self,
        session_id: UUID,
    ) -> list[ExamQuestion]:

        return (
            self.db.execute(
                select(ExamQuestion)
                .where(
                    ExamQuestion.session_id == session_id,
                )
                .order_by(
                    ExamQuestion.question_number,
                )
            )
            .scalars()
            .all()
        )

    ####################################################
    # SUBMISSIONS
    ####################################################

    def save_submission(
        self,
        submission: ExamSubmission,
    ) -> ExamSubmission:

        self.db.add(submission)
        self.db.commit()
        self.db.refresh(submission)

        return submission

    def save_submissions(
        self,
        submissions: list[ExamSubmission],
    ) -> None:

        self.db.add_all(submissions)
        self.db.commit()

    def get_submission(
        self,
        session_id: UUID,
        question_id: UUID,
    ) -> ExamSubmission | None:

        return (
            self.db.execute(
                select(ExamSubmission).where(
                    ExamSubmission.session_id == session_id,
                    ExamSubmission.question_id == question_id,
                )
            )
            .scalars()
            .first()
        )

    def get_session_submissions(
        self,
        session_id: UUID,
    ) -> list[ExamSubmission]:

        return (
            self.db.execute(
                select(ExamSubmission)
                .where(
                    ExamSubmission.session_id == session_id,
                )
                .order_by(
                    ExamSubmission.question_number,
                )
            )
            .scalars()
            .all()
        )

    def update_submission(
        self,
        submission: ExamSubmission,
    ) -> ExamSubmission:

        self.db.add(submission)
        self.db.commit()
        self.db.refresh(submission)

        return submission

    ####################################################
    # MARKING
    ####################################################

    def save_marking(
        self,
        submission: ExamSubmission,
        *,
        awarded_marks: float,
        ai_feedback: dict,
    ) -> ExamSubmission:

        submission.awarded_marks = awarded_marks
        submission.ai_feedback = ai_feedback
        submission.is_marked = True

        self.db.add(submission)
        self.db.commit()
        self.db.refresh(submission)

        return submission

    ####################################################
    # FINAL RESULT
    ####################################################

    def save_result(
        self,
        result: ExamResult,
    ) -> ExamResult:

        self.db.add(result)
        self.db.commit()
        self.db.refresh(result)

        return result

    def update_result(
        self,
        result: ExamResult,
    ) -> ExamResult:

        self.db.add(result)
        self.db.commit()
        self.db.refresh(result)

        return result

    def get_result(
        self,
        session_id: UUID,
    ) -> ExamResult | None:

        return (
            self.db.execute(
                select(ExamResult).where(
                    ExamResult.session_id == session_id,
                )
            )
            .scalars()
            .first()
        )

    ####################################################
    # HISTORY
    ####################################################

    def get_user_exam_history(
        self,
        user_id: UUID,
    ) -> list[ExamSession]:

        return (
            self.db.execute(
                select(ExamSession)
                .where(
                    ExamSession.user_id == user_id,
                )
                .order_by(
                    ExamSession.created_at.desc(),
                )
            )
            .scalars()
            .all()
        )

    ####################################################
    # DELETE
    ####################################################

    def delete_session(
        self,
        session: ExamSession,
    ) -> None:

        self.db.delete(session)
        self.db.commit()

