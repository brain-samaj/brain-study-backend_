from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import Field

from app.modules.exams.models import ExamDifficulty
from app.modules.exams.models import ExamType


# ============================================================
# CREATE EXAM
# ============================================================


class CreateExamRequest(BaseModel):

    model_config = ConfigDict(
        use_enum_values=True,
    )


    exam_type: ExamType

    difficulty: ExamDifficulty

    question_count: int = Field(
        ge=1,
        le=100,
    )

    duration_minutes: int = Field(
        ge=1,
        le=300,
    )



# ============================================================
# ANSWER PAYLOADS
# ============================================================


class ObjectiveAnswerRequest(BaseModel):

    selected_option: str = Field(
        min_length=1,
        max_length=1,
    )



class TheoryAnswerRequest(BaseModel):

    text_answer: str = Field(
        max_length=50000,
    )



# ============================================================
# QUESTION RESPONSE
# ============================================================


class ExamQuestionResponse(BaseModel):

    model_config = ConfigDict(
        from_attributes=True,
    )


    id: UUID

    question_number: int

    question_type: str

    question: str

    topic: str

    difficulty: str

    marks: int

    options: list[str]

    instructions: str | None = None



# ============================================================
# SESSION RESPONSE
# ============================================================


class ExamSessionResponse(BaseModel):

    model_config = ConfigDict(
        from_attributes=True,
    )


    id: UUID

    material_id: UUID

    exam_type: str

    difficulty: str

    status: str

    total_questions: int

    total_marks: int

    duration_minutes: int

    started_at: datetime | None = None

    expires_at: datetime | None = None

    questions: list[
        ExamQuestionResponse
    ] = []



# ============================================================
# RESULT RESPONSE
# ============================================================


class ExamResultResponse(BaseModel):

    model_config = ConfigDict(
        from_attributes=True,
    )


    id: UUID

    score: int

    total_marks: int

    percentage: float

    objective_score: int

    theory_score: int

    correct_answers: int

    incorrect_answers: int

    unanswered_questions: int

    strengths: list[str]

    weaknesses: list[str]

    recommendations: list[str]

    ai_summary: str | None = None



# ============================================================
# TIMER RESPONSE
# ============================================================


class ExamTimerResponse(BaseModel):

    started_at: datetime | None

    expires_at: datetime | None

    server_time: datetime

    remaining_seconds: int

    elapsed_seconds: int

    progress_percent: float

    expired: bool
