from __future__ import annotations

import json
import logging
import re
from collections.abc import Iterable
from typing import Any

from groq import AsyncGroq

from app.ai.providers.base import BaseAIProvider
from app.core.config import settings

logger = logging.getLogger(__name__)


class GroqProvider(BaseAIProvider):
    """
    Enterprise Groq Provider.
    """

    name = "Groq"

    MAX_PROMPT_CHARS = 16000

    def __init__(self) -> None:
        if not settings.GROQ_API_KEY:
            raise ValueError("GROQ_API_KEY is missing.")

        self.client = AsyncGroq(
            api_key=settings.GROQ_API_KEY,
        )

        self.model = settings.GROQ_MODEL

    # ==========================================================
    # INTERNAL
    # ==========================================================

    def _trim(self, prompt: str) -> str:
        if len(prompt) <= self.MAX_PROMPT_CHARS:
            return prompt

        return prompt[: self.MAX_PROMPT_CHARS] + "\n\n[Content truncated.]"

    # ==========================================================
    # HEALTH
    # ==========================================================

    async def health(self) -> bool:
        try:
            await self.generate(
                prompt="Reply ONLY with OK",
                max_tokens=5,
            )
            return True
        except Exception:
            logger.exception("Groq health check failed.")
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
                "Always follow the requested JSON schema exactly.\n"
                "Never omit required fields.\n"
                "Never wrap JSON in markdown."
            )
        )

        kwargs: dict[str, Any] = {
            "model": self.model,
            "messages": [
                {
                    "role": "system",
                    "content": system,
                },
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
            "temperature": temperature,
            "max_tokens": max_tokens,
        }

        if response_format is not None:
            kwargs["response_format"] = response_format

        response = await self.client.chat.completions.create(**kwargs)

        content = response.choices[0].message.content or ""

        logger.info("RAW GROQ RESPONSE:\n%s", content)

        return content.strip()

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

        logger.info("CLEANED GROQ JSON:\n%s", text)

        return json.loads(text)

    # ==========================================================
    # EMBEDDINGS
    # ==========================================================

    async def embeddings(
        self,
        texts: Iterable[str],
    ) -> list[list[float]]:
        raise NotImplementedError(
            "Groq does not provide embeddings."
        )
