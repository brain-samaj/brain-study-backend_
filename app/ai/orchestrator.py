from __future__ import annotations

import json

from app.ai.client import AIClient


class AIOrchestrator:
    """
    Central AI gateway.

    Every AI feature in Brain Study
    should go through this class.

    Features

    • Study Guide
    • Smart Study
    • Flashcards
    • Exam Generation
    • Theory Marking
    • Objective Marking
    • Summaries
    """

    def __init__(self):

        self.ai = AIClient()

    async def generate_json(
        self,
        prompt: str,
    ) -> dict:

        response = await self.ai.generate_json(
            prompt,
        )

        if isinstance(response, dict):
            return response

        return json.loads(response)

    async def generate_text(
        self,
        prompt: str,
    ) -> str:

        return await self.ai.generate(
            prompt,
        )
