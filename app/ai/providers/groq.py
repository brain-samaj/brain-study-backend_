from __future__ import annotations

import json
import re
from collections.abc import Iterable
from typing import Any

from groq import AsyncGroq

from app.ai.providers.base import BaseAIProvider
from app.core.config import settings


class GroqProvider(BaseAIProvider):
    """
    Enterprise Groq Provider.

    Compatible with AIClient.
    """

    name = "Groq"

    MAX_PROMPT_CHARS = 16000

    def __init__(self) -> None:

        self.client = AsyncGroq(
            api_key=settings.GROQ_API_KEY,
        )

        self.model = settings.GROQ_MODEL

    # ==========================================================
    # INTERNAL
    # ==========================================================

    def _trim(
        self,
        prompt: str,
    ) -> str:

        if len(prompt) <= self.MAX_PROMPT_CHARS:
            return prompt

        return (
            prompt[: self.MAX_PROMPT_CHARS]
            + "\n\n[Content truncated.]"
        )

    # ==========================================================
    # HEALTH CHECK
    # ==========================================================

    async def health_check(
        self,
    ) -> bool:

        try:

            await self.generate(
                prompt="Reply ONLY with OK",
                max_tokens=5,
            )

            return True

        except Exception:

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
        max_tokens: int = 2048,
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
                "\nDo not wrap it inside markdown."
            )

        response = await self.client.chat.completions.create(
            model=self.model,
            temperature=temperature,
            max_tokens=max_tokens,
            messages=[
                {
                    "role": "system",
                    "content": system,
                },
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
        )

        return (
            response.choices[0]
            .message.content
            .strip()
        )

    # ==========================================================
    # JSON
    # ==========================================================

    async def generate_json(
        self,
        *,
        prompt: str,
        system_prompt: str | None = None,
        temperature: float = 0.2,
        max_tokens: int = 2048,
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
            text = text[start : end + 1]

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
