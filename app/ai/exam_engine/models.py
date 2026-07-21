from __future__ import annotations

from pydantic import BaseModel, Field


class TheoryPart(BaseModel):
    label: str
    question: str
    marks: int
    marking_guide: list[str]


class TheoryQuestion(BaseModel):
    number: int
    title: str
    total_marks: int
    parts: list[TheoryPart]


class TheoryPaper(BaseModel):
    instructions: str
    questions_to_answer: int
    total_questions: int
    duration_minutes: int
    questions: list[TheoryQuestion] = Field(default_factory=list)
