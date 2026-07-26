from __future__ import annotations

from datetime import UTC
from datetime import datetime
from uuid import UUID

from app.ai.services.exam_generator import ExamGenerator
from app.modules.exams.exceptions import ExamNotFoundError
from app.modules.exams.models import (
    ExamQuestion,
    ExamSession,
    ExamStatus,
    QuestionType,
)
from app.modules.exams.repository import ExamRepository
from app.modules.exams.schemas import CreateExamRequest


class ExamService:
    """
    Main business service for exams.
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
    ) -> ExamSession:
        """
        Create an exam directly from the stored study material.
        """

study_material = await self._repository.get_study_material(material_id)

        if material is None:
            raise ValueError("Study material not found.")

        study_content = (
            material.extracted_text
            or material.description
            or ""
        ).strip()

        if not study_content:
            raise ValueError(
                "Study material contains no extracted text."
            )

        generated = await self._generator.generate(
            exam_type=request.exam_type,
            study_content=study_content,
            number_of_questions=request.question_count,
            difficulty=request.difficulty,
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
            started_at=datetime.now(UTC),
        )

        await self._repository.create_session(session)

        total_marks = 0

        for item in generated["questions"]:

            question_type = (
                QuestionType.OBJECTIVE
                if item.get("options")
                else QuestionType.THEORY
            )

            marks = int(item.get("marks", 1))
            total_marks += marks

            question = ExamQuestion(
                session_id=session.id,
                question_number=item["question_number"],
                question_type=question_type,
                question=item["question"],
                topic=item.get("topic", "General"),
                difficulty=item.get(
                    "difficulty",
                    str(request.difficulty),
                ),
                marks=marks,
                options=item.get("options", []),
                correct_answer=item.get("correct_answer"),
                explanation=item.get("explanation"),
                subquestions=item.get("subquestions", []),
                marking_scheme=item.get("marking_scheme", []),
                model_answer=item.get("model_answer"),
                instructions=item.get("instructions"),
            )

            await self._repository.create_question(question)

        session.total_marks = total_marks

        await self._repository.update_session(session)
        await self._repository.commit()

        return session

    async def get_exam(
        self,
        session_id: UUID,
    ) -> ExamSession:

        session = await self._repository.get_session(
            session_id
        )

        if session is None:
            raise ExamNotFoundError(
                "Exam session not found."
            )

        return session
