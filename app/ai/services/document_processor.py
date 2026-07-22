from __future__ import annotations

from pathlib import Path

from app.ai.analyzers.document_analyzer import DocumentAnalyzer
from app.ai.analyzers.models import DocumentAnalysis
from app.ai.retrieval.chunker import DocumentChunk
from app.ai.retrieval.chunker import SemanticChunker
from app.ai.retrieval.cleaner import TextCleaner
from app.ai.services.document_extractor import DocumentExtractor


class ProcessedDocument:

    def __init__(
        self,
        *,
        analysis: DocumentAnalysis,
        raw_text: str,
        cleaned_text: str,
        chunks: list[DocumentChunk],
    ) -> None:

        self.analysis = analysis
        self.raw_text = raw_text
        self.cleaned_text = cleaned_text
        self.chunks = chunks

    @property
    def chunk_count(self) -> int:
        return len(self.chunks)

    @property
    def total_words(self) -> int:
        return sum(chunk.words for chunk in self.chunks)


class DocumentProcessor:
    """
    Complete document processing pipeline.

    Upload
        ↓
    Extract
        ↓
    Clean
        ↓
    Analyze
        ↓
    Chunk
        ↓
    Ready for:
        • Study Guide
        • Smart Study
        • Flashcards
        • Practice Exam
    """

    def __init__(self) -> None:

        self.extractor = DocumentExtractor()
        self.cleaner = TextCleaner()
        self.analyzer = DocumentAnalyzer()
        self.chunker = SemanticChunker()

    async def process_file(
        self,
        path: str | Path,
    ) -> ProcessedDocument:

        extracted = await self.extractor.extract(path)

        cleaned = self.cleaner.clean(
            extracted.text,
        )

        analysis = await self.analyzer.analyze(
            title=Path(path).stem,
            content=cleaned,
        )

        chunks = self.chunker.chunk(
            cleaned,
        )

        return ProcessedDocument(
            analysis=analysis,
            raw_text=extracted.text,
            cleaned_text=cleaned,
            chunks=chunks,
        )

    async def process_topic(
        self,
        *,
        title: str,
        subject: str,
        topic: str,
    ) -> ProcessedDocument:

        extracted = await self.extractor.extract_topic(
            title=title,
            subject=subject,
            topic=topic,
        )

        cleaned = self.cleaner.clean(
            extracted.text,
        )

        analysis = await self.analyzer.analyze(
            title=title,
            content=cleaned,
        )

        chunks = self.chunker.chunk(
            cleaned,
        )

        return ProcessedDocument(
            analysis=analysis,
            raw_text=extracted.text,
            cleaned_text=cleaned,
            chunks=chunks,
        )
