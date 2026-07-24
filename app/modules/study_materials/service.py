from __future__ import annotations

from pathlib import Path
from uuid import UUID

from fastapi import UploadFile

from app.modules.knowledge_engine.service import KnowledgeEngineService
from app.modules.study_materials.models import ProcessingStatus
from app.modules.study_materials.models import StudyMaterial
from app.modules.study_materials.repository import StudyMaterialRepository
from app.modules.study_materials.schemas import StudyMaterialCreate
from app.modules.study_materials.schemas import StudyMaterialUpdate


class StudyMaterialService:
    """
    Enterprise Study Material Service.

    Responsibilities
    ----------------
    - Upload study materials
    - Read study materials
    - Update study materials
    - Archive/Delete study materials
    - Trigger Knowledge Engine

    NOT Responsible For
    -------------------
    - AI Prompting
    - AI Generation
    - Exam Generation
    - Flashcards
    - Summaries
    """

    def __init__(
        self,
        repository: StudyMaterialRepository,
        knowledge_service: KnowledgeEngineService,
    ) -> None:
        self._repository = repository
        self._knowledge_service = knowledge_service

    async def create(
        self,
        *,
        owner_id: UUID,
        file: UploadFile,
        stored_filename: str,
        storage_path: str,
        extracted_text: str,
        page_count: int | None,
    ) -> StudyMaterial:
        """
        Persist uploaded study material and immediately
        build the Knowledge Engine.
        """

        suffix = Path(file.filename or "").suffix.lower().replace(".", "")

        material = await self._repository.create(
            owner_id=owner_id,
            data=StudyMaterialCreate(
                title=Path(file.filename or "Untitled").stem,
                description=None,
                original_filename=file.filename or "Untitled",
                stored_filename=stored_filename,
                storage_path=storage_path,
                file_type=suffix,
                mime_type=file.content_type or "application/octet-stream",
                file_size=0,
                extracted_text=extracted_text,
                page_count=page_count,
                word_count=len(extracted_text.split()),
            ),
        )

        await self._repository.update_processing_status(
            material_id=material.id,
            status=ProcessingStatus.PROCESSING,
        )

        try:
            await self._knowledge_service.build_from_material(
                material_id=material.id,
            )

            await self._repository.update_processing_status(
                material_id=material.id,
                status=ProcessingStatus.READY,
            )

        except Exception as exc:

            await self._repository.update_processing_status(
                material_id=material.id,
                status=ProcessingStatus.FAILED,
                extraction_error=str(exc),
            )

            raise

        return material

    async def get(
        self,
        *,
        material_id: UUID,
        owner_id: UUID,
    ) -> StudyMaterial | None:

        return await self._repository.get_for_owner(
            material_id=material_id,
            owner_id=owner_id,
        )

    async def list(
        self,
        *,
        owner_id: UUID,
        skip: int = 0,
        limit: int = 20,
    ) -> list[StudyMaterial]:

        return await self._repository.list_for_owner(
            owner_id=owner_id,
            skip=skip,
            limit=limit,
        )

    async def count(
        self,
        owner_id: UUID,
    ) -> int:

        return await self._repository.count_for_owner(
            owner_id,
        )

    async def update(
        self,
        *,
        material: StudyMaterial,
        payload: StudyMaterialUpdate,
    ) -> StudyMaterial:

        return await self._repository.update(
            material,
            payload,
        )

    async def archive(
        self,
        *,
        material_id: UUID,
    ) -> bool:

        return await self._repository.archive(
            material_id,
        )

    async def delete(
        self,
        *,
        material: StudyMaterial,
    ) -> None:

        await self._repository.delete(
            material,
        )
