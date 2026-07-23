from __future__ import annotations

import json
import re
from typing import Iterable

from groq import AsyncGroq

from app.ai.providers.base import BaseAIProvider
from app.core.config import settings


class GroqProvider(BaseAIProvider):

    # Groq TPM limit is 12000 for your current tier.
    # Keep a safety margin.
    MAX_PROMPT_CHARS = 30000

    def __init__(self) -> None:

        self.client = AsyncGroq(
            api_key=settings.GROQ_API_KEY,
        )

        self.model = settings.GROQ_MODEL


    def trim_prompt(
        self,
        prompt: str,
    ) -> str:

        if len(prompt) <= self.MAX_PROMPT_CHARS:
            return prompt

        return (
            prompt[:self.MAX_PROMPT_CHARS]
            +
            "\n\n[Content shortened because it exceeded AI processing limit.]"
        )


    async def generate(
        self,
        *,
        prompt: str,
        temperature: float = 0.2,
        max_tokens: int = 4096,
    ) -> str:


        prompt = self.trim_prompt(
            prompt
        )


        response = await self.client.chat.completions.create(

            model=self.model,

            temperature=temperature,

            max_tokens=max_tokens,

            messages=[

                {
                    "role": "system",

                    "content": (
                        "You are Brain Study's educational engine.\n"
                        "Generate clear educational content.\n"
                        "Follow instructions exactly.\n"
                        "Never wrap JSON inside markdown unless requested."
                    ),
                },

                {
                    "role": "user",
                    "content": prompt,
                },

            ],

        )


        return (
            response
            .choices[0]
            .message
            .content
            .strip()
        )



    async def generate_json(
        self,
        *,
        prompt: str,
        temperature: float = 0.2,
    ) -> dict:


        prompt = self.trim_prompt(
            prompt
        )


        prompt = (
            prompt
            + "\n\n"
            + "IMPORTANT:\n"
            + "Return ONLY valid JSON.\n"
            + "Do NOT use markdown.\n"
            + "Do NOT use ```json.\n"
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
                f"Groq returned invalid JSON:\n\n{result}"
            ) from exc



    async def embeddings(
        self,
        texts: Iterable[str],
    ) -> list[list[float]]:

        raise NotImplementedError(
            "Groq currently does not provide embeddings."
        )



    async def health(
        self,
    ) -> bool:

        try:

            await self.generate(
                prompt="Reply with OK",
                max_tokens=5,
            )

            return True


        except Exception:

            return False
