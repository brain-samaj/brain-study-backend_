from __future__ import annotations

import time
from uuid import UUID

from app.ai.client import AIClient
from app.modules.knowledge_engine.models import KnowledgeSource
from app.modules.knowledge_engine.models import KnowledgeStatus
from app.modules.knowledge_engine.repository import KnowledgeRepository
from app.modules.knowledge_engine.schemas import KnowledgeCreate
from app.modules.knowledge_engine.schemas import KnowledgeUpdate
from app.modules.study_materials.repository import StudyMaterialRepository


class KnowledgeEngineService:
    """
    Enterprise Knowledge Engine.

    Responsibilities
    ----------------
    - Load study material
    - Generate structured knowledge
    - Cache processed knowledge
    - Provide knowledge for downstream AI services

    This service is the ONLY place where AI is used to process
    uploaded study materials.

    The frontend never communicates with this service directly.
    """

    def __init__(
        self,
        repository: KnowledgeRepository,
        study_material_repository: StudyMaterialRepository,
        ai_client: AIClient,
    ) -> None:
        self._repository = repository
        self._materials = study_material_repository
        self._ai = ai_client

    async def build_from_material(
        self,
        *,
        material_id: UUID,
    ) -> KnowledgeSource:
        """
        Build knowledge from a study material.

        If knowledge already exists, the cached version is returned.
        """

        cached = await self._repository.get_by_material(
            material_id,
        )

        if cached is not None:
            return cached

        material = await self._materials.get(
            material_id,
        )

        if material is None:
            raise ValueError(
                "Study material not found."
            )

        start = time.perf_counter()

        prompt = f"""
You are Brain Study's Knowledge Engine.

Extract structured knowledge from the study material.

Return ONLY valid JSON.

JSON structure:

{{
    "title": "...",
    "summary": "...",
    "topics": [
        {{
            "title": "...",
            "content": "...",
            "keywords": ["..."]
        }}
    ],
    "glossary": [
        {{
            "term": "...",
            "definition": "..."
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

Study Material

{material.content}
"""

        await self._repository.update_status(
            material_id,
            KnowledgeStatus.PROCESSING,
        )

        response = await self._ai.generate_json(
            prompt=prompt,
            temperature=0.2,
        )

        elapsed = int(
            (time.perf_counter() - start) * 1000
        )

        knowledge = KnowledgeCreate(
            material_id=material.id,
            title=response["title"],
            summary=response["summary"],
            knowledge=response,
            topics=response.get(
                "topics",
                [],
            ),
            glossary=response.get(
                "glossary",
                [],
            ),
            learning_objectives=response.get(
                "learning_objectives",
                [],
            ),
            key_points=response.get(
                "key_points",
                [],
            ),
            sample_questions=response.get(
                "sample_questions",
                [],
            ),
            processing_time_ms=elapsed,
            total_tokens=0,
            is_cached=False,
        )

        return await self._repository.create(
            knowledge,
        )

    async def refresh(
        self,
        *,
        material_id: UUID,
    ) -> KnowledgeSource:
        """
        Regenerate knowledge from the latest study material.
        """

        await self._repository.delete(
            material_id,
        )

        return await self.build_from_material(
            material_id=material_id,
        )

    async def get(
        self,
        *,
        material_id: UUID,
    ) -> KnowledgeSource | None:
        """
        Retrieve cached knowledge for a study material.
        """

        return await self._repository.get_by_material(
            material_id,
        )

    async def update(
        self,
        *,
        knowledge: KnowledgeSource,
        payload: KnowledgeUpdate,
    ) -> KnowledgeSource:
        """
        Update an existing knowledge record.
        """

        return await self._repository.update(
            knowledge,
            payload,
        )
