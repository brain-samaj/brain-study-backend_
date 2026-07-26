from __future__ import annotations

import json
import time
from pathlib import Path
from uuid import UUID

from app.ai.client import AIClient

from app.modules.knowledge_engine.models import (
    KnowledgeSource,
    KnowledgeStatus,
)

from app.modules.knowledge_engine.repository import (
    KnowledgeRepository,
)

from app.modules.knowledge_engine.schemas import (
    GlossaryItem,
    KnowledgeCreate,
    KnowledgeTopic,
    KnowledgeUpdate,
    LearningObjective,
    SampleQuestion,
)

from app.modules.study_materials.models import (
    ProcessingStatus,
)

from app.modules.study_materials.repository import (
    StudyMaterialRepository,
)


class KnowledgeEngineService:
    """
    Brain Study Knowledge Engine

    Responsibilities
    ----------------
    ✓ Extract text from uploaded study materials

    ✓ Generate structured knowledge using AI

    ✓ Save processed knowledge

    ✓ Provide a single source of truth for:

        • Exams
        • Flashcards
        • Summaries
        • Smart Study
        • Future AI Tutor

    This is the ONLY service allowed to communicate
    with AI providers.
    """

    def __init__(
        self,
        *,
        repository: KnowledgeRepository,
        study_material_repository: StudyMaterialRepository,
        ai_client: AIClient,
    ) -> None:

        self.repository = repository
        self.study_material_repository = (
            study_material_repository
        )

        self.ai = ai_client

    # ==========================================================
    # INTERNAL HELPERS
    # ==========================================================

    async def _load_material(
        self,
        material_id: UUID,
    ):

        material = await self.study_material_repository.get(
            material_id,
        )

        if material is None:
            raise ValueError(
                "Study material not found."
            )

        return material

    async def _mark_processing(
        self,
        material,
    ):

        material.processing_status = (
            ProcessingStatus.PROCESSING
        )

        await self.study_material_repository._db.commit()

        await self.study_material_repository._db.refresh(
            material,
        )

    async def _mark_ready(
        self,
        material,
    ):

        material.processing_status = (
            ProcessingStatus.READY
        )

        material.extraction_error = None

        await self.study_material_repository._db.commit()

        await self.study_material_repository._db.refresh(
            material,
        )

    async def _mark_failed(
        self,
        material,
        error: Exception,
    ):

        material.processing_status = (
            ProcessingStatus.FAILED
        )

        material.extraction_error = str(error)

        await self.study_material_repository._db.commit()

        await self.study_material_repository._db.refresh(
            material,
        )

    def _safe_list(
        self,
        value,
    ):

        if value is None:
            return []

        return value


    # ==========================================================
    # TEXT EXTRACTION
    # ==========================================================

    async def _extract_text(
        self,
        material,
    ) -> str:
        """
        Extract plain text from a study material.

        Supports:
            • PDF
            • DOCX
            • PPTX
            • TXT
            • Markdown
            • Images (future OCR)
            • Topic materials
        """

        # Already extracted
        if (
            material.extracted_text is not None
            and material.extracted_text.strip()
        ):
            return material.extracted_text

        path = Path(material.storage_path)

        if not path.exists():
            raise FileNotFoundError(
                f"Missing uploaded file: {path}"
            )

        suffix = path.suffix.lower()

        text = ""

        # ------------------------------------------------------
        # TXT / MD
        # ------------------------------------------------------

        if suffix in {".txt", ".md"}:

            text = path.read_text(
                encoding="utf-8",
                errors="ignore",
            )

        # ------------------------------------------------------
        # PDF
        # ------------------------------------------------------

        elif suffix == ".pdf":

            try:
                from pypdf import PdfReader

                reader = PdfReader(str(path))

                pages = []

                for page in reader.pages:

                    pages.append(
                        page.extract_text() or ""
                    )

                text = "\n".join(pages)

                material.page_count = len(reader.pages)

            except Exception as exc:
                raise RuntimeError(
                    "Unable to extract PDF."
                ) from exc

        # ------------------------------------------------------
        # DOCX
        # ------------------------------------------------------

        elif suffix == ".docx":

            try:
                from docx import Document

                document = Document(str(path))

                text = "\n".join(
                    paragraph.text
                    for paragraph in document.paragraphs
                )

            except Exception as exc:
                raise RuntimeError(
                    "Unable to extract DOCX."
                ) from exc

        # ------------------------------------------------------
        # PPTX
        # ------------------------------------------------------

        elif suffix == ".pptx":

            try:
                from pptx import Presentation

                presentation = Presentation(str(path))

                slides = []

                for slide in presentation.slides:

                    for shape in slide.shapes:

                        if hasattr(shape, "text"):
                            slides.append(shape.text)

                text = "\n".join(slides)

                material.page_count = len(
                    presentation.slides
                )

            except Exception as exc:
                raise RuntimeError(
                    "Unable to extract PPTX."
                ) from exc

        # ------------------------------------------------------
        # IMAGES
        # ------------------------------------------------------

        elif suffix in {
            ".png",
            ".jpg",
            ".jpeg",
            ".bmp",
            ".gif",
            ".webp",
        }:

            # OCR will be implemented later.
            text = ""

        else:

            raise RuntimeError(
                f"Unsupported file format: {suffix}"
            )

        text = text.strip()

        material.extracted_text = text

        material.word_count = (
            len(text.split())
            if text
            else 0
        )

        await self.study_material_repository._db.commit()

        await self.study_material_repository._db.refresh(
            material,
        )

        return text


    # ==========================================================
    # BUILD KNOWLEDGE FROM MATERIAL
    # ==========================================================

    async def build_from_material(
        self,
        *,
        material_id: UUID,
    ) -> KnowledgeSource:

        existing = await self.repository.get_by_material(
            material_id,
        )

        if existing is not None:
            return existing

        material = await self._load_material(
            material_id,
        )

        await self._mark_processing(
            material,
        )

        try:

            extracted_text = await self._extract_text(
                material,
            )

            if not extracted_text.strip():

                raise ValueError(
                    "No readable text could be extracted from the uploaded material."
                )

            started = time.perf_counter()

            prompt = f"""
You are Brain Study's Knowledge Engine.

Analyse the following study material and return ONLY valid JSON.

Required JSON format:

{{
    "title": "...",
    "summary": "...",
    "topics":[
        {{
            "title":"...",
            "content":"...",
            "keywords":["..."],
            "difficulty":"easy"
        }}
    ],
    "glossary":[
        {{
            "term":"...",
            "definition":"..."
        }}
    ],
    "learning_objectives":[
        {{
            "objective":"..."
        }}
    ],
    "key_points":[
        "..."
    ],
    "sample_questions":[
        {{
            "question":"...",
            "answer":"..."
        }}
    ]
}}

Study Material:

{extracted_text}
"""

            response = await self.ai.generate_json(
                prompt=prompt,
                temperature=0.2,
            )

            elapsed = int(
                (
                    time.perf_counter() - started
                )
                * 1000
            )

            knowledge = await self.repository.create(
                KnowledgeCreate(
                    material_id=material.id,
                    title=response.get(
                        "title",
                        material.title,
                    ),
                    summary=response.get(
                        "summary",
                        "",
                    ),
                    knowledge=response,
                    topics=[
                        KnowledgeTopic(**topic)
                        for topic in response.get(
                            "topics",
                            [],
                        )
                    ],
                    glossary=[
                        GlossaryItem(**item)
                        for item in response.get(
                            "glossary",
                            [],
                        )
                    ],
                    learning_objectives=[
                        LearningObjective(**item)
                        for item in response.get(
                            "learning_objectives",
                            [],
                        )
                    ],
                    key_points=response.get(
                        "key_points",
                        [],
                    ),
                    sample_questions=[
                        SampleQuestion(**item)
                        for item in response.get(
                            "sample_questions",
                            [],
                        )
                    ],
                    total_tokens=0,
                    ai_provider="Brain AI",
                    ai_model="default",
                    processing_time_ms=elapsed,
                    is_cached=False,
                )
            )

            await self._mark_ready(
                material,
            )

            return knowledge

        except Exception as exc:

            await self._mark_failed(
                material,
                exc,
            )

            raise



    # ==========================================================
    # REFRESH KNOWLEDGE
    # ==========================================================

    async def refresh(
        self,
        *,
        material_id: UUID,
    ) -> KnowledgeSource:
        """
        Force regeneration of knowledge for a study material.
        """

        await self.repository.delete(
            material_id,
        )

        return await self.build_from_material(
            material_id=material_id,
        )

    # ==========================================================
    # GET KNOWLEDGE
    # ==========================================================

    async def get(
        self,
        *,
        material_id: UUID,
    ) -> KnowledgeSource | None:

        return await self.repository.get_by_material(
            material_id,
        )

    # ==========================================================
    # UPDATE KNOWLEDGE
    # ==========================================================

    async def update(
        self,
        *,
        knowledge: KnowledgeSource,
        payload: KnowledgeUpdate,
    ) -> KnowledgeSource:

        return await self.repository.update(
            knowledge,
            payload,
        )

    # ==========================================================
    # DELETE KNOWLEDGE
    # ==========================================================

    async def delete(
        self,
        *,
        material_id: UUID,
    ) -> bool:

        return await self.repository.delete(
            material_id,
        )

    # ==========================================================
    # CHECK CACHE
    # ==========================================================

    async def exists(
        self,
        *,
        material_id: UUID,
    ) -> bool:

        return await self.repository.exists(
            material_id,
        )

    # ==========================================================
    # EXPORT KNOWLEDGE
    # ==========================================================

    async def export_json(
        self,
        *,
        material_id: UUID,
    ) -> dict:

        knowledge = await self.repository.get_by_material(
            material_id,
        )

        if knowledge is None:
            raise ValueError(
                "Knowledge has not been generated."
            )

        return {
            "id": str(knowledge.id),
            "material_id": str(knowledge.material_id),
            "title": knowledge.title,
            "summary": knowledge.summary,
            "knowledge": knowledge.knowledge,
            "topics": knowledge.topics,
            "glossary": knowledge.glossary,
            "learning_objectives": knowledge.learning_objectives,
            "key_points": knowledge.key_points,
            "sample_questions": knowledge.sample_questions,
            "status": knowledge.status.value,
            "cached": knowledge.is_cached,
            "provider": knowledge.ai_provider,
            "model": knowledge.ai_model,
            "tokens": knowledge.total_tokens,
            "processing_time_ms": knowledge.processing_time_ms,
        }

