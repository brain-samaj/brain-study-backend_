from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class AIProviderError(Exception):
    """Base exception for AI provider failures."""


class AIProviderUnavailableError(AIProviderError):
    """Raised when a provider cannot process a request."""


class AIProvider(ABC):
    """
    Base interface implemented by every AI provider.

    The AIClient depends only on this interface and is unaware of
    Groq, Gemini, or any future provider implementation.
    """

    @property
    @abstractmethod
    def name(self) -> str:
        """Human-readable provider name."""

    @abstractmethod
    async def generate(
        self,
        *,
        prompt: str,
        system_prompt: str | None = None,
        temperature: float = 0.2,
        max_tokens: int = 4096,
        response_format: dict[str, Any] | None = None,
    ) -> str:
        """
        Generate a completion.

        Args:
            prompt:
                User prompt.

            system_prompt:
                Optional system instruction.

            temperature:
                Sampling temperature.

            max_tokens:
                Maximum output tokens.

            response_format:
                Provider-specific response format (for example,
                JSON schema or JSON object mode).

        Returns:
            Raw text returned by the provider.

        Raises:
            AIProviderError:
                If generation fails.
        """
        raise NotImplementedError

    @abstractmethod
    async def health_check(self) -> bool:
        """
        Verify whether the provider is currently available.

        Returns:
            True if healthy.
        """
        raise NotImplementedError
