from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any

from app.ai.client import AIClient
from app.modules.exams.exceptions import ReviewGenerationError
from app.modules.exams.models import ExamSession
from app.modules.exams.repository import ExamRepository


@dataclass(slots=True)
class ExamReviewResult:
    """
    Final AI-generated exam review.
    """

    overall_feedback: str

    strengths: list[str]

    weaknesses: list[str]

    recommendations: list[str]

    study_plan: list[str]

    topic_analysis: list[dict[str, Any]]

    confidence_score: float


class ExamReviewService:
    """
    Enterprise Exam Review Generator.

    Responsibilities
    ----------------
    - Analyze completed exams.
    - Generate personalized feedback.
    - Identify weak areas.
    - Recommend improvements.

    AI is backend-only.

    Frontend receives only JSON.
    """

    def __init__(
        self,
        *,
        repository: ExamRepository,
        ai_client: AIClient,
    ) -> None:

        self._repository = repository
        self._ai_client = ai_client


    async def generate_review(
        self,
        session: ExamSession,
    ) -> ExamReviewResult:

        prompt = self._build_prompt(
            session,
        )

        response = await self._ai_client.generate_json(
            system_prompt=(
                "You are an expert learning coach "
                "and academic analyst."
            ),
            prompt=prompt,
            temperature=0.3,
        )

        self._validate(
            response,
        )

        review = ExamReviewResult(
            overall_feedback=response[
                "overall_feedback"
            ],
            strengths=response[
                "strengths"
            ],
            weaknesses=response[
                "weaknesses"
            ],
            recommendations=response[
                "recommendations"
            ],
            study_plan=response[
                "study_plan"
            ],
            topic_analysis=response[
                "topic_analysis"
            ],
            confidence_score=float(
                response[
                    "confidence_score"
                ]
            ),
        )

        return review


    def _build_prompt(
        self,
        session: ExamSession,
    ) -> str:

        return f"""
Analyze this completed exam.

Exam Type:
{session.exam_type.value}

Difficulty:
{session.difficulty.value}

Score:
{session.obtained_marks}/{session.total_marks}

Percentage:
{session.percentage}

Questions:
{[
    {
        "question": question.question,
        "topic": question.topic,
        "marks": question.marks
    }
    for question in session.questions
]}

Create a personalized learning review.

Return JSON only:

{{
 "overall_feedback":"",
 "strengths":[],
 "weaknesses":[],
 "recommendations":[],
 "study_plan":[],
 "topic_analysis":[],
 "confidence_score":0
}}
"""


    def _validate(
        self,
        payload: dict[str, Any],
    ) -> None:

        required = (
            "overall_feedback",
            "strengths",
            "weaknesses",
            "recommendations",
            "study_plan",
            "topic_analysis",
            "confidence_score",
        )

        for field in required:

            if field not in payload:
                raise ReviewGenerationError(
                    f"Missing review field: {field}"
                )

        if not isinstance(
            payload["strengths"],
            list,
        ):
            raise ReviewGenerationError(
                "Strengths must be a list."
            )

        if not isinstance(
            payload["weaknesses"],
            list,
        ):
            raise ReviewGenerationError(
                "Weaknesses must be a list."
            )

        score = float(
            payload["confidence_score"]
        )

        if score < 0 or score > 100:
            raise ReviewGenerationError(
                "Invalid confidence score."
            )
