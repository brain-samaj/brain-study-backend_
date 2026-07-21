from __future__ import annotations

from enum import Enum

from pydantic import BaseModel


class Grade(str, Enum):

    A_PLUS = "A+"
    A = "A"
    B_PLUS = "B+"
    B = "B"
    C = "C"
    D = "D"
    E = "E"
    F = "F"


class EvaluationReport(BaseModel):

    score: float

    max_score: float

    percentage: float

    grade: Grade

    passed: bool

    strengths: list[str]

    mistakes: list[str]

    missing_points: list[str]

    feedback: str

    model_answer: str

    recommended_revision_topics: list[str]

    confidence: float
