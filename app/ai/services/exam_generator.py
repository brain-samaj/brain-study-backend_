from __future__ import annotations

from typing import Any

from app.ai.client import AIClient
from app.ai.formatters import Formatter
from app.ai.prompts.objective_exam import OBJECTIVE_EXAM_PROMPT
from app.ai.prompts.theory_exam import THEORY_EXAM_PROMPT


class ExamGenerationError(Exception):
    """
    Raised when AI fails to generate a valid exam.
    """


class ExamGenerator:
    """
    Enterprise AI Exam Generator.

    Responsibilities
    ----------------
    - Generate objective or theory examinations.
    - Apply the centralized Formatter pipeline.
    - Normalize AI output into the internal exam schema.
    - Validate the final exam payload.
    """

    def __init__(
        self,
        ai_client: AIClient,
    ) -> None:
        self._client = ai_client
        self._formatter = Formatter()

    async def generate(
        self,
        *,
        exam_type: str,
        study_content: str,
        number_of_questions: int,
        difficulty: str,
    ) -> dict[str, Any]:

        exam_type = exam_type.lower().strip()
        difficulty = difficulty.lower().strip()

        if exam_type not in {"objective", "theory"}:
            raise ExamGenerationError(
                f"Unsupported exam type: {exam_type}"
            )

        if number_of_questions <= 0:
            raise ExamGenerationError(
                "Number of questions must be greater than zero."
            )

        prompt = (
            OBJECTIVE_EXAM_PROMPT
            if exam_type == "objective"
            else THEORY_EXAM_PROMPT
        )

        # --------------------------------------------------
        # Render prompt safely.
        #
        # DO NOT use str.format() here.
        #
        # The examination prompts contain LaTeX such as:
        #
        #   \frac{{2}}{{3}}
        #   \sqrt{{x+4}}
        #   \begin{{bmatrix}}
        #
        # str.format() interprets those braces as formatting
        # fields and causes:
        #
        # ValueError: unexpected '{' in field name
        #
        # We therefore replace only our known placeholders.
        # --------------------------------------------------

        rendered_prompt = prompt.replace(
            "{study_content}",
            study_content,
        ).replace(
            "{question_count_plus_one}",
            str(number_of_questions + 1),
        ).replace(
            "{question_count}",
            str(number_of_questions),
        ).replace(
            "{difficulty}",
            difficulty,
        )

        # --------------------------------------------------
        # Generate structured AI response
        # --------------------------------------------------

        payload = await self._client.generate_json(
            prompt=rendered_prompt,
        )

        # --------------------------------------------------
        # Centralized formatting pipeline
        #
        # This is intentionally done BEFORE normalization
        # so mathematical/scientific notation is preserved
        # throughout the final exam payload.
        # --------------------------------------------------

        payload = self._formatter.format_payload(payload)

        # --------------------------------------------------
        # Normalize into Brain Study schema
        # --------------------------------------------------

        payload = self._normalize_payload(
            payload,
            exam_type=exam_type,
            requested_questions=number_of_questions,
            difficulty=difficulty,
        )

        # --------------------------------------------------
        # Validate final payload
        # --------------------------------------------------

        self._validate_payload(payload)

        return payload

    # ============================================================
    # NORMALIZATION
    # ============================================================

    def _normalize_payload(
        self,
        payload: dict[str, Any],
        *,
        exam_type: str,
        requested_questions: int,
        difficulty: str,
    ) -> dict[str, Any]:

        if not isinstance(payload, dict):
            payload = {}

        questions = payload.get("questions")

        if not isinstance(questions, list):
            questions = []

        normalized: list[dict[str, Any]] = []

        # ========================================================
        # OBJECTIVE EXAM
        # ========================================================

        if exam_type == "objective":

            questions = questions[:requested_questions]

            for index, question in enumerate(
                questions,
                start=1,
            ):
                if not isinstance(question, dict):
                    question = {}

                question["question_number"] = index

                question.setdefault(
                    "topic",
                    "General",
                )

                question.setdefault(
                    "difficulty",
                    difficulty,
                )

                question.setdefault(
                    "marks",
                    2,
                )

                question.setdefault(
                    "explanation",
                    "",
                )

                options = question.get(
                    "options",
                    [],
                )

                if not isinstance(options, list):
                    options = []

                while len(options) < 4:
                    options.append("Option")

                question["options"] = options[:4]

                answer = str(
                    question.get(
                        "correct_answer",
                        "A",
                    )
                ).upper().strip()

                if answer not in {
                    "A",
                    "B",
                    "C",
                    "D",
                }:
                    answer = "A"

                question["correct_answer"] = answer

                normalized.append(question)

            payload["questions"] = normalized

            return payload

        # ========================================================
        # THEORY EXAM
        # ========================================================

        payload["exam_instruction"] = (
            f"Answer any {requested_questions} questions."
        )

        for index, question in enumerate(
            questions,
            start=1,
        ):

            if not isinstance(question, dict):
                question = {}

            question["question_number"] = index

            question.setdefault(
                "topic",
                "General",
            )

            question.setdefault(
                "difficulty",
                difficulty,
            )

            question.setdefault(
                "instructions",
                "Answer all subquestions.",
            )

            question.setdefault(
                "marks",
                20,
            )

            question.setdefault(
                "model_answer",
                "",
            )

            # ----------------------------------------------------
            # Subquestions
            # ----------------------------------------------------

            subquestions = question.get(
                "subquestions",
                [],
            )

            if not isinstance(subquestions, list):
                subquestions = []

            labels = [
                "a",
                "b",
                "c",
                "d",
                "e",
            ]

            fixed_subquestions: list[dict[str, str]] = []

            for i, sub in enumerate(
                subquestions[:5]
            ):

                if isinstance(sub, str):

                    fixed_subquestions.append(
                        {
                            "label": labels[i],
                            "question": sub,
                        }
                    )

                elif isinstance(sub, dict):

                    fixed_subquestions.append(
                        {
                            "label": str(
                                sub.get(
                                    "label",
                                    labels[i],
                                )
                            ),
                            "question": str(
                                sub.get(
                                    "question",
                                    "",
                                )
                            ),
                        }
                    )

            # Guarantee at least two subquestions.

            while len(fixed_subquestions) < 2:

                fixed_subquestions.append(
                    {
                        "label": labels[
                            len(fixed_subquestions)
                        ],
                        "question": (
                            "Explain your answer."
                        ),
                    }
                )

            question["subquestions"] = fixed_subquestions

            # ----------------------------------------------------
            # Marking scheme
            # ----------------------------------------------------

            marking_scheme = question.get(
                "marking_scheme",
                [],
            )

            if not isinstance(
                marking_scheme,
                list,
            ):
                marking_scheme = []

            fixed_scheme: list[dict[str, Any]] = []

            for item in marking_scheme:

                if isinstance(item, dict):

                    try:
                        marks = int(
                            item.get(
                                "marks",
                                2,
                            )
                        )
                    except (
                        TypeError,
                        ValueError,
                    ):
                        marks = 2

                    fixed_scheme.append(
                        {
                            "point": item.get(
                                "point",
                                "",
                            ),
                            "marks": marks,
                        }
                    )

            if not fixed_scheme:

                fixed_scheme = [
                    {
                        "point": "Correct explanation",
                        "marks": question["marks"],
                    }
                ]

            question["marking_scheme"] = fixed_scheme

            normalized.append(question)

        payload["questions"] = normalized

        return payload

    # ============================================================
    # VALIDATION
    # ============================================================

    def _validate_payload(
        self,
        payload: dict[str, Any],
    ) -> None:

        if not isinstance(payload, dict):
            raise ExamGenerationError(
                "Expected JSON object."
            )

        questions = payload.get("questions")

        if not isinstance(
            questions,
            list,
        ):
            raise ExamGenerationError(
                "'questions' must be a list."
            )

        if not questions:
            raise ExamGenerationError(
                "No questions were generated."
            )

        for question in questions:

            if not isinstance(
                question,
                dict,
            ):
                raise ExamGenerationError(
                    "Each question must be an object."
                )

            if question.get("options") is not None:
                self._validate_objective(
                    question
                )
            else:
                self._validate_theory(
                    question
                )

    # ============================================================
    # OBJECTIVE VALIDATION
    # ============================================================

    def _validate_objective(
        self,
        question: dict[str, Any],
    ) -> None:

        required = (
            "question_number",
            "question",
            "options",
            "correct_answer",
            "difficulty",
            "topic",
            "marks",
            "explanation",
        )

        for field in required:

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

        if len(question["options"]) != 4:

            raise ExamGenerationError(
                "Objective questions must contain exactly four options."
            )

        if question["correct_answer"] not in {
            "A",
            "B",
            "C",
            "D",
        }:

            raise ExamGenerationError(
                "Objective correct_answer must be A, B, C, or D."
            )

    # ============================================================
    # THEORY VALIDATION
    # ============================================================

    def _validate_theory(
        self,
        question: dict[str, Any],
    ) -> None:

        required = (
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

        for field in required:

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

        if len(
            question["subquestions"]
        ) < 2:

            raise ExamGenerationError(
                "Theory questions require at least two subquestions."
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
