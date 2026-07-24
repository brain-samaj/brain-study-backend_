from __future__ import annotations

from datetime import datetime
from enum import Enum
from uuid import uuid4

from sqlalchemy import DateTime
from sqlalchemy import Enum as SqlEnum
from sqlalchemy import Float
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database.base import Base


# ============================================================
# ENUMS
# ============================================================


class ExamType(str, Enum):
    OBJECTIVE = "objective"
    THEORY = "theory"
    MIXED = "mixed"


class ExamDifficulty(str, Enum):
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"


class ExamStatus(str, Enum):
    CREATED = "created"
    IN_PROGRESS = "in_progress"
    SUBMITTED = "submitted"
    GRADING = "grading"
    GRADED = "graded"
    EXPIRED = "expired"
    FAILED = "failed"


class QuestionType(str, Enum):
    OBJECTIVE = "objective"
    THEORY = "theory"


# ============================================================
# EXAM SESSION
# ============================================================


class ExamSession(Base):

    __tablename__ = "exam_sessions"


    id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
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

    owner = relationship(
        "User",
    )

    study_material = relationship(
        "StudyMaterial",
        back_populates="exam_sessions",
    )

    exam_type: Mapped[ExamType] = mapped_column(
        SqlEnum(ExamType),
        nullable=False,
    )

    difficulty: Mapped[ExamDifficulty] = mapped_column(
        SqlEnum(ExamDifficulty),
        nullable=False,
    )


    status: Mapped[ExamStatus] = mapped_column(
        SqlEnum(ExamStatus),
        default=ExamStatus.CREATED,
        nullable=False,
        index=True,
    )


    total_questions: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )


    total_marks: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )


    obtained_marks: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )


    percentage: Mapped[float] = mapped_column(
        Float,
        default=0,
        nullable=False,
    )


    duration_minutes: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )


    started_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )


    expires_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )


    submitted_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )


    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )


    questions = relationship(
        "ExamQuestion",
        back_populates="session",
        cascade="all, delete-orphan",
        lazy="selectin",
    )


    answers = relationship(
        "ExamAnswer",
        back_populates="session",
        cascade="all, delete-orphan",
        lazy="selectin",
    )


# ============================================================
# EXAM QUESTION
# ============================================================


class ExamQuestion(Base):

    __tablename__ = "exam_questions"


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
        index=True,
    )


    question_number: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )


    question_type: Mapped[QuestionType] = mapped_column(
        SqlEnum(QuestionType),
        nullable=False,
    )


    question: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )


    topic: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )


    difficulty: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )


    marks: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )


    options: Mapped[list] = mapped_column(
        JSONB,
        default=list,
        nullable=False,
    )


    correct_answer: Mapped[str | None] = mapped_column(
        String(10),
        nullable=True,
    )


    explanation: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )


    subquestions: Mapped[list] = mapped_column(
        JSONB,
        default=list,
        nullable=False,
    )


    marking_scheme: Mapped[list] = mapped_column(
        JSONB,
        default=list,
        nullable=False,
    )


    model_answer: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )


    instructions: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )


    session = relationship(
        "ExamSession",
        back_populates="questions",
    )


# ============================================================
# EXAM ANSWER
# ============================================================


class ExamAnswer(Base):

    __tablename__ = "exam_answers"


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
        index=True,
    )


    question_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey(
            "exam_questions.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )


    selected_option: Mapped[str | None] = mapped_column(
        String(10),
        nullable=True,
    )


    text_answer: Mapped[str] = mapped_column(
        Text,
        default="",
        nullable=False,
    )


    ocr_answer: Mapped[str] = mapped_column(
        Text,
        default="",
        nullable=False,
    )


    final_answer: Mapped[str] = mapped_column(
        Text,
        default="",
        nullable=False,
    )


    awarded_marks: Mapped[float] = mapped_column(
        Float,
        default=0,
        nullable=False,
    )


    is_correct: Mapped[bool | None] = mapped_column(
        nullable=True,
    )


    feedback: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )


    corrections: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )


    suggestions: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )


    reasoning: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )


    answered_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )


    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )


    session = relationship(
        "ExamSession",
        back_populates="answers",
    )


    question = relationship(
        "ExamQuestion",
        lazy="joined",
    )


    attachments = relationship(
        "ExamAnswerAttachment",
        back_populates="answer",
        cascade="all, delete-orphan",
        lazy="selectin",
    )
