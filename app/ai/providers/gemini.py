from __future__ import annotations

import json
import re
from typing import Iterable

from google import genai

from app.ai.providers.base import BaseAIProvider
from app.core.config import settings


class GeminiProvider(BaseAIProvider):

    def __init__(self) -> None:

        if not settings.GEMINI_API_KEY:
            raise ValueError(
                "GEMINI_API_KEY is missing"
            )

        self.client = genai.Client(
            api_key=settings.GEMINI_API_KEY,
        )

        self.model = settings.GEMINI_MODEL


    async def generate(
        self,
        *,
        prompt: str,
        temperature: float = 0.2,
        max_tokens: int = 4096,
    ) -> str:


        response = await self.client.aio.models.generate_content(
            model=self.model,
            contents=prompt,
            config={
                "temperature": temperature,
                "max_output_tokens": max_tokens,
            },
        )


        return response.text.strip()



    async def generate_json(
        self,
        *,
        prompt: str,
        temperature: float = 0.2,
    ) -> dict:


        prompt = (
            prompt
            + "\n\n"
            + "IMPORTANT:\n"
            + "Return ONLY valid JSON.\n"
            + "Do NOT use markdown.\n"
            + "Do NOT explain anything.\n"
            + "Output must begin with '{' and end with '}'."
        )


        result = await self.generate(
            prompt=prompt,
            temperature=temperature,
        )


        result = result.strip()


        result = re.sub(
            r"^```(?:json)?",
            "",
            result,
            flags=re.IGNORECASE,
        )


        result = re.sub(
            r"```$",
            "",
            result,
        ).strip()


        start = result.find("{")
        end = result.rfind("}")


        if start != -1 and end != -1:

            result = result[start:end + 1]


        try:

            return json.loads(result)


        except json.JSONDecodeError as exc:

            raise ValueError(
                f"Gemini returned invalid JSON:\n\n{result}"
            ) from exc



    async def embeddings(
        self,
        texts: Iterable[str],
    ) -> list[list[float]]:

        raise NotImplementedError(
            "Gemini embeddings not implemented yet."
        )



    async def health(
        self,
    ) -> bool:

        try:

            result = await self.generate(
                prompt="Reply with OK",
                max_tokens=5,
            )

            return result == "OK" or bool(result)


        except Exception:

            return False
