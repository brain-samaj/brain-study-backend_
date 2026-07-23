from __future__ import annotations

from app.ai.providers.base import BaseAIProvider
from app.ai.providers.groq import GroqProvider
from app.ai.providers.gemini import GeminiProvider

from app.core.config import settings



class FallbackAIProvider(BaseAIProvider):
    """
    Automatically switches between AI providers.

    Primary provider is tried first.
    If it fails, fallback provider is used.
    """


    def __init__(
        self,
        primary: BaseAIProvider,
        fallback: BaseAIProvider,
    ) -> None:

        self.primary = primary
        self.fallback = fallback



    async def generate(
        self,
        *,
        prompt: str,
        temperature: float = 0.2,
        max_tokens: int = 4096,
    ) -> str:


        try:

            return await self.primary.generate(
                prompt=prompt,
                temperature=temperature,
                max_tokens=max_tokens,
            )


        except Exception as primary_error:

            print(
                "Primary AI failed:",
                primary_error,
            )


            return await self.fallback.generate(
                prompt=prompt,
                temperature=temperature,
                max_tokens=max_tokens,
            )



    async def generate_json(
        self,
        *,
        prompt: str,
        temperature: float = 0.2,
    ) -> dict:


        try:

            return await self.primary.generate_json(
                prompt=prompt,
                temperature=temperature,
            )


        except Exception as primary_error:

            print(
                "Primary AI JSON failed:",
                primary_error,
            )


            return await self.fallback.generate_json(
                prompt=prompt,
                temperature=temperature,
            )



    async def embeddings(
        self,
        texts,
    ):

        return await self.primary.embeddings(
            texts
        )



    async def health(
        self,
    ) -> bool:

        primary_health = await self.primary.health()

        if primary_health:
            return True


        return await self.fallback.health()



def create_provider(
    name: str,
) -> BaseAIProvider:


    name = name.lower().strip()


    if name == "gemini":

        return GeminiProvider()



    if name == "groq":

        return GroqProvider()



    raise ValueError(
        f"Unsupported AI provider: {name}"
    )



def get_ai_provider() -> BaseAIProvider:


    primary = create_provider(
        settings.PRIMARY_AI_PROVIDER
    )


    fallback = create_provider(
        settings.FALLBACK_AI_PROVIDER
    )


    return FallbackAIProvider(
        primary=primary,
        fallback=fallback,
    )
