from __future__ import annotations

from uuid import UUID
from uuid import uuid4

from app.modules.exams.exceptions import (
    InvalidAttachmentError,
)
from app.modules.exams.models import ExamAnswerAttachment
from app.modules.exams.repository import ExamRepository
from app.modules.exams.validators import ExamValidator


class ExamAttachmentService:
    """
    Theory Answer Attachment Service.

    Handles:

    - Camera image uploads
    - Handwritten answer pages
    - Multiple images per question
    - File ownership validation
    - OCR preparation

    The frontend only uploads.
    Backend manages storage and processing.
    """


    def __init__(
        self,
        *,
        repository: ExamRepository,
        upload_directory: str,
    ) -> None:

        self._repository = repository

        self._upload_directory = (
            upload_directory
        )



    async def add_attachment(
        self,
        *,
        answer_id: UUID,
        filename: str,
        mime_type: str,
        file_size: int,
        storage_path: str,
        page_number: int,
    ) -> ExamAnswerAttachment:


        ExamValidator.validate_attachment(
            file_size=file_size,
            mime_type=mime_type,
        )


        answer = await (
            self._repository
            .get_answer_by_id(
                answer_id,
            )
        )


        if answer is None:

            raise InvalidAttachmentError(
                "Answer not found."
            )



        attachment = ExamAnswerAttachment(

            answer_id=answer_id,

            original_filename=filename,

            stored_filename=(
                f"{uuid4()}_{filename}"
            ),

            storage_path=storage_path,

            mime_type=mime_type,

            file_size=file_size,

            page_number=page_number,
        )


        self._repository.session.add(
            attachment,
        )


        await self._repository.session.flush()


        await self._repository.commit()


        return attachment



    async def delete_attachment(
        self,
        *,
        attachment_id: UUID,
    ) -> None:


        attachment = await (
            self._repository
            .get_attachment(
                attachment_id,
            )
        )


        if attachment is None:

            raise InvalidAttachmentError(
                "Attachment not found."
            )


        await self._repository.session.delete(
            attachment,
        )


        await self._repository.commit()
