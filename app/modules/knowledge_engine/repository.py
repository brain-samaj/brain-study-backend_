from __future__ import annotations

import shutil
from datetime import datetime
from pathlib import Path
from uuid import UUID

from fastapi import UploadFile
from sqlalchemy.orm import Session

from app.ai.orchestrator import KnowledgeOrchestrator
from app.modules.knowledge_engine.models import KnowledgeSource


UPLOAD_DIRECTORY = Path("storage/knowledge")
UPLOAD_DIRECTORY.mkdir(parents=True, exist_ok=True)


class KnowledgeRepository:

    def __init__(
        self,
        db: Session,
    ):
        self.db = db
        self.orchestrator = KnowledgeOrchestrator()

    async def create_topic(
        self,
        *,
        user_id: UUID,
        title: str,
        subject: str,
        topic_description: str,
    ):

        source = KnowledgeSource(
            user_id=user_id,
            title=title,
            subject=subject,
            source_type="topic",
            description=topic_description,
            processing_status="processing",
        )

        self.db.add(source)
        self.db.commit()
        self.db.refresh(source)

        try:

            knowledge = await self.orchestrator.process_topic(
                title=title,
                subject=subject,
                topic=topic_description,
            )

            source.raw_text = knowledge.cleaned_text
            source.cleaned_text = knowledge.cleaned_text
            source.processing_status = "completed"
            source.processed_at = datetime.utcnow()

            self.db.commit()
            self.db.refresh(source)

            return source

        except Exception as exc:

            source.processing_status = "failed"
            source.error_message = str(exc)

            self.db.commit()

            raise

    async def save_document(
        self,
        *,
        user_id: UUID,
        file: UploadFile,
    ):

        filename = f"{datetime.utcnow().timestamp()}_{file.filename}"

        destination = UPLOAD_DIRECTORY / filename

        with destination.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        source = KnowledgeSource(
            user_id=user_id,
            title=Path(file.filename).stem,
            subject="General",
            source_type=destination.suffix.lower().replace(".", ""),
            file_name=file.filename,
            file_path=str(destination),
            mime_type=file.content_type,
            file_size=destination.stat().st_size,
            processing_status="processing",
        )

        self.db.add(source)
        self.db.commit()
        self.db.refresh(source)

        try:

            knowledge = await self.orchestrator.process_file(
                destination,
            )

            source.subject = knowledge.subject
            source.raw_text = knowledge.cleaned_text
            source.cleaned_text = knowledge.cleaned_text
            source.processing_status = "completed"
            source.processed_at = datetime.utcnow()

            self.db.commit()
            self.db.refresh(source)

            return source

        except Exception as exc:

            source.processing_status = "failed"
            source.error_message = str(exc)

            self.db.commit()

            raise
