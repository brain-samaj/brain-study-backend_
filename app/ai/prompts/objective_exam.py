from __future__ import annotations


class ObjectiveExamPromptBuilder:

    @staticmethod
    def build(
        *,
        subject: str,
        topic: str,
        difficulty: str,
        question_count: int,
        content: str,
    ) -> str:

        return f"""
You are an elite examination setter.

Create a professional objective examination.

Rules

- Return ONLY valid JSON.
- No markdown.
- No explanations outside JSON.
- Every question must have exactly four options.
- Only one correct answer.
- Questions must test understanding, not memorization.
- Include easy, medium and hard questions.
- Base everything on the supplied material.

JSON FORMAT

[
  {{
    "question":"",
    "options":[
      "",
      "",
      "",
      ""
    ],
    "correct_answer":"",
    "explanation":"",
    "difficulty":"medium"
  }}
]

Subject:
{subject}

Topic:
{topic}

Difficulty:
{difficulty}

Questions:
{question_count}

Material

{content}
"""
