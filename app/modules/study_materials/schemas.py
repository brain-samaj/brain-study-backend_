from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import Field


class StudyMaterialCreate(BaseModel):
    """
    Metadata supplied alongside an uploaded file.
    """

    title: str = Field(
        ...,
        min_length=2,
        max_length=255,
    )

    description: str | None = Field(
        default=None,
        max_length=5000,
    )


class StudyMaterialUpdate(BaseModel):
    """
    Editable fields.
    """

    title: str | None = Field(
        default=None,
        min_length=2,
        max_length=255,
    )

    description: str | None = Field(
        default=None,
        max_length=5000,
    )


class StudyMaterialResponse(BaseModel):
    """
    Single study material returned to clients.
    """

    id: UUID

    user_id: UUID

    title: str

    description: str | None

    original_filename: str

    stored_filename: str

    mime_type: str

    file_extension: str

    file_size: int

    storage_path: str

    ai_processed: bool

    created_at: datetime

    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )


class StudyMaterialListResponse(BaseModel):
    """
    Paginated list of study materials.
    """

    total: int

    items: list[StudyMaterialResponse]


class DeleteStudyMaterialResponse(BaseModel):
    """
    Delete confirmation.
    """

    success: bool

    message: str
