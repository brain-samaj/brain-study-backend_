from __future__ import annotations

import json
import re
from collections.abc import Iterable
from typing import Any

from google import genai

from app.ai.providers.base import BaseAIProvider
from app.core.config import settings


class GeminiProvider(BaseAIProvider):
    """
    Enterprise Gemini Provider.

    Compatible with AIClient.
    """

    name = "Gemini"

    MAX_PROMPT_CHARS = 16000

    def __init__(self) -> None:
        if not settings.GEMINI_API_KEY:
            raise ValueError(
                "GEMINI_API_KEY is missing."
            )

        self.client = genai.Client(
            api_key=settings.GEMINI_API_KEY,
        )

        self.model = settings.GEMINI_MODEL

    # ==========================================================
    # INTERNAL
    # ==========================================================

    def _trim(self, prompt: str) -> str:
        if len(prompt) <= self.MAX_PROMPT_CHARS:
            return prompt

        return (
            prompt[: self.MAX_PROMPT_CHARS]
            + "\n\n[Content truncated.]"
        )

    # ==========================================================
    # HEALTH CHECK
    # ==========================================================

    async def health(self) -> bool:
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
                "\nDo not wrap it inside markdown."
            )

        response = await self.client.aio.models.generate_content(
            model=self.model,
            contents=system + "\n\n" + prompt,
            config={
                "temperature": temperature,
                "max_output_tokens": max_tokens,
            },
        )

        if not response.text:
            raise ValueError(
                "Gemini returned empty response."
            )

        return response.text.strip()

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
            text = text[start : end + 1]

        try:
            return json.loads(text)
        except json.JSONDecodeError as exc:
            raise ValueError(
                f"Gemini returned invalid JSON:\n\n{text}"
            ) from exc

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
