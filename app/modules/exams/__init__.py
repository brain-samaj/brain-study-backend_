"""
Brain Study Exam Module.

Production exam system containing:

- AI exam generation
- Objective examinations
- Theory examinations
- Handwritten answer capture
- OCR processing
- Autosave
- AI grading
- Result analytics
- Learning recommendations
"""

from app.modules.exams.models import ExamAnswer
from app.modules.exams.models import ExamQuestion
from app.modules.exams.models import ExamSession

from app.modules.exams.result_models import ExamResult

from app.modules.exams.submission_models import (
    ExamSubmission,
)

from app.modules.exams.attachment_models import (
    ExamAnswerAttachment,
)


__all__ = [

    "ExamSession",

    "ExamQuestion",

    "ExamAnswer",

    "ExamResult",

    "ExamSubmission",

    "ExamAnswerAttachment",

]
