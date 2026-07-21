from __future__ import annotations

from uuid import UUID

from fastapi import UploadFile

from app.modules.knowledge_engine.models import KnowledgeSource
from app.modules.knowledge_engine.repository import KnowledgeRepository


class KnowledgeEngineService:

    def __init__(
        self,
        repository: KnowledgeRepository,
    ):
        self.repository = repository

    async def create_topic(
        self,
        *,
        user_id: UUID,
        title: str,
        subject: str,
        topic_description: str,
    ) -> KnowledgeSource:

        return self.repository.create_topic(
            user_id=user_id,
            title=title,
            subject=subject,
            topic_description=topic_description,
        )

    async def upload_document(
        self,
        *,
        user_id: UUID,
        file: UploadFile,
    ) -> KnowledgeSource:

        allowed_extensions = {
            ".pdf",
            ".docx",
            ".pptx",
            ".txt",
            ".png",
            ".jpg",
            ".jpeg",
            ".webp",
        }

        extension = (
            "." + file.filename.split(".")[-1].lower()
            if "." in file.filename
            else ""
        )

        if extension not in allowed_extensions:
            raise ValueError(
                "Unsupported file format."
            )

        return await self.repository.save_document(
            user_id=user_id,
            file=file,
        )

    async def get_source(
        self,
        *,
        knowledge_id: UUID,
    ) -> KnowledgeSource | None:

        return self.repository.get(
            knowledge_id,
        )

    async def list_sources(
        self,
        *,
        user_id: UUID,
    ) -> list[KnowledgeSource]:

        return self.repository.list_by_user(
            user_id,
        )

    async def delete_source(
        self,
        *,
        source: KnowledgeSource,
    ) -> None:

        self.repository.delete(
            source,
        )
