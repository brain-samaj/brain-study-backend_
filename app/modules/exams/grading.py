from __future__ import annotations

from datetime import UTC
from datetime import datetime

from app.ai.services.theory_marker import TheoryMarker

from app.modules.exams.exceptions import (
    ObjectiveGradingError,
    TheoryGradingError,
)
from app.modules.exams.models import (
    ExamQuestion,
)
from app.modules.exams.models import (
    ExamStatus,
)
from app.modules.exams.repository import ExamRepository
from app.modules.exams.result_models import ExamResult


class ExamGradingService:
    """
    Enterprise Exam Grading Engine.

    Responsibilities
    ----------------
    Objective:
        - Instant backend marking.

    Theory:
        - AI evaluation through TheoryMarker.

    Final:
        - Calculate score.
        - Save ExamResult.
        - Update session state.

    The frontend never performs grading.
    """

    def __init__(
        self,
        *,
        repository: ExamRepository,
        theory_marker: TheoryMarker,
    ) -> None:

        self._repository = repository
        self._theory_marker = theory_marker


    async def grade_session(
        self,
        *,
        session_id,
    ) -> ExamResult:

        session = await self._repository.get_session(
            session_id,
        )

        if session is None:
            raise ValueError(
                "Exam session not found."
            )

        session.status = ExamStatus.GRADING

        await self._repository.commit()

        try:

            objective_score = 0
            theory_score = 0

            correct_answers = 0
            incorrect_answers = 0
            unanswered = 0

            for question in session.questions:

                answer = question.answer

                if answer is None:

                    unanswered += 1
                    continue


                if question.question_type.value == "objective":

                    result = (
                        self._grade_objective(
                            question,
                            answer,
                        )
                    )

                    if result:

                        correct_answers += 1

                        objective_score += (
                            question.marks
                        )

                    else:

                        incorrect_answers += 1


                else:

                    marks = (
                        await self._grade_theory(
                            question,
                            answer,
                        )
                    )

                    theory_score += marks


            total_score = (
                objective_score
                +
                theory_score
            )


            percentage = (
                total_score
                /
                session.total_marks
                *
                100
                if session.total_marks
                else 0
            )


            result = ExamResult(
                session_id=session.id,
                owner_id=session.owner_id,
                material_id=session.material_id,
                score=int(total_score),
                total_marks=session.total_marks,
                percentage=percentage,
                objective_score=int(
                    objective_score
                ),
                theory_score=int(
                    theory_score
                ),
                correct_answers=correct_answers,
                incorrect_answers=incorrect_answers,
                unanswered_questions=unanswered,
            )


            await self._repository.create_result(
                result,
            )


            session.obtained_marks = int(
                total_score
            )

            session.percentage = percentage

            session.status = (
                ExamStatus.GRADED
            )

            session.submitted_at = (
                datetime.now(
                    UTC,
                )
            )

            await self._repository.commit()

            return result


        except Exception:

            session.status = ExamStatus.FAILED

            await self._repository.commit()

            raise


    def _grade_objective(
        self,
        question: ExamQuestion,
        answer,
    ) -> bool:

        if not answer.selected_option:
            return False

        return (
            answer.selected_option.strip()
            ==
            question.correct_answer.strip()
        )


    async def _grade_theory(
        self,
        question: ExamQuestion,
        answer,
    ) -> float:

        try:

            result = await self._theory_marker.mark(
                question=question.question,
                marking_scheme=(
                    question.marking_scheme
                ),
                model_answer=(
                    question.model_answer
                ),
                student_answer=(
                    answer.final_answer
                ),
                total_marks=(
                    question.marks
                ),
            )

            answer.awarded_marks = (
                result.awarded_marks
            )

            answer.feedback = (
                result.feedback
            )

            answer.reasoning = (
                result.reasoning
            )

            answer.corrections = (
                result.corrections
            )

            answer.suggestions = (
                result.suggestions
            )

            return result.awarded_marks


        except Exception as exc:

            raise TheoryGradingError(
                str(exc)
            ) from exc
