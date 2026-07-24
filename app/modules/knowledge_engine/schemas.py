from __future__ import annotations

from datetime import datetime
from enum import Enum
from uuid import UUID

from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import Field


class KnowledgeStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    READY = "ready"
    FAILED = "failed"


class KnowledgeTopic(BaseModel):
    title: str
    content: str
    keywords: list[str] = Field(default_factory=list)
    difficulty: str | None = None


class GlossaryItem(BaseModel):
    term: str
    definition: str


class LearningObjective(BaseModel):
    objective: str


class SampleQuestion(BaseModel):
    question: str
    answer: str


class KnowledgeCreate(BaseModel):
    material_id: UUID
    title: str
    summary: str = ""
    knowledge: dict = Field(default_factory=dict)
    topics: list[KnowledgeTopic] = Field(default_factory=list)
    glossary: list[GlossaryItem] = Field(default_factory=list)
    learning_objectives: list[LearningObjective] = Field(default_factory=list)
    key_points: list[str] = Field(default_factory=list)
    sample_questions: list[SampleQuestion] = Field(default_factory=list)
    total_tokens: int = 0
    ai_provider: str | None = None
    ai_model: str | None = None
    processing_time_ms: int | None = None
    is_cached: bool = False


class KnowledgeUpdate(BaseModel):
    status: KnowledgeStatus | None = None
    summary: str | None = None
    knowledge: dict | None = None
    topics: list[KnowledgeTopic] | None = None
    glossary: list[GlossaryItem] | None = None
    learning_objectives: list[LearningObjective] | None = None
    key_points: list[str] | None = None
    sample_questions: list[SampleQuestion] | None = None
    total_tokens: int | None = None
    ai_provider: str | None = None
    ai_model: str | None = None
    processing_time_ms: int | None = None
    error_message: str | None = None
    is_cached: bool | None = None


class KnowledgeResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    material_id: UUID

    status: KnowledgeStatus

    title: str
    summary: str

    knowledge: dict

    topics: list[KnowledgeTopic]

    glossary: list[GlossaryItem]

    learning_objectives: list[LearningObjective]

    key_points: list[str]

    sample_questions: list[SampleQuestion]

    total_tokens: int

    ai_provider: str | None

    ai_model: str | None

    processing_time_ms: int | None

    error_message: str | None

    is_cached: bool

    created_at: datetime

    updated_at: datetime


class KnowledgeSummaryResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    material_id: UUID

    status: KnowledgeStatus

    title: str

    summary: str

    topics: list[KnowledgeTopic]

    key_points: list[str]
