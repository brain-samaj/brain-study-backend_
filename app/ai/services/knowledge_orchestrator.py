from __future__ import annotations

from app.ai.analyzers.document_analyzer import DocumentAnalyzer
from app.ai.client import AIClient


class KnowledgeOrchestrator:
    """
    Brain Study AI Pipeline

    Upload
        ↓
    Text Extraction
        ↓
    DocumentAnalyzer
        ↓
    Educational Metadata
        ↓
    Knowledge Engine
        ↓
    Structured Knowledge
        ↓
    TeacherAI
        ↓
    Study Guide

    This class coordinates every AI stage.
    It ensures each AI performs only its own responsibility.
    """

    def __init__(
        self,
        client: AIClient | None = None,
    ) -> None:
        self.client = client or AIClient()
        self.document_analyzer = DocumentAnalyzer(self.client)

    async def analyze_document(
        self,
        *,
        title: str,
        content: str,
    ):
        """
        Performs the one-time educational analysis
        of an uploaded document.
        """
        return await self.document_analyzer.analyze(
            title=title,
            content=content,
        )

    async def build_knowledge(
        self,
        *,
        title: str,
        content: str,
    ) -> dict:
        """
        Runs the educational analysis and returns
        the analysis metadata as a dictionary.

        The Knowledge Engine can merge this metadata
        into the structured knowledge JSON before saving.
        """
        analysis = await self.analyze_document(
            title=title,
            content=content,
        )

        return analysis.__dict__
