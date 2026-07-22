from __future__ import annotations

from uuid import UUID

from sqlalchemy import Select
from sqlalchemy import desc
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.modules.smart_study.models import QuestionHistory
from app.modules.smart_study.models import SmartStudySession


class SmartStudyRepository:

    def __init__(
        self,
        db: Session,
    ):
        self.db = db

    # --------------------------------------------------
    # Session
    # --------------------------------------------------

    def create_session(
        self,
        *,
        user_id: UUID,
        source_id: UUID,
    ) -> SmartStudySession:

        session = SmartStudySession(
            user_id=user_id,
            source_id=source_id,
            total_questions=0,
            correct_answers=0,
            wrong_answers=0,
            current_streak=0,
            longest_streak=0,
            mastery_score=0.0,
            difficulty_level="easy",
            is_completed=False,
        )

        self.db.add(session)
        self.db.commit()
        self.db.refresh(session)

        return session

    def get_session(
        self,
        session_id: UUID,
    ) -> SmartStudySession | None:

        statement: Select = (
            select(SmartStudySession)
            .where(
                SmartStudySession.id == session_id,
            )
        )

        return self.db.scalar(statement)

    def save_session(
        self,
        session: SmartStudySession,
    ) -> SmartStudySession:

        self.db.add(session)
        self.db.commit()
        self.db.refresh(session)

        return session

    # --------------------------------------------------
    # Question History
    # --------------------------------------------------

    def add_question(
        self,
        *,
        session_id: UUID,
        question: str,
        correct_answer: str,
        selected_answer: str | None,
        is_correct: bool | None,
        explanation: str,
        concept: str,
        difficulty: str,
    ) -> QuestionHistory:

        history = QuestionHistory(
            session_id=session_id,
            question=question,
            correct_answer=correct_answer,
            selected_answer=selected_answer,
            is_correct=is_correct,
            explanation=explanation,
            concept=concept,
            difficulty=difficulty,
        )

        self.db.add(history)
        self.db.commit()
        self.db.refresh(history)

        return history

    def get_previous_questions(
        self,
        session_id: UUID,
    ) -> list[str]:

        statement = (
            select(
                QuestionHistory.question,
            )
            .where(
                QuestionHistory.session_id == session_id,
            )
            .order_by(
                desc(QuestionHistory.created_at),
            )
        )

        return list(self.db.scalars(statement).all())

    def get_weak_topics(
        self,
        session_id: UUID,
    ) -> list[str]:

        statement = (
            select(
                QuestionHistory.concept,
            )
            .where(
                QuestionHistory.session_id == session_id,
                QuestionHistory.is_correct.is_(False),
            )
        )

        return list(
            {
                topic
                for topic in self.db.scalars(statement).all()
            }
        )

