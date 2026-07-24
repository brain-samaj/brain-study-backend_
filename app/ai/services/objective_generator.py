from __future__ import annotations

from typing import Any

from app.ai.client import AIClient
from app.ai.prompts.objective_exam import (
    OBJECTIVE_EXAM_PROMPT,
)


class ObjectiveGeneratorError(Exception):
    """Raised when objective question generation fails."""


class ObjectiveGenerator:
    """
    Enterprise Objective Question Generator.

    Responsibilities
    ----------------
    - Generate ONLY objective questions.
    - Never generate theory questions.
    - Never perform grading.
    - Never know which AI provider is being used.

    AI selection is handled internally by AIClient.
    """

    def __init__(
        self,
        ai_client: AIClient,
    ) -> None:
        self._client = ai_client

    async def generate(
        self,
        *,
        study_content: str,
        question_count: int,
        difficulty: str,
    ) -> dict[str, Any]:

        prompt = OBJECTIVE_EXAM_PROMPT.format(
            study_content=study_content,
            question_count=question_count,
            difficulty=difficulty,
        )

        response = await self._client.generate_json(
            system_prompt=(
                "You are an expert examination paper setter. "
                "Return ONLY valid JSON."
            ),
            prompt=prompt,
            temperature=0.4,
        )

        self._validate(response)

        return response

    def _validate(
        self,
        payload: dict[str, Any],
    ) -> None:
        """
        Validate the generated objective exam payload.
        """

        if not isinstance(payload, dict):
            raise ObjectiveGeneratorError(
                "AI response must be a JSON object."
            )

        questions = payload.get("questions")

        if not isinstance(questions, list):
            raise ObjectiveGeneratorError(
                "'questions' must be a list."
            )

        if len(questions) == 0:
            raise ObjectiveGeneratorError(
                "No objective questions were generated."
            )

        required_fields = (
            "question_number",
            "question",
            "options",
            "correct_answer",
            "explanation",
            "difficulty",
            "topic",
            "marks",
        )

        for index, question in enumerate(
            questions,
            start=1,
        ):
            if not isinstance(question, dict):
                raise ObjectiveGeneratorError(
                    f"Question {index} must be an object."
                )

            for field in required_fields:
                if field not in question:
                    raise ObjectiveGeneratorError(
                        f"Question {index} is missing '{field}'."
                    )

            options = question["options"]

            if not isinstance(options, list):
                raise ObjectiveGeneratorError(
                    f"Question {index}: options must be a list."
                )

            if len(options) != 4:
                raise ObjectiveGeneratorError(
                    f"Question {index} must contain exactly four options."
                )

            correct_answer = str(
                question["correct_answer"],
            ).strip()

            if correct_answer not in {
                "A",
                "B",
                "C",
                "D",
            }:
                raise ObjectiveGeneratorError(
                    f"Question {index}: correct_answer must be A, B, C or D."
                )

            marks = question["marks"]

            if not isinstance(
                marks,
                int,
            ):
                raise ObjectiveGeneratorError(
                    f"Question {index}: marks must be an integer."
                )

            if marks <= 0:
                raise ObjectiveGeneratorError(
                    f"Question {index}: marks must be greater than zero."
                )

            for text_field in (
                "question",
                "topic",
                "difficulty",
                "explanation",
            ):
                if not str(
                    question[text_field],
                ).strip():
                    raise ObjectiveGeneratorError(
                        f"Question {index}: '{text_field}' cannot be empty."
                    )
