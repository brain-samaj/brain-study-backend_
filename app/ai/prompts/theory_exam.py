from __future__ import annotations


class TheoryExamPromptBuilder:

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
You are an experienced university examination setter.

Generate a professional THEORY examination.

Rules

- Return ONLY valid JSON.
- No markdown.
- No explanations outside JSON.
- Questions must require reasoning.
- Include define, explain, compare, discuss, evaluate, calculate and analyze questions.
- Cover the entire study material.
- Questions should progressively increase in difficulty.

JSON FORMAT

[
  {{
    "question":"",
    "mark":10,
    "difficulty":"medium",
    "expected_points":[
      "",
      "",
      ""
    ],
    "sample_answer":""
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
