from __future__ import annotations

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.ai.client import AIClient
from app.ai.services.exam_generator import ExamGenerator
from app.ai.services.theory_marker import TheoryMarker
from app.database.async_session import get_async_session

from app.modules.exams.autosave import ExamAutosaveService
from app.modules.exams.grading import ExamGradingService
from app.modules.exams.repository import ExamRepository
from app.modules.exams.review import ExamReviewService
from app.modules.exams.service import ExamService

from app.modules.knowledge_engine.repository import (
    KnowledgeRepository,
)


# ============================================================
# DATABASE
# ============================================================

async def get_exam_repository(
    session: AsyncSession = Depends(get_async_session),
) -> ExamRepository:
    return ExamRepository(session)


async def get_knowledge_repository(
    session: AsyncSession = Depends(get_async_session),
) -> KnowledgeRepository:
    return KnowledgeRepository(session)


# ============================================================
# AI
# ============================================================

def get_ai_client() -> AIClient:
    return AIClient()


def get_exam_generator(
    ai_client: AIClient = Depends(get_ai_client),
) -> ExamGenerator:
    return ExamGenerator(ai_client)


def get_theory_marker(
    ai_client: AIClient = Depends(get_ai_client),
) -> TheoryMarker:
    return TheoryMarker(ai_client)


# ============================================================
# SERVICES
# ============================================================

def get_exam_service(
    repository: ExamRepository = Depends(get_exam_repository),
    knowledge_repository: KnowledgeRepository = Depends(
        get_knowledge_repository
    ),
    generator: ExamGenerator = Depends(get_exam_generator),
) -> ExamService:
    return ExamService(
        repository=repository,
        knowledge_repository=knowledge_repository,
        generator=generator,
    )


def get_autosave_service(
    repository: ExamRepository = Depends(get_exam_repository),
) -> ExamAutosaveService:
    return ExamAutosaveService(
        repository=repository,
    )


def get_grading_service(
    repository: ExamRepository = Depends(get_exam_repository),
    theory_marker: TheoryMarker = Depends(get_theory_marker),
) -> ExamGradingService:
    return ExamGradingService(
        repository=repository,
        theory_marker=theory_marker,
    )


def get_review_service(
    session: AsyncSession = Depends(get_async_session),
) -> ExamReviewService:
    return ExamReviewService(session)

