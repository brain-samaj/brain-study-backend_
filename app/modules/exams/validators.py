from __future__ import annotations

from uuid import UUID

from app.modules.exams.exceptions import (
    InvalidAnswerError,
    InvalidExamConfigurationError,
)


class ExamValidator:
    """
    Central Exam Validation Service.

    Responsibilities
    ----------------
    - Validate exam creation input.
    - Validate answer submissions.
    - Validate attachment ownership.
    - Prevent invalid exam states.

    This keeps validation out of:
    - routers
    - repositories
    - AI services
    """


    @staticmethod
    def validate_question_count(
        count: int,
    ) -> None:

        if count < 1:

            raise InvalidExamConfigurationError(
                "Question count must be at least 1."
            )


        if count > 100:

            raise InvalidExamConfigurationError(
                "Question count cannot exceed 100."
            )



    @staticmethod
    def validate_duration(
        duration_minutes: int,
    ) -> None:

        if duration_minutes < 1:

            raise InvalidExamConfigurationError(
                "Duration must be greater than zero."
            )


        if duration_minutes > 300:

            raise InvalidExamConfigurationError(
                "Maximum exam duration is 300 minutes."
            )



    @staticmethod
    def validate_objective_answer(
        selected_option: str | None,
    ) -> None:

        if not selected_option:

            raise InvalidAnswerError(
                "Objective answer cannot be empty."
            )


        option = (
            selected_option
            .strip()
            .upper()
        )


        if option not in {
            "A",
            "B",
            "C",
            "D",
        }:

            raise InvalidAnswerError(
                "Invalid objective option."
            )



    @staticmethod
    def validate_theory_answer(
        answer: str | None,
    ) -> None:

        if answer is None:

            raise InvalidAnswerError(
                "Theory answer is required."
            )


        if len(
            answer.strip()
        ) == 0:

            raise InvalidAnswerError(
                "Theory answer cannot be empty."
            )


        if len(answer) > 50000:

            raise InvalidAnswerError(
                "Answer exceeds maximum length."
            )



    @staticmethod
    def validate_uuid(
        value: UUID | None,
    ) -> None:

        if value is None:

            raise InvalidExamConfigurationError(
                "Invalid identifier."
            )



    @staticmethod
    def validate_attachment(
        *,
        file_size: int,
        mime_type: str,
    ) -> None:

        max_size = (
            10
            *
            1024
            *
            1024
        )


        if file_size > max_size:

            raise InvalidAnswerError(
                "Attachment exceeds 10MB limit."
            )


        allowed = {
            "image/jpeg",
            "image/png",
            "application/pdf",
        }


        if mime_type not in allowed:

            raise InvalidAnswerError(
                "Unsupported attachment type."
            )
