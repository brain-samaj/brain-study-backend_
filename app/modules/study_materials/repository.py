from __future__ import annotations

from uuid import UUID

from sqlalchemy import func
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.study_materials.models import ProcessingStatus
from app.modules.study_materials.models import StudyMaterial
from app.modules.study_materials.schemas import StudyMaterialCreate
from app.modules.study_materials.schemas import StudyMaterialUpdate


class StudyMaterialRepository:
    """
    Repository responsible ONLY for StudyMaterial persistence.

    Responsibilities
    ----------------
    - CRUD operations
    - Search
    - Ownership lookups
    - Status updates

    No business logic.
    No AI.
    No file extraction.
    """

    def __init__(
        self,
        db: AsyncSession,
    ) -> None:
        self._db = db

    async def create(
        self,
        *,
        owner_id: UUID,
        data: StudyMaterialCreate,
    ) -> StudyMaterial:

        material = StudyMaterial(
            owner_id=owner_id,
            title=data.title,
            description=data.description,
            original_filename=data.original_filename,
            stored_filename=data.stored_filename,
            storage_path=data.storage_path,
            file_type=data.file_type,
            mime_type=data.mime_type,
            file_size=data.file_size,
            extracted_text=data.extracted_text,
            page_count=data.page_count,
            word_count=data.word_count,
            processing_status=ProcessingStatus.UPLOADING,
        )

        self._db.add(material)

        await self._db.commit()

        await self._db.refresh(material)

        return material

    async def get(
        self,
        material_id: UUID,
    ) -> StudyMaterial | None:

        result = await self._db.execute(
            select(StudyMaterial).where(
                StudyMaterial.id == material_id,
            )
        )

        return result.scalar_one_or_none()

    async def get_for_owner(
        self,
        *,
        material_id: UUID,
        owner_id: UUID,
    ) -> StudyMaterial | None:

        result = await self._db.execute(
            select(StudyMaterial).where(
                StudyMaterial.id == material_id,
                StudyMaterial.owner_id == owner_id,
            )
        )

        return result.scalar_one_or_none()

    async def list_for_owner(
        self,
        *,
        owner_id: UUID,
        skip: int = 0,
        limit: int = 20,
    ) -> list[StudyMaterial]:

        result = await self._db.execute(
            select(StudyMaterial)
            .where(
                StudyMaterial.owner_id == owner_id,
                StudyMaterial.is_archived.is_(False),
            )
            .order_by(
                StudyMaterial.created_at.desc(),
            )
            .offset(skip)
            .limit(limit)
        )

        return list(result.scalars().all())

    async def count_for_owner(
        self,
        owner_id: UUID,
    ) -> int:

        result = await self._db.execute(
            select(func.count())
            .select_from(StudyMaterial)
            .where(
                StudyMaterial.owner_id == owner_id,
                StudyMaterial.is_archived.is_(False),
            )
        )

        return int(result.scalar_one())

    async def update(
        self,
        material: StudyMaterial,
        payload: StudyMaterialUpdate,
    ) -> StudyMaterial:

        updates = payload.model_dump(
            exclude_none=True,
        )

        for field, value in updates.items():
            setattr(
                material,
                field,
                value,
            )

        await self._db.commit()

        await self._db.refresh(material)

        return material

    async def update_processing_status(
        self,
        *,
        material_id: UUID,
        status: ProcessingStatus,
        extraction_error: str | None = None,
    ) -> StudyMaterial | None:

        material = await self.get(
            material_id,
        )

        if material is None:
            return None

        material.processing_status = status
        material.extraction_error = extraction_error

        await self._db.commit()

        await self._db.refresh(material)

        return material

    async def archive(
        self,
        material_id: UUID,
    ) -> bool:

        material = await self.get(
            material_id,
        )

        if material is None:
            return False

        material.is_archived = True

        await self._db.commit()

        return True

    async def delete(
        self,
        material: StudyMaterial,
    ) -> None:

        await self._db.delete(material)

        await self._db.commit()
