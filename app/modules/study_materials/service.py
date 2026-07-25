from __future__ import annotations

import mimetypes
from pathlib import Path
from uuid import UUID
from uuid import uuid4

from fastapi import HTTPException
from fastapi import UploadFile
from fastapi import status

from app.ai.client import AIClient

from app.modules.auth.models import User

from app.modules.knowledge_engine.service import KnowledgeEngineService

from app.modules.study_materials.models import MaterialType
from app.modules.study_materials.models import ProcessingStatus
from app.modules.study_materials.models import StudyMaterial

from app.modules.study_materials.repository import (
    StudyMaterialRepository,
)

from app.modules.study_materials.schemas import (
    StudyMaterialCreate,
    StudyMaterialUpdate,
)


class StudyMaterialService:
    """
    Brain Study Upload Service

    Responsibilities
    ----------------
    • Upload study materials
    • Upload handwritten notes/images
    • Create topic-only materials
    • Store files safely
    • Trigger Knowledge Engine
    • CRUD operations

    This service contains NO AI logic.
    AI processing is delegated to KnowledgeEngineService.
    """

    STORAGE_DIR = Path("storage/study_materials")

    ALLOWED_EXTENSIONS = {
        ".pdf",
        ".docx",
        ".pptx",
        ".txt",
        ".md",
        ".png",
        ".jpg",
        ".jpeg",
        ".bmp",
        ".gif",
        ".webp",
    }

    MAX_FILE_SIZE = 25 * 1024 * 1024

    def __init__(
        self,
        *,
        repository: StudyMaterialRepository,
        knowledge_service: KnowledgeEngineService,
        ai_client: AIClient | None = None,
    ) -> None:

        self.repository = repository
        self.knowledge_service = knowledge_service
        self.ai_client = ai_client

        self.STORAGE_DIR.mkdir(
            parents=True,
            exist_ok=True,
        )

    # ==========================================================
    # INTERNAL HELPERS
    # ==========================================================

    def _detect_material_type(
        self,
        extension: str,
    ) -> MaterialType:

        extension = extension.lower()

        mapping = {
            ".pdf": MaterialType.PDF,
            ".docx": MaterialType.DOCX,
            ".pptx": MaterialType.PPTX,
            ".txt": MaterialType.TXT,
            ".md": MaterialType.MD,
            ".png": MaterialType.PNG,
            ".jpg": MaterialType.JPG,
            ".jpeg": MaterialType.JPEG,
            ".bmp": MaterialType.BMP,
            ".gif": MaterialType.GIF,
            ".webp": MaterialType.WEBP,
        }

        try:
            return mapping[extension]
        except KeyError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Unsupported file type.",
            )

    def _guess_mime_type(
        self,
        filename: str,
    ) -> str:

        mime, _ = mimetypes.guess_type(filename)

        return mime or "application/octet-stream"

    def _generate_filename(
        self,
        extension: str,
    ) -> str:
        return f"{uuid4().hex}{extension.lower()}"

    def _storage_path(
        self,
        filename: str,
    ) -> Path:
        return self.STORAGE_DIR / filename


    # ==========================================================
    # CREATE MATERIAL FROM TOPIC
    # ==========================================================

    async def create_from_topic(
        self,
        *,
        current_user: User,
        title: str,
        description: str,
    ) -> StudyMaterial:

        title = title.strip()

        description = description.strip()

        material = await self.repository.create(
            owner_id=current_user.id,
            data=StudyMaterialCreate(
                title=title,
                description=description,
                original_filename="Topic",
                stored_filename="topic",
                storage_path="",
                file_type=MaterialType.TOPIC,
                mime_type="text/plain",
                file_size=len(description.encode("utf-8")),
                extracted_text=description,
                page_count=1,
                word_count=len(description.split()),
            ),
        )

        material = await self.repository.update(
            material,
            StudyMaterialUpdate(
                processing_status=ProcessingStatus.PROCESSING,
            ),
        )

        try:
            await self.knowledge_service.build_from_material(
                material_id=material.id,
            )

            material = await self.repository.update(
                material,
                StudyMaterialUpdate(
                    processing_status=ProcessingStatus.READY,
                ),
            )

        except Exception as exc:

            material = await self.repository.update(
                material,
                StudyMaterialUpdate(
                    processing_status=ProcessingStatus.FAILED,
                    extraction_error=str(exc),
                ),
            )

            raise

        return material


    # ==========================================================
    # UPLOAD MATERIAL
    # ==========================================================

    async def upload(
        self,
        *,
        current_user: User,
        title: str,
        description: str | None,
        file: UploadFile,
    ) -> StudyMaterial:

        if not file.filename:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No file selected.",
            )

        extension = Path(file.filename).suffix.lower()

        if extension not in self.ALLOWED_EXTENSIONS:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Unsupported file type.",
            )

        contents = await file.read()

        if len(contents) == 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Uploaded file is empty.",
            )

        if len(contents) > self.MAX_FILE_SIZE:
            raise HTTPException(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                detail="File exceeds the maximum allowed size (25 MB).",
            )

        stored_filename = self._generate_filename(extension)

        storage_path = self._storage_path(stored_filename)

        storage_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        with storage_path.open("wb") as f:
            f.write(contents)

        material = await self.repository.create(
            owner_id=current_user.id,
            data=StudyMaterialCreate(
                title=title.strip(),
                description=description,
                original_filename=file.filename,
                stored_filename=stored_filename,
                storage_path=str(storage_path),
                file_type=self._detect_material_type(extension),
                mime_type=file.content_type
                or self._guess_mime_type(file.filename),
                file_size=len(contents),
                extracted_text="",
                page_count=None,
                word_count=0,
            ),
        )

        await self.repository.update(
            material,
            StudyMaterialUpdate(
                processing_status=ProcessingStatus.EXTRACTING,
            ),
        )

        # Reset stream so downstream services can read it again.
        file.file.seek(0)

        try:

            await self.knowledge_service.build_from_material(
                material_id=material.id,
            )

            material = await self.repository.get(material.id)

            material = await self.repository.update(
                material,
                StudyMaterialUpdate(
                    processing_status=ProcessingStatus.READY,
                ),
            )

        except Exception as exc:

            material = await self.repository.get(material.id)

            material = await self.repository.update(
                material,
                StudyMaterialUpdate(
                    processing_status=ProcessingStatus.FAILED,
                    extraction_error=str(exc),
                ),
            )

            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to process uploaded material: {exc}",
            ) from exc

        return material


    # ==========================================================
    # LIST MATERIALS
    # ==========================================================

    async def list(
        self,
        *,
        current_user: User,
        skip: int = 0,
        limit: int = 20,
    ) -> list[StudyMaterial]:

        return await self.repository.list_for_owner(
            owner_id=current_user.id,
            skip=skip,
            limit=limit,
        )

    # ==========================================================
    # GET MATERIAL
    # ==========================================================

    async def get(
        self,
        *,
        material_id: UUID,
        current_user: User,
    ) -> StudyMaterial:

        material = await self.repository.get_for_owner(
            material_id=material_id,
            owner_id=current_user.id,
        )

        if material is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Study material not found.",
            )

        return material

    # ==========================================================
    # UPDATE MATERIAL
    # ==========================================================

    async def update(
        self,
        *,
        material_id: UUID,
        current_user: User,
        payload: StudyMaterialUpdate,
    ) -> StudyMaterial:

        material = await self.get(
            material_id=material_id,
            current_user=current_user,
        )

        return await self.repository.update(
            material,
            payload,
        )

    # ==========================================================
    # DELETE MATERIAL
    # ==========================================================

    async def delete(
        self,
        *,
        material_id: UUID,
        current_user: User,
    ) -> None:

        material = await self.get(
            material_id=material_id,
            current_user=current_user,
        )

        path = Path(material.storage_path)

        if path.exists():
            path.unlink()

        await self.repository.delete(material)

    # ==========================================================
    # ARCHIVE MATERIAL
    # ==========================================================

    async def archive(
        self,
        *,
        material_id: UUID,
        current_user: User,
    ) -> bool:

        material = await self.get(
            material_id=material_id,
            current_user=current_user,
        )

        return await self.repository.archive(
            material.id,
        )

    # ==========================================================
    # REPROCESS MATERIAL
    # ==========================================================

    async def reprocess(
        self,
        *,
        material_id: UUID,
        current_user: User,
    ) -> StudyMaterial:

        material = await self.get(
            material_id=material_id,
            current_user=current_user,
        )

        await self.repository.update(
            material,
            StudyMaterialUpdate(
                processing_status=ProcessingStatus.PROCESSING,
                extraction_error=None,
            ),
        )

        try:

            await self.knowledge_service.refresh(
                material_id=material.id,
            )

            material = await self.repository.get(
                material.id,
            )

            material = await self.repository.update(
                material,
                StudyMaterialUpdate(
                    processing_status=ProcessingStatus.READY,
                ),
            )

            return material

        except Exception as exc:

            material = await self.repository.get(
                material.id,
            )

            material = await self.repository.update(
                material,
                StudyMaterialUpdate(
                    processing_status=ProcessingStatus.FAILED,
                    extraction_error=str(exc),
                ),
            )

            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to reprocess study material.",
            ) from exc

