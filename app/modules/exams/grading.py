from __future__ import annotations

from dataclasses import dataclass
from typing import Any


GRADE_SCALE = (
    (70, "A"),
    (60, "B"),
    (50, "C"),
    (45, "D"),
    (40, "E"),
    (0, "F"),
)


@dataclass(slots=True)
class ObjectiveQuestionResult:
    question_number: int
    is_answered: bool
    is_correct: bool
    awarded_marks: float
    max_marks: float
    correct_answer: Any
    student_answer: Any
    explanation: str | None = None


@dataclass(slots=True)
class TheoryQuestionResult:
    question_number: int
    is_answered: bool
    awarded_marks: float
    max_marks: float
    feedback: str
    marking_scheme: dict


class ExamGradingEngine:

    @staticmethod
    def grade_objective(
        *,
        questions: list,
        student_answers: dict,
    ) -> dict:

        results = []

        total_score = 0.0
        total_possible = 0.0

        for question in questions:

            max_marks = float(question.marks)
            total_possible += max_marks

            answer = student_answers.get(str(question.question_number))

            answered = answer is not None

            correct = answered and answer == question.answer["correct"]

            awarded = max_marks if correct else 0.0

            total_score += awarded

            results.append(
                ObjectiveQuestionResult(
                    question_number=question.question_number,
                    is_answered=answered,
                    is_correct=correct,
                    awarded_marks=awarded,
                    max_marks=max_marks,
                    correct_answer=question.answer["correct"],
                    student_answer=answer,
                    explanation=question.explanation,
                )
            )

        percentage = (
            total_score / total_possible * 100
            if total_possible
            else 0
        )

        grade = ExamGradingEngine.grade_letter(
            percentage
        )

        return {
            "score": total_score,
            "total": total_possible,
            "percentage": round(
                percentage,
                2,
            ),
            "grade": grade,
            "results": results,
            "answered": len(student_answers),
            "unanswered": len(questions) - len(student_answers),
        }


    @staticmethod
    def grade_theory(
        *,
        question_limit: int,
        generated_questions: list,
        ai_marks: dict,
    ) -> dict:

        results = []

        total = 0.0

        max_total = 0.0

        marked = 0

        ordered = sorted(
            generated_questions,
            key=lambda q: q.question_number,
        )

        for question in ordered:

            if marked >= question_limit:
                break

            key = str(question.question_number)

            mark = ai_marks.get(
                key,
            )

            max_marks = float(question.marks)

            max_total += max_marks

            if mark is None:

                results.append(
                    TheoryQuestionResult(
                        question_number=question.question_number,
                        is_answered=False,
                        awarded_marks=0,
                        max_marks=max_marks,
                        feedback="Question not answered.",
                        marking_scheme=question.marking_scheme,
                    )
                )

                marked += 1

                continue

            awarded = float(
                mark["score"]
            )

            total += awarded

            results.append(
                TheoryQuestionResult(
                    question_number=question.question_number,
                    is_answered=True,
                    awarded_marks=awarded,
                    max_marks=max_marks,
                    feedback=mark["feedback"],
                    marking_scheme=question.marking_scheme,
                )
            )

            marked += 1

        percentage = (
            total / max_total * 100
            if max_total
            else 0
        )

        grade = ExamGradingEngine.grade_letter(
            percentage
        )

        return {
            "score": total,
            "total": max_total,
            "percentage": round(
                percentage,
                2,
            ),
            "grade": grade,
            "results": results,
            "required_questions": question_limit,
        }


    @staticmethod
    def grade_letter(
        percentage: float,
    ) -> str:

        for cutoff, letter in GRADE_SCALE:

            if percentage >= cutoff:
                return letter

        return "F"

