from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from app.ai.client import AIClient
from app.ai.prompts.theory_marking import (
    THEORY_MARKING_PROMPT,
)


class TheoryMarkingError(Exception):
    """
    Raised when AI theory marking fails.
    """


@dataclass(slots=True)
class TheoryMarkResult:
    """
    Structured result returned by the AI marker.
    """

    awarded_marks: float

    total_marks: float

    percentage: float

    feedback: str

    corrections: str

    suggestions: str

    reasoning: str


class TheoryMarker:
    """
    Enterprise Theory Answer Marker.

    Responsibilities
    ----------------
    • Mark theory answers.
    • Support typed answers.
    • Support handwritten answers after OCR.
    • Validate AI output.
    • Never expose AI providers.

    AIClient automatically selects:

        Primary
            Groq

        Fallback
            Gemini
    """

    def __init__(
        self,
        ai_client: AIClient,
    ) -> None:

        self._client = ai_client

    async def mark(
        self,
        *,
        question: str,
        marking_scheme: str,
        model_answer: str,
        student_answer: str,
        total_marks: int,
    ) -> TheoryMarkResult:

        prompt = THEORY_MARKING_PROMPT.format(
            question=question,
            marking_scheme=marking_scheme,
            model_answer=model_answer,
            student_answer=student_answer,
            total_marks=total_marks,
        )

        response = await self._client.generate_json(
            system_prompt=(
                "You are an experienced university examiner. "
                "Return ONLY valid JSON."
            ),
            prompt=prompt,
            temperature=0.2,
        )

        self._validate(
            response,
            total_marks,
        )

        return TheoryMarkResult(
            awarded_marks=float(
                response["awarded_marks"],
            ),
            total_marks=float(total_marks),
            percentage=float(
                response["percentage"],
            ),
            feedback=response["feedback"],
            corrections=response["corrections"],
            suggestions=response["suggestions"],
            reasoning=response["reasoning"],
        )


    def _validate(
        self,
        payload: dict[str, Any],
        total_marks: int,
    ) -> None:
        """
        Validate the AI marking response.
        """

        if not isinstance(
            payload,
            dict,
        ):
            raise TheoryMarkingError(
                "AI response must be a JSON object."
            )

        required_fields = (
            "awarded_marks",
            "percentage",
            "feedback",
            "corrections",
            "suggestions",
            "reasoning",
        )

        for field in required_fields:
            if field not in payload:
                raise TheoryMarkingError(
                    f"Missing required field '{field}'."
                )

        try:
            awarded_marks = float(
                payload["awarded_marks"],
            )
        except (TypeError, ValueError) as exc:
            raise TheoryMarkingError(
                "'awarded_marks' must be numeric."
            ) from exc

        if awarded_marks < 0:
            raise TheoryMarkingError(
                "Awarded marks cannot be negative."
            )

        if awarded_marks > total_marks:
            raise TheoryMarkingError(
                "Awarded marks exceed total marks."
            )

        try:
            percentage = float(
                payload["percentage"],
            )
        except (TypeError, ValueError) as exc:
            raise TheoryMarkingError(
                "'percentage' must be numeric."
            ) from exc

        if percentage < 0 or percentage > 100:
            raise TheoryMarkingError(
                "Percentage must be between 0 and 100."
            )

        for text_field in (
            "feedback",
            "corrections",
            "suggestions",
            "reasoning",
        ):
            value = payload.get(
                text_field,
            )

            if not isinstance(
                value,
                str,
            ):
                raise TheoryMarkingError(
                    f"'{text_field}' must be a string."
                )

            if not value.strip():
                raise TheoryMarkingError(
                    f"'{text_field}' cannot be empty."
                )
