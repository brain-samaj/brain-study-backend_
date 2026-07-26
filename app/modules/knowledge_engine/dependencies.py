from __future__ import annotations

from fastapi import Depends
from sqlalchemy.orm import Session

from app.database.async_session import get_async_db
from app.modules.knowledge_engine.repository import KnowledgeRepository


def get_repository(
    db: Session = Depends(get_db),
) -> KnowledgeRepository:

    return KnowledgeRepository(db)
