from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import Field

from app.modules.study_materials.models import MaterialType
from app.modules.study_materials.models import ProcessingStatus


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

    description: str | None

    original_filename: str

    file_type: MaterialType

    file_size: int

    page_count: int | None

    word_count: int

    processing_status: ProcessingStatus

    created_at: datetime


class StudyMaterialListResponse(BaseModel):
    total: int
    items: list[StudyMaterialListItem]


class StudyMaterialSearchResponse(BaseModel):
    total: int
    items: list[StudyMaterialListItem]


class DeleteStudyMaterialResponse(BaseModel):
    success: bool
    message: str
