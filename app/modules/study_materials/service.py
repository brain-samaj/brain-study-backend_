from __future__ import annotations

from pathlib import Path
from uuid import UUID, uuid4

from fastapi import HTTPException, UploadFile, status

from app.modules.auth.models import User
from app.modules.knowledge_engine.repository import KnowledgeRepository
from app.modules.study_materials.models import StudyMaterial
from app.modules.study_materials.repository import StudyMaterialRepository
from app.modules.study_materials.schemas import (
    StudyMaterialCreate,
    StudyMaterialUpdate,
)


class StudyMaterialService:
    """
    Study Material Service

    Responsibilities
    ----------------
    • Create study kits from a typed topic
    • Upload study materials
    • Automatically send everything to the
      Knowledge Engine
    • Keep StudyMaterial and KnowledgeSource
      synchronized
    """

    STORAGE_DIR = Path("storage/study_materials")

    ALLOWED_EXTENSIONS = {
        ".pdf",
        ".docx",
        ".pptx",
        ".txt",
        ".rtf",
        ".png",
        ".jpg",
        ".jpeg",
    }

    MAX_FILE_SIZE = 25 * 1024 * 1024  # 25 MB

    def __init__(
        self,
        repository: StudyMaterialRepository,
        knowledge_repository: KnowledgeRepository,
    ):
        self.repository = repository
        self.knowledge_repository = knowledge_repository

        self.STORAGE_DIR.mkdir(
            parents=True,
            exist_ok=True,
        )

    async def create_from_topic(
        self,
        *,
        current_user: User,
        title: str,
        subject: str,
        topic_description: str,
    ) -> StudyMaterial:
        """
        Create a study kit from a typed topic.
        """

        title = title.strip()
        topic_description = topic_description.strip()

        if len(title) < 2:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Title is required.",
            )

        if len(topic_description) < 10:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Please describe your study topic.",
            )

        material = StudyMaterial(
            user_id=current_user.id,
            title=title,
            description=topic_description,
            original_filename="Topic",
            stored_filename="topic",
            mime_type="text/plain",
            file_extension=".topic",
            file_size=len(topic_description.encode("utf-8")),
            storage_path="",
            extracted_text=topic_description,
            ai_processed=False,
        )

        material = self.repository.create(material)

        await self.knowledge_repository.create_topic(
            user_id=current_user.id,
            title=title,
            subject=subject,
            topic_description=topic_description,
        )

        material.ai_processed = True

        return self.repository.update(material)

    async def upload(
        self,
        *,
        current_user: User,
        metadata: StudyMaterialCreate,
        file: UploadFile,
    ) -> StudyMaterial:
        """
        Upload a study material and automatically send
        it to the Knowledge Engine.
        """

        extension = Path(file.filename).suffix.lower()

        if extension not in self.ALLOWED_EXTENSIONS:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Unsupported file type.",
            )

        contents = await file.read()

        if len(contents) > self.MAX_FILE_SIZE:
            raise HTTPException(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                detail="File exceeds the maximum allowed size.",
            )

        stored_filename = f"{uuid4()}{extension}"

        storage_path = self.STORAGE_DIR / stored_filename

        with storage_path.open("wb") as output:
            output.write(contents)

        # Reset pointer so the Knowledge Engine
        # can read the uploaded file.
        file.file.seek(0)

        material = StudyMaterial(
            user_id=current_user.id,
            title=metadata.title.strip(),
            description=metadata.description,
            original_filename=file.filename,
            stored_filename=stored_filename,
            mime_type=file.content_type or "application/octet-stream",
            file_extension=extension,
            file_size=len(contents),
            storage_path=str(storage_path),
            extracted_text=None,
            ai_processed=False,
        )

        material = self.repository.create(material)

        await self.knowledge_repository.save_document(
            user_id=current_user.id,
            file=file,
        )

        material.ai_processed = True

        return self.repository.update(material)

    def list(
        self,
        *,
        current_user: User,
        skip: int = 0,
        limit: int = 20,
    ) -> list[StudyMaterial]:
        """
        List all study materials belonging
        to the current user.
        """

        return self.repository.list_by_user(
            current_user.id,
            skip,
            limit,
        )

    def get(
        self,
        *,
        material_id: UUID,
        current_user: User,
    ) -> StudyMaterial:
        """
        Retrieve a single study material.
        """

        material = self.repository.get_by_user(
            material_id,
            current_user.id,
        )

        if material is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Study material not found.",
            )

        return material

    def update(
        self,
        *,
        material_id: UUID,
        current_user: User,
        payload: StudyMaterialUpdate,
    ) -> StudyMaterial:
        """
        Update a study material.
        """

        material = self.get(
            material_id=material_id,
            current_user=current_user,
        )

        if payload.title is not None:
            material.title = payload.title.strip()

        if payload.description is not None:
            material.description = payload.description

        return self.repository.update(material)

    def delete(
        self,
        *,
        material_id: UUID,
        current_user: User,
    ) -> None:
        """
        Delete a study material.

        This removes the uploaded file from storage
        and deletes the StudyMaterial record.

        (Knowledge Engine records remain available
        for previously generated learning content.)
        """

        material = self.get(
            material_id=material_id,
            current_user=current_user,
        )

        storage_file = Path(material.storage_path)

        if (
            material.storage_path
            and storage_file.exists()
        ):
            storage_file.unlink()

        self.repository.delete(material)
