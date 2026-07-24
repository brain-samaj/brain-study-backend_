from __future__ import annotations

from datetime import UTC
from datetime import datetime
from datetime import timedelta
from uuid import UUID

from app.ai.services.exam_generator import ExamGenerator
from app.modules.exams.models import (
    ExamDifficulty,
    ExamQuestion,
    ExamSession,
    ExamStatus,
    ExamType,
    QuestionType,
)
from app.modules.exams.repository import ExamRepository
from app.modules.knowledge_engine.service import KnowledgeEngineService
from app.modules.study_materials.repository import StudyMaterialRepository


class ExamGenerationError(Exception):
    """Raised when exam generation fails."""


class ExamSessionGenerator:
    """
    Creates a complete exam session.

    Flow
    ----
    Study Material
        ↓
    Knowledge Engine
        ↓
    AI Exam Generator
        ↓
    Exam Session
        ↓
    Exam Questions
        ↓
    Persist
    """

    def __init__(
        self,
        *,
        repository: ExamRepository,
        material_repository: StudyMaterialRepository,
        knowledge_service: KnowledgeEngineService,
        exam_generator: ExamGenerator,
    ) -> None:
        self._repository = repository
        self._materials = material_repository
        self._knowledge = knowledge_service
        self._generator = exam_generator

    async def generate(
        self,
        *,
        owner_id: UUID,
        material_id: UUID,
        exam_type: ExamType,
        difficulty: ExamDifficulty,
        question_count: int,
        duration_minutes: int,
    ) -> ExamSession:
        """
        Generate and persist a new exam session.
        """

        material = await self._materials.get_for_owner(
            material_id=material_id,
            owner_id=owner_id,
        )

        if material is None:
            raise ExamGenerationError(
                "Study material not found."
            )

        knowledge = await self._knowledge.get(
            material_id=material.id,
        )

        if knowledge is None:
            knowledge = await self._knowledge.build_from_material(
                material_id=material.id,
            )

        payload = await self._generator.generate(
            exam_type=exam_type.value,
            study_content=knowledge.summary,
            number_of_questions=question_count,
            difficulty=difficulty.value,
        )

        session = ExamSession(
            owner_id=owner_id,
            material_id=material.id,
            exam_type=exam_type,
            difficulty=difficulty,
            total_questions=question_count,
            duration_minutes=duration_minutes,
            status=ExamStatus.IN_PROGRESS,
            started_at=datetime.now(UTC),
            expires_at=datetime.now(UTC)
            + timedelta(minutes=duration_minutes),
        )

        await self._repository.create_session(
            session,
        )

        questions: list[ExamQuestion] = []

        total_marks = 0

        for item in payload["questions"]:

            marks = int(item.get("marks", 1))

            total_marks += marks

            questions.append(
                ExamQuestion(
                    session_id=session.id,
                    question_number=item["question_number"],
                    question_type=(
                        QuestionType.OBJECTIVE
                        if exam_type == ExamType.OBJECTIVE
                        else QuestionType.THEORY
                    ),
                    topic=item["topic"],
                    difficulty=item["difficulty"],
                    question=item["question"],
                    options=item.get("options"),
                    correct_answer=item.get(
                        "correct_answer"
                    ),
                    explanation=item.get(
                        "explanation"
                    ),
                    subquestions=item.get(
                        "subquestions"
                    ),
                    marking_scheme=item.get(
                        "marking_scheme"
                    ),
                    model_answer=item.get(
                        "model_answer"
                    ),
                    instructions=item.get(
                        "instructions"
                    ),
                    marks=marks,
                )
            )

        session.total_marks = total_marks

        await self._repository.create_questions(
            questions,
        )

        await self._repository.commit()

        return await self._repository.get_session(
            session.id,
        )
