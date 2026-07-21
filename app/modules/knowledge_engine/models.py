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
    Unified learning input.

    This can represent:

    - PDF
    - DOCX
    - PPTX
    - TXT
    - Handwritten image
    - Printed image
    - Topic description
    - Pasted text
    """

    __tablename__ = "knowledge_sources"

    __table_args__ = (
        Index("ix_knowledge_user_id", "user_id"),
        Index("ix_knowledge_source_type", "source_type"),
        Index("ix_knowledge_status", "processing_status"),
    )

    # owner

    user_id: Mapped[UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )

    # source information

    source_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    # pdf
    # image
    # text
    # topic

    title: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    # storage

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

    # extracted text

    raw_text: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    cleaned_text: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    # OCR

    ocr_completed: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        server_default="false",
        nullable=False,
    )

    # processing

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

    def __repr__(self) -> str:
        return (
            f"<KnowledgeSource("
            f"id={self.id}, "
            f"type={self.source_type}, "
            f"title='{self.title}'"
            f")>"
        )
