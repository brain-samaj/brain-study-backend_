from __future__ import annotations

from datetime import datetime
from enum import Enum
from uuid import uuid4

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


class AttachmentType(str, Enum):
    """
    Type of student answer attachment.
    """

    IMAGE = "image"
    PDF = "pdf"


class OCRStatus(str, Enum):
    """
    OCR processing lifecycle.
    """

    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class ExamAnswerAttachment(Base):
    """
    Stores handwritten answer attachments.

    One theory answer can contain:

    - typed text
    - image page 1
    - image page 2
    - image page 3
    - OCR extracted text

    The final answer is rebuilt by autosave service.
    """

    __tablename__ = "exam_answer_attachments"

    id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
    )

    answer_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey(
            "exam_answers.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    attachment_type: Mapped[AttachmentType] = mapped_column(
        SqlEnum(AttachmentType),
        nullable=False,
        default=AttachmentType.IMAGE,
    )

    original_filename: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    stored_filename: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    storage_path: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    mime_type: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    file_size: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    page_number: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=1,
    )

    ocr_status: Mapped[OCRStatus] = mapped_column(
        SqlEnum(OCRStatus),
        nullable=False,
        default=OCRStatus.PENDING,
        index=True,
    )

    ocr_text: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    processed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )


    answer = relationship(
        "ExamAnswer",
        back_populates="attachments",
        lazy="joined",
    )
