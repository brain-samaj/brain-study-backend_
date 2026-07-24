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
from app.modules.exams.service import ExamService


# ============================================================
# Repository
# ============================================================


async def get_exam_repository(
    session: AsyncSession = Depends(
        get_async_session
    ),
) -> ExamRepository:

    return ExamRepository(
        session,
    )



# ============================================================
# AI
# ============================================================


def get_ai_client() -> AIClient:

    return AIClient()



def get_exam_generator(
    ai_client: AIClient = Depends(
        get_ai_client
    ),
) -> ExamGenerator:

    return ExamGenerator(
        ai_client,
    )



def get_theory_marker(
    ai_client: AIClient = Depends(
        get_ai_client
    ),
) -> TheoryMarker:

    return TheoryMarker(
        ai_client,
    )



# ============================================================
# Services
# ============================================================


def get_exam_service(
    repository: ExamRepository = Depends(
        get_exam_repository
    ),
    generator: ExamGenerator = Depends(
        get_exam_generator
    ),
) -> ExamService:

    return ExamService(
        repository=repository,
        generator=generator,
    )



def get_autosave_service(
    repository: ExamRepository = Depends(
        get_exam_repository
    ),
) -> ExamAutosaveService:

    return ExamAutosaveService(
        repository=repository,
    )



def get_grading_service(
    repository: ExamRepository = Depends(
        get_exam_repository
    ),
    theory_marker: TheoryMarker = Depends(
        get_theory_marker
    ),
) -> ExamGradingService:

    return ExamGradingService(
        repository=repository,
        theory_marker=theory_marker,
    )
