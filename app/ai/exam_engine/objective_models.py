from __future__ import annotations

from pydantic import BaseModel, Field


class ObjectiveOption(BaseModel):
    id: str
    text: str


class ObjectiveQuestion(BaseModel):
    id: str
    question: str
    options: list[ObjectiveOption]
    answer: str
    explanation: str
    difficulty: str
    topic: str


class ObjectivePaper(BaseModel):
    duration_minutes: int
    total_questions: int
    questions: list[ObjectiveQuestion] = Field(default_factory=list)
