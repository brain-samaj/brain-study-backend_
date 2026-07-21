from uuid import UUID

from pydantic import BaseModel


class KnowledgeSourceResponse(BaseModel):
    id: UUID
    title: str
    subject: str
    source_type: str
    processing_status: str


class CreateTopicRequest(BaseModel):
    title: str
    subject: str
    topic_description: str


class UploadResponse(BaseModel):
    id: UUID
    processing_status: str
