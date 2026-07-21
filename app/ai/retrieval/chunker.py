from __future__ import annotations

import re
from dataclasses import dataclass


@dataclass(slots=True)
class TextChunk:
    """
    Represents one semantic chunk of a study material.
    """

    index: int
    text: str
    word_count: int
    start_word: int
    end_word: int


class SemanticChunker:
    """
    Production semantic chunker.

    Goals

    • Preserve paragraphs
    • Preserve headings
    • Avoid splitting equations
    • Keep related explanations together
    • Produce embedding-friendly chunks
    """

    def __init__(
        self,
        *,
        chunk_size: int = 700,
        overlap: int = 100,
    ):

        self.chunk_size = chunk_size
        self.overlap = overlap

    ############################################################
    # PARAGRAPH SPLITTING
    ############################################################

    def paragraphs(
        self,
        text: str,
    ) -> list[str]:

        paragraphs = re.split(
            r"\n\s*\n",
            text,
        )

        return [
            p.strip()
            for p in paragraphs
            if p.strip()
        ]

    ############################################################
    # WORD COUNT
    ############################################################

    def words(
        self,
        text: str,
    ) -> int:

        return len(
            text.split(),
        )

    ############################################################
    # BUILD CHUNKS
    ############################################################

    def chunk(
        self,
        text: str,
    ) -> list[TextChunk]:

        paragraphs = self.paragraphs(
            text,
        )

        chunks: list[TextChunk] = []

        current: list[str] = []

        current_words = 0

        start_word = 0

        chunk_index = 1

        for paragraph in paragraphs:

            paragraph_words = self.words(
                paragraph,
            )

            if (
                current
                and current_words + paragraph_words > self.chunk_size
            ):

                joined = "\n\n".join(
                    current,
                )

                chunks.append(
                    TextChunk(
                        index=chunk_index,
                        text=joined,
                        word_count=current_words,
                        start_word=start_word,
                        end_word=start_word + current_words,
                    )
                )

                overlap_words = joined.split()[-self.overlap :]

                current = [
                    " ".join(overlap_words),
                ]

                current_words = len(
                    overlap_words,
                )

                start_word += (
                    current_words
                    - len(overlap_words)
                )

                chunk_index += 1

            current.append(
                paragraph,
            )

            current_words += paragraph_words

        if current:

            joined = "\n\n".join(
                current,
            )

            chunks.append(
                TextChunk(
                    index=chunk_index,
                    text=joined,
                    word_count=current_words,
                    start_word=start_word,
                    end_word=start_word + current_words,
                )
            )

        return chunks
