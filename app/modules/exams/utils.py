from __future__ import annotations

import json
from typing import Any


class ExamFileUtils:
    """
    Utility functions for exam answer processing.
    """


    @staticmethod
    def merge_answers(
        *,
        typed_answer: str | None,
        ocr_answer: str | None,
    ) -> str:
        """
        Combine typed and handwritten OCR answers.

        Students can:
        - type everything
        - upload handwritten pages
        - mix both methods
        """

        parts: list[str] = []

        if typed_answer:

            cleaned = typed_answer.strip()

            if cleaned:

                parts.append(
                    cleaned
                )


        if ocr_answer:

            cleaned = ocr_answer.strip()

            if cleaned:

                parts.append(
                    cleaned
                )


        return "\n\n".join(
            parts
        )



class ExamScoreUtils:
    """
    Score calculation helpers.
    """


    @staticmethod
    def calculate_percentage(
        score: float,
        total_marks: float,
    ) -> float:

        if total_marks <= 0:

            return 0.0


        return round(
            (
                score
                /
                total_marks
            )
            *
            100,
            2,
        )



    @staticmethod
    def calculate_grade(
        percentage: float,
    ) -> str:

        if percentage >= 80:

            return "A"


        if percentage >= 70:

            return "B"


        if percentage >= 60:

            return "C"


        if percentage >= 50:

            return "D"


        return "F"



class ExamJSONUtils:
    """
    Safe JSON helpers for AI responses.
    """


    @staticmethod
    def parse_json(
        value: str,
    ) -> dict[str, Any]:

        data = json.loads(
            value
        )

        if not isinstance(
            data,
            dict,
        ):

            raise ValueError(
                "Expected JSON object."
            )


        return data



    @staticmethod
    def stringify(
        value: dict[str, Any],
    ) -> str:

        return json.dumps(
            value,
            ensure_ascii=False,
        )
