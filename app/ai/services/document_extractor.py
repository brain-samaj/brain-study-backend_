from __future__ import annotations

from pathlib import Path

from app.ai.extractors.base import ExtractionResult
from app.ai.extractors.factory import ExtractorFactory


class DocumentExtractor:
    """
    Unified extraction service.

    Supports:

    • PDF
    • DOCX
    • PPTX
    • TXT
    • Images (OCR)
    • Topic text
    """

    def __init__(self) -> None:
        self.factory = ExtractorFactory()

    async def extract(
        self,
        path: str | Path,
    ) -> ExtractionResult:

        path = Path(path)

        extractor = self.factory.get(path)

        # Extractors are synchronous.
        return extractor.extract(path)

    async def extract_topic(
        self,
        title: str,
        subject: str,
        topic: str,
    ) -> ExtractionResult:

        extractor = self.factory.get_topic()

        # Topic extractor is also synchronous.
        return extractor.extract(
            title=title,
            subject=subject,
            topic=topic,
        )
