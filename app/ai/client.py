from __future__ import annotations

import json
import logging
from typing import Any

from app.ai.base import AIProviderError, AIProviderUnavailableError
from app.ai.factory import AIProviderFactory

logger = logging.getLogger(__name__)


class AIClient:
    """
    Enterprise AI client.

    Responsibilities
    ----------------
    - Hide provider implementation details.
    - Select the primary provider through AIProviderFactory.
    - Automatically fall back to the next provider on failure.
    - Return only parsed data to application services.
    """

    def __init__(
        self,
        factory: AIProviderFactory | None = None,
    ) -> None:
        self._factory = factory or AIProviderFactory()

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
        Generate text using the first available provider.
        """

        last_error: Exception | None = None

        for provider in self._factory.providers:
            try:
                healthy = await provider.health_check()

                if not healthy:
                    logger.warning(
                        "Skipping unhealthy AI provider: %s",
                        provider.name,
                    )
                    continue

                logger.info(
                    "Generating response with provider: %s",
                    provider.name,
                )

                return await provider.generate(
                    prompt=prompt,
                    system_prompt=system_prompt,
                    temperature=temperature,
                    max_tokens=max_tokens,
                    response_format=response_format,
                )

            except Exception as exc:
                last_error = exc

                logger.exception(
                    "Provider '%s' failed. Trying next provider.",
                    provider.name,
                )

        if last_error:
            raise AIProviderUnavailableError(
                "All AI providers failed."
            ) from last_error

        raise AIProviderUnavailableError(
            "No AI providers are available."
        )

    async def generate_json(
        self,
        *,
        prompt: str,
        system_prompt: str | None = None,
        temperature: float = 0.2,
        max_tokens: int = 4096,
    ) -> dict[str, Any]:
        """
        Generate structured JSON.
        """

        raw = await self.generate(
            prompt=prompt,
            system_prompt=system_prompt,
            temperature=temperature,
            max_tokens=max_tokens,
            response_format={
                "type": "json_object",
            },
        )

        try:
            return json.loads(raw)

        except json.JSONDecodeError as exc:
            logger.exception(
                "AI returned invalid JSON."
            )
            raise AIProviderError(
                "AI provider returned malformed JSON."
            ) from exc
