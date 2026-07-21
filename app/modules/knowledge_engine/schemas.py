from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import Field


class CreateTopicRequest(BaseModel):
    title: str = Field(min_length=2, max_length=255)
    subject: str = Field(min_length=2, max_length=120)
    topic_description: str = Field(min_length=20)


class KnowledgeSourceResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    title: str
    subject: str
    source_type: str
    description: str | None
    processing_status: str
    created_at: datetime


class UploadResponse(BaseModel):
    id: UUID
    title: str
    subject: str
    source_type: str
    processing_status: str


class KnowledgeListResponse(BaseModel):
    items: list[KnowledgeSourceResponse]


class ProcessingStatusResponse(BaseModel):
    id: UUID
    processing_status: str
    error_message: str | None = None
