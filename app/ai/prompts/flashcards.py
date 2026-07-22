from __future__ import annotations


class FlashcardPromptBuilder:

    @staticmethod
    def build(
        *,
        subject: str,
        topic: str,
        content: str,
    ) -> str:

        return f"""
You are one of the world's best teachers.

Generate high-quality flashcards from the study material.

Rules

- Return ONLY valid JSON.
- Do not include markdown.
- Generate between 25 and 60 flashcards.
- Cover ALL important concepts.
- Mix definitions, facts, formulas, concepts and applications.
- Questions must be concise.
- Answers must be clear and educational.
- Avoid duplicates.

JSON FORMAT

[
  {{
    "question": "",
    "answer": "",
    "difficulty": "easy"
  }}
]

Subject:
{subject}

Topic:
{topic}

Material:

{content}
"""
