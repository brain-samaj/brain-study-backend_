from __future__ import annotations

from uuid import UUID

from sqlalchemy import Float
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from app.database.base import BaseModel


class SmartStudyProgress(BaseModel):
    """
    Stores long-term learning progress for a student
    on a particular study material.
    """

    __tablename__ = "smart_study_progress"

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

    current_topic: Mapped[str | None] = mapped_column(
        String(255),
    )

    difficulty: Mapped[str] = mapped_column(
        String(20),
        default="adaptive",
    )

    total_questions: Mapped[int] = mapped_column(
        Integer,
        default=0,
    )

    correct_answers: Mapped[int] = mapped_column(
        Integer,
        default=0,
    )

    wrong_answers: Mapped[int] = mapped_column(
        Integer,
        default=0,
    )

    mastery_score: Mapped[float] = mapped_column(
        Float,
        default=0.0,
    )

    confidence_score: Mapped[float] = mapped_column(
        Float,
        default=0.0,
    )
