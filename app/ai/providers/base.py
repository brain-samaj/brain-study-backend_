from __future__ import annotations

from abc import ABC
from abc import abstractmethod


class AIProvider(ABC):
    """
    Base class for every AI provider.

    Every provider must implement these methods.
    """

    @abstractmethod
    async def generate(
        self,
        prompt: str,
        *,
        temperature: float = 0.2,
        model: str | None = None,
    ) -> str:
        ...

    @abstractmethod
    async def generate_json(
        self,
        prompt: str,
        *,
        temperature: float = 0.2,
        model: str | None = None,
    ) -> dict:
        ...

    @abstractmethod
    async def health_check(
        self,
    ) -> bool:
        ...
