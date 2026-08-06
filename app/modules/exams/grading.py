from __future__ import annotations

from datetime import UTC, datetime
from uuid import UUID

from app.ai.services.theory_marker import TheoryMarker
from app.modules.exams.exceptions import (
    ObjectiveGradingError,
    TheoryGradingError,
)
from app.modules.exams.models import (
    ExamQuestion,
    ExamStatus,
)
from app.modules.exams.repository import ExamRepository
from app.modules.exams.result_models import ExamResult


class ExamGradingService:
    """
    Enterprise Exam Grading Engine.

    - Objective questions are marked instantly.
    - Theory questions are marked by AI.
    - Stores final results.
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
        session_id: UUID,
    ) -> ExamResult:

        session = await self._repository.get_session(session_id)

        if session is None:
            raise ValueError("Exam session not found.")

        session.status = ExamStatus.GRADING
        await self._repository.commit()

        try:
            objective_score = 0.0
            theory_score = 0.0

            correct_answers = 0
            incorrect_answers = 0
            unanswered = 0

            answers = await self._repository.get_answers_for_session(
                session.id
            )

            answers_by_question = {
                answer.question_id: answer
                for answer in answers
            }

            for question in session.questions:

                answer = answers_by_question.get(question.id)

                if answer is None:
                    answer = await self._repository.get_answer(
                        session_id=session.id,
                        question_id=question.id,
                    )

                if answer is None:
                    unanswered += 1
                    continue

                if question.question_type.value == "objective":

                    correct = self._grade_objective(
                        question,
                        answer,
                    )

                    answer.is_correct = correct

                    if correct:
                        correct_answers += 1
                        objective_score += float(question.marks)
                        answer.awarded_marks = float(question.marks)
                        answer.feedback = "Correct."
                    else:
                        incorrect_answers += 1
                        answer.awarded_marks = 0.0
                        answer.feedback = "Incorrect."

                else:

                    marks = await self._grade_theory(
                        question,
                        answer,
                    )

                    theory_score += marks

            total_score = objective_score + theory_score

            percentage = (
                (total_score / session.total_marks) * 100
                if session.total_marks
                else 0
            )

            result = ExamResult(
                session_id=session.id,
                owner_id=session.owner_id,
                material_id=session.material_id,
                score=int(round(total_score)),
                total_marks=session.total_marks,
                percentage=percentage,
                objective_score=int(round(objective_score)),
                theory_score=int(round(theory_score)),
                correct_answers=correct_answers,
                incorrect_answers=incorrect_answers,
                unanswered_questions=unanswered,
            )

            await self._repository.create_result(result)

            session.obtained_marks = int(round(total_score))
            session.percentage = percentage
            session.status = ExamStatus.GRADED
            session.submitted_at = datetime.now(UTC)

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

        if not question.correct_answer:
            raise ObjectiveGradingError(
                "Objective question has no correct answer."
            )

        return (
            answer.selected_option.strip().upper()
            ==
            question.correct_answer.strip().upper()
        )

    async def _grade_theory(
        self,
        question: ExamQuestion,
        answer,
    ) -> float:

        try:
            marking_scheme = question.marking_scheme

            if isinstance(marking_scheme, list):
                marking_scheme = "\n".join(
                    f"- {item}"
                    for item in marking_scheme
                )

            result = await self._theory_marker.mark(
                question=question.question,
                marking_scheme=marking_scheme or "",
                model_answer=question.model_answer or "",
                student_answer=answer.final_answer or "",
                total_marks=question.marks,
            )

            answer.awarded_marks = result.awarded_marks
            answer.feedback = result.feedback
            answer.reasoning = result.reasoning
            answer.corrections = result.corrections
            answer.suggestions = result.suggestions

            return float(result.awarded_marks)

        except Exception as exc:
            raise TheoryGradingError(str(exc)) from exc
