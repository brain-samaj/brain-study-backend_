from __future__ import annotations

from datetime import UTC
from datetime import datetime
from uuid import UUID

from app.modules.exams.exceptions import (
    AttachmentError,
)
from app.modules.exams.repository import ExamRepository
from app.modules.exams.utils import ExamFileUtils


class ExamOCRService:
    """
    Handwritten Answer OCR Processing Service.

    Responsibilities
    ----------------
    - Process uploaded handwritten answers.
    - Store extracted OCR text.
    - Rebuild final answer.
    - Prepare answers for AI grading.

    OCR provider is isolated from exam logic.
    """


    def __init__(
        self,
        *,
        repository: ExamRepository,
    ) -> None:

        self._repository = repository



    async def process_attachment(
        self,
        *,
        answer_id: UUID,
        attachment_id: UUID,
        extracted_text: str,
    ):

        attachment = await (
            self._repository
            .get_attachment(
                attachment_id,
            )
        )


        if attachment is None:

            raise AttachmentError(
                "Attachment not found."
            )


        if attachment.answer_id != answer_id:

            raise AttachmentError(
                "Attachment does not belong to answer."
            )


        attachment.ocr_text = (
            extracted_text.strip()
        )

        attachment.processed_at = (
            datetime.now(
                UTC,
            )
        )


        answer = await (
            self._repository
            .get_answer_by_id(
                answer_id,
            )
        )


        if answer is None:

            raise AttachmentError(
                "Answer not found."
            )


        ocr_parts = []


        for item in answer.attachments:

            if item.ocr_text:

                ocr_parts.append(
                    item.ocr_text
                )


        answer.ocr_answer = (
            "\n\n".join(
                ocr_parts
            )
        )


        answer.final_answer = (
            ExamFileUtils.merge_answers(
                typed_answer=(
                    answer.text_answer
                ),
                ocr_answer=(
                    answer.ocr_answer
                ),
            )
        )


        await self._repository.commit()


        return answer
