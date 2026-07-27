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
    Enterprise AI Client.

    Responsibilities
    ----------------
    - Hide provider implementations.
    - Automatically use Groq then Gemini.
    - Retry providers on failure.
    - Return clean text or JSON.
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
                    "Using provider: %s",
                    provider.name,
                )

                response = await provider.generate(
                    prompt=prompt,
                    system_prompt=system_prompt,
                    temperature=temperature,
                    max_tokens=max_tokens,
                    response_format=response_format,
                )

                if response and str(response).strip():
                    return str(response)

            except Exception as exc:
                last_error = exc

                logger.exception(
                    "Provider %s failed.",
                    provider.name,
                )

        if last_error is not None:
            raise AIProviderUnavailableError(
                "All AI providers failed."
            ) from last_error

        raise AIProviderUnavailableError(
            "No AI provider available."
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

        cleaned = self._extract_json(raw)

        try:
            return json.loads(cleaned)

        except Exception as exc:

            logger.exception(
                "Invalid JSON returned by AI."
            )

            raise AIProviderError(
                f"AI returned invalid JSON.\n\n{raw}"
            ) from exc

    def _extract_json(
        self,
        text: str,
    ) -> str:

        text = text.strip()

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

        text = text.strip()

        start = text.find("{")
        end = text.rfind("}")

        if start != -1 and end != -1:
            return text[start:end + 1]

        return text
