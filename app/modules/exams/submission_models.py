from __future__ import annotations

from datetime import datetime
from uuid import UUID

from sqlalchemy import Boolean
from sqlalchemy import DateTime
from sqlalchemy import Float
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import JSON
from sqlalchemy import String
from sqlalchemy import Text
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from app.database.base import BaseModel


class ExamSubmission(BaseModel):

    __tablename__ = "exam_submissions"

    session_id: Mapped[UUID] = mapped_column(
        ForeignKey(
            "exam_sessions.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    question_id: Mapped[UUID] = mapped_column(
        ForeignKey(
            "exam_questions.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    question_number: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    answer_type: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )

    typed_answer: Mapped[str | None] = mapped_column(
        Text,
    )

    handwritten_image: Mapped[str | None] = mapped_column(
        String(1000),
    )

    extracted_text: Mapped[str | None] = mapped_column(
        Text,
    )

    awarded_marks: Mapped[float] = mapped_column(
        Float,
        default=0,
    )

    max_marks: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    ai_feedback: Mapped[dict | None] = mapped_column(
        JSON,
    )

    is_marked: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
    )

    submitted_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow,
    )

    session = relationship(
        "ExamSession",
        back_populates="submissions",
    )

    question = relationship(
        "ExamQuestion",
    )

