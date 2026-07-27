from __future__ import annotations

import json
import logging
import re
import traceback
from collections.abc import Iterable
from typing import Any

from google import genai

from app.ai.providers.base import BaseAIProvider
from app.core.config import settings

logger = logging.getLogger(__name__)


class GeminiProvider(BaseAIProvider):
    """
    Enterprise Gemini Provider.

    Compatible with AIClient.
    """

    name = "Gemini"

    MAX_PROMPT_CHARS = 16000

    def __init__(self) -> None:
        if not settings.GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY is missing.")

        self.client = genai.Client(
            api_key=settings.GEMINI_API_KEY,
        )

        self.model = settings.GEMINI_MODEL

        logger.info("=" * 80)
        logger.info("Gemini Provider Initialized")
        logger.info("Model: %s", self.model)
        logger.info(
            "API Key Prefix: %s",
            settings.GEMINI_API_KEY[:5],
        )
        logger.info("=" * 80)

    # ==========================================================
    # INTERNAL
    # ==========================================================

    def _trim(self, prompt: str) -> str:
        if len(prompt) <= self.MAX_PROMPT_CHARS:
            return prompt

        logger.warning(
            "Prompt exceeded %d characters. Truncating.",
            self.MAX_PROMPT_CHARS,
        )

        return (
            prompt[: self.MAX_PROMPT_CHARS]
            + "\n\n[Content truncated.]"
        )

    # ==========================================================
    # HEALTH CHECK
    # ==========================================================

    async def health(self) -> bool:
        try:
            logger.info("=" * 80)
            logger.info("Running Gemini health check...")
            logger.info("Model: %s", self.model)

            response = await self.generate(
                prompt="Reply ONLY with OK",
                max_tokens=5,
            )

            logger.info(
                "Gemini health response: %s",
                response,
            )

            return bool(response and response.strip())

        except Exception:
            logger.exception("Gemini health check FAILED")

            print("=" * 80)
            print("GEMINI HEALTH CHECK FAILED")
            traceback.print_exc()
            print("=" * 80)

            return False

    # ==========================================================
    # GENERATE
    # ==========================================================

    async def generate(
        self,
        *,
        prompt: str,
        system_prompt: str | None = None,
        temperature: float = 0.2,
        max_tokens: int = 4096,
        response_format: dict[str, Any] | None = None,
    ) -> str:

        prompt = self._trim(prompt)

        system = (
            system_prompt
            or (
                "You are Brain Study's AI engine.\n"
                "Generate accurate educational content.\n"
                "Follow every instruction exactly."
            )
        )

        if response_format:
            system += (
                "\n\nReturn ONLY valid JSON."
                "\nDo not wrap it in markdown."
                "\nDo not add explanations."
            )

        config: dict[str, Any] = {
            "temperature": temperature,
            "max_output_tokens": max_tokens,
        }

        if response_format:
            config["response_mime_type"] = "application/json"

        try:
            logger.info("=" * 80)
            logger.info("Sending request to Gemini")
            logger.info("Model: %s", self.model)
            logger.info("Temperature: %s", temperature)
            logger.info("Max Tokens: %s", max_tokens)
            logger.info("=" * 80)

            response = await self.client.aio.models.generate_content(
                model=self.model,
                contents=f"{system}\n\n{prompt}",
                config=config,
            )

            logger.info("=" * 80)
            logger.info("Gemini raw response object:")
            logger.info(repr(response))
            logger.info("=" * 80)

            text = getattr(response, "text", None)

            if not text:
                logger.error("Gemini returned an empty text field.")
                logger.error("Response object: %r", response)

                raise ValueError(
                    "Gemini returned empty response."
                )

            logger.info("=" * 80)
            logger.info("Gemini TEXT:")
            logger.info(text)
            logger.info("=" * 80)

            return text.strip()

        except Exception:
            logger.exception("Gemini generate() FAILED")

            print("=" * 80)
            print("GEMINI GENERATE FAILED")
            traceback.print_exc()
            print("=" * 80)

            raise

    # ==========================================================
    # JSON
    # ==========================================================

    async def generate_json(
        self,
        *,
        prompt: str,
        system_prompt: str | None = None,
        temperature: float = 0.2,
        max_tokens: int = 4096,
    ) -> dict[str, Any]:

        text = await self.generate(
            prompt=prompt,
            system_prompt=system_prompt,
            temperature=temperature,
            max_tokens=max_tokens,
            response_format={
                "type": "json_object",
            },
        )

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
        ).strip()

        start = text.find("{")
        end = text.rfind("}")

        if start != -1 and end != -1:
            text = text[start:end + 1]

        logger.info("=" * 80)
        logger.info("Gemini cleaned JSON:")
        logger.info(text)
        logger.info("=" * 80)

        try:
            payload = json.loads(text)

            logger.info("=" * 80)
            logger.info("Gemini parsed JSON successfully.")
            logger.info("=" * 80)

            return payload

        except json.JSONDecodeError:
            logger.exception("Gemini JSON parsing FAILED")

            print("=" * 80)
            print("INVALID GEMINI JSON")
            print(text)
            print("=" * 80)

            raise ValueError(
                f"Gemini returned invalid JSON:\n\n{text}"
            )

    # ==========================================================
    # EMBEDDINGS
    # ==========================================================

    async def embeddings(
        self,
        texts: Iterable[str],
    ) -> list[list[float]]:
        raise NotImplementedError(
            "Gemini embeddings are not implemented."
        )
