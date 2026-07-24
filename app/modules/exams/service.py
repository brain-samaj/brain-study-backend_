from __future__ import annotations

from datetime import UTC
from datetime import datetime
from uuid import UUID

from app.ai.services.exam_generator import ExamGenerator
from app.modules.exams.exceptions import ExamNotFoundError
from app.modules.exams.models import ExamQuestion
from app.modules.exams.models import ExamSession
from app.modules.exams.models import ExamStatus
from app.modules.exams.models import QuestionType
from app.modules.exams.repository import ExamRepository
from app.modules.exams.schemas import CreateExamRequest


class ExamService:
    """
    Main Exam Business Service.

    Responsibilities
    ----------------
    - Coordinate exam lifecycle.
    - Communicate with AI generator.
    - Create sessions.
    - Store questions.
    - Submit exams.

    Does NOT:
    - Access database directly.
    - Call AI providers directly.

    Dependencies:
        Repository
        AI Services
    """

    def __init__(
        self,
        *,
        repository: ExamRepository,
        generator: ExamGenerator,
    ) -> None:

        self._repository = repository
        self._generator = generator


    async def create_exam(
        self,
        *,
        owner_id: UUID,
        material_id: UUID,
        request: CreateExamRequest,
        study_content: str,
    ) -> ExamSession:

        generated = await self._generator.generate(
            exam_type=request.exam_type.value,
            study_content=study_content,
            number_of_questions=request.question_count,
            difficulty=request.difficulty.value,
        )


        session = ExamSession(
            owner_id=owner_id,
            material_id=material_id,
            exam_type=request.exam_type,
            difficulty=request.difficulty,
            total_questions=request.question_count,
            total_marks=0,
            duration_minutes=request.duration_minutes,
            status=ExamStatus.CREATED,
            started_at=datetime.now(
                UTC,
            ),
        )


        await self._repository.create_session(
            session,
        )


        total_marks = 0


        for item in generated["questions"]:

            question_type = (
                QuestionType.OBJECTIVE
                if "options" in item
                else QuestionType.THEORY
            )


            question = ExamQuestion(
                session_id=session.id,
                question_number=item[
                    "question_number"
                ],
                question_type=question_type,
                question=item[
                    "question"
                ],
                topic=item[
                    "topic"
                ],
                difficulty=item[
                    "difficulty"
                ],
                marks=item[
                    "marks"
                ],
                options=item.get(
                    "options",
                    [],
                ),
                correct_answer=item.get(
                    "correct_answer",
                ),
                explanation=item.get(
                    "explanation",
                ),
                subquestions=item.get(
                    "subquestions",
                    [],
                ),
                marking_scheme=item.get(
                    "marking_scheme",
                    [],
                ),
                model_answer=item.get(
                    "model_answer",
                ),
                instructions=item.get(
                    "instructions",
                ),
            )


            total_marks += (
                item["marks"]
            )


            await self._repository.create_question(
                question,
            )


        session.total_marks = total_marks

        await self._repository.commit()


        return session



    async def get_exam(
        self,
        session_id: UUID,
    ) -> ExamSession:

        session = await (
            self._repository
            .get_session(
                session_id,
            )
        )


        if session is None:

            raise ExamNotFoundError(
                "Exam session not found."
            )


        return session
