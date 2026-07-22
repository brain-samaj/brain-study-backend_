from __future__ import annotations

import re
from dataclasses import dataclass


@dataclass(slots=True)
class DocumentChunk:

    id: int

    text: str

    words: int

    characters: int


class SemanticChunker:
    """
    Splits cleaned documents into
    overlapping semantic chunks.

    Optimized for:

    • Study Guide
    • Smart Study
    • Flashcards
    • Practice Exam
    """

    def __init__(
        self,
        *,
        chunk_size: int = 700,
        overlap: int = 120,
    ):

        self.chunk_size = chunk_size
        self.overlap = overlap

    def chunk(
        self,
        text: str,
    ) -> list[DocumentChunk]:

        paragraphs = [
            p.strip()
            for p in re.split(r"\n{2,}", text)
            if p.strip()
        ]

        chunks: list[DocumentChunk] = []

        current = ""
        chunk_id = 1

        for paragraph in paragraphs:

            if len(current) + len(paragraph) < self.chunk_size:

                current += "\n\n" + paragraph

                continue

            current = current.strip()

            if current:

                chunks.append(
                    DocumentChunk(
                        id=chunk_id,
                        text=current,
                        words=len(current.split()),
                        characters=len(current),
                    )
                )

                chunk_id += 1

            overlap_text = ""

            if self.overlap:

                words = current.split()

                overlap_text = " ".join(
                    words[-self.overlap:]
                )

            current = overlap_text + "\n\n" + paragraph

        current = current.strip()

        if current:

            chunks.append(
                DocumentChunk(
                    id=chunk_id,
                    text=current,
                    words=len(current.split()),
                    characters=len(current),
                )
            )

        return chunks
