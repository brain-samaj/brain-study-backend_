from __future__ import annotations

from functools import lru_cache

from app.ai.providers.base import BaseAIProvider
from app.ai.providers.groq import GroqProvider


@lru_cache(maxsize=1)
def get_provider() -> BaseAIProvider:
    """
    Returns the configured language model provider.

    Using a singleton avoids recreating the HTTP client
    for every request.
    """
    return GroqProvider()


class AIClient:
    """
    High-level interface used throughout the backend.

    Study Guide
    Smart Study
    Flashcards
    Practice Exam

    All communicate through this class rather than
    talking directly to the provider.
    """

    def __init__(
        self,
        provider: BaseAIProvider | None = None,
    ) -> None:

        self.provider = provider or get_provider()

    async def generate(
        self,
        *,
        prompt: str,
        temperature: float = 0.2,
        max_tokens: int = 4096,
    ) -> str:

        return await self.provider.generate(
            prompt=prompt,
            temperature=temperature,
            max_tokens=max_tokens,
        )

    async def generate_json(
        self,
        *,
        prompt: str,
        temperature: float = 0.2,
    ) -> dict:

        return await self.provider.generate_json(
            prompt=prompt,
            temperature=temperature,
        )

    async def health(self) -> bool:
        return await self.provider.health()
