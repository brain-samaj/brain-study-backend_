from __future__ import annotations

from uuid import UUID

from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import Field


class StartSmartStudyRequest(BaseModel):
    source_id: UUID


class SubmitAnswerRequest(BaseModel):
    question: str = Field(
        min_length=5,
    )

    selected_answer: str = Field(
        pattern="^[A-D]$",
    )


class SmartStudyQuestionResponse(BaseModel):

    question: str

    options: list[dict]

    concept: str

    difficulty: str

    estimated_time_seconds: int


class SmartStudyAnswerResponse(BaseModel):

    correct: bool

    selected_answer: str

    correct_answer: str

    explanation: str

    concept: str

    mastery_score: float

    difficulty: str

    streak: int


class SmartStudyProgressResponse(BaseModel):

    model_config = ConfigDict(
        from_attributes=True,
    )

    session_id: UUID

    total_questions: int

    correct_answers: int

    wrong_answers: int

    mastery_score: float

    difficulty: str

    current_streak: int

    longest_streak: int

    completed: bool

