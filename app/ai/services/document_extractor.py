from __future__ import annotations

from pathlib import Path

from app.ai.analyzers.document_analyzer import DocumentAnalyzer
from app.ai.extractors.factory import ExtractorFactory


class DocumentExtractorService:

    def __init__(self) -> None:
        self.factory = ExtractorFactory()
        self.analyzer = DocumentAnalyzer()

    def process(
        self,
        source: str | Path,
    ):

        source = Path(source)

        extractor = self.factory.get(source)

        extraction = extractor.extract(source)

        analysis = self.analyzer.analyze(
            extraction.text,
        )

        return {
            "extraction": extraction,
            "analysis": analysis,
        }
