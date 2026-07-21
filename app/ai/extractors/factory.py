from __future__ import annotations

from pathlib import Path

from app.ai.extractors.base import BaseExtractor
from app.ai.extractors.docx import DocxExtractor
from app.ai.extractors.image import ImageExtractor
from app.ai.extractors.pdf import PdfExtractor
from app.ai.extractors.pptx import PptxExtractor
from app.ai.extractors.topic import TopicExtractor
from app.ai.extractors.txt import TxtExtractor


class ExtractorFactory:

    def __init__(self) -> None:

        self.extractors: list[BaseExtractor] = [
            PdfExtractor(),
            DocxExtractor(),
            PptxExtractor(),
            TxtExtractor(),
            ImageExtractor(),
            TopicExtractor(),
        ]

    def get(self, source: Path) -> BaseExtractor:

        suffix = source.suffix.lower()

        for extractor in self.extractors:

            if extractor.supports(suffix):
                return extractor

        raise ValueError(
            f"Unsupported document type: {suffix}"
        )
