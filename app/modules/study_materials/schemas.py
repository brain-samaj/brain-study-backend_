from __future__ import annotations

from datetime import datetime
from enum import Enum
from uuid import UUID

from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import Field


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


class StudyMaterialCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    description: str | None = None

    original_filename: str
    stored_filename: str
    storage_path: str

    file_type: MaterialType
    mime_type: str

    file_size: int

    extracted_text: str = ""

    page_count: int | None = None

    word_count: int = 0


class StudyMaterialUpdate(BaseModel):
    title: str | None = Field(default=None, max_length=255)
    description: str | None = None

    extracted_text: str | None = None

    page_count: int | None = None

    word_count: int | None = None

    processing_status: ProcessingStatus | None = None

    extraction_error: str | None = None

    is_archived: bool | None = None


class StudyMaterialResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID

    owner_id: UUID

    title: str

    description: str | None

    original_filename: str

    stored_filename: str

    storage_path: str

    file_type: MaterialType

    mime_type: str

    file_size: int

    extracted_text: str

    page_count: int | None

    word_count: int

    processing_status: ProcessingStatus

    extraction_error: str | None

    is_archived: bool

    created_at: datetime

    updated_at: datetime


class StudyMaterialListItem(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID

    title: str

    file_type: MaterialType

    file_size: int

    page_count: int | None

    word_count: int

    processing_status: ProcessingStatus

    created_at: datetime


class StudyMaterialSearchResponse(BaseModel):
    items: list[StudyMaterialListItem]

    total: int


class DeleteStudyMaterialResponse(BaseModel):
    """
    Response returned after successfully deleting a study material.
    """

    id: UUID

    message: str


class StudyMaterialListResponse(BaseModel):
    """
    Response returned when listing study materials.
    """

    items: list[StudyMaterialListItem]

    total: int
