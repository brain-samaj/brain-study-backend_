from __future__ import annotations

import json

from groq import AsyncGroq

from app.core.config import settings


class AIClient:

    def __init__(self):

        self.client = AsyncGroq(
            api_key=settings.GROQ_API_KEY,
        )

        self.model = settings.GROQ_MODEL

    async def generate(
        self,
        prompt: str,
    ) -> str:

        response = await self.client.chat.completions.create(
            model=self.model,
            temperature=0.2,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are Brain Study AI, an elite educational AI."
                    ),
                },
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
        )

        return response.choices[0].message.content.strip()

    async def generate_json(
        self,
        prompt: str,
    ):

        text = await self.generate(prompt)

        text = text.strip()

        if text.startswith("```json"):
            text = text[7:]

        if text.startswith("```"):
            text = text[3:]

        if text.endswith("```"):
            text = text[:-3]

        return json.loads(text.strip())
