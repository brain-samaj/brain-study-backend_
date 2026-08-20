from __future__ import annotations

from typing import Any

from app.ai.client import AIClient
from app.ai.exam_engine.models import (
    TheoryPaper,
    TheoryPart,
    TheoryQuestion,
)
from app.ai.formatters import Formatter
from app.ai.prompts.theory_exam import THEORY_EXAM_PROMPT


class TheoryExamGenerationError(Exception):
    """Raised when theory exam generation fails."""


class TheoryExamGenerator:
    """
    Generates theory examinations using the centralized AI pipeline.

    Pipeline:

        Study material
            ↓
        THEORY_EXAM_PROMPT
            ↓
        AIClient.generate_json()
            ↓
        Formatter
            ↓
        Schema normalization
            ↓
        TheoryPaper
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
        duration: int,
        answer_any: int,
    ) -> TheoryPaper:
        """
        Generate a theory examination.

        The AI generates question content only.
        Backend code is responsible for:

        - numbering
        - marks
        - labels
        - marking guides
        - instructions
        - difficulty/topic metadata where applicable
        """

        if answer_any <= 0:
            raise TheoryExamGenerationError(
                "answer_any must be greater than zero."
            )

        difficulty = self._get_difficulty(analysis)

        prompt = THEORY_EXAM_PROMPT.format(
            study_content=material,
            difficulty=difficulty,
            question_count=answer_any,
        )

        try:
            payload = await self.ai.generate_json(
                prompt=prompt,
            )
        except Exception as exc:
            raise TheoryExamGenerationError(
                "Unable to generate theory examination."
            ) from exc

        # Apply the centralized mathematics/scientific formatter.
        payload = self.formatter.format_payload(payload)

        questions = self._normalize_questions(
            payload,
            answer_any=answer_any,
        )

        if not questions:
            raise TheoryExamGenerationError(
                "AI did not generate any theory questions."
            )

        return TheoryPaper(
            instructions=(
                f"Answer any {answer_any} questions."
            ),
            questions_to_answer=answer_any,
            total_questions=len(questions),
            duration_minutes=duration,
            questions=questions,
        )

    def _normalize_questions(
        self,
        payload: Any,
        *,
        answer_any: int,
    ) -> list[TheoryQuestion]:
        """
        Convert raw AI JSON into TheoryQuestion models.
        """

        if not isinstance(payload, dict):
            raise TheoryExamGenerationError(
                "AI response must be a JSON object."
            )

        raw_questions = payload.get("questions")

        if not isinstance(raw_questions, list):
            raise TheoryExamGenerationError(
                "AI response must contain a 'questions' list."
            )

        normalized: list[TheoryQuestion] = []

        for index, raw_question in enumerate(
            raw_questions,
            start=1,
        ):
            if not isinstance(raw_question, dict):
                continue

            question_text = str(
                raw_question.get("question", "")
            ).strip()

            if not question_text:
                continue

            raw_subquestions = raw_question.get(
                "subquestions",
                [],
            )

            if not isinstance(raw_subquestions, list):
                raw_subquestions = []

            parts = self._normalize_parts(
                raw_subquestions,
            )

            if len(parts) < 2:
                raise TheoryExamGenerationError(
                    f"Theory question {index} must contain "
                    "at least two subquestions."
                )

            total_marks = sum(
                part.marks
                for part in parts
            )

            normalized.append(
                TheoryQuestion(
                    number=index,
                    title=question_text,
                    total_marks=total_marks,
                    parts=parts,
                )
            )

        return normalized

    def _normalize_parts(
        self,
        raw_parts: list[Any],
    ) -> list[TheoryPart]:
        """
        Convert AI subquestions into TheoryPart models.

        The AI prompt deliberately does not provide:
        - labels
        - marks
        - marking schemes

        Those are created by the backend.
        """

        labels = [
            "a",
            "b",
            "c",
            "d",
            "e",
        ]

        parts: list[TheoryPart] = []

        for index, raw_part in enumerate(
            raw_parts[:5],
        ):
            if isinstance(raw_part, str):
                question_text = raw_part.strip()

            elif isinstance(raw_part, dict):
                question_text = str(
                    raw_part.get(
                        "question",
                        "",
                    )
                ).strip()

            else:
                continue

            if not question_text:
                continue

            label = labels[index]

            # Backend-controlled marks.
            marks = self._default_marks(
                question_text,
            )

            # Backend-controlled marking guide.
            marking_guide = [
                "Correct and relevant answer.",
                "Clear explanation or working where required.",
            ]

            parts.append(
                TheoryPart(
                    label=label,
                    question=question_text,
                    marks=marks,
                    marking_guide=marking_guide,
                )
            )

        return parts

    @staticmethod
    def _default_marks(
        question: str,
    ) -> int:
        """
        Assign sensible default marks.

        This is intentionally conservative because
        the AI prompt does not generate marks.
        """

        text = question.lower()

        if any(
            keyword in text
            for keyword in (
                "derive",
                "prove",
                "calculate",
                "solve",
                "show all workings",
                "balance",
                "draw and label",
            )
        ):
            return 5

        return 4

    @staticmethod
    def _get_difficulty(
        analysis: Any,
    ) -> str:
        """
        Safely obtain difficulty from DocumentAnalysis.
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
