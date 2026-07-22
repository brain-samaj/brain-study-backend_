from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import Field


class CreateTopicRequest(BaseModel):
    """
    Create a topic without uploading a document.
    """

    title: str = Field(
        min_length=3,
        max_length=255,
    )

    subject: str = Field(
        min_length=2,
        max_length=120,
    )

    topic_description: str = Field(
        min_length=20,
    )


class KnowledgeSourceResponse(BaseModel):
    """
    Response returned after creating a topic
    or uploading a study material.
    """

    model_config = ConfigDict(
        from_attributes=True,
    )

    id: UUID

    title: str

    subject: str

    source_type: str

    processing_status: str


class KnowledgeSourceDetails(BaseModel):

    model_config = ConfigDict(
        from_attributes=True,
    )

    id: UUID

    title: str

    subject: str

    source_type: str

    description: str | None

    raw_text: str | None

    cleaned_text: str | None

    processing_status: str

    error_message: str | None

    file_name: str | None

    file_size: int | None

    mime_type: str | None

    created_at: datetime

    updated_at: datetime

    processed_at: datetime | None


class UploadResponse(BaseModel):

    id: UUID

    title: str

    subject: str

    source_type: str

    processing_status: str
