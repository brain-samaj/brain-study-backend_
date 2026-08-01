from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(slots=True)
class DocumentAnalysis:
    """
    Educational analysis produced once by the Knowledge Engine.

    This analysis is reused by every learning feature.

    The Teacher AI MUST NEVER analyse the uploaded document again.
    It simply follows this educational blueprint.

    Used by:
    • Study Guide
    • Smart Study
    • Flashcards
    • Practice Exams
    • AI Tutor
    • Future learning systems
    """

    # ==========================================================
    # BASIC INFORMATION
    # ==========================================================

    title: str
    subject: str
    topic: str

    difficulty: str
    language: str
    education_level: str

    estimated_reading_minutes: int
    word_count: int

    # ==========================================================
    # CONTENT CHARACTERISTICS
    # ==========================================================

    requires_calculations: bool
    requires_formulae: bool
    requires_tables: bool
    requires_diagrams: bool
    requires_code: bool
    requires_memorization: bool

    # ==========================================================
    # TEACHING BLUEPRINT
    # ==========================================================

    teaching_style: str
    explanation_style: str
    example_density: str
    reasoning_depth: str

    needs_worked_examples: bool
    needs_real_life_examples: bool
    needs_visual_explanations: bool
    needs_step_by_step: bool
    needs_definitions_first: bool
    needs_classification: bool
    needs_comparison_tables: bool
    needs_timelines: bool
    needs_mnemonics: bool

    # ==========================================================
    # LEARNING DATA
    # ==========================================================

    keywords: list[str]
    learning_objectives: list[str]
    important_terms: list[str]
    prerequisites: list[str]

    learning_style: str

    confidence: float


@dataclass(slots=True)
class AIQuestionAnalysis:
    """
    Metadata describing a generated question.
    """

    topic: str
    difficulty: str
    cognitive_level: str
    estimated_time_seconds: int

    explanation: str | None = None


@dataclass(slots=True)
class AIAnswerAnalysis:
    """
    AI evaluation of a student's answer.
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
    AI understanding of study progress.
    """

    summary: str
    key_topics: list[str]
    important_concepts: list[str]
    difficulty_level: str
    recommended_focus: list[str]


@dataclass(slots=True)
class AIReviewAnalysis:
    """
    AI-generated review after assessment.
    """

    overall_score_comment: str

    strengths: list[str]
    weaknesses: list[str]
    recommendations: list[str]

    study_plan: list[str]

    topic_performance: list[dict[str, Any]]

    confidence_score: float
