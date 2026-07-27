from __future__ import annotations

import json
import logging
import re
import traceback
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
    - Automatically use configured providers.
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
                logger.info("=" * 80)
                logger.info("Checking provider: %s", provider.name)
                logger.info("=" * 80)

                healthy = await provider.health()

                logger.info(
                    "Health check for %s: %s",
                    provider.name,
                    healthy,
                )

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
                    logger.info(
                        "Provider %s generated %d characters.",
                        provider.name,
                        len(response),
                    )
                    return str(response)

                logger.warning(
                    "Provider %s returned an empty response.",
                    provider.name,
                )

            except Exception as exc:
                last_error = exc

                logger.exception(
                    "Provider %s failed.",
                    provider.name,
                )

                print("=" * 80)
                print(f"PROVIDER FAILURE: {provider.name}")
                traceback.print_exc()
                print("=" * 80)

        if last_error is not None:
            print("=" * 80)
            print("LAST AI ERROR")
            traceback.print_exception(
                type(last_error),
                last_error,
                last_error.__traceback__,
            )
            print("=" * 80)

            raise AIProviderUnavailableError(
                f"All AI providers failed. Last error: {repr(last_error)}"
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

        logger.info("=" * 80)
        logger.info("RAW AI RESPONSE")
        logger.info("=" * 80)
        logger.info(raw)
        logger.info("=" * 80)

        cleaned = self._extract_json(raw)

        logger.info("=" * 80)
        logger.info("CLEANED JSON")
        logger.info("=" * 80)
        logger.info(cleaned)
        logger.info("=" * 80)

        try:
            payload = json.loads(cleaned)

            logger.info("=" * 80)
            logger.info("PARSED JSON PAYLOAD")
            logger.info("=" * 80)
            logger.info(
                json.dumps(
                    payload,
                    indent=2,
                    ensure_ascii=False,
                )
            )
            logger.info("=" * 80)

            return payload

        except Exception as exc:
            logger.exception(
                "Invalid JSON returned by AI."
            )

            logger.error(
                "RAW RESPONSE:\n%s",
                raw,
            )

            logger.error(
                "CLEANED RESPONSE:\n%s",
                cleaned,
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
            return text[start : end + 1]

        return text
