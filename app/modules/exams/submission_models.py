from __future__ import annotations

from datetime import datetime
from enum import Enum
from uuid import uuid4

from sqlalchemy import Boolean
from sqlalchemy import DateTime
from sqlalchemy import Enum as SqlEnum
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database.base import Base


class SubmissionStatus(str, Enum):
    """
    Lifecycle of an exam submission.
    """

    DRAFT = "draft"
    AUTOSAVED = "autosaved"
    SUBMITTED = "submitted"
    GRADING = "grading"
    GRADED = "graded"
    FAILED = "failed"


class ExamSubmission(Base):
    """
    Immutable submission record.

    Purpose
    -------
    Records the exact state of an exam when the student
    pressed "Submit".

    This provides:
    - audit trail
    - dispute resolution
    - analytics
    - grading history
    - future re-grading support

    A submission references an ExamSession while preserving
    a snapshot of the student's work at submission time.
    """

    __tablename__ = "exam_submissions"

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

    status: Mapped[SubmissionStatus] = mapped_column(
        SqlEnum(SubmissionStatus),
        default=SubmissionStatus.DRAFT,
        nullable=False,
        index=True,
    )

    submitted_answers: Mapped[list] = mapped_column(
        JSONB,
        default=list,
        nullable=False,
    )

    question_snapshot: Mapped[list] = mapped_column(
        JSONB,
        default=list,
        nullable=False,
    )

    grading_snapshot: Mapped[dict] = mapped_column(
        JSONB,
        default=dict,
        nullable=False,
    )

    total_questions: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    answered_questions: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )

    attachment_count: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )

    contains_handwritten_answers: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    client_version: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    submission_notes: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    submitted_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    graded_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    session = relationship(
        "ExamSession",
        lazy="joined",
    )
