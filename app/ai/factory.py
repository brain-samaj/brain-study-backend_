from __future__ import annotations

import logging
from collections.abc import Sequence

from app.ai.base import AIProvider, AIProviderUnavailableError
from app.ai.providers.gemini import GeminiProvider
from app.ai.providers.groq import GroqProvider

logger = logging.getLogger(__name__)


class AIProviderFactory:
    """
    Enterprise AI Provider Factory.

    Provider priority:

        1. Groq
        2. Gemini

    The AIClient should never instantiate providers directly.
    It should always obtain them from this factory.
    """

    def __init__(self) -> None:
        self._providers: tuple[AIProvider, ...] = (
            GroqProvider(),
            GeminiProvider(),
        )

    @property
    def providers(self) -> Sequence[AIProvider]:
        return self._providers

    async def get_primary_provider(self) -> AIProvider:
        """
        Returns the first healthy provider.

        Raises:
            AIProviderUnavailableError
        """
        for provider in self._providers:
            try:
                healthy = await provider.health_check()

                if healthy:
                    logger.info(
                        "AI Provider selected: %s",
                        provider.name,
                    )
                    return provider

            except Exception:
                logger.exception(
                    "Health check failed for provider: %s",
                    provider.name,
                )

        raise AIProviderUnavailableError(
            "No AI provider is currently available."
        )

    async def get_provider_by_name(
        self,
        provider_name: str,
    ) -> AIProvider:
        """
        Retrieve a provider by name.

        Raises:
            AIProviderUnavailableError
        """
        provider_name = provider_name.lower()

        for provider in self._providers:
            if provider.name.lower() == provider_name:
                return provider

        raise AIProviderUnavailableError(
            f"Unknown AI provider: {provider_name}"
        )
