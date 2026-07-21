from __future__ import annotations

from datetime import datetime
from enum import Enum
from uuid import UUID

from sqlalchemy import Boolean
from sqlalchemy import DateTime
from sqlalchemy import Enum as SqlEnum
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import JSON
from sqlalchemy import Numeric
from sqlalchemy import String
from sqlalchemy import Text
from sqlalchemy import func
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from app.database.base import BaseModel


class ExamType(str, Enum):
    OBJECTIVE = "objective"
    THEORY = "theory"


class ExamStatus(str, Enum):
    CREATED = "created"
    IN_PROGRESS = "in_progress"
    SUBMITTED = "submitted"
    EXPIRED = "expired"
    CANCELLED = "cancelled"


class ExamSession(BaseModel):
    __tablename__ = "exam_sessions"

    user_id: Mapped[UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        index=True,
    )

    study_material_id: Mapped[UUID] = mapped_column(
        ForeignKey("study_materials.id", ondelete="CASCADE"),
        index=True,
    )

    exam_type: Mapped[ExamType] = mapped_column(SqlEnum(ExamType))

    status: Mapped[ExamStatus] = mapped_column(
        SqlEnum(ExamStatus),
        default=ExamStatus.CREATED,
        index=True,
    )

    duration_minutes: Mapped[int]
    requested_questions: Mapped[int]
    generated_questions: Mapped[int]

    instructions: Mapped[str | None] = mapped_column(Text)

    started_at: Mapped[datetime | None]
    ends_at: Mapped[datetime | None]
    submitted_at: Mapped[datetime | None]

    score: Mapped[float] = mapped_column(Numeric(6,2), default=0)
    percentage: Mapped[float] = mapped_column(Numeric(5,2), default=0)

    grade: Mapped[str | None] = mapped_column(String(5))
    ai_feedback: Mapped[str | None] = mapped_column(Text)

    questions: Mapped[list["ExamQuestion"]] = relationship(
        back_populates="session",
        cascade="all, delete-orphan",
    )


class ExamQuestion(BaseModel):
    __tablename__ = "exam_questions"

    session_id: Mapped[UUID] = mapped_column(
        ForeignKey("exam_sessions.id", ondelete="CASCADE"),
        index=True,
    )

    question_number: Mapped[int]

    question_type: Mapped[str]
    topic: Mapped[str]
    difficulty: Mapped[str]

    instruction: Mapped[str | None] = mapped_column(Text)

    question: Mapped[str] = mapped_column(Text)

    sub_questions: Mapped[dict | None] = mapped_column(JSON)

    options: Mapped[dict | None] = mapped_column(JSON)

    answer: Mapped[dict | None] = mapped_column(JSON)

    marking_scheme: Mapped[dict | None] = mapped_column(JSON)

    explanation: Mapped[str | None] = mapped_column(Text)

    marks: Mapped[int] = mapped_column(default=1)

    shuffle_options: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
    )

    session: Mapped["ExamSession"] = relationship(
        back_populates="questions",
    )

    answers: Mapped[list["ExamAnswer"]] = relationship(
        back_populates="question",
        cascade="all, delete-orphan",
    )


class ExamAnswer(BaseModel):
    __tablename__ = "exam_answers"

    session_id: Mapped[UUID] = mapped_column(
        ForeignKey("exam_sessions.id", ondelete="CASCADE"),
        index=True,
    )

    question_id: Mapped[UUID] = mapped_column(
        ForeignKey("exam_questions.id", ondelete="CASCADE"),
        index=True,
    )

    typed_answer: Mapped[str | None] = mapped_column(Text)

    selected_option: Mapped[str | None] = mapped_column(String(10))

    handwriting_image: Mapped[str | None] = mapped_column(
        String(1000)
    )

    ocr_text: Mapped[str | None] = mapped_column(Text)

    ai_marks: Mapped[float] = mapped_column(
        Numeric(5,2),
        default=0,
    )

    max_marks: Mapped[float] = mapped_column(
        Numeric(5,2),
    )

    is_correct: Mapped[bool | None]

    ai_feedback: Mapped[str | None] = mapped_column(Text)

    question: Mapped["ExamQuestion"] = relationship(
        back_populates="answers",
    )

submissions = relationship(
    "ExamSubmission",
    back_populates="session",
    cascade="all, delete-orphan",
)

result = relationship(
    "ExamResult",
    back_populates="session",
    uselist=False,
    cascade="all, delete-orphan",
)
