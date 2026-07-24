from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter
from fastapi import Depends
from fastapi import File
from fastapi import HTTPException
from fastapi import UploadFile
from fastapi import status

from app.modules.auth.dependencies import get_current_user

from app.modules.exams.attachment_service import (
    ExamAttachmentService,
)

from app.modules.exams.dependencies import (
    get_attachment_service,
)


router = APIRouter(
    prefix="/exams",
    tags=[
        "Exam Attachments",
    ],
)



# ============================================================
# UPLOAD HANDWRITTEN ANSWER IMAGE
# ============================================================


@router.post(
    "/answers/{answer_id}/attachments",
    status_code=status.HTTP_201_CREATED,
)
async def upload_answer_attachment(
    answer_id: UUID,
    file: UploadFile = File(...),
    page_number: int = 1,
    current_user=Depends(
        get_current_user,
    ),
    service: ExamAttachmentService = Depends(
        get_attachment_service,
    ),
):

    try:

        content = await file.read()


        attachment = await service.add_attachment(
            answer_id=answer_id,
            filename=file.filename,
            mime_type=file.content_type,
            file_size=len(content),
            storage_path=(
                f"exam_answers/{answer_id}"
            ),
            page_number=page_number,
        )


        return {
            "success": True,
            "attachment_id": attachment.id,
            "filename": attachment.original_filename,
            "page_number": attachment.page_number,
            "message": (
                "Handwritten answer uploaded."
            ),
        }


    except Exception as exc:

        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc




# ============================================================
# DELETE ATTACHMENT
# ============================================================


@router.delete(
    "/attachments/{attachment_id}",
)
async def delete_attachment(
    attachment_id: UUID,
    current_user=Depends(
        get_current_user,
    ),
    service: ExamAttachmentService = Depends(
        get_attachment_service,
    ),
):

    try:

        await service.delete_attachment(
            attachment_id=attachment_id,
        )


        return {
            "success": True,
            "message": (
                "Attachment deleted."
            ),
        }


    except Exception as exc:

        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc
