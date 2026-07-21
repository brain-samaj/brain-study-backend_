from __future__ import annotations

from pydantic import BaseModel, Field


class Flashcard(BaseModel):
    front: str
    back: str
    category: str
    difficulty: str


class FlashcardDeck(BaseModel):
    title: str
    cards: list[Flashcard] = Field(default_factory=list)
