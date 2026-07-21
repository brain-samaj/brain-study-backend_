from __future__ import annotations

import json

from app.ai.client import AIClient


class FlashcardGenerator:

    def __init__(self):
        self.ai = AIClient()


    async def generate(
        self,
        *,
        subject: str,
        study_material: str,
        study_guide: str,
    ) -> dict:

        prompt = f"""
You are an expert university tutor.

Subject

{subject}

Study Material

{study_material}

Study Guide

{study_guide}

Generate intelligent flashcards.

Rules

Do NOT copy sentences directly.

Every flashcard must teach one important idea.

Mix different flashcard styles.

Types

Definition

Concept

Formula

Worked Example

Comparison

Cause and Effect

Advantages vs Disadvantages

Step-by-step Process

Memory Trick

Common Mistake

Application

Return JSON.

Each flashcard should contain

type

front

back

difficulty

topic

importance

Return ONLY JSON.
"""

        response = await self.ai.generate_json(prompt)

        return json.loads(response)

