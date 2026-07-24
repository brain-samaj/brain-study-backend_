from __future__ import annotations

from datetime import datetime
from enum import Enum
from uuid import uuid4

from sqlalchemy import Boolean
from sqlalchemy import DateTime
from sqlalchemy import Enum as SqlEnum
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database.base import Base


class MaterialType(str, Enum):
    PDF = "pdf"
    DOCX = "docx"
    PPTX = "pptx"
    TXT = "txt"
    MD = "md"


class ProcessingStatus(str, Enum):
    UPLOADING = "uploading"
    EXTRACTING = "extracting"
    PROCESSING = "processing"
    READY = "ready"
    FAILED = "failed"


class StudyMaterial(Base):
    """
    Canonical study material entity.

    Responsibilities
    ----------------
    - Stores uploaded study material metadata.
    - Stores extracted plain text.
    - Owns one KnowledgeSource.
    - Owns many ExamSessions.
    - Belongs to one User.

    The frontend interacts only with this entity.
    AI services consume the extracted content.
    """

    __tablename__ = "study_materials"

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

    title: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    original_filename: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    stored_filename: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        unique=True,
    )

    storage_path: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    file_type: Mapped[MaterialType] = mapped_column(
        SqlEnum(MaterialType),
        nullable=False,
        index=True,
    )

    mime_type: Mapped[str] = mapped_column(
        String(120),
        nullable=False,
    )

    file_size: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    extracted_text: Mapped[str] = mapped_column(
        Text,
        default="",
        nullable=False,
    )

    page_count: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    word_count: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )

    processing_status: Mapped[ProcessingStatus] = mapped_column(
        SqlEnum(ProcessingStatus),
        default=ProcessingStatus.UPLOADING,
        nullable=False,
        index=True,
    )

    extraction_error: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    is_archived: Mapped[bool] = mapped_column(
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

    owner = relationship(
        "User",
        back_populates="study_materials",
    )

    knowledge_source = relationship(
        "KnowledgeSource",
        back_populates="study_material",
        uselist=False,
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

    exam_sessions = relationship(
        "ExamSession",
        back_populates="study_material",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
