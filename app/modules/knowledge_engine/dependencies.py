from __future__ import annotations

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.async_session import get_async_db
from app.modules.knowledge_engine.repository import KnowledgeRepository


def get_repository(
    db: AsyncSession = Depends(get_async_db),
) -> KnowledgeRepository:
    return KnowledgeRepository(db)
