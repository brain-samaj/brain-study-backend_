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

    Every uploaded study material enters the
    system through this service.
    """

    def __init__(self) -> None:
        self.factory = ExtractorFactory()

    async def extract(
        self,
        path: str | Path,
    ) -> ExtractionResult:

        path = Path(path)

        extractor = self.factory.get(path)

        return await extractor.extract(path)

    async def extract_topic(
        self,
        title: str,
        subject: str,
        topic: str,
    ) -> ExtractionResult:

        extractor = self.factory.get_topic()

        return await extractor.extract(
            title=title,
            subject=subject,
            topic=topic,
        )
