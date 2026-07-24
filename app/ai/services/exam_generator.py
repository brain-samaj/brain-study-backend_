from __future__ import annotations

import json
from typing import Any

from app.ai.client import AIClient
from app.ai.prompts.objective_exam import (
    OBJECTIVE_EXAM_PROMPT,
)
from app.ai.prompts.theory_exam import (
    THEORY_EXAM_PROMPT,
)


class ExamGenerationError(Exception):
    """
    Raised when AI fails to generate a valid exam.
    """


class ExamGenerator:
    """
    Enterprise AI Exam Generator.

    Responsibilities
    ----------------
    - Choose the correct prompt.
    - Call AIClient.
    - Parse JSON.
    - Validate response.
    - Return structured data.

    AIClient automatically selects:

        Primary:
            Groq

        Fallback:
            Gemini

    This class never knows which provider was used.
    """

    def __init__(
        self,
        ai_client: AIClient,
    ) -> None:

        self._client = ai_client

    async def generate(
        self,
        *,
        exam_type: str,
        study_content: str,
        number_of_questions: int,
        difficulty: str,
    ) -> dict[str, Any]:

        if exam_type == "objective":
            prompt = OBJECTIVE_EXAM_PROMPT
        else:
            prompt = THEORY_EXAM_PROMPT

        rendered_prompt = prompt.format(
            study_content=study_content,
            question_count=number_of_questions,
            difficulty=difficulty,
        )

        response = await self._client.generate_text(
            rendered_prompt,
        )

        return self._parse_response(
            response,
        )

    def _parse_response(
        self,
        response: str,
    ) -> dict[str, Any]:
        """
        Parse and validate AI JSON response.
        """

        try:
            payload = json.loads(
                response,
            )

        except json.JSONDecodeError as exc:
            raise ExamGenerationError(
                "AI returned invalid JSON."
            ) from exc

        self._validate_payload(
            payload,
        )

        return payload

    def _validate_payload(
        self,
        payload: dict[str, Any],
    ) -> None:
        """
        Validate the top-level payload.
        """

        if not isinstance(
            payload,
            dict,
        ):
            raise ExamGenerationError(
                "Expected JSON object."
            )

        if "questions" not in payload:
            raise ExamGenerationError(
                "Missing 'questions'."
            )

        questions = payload["questions"]

        if not isinstance(
            questions,
            list,
        ):
            raise ExamGenerationError(
                "'questions' must be a list."
            )

        if len(questions) == 0:
            raise ExamGenerationError(
                "No questions were generated."
            )

        for question in questions:

            if question.get(
                "options",
            ) is not None:

                self._validate_objective(
                    question,
                )

            else:

                self._validate_theory(
                    question,
                )

    def _validate_objective(
        self,
        question: dict[str, Any],
    ) -> None:
        """
        Validate one objective question.
        """

        required_fields = (
            "question_number",
            "question",
            "options",
            "correct_answer",
            "difficulty",
            "topic",
            "marks",
            "explanation",
        )

        for field in required_fields:

            if field not in question:
                raise ExamGenerationError(
                    f"Objective question missing '{field}'."
                )

        if not isinstance(
            question["options"],
            list,
        ):
            raise ExamGenerationError(
                "'options' must be a list."
            )

        if len(question["options"]) < 2:
            raise ExamGenerationError(
                "Objective question requires at least two options."
            )

    def _validate_theory(
        self,
        question: dict[str, Any],
    ) -> None:
        """
        Validate one theory question.
        """

        required_fields = (
            "question_number",
            "question",
            "subquestions",
            "marking_scheme",
            "model_answer",
            "difficulty",
            "topic",
            "marks",
            "instructions",
        )

        for field in required_fields:
            if field not in question:
                raise ExamGenerationError(
                    f"Theory question missing '{field}'."
                )

        if not isinstance(
            question["subquestions"],
            list,
        ):
            raise ExamGenerationError(
                "'subquestions' must be a list."
            )

        if not isinstance(
            question["marking_scheme"],
            list,
        ):
            raise ExamGenerationError(
                "'marking_scheme' must be a list."
            )

        if not isinstance(
            question["marks"],
            int,
        ):
            raise ExamGenerationError(
                "'marks' must be an integer."
            )

        if question["marks"] <= 0:
            raise ExamGenerationError(
                "'marks' must be greater than zero."
            )

        if not str(
            question["question"],
        ).strip():
            raise ExamGenerationError(
                "Theory question cannot be empty."
            )

        if not str(
            question["model_answer"],
        ).strip():
            raise ExamGenerationError(
                "Model answer cannot be empty."
            )

        if not str(
            question["topic"],
        ).strip():
            raise ExamGenerationError(
                "Topic cannot be empty."
            )

        if not str(
            question["difficulty"],
        ).strip():
            raise ExamGenerationError(
                "Difficulty cannot be empty."
            )

        if not str(
            question["instructions"],
        ).strip():
            raise ExamGenerationError(
                "Instructions cannot be empty."
            )
