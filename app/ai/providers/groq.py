from __future__ import annotations

import asyncio
import json

from groq import Groq

from app.ai.providers.base import AIProvider
from app.core.config import settings


class GroqProvider(AIProvider):

    def __init__(self):

        self.client = Groq(
            api_key=settings.GROQ_API_KEY,
        )

        self.model = settings.GROQ_MODEL

    def _completion(
        self,
        *,
        prompt: str,
        temperature: float,
        model: str,
        json_mode: bool,
    ):

        kwargs = {
            "model": model,
            "temperature": temperature,
            "messages": [
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
        }

        if json_mode:

            kwargs["response_format"] = {
                "type": "json_object",
            }

        return self.client.chat.completions.create(
            **kwargs,
        )

    async def generate(
        self,
        prompt: str,
        *,
        temperature: float = 0.2,
        model: str | None = None,
    ) -> str:

        response = await asyncio.to_thread(
            self._completion,
            prompt=prompt,
            temperature=temperature,
            model=model or self.model,
            json_mode=False,
        )

        return response.choices[0].message.content or ""

    async def generate_json(
        self,
        prompt: str,
        *,
        temperature: float = 0.2,
        model: str | None = None,
    ) -> dict:

        response = await asyncio.to_thread(
            self._completion,
            prompt=prompt,
            temperature=temperature,
            model=model or self.model,
            json_mode=True,
        )

        content = response.choices[0].message.content or "{}"

        return json.loads(content)

    async def health_check(
        self,
    ) -> bool:

        try:

            reply = await self.generate(
                "Reply ONLY with OK.",
            )

            return reply.strip().upper() == "OK"

        except Exception:

            return False
