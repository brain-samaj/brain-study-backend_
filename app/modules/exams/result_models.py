from __future__ import annotations

from datetime import datetime
from uuid import uuid4

from sqlalchemy import DateTime
from sqlalchemy import Float
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.sql import func

from app.database.base import Base


class ExamResult(Base):
    """
    Stores final exam grading result.

    This table represents the permanent academic outcome.

    Stores:
    - scores
    - grading breakdown
    - performance data
    - AI generated insights
    """

    __tablename__ = "exam_results"


    id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
    )


    session_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey(
            "exam_sessions.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        unique=True,
        index=True,
    )


    owner_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey(
            "users.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )


    material_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey(
            "study_materials.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )


    score: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )


    total_marks: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )


    percentage: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )


    objective_score: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )


    theory_score: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )


    correct_answers: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )


    incorrect_answers: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )


    unanswered_questions: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )


    topic_analysis: Mapped[dict] = mapped_column(
        JSONB,
        default=dict,
        nullable=False,
    )


    strengths: Mapped[list] = mapped_column(
        JSONB,
        default=list,
        nullable=False,
    )


    weaknesses: Mapped[list] = mapped_column(
        JSONB,
        default=list,
        nullable=False,
    )


    recommendations: Mapped[list] = mapped_column(
        JSONB,
        default=list,
        nullable=False,
    )


    ai_summary: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )


    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
