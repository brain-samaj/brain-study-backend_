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


class KnowledgeStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    READY = "ready"
    FAILED = "failed"


class KnowledgeSource(Base):
    """
    Stores AI-processed knowledge extracted from a study material.

    One uploaded material has exactly one KnowledgeSource.

    This table is the canonical knowledge store used by:
      • Exams
      • Flashcards
      • Smart Study
      • Summaries
      • AI Tutor
      • Future learning features

    The frontend never interacts with this table directly.
    """

    __tablename__ = "knowledge_sources"

    id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
    )

    material_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey(
            "study_materials.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        unique=True,
        index=True,
    )

    status: Mapped[KnowledgeStatus] = mapped_column(
        SqlEnum(KnowledgeStatus),
        default=KnowledgeStatus.PENDING,
        nullable=False,
        index=True,
    )

    title: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    summary: Mapped[str] = mapped_column(
        Text,
        nullable=False,
        default="",
    )

    knowledge: Mapped[dict] = mapped_column(
        JSONB,
        nullable=False,
        default=dict,
    )

    topics: Mapped[list] = mapped_column(
        JSONB,
        nullable=False,
        default=list,
    )

    glossary: Mapped[list] = mapped_column(
        JSONB,
        nullable=False,
        default=list,
    )

    learning_objectives: Mapped[list] = mapped_column(
        JSONB,
        nullable=False,
        default=list,
    )

    key_points: Mapped[list] = mapped_column(
        JSONB,
        nullable=False,
        default=list,
    )

    sample_questions: Mapped[list] = mapped_column(
        JSONB,
        nullable=False,
        default=list,
    )

    total_tokens: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )

    ai_provider: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    ai_model: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    processing_time_ms: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    error_message: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    is_cached: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    study_material = relationship(
        "StudyMaterial",
        back_populates="knowledge_source",
        uselist=False,
    )
