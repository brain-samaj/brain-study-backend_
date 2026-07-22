from __future__ import annotations

from abc import ABC
from abc import abstractmethod
from typing import Iterable


class BaseAIProvider(ABC):
    """
    Abstract interface implemented by every LLM provider.

    Examples:

    - Groq
    - OpenAI
    - Anthropic
    - Local models
    """

    @abstractmethod
    async def generate(
        self,
        *,
        prompt: str,
        temperature: float = 0.2,
        max_tokens: int = 4096,
    ) -> str:
        """
        Generate a completion.
        """
        raise NotImplementedError

    @abstractmethod
    async def generate_json(
        self,
        *,
        prompt: str,
        temperature: float = 0.2,
    ) -> dict:
        """
        Generate structured JSON.
        """
        raise NotImplementedError

    @abstractmethod
    async def embeddings(
        self,
        texts: Iterable[str],
    ) -> list[list[float]]:
        """
        Generate embeddings.

        Providers that don't support embeddings
        should raise NotImplementedError.
        """
        raise NotImplementedError

    @abstractmethod
    async def health(self) -> bool:
        """
        Provider health check.
        """
        raise NotImplementedError
