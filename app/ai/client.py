from __future__ import annotations

from groq import Groq

from app.core.config import settings


class AIClient:
    def __init__(self) -> None:
        self.client = Groq(
            api_key=settings.GROQ_API_KEY,
        )
        self.model = settings.GROQ_MODEL

    async def generate(
        self,
        prompt: str,
    ) -> str:

        response = self.client.chat.completions.create(
            model=self.model,
            temperature=0.2,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
        )

        return response.choices[0].message.content or ""

    async def generate_json(
        self,
        prompt: str,
    ) -> str:

        response = self.client.chat.completions.create(
            model=self.model,
            temperature=0.2,
            response_format={"type": "json_object"},
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
        )

        return response.choices[0].message.content or ""
