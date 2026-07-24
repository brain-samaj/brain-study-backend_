from __future__ import annotations

"""
Exam Module Registration.

Central place for connecting the exam
domain into the Brain Study backend.
"""


from fastapi import FastAPI


from app.modules.exams.router import (
    router as exam_router,
)

from app.modules.exams.attachment_router import (
    router as attachment_router,
)

from app.modules.exams.ocr_router import (
    router as ocr_router,
)

from app.modules.exams.review_router import (
    router as review_router,
)



def register_exam_module(
    app: FastAPI,
) -> None:
    """
    Register all exam related APIs.
    """


    app.include_router(
        exam_router,
        prefix="/api/v1",
    )


    app.include_router(
        attachment_router,
        prefix="/api/v1",
    )


    app.include_router(
        ocr_router,
        prefix="/api/v1",
    )


    app.include_router(
        review_router,
        prefix="/api/v1",
    )
