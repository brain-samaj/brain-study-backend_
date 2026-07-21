from __future__ import annotations

import shutil
from pathlib import Path
from uuid import uuid4

from fastapi import HTTPException
from fastapi import UploadFile
from fastapi import status

from app.modules.auth.models import User
from app.modules.study_materials.models import StudyMaterial
from app.modules.study_materials.repository import StudyMaterialRepository
from app.modules.study_materials.schemas import StudyMaterialCreate
from app.modules.study_materials.schemas import StudyMaterialUpdate


class StudyMaterialService:
    """
    Business logic for Study Materials.
    """

    ALLOWED_EXTENSIONS = {
        ".pdf",
        ".docx",
        ".pptx",
        ".txt",
    }

    MAX_FILE_SIZE = 25 * 1024 * 1024  # 25 MB

    STORAGE_DIR = Path("storage/study_materials")

    def __init__(
        self,
        repository: StudyMaterialRepository,
    ):
        self.repository = repository
        self.STORAGE_DIR.mkdir(
            parents=True,
            exist_ok=True,
        )

    def upload(
        self,
        *,
        current_user: User,
        metadata: StudyMaterialCreate,
        file: UploadFile,
    ) -> StudyMaterial:

        extension = Path(file.filename).suffix.lower()

        if extension not in self.ALLOWED_EXTENSIONS:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Unsupported file type.",
            )

        contents = file.file.read()

        if len(contents) > self.MAX_FILE_SIZE:
            raise HTTPException(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                detail="File exceeds maximum size.",
            )

        stored_filename = f"{uuid4()}{extension}"

        storage_path = (
            self.STORAGE_DIR / stored_filename
        )

        with open(storage_path, "wb") as output:
            output.write(contents)

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

        return self.repository.create(material)

    def list(
        self,
        *,
        current_user: User,
        skip: int = 0,
        limit: int = 20,
    ):
        return self.repository.list_by_user(
            current_user.id,
            skip,
            limit,
        )

    def get(
        self,
        *,
        material_id,
        current_user: User,
    ):

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
        material_id,
        current_user: User,
        payload: StudyMaterialUpdate,
    ):

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
        material_id,
        current_user: User,
    ):

        material = self.get(
            material_id=material_id,
            current_user=current_user,
        )

        storage_file = Path(
            material.storage_path,
        )

        if storage_file.exists():
            storage_file.unlink()

        self.repository.delete(material)
