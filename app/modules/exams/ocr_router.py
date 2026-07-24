from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from pydantic import BaseModel

from app.modules.auth.dependencies import get_current_user

from app.modules.exams.ocr import (
    ExamOCRService,
)

from app.modules.exams.dependencies import (
    get_ocr_service,
)


router = APIRouter(
    prefix="/exams",
    tags=[
        "Exam OCR",
    ],
)



class OCRProcessRequest(BaseModel):
    """
    OCR engine callback payload.

    External OCR providers or internal
    vision models send extracted text here.
    """

    extracted_text: str



# ============================================================
# PROCESS HANDWRITTEN OCR
# ============================================================


@router.post(
    "/answers/{answer_id}/attachments/{attachment_id}/ocr",
)
async def process_ocr(
    answer_id: UUID,
    attachment_id: UUID,
    payload: OCRProcessRequest,
    current_user=Depends(
        get_current_user,
    ),
    service: ExamOCRService = Depends(
        get_ocr_service,
    ),
):

    try:

        answer = await service.process_attachment(
            answer_id=answer_id,
            attachment_id=attachment_id,
            extracted_text=payload.extracted_text,
        )


        return {
            "success": True,

            "answer_id": answer.id,

            "final_answer": (
                answer.final_answer
            ),

            "message": (
                "OCR processed successfully."
            ),
        }


    except Exception as exc:

        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc
