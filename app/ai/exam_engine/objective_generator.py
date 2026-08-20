from __future__ import annotations

from typing import Any

from app.ai.client import AIClient
from app.ai.formatters import Formatter
from app.ai.prompts.objective_exam import OBJECTIVE_EXAM_PROMPT

from app.ai.exam_engine.objective_models import (
    ObjectiveOption,
    ObjectivePaper,
    ObjectiveQuestion,
)


class ObjectiveExamGenerationError(Exception):
    """Raised when objective exam generation fails."""


class ObjectiveExamGenerator:
    """
    Generates objective examinations using the centralized AI client.

    Pipeline:

        Study material
            ↓
        Objective prompt
            ↓
        AIClient.generate_json()
            ↓
        Formatter
            ↓
        Schema normalization
            ↓
        ObjectivePaper
    """

    def __init__(
        self,
        ai_client: AIClient | None = None,
    ) -> None:
        self.ai = ai_client or AIClient()
        self.formatter = Formatter()

    async def generate(
        self,
        *,
        analysis: Any,
        material: str,
        total_questions: int,
    ) -> ObjectivePaper:
        """
        Generate an objective examination.

        Parameters
        ----------
        analysis:
            Document analysis information.

        material:
            Extracted study material.

        total_questions:
            Number of questions requested.
        """

        if total_questions <= 0:
            raise ObjectiveExamGenerationError(
                "total_questions must be greater than zero."
            )

        difficulty = self._get_difficulty(analysis)

        prompt = OBJECTIVE_EXAM_PROMPT.format(
            study_content=material,
            difficulty=difficulty,
            question_count=total_questions,
        )

        try:
            payload = await self.ai.generate_json(
                prompt=prompt,
            )
        except Exception as exc:
            raise ObjectiveExamGenerationError(
                "Unable to generate objective examination."
            ) from exc

        # Apply the centralized mathematics/scientific formatter.
        payload = self.formatter.format_payload(payload)

        questions = self._normalize_questions(
            payload,
            total_questions=total_questions,
            difficulty=difficulty,
            analysis=analysis,
        )

        if not questions:
            raise ObjectiveExamGenerationError(
                "AI did not generate any objective questions."
            )

        return ObjectivePaper(
            duration_minutes=0,
            total_questions=len(questions),
            questions=questions,
        )

    def _normalize_questions(
        self,
        payload: Any,
        *,
        total_questions: int,
        difficulty: str,
        analysis: Any,
    ) -> list[ObjectiveQuestion]:
        """
        Convert raw AI JSON into ObjectiveQuestion models.
        """

        if not isinstance(payload, dict):
            raise ObjectiveExamGenerationError(
                "AI response must be a JSON object."
            )

        raw_questions = payload.get("questions")

        if not isinstance(raw_questions, list):
            raise ObjectiveExamGenerationError(
                "AI response must contain a 'questions' list."
            )

        normalized: list[ObjectiveQuestion] = []

        topic = self._get_topic(analysis)

        for index, raw_question in enumerate(
            raw_questions[:total_questions],
            start=1,
        ):
            if not isinstance(raw_question, dict):
                continue

            question_text = str(
                raw_question.get("question", "")
            ).strip()

            if not question_text:
                continue

            raw_options = raw_question.get("options", [])

            if not isinstance(raw_options, list):
                raw_options = []

            options = self._normalize_options(raw_options)

            if len(options) != 4:
                raise ObjectiveExamGenerationError(
                    f"Question {index} must contain exactly four options."
                )

            correct_answer = str(
                raw_question.get(
                    "correct_answer",
                    "A",
                )
            ).strip().upper()

            if correct_answer not in {"A", "B", "C", "D"}:
                raise ObjectiveExamGenerationError(
                    f"Question {index} has invalid correct_answer."
                )

            explanation = str(
                raw_question.get(
                    "explanation",
                    "",
                )
            ).strip()

            normalized.append(
                ObjectiveQuestion(
                    id=str(index),
                    question=question_text,
                    options=options,
                    answer=correct_answer,
                    explanation=explanation,
                    difficulty=str(
                        raw_question.get(
                            "difficulty",
                            difficulty,
                        )
                    ),
                    topic=str(
                        raw_question.get(
                            "topic",
                            topic,
                        )
                    ),
                )
            )

        return normalized

    def _normalize_options(
        self,
        raw_options: list[Any],
    ) -> list[ObjectiveOption]:
        """
        Convert AI options into ObjectiveOption models.
        """

        options: list[ObjectiveOption] = []

        for index, option in enumerate(raw_options[:4]):
            letter = chr(ord("A") + index)

            if isinstance(option, dict):
                text = str(
                    option.get(
                        "text",
                        option.get("option", ""),
                    )
                ).strip()

                option_id = str(
                    option.get(
                        "id",
                        letter,
                    )
                ).strip()
            else:
                text = str(option).strip()
                option_id = letter

            if not text:
                raise ObjectiveExamGenerationError(
                    f"Objective option {letter} is empty."
                )

            options.append(
                ObjectiveOption(
                    id=option_id,
                    text=text,
                )
            )

        return options

    @staticmethod
    def _get_difficulty(analysis: Any) -> str:
        """
        Safely obtain difficulty from document analysis.
        """

        if analysis is None:
            return "medium"

        if isinstance(analysis, dict):
            value = analysis.get("difficulty")
        else:
            value = getattr(
                analysis,
                "difficulty",
                None,
            )

        if value is None:
            return "medium"

        return str(value)

    @staticmethod
    def _get_topic(analysis: Any) -> str:
        """
        Safely obtain topic from document analysis.
        """

        if analysis is None:
            return "General"

        if isinstance(analysis, dict):
            value = analysis.get("topic")
        else:
            value = getattr(
                analysis,
                "topic",
                None,
            )

        if value is None:
            return "General"

        return str(value)
