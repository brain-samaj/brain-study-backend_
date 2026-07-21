from __future__ import annotations

from pydantic import BaseModel


class StudyQuestion(BaseModel):
    question: str
    options: list[str]
    answer: str
    explanation: str
    difficulty: str


class StudySession(BaseModel):
    material_id: str
    previous_questions: list[str] = []
    score: int = 0
    attempts: int = 0
