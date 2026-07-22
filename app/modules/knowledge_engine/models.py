from __future__ import annotations

from datetime import datetime
from uuid import UUID

from sqlalchemy import Boolean
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Index
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Text
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from app.database.base import BaseModel


class KnowledgeSource(BaseModel):
    """
    Canonical knowledge extracted from uploaded
    study materials or typed topics.

    Everything in Brain Study (Study Guide,
    Smart Study, Flashcards, Exams) is generated
    from this model.
    """

    __tablename__ = "knowledge_sources"

    __table_args__ = (
        Index("ix_knowledge_user_id", "user_id"),
        Index("ix_knowledge_source_type", "source_type"),
        Index("ix_knowledge_subject", "subject"),
        Index("ix_knowledge_status", "processing_status"),
    )

    user_id: Mapped[UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )

    # Link back to the uploaded Study Material.
    # Topics created without a file will keep this NULL.
    study_material_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("study_materials.id", ondelete="SET NULL"),
        nullable=True,
        unique=True,
    )

    source_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    title: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    subject: Mapped[str] = mapped_column(
        String(120),
        nullable=False,
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    file_name: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
    )

    file_path: Mapped[str | None] = mapped_column(
        String(1000),
        nullable=True,
    )

    file_size: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    mime_type: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    raw_text: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    cleaned_text: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    ocr_completed: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        server_default="false",
        nullable=False,
    )

    processing_status: Mapped[str] = mapped_column(
        String(50),
        default="pending",
        server_default="pending",
        nullable=False,
    )

    error_message: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    processed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    study_material = relationship(
        "StudyMaterial",
        lazy="joined",
    )

    owner = relationship(
        "User",
        lazy="joined",
    )

    def __repr__(self) -> str:
        return (
            f"<KnowledgeSource("
            f"id={self.id}, "
            f"title='{self.title}', "
            f"subject='{self.subject}', "
            f"type='{self.source_type}'"
            f")>"
        )

