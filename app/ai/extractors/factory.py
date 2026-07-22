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
    """
    Returns the appropriate extractor
    based on the uploaded file type.
    """

    def __init__(self) -> None:

        self._extractors: list[BaseExtractor] = [
            PdfExtractor(),
            DocxExtractor(),
            PptxExtractor(),
            TxtExtractor(),
            ImageExtractor(),
        ]

        self._topic = TopicExtractor()

    def get(
        self,
        path: str | Path,
    ) -> BaseExtractor:

        path = Path(path)

        extension = path.suffix.lower()

        for extractor in self._extractors:

            if extension in extractor.SUPPORTED_EXTENSIONS:
                return extractor

        raise ValueError(
            f"No extractor available for '{extension}'."
        )

    def get_topic(
        self,
    ) -> TopicExtractor:

        return self._topic
