from __future__ import annotations

from app.modules.exams.grading import ExamGradingEngine


class ExamService:

    def __init__(
        self,
        repository,
        ai_marker,
    ):
        self.repository = repository
        self.ai_marker = ai_marker

    ###########################################################
    # AUTOSAVE
    ###########################################################

    async def autosave_objective(
        self,
        *,
        session_id,
        answers: dict,
    ):
        return True

    async def autosave_theory(
        self,
        *,
        session_id,
        answers: dict,
    ):
        return True

    async def save_single_theory_answer(
        self,
        *,
        session_id,
        question_number: int,
        answer: str,
    ):
        return True

    async def process_theory_answer(
        self,
        *,
        session_id,
        question_number: int,
    ):
        return True

    ###########################################################
    # OBJECTIVE SUBMISSION
    ###########################################################

    async def submit_objective_exam(
        self,
        *,
        session_id,
        student_answers: dict,
    ):

        session = self.repository.get_session(session_id)

        if session is None:
            raise ValueError("Exam session not found.")

        questions = self.repository.get_questions(session_id)

        result = ExamGradingEngine.grade_objective(
            questions=questions,
            student_answers=student_answers,
        )

        if hasattr(self.repository, "save_objective_result"):
            self.repository.save_objective_result(
                session=session,
                result=result,
                submitted_answers=student_answers,
            )

        return result

    ###########################################################
    # THEORY SUBMISSION
    ###########################################################

    async def submit_theory_exam(
        self,
        *,
        session_id,
        submitted_answers: dict,
    ):

        session = self.repository.get_session(session_id)

        if session is None:
            raise ValueError("Exam session not found.")

        questions = self.repository.get_questions(session_id)

        required = getattr(
            session,
            "required_questions",
            len(questions),
        )

        accepted_answers = {}

        ignored_questions = []

        ordered_numbers = sorted(
            int(number)
            for number in submitted_answers.keys()
        )

        for number in ordered_numbers:

            if len(accepted_answers) >= required:

                ignored_questions.append(number)

                continue

            accepted_answers[str(number)] = submitted_answers[str(number)]

        ai_marks = {}

        for question in questions:

            key = str(question.question_number)

            if key not in accepted_answers:
                continue

            ai_marks[key] = await self.ai_marker.mark_theory_answer(
                question=question,
                student_answer=accepted_answers[key],
            )

        result = ExamGradingEngine.grade_theory(
            question_limit=required,
            generated_questions=questions,
            ai_marks=ai_marks,
        )

        result["ignored_questions"] = ignored_questions
        result["accepted_answers"] = len(accepted_answers)
        result["submitted_answers"] = len(submitted_answers)

        if ignored_questions:

            result["warning"] = (
                "You answered more questions than instructed. "
                "Only the first required questions were marked."
            )

        if hasattr(self.repository, "save_theory_result"):
            self.repository.save_theory_result(
                session=session,
                result=result,
                submitted_answers=accepted_answers,
            )

        return result

    ###########################################################
    # COMPLETE SUBMISSION
    ###########################################################

    async def submit_complete_exam(
        self,
        *,
        session_id,
    ):
        return self.repository.get_result(session_id)

    ###########################################################
    # REGENERATE
    ###########################################################

    async def regenerate_exam(
        self,
        *,
        session_id,
    ):
        return {
            "message": "Regeneration endpoint is not yet implemented.",
            "session_id": str(session_id),
        }

