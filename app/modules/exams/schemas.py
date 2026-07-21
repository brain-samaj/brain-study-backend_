from __future__ import annotations

from datetime import datetime
from typing import Any
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


# ============================================================
# CREATE EXAM
# ============================================================

class CreateExamRequest(BaseModel):
    study_material_id: UUID
    question_type: str = Field(pattern="^(objective|theory)$")
    total_questions: int = Field(ge=1, le=100)
    duration_minutes: int = Field(ge=1, le=300)


# ============================================================
# OBJECTIVE SUBMISSION
# ============================================================

class SubmitObjectiveRequest(BaseModel):
    answers: dict[str, Any]


# ============================================================
# THEORY SUBMISSION
# ============================================================

class SubmitTheoryRequest(BaseModel):
    answers: dict[str, str]


# ============================================================
# QUESTION
# ============================================================

class ExamQuestionResponse(BaseModel):

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    question_number: int
    question_type: str
    topic: str
    difficulty: str
    instruction: str | None
    question: str
    sub_questions: dict | None
    options: dict | None
    marks: int


# ============================================================
# SESSION
# ============================================================

class ExamSessionResponse(BaseModel):

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    study_material_id: UUID
    user_id: UUID

    exam_type: str

    total_questions: int

    duration_minutes: int

    status: str

    started_at: datetime | None

    submitted_at: datetime | None

    created_at: datetime


# ============================================================
# RESULT
# ============================================================

class ExamResultResponse(BaseModel):

    model_config = ConfigDict(from_attributes=True)

    score: float

    total_marks: float

    percentage: float

    grade: str

    passed: bool

    answered_questions: int

    unanswered_questions: int

    total_questions: int

    duration_seconds: int

    grading_summary: dict


# ============================================================
# HISTORY
# ============================================================

class ExamHistoryResponse(BaseModel):

    model_config = ConfigDict(from_attributes=True)

    id: UUID

    study_material_id: UUID

    exam_type: str

    status: str

    total_questions: int

    duration_minutes: int

    created_at: datetime

    submitted_at: datetime | None


# ============================================================
# REVIEW
# ============================================================

class ReviewQuestionResponse(BaseModel):

    question_number: int

    question: str

    student_answer: str | None

    correct_answer: Any | None

    awarded_marks: float

    max_marks: float

    feedback: dict | None


class ReviewResponse(BaseModel):

    session: ExamSessionResponse

    result: ExamResultResponse

    questions: list[ExamQuestionResponse]

    submissions: list[ReviewQuestionResponse]

