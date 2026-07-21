from __future__ import annotations

from uuid import UUID

from sqlalchemy import Boolean
from sqlalchemy import Float
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Text
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from app.database.base import BaseModel


class SmartStudyQuestionHistory(BaseModel):
    """
    Stores every Smart Study question generated for a student.

    Used for:
    - Preventing duplicate questions
    - Adaptive learning
    - Spaced repetition
    - Performance analytics
    """

    __tablename__ = "smart_study_question_history"

    user_id: Mapped[UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    study_material_id: Mapped[UUID] = mapped_column(
        ForeignKey("study_materials.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    topic: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        index=True,
    )

    subtopic: Mapped[str | None] = mapped_column(
        String(255),
    )

    difficulty: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )

    question_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    question: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    correct_answer: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    student_answer: Mapped[str | None] = mapped_column(
        Text,
    )

    is_correct: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
    )

    response_time_seconds: Mapped[float] = mapped_column(
        Float,
        default=0.0,
    )

    ai_explanation: Mapped[str | None] = mapped_column(
        Text,
    )

    mastery_after_question: Mapped[float] = mapped_column(
        Float,
        default=0.0,
    )
