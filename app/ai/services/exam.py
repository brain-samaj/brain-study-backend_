from __future__ import annotations

from pathlib import Path

from app.ai.exam_engine.objective_generator import ObjectiveExamGenerator
from app.ai.exam_engine.service import TheoryExamGenerator
from app.ai.services.document_processor import DocumentProcessor


class ExamService:
    """
    Application service for examination generation.

    Pipeline:

        File
          ↓
        DocumentProcessor
          ↓
        Extraction
          ↓
        Cleaning
          ↓
        Chunking
          ↓
        DocumentAnalysis
          ↓
        Exam Generator
          ↓
        Exam Paper

    The document is analyzed once by the Knowledge Engine.
    The resulting DocumentAnalysis is passed to the exam generator.
    """

    def __init__(self) -> None:
        self.documents = DocumentProcessor()
        self.objective = ObjectiveExamGenerator()
        self.theory = TheoryExamGenerator()

    async def create_objective_exam(
        self,
        source: str | Path,
        duration: int,
        questions: int,
    ):
        """
        Generate an objective examination from a document.

        The document is processed through the centralized
        DocumentProcessor so the existing DocumentAnalysis
        is reused by the exam engine.
        """

        if questions <= 0:
            raise ValueError(
                "questions must be greater than zero."
            )

        if duration <= 0:
            raise ValueError(
                "duration must be greater than zero."
            )

        processed = await self.documents.process_file(
            source
        )

        paper = await self.objective.generate(
            analysis=processed.analysis,
            material=processed.cleaned_text,
            total_questions=questions,
        )

        paper.duration_minutes = duration

        return paper

    async def create_theory_exam(
        self,
        source: str | Path,
        duration: int,
        answer_any: int,
    ):
        """
        Generate a theory examination from a document.

        The same processed document analysis is reused by
        the theory examination engine.
        """

        if answer_any <= 0:
            raise ValueError(
                "answer_any must be greater than zero."
            )

        if duration <= 0:
            raise ValueError(
                "duration must be greater than zero."
            )

        processed = await self.documents.process_file(
            source
        )

        return await self.theory.generate(
            analysis=processed.analysis,
            material=processed.cleaned_text,
            duration=duration,
            answer_any=answer_any,
        )
