from __future__ import annotations

from pydantic import BaseModel, Field


class DocumentAnalysis(BaseModel):
    subject: str
    topic: str
    subtopics: list[str] = Field(default_factory=list)

    learning_style: str

    difficulty: str

    requires_calculations: bool
    requires_worked_examples: bool
    requires_formulas: bool
    requires_code: bool
    requires_diagrams: bool
    requires_tables: bool
    requires_memorization: bool

    language: str

    confidence: float
