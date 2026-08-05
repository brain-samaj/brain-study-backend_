from __future__ import annotations

from datetime import UTC, datetime, timedelta
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
    Main business service for exams.
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

    async def create_exam(
        self,
        *,
        owner_id: UUID,
        material_id: UUID,
        request: CreateExamRequest,
    ) -> ExamSession:
        """
        Create an exam from the Knowledge Engine instead of raw material.
        """

        knowledge = await self._knowledge_repository.get_by_material(
            material_id
        )

        if knowledge is None:
            raise ValueError(
                "Knowledge has not been generated for this material."
            )

        analysis = {}

        if isinstance(knowledge.knowledge, dict):
            analysis = knowledge.knowledge.get("analysis", {})

        study_content = f"""
TITLE:
{knowledge.title}

SUMMARY:
{knowledge.summary}

TOPICS:
{chr(10).join(
    f"- {topic.get('title', '')}: {topic.get('content', '')[:500]}"
    for topic in (knowledge.topics or [])
)}

KEY POINTS:
{chr(10).join(
    f"- {point}"
    for point in (knowledge.key_points or [])
)}

LEARNING OBJECTIVES:
{chr(10).join(
    f"- {obj.get('objective', '')}"
    for obj in (knowledge.learning_objectives or [])
)}

IMPORTANT TERMS:
{", ".join(
    analysis.get("important_terms", [])
)}

EDUCATIONAL ANALYSIS:
Subject: {analysis.get("subject", "")}
Teaching Style: {analysis.get("teaching_style", "")}
Reasoning Depth: {analysis.get("reasoning_depth", "")}
Requires Formulae: {analysis.get("requires_formulae", False)}
Requires Calculations: {analysis.get("requires_calculations", False)}
Needs Worked Examples: {analysis.get("needs_worked_examples", False)}
Needs Step-by-Step: {analysis.get("needs_step_by_step", False)}
""".strip()

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

        # Reload the session with relationships already loaded
        reloaded_session = await self._repository.get_session(
            session.id
        )

        if reloaded_session is None:
            raise RuntimeError(
                "Failed to reload newly created exam session."
            )

        return reloaded_session

    async def get_exam(
        self,
        session_id: UUID,
    ) -> ExamSession:

        session = await self._repository.get_session(session_id)

        if session is None:
            raise ExamNotFoundError(
                "Exam session not found."
            )

        return session
