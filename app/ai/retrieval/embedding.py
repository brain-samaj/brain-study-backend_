from __future__ import annotations

from dataclasses import dataclass

from app.ai.client import AIClient


@dataclass(slots=True)
class EmbeddingVector:
    """
    Represents one embedding and its source chunk.
    """

    chunk_index: int

    text: str

    vector: list[float]


class EmbeddingService:
    """
    Converts semantic chunks into vector embeddings.

    These vectors are stored in the vector database and
    later used for semantic retrieval.
    """

    def __init__(self):

        self.client = AIClient()

    async def embed_text(
        self,
        text: str,
    ) -> list[float]:

        return await self.client.create_embedding(
            text=text,
        )

    async def embed_chunks(
        self,
        chunks,
    ) -> list[EmbeddingVector]:

        vectors: list[EmbeddingVector] = []

        for chunk in chunks:

            embedding = await self.embed_text(
                chunk.text,
            )

            vectors.append(
                EmbeddingVector(
                    chunk_index=chunk.index,
                    text=chunk.text,
                    vector=embedding,
                )
            )

        return vectors
