from __future__ import annotations

from datetime import UTC, datetime, timedelta
from typing import Any
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
from app.modules.knowledge_engine.repository import KnowledgeRepository


class ExamService:
    """
    Enterprise Exam Service.

    AI generates ONLY question content.

    Backend is responsible for:
    - numbering
    - marks
    - labels
    - instructions
    - total marks
    - exam metadata
    """

    def __init__(
        self,
        *,
        repository: ExamRepository,
        knowledge_repository: KnowledgeRepository,
        generator: ExamGenerator,
    ) -> None:
        self._repository = repository
        self._knowledge_repository = knowledge_repository
        self._generator = generator

    # ==========================================================
    # Helpers
    # ==========================================================

    @staticmethod
    def _build_study_content(knowledge: Any) -> str:
        analysis = {}

        if isinstance(knowledge.knowledge, dict):
            analysis = knowledge.knowledge.get("analysis", {})

        return f"""
TITLE:
{knowledge.title}

SUMMARY:
{knowledge.summary}

TOPICS:
{chr(10).join(
    f"- {topic.get('title','')}: {topic.get('content','')[:500]}"
    for topic in (knowledge.topics or [])
)}

KEY POINTS:
{chr(10).join(
    f"- {point}"
    for point in (knowledge.key_points or [])
)}

LEARNING OBJECTIVES:
{chr(10).join(
    f"- {obj.get('objective','')}"
    for obj in (knowledge.learning_objectives or [])
)}

IMPORTANT TERMS:
{", ".join(analysis.get("important_terms", []))}

Subject:
{analysis.get("subject","")}

Teaching Style:
{analysis.get("teaching_style","")}

Reasoning Depth:
{analysis.get("reasoning_depth","")}
""".strip()

    @staticmethod
    def _theory_instruction(question_count: int) -> str:
        return f"Answer any {question_count} questions."

    @staticmethod
    def _default_labels() -> list[str]:
        return ["a", "b", "c", "d", "e"]

    # ==========================================================
    # Create Exam
    # ==========================================================

    async def create_exam(
        self,
        *,
        owner_id: UUID,
        material_id: UUID,
        request: CreateExamRequest,
    ) -> ExamSession:

        knowledge = await self._knowledge_repository.get_by_material(
            material_id
        )

        if knowledge is None:
            raise ValueError(
                "Knowledge has not been generated for this material."
            )

        study_content = self._build_study_content(
            knowledge,
        )

        generated = await self._generator.generate(
            exam_type=request.exam_type,
            study_content=study_content,
            number_of_questions=request.question_count,
            difficulty=request.difficulty,
        )

        started_at = datetime.now(UTC)

        expires_at = started_at + timedelta(
            minutes=request.duration_minutes,
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
            started_at=started_at,
            expires_at=expires_at,
        )

        await self._repository.create_session(session)

        total_marks = 0

        questions = generated.get("questions", [])

        if not questions:
            raise ValueError("AI generated no questions.")

        for index, item in enumerate(questions, start=1):

            question_type = (
                QuestionType.OBJECTIVE
                if item.get("options")
                else QuestionType.THEORY
            )

            if question_type == QuestionType.OBJECTIVE:

                marks = int(item.get("marks", 2))

                question_number = index

                options = item.get("options") or []

                question = ExamQuestion(
                    session_id=session.id,
                    question_number=question_number,
                    question_type=question_type,
                    question=item.get("question", ""),
                    topic=item.get("topic", "General"),
                    difficulty=item.get(
                        "difficulty",
                        str(request.difficulty),
                    ),
                    marks=marks,
                    options=options,
                    correct_answer=item.get("correct_answer"),
                    explanation=item.get("explanation"),
                    subquestions=[],
                    marking_scheme=[],
                    model_answer=None,
                    instructions="Choose ONE correct option.",
                )

            else:

                marks = int(item.get("marks", 20))

                labelled_subquestions = []

                labels = self._default_labels()

                for sub_index, sub in enumerate(
                    item.get("subquestions", []),
                ):

                    if isinstance(sub, dict):

                        labelled_subquestions.append(
                            {
                                "label": labels[sub_index],
                                "question": sub.get(
                                    "question",
                                    "",
                                ),
                            }
                        )

                    else:

                        labelled_subquestions.append(
                            {
                                "label": labels[sub_index],
                                "question": str(sub),
                            }
                        )

                question = ExamQuestion(
                    session_id=session.id,
                    question_number=index,
                    question_type=QuestionType.THEORY,
                    question=item.get("question", ""),
                    topic=item.get("topic", "General"),
                    difficulty=item.get(
                        "difficulty",
                        str(request.difficulty),
                    ),
                    marks=marks,
                    options=[],
                    correct_answer=None,
                    explanation=None,
                    subquestions=labelled_subquestions,
                    marking_scheme=item.get(
                        "marking_scheme",
                        [],
                    ),
                    model_answer=item.get(
                        "model_answer",
                    ),
                    instructions=self._theory_instruction(
                        request.question_count
                    ),
                )

            total_marks += marks

            await self._repository.create_question(
                question
            )

        session.total_marks = total_marks

        await self._repository.update_session(
            session
        )

        await self._repository.commit()

        reloaded_session = (
            await self._repository.get_session(
                session.id
            )
        )

        if reloaded_session is None:
            raise RuntimeError(
                "Failed to reload exam session."
            )

        return reloaded_session


    # ==========================================================
    # Get Exam
    # ==========================================================

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

    # ==========================================================
    # Update Status
    # ==========================================================

    async def update_status(
        self,
        *,
        session_id: UUID,
        status: ExamStatus,
    ) -> ExamSession:

        session = await self.get_exam(
            session_id,
        )

        session.status = status

        await self._repository.update_session(
            session,
        )

        await self._repository.commit()

        refreshed = await self._repository.get_session(
            session_id,
        )

        if refreshed is None:
            raise RuntimeError(
                "Failed to reload updated session."
            )

        return refreshed

    # ==========================================================
    # Delete Exam
    # ==========================================================

    async def delete_exam(
        self,
        session_id: UUID,
    ) -> None:

        session = await self.get_exam(
            session_id,
        )

        await self._repository.delete_session(
            session,
        )

        await self._repository.commit()
