from __future__ import annotations

from functools import lru_cache

from app.ai.providers.base import BaseAIProvider
from app.ai.providers.factory import get_ai_provider


@lru_cache(maxsize=1)
def get_provider() -> BaseAIProvider:
    """
    Returns the configured AI provider.

    Uses the automatic primary/fallback system.
    """

    return get_ai_provider()



class AIClient:
    """
    Central AI interface used by Brain Study.

    All AI features communicate through this class.
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
