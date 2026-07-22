from __future__ import annotations

import json
from typing import Iterable

from groq import AsyncGroq

from app.ai.providers.base import BaseAIProvider
from app.core.config import settings


class GroqProvider(BaseAIProvider):

    def __init__(self) -> None:
        self.client = AsyncGroq(
            api_key=settings.GROQ_API_KEY,
        )

        self.model = settings.GROQ_MODEL

    async def generate(
        self,
        *,
        prompt: str,
        temperature: float = 0.2,
        max_tokens: int = 4096,
    ) -> str:

        response = await self.client.chat.completions.create(
            model=self.model,
            temperature=temperature,
            max_tokens=max_tokens,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are Brain Study's educational engine. "
                        "Produce accurate, structured, educational responses."
                    ),
                },
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
        )

        return (
            response
            .choices[0]
            .message.content
            .strip()
        )

    async def generate_json(
        self,
        *,
        prompt: str,
        temperature: float = 0.2,
    ) -> dict:

        result = await self.generate(
            prompt=(
                prompt
                + "\n\n"
                + "Return ONLY valid JSON."
            ),
            temperature=temperature,
        )

        return json.loads(result)

    async def embeddings(
        self,
        texts: Iterable[str],
    ) -> list[list[float]]:
        raise NotImplementedError(
            "Groq currently does not provide embeddings."
        )

    async def health(
        self,
    ) -> bool:

        try:

            await self.generate(
                prompt="Reply with OK",
                max_tokens=5,
            )

            return True

        except Exception:

            return False
