from __future__ import annotations

import shutil
from datetime import datetime
from datetime import timezone
from pathlib import Path
from uuid import UUID
from uuid import uuid4

from fastapi import UploadFile
from sqlalchemy.orm import Session

from app.modules.knowledge_engine.models import KnowledgeSource


UPLOAD_ROOT = Path("storage/knowledge")
UPLOAD_ROOT.mkdir(parents=True, exist_ok=True)


class KnowledgeRepository:

    def __init__(
        self,
        db: Session,
    ):
        self.db = db

    def create_topic(
        self,
        *,
        user_id: UUID,
        title: str,
        subject: str,
        topic_description: str,
    ) -> KnowledgeSource:

        source = KnowledgeSource(
            user_id=user_id,
            source_type="topic",
            title=title,
            subject=subject,
            description=topic_description,
            raw_text=topic_description,
            cleaned_text=topic_description,
            processing_status="completed",
            processed_at=datetime.now(timezone.utc),
        )

        self.db.add(source)
        self.db.commit()
        self.db.refresh(source)

        return source

    async def save_document(
        self,
        *,
        user_id: UUID,
        file: UploadFile,
    ) -> KnowledgeSource:

        extension = Path(file.filename).suffix.lower()

        filename = f"{uuid4()}{extension}"

        user_directory = UPLOAD_ROOT / str(user_id)

        user_directory.mkdir(
            parents=True,
            exist_ok=True,
        )

        destination = user_directory / filename

        with destination.open("wb") as buffer:
            shutil.copyfileobj(
                file.file,
                buffer,
            )

        size = destination.stat().st_size

        source = KnowledgeSource(
            user_id=user_id,
            source_type="document",
            title=Path(file.filename).stem,
            subject="General",
            file_name=file.filename,
            file_path=str(destination),
            file_size=size,
            mime_type=file.content_type,
            processing_status="pending",
        )

        self.db.add(source)
        self.db.commit()
        self.db.refresh(source)

        return source

    def get(
        self,
        knowledge_id: UUID,
    ) -> KnowledgeSource | None:

        return (
            self.db.query(KnowledgeSource)
            .filter(
                KnowledgeSource.id == knowledge_id,
            )
            .first()
        )

    def list_by_user(
        self,
        user_id: UUID,
    ) -> list[KnowledgeSource]:

        return (
            self.db.query(KnowledgeSource)
            .filter(
                KnowledgeSource.user_id == user_id,
            )
            .order_by(
                KnowledgeSource.created_at.desc(),
            )
            .all()
        )

    def update_processing(
        self,
        source: KnowledgeSource,
        *,
        status: str,
        raw_text: str | None = None,
        cleaned_text: str | None = None,
        error_message: str | None = None,
    ) -> KnowledgeSource:

        source.processing_status = status
        source.raw_text = raw_text
        source.cleaned_text = cleaned_text
        source.error_message = error_message
        source.processed_at = datetime.now(
            timezone.utc,
        )

        self.db.commit()
        self.db.refresh(source)

        return source

    def delete(
        self,
        source: KnowledgeSource,
    ) -> None:

        if source.file_path:
            path = Path(source.file_path)

            if path.exists():
                path.unlink()

        self.db.delete(source)
        self.db.commit()
