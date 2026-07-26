from __future__ import annotations

import json
import logging
import re
from typing import Any

from app.ai.base import (
    AIProviderError,
    AIProviderUnavailableError,
)

from app.ai.factory import AIProviderFactory


logger = logging.getLogger(__name__)


class AIClient:
    """
    Enterprise AI client.

    Responsibilities:
    - Hide provider implementation details.
    - Handle provider fallback.
    - Return parsed JSON safely.
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

        last_error: Exception | None = None

        for provider in self._factory.providers:

            try:
                healthy = await provider.health()

                if not healthy:
                    logger.warning(
                        "Skipping unhealthy provider: %s",
                        provider.name,
                    )
                    continue


                logger.info(
                    "Using AI provider: %s",
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
                    "Provider failed: %s",
                    provider.name,
                )


        if last_error:
            raise AIProviderUnavailableError(
                "All AI providers failed."
            ) from last_error


        raise AIProviderUnavailableError(
            "No AI providers available."
        )


    async def generate_json(
        self,
        *,
        prompt: str,
        system_prompt: str | None = None,
        temperature: float = 0.2,
        max_tokens: int = 4096,
    ) -> dict[str, Any]:

        raw = await self.generate(
            prompt=prompt,
            system_prompt=system_prompt,
            temperature=temperature,
            max_tokens=max_tokens,
            response_format={
                "type": "json_object",
            },
        )


        logger.info(
            "RAW AI RESPONSE: %r",
            raw,
        )


        cleaned = self._clean_json(raw)


        try:
            return json.loads(cleaned)


        except json.JSONDecodeError as exc:

            logger.exception(
                "AI returned invalid JSON after cleaning."
            )

            raise AIProviderError(
                f"Malformed AI JSON.\nRaw response: {raw!r}"
            ) from exc



    def _clean_json(
        self,
        text: str,
    ) -> str:

        """
        Remove markdown code fences from AI JSON.
        """

        text = text.strip()


        # Remove ```json ... ```
        text = re.sub(
            r"^```(?:json)?",
            "",
            text,
            flags=re.IGNORECASE,
        )

        text = re.sub(
            r"```$",
            "",
            text,
        )


        return text.strip()
