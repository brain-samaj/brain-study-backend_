from __future__ import annotations

from app.ai.services.document_extractor import DocumentExtractorService
from app.ai.smart_study.service import SmartStudyService


class RevisionService:

    def __init__(self):

        self.documents = DocumentExtractorService()
        self.study = SmartStudyService()

    def next(
        self,
        source: str,
        previous_questions: list[str],
    ):

        result = self.documents.process(source)

        return self.study.next_question(
            analysis=result["analysis"],
            material=result["extraction"].text,
            previous_questions=previous_questions,
        )
