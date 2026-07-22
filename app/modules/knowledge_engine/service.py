from __future__ import annotations

from fastapi import UploadFile

from app.modules.knowledge_engine.repository import KnowledgeRepository


class KnowledgeEngineService:
    """
    Application service for the Knowledge Engine.

    This layer coordinates the repository and
    contains business rules.
    """

    def __init__(
        self,
        repository: KnowledgeRepository,
    ) -> None:

        self.repository = repository

    async def create_topic(
        self,
        *,
        user_id,
        title: str,
        subject: str,
        topic_description: str,
    ):

        source = await self.repository.create_topic(
            user_id=user_id,
            title=title,
            subject=subject,
            topic_description=topic_description,
        )

        return {
            "id": source.id,
            "title": source.title,
            "subject": source.subject,
            "source_type": source.source_type,
            "processing_status": source.processing_status,
        }

    async def upload_document(
        self,
        *,
        user_id,
        file: UploadFile,
    ):

        source = await self.repository.save_document(
            user_id=user_id,
            file=file,
        )

        return {
            "id": source.id,
            "title": source.title,
            "subject": source.subject,
            "source_type": source.source_type,
            "processing_status": source.processing_status,
        }
