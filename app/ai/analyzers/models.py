from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(slots=True)
class DocumentAnalysis:
    """
    Represents AI analysis of an uploaded study document.

    Used by:
    - Study Guide generation
    - Smart Study generation
    - Flashcard generation
    - Exam generation
    """

    title: str

    subject: str

    topic: str

    difficulty: str

    language: str

    education_level: str

    estimated_reading_minutes: int

    word_count: int

    requires_calculations: bool

    requires_formulae: bool

    requires_tables: bool

    requires_diagrams: bool

    requires_code: bool

    requires_memorization: bool

    keywords: list[str]

    learning_objectives: list[str]

    important_terms: list[str]

    prerequisites: list[str]

    learning_style: str

    confidence: float



@dataclass(slots=True)
class AIQuestionAnalysis:
    """
    Represents AI analysis metadata for a generated question.
    """

    topic: str

    difficulty: str

    cognitive_level: str

    estimated_time_seconds: int

    explanation: str | None = None



@dataclass(slots=True)
class AIAnswerAnalysis:
    """
    Represents AI evaluation of a student's answer.
    """

    awarded_marks: float

    total_marks: float

    percentage: float

    correctness: str

    feedback: str

    strengths: list[str]

    weaknesses: list[str]

    improvements: list[str]

    reasoning: str



@dataclass(slots=True)
class AIStudyAnalysis:
    """
    Represents AI understanding of a study material.
    """

    summary: str

    key_topics: list[str]

    important_concepts: list[str]

    difficulty_level: str

    recommended_focus: list[str]



@dataclass(slots=True)
class AIReviewAnalysis:
    """
    Represents AI-generated exam review.
    """

    overall_score_comment: str

    strengths: list[str]

    weaknesses: list[str]

    recommendations: list[str]

    study_plan: list[str]

    topic_performance: list[dict[str, Any]]

    confidence_score: float
