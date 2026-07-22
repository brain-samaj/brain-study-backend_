from __future__ import annotations

from pathlib import Path

from docx import Document

from app.ai.extractors.base import BaseExtractor
from app.ai.extractors.base import ExtractionResult


class DocxExtractor(BaseExtractor):
    SUPPORTED_EXTENSIONS = {".docx"}

    def supports(self, suffix: str) -> bool:
        return suffix.lower() in self.SUPPORTED_EXTENSIONS

    def extract(
        self,
        source: Path,
    ) -> ExtractionResult:

        document = Document(source)

        paragraphs = [
            paragraph.text.strip()
            for paragraph in document.paragraphs
            if paragraph.text.strip()
        ]

        return ExtractionResult(
            text="\n".join(paragraphs),
            page_count=None,
            metadata={
                "type": "docx",
                "paragraphs": len(paragraphs),
            },
        )
