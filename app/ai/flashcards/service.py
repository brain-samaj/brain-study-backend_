from __future__ import annotations

import json

from app.ai.client import AIClient
from app.ai.flashcards.models import FlashcardDeck
from app.ai.prompts.flashcards import build_prompt


class FlashcardService:

    def __init__(self):

        self.ai = AIClient()

    def generate(
        self,
        analysis,
        material,
    ) -> FlashcardDeck:

        prompt = build_prompt(
            analysis,
            material,
        )

        response = self.ai.chat(prompt)

        return FlashcardDeck.model_validate(
            json.loads(response)
        )
