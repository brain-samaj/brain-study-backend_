from __future__ import annotations

from app.ai.client import AIClient
from app.ai.prompts.study_guide import STUDY_GUIDE_PROMPT
from app.modules.knowledge_engine.models import KnowledgeSource


class StudyGuideGenerator:

    def __init__(self):
        self.client = AIClient()

    async def generate(
        self,
        *,
        source: KnowledgeSource,
    ):

        prompt = STUDY_GUIDE_PROMPT.format(
            title=source.title,
            subject=source.subject,
            content=source.cleaned_text,
        )

        response = await self.client.generate_json(
            prompt,
        )

        return response
