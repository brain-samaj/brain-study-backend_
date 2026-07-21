from __future__ import annotations

from app.ai.flashcards.service import FlashcardService
from app.ai.services.document_extractor import DocumentExtractorService


class FlashcardGeneratorService:

    def __init__(self):

        self.documents = DocumentExtractorService()
        self.flashcards = FlashcardService()

    def create(
        self,
        source: str,
    ):

        result = self.documents.process(source)

        return self.flashcards.generate(
            result["analysis"],
            result["extraction"].text,
        )
