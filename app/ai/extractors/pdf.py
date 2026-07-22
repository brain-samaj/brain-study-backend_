from __future__ import annotations

from pathlib import Path

from pypdf import PdfReader

from app.ai.extractors.base import BaseExtractor
from app.ai.extractors.base import ExtractionResult


class PdfExtractor(BaseExtractor):
    SUPPORTED_EXTENSIONS = {".pdf"}

    def supports(self, suffix: str) -> bool:
        return suffix.lower() in self.SUPPORTED_EXTENSIONS

    def extract(
        self,
        source: Path,
    ) -> ExtractionResult:

        reader = PdfReader(str(source))

        pages: list[str] = []

        for page in reader.pages:
            pages.append(page.extract_text() or "")

        return ExtractionResult(
            text="\n".join(pages).strip(),
            page_count=len(reader.pages),
            metadata={
                "type": "pdf",
            },
        )
