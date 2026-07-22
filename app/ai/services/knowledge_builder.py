from __future__ import annotations

from dataclasses import dataclass

from app.ai.services.document_processor import ProcessedDocument


@dataclass(slots=True)
class KnowledgeDocument:
    """
    Canonical knowledge representation.

    Every downstream learning feature consumes this
    object instead of raw extracted text.
    """

    title: str

    subject: str

    topic: str

    difficulty: str

    language: str

    education_level: str

    cleaned_text: str

    keywords: list[str]

    learning_objectives: list[str]

    important_terms: list[str]

    prerequisites: list[str]

    chunk_count: int

    chunks: list[str]


class KnowledgeBuilder:
    """
    Converts a processed document into
    Brain Study's internal knowledge format.
    """

    def build(
        self,
        processed: ProcessedDocument,
    ) -> KnowledgeDocument:

        analysis = processed.analysis

        return KnowledgeDocument(
            title=analysis.title,
            subject=analysis.subject,
            topic=analysis.topic,
            difficulty=analysis.difficulty,
            language=analysis.language,
            education_level=analysis.education_level,
            cleaned_text=processed.cleaned_text,
            keywords=analysis.keywords,
            learning_objectives=analysis.learning_objectives,
            important_terms=analysis.important_terms,
            prerequisites=analysis.prerequisites,
            chunk_count=processed.chunk_count,
            chunks=[
                chunk.text
                for chunk in processed.chunks
            ],
        )
