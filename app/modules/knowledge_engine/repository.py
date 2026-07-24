from __future__ import annotations

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.knowledge_engine.models import KnowledgeSource
from app.modules.knowledge_engine.models import KnowledgeStatus
from app.modules.knowledge_engine.schemas import KnowledgeCreate
from app.modules.knowledge_engine.schemas import KnowledgeUpdate


class KnowledgeRepository:
    """
    Repository responsible ONLY for database access.

    No AI.
    No business logic.
    No validation.
    """

    def __init__(self, db: AsyncSession) -> None:
        self._db = db

    async def create(
        self,
        data: KnowledgeCreate,
    ) -> KnowledgeSource:
        knowledge = KnowledgeSource(
            material_id=data.material_id,
            title=data.title,
            summary=data.summary,
            knowledge=data.knowledge,
            topics=[item.model_dump() for item in data.topics],
            glossary=[item.model_dump() for item in data.glossary],
            learning_objectives=[
                item.model_dump()
                for item in data.learning_objectives
            ],
            key_points=data.key_points,
            sample_questions=[
                item.model_dump()
                for item in data.sample_questions
            ],
            total_tokens=data.total_tokens,
            ai_provider=data.ai_provider,
            ai_model=data.ai_model,
            processing_time_ms=data.processing_time_ms,
            is_cached=data.is_cached,
            status=KnowledgeStatus.READY,
        )

        self._db.add(knowledge)

        await self._db.commit()

        await self._db.refresh(knowledge)

        return knowledge

    async def get(
        self,
        knowledge_id: UUID,
    ) -> KnowledgeSource | None:
        result = await self._db.execute(
            select(KnowledgeSource).where(
                KnowledgeSource.id == knowledge_id,
            )
        )

        return result.scalar_one_or_none()

    async def get_by_material(
        self,
        material_id: UUID,
    ) -> KnowledgeSource | None:
        result = await self._db.execute(
            select(KnowledgeSource).where(
                KnowledgeSource.material_id == material_id,
            )
        )

        return result.scalar_one_or_none()

    async def exists(
        self,
        material_id: UUID,
    ) -> bool:
        return (
            await self.get_by_material(material_id)
        ) is not None

    async def update(
        self,
        knowledge: KnowledgeSource,
        data: KnowledgeUpdate,
    ) -> KnowledgeSource:

        updates = data.model_dump(
            exclude_none=True,
        )

        for key, value in updates.items():

            if key in {
                "topics",
                "glossary",
                "learning_objectives",
                "sample_questions",
            }:
                value = [
                    item.model_dump()
                    if hasattr(item, "model_dump")
                    else item
                    for item in value
                ]

            setattr(
                knowledge,
                key,
                value,
            )

        await self._db.commit()

        await self._db.refresh(
            knowledge,
        )

        return knowledge

    async def update_status(
        self,
        material_id: UUID,
        status: KnowledgeStatus,
        error_message: str | None = None,
    ) -> KnowledgeSource | None:

        knowledge = await self.get_by_material(
            material_id,
        )

        if knowledge is None:
            return None

        knowledge.status = status
        knowledge.error_message = error_message

        await self._db.commit()

        await self._db.refresh(
            knowledge,
        )

        return knowledge

    async def delete(
        self,
        material_id: UUID,
    ) -> bool:

        knowledge = await self.get_by_material(
            material_id,
        )

        if knowledge is None:
            return False

        await self._db.delete(
            knowledge,
        )

        await self._db.commit()

        return True
